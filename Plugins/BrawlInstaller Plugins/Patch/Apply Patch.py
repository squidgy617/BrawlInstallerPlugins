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
		try:
			createLogFile()
			backupCheck()

			# If temporary directory already exists, delete it to prevent duplicate files
			if Directory.Exists(TEMP_PATH):
				Directory.Delete(TEMP_PATH, 1)
			createDirectory(TEMP_PATH)

			# File prompts
			patchFile = BrawlAPI.OpenFileDialog("Select the patch file to install", "ZIP File|*.zip")
			if not patchFile:
				return
			file = BrawlAPI.OpenFileDialog("Select the file to patch", "All Files|*.*")
			if not file:
				return
			
			fileOpened = openFile(file)
			if fileOpened:
				unzipFile(patchFile)
				patchFolder = TEMP_PATH
				node = BrawlAPI.RootNode
				processPatchFiles(patchFolder, node)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
				BrawlAPI.ShowMessage("File patched successfully", "Success")
			
			archiveBackup()
			
			# Delete temporary directory
			if Directory.Exists(TEMP_PATH):
				Directory.Delete(TEMP_PATH, 1)
		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()

main()