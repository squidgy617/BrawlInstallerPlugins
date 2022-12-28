__author__ = "Squidgy"

from BrawlInstallerLib import *

def main():
		if str(BrawlAPI.RootNode) != "None":
			BrawlAPI.CloseFile()
		# If temporary directory already exists, delete it to prevent duplicate files
		if Directory.Exists(AppPath + '/temp'):
			Directory.Delete(AppPath + '/temp', 1)
		createLogFile()
		title = "Character Packaging Tool"
		# EX Configs
		exConfigs = BrawlAPI.OpenMultiFileDialog("Select fighter EX config files", "DAT files|*.dat")
		# Fighter files
		fighterFiles = BrawlAPI.OpenMultiFileDialog("Select fighter pac files", "PAC files|*.pac")
		# Module file
		moduleFile = BrawlAPI.OpenFileDialog("Select fighter module file", "REL files|*.rel")
		BrawlAPI.ShowMessage("You will be prompted to select your fighter's CSP files. When you select multiple files, they will be color smashed.\n\nYou will receive the prompt multiple times, so you can have multiple sets of CSPs that are not all color smashed together.", title)
		# CSPs
		cspFiles = []
		while True:
			cspsToAdd = BrawlAPI.OpenMultiFileDialog("Select fighter CSP files (if multiple, images will be color smashed)", "PNG files|*.png")
			if cspsToAdd:
				cspFiles.append(cspsToAdd)
			continueCSP = BrawlAPI.ShowYesNoPrompt("Do you have additional costumes to import?", title)
			if continueCSP:
				continue
			else:
				break
		# BPs
		bpFiles = BrawlAPI.OpenMultiFileDialog("Select vBrawl BP files", "PNG files|*.png")
		bpName = BrawlAPI.OpenFileDialog("Select vBrawl BP name", "PNG files|*.png")
		remixBpFiles = BrawlAPI.OpenMultiFileDialog("Select REMIX BP files", "PNG files|*.png")

		# CSS Icons
		pPlusIcon = BrawlAPI.OpenFileDialog("Select P+ style CSS icon", "PNG files|*.png")

		pmIcon = BrawlAPI.OpenFileDialog("Select PM style CSS icon", "PNG files|*.png")
		pmIconName = BrawlAPI.OpenFileDialog("Select PM style CSS icon nameplate", "PNG files|*.png")

		remixIcon = BrawlAPI.OpenFileDialog("Select REMIX style CSS icon", "PNG files|*.png")

		brawlIcon = BrawlAPI.OpenFileDialog("Select vBrawl style CSS icon", "PNG files|*.png")
		brawlIconName = BrawlAPI.OpenFileDialog("Select vBrawl style CSS icon nameplate", "PNG files|*.png")

		# Portrait Names
		pmName = BrawlAPI.OpenFileDialog("Select PM style portrait name", "PNG files|*.png")
		
		brawlName = BrawlAPI.OpenFileDialog("Select vBrawl style portrait name", "PNG files|*.png")

		# Stocks
		BrawlAPI.ShowMessage("You will be prompted to select your fighter's stock icon files. When you select multiple files, they will be color smashed.\n\nYou will receive the prompt multiple times, so you can have multiple sets of stocks that are not all color smashed together.", title)
		stockIcons = []
		while True:
			stockIconsToAdd = BrawlAPI.OpenMultiFileDialog("Select fighter stock icon files (if multiple, images will be color smashed)", "PNG files|*.png")
			if stockIconsToAdd:
				stockIcons.append(stockIconsToAdd)
			continueStockIcons = BrawlAPI.ShowYesNoPrompt("Do you have additional costumes to import?", title)
			if continueStockIcons:
				continue
			else:
				break

		# Replay Icon
		replayIcon = BrawlAPI.OpenFileDialog("Select replay icon", "PNG files|*.png")

		# Soundbank
		soundbank = BrawlAPI.OpenFileDialog("Select soundbank file", "SAWND files|*.sawnd")

		# Kirby hats
		installKirbyHats = BrawlAPI.ShowYesNoPrompt("Does your fighter have Kirby hat files to import?", title)
		if installKirbyHats:
			kirbyHatFiles = BrawlAPI.OpenMultiFileDialog("Select your fighter's kirby hat PAC files", "PAC files|*.pac")
			# Prompt user to input kirby hat fighter ID
			idEntered = False
			while idEntered != True:
				kirbyHatId = BrawlAPI.UserStringInput("Enter the fighter ID for your kirby hat")
				# Ensure fighter ID is just the hex digits
				if kirbyHatId.startswith('0x'):
					kirbyHatId = kirbyHatId
					break
				elif kirbyHatId.isnumeric():
					kirbyHatId = '0x' + str(hex(int(kirbyHatId))).split('0x')[1].upper()
					break
				else:
					BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
					continue
		else:
			kirbyHatFiles = 0
			kirbyHatId = ''

		# Franchise Icons
		franchiseIconBlack = BrawlAPI.OpenFileDialog("Select franchise icon with black background", "PNG files|*.png")
		franchiseIconTransparent = BrawlAPI.OpenFileDialog("Select franchise icon with transparent background", "PNG files|*.png")

		# Victory Theme
		victoryTheme = BrawlAPI.OpenFileDialog("Select your victory .brstm file", "BRSTM files|*.brstm")

		# Classic Intro
		classicIntro = BrawlAPI.OpenFileDialog("Select your classic intro .brres file", "BRRES files|*.brres")

		# Credits Theme
		creditsTheme = BrawlAPI.OpenFileDialog("Select your credits .brstm file", "BRSTM files|*.brstm")

		# Ending Files
		endingFiles = BrawlAPI.OpenMultiFileDialog("Select your ending .pac files", "PAC files|*.pac")

		# Ending Movie
		endingMovie = BrawlAPI.OpenFileDialog("Select your ending movie file", "THP files|*.thp")

		# Trophy
		trophySettings = TrophySettings()
		trophyModel = ""
		trophyThumbnail = ""
		configureTrophy = BrawlAPI.ShowYesNoPrompt("Would you like to configure a trophy for your custom fighter?", title)
		if configureTrophy:
			trophyModel = BrawlAPI.OpenFileDialog("Select your trophy model .brres file", "BRRES files|*.brres")
			trophyThumbnail = BrawlAPI.OpenFileDialog("Select your trophy thumbnail .png file", "PNG files|*.png")
			trophySettings.trophyName = BrawlAPI.UserStringInput("Enter trophy name")
			BrawlAPI.ShowMessage("You will be prompted to enter a trophy description. You can use <br/> to create line breaks in this description.", title)
			trophySettings.description = BrawlAPI.UserStringInput("Enter trophy description")
			trophySettings.gameName1 = BrawlAPI.UserStringInput("Enter the name of your character's first game")
			trophySettings.gameName2 = BrawlAPI.UserStringInput("Enter the name of your character's second game")
			BrawlAPI.ShowMessage("You will be prompted to choose values for two game icons. Enter an integer corresponding to one of the below options.\n0 : None\n1 : Nintendo 64\n2 : Gamecube\n3 : NES\n4 : Famicom Disk System\n5 : Nintendo DS\n6 : Super Nintendo\n7 : Gameboy Advance\n8 : Gameboy\n9 : Wii\n10 : Game & Watch", title)
			trophySettings.gameIcon1 = BrawlAPI.UserIntegerInput(title, "Game Icon 1 Option: ", 0, 0, 10)
			trophySettings.gameIcon2 = BrawlAPI.UserIntegerInput(title, "Game Icon 2 Option: ", 0, 0, 10)
			BrawlAPI.ShowMessage("You will be prompted to choose a value for your character's series. Enter an integer corresponding to one of the below options.\n0 : Super Smash Bros.\n1 : The Subspace Emissary\n2 : Super Mario Bros.\n3 : Donkey Kong\n4 : The Legend of Zelda\n5 : Metroid\n6 : Yoshi's Island\n7 : Kirby Super Star\n8 : Star Fox\n9 : Pokemon\n10 : F-Zero\n11 : Mother\n12 : Ice Climber\n13 : Fire Emblem\n14 : Kid Icarus\n15 : WarioWare\n16 : Pikmin\n17 : Animal Crossing\n18 : Game & Watch\n19 : Others\n20 : Metal Gear Solid\n21 : Sonic the Hedgehog", title)
			trophySettings.seriesIndex = BrawlAPI.UserIntegerInput(title, "Series Option: ", 0, 0, 21)

		# Codes
		codeFiles = BrawlAPI.OpenMultiFileDialog("Select .asm code files", "ASM files|*.asm")

		# Stage directory
		Directory.CreateDirectory(AppPath + '/temp')

		if exConfigs:
			for file in exConfigs:
				copyFile(file, AppPath + '/temp/EXConfigs')

		if fighterFiles:
			for file in fighterFiles:
				copyFile(file, AppPath + '/temp/Fighter')

		if moduleFile:
			copyFile(moduleFile, AppPath + '/temp/Module')
		if cspFiles != []:
			i = 1
			for fileSet in cspFiles:
				j = 1
				for file in fileSet:
					copyRenameFile(file, addLeadingZeros(str(j), 4) + '.png', AppPath + '/temp/CSPs/' + addLeadingZeros(str(i), 4))
					j += 1
				i += 1

		if bpFiles:
			i = 1
			for file in bpFiles:
				copyRenameFile(file, addLeadingZeros(str(i), 4) + '.png', AppPath + '/temp/BPs/vBrawl')
				i += 1
		
		if bpName:
			copyFile(bpName, AppPath + '/temp/BPs/vBrawl/Name')

		if remixBpFiles:
			i = 1
			for file in remixBpFiles:
				copyRenameFile(file, addLeadingZeros(str(i), 4) + '.png', AppPath + '/temp/BPs/REMIX')
				i += 1

		if pPlusIcon:
			copyFile(pPlusIcon, AppPath + '/temp/CSSIcon/P+')

		if pmIcon:
			copyFile(pmIcon, AppPath + '/temp/CSSIcon/PM')
			if pmIconName:
				copyFile(pmIconName, AppPath + '/temp/CSSIcon/PM/Name')

		if remixIcon:
			copyFile(remixIcon, AppPath + '/temp/CSSIcon/REMIX')

		if brawlIcon:
			copyFile(brawlIcon, AppPath + '/temp/CSSIcon/vBrawl')
			if brawlIconName:
				copyFile(brawlIconName, AppPath + '/temp/CSSIcon/vBrawl/Name')

		if pmName:
			copyFile(pmName, AppPath + '/temp/PortraitName/PM')

		if brawlName:
			copyFile(brawlName, AppPath + '/temp/PortraitName/vBrawl')

		if replayIcon:
			copyFile(replayIcon, AppPath + '/temp/ReplayIcon')

		if stockIcons != []:
			i = 1
			for fileSet in stockIcons:
				j = 1
				for file in fileSet:
					copyRenameFile(file, addLeadingZeros(str(j), 4) + '.png', AppPath + '/temp/StockIcons/' + addLeadingZeros(str(i), 4))
					j += 1
				i += 1

		if soundbank:
			copyFile(soundbank, AppPath + '/temp/Soundbank')

		if kirbyHatFiles:
			for file in kirbyHatFiles:
				copyFile(file, AppPath + '/temp/KirbyHats')
			if kirbyHatId:
				File.WriteAllText(AppPath + '/temp/KirbyHats/FighterID.txt', kirbyHatId)

		if franchiseIconBlack:
			copyFile(franchiseIconBlack, AppPath + '/temp/FranchiseIcons/Black')
		
		if franchiseIconTransparent:
			copyFile(franchiseIconTransparent, AppPath + '/temp/FranchiseIcons/Transparent')

		if victoryTheme:
			copyFile(victoryTheme, AppPath + '/temp/VictoryTheme')

		if classicIntro:
			copyFile(classicIntro, AppPath + '/temp/ClassicIntro')

		if creditsTheme:
			copyFile(creditsTheme, AppPath + '/temp/CreditsTheme')

		if endingFiles:
			for file in endingFiles:
				copyFile(file, AppPath + '/temp/Ending')

		if endingMovie:
			copyFile(endingMovie, AppPath + '/temp/Ending')

		if configureTrophy:
			if trophyModel:
				copyFile(trophyModel, AppPath + '/temp/Trophy')
			if trophyThumbnail:
				copyFile(trophyThumbnail, AppPath + '/temp/Trophy')
			attrs = vars(trophySettings)
			writeString = '\n'.join("%s = %s" % item for item in attrs.items())
			if writeString:
				File.WriteAllText(AppPath + '/temp/Trophy/TrophySettings.txt', writeString)
		
		if codeFiles:
			for codeFile in codeFiles:
				copyFile(codeFile, AppPath + '/temp/Codes')

		fighterSettings = FighterSettings()
		setThrowRelease = BrawlAPI.ShowYesNoPrompt("Would you like to set a throw release point for your fighter? (This step is optional.)", title)
		if setThrowRelease:
			fighterSettings.throwReleasePoint.append(BrawlAPI.UserFloatInput("Enter the first value", "First value in throw release code", 0.0))
			fighterSettings.throwReleasePoint.append(BrawlAPI.UserFloatInput("Enter the second value", "Second value in throw release code", 0.0))

		setCreditsThemeId = BrawlAPI.ShowYesNoPrompt("Would you like to set a specific custom credits theme ID for your fighter? (This step is optional. Only do this if you want this fighter to use a specific vanilla credits theme.)", title)
		if setCreditsThemeId:
			fighterSettings.creditsThemeId = showIdPrompt("Credits Theme ID")

		if moduleFile:
			moduleName = getClonedModuleName(moduleFile)
			if moduleName == 'ft_lucario':
				setLucarioCodes = BrawlAPI.ShowYesNoPrompt("This character appears to be a Lucario clone. Would you like to set values for the Lucario code fixes used in P+Ex?", title)
				if setLucarioCodes:
					fighterSettings.lucarioBoneId = showIdPrompt("Bone ID - Aura Sphere Fix")
					fighterSettings.lucarioKirbyEffectId = showIdPrompt("Kirby Effect.pac ID - Aura Sphere Fix")
			if moduleName == 'ft_purin':
				setJigglypuffCodes = BrawlAPI.ShowYesNoPrompt("This character appears to be a Jigglypuff clone. Would you like to set values for the Jigglypuff code fixes used in P+Ex?", title)
				if setJigglypuffCodes:
					fighterSettings.jigglypuffBoneId = showIdPrompt("Bone ID - Rollout Fix")
					fighterSettings.jigglypuffEFLSId = showIdPrompt("EFLS ID - Rollout Fix")
					fighterSettings.jigglypuffSfxIds = ""
					fighterSettings.jigglypuffSfxIds = fighterSettings.jigglypuffSfxIds + "" + showIdPrompt("SFX ID 1 - Rollout Fix")
					fighterSettings.jigglypuffSfxIds = fighterSettings.jigglypuffSfxIds + "," + showIdPrompt("SFX ID 2 - Rollout Fix")
					fighterSettings.jigglypuffSfxIds = fighterSettings.jigglypuffSfxIds + "," + showIdPrompt("SFX ID 3 - Rollout Fix")
					fighterSettings.jigglypuffSfxIds = fighterSettings.jigglypuffSfxIds + "," + showIdPrompt("SFX ID 4 - Rollout Fix")
			if moduleName == 'ft_koopa':
				setBowserCodes = BrawlAPI.ShowYesNoPrompt("This character appears to be a Bowser clone. Would you like to set values for the Bowser code fixes used in P+Ex?", title)
				if setBowserCodes:
					fighterSettings.bowserBoneId = showIdPrompt("Bone ID - Firebreath Fix")

			attrs = vars(fighterSettings)
			writeString = '\n'.join("%s = %s" % item for item in attrs.items())
			if writeString:
				File.WriteAllText(AppPath + '/temp/FighterSettings.txt', writeString)

		outputDirectory = BrawlAPI.OpenFolderDialog("Select output directory")
		fileName = BrawlAPI.UserStringInput("Enter a file name")
		
		ZipFile.CreateFromDirectory(AppPath + '/temp', outputDirectory + '/' + fileName + '.zip')

		BrawlAPI.ShowMessage("Fighter package created at " + outputDirectory + '\\' + fileName + '.zip', title)

main()