__author__ = "Squidgy"

from PatchLib import *

def processPatchFiles(patchFolder, node):
	writeLog("Processing patch files")
	# Drill down into any directories in the patch
	for directory in Directory.GetDirectories(patchFolder):
		patchNode = PatchNode(DirectoryInfo(directory).Name)
		newNode = findNodeToPatch(node, patchNode)
		# If a matching container node doesn't exist, create it
		if not newNode:
			newNode = createNodeFromString(patchNode.typeString)
			newNode.Name = patchNode.name
			node.AddChild(newNode)
		if newNode:
			processPatchFiles(directory, newNode)
	# Import any node files in the directory
	for patchFile in Directory.GetFiles(patchFolder):
		writeLog("Processing patch file " + patchFile)
		patchNode = PatchNode(getFileInfo(patchFile).Name)
		# Handle each node file based on the defined action
		if patchNode.action in [ "REPLACE", "REMOVE", "PARAM" ]:
			foundNode = findNodeToPatch(node, patchNode)
			if foundNode:
				if patchNode.action == "REPLACE":
					writeLog("Replacing " + foundNode.Name)
					foundNode.Replace(patchFile)
				if patchNode.action == "REMOVE":
					writeLog("Removing " + foundNode.Name)
					foundNode.Remove()
				if patchNode.action == "PARAM":
					writeLog("Updating params for " + foundNode.Name)
					tempNode = createNodeFromString(patchNode.typeString)
					node.AddChild(tempNode)
					tempNode.Replace(patchFile)
					copyNodeProperties(tempNode, foundNode)
					tempNode.Remove()
			# If a replace node can't be found, add it
			elif patchNode.action == "REPLACE":
				writeLog("Adding " + patchNode.name)
				newNode = createNodeFromString(patchNode.typeString)
				newNode.Name = patchNode.name
				node.AddChild(newNode)
				newNode.Replace(patchFile)
		elif patchNode.action == "ADD":
			writeLog("Adding " + patchNode.name)
			newNode = createNodeFromString(patchNode.typeString)
			newNode.Name = patchNode.name
			node.AddChild(newNode)
			newNode.Replace(patchFile)

def main():
		createLogFile()

		# File prompts
		patchFolder = BrawlAPI.OpenFolderDialog("Select the base folder of the patch")
		file = BrawlAPI.OpenFileDialog("Select the file to patch", "All Files|*.*")
		
		fileOpened = openFile(file)
		if fileOpened:
			node = BrawlAPI.RootNode
			processPatchFiles(patchFolder, node)

main()