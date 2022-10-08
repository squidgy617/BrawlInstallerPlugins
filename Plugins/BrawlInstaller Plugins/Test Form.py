__author__ = "Squidgy"
__version__ = "1.5.0"

from InstallLib import *
from UninstallLib import *
from BrawlInstallerForms import *
from System.Drawing import Bitmap

def main():
		form = CharacterForm()
		result = form.ShowDialog(MainForm.Instance)

main()