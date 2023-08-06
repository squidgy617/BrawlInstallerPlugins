__author__ = "Squidgy"

from PatchLib import *
from BrawlInstallerForms import *

def main():
		createLogFile()

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
			updatePatch(form)
			applyPatch(file)
		
		# Delete temporary directory
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)

main()