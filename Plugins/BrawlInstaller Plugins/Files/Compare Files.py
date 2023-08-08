__author__ = "Squidgy"

from PatchLib import *
from BrawlInstallerLib import *
from BrawlInstallerForms import *
from BrawlLib.SSBB import SupportedFilesHandler

def main():
		createLogFile()

		# If temporary directory already exists, delete it to prevent duplicate files
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)
		createDirectory(TEMP_PATH)

		# File prompts
		cleanFile = BrawlAPI.OpenFileDialog("Select the base file for your patch", SupportedFilesHandler.CompleteFilterEditableOnly)
		if not cleanFile:
			return
		alteredFile = BrawlAPI.OpenFileDialog("Select the altered file for your patch", SupportedFilesHandler.CompleteFilterEditableOnly)
		if not alteredFile:
			return
		
		try:
			fileName = createPatch(cleanFile, alteredFile)
		except Exception as e:
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. File comparison did not complete.", "An Error Has Occurred")
			return
		
		form = PatcherForm(TEMP_PATH)
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.OK and form.action == "save":
			updatePatch(form)

			# Package the patch
			saveDialog = SaveFileDialog()
			saveDialog.Filter = "BPATCH File|*.bpatch"
			saveDialog.Title = "Save patch file"
			saveDialog.FileName = fileName + ".bpatch"
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
		elif result == DialogResult.OK and form.action == "apply":
			updatePatch(form)
			applyPatch(cleanFile)
			form.Dispose()
		else:
			form.Dispose()

		# Delete temporary directory
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)

main()