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
		
		fileName = createPatch(cleanFile, alteredFile)
		
		form = PatcherForm(TEMP_PATH)
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.OK:
			updatePatch(form)

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