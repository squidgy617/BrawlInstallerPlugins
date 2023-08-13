__author__ = "Squidgy"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		if str(BrawlAPI.RootNode) != "None":
			BrawlAPI.CloseFile()
		if not MainForm.BuildPath:
			BrawlAPI.ShowMessage("Build path must be set. This can be done by navigating to Tools > Settings > General and setting the 'Default Build Path' to the path to your build's root folder.", "Build Path Not Set")
			return
		if not Directory.Exists(MainForm.BuildPath + '/pf/'):
			BrawlAPI.ShowMessage("Build path does not appear to be valid. Please change your build path by going to 'Tools > Settings' and modifying the 'Default Build Path' field.\n\nYour build path should contain a folder named 'pf' within it.", "Invalid Build Path")
			return
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
			BrawlAPI.ShowMessage("Build patch applied.", "Success")
		except Exception as e:
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Build patch did not complete. Backups restored.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()
			return
		

main()