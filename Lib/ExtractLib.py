version = "1.7.0"
# ExtractLib
# Library for BrawlInstaller's extraction plugins

from BrawlInstallerLib import *

def extractCharacter(fighterId, destination, fighterInfo=0, slotId="", cosmeticConfigId="", cssSlotConfigId="", skipMessage=False):
		try:
			# Get user settings
			if File.Exists(MainForm.BuildPath + '/settings.ini'):
				settings = getSettings()
			else:
				settings = initialSetup()
			# If temporary directory already exists, delete it to prevent duplicate files
			if Directory.Exists(AppPath + '/temp'):
				Directory.Delete(AppPath + '/temp', 1)
			Directory.CreateDirectory(AppPath + '/temp')

			#region USER INPUT/PRELIMINARY CHECKS
			stocksExtracted = False

			if not fighterInfo:
				fighterConfig = getFighterConfig(fighterId)
				cosmeticConfig = getCosmeticConfig(cosmeticConfigId)
				slotConfig = getSlotConfig(slotId)
				fighterInfo = getFighterInfo(fighterConfig, cosmeticConfig, slotConfig)
			moduleFiles = Directory.GetFiles(MainForm.BuildPath + '/pf/module', 'ft_' + fighterInfo.fighterName + '.rel')
			# Get the fighter this one is cloned from
			clonedModuleName = ""
			if moduleFiles:
				clonedModuleName = getClonedModuleName(moduleFiles[0])

			cosmeticId = fighterInfo.cosmeticId
			fighterSettings = FighterSettings()

			#endregion USER INPUT/PRELIMINARY CHECKS

			# Set up progressbar
			progressCounter = 0
			progressBar = ProgressWindow(MainForm.Instance, "Extracting Character...", "Extracting Character", False)
			progressBar.Begin(0, 17, progressCounter)

			# Extract CSPs
			extractCSPs(cosmeticId)

			#region SCSELCHARACTER

			# Extract CSS icon
			extractCSSIcon(cosmeticId, settings.cssIconStyle)
			
			# Extract CSS portrait name
			extractPortraitName(cosmeticId, settings.portraitNameStyle)

			# Extract stock icons
			if settings.installStocksToCSS == "true":
				extractStockIcons(cosmeticId, "Misc Data [90]", filePath='/pf/menu2/sc_selcharacter.pac', fiftyCC=settings.fiftyCostumeCode)
				stocksExtracted = True

			# Extract franchise icon
			extractFranchiseIcon(fighterInfo.franchiseIconId, '/pf/menu2/sc_selcharacter.pac')

			# If we did any work in sc_selcharacter, close it
			fileOpened = checkOpenFile("sc_selcharacter")
			if fileOpened:
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			#endregion SCSELCHARACTER

			#region info.pac

			# Extract stock icons if we haven't yet
			if settings.installStocksToInfo == "true" and not stocksExtracted:
				extractStockIcons(cosmeticId, "Misc Data [30]", filePath='/pf/info2/info.pac', fiftyCC=settings.fiftyCostumeCode)

			# Extract BP names
			if settings.installBPNames == "true":
				extractBPName(cosmeticId, '/pf/info2/info.pac', settings.bpStyle)

			fileOpened = checkOpenFile("info")
			if fileOpened:
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			#endregion info.pac

			#region Single Player Cosmetics
			
			# Extract Classic intro
			extractClassicIntro(cosmeticId)

			progressCounter += 1
			progressBar.Update(progressCounter)

			#endregion Single Player Cosmetics

			#region STGRESULT

			# Extract stock icons if we haven't yet
			if settings.installStockIconsToResult == "true" and not stocksExtracted:
				extractStockIcons(cosmeticId, "Misc Data [120]", rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC=settings.fiftyCostumeCode)

			# Extract transparent franchise icon from STGRESULT
			extractFranchiseIconResult(fighterInfo.franchiseIconId)

			fileOpened = checkOpenFile("STGRESULT")
			if fileOpened:
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)
			#endregion STGRESULT

			#region Other Stock Icon Locations

			# StockFaceTex.brres - used for things like rotation mode
			if settings.installStocksToStockFaceTex == "true":
				extractStockIcons(cosmeticId, "", filePath='/pf/menu/common/StockFaceTex.brres', fiftyCC=settings.fiftyCostumeCode)
				BrawlAPI.ForceCloseFile()
			# sc_selmap - used for SSS in vBrawl
			if settings.installStocksToSSS == "true":
				extractStockIcons(cosmeticId, "Misc Data [40]", filePath='/pf/menu2/sc_selmap.pac', fiftyCC=settings.fiftyCostumeCode)
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			#endregion Other Stock Icon Locations

			# Extract BPs
			extractBPs(cosmeticId, settings.bpStyle, settings.fiftyCostumeCode)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract replay icon
			extractReplayIcon(cosmeticId)
			BrawlAPI.ForceCloseFile()
			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract victory theme
			extractSongId = getVictoryThemeIDByFighterId(slotId)
			extractSong(extractSongId)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract soundbank
			# Need soundbank ID to match preferences
			soundbankId = fighterInfo.soundbankId
			modifier = 0 if settings.addSevenToSoundbankName == "false" else 7
			if settings.soundbankStyle == "hex":
				soundbankIdToExtract = str("%x" % (soundbankId + modifier)).upper()
			else:
				soundbankIdToExtract = str(soundbankId + modifier)
			extractSoundbank(soundbankIdToExtract)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract kirby hat
			extractKirbyHat(fighterId, fighterInfo.fighterName)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract fighter files
			extractFighterFiles(fighterInfo.fighterName)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract module file
			extractModuleFile(fighterInfo.fighterName)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract EX configs
			extractExConfigs(fighterId, slotConfigId=slotId, cosmeticConfigId=cosmeticConfigId, cssSlotConfigId=cssSlotConfigId)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract ending files
			extractEndingFiles(fighterInfo.fighterName, cosmeticConfigId)

			# Extract credits theme
			creditsThemeId = extractCreditsSong(slotId)

			# Extract trophy stuff
			extractTrophy(slotId)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract SSE CSS icon
			if settings.cssIconStyle != "vBrawl":
				extractCSSIconSSE(cosmeticId)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Extract code edits

			# Extract throw release point
			throwRelease = readThrowRelease(fighterId)
			if throwRelease:
				if throwRelease[0] != "0.0" and throwRelease[1] != "0.0":
					fighterSettings.throwReleasePoint = throwRelease[0] + "," + throwRelease[1]

			# Set credits theme ID if we didn't find a file
			if creditsThemeId:
				fighterSettings.creditsThemeId = str(creditsThemeId)

			# Extract Lucario settings
			if clonedModuleName == "ft_lucario":
				fighterSettings.lucarioKirbyEffectId = readCodeMacro(fighterId, "GFXFix", 0, "bne notKirby", returnPosition=1)
				fighterSettings.lucarioBoneId = readCodeMacro(fighterId, "BoneIDFixA", 1, returnPosition=2)

			# Extract Jigglypuff settings
			if clonedModuleName == "ft_purin":
				fighterSettings.jigglypuffBoneId = readCodeMacro(fighterId, "CloneBones", 0, returnPosition=1)
				fighterSettings.jigglypuffEFLSId = readCodeMacro(fighterId, "CloneGFX", 0, returnPosition=2)
				jigglypuffSfxIds = []
				jigglypuffSfxIds.append(readCodeMacro(fighterId, "CloneSFX", 0, preFindText="HOOK @ $80ACAE3C", returnPosition=1))
				jigglypuffSfxIds.append(readCodeMacro(fighterId, "CloneSFX", 0, preFindText="HOOK @ $80ACAE60", returnPosition=1))
				jigglypuffSfxIds.append(readCodeMacro(fighterId, "CloneSFX", 0, preFindText="HOOK @ $80ACF704", returnPosition=1))
				jigglypuffSfxIds.append(readCodeMacro(fighterId, "CloneSFX", 0, preFindText="HOOK @ $80ACA09C", returnPosition=1))
				fighterSettings.jigglypuffSfxIds = ""
				for sfxId in jigglypuffSfxIds:
					if sfxId:
						fighterSettings.jigglypuffSfxIds = fighterSettings.jigglypuffSfxIds + ("," if fighterSettings.jigglypuffSfxIds != "" else "") + sfxId

			# Extract Bowser settings
			if clonedModuleName == "ft_bowser":
				fighterSettings.bowserBoneId = readCodeMacro(fighterId, "BoneIDFix", 0, preFindText=".macro BoneIDFix(<FighterID>, <BoneID>)", returnPosition=1)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Write fighter settings
			attrs = vars(fighterSettings)
			writeString = '\n'.join("%s = %s" % item for item in attrs.items())
			if writeString:
				File.WriteAllText(AppPath + '/temp/FighterSettings.txt', writeString)

			# Create package
			filePath = destination + '/' + fighterInfo.fighterName + '.zip'
			if File.Exists(filePath):
				File.Delete(filePath)
			ZipFile.CreateFromDirectory(AppPath + '/temp', filePath)

			progressCounter += 1
			progressBar.Update(progressCounter)
			progressBar.Finish()

			if not skipMessage:
				BrawlAPI.ShowMessage("Fighter package created at " + destination + '\\' + fighterInfo.fighterName + '.zip', "Success")

			# Delete temporary directory
			Directory.Delete(AppPath + '/temp', 1)
		except Exception as e:
			if 'progressBar' in locals():
				progressBar.Finish()
			raise e
			