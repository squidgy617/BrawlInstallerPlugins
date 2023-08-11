__author__ = "Squidgy"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		createLogFile()

		# If temporary directory already exists, delete it to prevent duplicate files
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)
		createDirectory(TEMP_PATH)

		# File prompts
		buildPatchFile = BrawlAPI.OpenFileDialog("Select the build patch file to install", "BUILDPATCH File|*.buildpatch")
		if not buildPatchFile:
			return
		
		try:
			backupCheck()
			applyBuildPatch(buildPatchFile)
			archiveBackup()
		except Exception as e:
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Build patch did not complete. Backups restored.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()
			return
		

main()