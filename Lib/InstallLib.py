# InstallLib
# Library for BrawlInstaller's installation plugins

from BrawlInstallerLib import *
from BrawlLib.CustomLists import *
from BrawlInstallerForms import *

#region INSTALL CHARACTER

def installCharacter(fighterId="", cosmeticId=0, franchiseIconId=-1, auto=False, cosmeticConfigId="", slotConfigId="", cssSlotConfigId="", baseCssSlotId="", zipfile=""):
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
			# Prompt the user to pick a zip file
			if not zipfile:
				zipfile = BrawlAPI.OpenFileDialog("Select fighter zip file", "Zip files|*.zip")
			if zipfile:
				# Unzip the file and get temp path
				unzipFile(zipfile)
				folder = AppPath + '/temp'
				if folder:
					# Get options
					for directory in Directory.GetDirectories(folder, "*", SearchOption.AllDirectories):
						if directory and Directory.Exists(directory):
							optionDirectory = Directory.GetDirectories(directory, '#Options')
							if optionDirectory and len(optionDirectory) > 0:
								optionDirectories = Directory.GetDirectories(optionDirectory[0])
								if optionDirectories and len(optionDirectories) > 0:
									description = ""
									if File.Exists(directory + '\\OptionSettings.txt'):
										optionSettings = File.ReadAllLines(directory + '\\OptionSettings.txt')
										name = readValueFromKey(optionSettings, "name")
										description = readValueFromKey(optionSettings, "description")
									installOptions = [InstallOption(directory, name, description)]
									for option in optionDirectories:
										description = ""
										if File.Exists(option + '\\OptionSettings.txt'):
											optionSettings = File.ReadAllLines(option + '\\OptionSettings.txt')
											name = readValueFromKey(optionSettings, "name")
											description = readValueFromKey(optionSettings, "description")
										else:
											name = DirectoryInfo(option).Name
											description = ""
										installOptions.append(InstallOption(option, name, description))
									form = InstallOptionForm(installOptions, DirectoryInfo(directory).Name)
									result = form.ShowDialog(MainForm.Instance)
									if result != DialogResult.OK:
										return
									# If we did not choose the standard option, remove files from main folder, copy chosen file contents back into it, and
									#then delete options
									if form.chosenFolder != directory:
										filesToDelete = Directory.GetFiles(directory)
										i = 0
										while i < len(filesToDelete):
											File.Delete(filesToDelete[i])
											i += 1
										for file in Directory.GetFiles(form.chosenFolder):
											copyFile(file, directory)
									Directory.Delete(directory + '\\#Options', True)

					# Get all subdirectories in the folder
					fighterDir = Directory.CreateDirectory(folder).GetDirectories()
					# Set up directories
					cspFolder = getDirectoryByName("CSPs", fighterDir)
					cssIconFolder = getDirectoryByName("CSSIcon", fighterDir)
					portraitNameFolder = getDirectoryByName("PortraitName", fighterDir)
					bpFolder = getDirectoryByName("BPs", fighterDir)
					replayIconFolder = getDirectoryByName("ReplayIcon", fighterDir)
					fighterFolder = getDirectoryByName("Fighter", fighterDir)
					exConfigsFolder = getDirectoryByName("EXConfigs", fighterDir)
					moduleFolder = getDirectoryByName("Module", fighterDir)
					soundbankFolder = getDirectoryByName("Soundbank", fighterDir)
					franchiseIconFolder = getDirectoryByName("FranchiseIcons", fighterDir)
					kirbyHatFolder = getDirectoryByName("KirbyHats", fighterDir)
					stockIconFolder = getDirectoryByName("StockIcons", fighterDir)
					victoryThemeFolder = getDirectoryByName("VictoryTheme", fighterDir)
					endingFolder = getDirectoryByName("Ending", fighterDir)
					creditsFolder = getDirectoryByName("CreditsTheme", fighterDir)
					classicIntro = getDirectoryByName("ClassicIntro", fighterDir)
					trophyFolder = getDirectoryByName("Trophy", fighterDir)
					codeFolder = getDirectoryByName("Codes", fighterDir)
					# Get fighter info
					fighterConfig = Directory.GetFiles(folder + '/EXConfigs', "Fighter*.dat")[0]
					cosmeticConfig = Directory.GetFiles(folder + '/EXConfigs', "Cosmetic*.dat")[0]
					slotConfig = Directory.GetFiles(folder + '/EXConfigs', "Slot*.dat")[0]
					fighterInfo = getFighterInfo(fighterConfig, cosmeticConfig, slotConfig)
					effectId = getEffectId(fighterInfo.fighterName, AppPath + '/temp/Fighter')
					fighterSettings = getFighterSettings()
					# Get the fighter this one is cloned from
					if moduleFolder:
						clonedModuleName = getClonedModuleName(Directory.GetFiles(moduleFolder.FullName, "*.rel")[0])
					else:
						clonedModuleName = ""

					uninstallVictoryTheme = 0
					installVictoryTheme = False
					uninstallCreditsTheme = 0
					newSoundbankId = ""
					victoryThemeId = 0
					creditsThemeId = 0
					overwriteFighterName = ""
					changeEffectId = False
					oldEffectId = ""
					continueInstall = False
					changeSoundbankId = False

					#region USER INPUT/PRELIMINARY CHECKS

					# Prompt user to input fighter ID
					if not fighterId:
						fighterId = showIdPrompt("Enter your desired fighter ID")
						fighterId = fighterId.split('0x')[1].upper()

					# Check if fighter ID is already used		
					existingFighterConfigs = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig', 'Fighter' + str(fighterId) + '.dat')
					if existingFighterConfigs:
						existingFighterConfig = existingFighterConfigs[0]
					else:
						existingFighterConfig = False


					# Default config IDs if not passed
					if not slotConfigId:
						slotConfigId = fighterId
					if not cosmeticConfigId:
						cosmeticConfigId = fighterId
					if not cssSlotConfigId:
						cssSlotConfigId = fighterId

					# Erase franchise icon ID if we can't find folders or files
					if franchiseIconFolder:
						blackFranchiseIconFolder = Directory.GetDirectories(franchiseIconFolder.FullName, "Black")
						if blackFranchiseIconFolder:
							if len(Directory.GetFiles(blackFranchiseIconFolder[0], "*.png")) < 1:
								franchiseIconId = -1
						else:
							franchiseIconId = -1
						transparentFranchiseIconFolder = Directory.GetDirectories(franchiseIconFolder.FullName, "Black")
						if transparentFranchiseIconFolder:
							if len(Directory.GetFiles(transparentFranchiseIconFolder[0], "*.png")) < 1:
								franchiseIconId = -1
						else:
							franchiseIconId = -1
					if not franchiseIconFolder:
						franchiseIconId = -1
					
					# Check if fighter name is already used
					oldFighterName = ""
					existingFighterName = Directory.GetDirectories(MainForm.BuildPath + '/pf/fighter', fighterInfo.fighterName)
					if existingFighterName:
						overwriteFighterName = BrawlAPI.ShowYesNoPrompt("A fighter with this internal name already exists. Do you want to overwrite it?", "Overwrite fighter name?")
						if overwriteFighterName == False:
							changeFighterName = BrawlAPI.ShowYesNoPrompt("Would you like to change the internal name?", "Change fighter name?")
							if changeFighterName == False:
								BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
								return
							while True and changeFighterName:
								oldFighterName = fighterInfo.fighterName
								fighterInfo.fighterName = BrawlAPI.UserStringInput("Enter your desired fighter name")
								existingFighterName = Directory.GetDirectories(MainForm.BuildPath + '/pf/fighter', fighterInfo.fighterName)
								if existingFighterName:
									repeatFighterName = BrawlAPI.ShowYesNoPrompt("Fighter name already in use! Try a different name?", "Try again?")
									if repeatFighterName:
										continue
									else:
										BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
										return
								else:
									break
					
					# Victory theme checks
					if victoryThemeFolder and settings.installVictoryThemes == "true":
						# Ask user if they would like to install the included victory theme
						installVictoryTheme = BrawlAPI.ShowYesNoPrompt("This fighter comes with a victory theme. Would you like to install it?", "Install victory theme?")
						if installVictoryTheme == False:
							changeVictoryTheme = BrawlAPI.ShowYesNoPrompt("Would you like to change this fighter's victory theme ID?", "Change victory theme?")
							if changeVictoryTheme:
								victoryThemeId = showIdForm("Change Victory Theme", "Select", "victoryTheme", "Song ID:")
								if victoryThemeId:
									victoryThemeId = int(victoryThemeId, 16)
								else:
									return
						# Check if existing fighter has a different victory theme
						if installVictoryTheme:
							existingSlotConfig = getSlotConfig(slotConfigId)
							if existingSlotConfig:
								oldVictoryThemeName = getVictoryThemeByFighterId(slotConfigId)
								if oldVictoryThemeName:
									victoryThemeName = getFileInfo(Directory.GetFiles(folder + '/VictoryTheme', "*.brstm")[0]).Name
									if oldVictoryThemeName != victoryThemeName.split('.brstm')[0]:
										uninstallVictoryTheme = BrawlAPI.ShowYesNoPrompt("Previously installed fighter contains a victory theme with a different name. Do you want to remove it?", "Remove existing victory theme?")

					# Credits theme checks
					if creditsFolder and settings.installVictoryThemes == "true":
						# Ask user if they would like to install the included credits theme
						doInstallCreditsTheme = BrawlAPI.ShowYesNoPrompt("This fighter comes with a credits theme. Would you like to install it?", "Install credits theme?")
						if doInstallCreditsTheme == False:
							changeCreditsTheme = BrawlAPI.ShowYesNoPrompt("Would you like to change this fighter's credits theme ID?", "Change credits theme?")
							if changeCreditsTheme:
								creditsThemeId = showIdForm("Change Credits Theme", "Select", "creditsTheme", "Song ID:")
								if creditsThemeId:
									creditsThemeId = int(creditsThemeId, 16)
								else:
									return
						# Check if existing fighter has a different credits theme
						if doInstallCreditsTheme:
							oldThemeId = updateCreditsCode(slotConfigId, "", read=True)
							if oldThemeId and oldThemeId != "0x0000":
								oldCreditsThemeName = getSongNameById(int(oldThemeId, 16), 'Credits', 'Credits')
								creditsThemeName = getFileInfo(Directory.GetFiles(folder + '/CreditsTheme', "*.brstm")[0]).Name
								if oldCreditsThemeName != creditsThemeName.split('.brstm')[0]:
									uninstallCreditsTheme = BrawlAPI.ShowYesNoPrompt("Previously installed fighter contains a credits theme with a different name. Do you want to remove it?", "Remove existing credits theme?")

					if codeFolder:
						asmFiles = codeFolder.GetFiles("*.asm")
						if len(asmFiles) > 0:
							messageText = "This fighter comes with the following .asm files:\n"
							for asmFile in asmFiles:
								messageText += "\n" + asmFile.Name
							messageText += "\n\nWould you like to install these into your build?"
							installAsm = BrawlAPI.ShowYesNoPrompt(messageText, "Install .asm files?")
							if installAsm:
								matchFiles = []
								continueInstall = True
								for asmFile in asmFiles:
									codeMatches = checkGct(asmFile.FullName)
									if len(codeMatches) > 0:
										matchFiles.append(codeMatches)
								if len(matchFiles) > 0:
									messageText = "The following codes to install were found already installed in your build:\n"
									for matchFile in matchFiles:
										messageText += ""
										for matchCode in matchFile:
											messageText += "\n" + matchCode
									messageText += "\n\nWould you like to install codes anyway?"
									continueInstall = BrawlAPI.ShowYesNoPrompt(messageText, "Codes Found")
						
					# Check if soundbank is already in use
					if soundbankFolder:
						soundbankId = addLeadingZeros(str(hex(int(fighterInfo.soundbankId))).split('0x')[1].upper(), 3)
						# Get soundbank name to check
						modifier = 0 if settings.addSevenToSoundbankName == "false" else 7
						if settings.soundbankStyle == "hex":
							soundbankNameToCheck = addLeadingZeros(str(hex(int(soundbankId, 16) + modifier)).split('0x')[1].upper(), 3)
						else:
							soundbankNameToCheck = addLeadingZeros(str(int(soundbankId, 16) + modifier), 3)
						soundbankMatch = Directory.GetFiles(MainForm.BuildPath + '/pf/sfx', soundbankNameToCheck + '.sawnd')
						if soundbankMatch and settings.sfxChangeExe != "" and settings.sawndReplaceExe != "":
							if not auto:
								changeSoundbankId = BrawlAPI.ShowYesNoPrompt("A soundbank with the same ID already exists. Would you like to change the soundbank ID?", "Soundbank Already Exists")
							else:
								changeSoundbankId = True
							if changeSoundbankId:
								if not auto:
									autoSoundbankId = BrawlAPI.ShowYesNoPrompt("Do you want BrawlInstaller to choose the ID automatically?", "Resolve Automatically?")
								else:
									autoSoundbankId = True
								matchFound = True
								# Keep prompting for alternate soundbank ID until one that is not used is entered
								idMod = 0
								while matchFound:
									if not autoSoundbankId:
										soundbanks = Directory.GetFiles(MainForm.BuildPath + '/pf/sfx', '*.sawnd')
										soundbankIds = []
										for soundbank in soundbanks:
											soundbankName = getFileInfo(soundbank).Name
											if "_" not in soundbankName:
												soundbankIds.append('0x' + soundbankName.replace('.sawnd', ''))
										newSoundbankId = showIdForm("Change Soundbank", "Select", "custom", "Soundbank ID:", soundbankIds)
										if not newSoundbankId:
											return
									else:
										# Minimum soundbank ID is 331
										newSoundbankId = addLeadingZeros(str(331 + idMod), 3)
									if settings.soundbankStyle == "hex":
										soundbankNameToCheck = addLeadingZeros(str(hex(int(newSoundbankId, 16) + modifier)).split('0x')[1].upper(), 3)
									else:
										soundbankNameToCheck = addLeadingZeros(str(int(newSoundbankId, 16) + modifier), 3)
									soundbankMatch = Directory.GetFiles(MainForm.BuildPath + '/pf/sfx', newSoundbankId + '.sawnd')
									if soundbankMatch:
										if not auto and not autoSoundbankId:
											tryAgain = BrawlAPI.ShowYesNoPrompt("Soundbank ID entered already exists. Try entering a different ID?", "Soundbank Already Exists")
										else:
											tryAgain = True
											idMod += 1
										if tryAgain == False:
											BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
											return
										continue
									matchFound = False
								newSoundbankId = hexId(newSoundbankId)
							else:
								newSoundbankId = ""
						elif soundbankMatch:
							overwriteSoundbank = BrawlAPI.ShowYesNoPrompt("A soundbank with the same ID already exists. You do not have soundbank ID changing set up. Would you like to overwrite the current soundbank?", "Soundbank Already Exists")
							if overwriteSoundbank == False:
								BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
								return
					# Check if Effect.pac ID is already in use
					if settings.gfxChangeExe != "":
						oldEffectId = effectId
						if effectId:
							idMod = 0
							#matchFound = False
							directories = Directory.GetDirectories(MainForm.BuildPath + '/pf/fighter')
							progressCounter = 0
							progressBar = ProgressWindow(MainForm.Instance, "Conflict Check...", "Checking for Effect.pac ID conflicts", False)
							progressBar.Begin(0, len(directories), progressCounter)
							effectIds = []
							for directory in directories:
								progressCounter += 1
								progressBar.Update(progressCounter)
								addedEffectId = getEffectId(DirectoryInfo(directory).Name)
								if addedEffectId.strip() != "":
									effectIds.append(addedEffectId.strip())
							progressBar.Finish()
							autoEffectId = False
							while effectId in effectIds:
								if not auto and not autoEffectId:
									changeEffectId = BrawlAPI.ShowYesNoPrompt("A fighter with the same Effect.pac ID already exists. Would you like to change the Effect.pac ID?", "Effect.pac ID Already Exists")
									if changeEffectId:
										autoEffectId = BrawlAPI.ShowYesNoPrompt("Do you want BrawlInstaller to choose the ID automatically?", "Resolve Automatically?")
								else:
									changeEffectId = True
								if changeEffectId:
									if not auto and not autoEffectId:
										customIdList = []
										for idEntry in effectIds:
											idName = '0x' + idEntry
											if idName.strip() != '0x':
												customIdList.append(idName)
										newEffectId = showIdForm("Change Effect.pac ID", "Select", "custom", "Effect.pac ID:", customIdList)
										if not newEffectId:
											return
										else:
											effectId = newEffectId.strip().replace('0x','')
									else: 
										effectId = addLeadingZeros(hexId(idMod).replace('0x',''), 2)
										idMod += 1
								else:
									break
					# Franchise icon install prompt
					if franchiseIconFolder:
						doInstallFranchiseIcon = BrawlAPI.ShowYesNoPrompt("This character comes with a franchise icon. Would you like to install it?", "Install Franchise Icon")
						if doInstallFranchiseIcon:
							franchiseIconUsed = True
							if franchiseIconId == -1:
								while franchiseIconUsed:
									franchiseIconId = showIdForm("Install Franchise Icon", "Install", "franchiseImage", "Franchise Icon ID:")
									if franchiseIconId:
										franchiseIconId = int(franchiseIconId, 16)
									else:
										return
									franchiseIconUsed = franchiseIconIdUsed(franchiseIconId)
									if franchiseIconUsed:
										changeFranchiseIconId = BrawlAPI.ShowYesNoPrompt("A franchise icon with this ID already exists. Would you like to enter a different ID?", "Franchise Icon Already Exists")
										if changeFranchiseIconId == False:
											BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
											BrawlAPI.ForceCloseFile()
											return
										continue
									else:
										BrawlAPI.ForceCloseFile()
										break
						else:
							newFranchiseIconId = BrawlAPI.ShowYesNoPrompt("Would you like to change the franchise icon ID for this fighter?", "Change franchise icon ID?")
							if newFranchiseIconId:
								franchiseIconId = showIdForm("Install Franchise Icon", "Install", "franchiseImage", "Franchise Icon ID:")
								if franchiseIconId:
									franchiseIconId = int(franchiseIconId, 16)
								else:
									return
							if not newFranchiseIconId:
								franchiseIconId = -1
					#endregion USER INPUT/PRELIMINARY CHECKS

					# Set up progressbar
					progressCounter = 0
					progressBar = ProgressWindow(MainForm.Instance, "Installing Character...", "Installing Character", False)
					progressBar.Begin(0, 19, progressCounter)

					#region SCSELCHARACTER

					# Install CSPs
					if cspFolder:
						installCSPs(cosmeticId, cspFolder, settings.rspLoading)
					# Install CSS icon
					if cssIconFolder:
						# Get user's preferred icon style
						iconFolders = Directory.GetDirectories(cssIconFolder.FullName, settings.cssIconStyle)
						if iconFolders:
							if len(Directory.GetFiles(iconFolders[0], "*.png")) > 0:
								# Use CMPR for Brawl/PM style icons
								if settings.cssIconStyle == "vBrawl" or settings.cssIconStyle == "PM":
									format = WiiPixelFormat.CMPR
								else:
									format = WiiPixelFormat.CI8
								installCSSIcon(cosmeticId, Directory.GetFiles(iconFolders[0], "*.png")[0], format)
								nameFolders = Directory.GetDirectories(iconFolders[0], "Name")
								# If a name folder is found in the CSS icon directory, install CSS icon name
								if nameFolders and settings.installCSSIconNames == "true":
									if len(Directory.GetFiles(nameFolders[0], "*.png")) > 0:
										installCSSIconName(cosmeticId, Directory.GetFiles(nameFolders[0], "*.png")[0])
						else:
							BrawlAPI.ShowMessage("Could not find CSS icon in a format that matches your preferences. CSS icon installation will be skipped. Please install a CSS icon manually.", "CSS Icon Not Found")
					# Install CSS portrait name
					if portraitNameFolder and settings.installPortraitNames == "true":
						nameFolders = Directory.GetDirectories(portraitNameFolder.FullName, settings.portraitNameStyle)
						if nameFolders:
							if len(Directory.GetFiles(nameFolders[0], "*.png")) > 0:
								installPortraitName(cosmeticId, Directory.GetFiles(nameFolders[0], "*.png")[0])
						else:
							BrawlAPI.ShowMessage("Could not find portrait name in a format that matches your preferences. Portrait name installation will be skipped. Please install a portrait name manually.", "Portrait Name Not Found")
					# Install franchise icon to sc_selcharacter
					if franchiseIconFolder and doInstallFranchiseIcon:
						franchiseIconFolderCss = Directory.GetDirectories(franchiseIconFolder.FullName, "Black")
						if franchiseIconFolderCss:
							if len(Directory.GetFiles(franchiseIconFolderCss[0], "*.png")) > 0:
								installFranchiseIcon(franchiseIconId, Directory.GetFiles(franchiseIconFolderCss[0], "*.png")[0], '/pf/menu2/sc_selcharacter.pac', int(settings.franchiseIconSizeCSS))
					# If we did any work in sc_selcharacter, save and close it
					fileOpened = checkOpenFile("sc_selcharacter")
					if fileOpened:
						BrawlAPI.SaveFile()
						BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)

					#endregion SCSELCHARACTER

					#region info.pac

					# Install stock icons to info.pac
					if stockIconFolder and settings.installStocksToInfo == "true":
						installStockIcons(cosmeticId, stockIconFolder, "Misc Data [30]", "Misc Data [30]", rootName="", filePath='/pf/info2/info.pac', fiftyCC=settings.fiftyCostumeCode)
					# Install franchise icon to info.pac
					if franchiseIconFolder and doInstallFranchiseIcon:
						franchisIconFolderInfo = Directory.GetDirectories(franchiseIconFolder.FullName, "Black")
						if franchisIconFolderInfo:
							if len(Directory.GetFiles(franchisIconFolderInfo[0], "*.png")) > 0:
								installFranchiseIcon(franchiseIconId, Directory.GetFiles(franchisIconFolderInfo[0], "*.png")[0], '/pf/info2/info.pac')
					# Install BP names to info.pac
					if bpFolder and settings.installBPNames == "true":
						# Get preferred BP style
						bpFolders = Directory.GetDirectories(bpFolder.FullName, settings.bpStyle)
						if bpFolders:
							nameFolders = Directory.GetDirectories(bpFolders[0], "Name")
							if nameFolders:
								if len(Directory.GetFiles(nameFolders[0], "*.png")) > 0:
									installBPName(cosmeticId, Directory.GetFiles(nameFolders[0], "*.png")[0], '/pf/info2/info.pac', settings.fiftyCostumeCode)
					fileOpened = checkOpenFile("info")
					if fileOpened:
						BrawlAPI.SaveFile()
						BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)
					
					#endregion info.pac

					#region sc_selcharacter stocks

					# Have to install stocks after info.pac work is done, because info.pac contains extra textures and can't use the replace method like other stock locations can
					# Install stock icons to sc_selcharacter
					if stockIconFolder and settings.installStocksToCSS == "true":
						installStockIcons(cosmeticId, stockIconFolder, "Misc Data [90]", "", rootName="", filePath='/pf/menu2/sc_selcharacter.pac', fiftyCC=settings.fiftyCostumeCode)
						fileOpened = checkOpenFile("sc_selcharacter")
						if fileOpened:
							BrawlAPI.SaveFile()
							BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)

					#endregion sc_selcharacter stocks

					#region Single Player Cosmetics

					# Go through each info .pac file (aside from the standard info.pac) and install stuff
					if settings.installSingleplayerCosmetics == "true":
						for file in Directory.GetFiles(MainForm.BuildPath + '/pf/info2/', "*.pac"):
							fileName = getFileInfo(file).Name
							if fileName != "info.pac":
								# Franchise icons first
								if franchiseIconFolder and doInstallFranchiseIcon:
									franchisIconFolderInfo = Directory.GetDirectories(franchiseIconFolder.FullName, "Black")
									if franchisIconFolderInfo:
										if len(Directory.GetFiles(franchisIconFolderInfo[0], "*.png")) > 0:
											installFranchiseIcon(franchiseIconId, Directory.GetFiles(franchisIconFolderInfo[0], "*.png")[0], '/pf/info2/' + fileName)
								# BP names next
								if bpFolder and settings.installBPNames == "true":
									# Get preferred BP style
									bpFolders = Directory.GetDirectories(bpFolder.FullName, settings.bpStyle)
									if bpFolders:
										nameFolders = Directory.GetDirectories(bpFolders[0], "Name")
										if nameFolders:
											if len(Directory.GetFiles(nameFolders[0], "*.png")) > 0:
												installBPName(cosmeticId, Directory.GetFiles(nameFolders[0], "*.png")[0], '/pf/info2/' + fileName, settings.fiftyCostumeCode)
								fileOpened = checkOpenFile(fileName.split('.pac')[0])
								if fileOpened:
									BrawlAPI.SaveFile()
									BrawlAPI.ForceCloseFile()

					# Import the classic intro file if present
					if classicIntro:
						if len(Directory.GetFiles(classicIntro.FullName, "*.brres")) > 0:
							importClassicIntro(cosmeticId, Directory.GetFiles(classicIntro.FullName, "*.brres")[0])

					progressCounter += 1
					progressBar.Update(progressCounter)

					#endregion Single Player Cosmetics

					#region STGRESULT

					# Install stock icons to STGRESULT
					if stockIconFolder and settings.installStockIconsToResult == "true":
						installStockIcons(cosmeticId, stockIconFolder, "Misc Data [120]", "Misc Data [110]", rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC=settings.fiftyCostumeCode)
					# Install franchise icon to STGRESULT
					if franchiseIconFolder and doInstallFranchiseIcon:
						modelFranchise = ""
						textureFranchise = ""
						franchiseIconModel = Directory.GetDirectories(franchiseIconFolder.FullName, "Model")
						if franchiseIconModel:
							if len(Directory.GetFiles(franchiseIconModel[0], "*.mdl0")) > 0:
								modelFranchise = Directory.GetFiles(franchiseIconModel[0], "*.mdl0")[0]
						franchisIconFolderResult = Directory.GetDirectories(franchiseIconFolder.FullName, "Transparent")	
						if franchisIconFolderResult:
							if len(Directory.GetFiles(franchisIconFolderResult[0], "*.png")) > 0:
								textureFranchise = Directory.GetFiles(franchisIconFolderResult[0], "*.png")[0]
						if modelFranchise or textureFranchise:
							installFranchiseIconResult(franchiseIconId, textureFranchise, modelFranchise)
					fileOpened = checkOpenFile("STGRESULT")
					if fileOpened:
						BrawlAPI.SaveFile()
						BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion STGRESULT

					#region Other Stock Icon Locations

					if stockIconFolder:
						# StockFaceTex.brres - used for things like rotation mode
						if settings.installStocksToStockFaceTex == "true":
							installStockIcons(cosmeticId, stockIconFolder, "", "", filePath='/pf/menu/common/StockFaceTex.brres', fiftyCC=settings.fiftyCostumeCode)
							BrawlAPI.SaveFile()
							BrawlAPI.ForceCloseFile()
						# sc_selmap - used for SSS in vBrawl
						if settings.installStocksToSSS == "true":
							installStockIcons(cosmeticId, stockIconFolder, "Misc Data [40]", "Misc Data [20]", filePath='/pf/menu2/sc_selmap.pac', fiftyCC=settings.fiftyCostumeCode)
							BrawlAPI.SaveFile()
							BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Other Stock Icon Locations

					#region BPs

					if bpFolder:
						# Get user's preferred BP style
						bpFolders = Directory.GetDirectories(bpFolder.FullName, settings.bpStyle)
						if bpFolders:
							if len(Directory.GetFiles(bpFolders[0], "*.png")) > 0:
								installBPs(cosmeticId, Directory.GetFiles(bpFolders[0], "*.png"), fiftyCC=settings.fiftyCostumeCode)
						else:
							bpFolders = Directory.GetDirectories(bpFolder.FullName, "vBrawl")
							if bpFolders:
								if len(Directory.GetFiles(bpFolders[0], "*.png")) > 0:
									installBPs(cosmeticId, Directory.GetFiles(bpFolders[0], "*.png"), fiftyCC=settings.fiftyCostumeCode)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion BPs

					#region Replay Icon

					if replayIconFolder:
						# Legacy
						if len(Directory.GetFiles(replayIconFolder.FullName, "*.png")) > 0:
							installReplayIcon(cosmeticId, Directory.GetFiles(replayIconFolder.FullName, "*.png")[0])
						# Modern way
						elif settings.replayIconStyle:
							replayFolders = Directory.GetDirectories(replayIconFolder.FullName, settings.replayIconStyle)
							if replayFolders:
								if len(Directory.GetFiles(replayFolders[0], "*.png")) > 0:
									installReplayIcon(cosmeticId, Directory.GetFiles(replayFolders[0], "*.png")[0])
						elif not settings.replayIconStyle:
							replayFolders = Directory.GetDirectories(replayIconFolder.FullName)
							if replayFolders:
								if len(Directory.GetFiles(replayFolders[0], "*.png")) > 0:
									installReplayIcon(cosmeticId, Directory.GetFiles(replayFolders[0], "*.png")[0])
					progressCounter += 1
					progressBar.Update(progressCounter)

					#endregion Replay Icon

					#region Victory Theme

					# If user indicated they want victory theme removed, remove it first
					if uninstallVictoryTheme:
						removeSongId = getVictoryThemeIDByFighterId(slotConfigId)
						removeSong(removeSongId)
					# Add victory theme
					if victoryThemeFolder and settings.installVictoryThemes == "true" and installVictoryTheme:
						if len(Directory.GetFiles(victoryThemeFolder.FullName, "*.brstm")) > 0:
							victoryThemeId = addSong(Directory.GetFiles(victoryThemeFolder.FullName, "*.brstm")[0])

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Victory Theme

					#region Soundbank

					# Update soundbank ID if user set to do that
					if newSoundbankId:
						updateSoundbankId(getFileInfo(Directory.GetFiles(fighterFolder.FullName, "Fit" + fighterInfo.fighterName + ".pac")[0]), getFileInfo(settings.sawndReplaceExe), getFileInfo(settings.sfxChangeExe), str("%x" % fighterInfo.soundbankId).upper(), newSoundbankId, settings.addSevenToSoundbankIds)

					# Move soundbank
					if soundbankFolder:
						# Rename file based on user preferences
						if newSoundbankId == "":
							newSoundbankId = "%x" % fighterInfo.soundbankId
						modifier = 0 if settings.addSevenToSoundbankName == "false" else 7
						if settings.soundbankStyle == "hex":
							newSoundbankId = addLeadingZeros(str(hex(int(newSoundbankId, 16) + modifier)).split('0x')[1].upper(), 3)
						else:
							newSoundbankId = addLeadingZeros(str(int(newSoundbankId, 16) + modifier), 3)
						if len(Directory.GetFiles(soundbankFolder.FullName, "*.sawnd")) > 0:
							moveSoundbank(getFileInfo(Directory.GetFiles(soundbankFolder.FullName, "*.sawnd")[0]), newSoundbankId)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Soundbank

					#region Effect ID

					# Update effect ID if user opted to earlier
					if changeEffectId and oldEffectId:
						updateEffectId(getFileInfo(Directory.GetFiles(fighterFolder.FullName, "Fit" + fighterInfo.fighterName + ".pac")[0]), getFileInfo(settings.gfxChangeExe), oldEffectId, effectId)
					#endregion Effect ID

					#region Kirby Hats

					kirbyHatFighterId = -1
					if settings.kirbyHatExe != "" and settings.installKirbyHats == "true":
						if kirbyHatFolder:
							# Attempt to get the kirby hat fighter ID from text file
							fighterIdFile = getFileByName("FighterID.txt", kirbyHatFolder)
							if fighterIdFile:
								fighterIdString = File.ReadAllText(fighterIdFile.FullName)
								# Ensure fighter ID is the integer format
								if fighterIdString.startswith('0x'):
									kirbyHatFighterId = int(fighterIdString, 16)
								elif fighterIdString.isnumeric():
									kirbyHatFighterId = int(fighterIdString)
						# If we don't have a kirby hat fighter ID but settings say we should, generate kirby hat based on settings
						# If we don't have kirby hat files but do have an ID, generate kirby hat based on that
						if (kirbyHatFighterId == -1 or not Directory.GetFiles(AppPath + '/temp/KirbyHats', "*.pac")) and settings.defaultKirbyHat != "none" and settings.installKirbyHats == "true":
							# Delete Kirby hat folder if it already exists
							if kirbyHatFolder:
								Directory.Delete(kirbyHatFolder.FullName, 1)
							# Create the kirby hat folder
							kirbyHatFolder = Directory.CreateDirectory(AppPath + '/temp/KirbyHats')
							# Get name of fighter based on default kirby hat ID
							if kirbyHatFighterId == -1:
								kirbyHatFighterId = int(settings.defaultKirbyHat, 16)
							kirbyHatFighterName = FIGHTER_IDS[kirbyHatFighterId]
							# Get Kirby hat files from the build and copy them to the temp directory
							kirbyHatFiles = Directory.GetFiles(MainForm.BuildPath + '/pf/fighter/kirby', "FitKirby" + kirbyHatFighterName + "*.pac")
							# Rename them appropriately
							for kirbyHatFile in kirbyHatFiles:
								# Back up Kirby hat files if they already exist
								createBackup(getFileInfo(kirbyHatFile).FullName.replace(kirbyHatFighterName, fighterInfo.fighterName))
								File.Copy(kirbyHatFile, AppPath + '/temp/KirbyHats/' + getFileInfo(kirbyHatFile).Name.replace(kirbyHatFighterName, fighterInfo.fighterName), 1)
						# Install Kirby hat
						if settings.defaultKirbyHat != "none" and settings.installKirbyHats == "true":
							if existingFighterName and overwriteFighterName:
								# If we are overwriting an existing fighter name, clean up the old Kirby hats
								deleteKirbyHatFiles(DirectoryInfo(existingFighterName[0]).Name)
							installKirbyHat(fighterInfo.characterName, fighterInfo.fighterName, fighterId, str("%x" % kirbyHatFighterId).upper(), settings.kirbyHatExe, Directory.GetFiles(kirbyHatFolder.FullName, "FitKirby*.pac"), oldFighterName, fighterInfo.fighterName)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Kirby Hats

					#region Fighter Files

					# Install fighter files
					existingFighterConfigName = ""
					if fighterFolder:
						if overwriteFighterName and existingFighterName:
							deleteFighterFiles(DirectoryInfo(existingFighterName[0]).Name.lower())
						# If a fighter already exists at this ID, delete them
						if existingFighterConfig:
							BrawlAPI.OpenFile(existingFighterConfig)
							existingFighterConfigName = BrawlAPI.RootNode.FighterName
							BrawlAPI.ForceCloseFile()
						installFighterFiles(Directory.GetFiles(fighterFolder.FullName, "*.pac"), fighterInfo.fighterName, existingFighterConfigName, oldFighterName)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Fighter Files

					#region Module

					# Update and install module file
					if moduleFolder:
						if len(Directory.GetFiles(moduleFolder.FullName, "*.rel")) > 0:
							installModuleFile(Directory.GetFiles(moduleFolder.FullName, "*.rel")[0], moduleFolder, fighterId, fighterInfo.fighterName, existingFighterConfigName)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Module

					#region EX Configs

					# Update and move EX configs
					if exConfigsFolder:
						useKirbyHat = False if settings.defaultKirbyHat == "none" or kirbyHatFighterId == -1 or settings.installKirbyHats != "true" else True
						modifyExConfigs(Directory.GetFiles(exConfigsFolder.FullName, "*.dat"), cosmeticId, fighterId, fighterInfo.fighterName, franchiseIconId, useKirbyHat, newSoundbankId, victoryThemeId, kirbyHatFighterId, cosmeticConfigId, cssSlotConfigId, slotConfigId)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion EX Configs

					#region Misc Changes

					# Install ending files if they exist
					if endingFolder:
						installEndingFiles(endingFolder, fighterInfo.fighterName, cosmeticConfigId)

					# If user indicated they want credits theme removed, remove it first
					if uninstallCreditsTheme:
						uninstallCreditsSong(slotConfigId)

					# Update credits code if ID is provided
					if fighterSettings.creditsThemeId:
						updateCreditsCode(slotConfigId, fighterSettings.creditsThemeId)

					# Install credits song if one exists
					if creditsFolder and settings.installVictoryThemes == "true" and doInstallCreditsTheme:
						if Directory.GetFiles(creditsFolder.FullName, "*.brstm"):
							installCreditsTheme(Directory.GetFiles(creditsFolder.FullName, "*.brstm")[0], slotConfigId)

					# Assign trophy if applicable
					if fighterSettings.trophyId:
						assignTrophy(slotConfigId, fighterSettings.trophyId, fighterInfo.fighterName, settings.installToSse)

					# Install trophy if one exists
					if trophyFolder and settings.installTrophies == "true":
						trophySettings = getTrophySettings()
						brresFiles = Directory.GetFiles(trophyFolder.FullName, "*.brres")
						imageFiles = Directory.GetFiles(trophyFolder.FullName, "*.png")
						if imageFiles and brresFiles:
							installTrophy(slotConfigId, brresFiles[0], imageFiles[0], fighterInfo.fighterName, trophySettings, settings.installToSse)

					progressCounter += 1
					progressBar.Update(progressCounter)

					#endregion Misc Changes

					#region SSE

					# Add character to SSE roster
					if settings.installToSse == "true":
						updateSseModule(cssSlotConfigId, settings.sseUnlockStage, baseCssSlotId=baseCssSlotId)
						if cssIconFolder:
							iconFolders = Directory.GetDirectories(cssIconFolder.FullName, "vBrawl")
							if iconFolders:
								cssIconNameSse = ""
								nameFolders = Directory.GetDirectories(iconFolders[0], "Name")
								imageFiles = Directory.GetFiles(iconFolders[0], "*.png")
								if nameFolders:
									nameFiles = Directory.GetFiles(nameFolders[0], "*.png")
									if nameFiles:
										cssIconNameSse = nameFiles[0]
								imagePath = ""
								if len(imageFiles) > 0:
									imagePath = imageFiles[0]
								if imagePath:
									installCssIconSSE(cosmeticId, imagePath, cssIconNameSse)
									createNewcomerFile(cosmeticConfigId, imagePath)
						if stockIconFolder:
							installStockIcons(cosmeticId, stockIconFolder, "Misc Data [8]", "", filePath='/pf/menu2/if_adv_mngr.pac', fiftyCC="false", firstOnly=True)
						if franchiseIconFolder and doInstallFranchiseIcon:
							franchisIconFolderSse = Directory.GetDirectories(franchiseIconFolder.FullName, "Black")
							if franchisIconFolderSse:
								if len(Directory.GetFiles(franchisIconFolderSse[0], "*.png")) > 0:
									installFranchiseIcon(franchiseIconId, Directory.GetFiles(franchisIconFolderSse[0], "*.png")[0], '/pf/menu2/if_adv_mngr.pac')
						fileOpened = checkOpenFile("if_adv_mngr")
						if fileOpened:
							BrawlAPI.SaveFile()
							BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)

					#endregion SSE

					#region Code Menu

					# Add fighter to code menu
					if settings.assemblyFunctionsExe != "":
						addToCodeMenu(fighterInfo.characterName, fighterId, settings.assemblyFunctionsExe)

					# Add entry to L-load code
					if baseCssSlotId:
						addAltCharacter(cssSlotConfigId, baseCssSlotId)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Code Menu

					#region Code Edits

					# Install any codes included with the fighter
					if continueInstall:
						installAsms(asmFiles)

					# Make code changes to add a throw release point
					if fighterSettings.throwReleasePoint:
						updateThrowRelease(fighterId, fighterInfo.characterName, fighterSettings.throwReleasePoint)

					# Make code changes for Lucario clones
					if clonedModuleName == "ft_lucario":
						# Lucario Clone Aura Sphere GFX Fix [Dantarion, ds22, DesiacX]
						if effectId:
							addCodeMacro(fighterInfo.characterName, fighterId, "GFXFix", [ "0x" + str(fighterId), hexId(str(hex(int(effectId, 16) + 311))) ], 0)
						# Kirby Lucario Clone Aura Sphere GFX Fix [ds22, DesiacX, Eon]
						if fighterSettings.lucarioKirbyEffectId:
							addCodeMacro(fighterInfo.characterName, fighterId, "GFXFix", [ "0x" + str(fighterId), fighterSettings.lucarioKirbyEffectId ], 0, preFindText="bne notKirby")
						# Lucario Clone Aura Sphere Bone ID Fix [Dantarion, ds22, PyotrLuzhin, Yohan1044, KingJigglypuff, Desi]
						if fighterSettings.lucarioBoneId:
							addCodeMacro(fighterInfo.characterName, fighterId, "BoneIDFixA", [ "copy", "0x" + str(fighterId), fighterSettings.lucarioBoneId ], 1, True)

					# Make code changes for Jigglypuff clones
					if clonedModuleName == "ft_purin":
						# Jigglypuff Clone Rollout Bone Fix [codes, DesiacX]
						if fighterSettings.jigglypuffBoneId:
							addCodeMacro(fighterInfo.characterName, fighterId, "CloneBones", [ "0x" + str(fighterId), fighterSettings.jigglypuffBoneId, "copy" ], 0, True)
						# Jigglypuff Clone Rollout Max Charge GFX Fix [Codes, DesiacX]
						if fighterSettings.jigglypuffEFLSId and effectId:
							addCodeMacro(fighterInfo.characterName, fighterId, "CloneGFX", [ "0x" + str(fighterId), hexId(str(hex(int(effectId, 16) + 311))), fighterSettings.jigglypuffEFLSId, "copy" ], 0, True)
						# Jigglypuff Clone Rollout SFX Fix [codes, DesiacX]
						if len(fighterSettings.jigglypuffSfxIds) > 0:
							if changeSoundbankId:
								i = 0
								while i < len(fighterSettings.jigglypuffSfxIds):
									fighterSettings.jigglypuffSfxIds[i] = getNewSfxId(fighterSettings.jigglypuffSfxIds[i], settings.sfxChangeExe)
									i += 1
							addCodeMacro(fighterInfo.characterName, fighterId, "CloneSFX", [ "0x" + str(fighterId), fighterSettings.jigglypuffSfxIds[0], "copy" ], 0, False, "HOOK @ $80ACAE3C")
							addCodeMacro(fighterInfo.characterName, fighterId, "CloneSFX", [ "0x" + str(fighterId), fighterSettings.jigglypuffSfxIds[1], "copy" ], 0, False, "HOOK @ $80ACAE60")
							addCodeMacro(fighterInfo.characterName, fighterId, "CloneSFX", [ "0x" + str(fighterId), fighterSettings.jigglypuffSfxIds[2], "copy" ], 0, False, "HOOK @ $80ACF704")
							addCodeMacro(fighterInfo.characterName, fighterId, "CloneSFX", [ "0x" + str(fighterId), fighterSettings.jigglypuffSfxIds[3], "copy" ], 0, False, "HOOK @ $80ACA09C")
					
					# Make code changes for Dedede clones
					if clonedModuleName == "ft_dedede":
						# Dedede Clones Fix [MarioDox]
						addCodeMacro(fighterInfo.characterName, fighterId, "DededeFix", [ "0x" + str(fighterId) ], 0, True)

					# Make code changes for Bowser clones
					if clonedModuleName == "ft_koopa":
						# Bowser Clone Fire Breath Bone Fix [KingJigglypuff]
						if fighterSettings.bowserBoneId:
							addCodeMacro(fighterInfo.characterName, fighterId, "BoneIDFix", [ "0x" + str(fighterId), fighterSettings.bowserBoneId ], 0, False, preFindText=".macro BoneIDFix(<FighterID>, <BoneID>)")

					buildGct()

					progressCounter += 1
					progressBar.Update(progressCounter)

					#endregion Code Edits

					#region CSSRoster

					# Add fighter to roster
					if not baseCssSlotId:
						changesMade = addToRoster(cssSlotConfigId)
						if changesMade:
							BrawlAPI.SaveFile()
						BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)
					progressBar.Finish()
					#endregion
					
				# Delete temporary directory
				Directory.Delete(AppPath + '/temp', 1)
				archiveBackup()
				BrawlAPI.ShowMessage("Character successfully installed with fighter ID 0x" + fighterId + " and cosmetic ID " + str(cosmeticId) + ".", "Success")
		except Exception as e:
			if 'progressBar' in locals():
				progressBar.Finish()
			raise e
			
#endregion INSTALL CHARACTER

#region INSTALL COSTUME

def installCostume(cosmeticId, fighterId, cssSlotConfigId, position, cspImages, bpImages, stockImages, costumeFiles, skipPositions=[], startingId=0, cosmeticsOnly=False, updateConfig=True):
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
			Directory.CreateDirectory(AppPath + '/temp')

			fighterConfig = ""
			fighterInfo = ""
			if Directory.Exists(MainForm.BuildPath + '/pf/BrawlEx'):
				fighterConfig = getFighterConfig(fighterId)
				fighterInfo = getFighterInfo(fighterConfig, "", "")

			# Set up progressbar
			itemText = "Costume" if not cosmeticsOnly else "Cosmetics"
			progressCounter = 0
			progressBar = ProgressWindow(MainForm.Instance, "Installing " + itemText + "...", "Installing " + itemText, False)
			progressBar.Begin(0, 5, progressCounter)

			# sc_selcharacter
			index = addCSPs(cosmeticId, cspImages, settings.rspLoading, position, skipPositions)
			# If we did any work in sc_selcharacter, save and close it
			fileOpened = checkOpenFile("sc_selcharacter")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# BPs
			incrementBPNames(cosmeticId, index, increment=len(bpImages), fiftyCC=settings.fiftyCostumeCode)
			createBPs(cosmeticId, bpImages, startIndex=index)

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Stock icons
			# info.pac
			if settings.installStocksToInfo == "true":
				addStockIcons(cosmeticId, stockImages, index, "Misc Data [30]", "Misc Data [30]", rootName="", filePath='/pf/info2/info.pac', fiftyCC=settings.fiftyCostumeCode)
				fileOpened = checkOpenFile("info")
				if fileOpened:
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()

			# sc_selcharacter
			if settings.installStocksToCSS == "true":
				addStockIcons(cosmeticId, stockImages, index, "Misc Data [90]", "", rootName="", filePath='/pf/menu2/sc_selcharacter.pac', fiftyCC=settings.fiftyCostumeCode)
				fileOpened = checkOpenFile("sc_selcharacter")
				if fileOpened:
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()

			# STGRESULT
			if settings.installStockIconsToResult == "true":
				addStockIcons(cosmeticId, stockImages, index, "Misc Data [120]", "Misc Data [110]", rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC=settings.fiftyCostumeCode)
				fileOpened = checkOpenFile("STGRESULT")
				if fileOpened:
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()

			# StockFaceTex
			if settings.installStocksToStockFaceTex == "true":
				addStockIcons(cosmeticId, stockImages, index, "", "", filePath='/pf/menu/common/StockFaceTex.brres', fiftyCC=settings.fiftyCostumeCode)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			# sc_selmap
			if settings.installStocksToSSS == "true":
				addStockIcons(cosmeticId, stockImages, index, "Misc Data [40]", "Misc Data [20]", filePath='/pf/menu2/sc_selmap.pac', fiftyCC=settings.fiftyCostumeCode)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
			
			progressCounter += 1
			progressBar.Update(progressCounter)


			if cosmeticsOnly != True and costumeFiles and len(costumeFiles) > 0:
				# Costume files
				if fighterInfo:
					fighterName = fighterInfo.fighterName
				else:
					if fighterId == "2D":
						fighterName = "Knuckles"
					else:
						if not FighterNameGenerators.generated:
							FighterNameGenerators.GenerateLists()
						fighterName = FighterNameGenerators.InternalNameFromID(int(fighterId, 16), 16, "X")
				costumes = importCostumeFiles(costumeFiles, fighterName, cssSlotConfigId, cspImages, startingId=startingId)

			progressCounter += 1
			progressBar.Update(progressCounter)
			
			if cosmeticsOnly != True and updateConfig:
				# Ex Config
				enableAllCostumes(fighterId)
				addCssSlots(costumes, index, cssSlotConfigId)

			if Directory.Exists(AppPath + '/temp'):
				Directory.Delete(AppPath + '/temp', 1)
				
			progressCounter += 1
			progressBar.Update(progressCounter)
			progressBar.Finish()
			BrawlAPI.ShowMessage(itemText + " installed successfully.", "Success")

		except Exception as e:
			if 'progressBar' in locals():
				progressBar.Finish()
			raise e

#endregion INSTALL COSTUME
