__author__ = "Squidgy"

from BrawlInstallerLib import *

TEMP_PATH = AppPath + '/temp'

class Node:
		def __init__(self, node, md5):
			self.node = node
			self.md5 = md5

# Get only the highest level valid nodes from root
def getNodesForExport(rootNode):
		writeLog("Getting valid nodes for export")
		containers = [ "BrawlLib.SSBB.ResourceNodes.ARCNode", "BrawlLib.SSBB.ResourceNodes.BRRESNode", "BrawlLib.SSBB.ResourceNodes.BRESGroupNode"]
		allNodes = []
		if len(rootNode.Children) > 0:
			for child in rootNode.Children:
				if child.NodeType not in containers:
					allNodes.append(child)
				elif len(child.Children) > 0:
					allNodes.extend(getNodesForExport(child))
		writeLog("Got valid nodes for export")
		return allNodes

# Get all valid nodes in a file, including their MD5s
def getNodes(filePath, closeFile=True):
		writeLog("Getting nodes for file " + filePath)
		fileNodeList = []
		fileOpened = openFile(filePath, False)
		if fileOpened:
			#fileNodes = BrawlAPI.RootNode.GetChildrenRecursive()
			fileNodes = getNodesForExport(BrawlAPI.RootNode)
			for fileNode in fileNodes:
				fileNodeList.append(Node(fileNode, fileNode.MD5Str()))
		if closeFile:
			BrawlAPI.ForceCloseFile()
		writeLog("Finished getting nodes")
		return fileNodeList

# Export node and create directory if it can't be found
def exportNode(node):
		writeLog("Exporting node " + node.TreePathAbsolute)
		nodeSplit = node.TreePathAbsolute.split('/')
		nodePath = ""
		i = 0
		while i < len(nodeSplit):
			nodePath += nodeSplit[i] + '\\' if i < len(nodeSplit) - 1 else ''
			i += 1
		createDirectory(TEMP_PATH + '\\' + nodePath)
		node.Export(TEMP_PATH + '\\' + nodePath + '\\' + node.Name)
		writeLog("Exported node")

def main():
		text = ""
		createLogFile()

		# If temporary directory already exists, delete it to prevent duplicate files
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)
		createDirectory(TEMP_PATH)
		
		# Get nodes for altered file and clean file for comparison
		cleanFileNodes = getNodes(MainForm.BuildPath + '/pf/menu2/sc_selcharacter - Copy.pac', closeFile=True)
		alteredFileNodes = getNodes(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac', closeFile=False)

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
						exportNode(alteredFileNode.node)
						text += "\n" + alteredFileNode.node.TreePathAbsolute + ": " + alteredFileNode.md5 + " " + cleanFileNode.md5 + "\n"
					break
			# If we never found a match for a node in the altered file, it's a brand new node, and should be exported
			if not matchFound:
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
			removeText += "\n" + removeNode.node.Name + "\n"
		writeLog(removeText)
		BrawlAPI.ShowMessage(removeText, "")
main()