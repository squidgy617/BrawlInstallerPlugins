__author__ = "Squidgy"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		# Initial checks
		if str(BrawlAPI.RootNode) != "None":
			BrawlAPI.CloseFile()
		if not MainForm.BuildPath:
			BrawlAPI.ShowMessage("Build path must be set. This can be done by navigating to Tools > Settings > General and setting the 'Default Build Path' to the path to your build's root folder.", "Build Path Not Set")
			return
		if not Directory.Exists(MainForm.BuildPath + '/pf/'):
			BrawlAPI.ShowMessage("Build path does not appear to be valid. Please change your build path by going to 'Tools > Settings' and modifying the 'Default Build Path' field.\n\nYour build path should contain a folder named 'pf' within it.", "Invalid Build Path")
			return

		settings = initialSetup()
		if not settings:
			return
		
		form = UninstallTrophyForm()
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.OK:
			trophy = form.trophyBox.selectedNode
			slotId = hexId(form.slotIdBox.textBox.Text).replace('0x', '') if form.slotIdBox.textBox.Text else ""
			# Uninstall trophy
			try:
				createLogFile()
				backupCheck()
				# If temporary directory already exists, delete it to prevent duplicate files
				if Directory.Exists(TEMP_PATH):
					Directory.Delete(TEMP_PATH, 1)
				createDirectory(TEMP_PATH)
				uninstallTrophyGeneric(trophy, slotId, settings.installToSse)
				if slotId:
					buildGct()
				archiveBackup()
				BrawlAPI.ShowMessage("Trophy uninstalled.", "Success")
			except Exception as e:
				writeLog("ERROR " + str(e))
				if 'progressBar' in locals():
					progressBar.Finish()
				BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
				BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
				restoreBackup()
				archiveBackup()
		form.Dispose()

main()