__author__ = "Squidgy"
__version__ = "1.7.0"

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
		backupCheck()
		form = StageList()
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.Abort:
			restoreBackup()
			archiveBackup()

main()