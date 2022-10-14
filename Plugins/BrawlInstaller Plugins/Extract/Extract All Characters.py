__author__ = "Squidgy"
__version__ = "1.5.0"

from BrawlInstallerLib import *
from ExtractLib import *

def main():
		try: 
			if str(BrawlAPI.RootNode) != "None":
				BrawlAPI.CloseFile()
			if not MainForm.BuildPath:
				BrawlAPI.ShowMessage("Build path must be set. This can be done by navigating to Tools > Settings > General and setting the 'Default Build Path' to the path to your build's root folder.", "Build Path Not Set")
				return
			if not Directory.Exists(MainForm.BuildPath + '/pf/'):
				BrawlAPI.ShowMessage("Build path does not appear to be valid. Please change your build path by going to 'Tools > Settings' and modifying the 'Default Build Path' field.\n\nYour build path should contain a folder named 'pf' within it.", "Invalid Build Path")
				return
			createLogFile()

			destination = BrawlAPI.OpenFolderDialog("Select destination for extracted character package")

			# Get fighter info
			fighterList = getAllFighterInfo()
			
			for fighter in fighterList:
				if fighter.fighterId and fighter.slotConfigId and fighter.cosmeticConfigId and fighter.cssSlotConfigId:
					extractCharacter(fighter.fighterId, destination, fighter, fighter.slotConfigId, fighter.cosmeticConfigId, fighter.cssSlotConfigId, True)
			BrawlAPI.ShowMessage("Characters extracted to " + destination, "Success")
		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")


main()