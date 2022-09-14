__author__ = "Squidgy"
__version__ = "1.3.0"

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
				BrawlAPI.ShowMessage("Build path does not appear to be valid. Please change your build path by going to 'Tools > Settings' and modifying the 'Default Build Path' field.\n\nYour build path should contain a folder named 'pf' within it.")
				return
			createLogFile()

			# Prompt user to input fighter ID
			fighterId = showIdPrompt("Enter the ID for the fighter you wish to extract")
			fighterId = fighterId.split('0x')[1].upper()

			destination = BrawlAPI.OpenFolderDialog("Select destination for extracted character package")

			# Get fighter info

			# Set up progressbar
			progressCounter = 0
			progressBar = ProgressWindow(MainForm.Instance, "Redirect Check...", "Checking for Ex Config redirects", False)
			progressBar.Begin(0, 3, progressCounter)

			fighterConfig = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig', "Fighter" + fighterId + ".dat")[0]
			# Slot configs
			for config in Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig', "Slot*.dat"):
				BrawlAPI.OpenFile(config)
				if BrawlAPI.RootNode.SetSlot == True and BrawlAPI.RootNode.CharSlot1 == int(fighterId, 16):
					slotConfig = config
					slotId = str(getFileInfo(config).Name.split('Slot')[1]).replace('.dat', '')
				BrawlAPI.ForceCloseFile()
			if 'slotConfig' not in locals():
				slotConfig = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig', "Slot" + fighterId + ".dat")[0]
				slotId = str(fighterId)
			progressCounter += 1
			progressBar.Update(progressCounter)
			# Cosmetic configs
			for config in Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig', "Cosmetic*.dat"):
				BrawlAPI.OpenFile(config)
				if BrawlAPI.RootNode.HasSecondary == True and BrawlAPI.RootNode.CharSlot1 == int(slotId, 16):
					cosmeticConfig = config
					cosmeticConfigId = str(getFileInfo(config).Name.split('Cosmetic')[1]).replace('.dat', '')
				BrawlAPI.ForceCloseFile()
			if 'cosmeticConfig' not in locals():
				cosmeticConfig = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig', "Cosmetic" + fighterId + ".dat")[0]
				cosmeticConfigId = str(fighterId)
			progressCounter += 1
			progressBar.Update(progressCounter)
			# CSS Slot configs
			for config in Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig', 'CSSSlot*.dat'):
				BrawlAPI.OpenFile(config)
				if (BrawlAPI.RootNode.SetPrimarySecondary == True and BrawlAPI.RootNode.CharSlot1 == int(slotId, 16)) or (BrawlAPI.RootNode.SetCosmeticSlot == True and BrawlAPI.RootNode.CosmeticSlot == int(cosmeticConfigId, 16)):
					cssSlotConfig = config
					cssSlotConfigId = str(getFileInfo(config).Name.split('CSSSlot')[1]).replace('.dat', '')
			if 'cssSlotConfig' not in locals():
				cssSlotConfig = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig', "Cosmetic" + fighterId + ".dat")[0]
				cssSlotConfigId = str(fighterId)
			progressCounter += 1
			progressBar.Update(progressCounter)
			progressBar.Finish()
			fighterInfo = getFighterInfo(fighterConfig, cosmeticConfig, slotConfig)
			extractCharacter(fighterId, destination, fighterInfo, slotId, cosmeticConfigId, cssSlotConfigId)
		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")


main()