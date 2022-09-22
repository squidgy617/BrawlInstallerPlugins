__author__ = "Squidgy"
__version__ = "1.3.0"

from BrawlInstallerLib import *

def main():
		Directory.CreateDirectory(AppPath + '/temp')
		updateTrophyCode('41', '0x123', 'RockmanX')
		#addTrophy("TestTrophy", 0, 0, "Test Trophy4", "TEST GAME4", "TEST GAME THE SEQUEL4", "THIS IS A TEST GAME4", 0, 0, 631)

main()