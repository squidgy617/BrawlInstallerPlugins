# PatchLib
# Library for BrawlInstaller's patching plugins

from BrawlInstallerLib import *
from System import Type
from System import Activator
clr.AddReference("System.Web")
from System.Web import HttpUtility
from System import Text
from System.Text import Encoding
from System import Convert

TEMP_PATH = AppPath + '/temp'
CONTAINERS = [ 
	"BrawlLib.SSBB.ResourceNodes.ARCNode", 
	"BrawlLib.SSBB.ResourceNodes.BRRESNode", 
	"BrawlLib.SSBB.ResourceNodes.BLOCNode", 
	"BrawlLib.SSBB.ResourceNodes.BRESGroupNode",
	"BrawlLib.SSBB.ResourceNodes.TyDataNode",
	"BrawlLib.SSBB.ResourceNodes.TyDataListNode",
	"BrawlLib.SSBB.ResourceNodes.GDORNode",
	"BrawlLib.SSBB.ResourceNodes.GDBFNode",
	"BrawlLib.SSBB.ResourceNodes.MDL0GroupNode",
	# "BrawlLib.SSBB.ResourceNodes.ItmFreqNode",
	# "BrawlLib.SSBB.ResourceNodes.ItmTableNode",
	# "BrawlLib.SSBB.ResourceNodes.ItmTableGroupNode",
	"BrawlLib.SSBB.ResourceNodes.GIB2Node",
	"BrawlLib.SSBB.ResourceNodes.GMOVNode",
	"BrawlLib.SSBB.ResourceNodes.GET1Node",
	"BrawlLib.SSBB.ResourceNodes.GLK2Node",
	"BrawlLib.SSBB.ResourceNodes.GNDVNode",
	"BrawlLib.SSBB.ResourceNodes.GEG1Node"
]
FOLDERS = [
	"BrawlLib.SSBB.ResourceNodes.BRESGroupNode",
	"BrawlLib.SSBB.ResourceNodes.MDL0GroupNode"
]
PARAM_BLACKLIST = [ "FileType", "FileIndex", "GroupID", "RedirectIndex", "RedirectTarget" ]
# MDL0GroupNode is blacklisted because it is handled by getGroupNodeTypeFromParent
NODE_BLACKLIST = [ "BrawlLib.SSBB.ResourceNodes.MDL0GroupNode" ]
# Nodes that should never have params exported - bones shouldn't because they should always be fully replaced
NODE_NOPARAMS = [ "BrawlLib.SSBB.ResourceNodes.MDL0BoneNode" ]
UNIQUE_PROPERTIES = [ "BoneIndex" ]

# Temporary check to make sure the user has the necessary version to run the plugin
def versionCheck(showMessage=True):
	date = DateTime.Parse("2023-08-04T06:02:03.4382103+00:00")
	if File.Exists(AppPath + '\\Canary\\New'):
		fileText = File.ReadAllLines(AppPath + '\\Canary\\New')
		if DateTime.Parse(fileText[0]) >= date:
			return True
	if showMessage:
		BrawlAPI.ShowMessage("This feature requires BrawlCrate Canary. To enable Canary, navigate to Tools > Settings > Updater and check the box that says 'Opt into BrawlCrate Canary (Experimental) updates'.", "Canary Required")
	return False

class NodeObject:
		def __init__(self, node, md5, patchNodePath):
			self.node = node
			self.md5 = md5
			self.patchNodePath = patchNodePath

class NodeInfo:
		def __init__(self, nodeType, index, action="", groupName="", forceAdd=False, disableContainer=False):
			self.nodeType = nodeType.split('.')[-1]
			# {action} values:
			#	- REPLACE - import and replace existing node; if it does not exist, add
			#	- ADD - functions the same as replace; just informational that this node was added to the original file
			#	- PARAM - only get the parameters for this node, do not fully replace (for containers)
			#	- REMOVE - remove this node
			#	- FOLDER - no action, just a container
			self.action = action if action else "PARAM" if nodeType in CONTAINERS else "REPLACE"
			self.index = index
			self.groupName = groupName
			self.forceAdd = forceAdd
			self.fullType = nodeType

class PatchNode:
		def __init__(self, patchNodeName, path, parentNode=None):
			self.containerIndex = int(patchNodeName.split('$$')[0])
			self.name = str(HttpUtility.UrlDecode(removeFlags(patchNodeName.split('$$')[1]), Encoding.ASCII))
			# Get info for node
			if File.Exists(removeFlags(path) + '$$I'):
				attributes = File.ReadAllLines(removeFlags(path) + '$$I')
				self.typeString = readValueFromKey(attributes, "nodeType")
				self.action = readValueFromKey(attributes, "action")
				self.groupName = readValueFromKey(attributes, "groupName")
				index = readValueFromKey(attributes, "index")
				if index:
					self.index = int(index) if index else -1
				forceAdd = readValueFromKey(attributes, "forceAdd")
				self.forceAdd = textBool(forceAdd) if forceAdd else False
				self.fullType = readValueFromKey(attributes, "fullType")
			# If no info (should never happen), treat it as a folder
			else:
				self.fullType = getGroupNodeTypeFromParent(parentNode)
				self.typeString = self.fullType.split('.')[-1]
				self.action = "FOLDER"
				self.groupName = ""
				self.index = self.containerIndex
				self.forceAdd = False
			self.type = getNodeType(self.fullType)
			self.path = path
			self.originalString = patchNodeName
			self.disableContainer = False

class ARCEntry:
		def __init__(self, FileType, FileIndex, GroupID, RedirectIndex, RedirectTarget):
			self.FileType = FileType
			self.FileIndex = FileIndex
			self.GroupID = GroupID
			self.RedirectIndex = RedirectIndex
			self.RedirectTarget = RedirectTarget

class BuildPatchFile():
		def __init__(self, name="New File"):
				self.name = name
				self.path = ""
				self.file = ""
				self.fileName = ""
				self.patchFile = ""
				self.patchFileName = ""
				self.overwriteFile = True
				self.updateFighterIds = False

# Get all nodes with a particular path
def findChildren(node, path):
		# path = TreePath of a node, not TreePathAbsolute
		# node should be the root node to search from, generally the root node of the whole file
		nodes = []
		if node and node.Children:
			# Having a slash indicates we are not at the final node yet, so continue to drill down
			if '/' in path:
				# Node we are currently searching for
				nodeName = path.split('/')[0]
				# The new path for the next search step
				nextPath = path[path.find('/') + 1:len(path)]
				if len(node.Children) > 0:
					for child in node.Children:
						if child.Name == nodeName:
							# Drill down to check child paths
							nodes.extend(findChildren(child, nextPath))
			# No slash means we are at the end, so we are checking for the actual node at the end of the path
			else:
				for child in node.Children:
					if child.Name == path:
						# If the node exists, it finally gets added to the list
						nodes.append(child)
		return nodes

# Find the node to be patched based on a patch node's name
def findNodeToPatch(node, patchNode):
		index = 1
		if node and node.Children:
			for child in node.Children:
				if child.Name == patchNode.name and child.GetType() == patchNode.type:
					if index == patchNode.index:
						return child
					else:
						index += 1
		return None

# Get all settable, public node properties for the node
def getNodeProperties(node):
		properties = []
		for property in node.GetType().GetProperties():
			# if property.CanWrite and property.DeclaringType == node.GetType() and property.GetSetMethod() != None:
			if property.CanWrite and property.GetSetMethod() != None:
				properties.append(property)
		return properties

# Get any properties of a node with a name in a list of property names
def getSpecificNodeProperties(node, propertyNames):
		returnProperties = []
		properties = getNodeProperties(node)
		for property in properties:
			if property.Name in propertyNames:
				returnProperties.append(property)
		return returnProperties

# Get a property of a node with a specified name
def getSpecificNodeProperty(node, propertyName):
		properties = getNodeProperties(node)
		for property in properties:
			if property.Name == propertyName:
				return property
		return None

# Increment properties that must be unique on a given node
def uniquePropertyUpdate(node):
		uniqueProperties = getSpecificNodeProperties(node, UNIQUE_PROPERTIES)
		for property in uniqueProperties:
			usedValues = []
			for sibling in node.Parent.Children:
				if sibling != node:
					siblingProperty = getSpecificNodeProperty(sibling, property.Name)
					if siblingProperty != None:
						usedValues.append(siblingProperty.GetValue(sibling, None))
			value = property.GetValue(node, None)
			if value in usedValues:
				while value in usedValues:
					value += 1
				property.SetValue(node, value, None)

# Update fighter IDs for a node, for use in build patches included in a character package
def updateNodeIds(node, oldFighterIds, newFighterIds):
		properties = getNodeProperties(node)
		for property in properties:
			if str(property.Name).lower() == "fighterid" and oldFighterIds.fighterId and newFighterIds.fighterId and property.GetValue(node, None) == int(oldFighterIds.fighterId, 16):
				property.SetValue(node, Convert.ToByte(int(newFighterIds.fighterId, 16)), None)
			if str(property.Name).lower() == "slotid" and oldFighterIds.slotId and newFighterIds.slotId and property.GetValue(node, None) == int(oldFighterIds.slotId, 16):
				property.SetValue(node, Convert.ToByte(int(newFighterIds.slotId, 16)), None)
			if str(property.Name).lower() == "cosmeticid" and oldFighterIds.cosmeticId and newFighterIds.cosmeticId and property.GetValue(node, None) == int(oldFighterIds.cosmeticId, 16):
				property.SetValue(node, Convert.ToByte(int(newFighterIds.cosmeticId, 16)), None)
			if str(property.Name).lower() == "cssslotid" and oldFighterIds.cssSlotId and newFighterIds.cssSlotId and property.GetValue(node, None) == int(oldFighterIds.cssSlotId, 16):
				property.SetValue(node, Convert.ToByte(int(newFighterIds.cssSlotId, 16)), None)

# Copy node property values from one node to another
def copyNodeProperties(sourceNode, targetNode):
		properties = getNodeProperties(targetNode)
		for property in properties:
			if property.GetValue(targetNode, None) != property.GetValue(sourceNode, None) and str(property.Name) not in PARAM_BLACKLIST:
				property.SetValue(targetNode, property.GetValue(sourceNode, None), None)

# Get actual node type from string
def getNodeType(fullTypeString):
		fullString = str(fullTypeString) + ", BrawlLib"
		nodeType = Type.GetType(fullString)
		return nodeType

# Get the type for a group node based on passed in parent node
def getGroupNodeTypeFromParent(parentNode):
		type = "BrawlLib.SSBB.ResourceNodes.BRESGroupNode"
		if parentNode != None:
			if parentNode.NodeType == "BrawlLib.SSBB.ResourceNodes.MDL0Node":
				type = "BrawlLib.SSBB.ResourceNodes.MDL0GroupNode"
		return type

# Check if node is a container
def isContainer(node):
		# Whitelisted containers are always true
		if node.NodeType in CONTAINERS:
			return True
		# MDL0Nodes are only containers if they don't have anything other than Bones and Definitions
		if node.NodeType == "BrawlLib.SSBB.ResourceNodes.MDL0Node" and len(node.Children) > 0:
			for child in node.Children:
				if child.Name != "Bones" and child.Name != "Definitions":
					return False
			return True
		# MDL0BoneNodes are only containers if they have children
		if node.NodeType == "BrawlLib.SSBB.ResourceNodes.MDL0BoneNode" and len(node.Children) > 0:
			return True
		# If no checks passed, it's not a container
		return False

# Instantiate node based on type string
def createNodeFromString(fullTypeString):
		type = getNodeType(fullTypeString)
		instance = Activator.CreateInstance(type)
		return instance

# Get only the highest level valid nodes from root
def getPatchNodes(rootNode):
		writeLog("Getting valid patch nodes for export")
		allNodes = []
		if len(rootNode.Children) > 0:
			for child in rootNode.Children:
				if isContainer(child):
					if child.NodeType not in FOLDERS:
						allNodes.append(child)
					if len(child.Children) > 0:
						allNodes.extend(getPatchNodes(child))
				elif not isContainer(child):
					allNodes.append(child)
		writeLog("Got valid patch nodes for export")
		return allNodes

# Get name for color smash group
def getNodeGroupName(node):
		groupName = ""
		if node.NodeType == "BrawlLib.SSBB.ResourceNodes.TEX0Node" and node.SharesData:
			currentNode = node
			while currentNode.NextSibling():
				currentNode = currentNode.NextSibling()
				if not currentNode.SharesData:
					break
			groupName = currentNode.Name
		elif node.NodeType == "BrawlLib.SSBB.ResourceNodes.TEX0Node" and node.PrevSibling() and node.PrevSibling().SharesData:
			groupName = node.Name
		return groupName

# Get NodePath for a node
def getNodePath(node):
		pathNodeNames = []
		while node.Parent:
			pathNodeNames.insert(0, getPatchNodeName(node))
			node = node.Parent
		nodePath = ""
		i = 0
		while i < len(pathNodeNames):
			nodePath += pathNodeNames[i] + '\\' if i < len(pathNodeNames) - 1 else ''
			i += 1
		return nodePath

# Get NodeObjects for all patch nodes in file
def getNodeObjects(filePath, closeFile=True):
		writeLog("Getting node objects for file " + filePath)
		fileNodeList = []
		fileOpened = openFile(filePath, False)
		if fileOpened:
			#fileNodes = BrawlAPI.RootNode.GetChildrenRecursive()
			fileNodes = getPatchNodes(BrawlAPI.RootNode)
			for fileNode in fileNodes:
				nodePath = getNodePath(fileNode)
				fileNodeList.append(NodeObject(fileNode, fileNode.MD5Str(), nodePath))
		if closeFile:
			BrawlAPI.ForceCloseFile()
		writeLog("Finished getting node objects")
		return fileNodeList

# Get the number that should be appended to the beginning of a patch node
def getPatchNodeIndex(node):
		if node.Parent:
			i = 0
			for child in node.Parent.Children:
				if child.Name == node.Name:
					i +=1
				if child.Index == node.Index:
					return i
		return 1

# Get the patch node name for a node
def getPatchNodeName(node, action=""):
		# Folders don't have info, so they use the dupe index instead of container index
		index = node.Index if node.NodeType not in FOLDERS else getPatchNodeIndex(node)
		# Patch node name format: {index}$${name}$${flag}
		# {flag} values:
		#	- R - (Remove)		- Node to be removed
		#	- P - (Param)		- Update node properties without replacing
		#	- S - (Settings)	- Configure additional settings for node
		#	- I - (Info)		- Core information for the node
		nodeName = addLeadingZeros(str(index), 4) + '$$' + HttpUtility.UrlEncode(node.Name, Encoding.ASCII) + (('$$' + action) if action else "")
		return nodeName

# Generate node info file
def generateNodeInfo(nodeType, index, action, path, groupName="", forceAdd=False):
		nodeInfo = NodeInfo(nodeType, index, action, groupName=groupName, forceAdd=forceAdd)
		attrs = vars(nodeInfo)
		File.WriteAllText(path, '\n'.join("%s = %s" % item for item in attrs.items()))

# Remove flags from a node filename or path
def removeFlags(nodeString):
		# Remove file extensions
		nodeString = nodeString.replace(".tex0", "")
		# Remove flags
		flags = ["$$R", "$$I", "$$P", "$$S"]
		for flag in flags:
			if nodeString.endswith(flag):
				nodeString = "".join(nodeString.rsplit(flag, 1))
		return nodeString

# Apply settings file to a node if one exists
def applyNodeSettings(node, path):
	writeLog("Applying node settings found at " + path + " to " + node.Name)
	filePath = path + "$$S"
	# If there's a settings file, apply the special settings
	if File.Exists(filePath):
		fileText = File.ReadAllLines(filePath)
		fileType = readValueFromKey(fileText, "FileType")
		if fileType:
			node.FileType = ARCFileType[fileType]
		node.FileIndex = int(readValueFromKey(fileText, "FileIndex"))
		node.GroupID = int(readValueFromKey(fileText, "GroupID"))
		node.RedirectIndex = int(readValueFromKey(fileText, "RedirectIndex"))
		node.RedirectTarget = readValueFromKey(fileText, "RedirectTarget")
	return node

# Update patch data based on selected form options
def updatePatch(form):
		for removedNode in form.uncheckedNodes:
			# Always delete info for unchecked nodes
			flaglessPath = removeFlags(removedNode.path)
			if File.Exists(flaglessPath + "$$I"):
				File.Delete(flaglessPath + "$$I")
			if File.Exists(flaglessPath + "$$P"):
				File.Delete(flaglessPath + "$$P")
			if File.Exists(flaglessPath + "$$S"):
				File.Delete(flaglessPath + "$$S")
			# Remove any files or folders for the node
			if Directory.Exists(removedNode.path):
				Directory.Delete(removedNode.path, True)
			if File.Exists(removedNode.path):
				File.Delete(removedNode.path)
		# Generate new info for updated nodes
		for changedNode in form.changedNodes:
			if changedNode not in form.uncheckedNodes:
				# If the container was disabled, clean up so it is set to a regular node
				if changedNode.disableContainer == True:
					changedNode.action = "REPLACE"
					if Directory.Exists(changedNode.path):
						Directory.Delete(changedNode.path, True)
					flaglessPath = removeFlags(changedNode.path)
					if File.Exists(flaglessPath + "$$P"):
						File.Move(flaglessPath + "$$P", flaglessPath)
				generateNodeInfo(changedNode.fullType, changedNode.index, changedNode.action, changedNode.path + "$$I", changedNode.groupName, changedNode.forceAdd)

# Export node for a patch and create directory if it can't be found
def exportPatchNode(nodeObject, add=False, recursive=False):
		writeLog("Exporting patch node " + nodeObject.node.TreePathAbsolute)
		# Only export if parent node was not already exported (e.g. a MDL0 was exported, meaning it wasn't a container in one of the files)
		node = nodeObject.node
		while node.Parent:
			parentPath = getNodePath(node.Parent)
			parentFile = TEMP_PATH + '\\' + parentPath + '\\' + getPatchNodeName(node.Parent)
			if File.Exists(parentFile):
				writeLog("Parent node was already exported.")
				return
			node = node.Parent
		# Create directory if it doesn't exist
		createDirectory(TEMP_PATH + '\\' + nodeObject.patchNodePath)
		action = ""
		groupName = ""
		# If it's a real node, export it
		if nodeObject.node.MD5Str() or recursive:
			if nodeObject.node.MD5Str() and nodeObject.node.NodeType not in NODE_BLACKLIST:
				action = "ADD" if add else "PARAM" if isContainer(nodeObject.node) else ""
				groupName = getNodeGroupName(nodeObject.node)
				patchNodePath = TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "P" if isContainer(nodeObject.node) else "")
				if not (isContainer(nodeObject.node) and nodeObject.node.NodeType in NODE_NOPARAMS):
					nodeObject.node.Export(patchNodePath + (".tex0" if nodeObject.node.NodeType == "BrawlLib.SSBB.ResourceNodes.TEX0Node" else ""))
				# Export image for preview if eligible
				if nodeObject.node.NodeType == "BrawlLib.SSBB.ResourceNodes.TEX0Node":
					nodeObject.node.Export(patchNodePath + ".png")
				# Export special settings for ARCEntry nodes
				if nodeObject.node.GetType().IsSubclassOf(ARCEntryNode):
					arcEntry = ARCEntry(nodeObject.node.FileType, nodeObject.node.FileIndex, nodeObject.node.GroupID, nodeObject.node.RedirectIndex, nodeObject.node.RedirectTarget)
					attrs = vars(arcEntry)
					File.WriteAllText(TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "S"), '\n'.join("%s = %s" % item for item in attrs.items()))
			# Export parent nodes if they exist
			if nodeObject.node.Parent and isContainer(nodeObject.node.Parent) and nodeObject.node.Parent != BrawlAPI.RootNode:
				parentPath = getNodePath(nodeObject.node.Parent)
				parentFile = TEMP_PATH + '\\' + parentPath + '\\' + getPatchNodeName(nodeObject.node.Parent, "P")
				if not File.Exists(parentFile):
					parentObject = NodeObject(nodeObject.node.Parent, nodeObject.node.Parent.MD5Str(), parentPath)
					exportPatchNode(parentObject, recursive=True)
		# Otherwise, create a flag to indicate removal
		elif not recursive:
			action = "REMOVE"
			File.CreateText(TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "R")).Close()
		# No matter what, create an info node so we can gather all necessary info about it
		if nodeObject.node.NodeType not in NODE_BLACKLIST:
			generateNodeInfo(nodeObject.node.NodeType, getPatchNodeIndex(nodeObject.node), action, TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "I"), groupName)
		writeLog("Exported patch node")

# Create a patch file
def createPatch(cleanFile, alteredFile):
		# Get nodes for altered file and clean file for comparison
		cleanFileNodes = getNodeObjects(cleanFile, closeFile=True)
		alteredFileNodes = getNodeObjects(alteredFile, closeFile=False)

		try:
			# Set up progressbar
			progressCounter = 0
			totalNodes = len(alteredFileNodes)
			progressBar = ProgressWindow(MainForm.Instance, "Comparing", "Comparing files...", False)
			progressBar.Begin(0, totalNodes, progressCounter)

			# Iterate through nodes from our altered file
			for alteredFileNode in alteredFileNodes:
				progressCounter += 1
				progressBar.Update(progressCounter)
				removeNode = False
				matchFound = False
				# For every altered file node, search the clean file nodes for a match
				for cleanFileNode in cleanFileNodes:
					# If the path matches, we've found a match
					# Use TreePath instead of TreePathAbsolute, because TreePath excludes the root node, which is sometimes the file name
					if alteredFileNode.node.TreePath == cleanFileNode.node.TreePath:
						removeNode = cleanFileNode
						matchFound = True
						# If we've found a match, but MD5s do NOT match, this is an altered node and should be exported
						if alteredFileNode.md5 != cleanFileNode.md5:
							exportPatchNode(alteredFileNode)
						break
				# If we never found a match for a node in the altered file, it's a brand new node, and should be exported
				if not matchFound:
					exportPatchNode(alteredFileNode, add=True)
				# If we found a match at all, the clean file node should be removed from the list for comparison, to speed up searches and
				#to prevent false positives when nodes share paths.
				if removeNode:
					cleanFileNodes.remove(removeNode)
			progressBar.Finish()
		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ForceCloseFile()
			raise e
		fileName = BrawlAPI.RootNode.FileName.replace(getFileInfo(BrawlAPI.RootNode.FileName).Extension, "")
		BrawlAPI.ForceCloseFile()
		# Any nodes remaining in the clean file node list are nodes with no matches in the altered file, meaning they should be removed when the patch is installed
		for removeNode in cleanFileNodes:
			exportPatchNode(removeNode)
		# Clean up folders for deleted stuff
		directories = Directory.GetDirectories(TEMP_PATH, "*", SearchOption.AllDirectories)
		i = 0
		while i < len(directories):
			if Directory.Exists(directories[i]):
				directoryInfo = DirectoryInfo(directories[i])
				#if '$$FOLDER' in directoryInfo.Name:
				#BrawlAPI.ShowMessage(directoryInfo.Parent.FullName + '\\' + directoryInfo.Name.replace('$$FOLDER', '$$REMOVE'), "")
				if File.Exists(directoryInfo.Parent.FullName + '\\' + directoryInfo.Name + "$$R"):
					Directory.Delete(directories[i], True)
			i += 1
		return fileName

# Process an individual patch file
def processPatchFiles(patchFolder, node, progressBar):
	writeLog("Processing patch files for " + node.Name)
	newNode = None
	# Drill down into any directories in the patch
	for directory in Directory.GetDirectories(patchFolder):
		patchNode = PatchNode(DirectoryInfo(directory).Name, directory, node)
		newNode = findNodeToPatch(node, patchNode)
		# If a matching container node doesn't exist, create it
		if not newNode:
			newNode = createNodeFromString(patchNode.type)
			node.InsertChild(newNode, patchNode.containerIndex)
			newNode.Name = patchNode.name
		if newNode:
			processPatchFiles(directory, newNode, progressBar)
		if newNode.GetType().IsSubclassOf(ARCEntryNode):
			applyNodeSettings(newNode, patchNode.path)
		progressBar.CurrentValue += 1
		progressBar.Update()
	newNode = None
	# Import any node files in the directory
	for patchFile in Directory.GetFiles(patchFolder):
		if patchFile.replace(".tex0", "").endswith("$$S") or patchFile.replace(".tex0", "").endswith("$$I") or patchFile.endswith(".png"):
			progressBar.CurrentValue += 1
			progressBar.Update()
			continue
		writeLog("Processing patch file " + patchFile)
		patchNode = PatchNode(getFileInfo(patchFile).Name, patchFile)
		# Handle each node file based on the defined action
		if patchNode.action in [ "REPLACE", "REMOVE", "PARAM", "ADD" ] and not patchNode.forceAdd:
			foundNode = findNodeToPatch(node, patchNode)
			if foundNode:
				if patchNode.action == "REPLACE" or patchNode.action == "ADD":
					writeLog("Replacing " + foundNode.Name)
					foundNode.Replace(patchFile)
					uniquePropertyUpdate(foundNode)
				if patchNode.action == "REMOVE":
					writeLog("Removing " + foundNode.Name)
					foundNode.Remove()
				if patchNode.action == "PARAM":
					writeLog("Updating params for " + foundNode.Name)
					tempNode = createNodeFromString(patchNode.type)
					name = foundNode.Name
					node.AddChild(tempNode)
					tempNode.Replace(patchFile)
					copyNodeProperties(tempNode, foundNode)
					tempNode.Remove()
					foundNode.Name = name
					uniquePropertyUpdate(foundNode)
			# If a replace node can't be found, add it
			elif patchNode.action == "REPLACE" or patchNode.action == "ADD":
				writeLog("Adding " + patchNode.name)
				newNode = createNodeFromString(patchNode.type)
				node.InsertChild(newNode, patchNode.containerIndex)
				newNode.Replace(patchFile)
				newNode.Name = patchNode.name
				uniquePropertyUpdate(newNode)
		elif patchNode.forceAdd:
			writeLog("Adding " + patchNode.name)
			newNode = createNodeFromString(patchNode.type)
			node.InsertChild(newNode, patchNode.containerIndex)
			newNode.Replace(patchFile)
			newNode.Name = patchNode.name
			uniquePropertyUpdate(newNode)
		if newNode and newNode.GetType().IsSubclassOf(ARCEntryNode):
			applyNodeSettings(newNode, patchNode.path)
		progressBar.CurrentValue += 1
		progressBar.Update()

# Apply a patch to a file
def applyPatch(file, patchFolder=TEMP_PATH):
		fileOpened = openFile(file)
		if fileOpened:
			node = BrawlAPI.RootNode
			try:
				# Set up progressbar
				totalNodes = len(Directory.GetFiles(patchFolder, "*", SearchOption.AllDirectories)) + len(Directory.GetDirectories(patchFolder, "*", SearchOption.AllDirectories))
				progressBar = ProgressWindow(MainForm.Instance, "Patching", "Applying patch...", False)
				progressBar.Begin(0, totalNodes, 0)
				processPatchFiles(patchFolder, node, progressBar)
				progressBar.Finish()
			except Exception as e:
				writeLog("ERROR " + str(e))
				if 'progressBar' in locals():
					progressBar.Finish()
				raise e

# Get info for build patch file	
def getPatchInfo(file):
		patchInfo = BuildPatchFile()
		if File.Exists(file):
			fileText = File.ReadAllLines(file)
			patchInfo.name = readValueFromKey(fileText, "name")
			patchInfo.fileName = readValueFromKey(fileText, "fileName")
			patchInfo.patchFileName = readValueFromKey(fileText, "patchFileName")
			patchInfo.path = readValueFromKey(fileText, "path")
			patchInfo.overwriteFile = textBool(readValueFromKey(fileText, "overwriteFile"))
			patchInfo.updateFighterIds = textBool(readValueFromKey(fileText, "updateFighterIds"))
		return patchInfo

# Apply a build patch
def applyBuildPatch(buildPatch, oldFighterIds=None, newFighterIds=None):
		tempPath = Path.Combine(AppPath, "tempBuildPatch")
		if Directory.Exists(tempPath):
			Directory.Delete(tempPath, True)
		tempPatchPath = Path.Combine(AppPath, "tempPatch")
		unzipFile(buildPatch, "tempBuildPatch")
		files = Directory.GetFiles(tempPath, "*.patchinfo")
		newFile = ""
		try:
			# Set up progressbar
			totalFiles = len(files)
			progressBar = ProgressWindow(MainForm.Instance, "Patching Build", "Applying build patch...", False)
			progressBar.Begin(0, totalFiles, 0)
			# Iterate through patchinfo files
			for file in files:
				patchInfo = getPatchInfo(file)
				path = patchInfo.path.lstrip("\\").lstrip("/")
				if patchInfo.path:
					fullPath = Path.Combine(MainForm.BuildPath, path)
					# If we find the file...
					if File.Exists(fullPath):
						# First attempt to patch
						patchFile = Path.Combine(tempPath, patchInfo.patchFileName) if patchInfo.patchFileName else ""
						if patchFile and File.Exists(patchFile):
							if Directory.Exists(tempPatchPath):
								Directory.Delete(tempPatchPath, 1)
							unzipFile(patchFile, tempPatchPath)
							applyPatch(fullPath, tempPatchPath)
						# If there's no patch, try overwriting
						elif patchInfo.overwriteFile and patchInfo.fileName:
							newFile = Path.Combine(tempPath, patchInfo.fileName) if patchInfo.fileName else ""
							if newFile:
								copyRenameFile(newFile, getFileInfo(fullPath).Name, getFileInfo(fullPath).DirectoryName)
					# If we don't find the file, check if we have a file to place and place it
					elif patchInfo.fileName:
						newFile = Path.Combine(tempPath, patchInfo.fileName) if patchInfo.fileName else ""
						if newFile:
							copyRenameFile(newFile, getFileInfo(fullPath).Name, getFileInfo(fullPath).DirectoryName)
				# Update fighter IDs
				if patchInfo.updateFighterIds and oldFighterIds and newFighterIds:
					if newFile:
						openFile(fullPath, False)
					allNodes = BrawlAPI.RootNode.GetChildrenRecursive()
					for node in allNodes:
						updateNodeIds(node, oldFighterIds, newFighterIds)
				if BrawlAPI.RootNode:
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()
				progressBar.CurrentValue += 1
				progressBar.Update()
			progressBar.Finish()
			if Directory.Exists(tempPatchPath):
				Directory.Delete(tempPatchPath, True)
			if Directory.Exists(tempPath):
				Directory.Delete(tempPath, True)
		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			raise e