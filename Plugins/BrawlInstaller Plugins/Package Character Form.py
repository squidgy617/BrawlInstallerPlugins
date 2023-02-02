__author__ = "Squidgy"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		form = PackageCharacterForm()
		result = form.ShowDialog(MainForm.Instance)
		while(result == DialogResult.Retry):
			zipFile = form.zipFile
			form.Dispose()
			form = PackageCharacterForm(zipFile)
			result = form.ShowDialog(MainForm.Instance)
		form.Dispose()
		if Directory.Exists(TEMP_PATH):
			Directory.Delete(TEMP_PATH, 1)

main()