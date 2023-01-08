__author__ = "Squidgy"

from BrawlInstallerLib import *

TEMP_PATH = AppPath + '/temp'
CONTAINERS = [ "BrawlLib.SSBB.ResourceNodes.ARCNode", "BrawlLib.SSBB.ResourceNodes.BRRESNode", "BrawlLib.SSBB.ResourceNodes.BRESGroupNode"]

class NodeObject:
		def __init__(self, node, md5):
			self.node = node
			self.md5 = md5

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

# Get all settable, public node properties for the node
def getNodeProperties(node):
		properties = []
		for property in node.GetType().GetProperties():
			if property.CanWrite and property.DeclaringType == node.GetType() and property.GetSetMethod():
				properties.append(property)
		return properties

# Copy node property values from one node to another
def copyNodeProperties(sourceNode, targetNode):
		properties = getNodeProperties(targetNode)
		for property in properties:
			property.SetValue(targetNode, property.GetValue(sourceNode, None), None)

# Get only the highest level valid nodes from root
def getPatchNodes(rootNode):
		writeLog("Getting valid patch nodes for export")
		allNodes = []
		if len(rootNode.Children) > 0:
			for child in rootNode.Children:
				if child.NodeType not in CONTAINERS:
					allNodes.append(child)
				elif len(child.Children) > 0:
					allNodes.extend(getPatchNodes(child))
		writeLog("Got valid patch nodes for export")
		return allNodes

# Get NodeObjects for all patch nodes in file
def getNodeObjects(filePath, closeFile=True):
		writeLog("Getting node objects for file " + filePath)
		fileNodeList = []
		fileOpened = openFile(filePath, False)
		if fileOpened:
			#fileNodes = BrawlAPI.RootNode.GetChildrenRecursive()
			fileNodes = getPatchNodes(BrawlAPI.RootNode)
			for fileNode in fileNodes:
				fileNodeList.append(NodeObject(fileNode, fileNode.MD5Str()))
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
def getPatchNodeName(node, remove=False, folder=False):
		index = getPatchNodeIndex(node)
		# Patch node name format: {index}$${name}$${action}
		# {action} values:
		#	- IMPORT - import as normal
		#	- PARAM - only get the parameters for this node, do not fully replace (for containers)
		#	- REMOVE - remove this node
		action = "IMPORT"
		if node.NodeType in CONTAINERS:
			action = "PARAM"
		if remove:
			action = "REMOVE"
		if folder:
			action = "FOLDER"
		nodeName = addLeadingZeros(str(index), 4) + '$$' + node.Name + '$$' + action
		return nodeName

# Export node for a patch and create directory if it can't be found
def exportPatchNode(node, remove=False):
		writeLog("Exporting patch node " + node.TreePathAbsolute)
		# Old way, just creates directories based on node tree path
		#nodeSplit = node.TreePathAbsolute.split('/')
		#nodePath = ""
		#i = 0
		#while i < len(nodeSplit):
		#	nodePath += nodeSplit[i] + '\\' if i < len(nodeSplit) - 1 else ''
		#	i += 1
		# New way, export with an index at the beginning, which is useful for importer if multiple children have the same name
		currentNode = node
		pathNodeNames = []
		while currentNode.Parent:
			pathNodeNames.insert(0, getPatchNodeName(currentNode, folder=True))
			currentNode = currentNode.Parent
		nodePath = ""
		i = 0
		while i < len(pathNodeNames):
			nodePath += pathNodeNames[i] + '\\' if i < len(pathNodeNames) - 1 else ''
			i += 1
		createDirectory(TEMP_PATH + '\\' + nodePath)
		node.Export(TEMP_PATH + '\\' + nodePath + '\\' + getPatchNodeName(node, remove))
		writeLog("Exported patch node")

def main():
		text = ""
		createLogFile()

		# If temporary directory already exists, delete it to prevent duplicate files
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)
		createDirectory(TEMP_PATH)

		# File prompts
		cleanFile = BrawlAPI.OpenFileDialog("Select the base file for your patch", "All Files|*.*")
		alteredFile = BrawlAPI.OpenFileDialog("Select the altered file for your patch", "All Files|*.*")
		
		# Get nodes for altered file and clean file for comparison
		cleanFileNodes = getNodeObjects(cleanFile, closeFile=True)
		alteredFileNodes = getNodeObjects(alteredFile, closeFile=False)

		# Set up progressbar
		progressCounter = 0
		totalNodes = len(alteredFileNodes)
		progressBar = ProgressWindow(MainForm.Instance, "Comparing files...", "Comparing", False)
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
				if alteredFileNode.node.TreePathAbsolute == cleanFileNode.node.TreePathAbsolute:
					removeNode = cleanFileNode
					matchFound = True
					# If we've found a match, but MD5s do NOT match, this is an altered node and should be exported
					if alteredFileNode.md5 != cleanFileNode.md5:
						exportPatchNode(alteredFileNode.node)
						text += "\n" + alteredFileNode.node.TreePathAbsolute + ": " + alteredFileNode.md5 + " " + cleanFileNode.md5 + "\n"
					break
			# If we never found a match for a node in the altered file, it's a brand new node, and should be exported
			if not matchFound:
				exportPatchNode(alteredFile.node)
				text += "\n" + alteredFileNode.node.TreePathAbsolute + ": " + "NEW\n"
			# If we found a match at all, the clean file node should be removed from the list for comparison, to speed up searches and
			#to prevent false positives when nodes share paths.
			if removeNode:
				cleanFileNodes.remove(removeNode)
		progressBar.Finish()
		BrawlAPI.ForceCloseFile()
		writeLog(text)
		BrawlAPI.ShowMessage(text, "")
		removeText = ""
		# Any nodes remaining in the clean file node list are nodes with no matches in the altered file, meaning they should be removed when the patch is installed
		for removeNode in cleanFileNodes:
			exportPatchNode(removeNode.node, True)
			removeText += "\n" + removeNode.node.Name + "\n"
		writeLog(removeText)
		BrawlAPI.ShowMessage(removeText, "")

main()