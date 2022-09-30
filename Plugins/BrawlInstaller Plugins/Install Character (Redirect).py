__author__ = "Squidgy"
__version__ = "1.4.0"

from InstallLib import *

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
			backupCheck()

			# Prompt user to input IDs
			fighterId = showIdPrompt("Enter your desired fighter ID")
			fighterId = fighterId.split('0x')[1].upper()

			slotConfigId = showIdPrompt("Enter your desired slot config ID")
			slotConfigId = slotConfigId.split('0x')[1].upper()

			cosmeticConfigId = showIdPrompt("Enter your desired cosmetic config ID")
			cosmeticConfigId = cosmeticConfigId.split('0x')[1].upper()

			cssSlotConfigId = showIdPrompt("Enter your desired CSS slot config ID")
			cssSlotConfigId = cssSlotConfigId.split('0x')[1].upper()

			installCharacter(fighterId=fighterId, cosmeticConfigId=cosmeticConfigId, slotConfigId=slotConfigId, cssSlotConfigId=cssSlotConfigId)
		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()



main()