__author__ = "Squidgy"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		form = PackageCharacterForm()
		result = form.ShowDialog(MainForm.Instance)
		form.Dispose()

main()