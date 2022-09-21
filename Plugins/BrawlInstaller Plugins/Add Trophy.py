__author__ = "Squidgy"
__version__ = "1.3.0"

from BrawlInstallerLib import *

def main():
		Directory.CreateDirectory(AppPath + '/temp')
		addTrophy("TestTrophy", 0, 0, "Test Trophy2", "TEST GAME2", "TEST GAME THE SEQUEL2", "THIS IS A TEST GAME2", 0, 0, 1088, 1089, 544)

main()