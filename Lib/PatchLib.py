# PatchLib
# Library for BrawlInstaller's patching plugins

from BrawlInstallerLib import *
from System import Type
from System import Activator

TEMP_PATH = AppPath + '/temp'
CONTAINERS = [ "BrawlLib.SSBB.ResourceNodes.ARCNode", "BrawlLib.SSBB.ResourceNodes.BRRESNode", "BrawlLib.SSBB.ResourceNodes.BLOCNode", "BrawlLib.SSBB.ResourceNodes.BRESGroupNode"]
PARAM_WHITELIST = [ "Compression" ]

class NodeObject:
		def __init__(self, node, md5, patchNodePath):
			self.node = node
			self.md5 = md5
			self.patchNodePath = patchNodePath

class NodeInfo:
		def __init__(self, nodeType, index, action="", groupName="", forceAdd=False):
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

class PatchNode:
		def __init__(self, patchNodeName, path):
			self.containerIndex = int(patchNodeName.split('$$')[0])
			self.name = patchNodeName.split('$$')[1].replace(".tex0", "")
			# Get info for node
			if File.Exists(path.replace(".tex0", "").replace("$$R", "") + '$$I'):
				attributes = File.ReadAllLines(path.replace(".tex0", "").replace("$$R", "") + '$$I')
				self.typeString = readValueFromKey(attributes, "nodeType")
				self.action = readValueFromKey(attributes, "action")
				self.groupName = readValueFromKey(attributes, "groupName")
				index = readValueFromKey(attributes, "index")
				if index:
					self.index = int(index) if index else -1
				forceAdd = readValueFromKey(attributes, "forceAdd")
				self.forceAdd = textBool(forceAdd) if forceAdd else False
			# If no info (should never happen), treat it as a folder
			else:
				self.typeString = "BRESGroupNode"
				self.action = "FOLDER"
				self.groupName = ""
				self.index = self.containerIndex
				self.forceAdd = False
			self.type = getNodeType(self.typeString)
			self.path = path
			self.originalString = patchNodeName

class ARCEntry:
		def __init__(self, FileType, FileIndex, GroupID, RedirectIndex, RedirectTarget):
			self.FileType = FileType
			self.FileIndex = FileIndex
			self.GroupID = GroupID
			self.RedirectIndex = RedirectIndex
			self.RedirectTarget = RedirectTarget

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
			if property.CanWrite and property.GetSetMethod() != None and str(property.Name) in PARAM_WHITELIST:
				properties.append(property)
		return properties

# Copy node property values from one node to another
def copyNodeProperties(sourceNode, targetNode):
		properties = getNodeProperties(targetNode)
		for property in properties:
			if property.GetValue(targetNode, None) != property.GetValue(sourceNode, None):
				property.SetValue(targetNode, property.GetValue(sourceNode, None), None)

# Get actual node type from string
def getNodeType(typeString):
		fullString = "BrawlLib.SSBB.ResourceNodes." + typeString + ", BrawlLib"
		nodeType = Type.GetType(fullString)
		return nodeType

# Instantiate node based on type string
def createNodeFromString(typeString):
		type = getNodeType(typeString)
		instance = Activator.CreateInstance(type)
		return instance

# Get only the highest level valid nodes from root
def getPatchNodes(rootNode):
		writeLog("Getting valid patch nodes for export")
		allNodes = []
		if len(rootNode.Children) > 0:
			for child in rootNode.Children:
				if child.NodeType in CONTAINERS:
					if child.NodeType != "BrawlLib.SSBB.ResourceNodes.BRESGroupNode":
						allNodes.append(child)
					if len(child.Children) > 0:
						allNodes.extend(getPatchNodes(child))
				elif child.NodeType not in CONTAINERS:
					allNodes.append(child)
		writeLog("Got valid patch nodes for export")
		return allNodes

# Get name for color smash group
def getNodeGroupName(node):
		groupName = ""
		if node.NodeType == "BrawlLib.SSBB.ResourceNodes.TEX0Node" and (node.SharesData or (node.PrevSibling() and node.PrevSibling().SharesData)):
			currentNode = node
			while currentNode.NextSibling():
				currentNode = currentNode.NextSibling()
				if not currentNode.SharesData:
					break
			groupName = currentNode.Name
		return groupName

# Get NodeObjects for all patch nodes in file
def getNodeObjects(filePath, closeFile=True):
		writeLog("Getting node objects for file " + filePath)
		fileNodeList = []
		fileOpened = openFile(filePath, False)
		if fileOpened:
			#fileNodes = BrawlAPI.RootNode.GetChildrenRecursive()
			fileNodes = getPatchNodes(BrawlAPI.RootNode)
			for fileNode in fileNodes:
				currentNode = fileNode
				pathNodeNames = []
				while currentNode.Parent:
					pathNodeNames.insert(0, getPatchNodeName(currentNode))
					currentNode = currentNode.Parent
				nodePath = ""
				i = 0
				while i < len(pathNodeNames):
					nodePath += pathNodeNames[i] + '\\' if i < len(pathNodeNames) - 1 else ''
					i += 1
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
		index = node.Index if node.NodeType != "BrawlLib.SSBB.ResourceNodes.BRESGroupNode" else getPatchNodeIndex(node)
		# Patch node name format: {index}$${name}$${flag}
		# {flag} values:
		#	- R - (Remove)		- Node to be removed
		#	- P - (Param)		- Update node properties without replacing
		#	- S - (Settings)	- Configure additional settings for node
		#	- I - (Info)		- Core information for the node
		nodeName = addLeadingZeros(str(index), 4) + '$$' + node.Name + (('$$' + action) if action else "")
		return nodeName

# Generate node info file
def generateNodeInfo(nodeType, index, action, path, groupName="", forceAdd=False):
		nodeInfo = NodeInfo(nodeType, index, action, groupName=groupName, forceAdd=forceAdd)
		attrs = vars(nodeInfo)
		File.WriteAllText(path, '\n'.join("%s = %s" % item for item in attrs.items()))

# Update patch data based on selected form options
def updatePatch(form):
		for removedNode in form.uncheckedNodes:
			# Always delete info for unchecked nodes
			if File.Exists(removedNode.path.replace(".tex0", "") + "$$I"):
				File.Delete(removedNode.path.replace(".tex0", "") + "$$I")
			if File.Exists(removedNode.path + "$$P"):
				File.Delete(removedNode.path + "$$P")
			if File.Exists(removedNode.path + "$$S"):
				File.Delete(removedNode.path + "$$S")
			# For containers, remove all associated folders
			if removedNode.type.FullName in CONTAINERS:
				if Directory.Exists(removedNode.path):
					Directory.Delete(removedNode.path, True)
			else:
				if File.Exists(removedNode.path):
					File.Delete(removedNode.path)
		# Generate new info for updated nodes
		for changedNode in form.changedNodes:
			if changedNode not in form.uncheckedNodes:
				generateNodeInfo(changedNode.typeString, changedNode.index, changedNode.action, changedNode.path + "$$I", changedNode.groupName, changedNode.forceAdd)

# Export node for a patch and create directory if it can't be found
def exportPatchNode(nodeObject, add=False):
		writeLog("Exporting patch node " + nodeObject.node.TreePathAbsolute)
		createDirectory(TEMP_PATH + '\\' + nodeObject.patchNodePath)
		action = ""
		groupName = ""
		# If it's a real node, export it
		if nodeObject.node.MD5Str():
			action = "ADD" if add else ""
			groupName = getNodeGroupName(nodeObject.node)
			nodeObject.node.Export(TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "P" if nodeObject.node.NodeType in CONTAINERS else "") + (".tex0" if nodeObject.node.NodeType == "BrawlLib.SSBB.ResourceNodes.TEX0Node" else ""))
			# Export special settings for ARCEntry nodes
			if nodeObject.node.GetType().IsSubclassOf(ARCEntryNode):
				arcEntry = ARCEntry(nodeObject.node.FileType, nodeObject.node.FileIndex, nodeObject.node.GroupID, nodeObject.node.RedirectIndex, nodeObject.node.RedirectTarget)
				attrs = vars(arcEntry)
				File.WriteAllText(TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "S"), '\n'.join("%s = %s" % item for item in attrs.items()))
		# Otherwise, create a flagged to indicate removal
		else:
			action = "REMOVE"
			File.CreateText(TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "R")).Close()
		# No matter what, create an info node so we can gather all necessary info about it
		generateNodeInfo(nodeObject.node.NodeType, getPatchNodeIndex(nodeObject.node), action, TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "I"), groupName)
		writeLog("Exported patch node")