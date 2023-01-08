__author__ = "Squidgy"

from BrawlInstallerLib import *

class Node:
		def __init__(self, node, md5):
			self.node = node
			self.md5 = md5

def getNodes(filePath, closeFile=True):
		writeLog("Getting nodes for file " + filePath)
		fileNodeList = []
		fileOpened = openFile(filePath, False)
		if fileOpened:
			fileNodes = BrawlAPI.RootNode.GetChildrenRecursive()
			for fileNode in fileNodes:
				fileNodeList.append(Node(fileNode, fileNode.MD5Str()))
		if closeFile:
			BrawlAPI.ForceCloseFile()
		writeLog("Finished getting nodes")
		return fileNodeList

def main():
		text = ""
		createLogFile()
		
		# Get nodes for altered file and clean file for comparison
		alteredFileNodes = getNodes(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac', closeFile=True)
		cleanFileNodes = getNodes(MainForm.BuildPath + '/pf/menu2/sc_selcharacter - Copy.pac', closeFile=False)

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
		# Any nodes remaining in the clean file node list are nodes with no matches in the altered file, meaning they should be removed
		for removeNode in cleanFileNodes:
			removeText += "\n" + removeNode.node.Name + "\n"
		writeLog(removeText)
		BrawlAPI.ShowMessage(removeText, "")
main()