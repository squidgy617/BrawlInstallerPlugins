__author__ = "Squidgy"
__version__ = "1.1.0"

from BrawlInstallerLib import *

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
			backupCheck()
			# Get user settings
			if File.Exists(RESOURCE_PATH + '/settings.ini'):
				settings = getSettings()
			else:
				settings = initialSetup()

			#region USER INPUT/PRELIMINARY CHECKS

			# Prompt user to input fighter ID
			fighterId = showIdPrompt("Enter the ID for the fighter you wish to remove")
			fighterId = fighterId.split('0x')[1].upper()

			uninstallFranchiseIcon = BrawlAPI.ShowYesNoPrompt("Do you want to uninstall the fighter's franchise icon?", "Uninstall franchise icon?")
			if settings.installVictoryThemes:
				uninstallVictoryTheme = BrawlAPI.ShowYesNoPrompt("Do you want to uninstall the fighter's victory theme?", "Uninstall victory theme?")
			else:
				uninstallVictoryTheme = False

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
			progressBar.Finish()
			fighterInfo = getFighterInfo(fighterConfig, cosmeticConfig, slotConfig)
			moduleFiles = Directory.GetFiles(MainForm.BuildPath + '/pf/module', 'ft_' + fighterInfo.fighterName + '.rel')
			# Get the fighter this one is cloned from
			clonedModuleName = ""
			if moduleFiles:
				clonedModuleName = getClonedModuleName(moduleFiles[0])

			cosmeticId = fighterInfo.cosmeticId
			#endregion USER INPUT/PRELIMINARY CHECKS

			# Set up progressbar
			progressCounter = 0
			progressBar = ProgressWindow(MainForm.Instance, "Uninstalling Character...", "Uninstalling Character", False)
			progressBar.Begin(0, 15, progressCounter)

			#region SCSELCHARACTER

			# Uninstall CSPs
			removeCSPs(cosmeticId)
			# Uninstall CSS icon
			removeCSSIcon(cosmeticId)
			# Uninstall CSS portrait name
			if settings.installPortraitNames:
				removePortraitName(cosmeticId)
			# Uninstall stock icons from sc_selcharacter
			if settings.installStocksToCSS == "true":
				removeStockIcons(cosmeticId, "Misc Data [90]", "", rootName="", filePath='/pf/menu2/sc_selcharacter.pac', fiftyCC=settings.fiftyCostumeCode)
			# Uninstall franchise icon from sc_selcharacter
			if uninstallFranchiseIcon:
				removeFranchiseIcon(fighterInfo.franchiseIconId, '/pf/menu2/sc_selcharacter.pac')
			# If we did any work in sc_selcharacter, save and close it
			fileOpened = checkOpenFile("sc_selcharacter")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			#endregion SCSELCHARACTER

			#region info.pac

			# Uninstall stock icons from info.pac
			if settings.installStocksToInfo == "true":
				removeStockIcons(cosmeticId, "Misc Data [30]", "Misc Data [30]", rootName="", filePath='/pf/info2/info.pac', fiftyCC=settings.fiftyCostumeCode)
			# Uninstall franchise icon from info.pac
			if uninstallFranchiseIcon:
				removeFranchiseIcon(fighterInfo.franchiseIconId, '/pf/info2/info.pac')
			# Uninstall BP name from info.pac
			if settings.installBPNames == "true":
				removeBPName(cosmeticId, '/pf/info2/info.pac')
			fileOpened = checkOpenFile("info")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)
			
			#endregion info.pac

			#region STGRESULT

			# Uninstall stock icons from STGRESULT
			if settings.installStockIconsToResult == "true":
				removeStockIcons(cosmeticId, "Misc Data [120]", "Misc Data [110]", rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC=settings.fiftyCostumeCode)
			# Uninstall franchise icon from STGRESULT
			if uninstallFranchiseIcon:
				removeFranchiseIconResult(fighterInfo.franchiseIconId)
			fileOpened = checkOpenFile("STGRESULT")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)
			#endregion STGRESULT

			#region Other Stock Icon Locations

			# StockFaceTex.brres - used for things like rotation mode
			if settings.installStocksToStockFaceTex == "true":
				removeStockIcons(cosmeticId, "", "", filePath='/pf/menu/common/StockFaceTex.brres', fiftyCC=settings.fiftyCostumeCode)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
			# sc_selmap - used for SSS in vBrawl
			if settings.installStocksToSSS == "true":
				removeStockIcons(cosmeticId, "Misc Data [40]", "Misc Data [20]", filePath='/pf/menu2/sc_selmap.pac', fiftyCC=settings.fiftyCostumeCode)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)
			#endregion Other Stock Icon Locations

			# Delete BPs
			deleteBPs(cosmeticId, settings.fiftyCostumeCode)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Remove replay icon
			removeReplayIcon(cosmeticId)
			BrawlAPI.SaveFile()
			BrawlAPI.ForceCloseFile()
			progressCounter += 1
			progressBar.Update(progressCounter)

			# Remove victory theme
			if uninstallVictoryTheme:
				removeSongId = getVictoryThemeIDByFighterId(slotId)
				removeVictoryTheme(removeSongId)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Remove soundbank
			# Need soundbank ID to match preferences
			soundbankId = fighterInfo.soundbankId
			modifier = 0 if settings.addSevenToSoundbankName == "false" else 7
			if settings.soundbankStyle == "hex":
				soundbankIdToDelete = str("%x" % (soundbankId + modifier)).upper()
			else:
				soundbankIdToDelete = str(soundbankId + modifier)
			deleteSoundbank(soundbankIdToDelete)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Remove kirby hat
			if settings.kirbyHatExe != "":
				removeKirbyHat(fighterId, settings.kirbyHatExe)
				deleteKirbyHatFiles(fighterInfo.fighterName)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Uninstall fighter files
			deleteFighterFiles(fighterInfo.fighterName)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Delete module file
			deleteModule(fighterInfo.fighterName)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Delete EX configs
			deleteExConfigs(fighterId, slotConfigId=slotId, cosmeticConfigId=cosmeticConfigId, cssSlotConfigId=cssSlotConfigId)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Remove fighter from code menu
			if settings.assemblyFunctionsExe != "":
				removeFromCodeMenu(fighterId, settings.assemblyFunctionsExe)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Remove code edits

			# Remove code changes for throw release points
			updateThrowRelease(fighterId, "EXFighter" + str(fighterId), [ "0.0", "0.0" ])

			# Remove code changes for Lucario clones
			if clonedModuleName == "ft_lucario":
				removeCodeMacro(fighterId, "GFXFix", 0)
				removeCodeMacro(fighterId, "GFXFix", 0, preFindText="bne notKirby")
				removeCodeMacro(fighterId, "BoneIDFixA", 1, True)

			# Remove code changes for Jigglypuff clones
			if clonedModuleName == "ft_purin":
				removeCodeMacro(fighterId, "CloneBones", 0, True)
				removeCodeMacro(fighterId, "CloneGFX", 0, True)
				removeCodeMacro(fighterId, "CloneSFX", 0, True)
			
			# Remove code changes for Dedede clones
			if clonedModuleName == "ft_dedede":
				removeCodeMacro(fighterId, "DededeFix", 0, True)

			# Remove code changes for Bowser clones
			if clonedModuleName == "ft_bowser":
				removeCodeMacro(fighterId, "BoneIDFix", 0, False)

			buildGct()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Remove fighter from roster
			if settings.useCssRoster == "true":
				removeFromRoster(fighterId)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressBar.Finish()
			archiveBackup()
			BrawlAPI.ShowMessage("Character successfully uninstalled.", "Success")
		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()


main()