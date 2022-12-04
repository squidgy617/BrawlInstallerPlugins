__author__ = "Squidgy"
__version__ = "1.6.0"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		createLogFile()
		backupCheck()
		form = MusicList()
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.Abort:
			restoreBackup()
			archiveBackup()

main()