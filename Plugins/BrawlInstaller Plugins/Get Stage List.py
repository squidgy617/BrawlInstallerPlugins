__author__ = "Squidgy"
__version__ = "1.6.0"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		createLogFile()
		form = StageList()
		result = form.ShowDialog(MainForm.Instance)

main()