__author__ = "Squidgy"
__version__ = "1.0.0"

from BrawlInstallerLib import *

def main():
		if Directory.Exists(BACKUP_PATH):
			backupFiles = Directory.GetFiles(BACKUP_PATH, "*", SearchOption.AllDirectories)
			for file in backupFiles:
				Directory.CreateDirectory(file.replace(BACKUP_PATH, MainForm.BuildPath).replace(FileInfo(file).Name, ''))
				File.Copy(file, file.replace(BACKUP_PATH, MainForm.BuildPath), True)
			BrawlAPI.ShowMessage("Backup restored.", "Success")

main()