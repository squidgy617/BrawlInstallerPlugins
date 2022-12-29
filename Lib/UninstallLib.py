# UninstallLib
# Library for BrawlInstaller's uninstallation plugins

from BrawlInstallerLib import *
from BrawlLib.CustomLists import *

#region UNINSTALL COSTUME

def uninstallCostume(cosmeticId, fighterId, cssSlotConfigId, position, skipPositions=[], skipMessage=False):
		try: 
			# Get user settings
			if File.Exists(MainForm.BuildPath + '/settings.ini'):
				settings = getSettings()
			else:
				settings = initialSetup()
			if not settings:
				return
			# If temporary directory already exists, delete it to prevent duplicate files
			if Directory.Exists(AppPath + '/temp'):
				Directory.Delete(AppPath + '/temp', 1)

			fighterConfig = ""
			fighterInfo = ""
			if Directory.Exists(MainForm.BuildPath + '/pf/BrawlEx'):
				fighterConfig = getFighterConfig(fighterId)
				fighterInfo = getFighterInfo(fighterConfig, "", "")

			# Set up progressbar
			progressCounter = 0
			progressBar = ProgressWindow(MainForm.Instance, "Uninstalling Costume...", "Uninstalling Costume", False)
			progressBar.Begin(0, 5, progressCounter)

			# sc_selcharacter
			indexes = subtractCSPs(cosmeticId, settings.rspLoading, position, skipPositions=skipPositions)
			if settings.installStocksToCSS == "true":
				subtractStockIcons(cosmeticId, indexes[0], "Misc Data [90]", "", rootName="", filePath='/pf/menu2/sc_selcharacter.pac', fiftyCC=settings.fiftyCostumeCode)
		
			# If we did any work in sc_selcharacter, save and close it
			fileOpened = checkOpenFile("sc_selcharacter")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# BPs
			deleteBPs(cosmeticId, settings.fiftyCostumeCode, indexes[0], indexes[1])
			incrementBPNames(cosmeticId, indexes[1], increment=(-1 * ((indexes[1] - indexes[0]) + 1)), fiftyCC=settings.fiftyCostumeCode)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Stock icons
			# STGRESULT
			if settings.installStockIconsToResult == "true":
				subtractStockIcons(cosmeticId, indexes[0], "Misc Data [120]", "Misc Data [110]", endIndex=indexes[1], rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC=settings.fiftyCostumeCode)
				fileOpened = checkOpenFile("STGRESULT")
				if fileOpened:
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()

			# info.pac
			if settings.installStocksToInfo == "true":
				subtractStockIcons(cosmeticId, indexes[0], "Misc Data [30]", "Misc Data [30]", endIndex=indexes[1], rootName="", filePath='/pf/info2/info.pac', fiftyCC=settings.fiftyCostumeCode)
				fileOpened = checkOpenFile("info")
				if fileOpened:
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()

			# StockFaceTex
			if settings.installStocksToStockFaceTex == "true":
				subtractStockIcons(cosmeticId, indexes[0], "", "", endIndex=indexes[1], filePath='/pf/menu/common/StockFaceTex.brres', fiftyCC=settings.fiftyCostumeCode)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			# sc_selmap
			if settings.installStocksToSSS == "true":
				subtractStockIcons(cosmeticId, indexes[0], "Misc Data [40]", "Misc Data [20]", endIndex=indexes[1], filePath='/pf/menu2/sc_selmap.pac', fiftyCC=settings.fiftyCostumeCode)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
			
			progressCounter += 1
			progressBar.Update(progressCounter)

			# Ex Config
			costumeIds = removeCssSlots(indexes[0], indexes[1], cssSlotConfigId)
			progressCounter += 1
			progressBar.Update(progressCounter)

			# Costume files
			if fighterInfo:
				fighterName = fighterInfo.fighterName
			else:
				if not FighterNameGenerators.generated:
					FighterNameGenerators.GenerateLists()
				fighterName = FighterNameGenerators.FromID(int(fighterId, 16), 16, "X")
			deleteCostumeFiles(costumeIds, fighterName)

			progressCounter += 1
			progressBar.Update(progressCounter)
			progressBar.Finish()
			
			if not skipMessage:
				BrawlAPI.ShowMessage("Costume uninstalled successfully.", "Success")

		except Exception as e:
			if 'progressBar' in locals():
				progressBar.Finish()
			raise e

#endregion UNINSTALL COSTUME