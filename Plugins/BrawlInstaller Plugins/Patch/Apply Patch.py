__author__ = "Squidgy"

from PatchLib import *
from BrawlInstallerForms import *

def processPatchFiles(patchFolder, node, progressBar):
	writeLog("Processing patch files")
	# Drill down into any directories in the patch
	for directory in Directory.GetDirectories(patchFolder):
		patchNode = PatchNode(DirectoryInfo(directory).Name, directory)
		newNode = findNodeToPatch(node, patchNode)
		# If a matching container node doesn't exist, create it
		if not newNode:
			newNode = createNodeFromString(patchNode.typeString)
			newNode.Name = patchNode.name
			node.InsertChild(newNode, patchNode.containerIndex)
		if newNode:
			processPatchFiles(directory, newNode, progressBar)
		if newNode.GetType().IsSubclassOf(ARCEntryNode):
			filePath = patchNode.path + "$$S"
			# If there's a settings file, apply the special settings
			if File.Exists(filePath):
				fileText = File.ReadAllLines(filePath)
				fileType = readValueFromKey(fileText, "FileType")
				if fileType:
					newNode.FileType = ARCFileType[fileType]
				newNode.FileIndex = int(readValueFromKey(fileText, "FileIndex"))
				newNode.GroupID = int(readValueFromKey(fileText, "GroupID"))
				newNode.RedirectIndex = int(readValueFromKey(fileText, "RedirectIndex"))
				newNode.RedirectTarget = readValueFromKey(fileText, "RedirectTarget")
		progressBar.CurrentValue += 1
		progressBar.Update()
	# Import any node files in the directory
	for patchFile in Directory.GetFiles(patchFolder):
		writeLog("Processing patch file " + patchFile)
		patchNode = PatchNode(getFileInfo(patchFile).Name, patchFile)
		# Handle each node file based on the defined action
		if patchNode.action in [ "REPLACE", "REMOVE", "PARAM", "ADD" ]:
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
			elif patchNode.action == "REPLACE" or patchNode.action == "ADD":
				writeLog("Adding " + patchNode.name)
				newNode = createNodeFromString(patchNode.typeString)
				newNode.Name = patchNode.name
				node.InsertChild(newNode, patchNode.containerIndex)
				newNode.Replace(patchFile)
		# elif patchNode.action == "ADD":
		# 	writeLog("Adding " + patchNode.name)
		# 	newNode = createNodeFromString(patchNode.typeString)
		# 	newNode.Name = patchNode.name
		# 	node.AddChild(newNode)
		# 	newNode.Replace(patchFile)
		progressBar.CurrentValue += 1
		progressBar.Update()

def main():
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
		
		unzipFile(patchFile)
		
		form = PatcherForm(TEMP_PATH)
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.OK:
			for removedNode in form.uncheckedNodes:
				# Always delete info for unchecked nodes
				if File.Exists(removedNode.path.replace(".tex0", "") + "$$I"):
					File.Delete(removedNode.path.replace(".tex0", "") + "$$I")
				# For containers, remove all associated nodes when they are unchecked
				if removedNode.type.FullName in CONTAINERS:
					if File.Exists(removedNode.path + "$$P"):
						File.Delete(removedNode.path + "$$P")
					if File.Exists(removedNode.path + "$$S"):
						File.Delete(removedNode.path + "$$S")
					if Directory.Exists(removedNode.path):
						Directory.Delete(removedNode.path, True)
				else:
					if File.Exists(removedNode.path):
						File.Delete(removedNode.path)
		
			fileOpened = openFile(file)
			if fileOpened:
				patchFolder = TEMP_PATH
				node = BrawlAPI.RootNode
				try:
					# Set up progressbar
					totalNodes = len(Directory.GetFiles(patchFolder, "*", SearchOption.AllDirectories)) + len(Directory.GetDirectories(patchFolder, "*", SearchOption.AllDirectories))
					progressBar = ProgressWindow(MainForm.Instance, "Applying patch...", "Patching", False)
					progressBar.Begin(0, totalNodes, 0)
					processPatchFiles(patchFolder, node, progressBar)
					progressBar.Finish()
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()
					BrawlAPI.ShowMessage("File patched successfully", "Success")
				except Exception as e:
					writeLog("ERROR " + str(e))
					if 'progressBar' in locals():
						progressBar.Finish()
					BrawlAPI.ForceCloseFile()
					BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
					BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
					restoreBackup()
					archiveBackup()
		
		archiveBackup()
		
		# Delete temporary directory
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)

main()