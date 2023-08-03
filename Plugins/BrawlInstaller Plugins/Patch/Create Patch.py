__author__ = "Squidgy"

from PatchLib import *
from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		createLogFile()

		# If temporary directory already exists, delete it to prevent duplicate files
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)
		createDirectory(TEMP_PATH)

		# File prompts
		cleanFile = BrawlAPI.OpenFileDialog("Select the base file for your patch", "All Files|*.*")
		if not cleanFile:
			return
		alteredFile = BrawlAPI.OpenFileDialog("Select the altered file for your patch", "All Files|*.*")
		if not alteredFile:
			return
		
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
				if '$$FOLDER' in directoryInfo.Name:
					#BrawlAPI.ShowMessage(directoryInfo.Parent.FullName + '\\' + directoryInfo.Name.replace('$$FOLDER', '$$REMOVE'), "")
					if File.Exists(directoryInfo.Parent.FullName + '\\' + directoryInfo.Name.replace('$$FOLDER', '$$REMOVE')):
						Directory.Delete(directories[i], True)
			i += 1

		form = PatcherForm(TEMP_PATH)
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.OK:
			for removedNode in form.uncheckedNodes:
				if removedNode.action == "FOLDER":
					if File.Exists(removedNode.path.replace(removedNode.originalString, removedNode.originalString.replace("$$FOLDER", "$$PARAM"))):
						File.Delete(removedNode.path.replace(removedNode.originalString, removedNode.originalString.replace("$$FOLDER", "$$PARAM")))
					if File.Exists(removedNode.path.replace(removedNode.originalString, removedNode.originalString.replace("$$FOLDER", "$$SETTINGS"))):
						File.Delete(removedNode.path.replace(removedNode.originalString, removedNode.originalString.replace("$$FOLDER", "$$SETTINGS")))
					if Directory.Exists(removedNode.path):
						Directory.Delete(removedNode.path, True)
				else:
					if File.Exists(removedNode.path):
						File.Delete(removedNode.path)

			# Package the patch
			saveDialog = SaveFileDialog()
			saveDialog.Filter = "ZIP File|*.zip"
			saveDialog.Title = "Save patch file"
			saveDialog.FileName = fileName + ".zip"
			result = saveDialog.ShowDialog()
			if result == DialogResult.OK and saveDialog.FileName:
				filePath = saveDialog.FileName
			
				if File.Exists(filePath):
					File.Delete(filePath)
				if Directory.Exists(TEMP_PATH):
					ZipFile.CreateFromDirectory(TEMP_PATH, filePath)
					Directory.Delete(TEMP_PATH, 1)
					BrawlAPI.ShowMessage("Patch file created at " + filePath, "Success")
				else:
					BrawlAPI.ShowMessage("Patch file is empty. No patch file created.", "Empty Patch File")
					
			saveDialog.Dispose()

		form.Dispose()

		# Delete temporary directory
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)

main()