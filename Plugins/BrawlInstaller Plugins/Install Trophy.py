__author__ = "Squidgy"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		form = TrophyForm()
		result = form.ShowDialog(MainForm.Instance)
		form.Dispose()

main()