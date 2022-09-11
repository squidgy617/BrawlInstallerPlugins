__author__ = "Squidgy"
__version__ = "1.3.0"

from BrawlInstallerLib import *

def main():
		if str(BrawlAPI.RootNode) != "None":
			BrawlAPI.CloseFile()
		if not MainForm.BuildPath:
			BrawlAPI.ShowMessage("Build path must be set. This can be done by navigating to Tools > Settings > General and setting the 'Default Build Path' to the path to your build's root folder.", "Build Path Not Set")
			return
		if not Directory.Exists(MainForm.BuildPath + '/pf/'):
			BrawlAPI.ShowMessage("Build path does not appear to be valid. Please change your build path by going to 'Tools > Settings' and modifying the 'Default Build Path' field.\n\nYour build path should contain a folder named 'pf' within it.")
			return
		createLogFile()
		infoLines = []
		firstLine = 'FighterID Name CosmeticID FranchiseID Soundbank EffectID SongID'
		formattedFirstLine = "{: <9} {: <20} {: <10} {: <11} {: <10} {: <8} {: <6}".format(*firstLine.split(' '))
		infoLines.append(formattedFirstLine)
		fighterConfigs = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig')
		for fighterConfig in fighterConfigs:
			fighterId = FileInfo(fighterConfig).Name.split('Fighter')[1].split('.dat')[0]
			cosmeticConfig = getCosmeticConfig(fighterId)
			slotConfig = getSlotConfig(fighterId)
			fighterInfo = getFighterInfo(fighterConfig, cosmeticConfig, slotConfig)
			effectId = getEffectId(fighterInfo.fighterName)
			infoLine = str(int(fighterId, 16)) + ' ' + fighterInfo.fighterName + ' ' + str(fighterInfo.cosmeticId) + ' ' + str(fighterInfo.franchiseIconId) + ' ' + str(fighterInfo.soundbankId) + ' ' + str(effectId) + ' ' + str(fighterInfo.songId)
			formattedLine = "{: <9} {: <20} {: <10} {: <11} {: <10} {: <8} {: <6}".format(*infoLine.split(' '))
			infoLines.append(formattedLine)
		finalPrint = ""
		for line in infoLines:
			finalPrint = finalPrint + '\n' + line
		File.WriteAllText(RESOURCE_PATH + '/fighter_info.txt', finalPrint)
		BrawlAPI.ShowMessage("Wrote text file to " + RESOURCE_PATH + '\\fighter_info.txt', "Success")

main()