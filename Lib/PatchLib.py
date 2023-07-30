# PatchLib
# Library for BrawlInstaller's patching plugins

from BrawlInstallerLib import *
from System import Type
from System import Activator

TEMP_PATH = AppPath + '/temp'
CONTAINERS = [ "BrawlLib.SSBB.ResourceNodes.ARCNode", "BrawlLib.SSBB.ResourceNodes.BRRESNode", "BrawlLib.SSBB.ResourceNodes.BRESGroupNode"]
PARAM_WHITELIST = [ "Compression" ]

class NodeObject:
		def __init__(self, node, md5, patchNodePath):
			self.node = node
			self.md5 = md5
			self.patchNodePath = patchNodePath

class PatchNode:
		def __init__(self, patchNodeName):
			attributes = patchNodeName.split("$$")
			self.index = attributes[0]
			self.name = attributes[1]
			self.typeString = attributes[2]
			self.type = getNodeType(self.typeString)
			self.action = attributes[3]

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
					if addLeadingZeros(str(index), 4) == patchNode.index:
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
					pathNodeNames.insert(0, getPatchNodeName(currentNode, action="FOLDER"))
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
		index = getPatchNodeIndex(node)
		# Patch node name format: {index}$${name}$${nodeType}$${action}
		# {action} values:
		#	- REPLACE - import and replace existing node; if it does not exist, add
		#	- ADD - import and add as a new node
		#	- PARAM - only get the parameters for this node, do not fully replace (for containers)
		#	- REMOVE - remove this node
		if not action:
			action = "REPLACE"
			if node.NodeType in CONTAINERS:
				action = "PARAM"
		nodeName = addLeadingZeros(str(index), 4) + '$$' + node.Name + '$$' + node.NodeType.split('.')[-1] + '$$' + action
		return nodeName

# Export node for a patch and create directory if it can't be found
def exportPatchNode(nodeObject, add=False):
		writeLog("Exporting patch node " + nodeObject.node.TreePathAbsolute)
		createDirectory(TEMP_PATH + '\\' + nodeObject.patchNodePath)
		if nodeObject.node.MD5Str():
			nodeObject.node.Export(TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "ADD" if add else ""))
		else:
			File.CreateText(TEMP_PATH + '\\' + nodeObject.patchNodePath + '\\' + getPatchNodeName(nodeObject.node, "REMOVE")).Close()
		writeLog("Exported patch node")