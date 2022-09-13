version = "1.0"
# BrawlInstallerLib
# Functions used by BrawlInstaller plugins

import binascii
import clr
clr.AddReference("System.Drawing")
clr.AddReference("System.IO.Compression.FileSystem")
from BrawlCrate.API import BrawlAPI
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.UI import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.Types import *
from BrawlLib.Internal import *
from BrawlLib.Internal.Windows.Forms import *
from BrawlCrate.NodeWrappers import *
from BrawlCrate.ExternalInterfacing.ColorSmash import *
from BrawlLib.Wii.Textures import *
from System.IO import *
from System import Array
from System.Diagnostics import Process
from System.Drawing import Size
from System.Collections.Generic import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from System.IO.Compression import ZipFile

# TODO: Rename files when importing for most things

#region CONSTANTS

RESOURCE_PATH = AppPath + '/BrawlAPI/Resources/BrawlInstaller'

BASE_BACKUP_PATH = AppPath + '\\Backups'

BACKUP_PATH = BASE_BACKUP_PATH + '\\backup'

LOG_PATH = AppPath + '\\Logs'

FIGHTER_IDS = {
	0 : "Mario",
	1 : "Donkey",
	2 : "Link",
	3 : "Samus",
	4 : "Yoshi",
	5 : "Kirby",
	6 : "Fox",
	7 : "Pikachu",
	8 : "Luigi",
	9 : "Captain",
	10 : "Ness",
	11 : "Koopa",
	12 : "Peach",
	13 : "Zelda",
	14 : "Sheik",
	15 : "Popo",
	16 : "Nana",
	17 : "Marth",
	18 : "GameWatch",
	19 : "Falco",
	20 : "Ganon",
	21 : "Wario",
	22 : "MetaKnight",
	23 : "Pit",
	24 : "SZeroSuit",
	25 : "Pikmin",
	26 : "Lucas",
	27 : "Diddy",
	28 : "PokeTrainer",
	29 : "PokeLizardon",
	30 : "PokeZenigame",
	31 : "PokeFushigisou",
	32 : "Dedede",
	33 : "Lucario",
	34 : "Ike",
	35 : "Robot",
	36 : "Pramai",
	37 : "Purin",
	38 : "Mewtwo",
	39 : "Roy",
	40 : "Dr_Mario",
	41 : "ToonLink",
	42 : "ToonZelda",
	43 : "ToonSheik",
	44 : "Wolf",
	45 : "Dixie",
	46 : "Snake",
	47 : "Sonic",
	48 : "GKoopa",
	49 : "WarioMan",
	50 : "ZakoBoy",
	51 : "ZakoGirl",
	52 : "ZakoChild",
	53 : "ZakoBall",
	54 : "MarioD"
}

KIRBY_SOUNDBANKS = {
	"Mario" : 57,
	"Donkey" : 45,
	"Link" : 53,
	"Samus" : 71,
	"Yoshi" : 75,
	"Kirby" : 41,
	"Fox" : 47,
	"Pikachu" : 62,
	"Luigi" : 56,
	"Captain" : 42,
	"Ness" : 60,
	"Koopa" : 52,
	"Peach" : 61,
	"Zelda" : 68,
	"Sheik" : 68,
	"Popo" : 50,
	"Nana" : 50,
	"Marth" : 58,
	"GameWatch" : 48,
	"Falco" : 46,
	"Ganon" : 49,
	"Wario" : 73,
	"MetaKnight" : 59,
	"Pit" : 64,
	"SZeroSuit" : 71,
	"Pikmin" : 63,
	"Lucas" : 55,
	"Diddy" : 44,
	"PokeTrainer" : 0,
	"PokeLizardon" : 41,
	"PokeZenigame" : 41,
	"PokeFushigisou" : 41,
	"Dedede" : 43,
	"Lucario" : 54,
	"Ike" : 51,
	"Robot" : 67,
	"Pramai" : 0,
	"Purin" : 34,
	"Mewtwo" : 0,
	"Roy" : 0,
	"Dr_Mario" : 0,
	"ToonLink" : 72,
	"ToonZelda" : 0,
	"ToonSheik" : 0,
	"Wolf" : 74,
	"Dixie" : 0,
	"Snake" : 69,
	"Sonic" : 70,
	"GKoopa" : 0,
	"WarioMan" : 73,
	"ZakoBoy" : 0,
	"ZakoGirl" : 0,
	"ZakoChild" : 0,
	"ZakoBall" : 0,
	"MarioD" : 0
}

#endregion CONSTANTS

#region HELPER FUNCTIONS
# These are common functions frequently used by parts of the BrawlInstaller plugin suite

# Get child node by name; similar to markyMawwk's function, but didn't want to make it a dependency
def getChildByName(node, name):
		if node.Children:
			for child in node.Children:
				if child.Name == str(name):
					return child
		return 0

# Get child node by FighterID
def getChildByFighterID(node, fighterId):
		if node.Children:
			for child in node.Children:
				if child.FighterID == int(fighterId, 16):
					return child
		return 0

# Helper function to sort PAT0Entry nodes by FrameIndex
def sortChildrenByFrameIndex(parentNode):
		childList = []
		for child in parentNode.Children:
			childList.append(child)
		for child in childList:
			while child.PrevSibling() is not None and child.FrameIndex < child.PrevSibling().FrameIndex:
				child.MoveUp()

# Helper function that gets files from a directory by their name
def getFileByName(name, directory):
		writeLog("Attempting to get file " + name + " at directory " + directory.FullName)
		files = Directory.GetFiles(directory.FullName, name)
		if files:
			return getFileInfo(files[0])
		else:
			return 0

# Helper function that gets a directory from a base directory by specified name
def getDirectoryByName(name, baseDirectory):
		writeLog("Attempting to get directory " + name)
		for directory in baseDirectory:
			if directory.Name == name:
				return directory
		return 0

# Helper function to get FileInfo object for file and return an error if invalid
def getFileInfo(filePath):
		try:
			writeLog("Attempting to read file " + filePath)
			return FileInfo(filePath)
		except Exception as e:
			BrawlAPI.ShowMessage("Error occurred trying to process filepath " + filePath + ", please check that the default build path and all paths in settings.ini are formatted correctly.", "Filepath Error")
			raise e

# Helper function that gets names of all files in the provided directory
def getFileNames(directory):
		files = directory.GetFiles()
		fileNames = [0] * len(files)
		for i, file in enumerate(files):
			fileNames[i] = file.FullName
		return Array[str](fileNames)

# Helper function to create a directory if it does not exist
def createDirectory(path):
		if not Directory.Exists(path):
			Directory.CreateDirectory(path)
		return path

# Helper function that imports a texture automatically without prompting the user
def importTexture(node, imageSource, format, sizeW=0, sizeH=0):
		writeLog("Importing texture " + imageSource + " to node " + node.Name)
		dlg = TextureConverterDialog()
		dlg.ImageSource = imageSource
		dlg.InitialFormat = format
		dlg.Automatic = 1
		# Resize image if sizes are passed in
		if sizeW != 0:
			if sizeH != 0:
				# If both width and height are passed in, resize using both
				dlg.InitialSize = Size(sizeW, sizeH)
			# If only width is passed in, use it for both
			else:
				dlg.InitialSize = Size(sizeW, sizeW)
		dlg.ShowDialog(MainForm.Instance, node)
		dlg.Dispose()
		texFolder = getChildByName(node, "Textures(NW4R)")
		newNode = texFolder.Children[len(texFolder.Children) - 1]
		writeLog("Texture " + imageSource + " imported successfully")
		return newNode

# Helper function that checks if the file passed in is opened in BrawlCrate
def checkOpenFile(fileName):
		if str(BrawlAPI.RootNode) != "None":
			if str(BrawlAPI.RootNode.Name).startswith(fileName):
				return 1
		return 0

# Got this helper method from markymawwk's code, adds leading zeroes
def addLeadingZeros(value, count):
		while len(str(value)) < count:
			value = "0" + str(value)
		return str(value)

# Gotten from markymawwk's code, gets song IDs that have already been used for tracklists
def getUsedSongIds(parentNode):
		writeLog("Checking song IDs currently in use")
		IDs = []
		for track in parentNode.Children:
			if track.SongID >= 61440: #0xF000 
				IDs.append(track.SongID)
		writeLog("Finished song ID check")
		return IDs

# Helper function to get children where the first characters match what is passed in
def getChildrenByPrefix(parentNode, prefix):
		matches = []
		for child in parentNode.Children:
			if child.Name.StartsWith(prefix):
				matches.append(child)
		return matches

# Helper function to add a new pat0TexEntry to specified pat0
def addToPat0(parentNode, pat0NodeName, pat0texNodeName, name, texture, frameIndex, palette="", frameCountOffset=0, overrideFrameCount=0):
		writeLog("Adding " + name + " to PAT0 " + pat0NodeName + " in parent node " + parentNode.Name)
		pat0Node = getChildByName(getChildByName(parentNode, "AnmTexPat(NW4R)"), pat0NodeName)
		# Add to pat0texNode
		pat0texNode = getChildByName(pat0Node, pat0texNodeName).Children[0]
		pat0texEntryNode = PAT0TextureEntryNode()
		pat0texEntryNode.FrameIndex = frameIndex
		pat0texEntryNode.Name = name
		pat0texEntryNode.Texture = texture
		pat0texNode.AddChild(pat0texEntryNode)
		# Palette gets screwed up for some reason if we don't do it this way
		if palette != "":
			pat0texEntryNode = getChildByName(pat0texNode, name)
			pat0texEntryNode.Palette = palette
		sortChildrenByFrameIndex(pat0texNode)
		if overrideFrameCount > pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset:
			pat0Node.FrameCount = overrideFrameCount
		elif frameCountOffset != 0:
			pat0Node.FrameCount = pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset
		writeLog("PAT0 entry added successfully")

# Helper function to remove pat0TexEntry from specified pat0
def removeFromPat0(parentNode, pat0NodeName, pat0texNodeName, name, frameCountOffset=0, overrideFrameCount=0):
		writeLog("Removing " + name + " from PAT0 " + pat0NodeName + " in parent node " + parentNode.Name)
		pat0Node = getChildByName(getChildByName(parentNode, "AnmTexPat(NW4R)"), pat0NodeName)
		# Remove from pat0texNode
		pat0texNode = getChildByName(pat0Node, pat0texNodeName).Children[0]
		pat0texEntryNode = getChildByName(pat0texNode, name)
		if pat0texEntryNode:
			pat0texEntryNode.Remove()
		if overrideFrameCount > pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset:
			pat0Node.FrameCount = overrideFrameCount
		elif frameCountOffset != 0:
			pat0Node.FrameCount = pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset
		writeLog("PAT0 entry removed successfully")

# Get value of key from settings
def readValueFromKey(settings, key):
		writeLog("Attempting to read setting " + key + " from settings file")
		# Search for a matching key and if one is found, return value
		for line in settings:
			if line.StartsWith(';') or len(line) == 0:
				continue
			if str(line.split('=')[0]).strip() == key:
				writeLog("Setting " + key + " found with value " + str(line.split('=')[1]).strip())
				return str(line.split('=')[1]).strip()
		writeLog("No value found for setting " + key)
		return ""

# Check if fighter ID is already in use
def getFighterConfig(fighterId):
		writeLog("Attempting to get FighterConfig for ID " + str(fighterId))
		fighterConfigs = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig', 'Fighter' + str(fighterId) + '.dat')
		if fighterConfigs:
			return fighterConfigs[0]
		else:
			return 0

# Check if cosmetic ID is already in use
def getCosmeticConfig(fighterId):
		writeLog("Attempting to get CosmeticConfig for ID " + str(fighterId))
		cosmeticConfigs = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig', 'Cosmetic' + str(fighterId) + '.dat')
		if cosmeticConfigs:
			return cosmeticConfigs[0]
		else:
			return 0

# Check if slot ID is already in use
def getSlotConfig(fighterId):
		writeLog("Attempting to get SlotConfig for ID " + str(fighterId))
		slotConfigs = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig', 'Slot' + str(fighterId) + '.dat')
		if slotConfigs:
			return slotConfigs[0]
		else:
			return 0

# Get Effect.pac ID for specified fighter name
def getEffectId(fighterName, rootDir=""):
		writeLog("Getting effect ID for fighter name " + fighterName)
		if rootDir == "":
			dir = MainForm.BuildPath + '/pf/fighter/' + fighterName
		else:
			dir = rootDir
		if Directory.Exists(dir):
			fighterFiles = Directory.GetFiles(dir, 'Fit' + fighterName + '.pac')
			if fighterFiles:
				BrawlAPI.OpenFile(fighterFiles[0])
				if BrawlAPI.RootNode.Children:
					for node in BrawlAPI.RootNode.Children:
						if node.Name.StartsWith("ef_custom"):
							effectId = node.Name.split('ef_custom')[1]
							BrawlAPI.ForceCloseFile()
							return effectId
		BrawlAPI.ForceCloseFile()
		return 0

# Get song name from tracklist by song ID
def getSongNameById(songId, songDirectory='Victory!', tracklist='Results'):
		writeLog("Getting song name from song ID " + str(songId))
		BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist + '.tlst')
		for song in BrawlAPI.RootNode.Children:
			if song.SongID == songId:
				BrawlAPI.ForceCloseFile()
				return song.SongFileName.split(songDirectory + '/')[1]
		BrawlAPI.ForceCloseFile()
		return 0

# Get the victory theme of a fighter by their ID
def getVictoryThemeByFighterId(fighterId):
		writeLog("Getting victory theme by fighter ID " + str(fighterId))
		slotConfig = getSlotConfig(fighterId)
		if slotConfig:
			BrawlAPI.OpenFile(slotConfig)
			songId = BrawlAPI.RootNode.VictoryTheme
			BrawlAPI.ForceCloseFile()
			songName = getSongNameById(songId)
			return songName
		return 0

# Get the victory theme ID of a fighter by their ID
def getVictoryThemeIDByFighterId(slotId):
		writeLog("Getting victory theme ID by fighter slot ID " + str(slotId))
		slotConfig = getSlotConfig(slotId)
		if slotConfig:
			BrawlAPI.OpenFile(slotConfig)
			songId = BrawlAPI.RootNode.VictoryTheme
			BrawlAPI.ForceCloseFile()
			return songId
		return 0

# Helper method to more easily copy files
def copyFile(sourcePath, destinationPath):
		writeLog("Copying file " + sourcePath + " to " + destinationPath)
		Directory.CreateDirectory(destinationPath)
		File.Copy(sourcePath, destinationPath + '/' + getFileInfo(sourcePath).Name, True)

# Helper method to create a backup of the provided file with correct folder structure
def createBackup(sourcePath):
		writeLog("Creating backup of file " + sourcePath)
		fullPath = BACKUP_PATH + sourcePath.replace(MainForm.BuildPath, '')
		path = fullPath.replace(getFileInfo(sourcePath).Name, '')
		Directory.CreateDirectory(path)
		if File.Exists(sourcePath) and not File.Exists(fullPath):
			File.Copy(sourcePath, fullPath)

# Helper method to write a log
def writeLog(message):
		Directory.CreateDirectory(LOG_PATH)
		if File.Exists(LOG_PATH + '\\log.txt'):
			File.AppendAllText(LOG_PATH + '\\log.txt', message + "\n")

# Helper method to create log file
def createLogFile():
		Directory.CreateDirectory(LOG_PATH)
		File.WriteAllText(LOG_PATH + '\\log.txt', "--LOG START-\n")

# Helper method to check if a file is open, and if it is not, open it and create a backup
def openFile(filePath, backup=True):
		writeLog("Attempting to open file " + filePath)
		nodeName = getFileInfo(filePath).Name.split('.')[0]
		fileOpened = checkOpenFile(nodeName)
		if fileOpened == 0:
			if backup:
				createBackup(filePath)
			fileOpened = BrawlAPI.OpenFile(filePath)
		return fileOpened

# Helper method to more easily copy and rename files
def copyRenameFile(sourcePath, newName, destinationPath):
		writeLog("Attempting to copy file " + sourcePath + " to " + destinationPath + '/' + newName)
		Directory.CreateDirectory(destinationPath)
		File.Copy(sourcePath, destinationPath + '/' + newName, True)

# Return the text version of a boolean value
def boolText(boolVal):
		if boolVal == True:
			return "true"
		else:
			return "false"

# Ensure an ID is hexadecimal whether it was passed in as decimal or hex
def hexId(id):
		if str(id).startswith('0x'):
			id = str(id).upper().replace('0X', '0x')
			return id
		elif str(id).isnumeric():
			id = str(hex(int(id))).upper().replace('0X', '0x')
			return id
		else:
			return ""

# Create a prompt for user to enter a valid ID in hex or dec format
def showIdPrompt(message):
		idEntered = False
		while idEntered != True:
			id = hexId(BrawlAPI.UserStringInput(message))
			if id != "":
				return id
			else:
				BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
				continue

#endregion HELPER FUNCTIONS

#region IMPORT FUNCTIONS
# Functions used by the BrawlInstaller suite to add elements to a build

# Import CSPs
def importCSPs(cosmeticId, directory, rspLoading="false"):
		writeLog("Importing CSPs with cosmetic ID " + str(cosmeticId))
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			# Find char_bust_tex_lz77
			arcNode = getChildByName(BrawlAPI.RootNode, "char_bust_tex_lz77")
			# Create a new node and then sort
			newNode = BRRESNode()
			newNode.Name = "Misc Data [" + str(cosmeticId) + "]"
			newNode.FileType = ARCFileType.MiscData
			newNode.FileIndex = cosmeticId
			newNode.Compression = "ExtendedLZ77"
			arcNode.AddChild(newNode)
			BaseWrapper.Wrap(arcNode).SortChildrenByFileIndex()
			# Import images from folders
			for folder in Directory.GetDirectories(directory.FullName):
				writeLog("Importing CSPs from folder " + folder)
				images = Directory.GetFiles(folder, "*.png")
				# Color smash images in folders with multiple
				if len(images) > 1:
					ColorSmashImport(newNode, images, 256)
				else:
					importTexture(newNode, images[0], WiiPixelFormat.CI8, 128, 160)
			# Rename the texture nodes
			texFolder = getChildByName(newNode, "Textures(NW4R)")
			texNodes = texFolder.GetChildrenRecursive()
			i = 1
			for texNode in texNodes:
				texNode.Name = "MenSelchrFaceB." + addLeadingZeros(str((cosmeticId * 10) + i), 2)
				i += 1
			# Export RSP while we're at it
			newNode.Compression = "None"
			# Back up RSP if it exists
			createBackup(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
			writeLog("Exporting RSPs")
			newNode.Export(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
			# Set compression back
			newNode.Compression = "ExtendedLZ77"
			# If user has RSP loading on, get rid of changes to this file
			if rspLoading == "true":
				newNode.Remove()
			writeLog("Importing CSPs completed successfully")

# Import stock icons
def importStockIcons(cosmeticId, directory, tex0BresName, pat0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true"):
		writeLog("Importing stock icons to " + filePath + " with cosmetic ID " + str(cosmeticId))
		# If info.pac is not already opened, open it
		# Check this out: https://github.com/soopercool101/BrawlCrate/blob/b089bf32f0cfb2b5f1e6d729b95da4dd169903f2/BrawlCrate/NodeWrappers/Graphics/TEX0Wrapper.cs#L231
		fileOpened = openFile(MainForm.BuildPath + filePath)
		if fileOpened:
			rootNode = BrawlAPI.RootNode
			if rootName != "":
				rootNode = getChildByName(BrawlAPI.RootNode, rootName)
			if tex0BresName != "":
				node = getChildByName(rootNode, tex0BresName)
			else:
				node = rootNode
			# Import images and color smash them
			totalImages = []
			for folder in Directory.GetDirectories(directory.FullName):
				writeLog("Importing stock icons from folder " + folder)
				images = Directory.GetFiles(folder, "*.png")
				# Color smash images in folders with multiple
				if len(images) > 1:
					writeLog("Color smashing stock icons")
					ColorSmashImport(node, images, 256)
					writeLog("Imported color smashed icons")
				else:
					writeLog("Importing standalone icon")
					importTexture(node, images[0], WiiPixelFormat.CI8, 32, 32)
					writeLog("Imported standalone icon")
				for image in images:
					totalImages.append(image)
			# Rename the texture nodes
			texFolder = getChildByName(node, "Textures(NW4R)")
			# Get the starting ID for imported stocks
			newId = (cosmeticId * 50) + 1 if fiftyCC == "true" else int(str(cosmeticId) + "1")
			# Change the name of each newly added node and store it
			texNodes = []
			imageCount = len(totalImages)
			while imageCount > 0:
				texNode = texFolder.Children[len(texFolder.Children) - imageCount]
				# If using 50CC, the ID should be 4 characters, otherwise it's 3
				texNode.Name = "InfStc." + addLeadingZeros(str(newId), 4 if fiftyCC == "true" else 3)
				texNodes.append(texNode)
				newId += 1
				imageCount -= 1
			# Add to pat0
			if pat0BresName == "":
				return
			pat0BresNode = getChildByName(rootNode, pat0BresName)
			anmTexPat = getChildByName(pat0BresNode, "AnmTexPat(NW4R)")
			if (BrawlAPI.RootNode.Name.StartsWith("sc_selmap")):
				pat0Nodes = [ getChildByName(anmTexPat, "MenSelmapPlayer1_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer2_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer3_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer4_TopN") ]
			else:
				pat0Nodes = [ getChildByName(anmTexPat, "InfStockface_TopN__0") ]
			for pat0Node in pat0Nodes:
				# For each texture we added, add a pat0 entry
				for texNode in texNodes:
					# Frame count is 9201 with 50 CC, 501 without, and it's 9301 or 601 on sc_selmap
					frameCount = 9201 if fiftyCC == "true" else 501
					if BrawlAPI.RootNode.Name.StartsWith("sc_selmap"):
						frameCount += 100
					addToPat0(pat0BresNode, pat0Node.Name, pat0Node.Children[0].Name, texNode.Name, texNode.Name, int(texNode.Name.split('.')[1]), palette=texNode.Name, frameCountOffset=1, overrideFrameCount=frameCount)
		writeLog("Import stock icons completed")

# Create battle portraits frome images
def createBPs(cosmeticId, images, fiftyCC="true"):
		writeLog("Creating BPs for cosmetic ID " + str(cosmeticId))
		# For 50 costume code, we must multiply the cosmetic ID by 50
		newId = (cosmeticId * 50) + 1 if fiftyCC == "true" else int(str(cosmeticId) + "1")
		# Create a BP file for each texture
		for image in images:
			outputPath = MainForm.BuildPath + '/pf/info/portrite/InfFace' + addLeadingZeros(str(newId), 4 if fiftyCC == "true" else 3) + '.brres'
			# If the file exists already, make a backup (probably will never hit this because of the delete coming first on install but just in case)
			createBackup(outputPath)
			BrawlAPI.New[BRRESNode]()
			importTexture(BrawlAPI.RootNode, image, WiiPixelFormat.CI8)
			BrawlAPI.SaveFileAs(outputPath)
			newId += 1
		writeLog("Finished creating BPs")
		BrawlAPI.ForceCloseFile()

# Update and move EX config files
def modifyExConfigs(files, cosmeticId, fighterId, fighterName, franchiseIconId=-1, useKirbyHat=False, newSoundBankId="", victoryThemeId=0, kirbyHatFighterId=-1):
		writeLog("Modifying Ex Configs for fighter ID " + str(fighterId))
		# Iterate through each file
		for file in files:
			file = getFileInfo(file)
			BrawlAPI.OpenFile(file.FullName)
			# Update CosmeticID field and rename CosmeticConfig
			if file.Name.lower().StartsWith("cosmetic"):
				writeLog("Updating " + file.Name)
				BrawlAPI.RootNode.CosmeticID = cosmeticId
				# TODO: Allow users to choose redirects
				BrawlAPI.RootNode.HasSecondary = False
				if franchiseIconId != -1:
					BrawlAPI.RootNode.FranchiseIconID = franchiseIconId - 1
				# Back up first
				createBackup(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig/' + file.Name.replace(file.Name, "Cosmetic" + fighterId + ".dat"))
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig/' + file.Name.replace(file.Name, "Cosmetic" + fighterId + ".dat"))
			# Rename FighterConfig 
			if file.Name.lower().StartsWith("fighter"):
				writeLog("Updating " + file.Name)
				# TODO: Update fighter name based on fit[fighter].pac?
				if useKirbyHat:
					BrawlAPI.RootNode.KirbyLoadType = FCFGNode.KirbyLoadFlags.Single
					BrawlAPI.RootNode.HasKirbyHat = 1
					# Set kirby soundbank
					if kirbyHatFighterId != -1:
						kirbySoundbank = KIRBY_SOUNDBANKS[FIGHTER_IDS[kirbyHatFighterId]]
						if kirbySoundbank:
							BrawlAPI.RootNode.KirbySoundBank = kirbySoundbank
				else:
					BrawlAPI.RootNode.KirbyLoadType = FCFGNode.KirbyLoadFlags.None
					BrawlAPI.RootNode.HasKirbyHat = 0
				if newSoundBankId != "":
					BrawlAPI.RootNode.SoundBank = int(newSoundBankId, 16)
				# Set fighter name
				BrawlAPI.RootNode.FighterName = fighterName.upper()
				BrawlAPI.RootNode.PacName = fighterName + '/Fit' + fighterName.upper() + '.pac'
				BrawlAPI.RootNode.KirbyPacName = 'kirby/FitKirby' + fighterName.upper() + '.pac'
				BrawlAPI.RootNode.ModuleName = 'ft_' + fighterName.lower() + '.rel'
				BrawlAPI.RootNode.InternalFighterName = fighterName.upper()
				# Back up first
				createBackup(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig/' + file.Name.replace(file.Name, "Fighter" + fighterId + ".dat"))
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig/' + file.Name.replace(file.Name, "Fighter" + fighterId + ".dat"))
			# Rename CSSSlotConfig 
			if file.Name.lower().StartsWith("cssslot"):
				writeLog("Updating " + file.Name)
				# TODO: Allow users to choose redirects
				BrawlAPI.RootNode.SetPrimarySecondary = False
				BrawlAPI.RootNode.SetCosmeticSlot = False
				# Back up first
				createBackup(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/' + file.Name.replace(file.Name, "CSSSlot" + fighterId + ".dat"))
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/' + file.Name.replace(file.Name, "CSSSlot" + fighterId + ".dat"))
			# Rename SlotConfig
			if file.Name.lower().StartsWith("slot"):
				writeLog("Updating " + file.Name)
				if victoryThemeId:
					BrawlAPI.RootNode.VictoryTheme = victoryThemeId
				# TODO: Allow users to choose redirects
				BrawlAPI.RootNode.SetSlot = False
				# Back up first
				createBackup(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig/' + file.Name.replace(file.Name, "Slot" + fighterId + ".dat"))
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig/' + file.Name.replace(file.Name, "Slot" + fighterId + ".dat"))
			writeLog("Finished updating Ex Configs")
			BrawlAPI.ForceCloseFile()

# Import CSS icon
def importCSSIcon(cosmeticId, iconImagePath, format):
		writeLog("Attempting to import CSS icon with cosmetic ID" + str(cosmeticId))
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			# Import icon texture
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [70]")
			newNode = importTexture(node, iconImagePath, format)
			newNode.Name = "MenSelchrChrFace." + addLeadingZeros(str(cosmeticId), 3)
			# Sort textures
			newNode.Parent.SortChildren()
			# Add CSS icon to CSS
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			anmTexPat = getChildByName(node, "AnmTexPat(NW4R)")
			pat0Nodes = getChildrenByPrefix(anmTexPat, "MenSelchrFace")
			for pat0Node in pat0Nodes:
				addToPat0(node, pat0Node.Name, "Face02", newNode.Name, newNode.Name, int(str(cosmeticId) + "1"), palette=newNode.Name, frameCountOffset=10)
			writeLog("Finished importing CSS icon")

# Import replay icon
def importReplayIcon(cosmeticId, replayIconImagePath):
		writeLog("Importing replay icon with cosmetic ID " + str(cosmeticId))
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu/collection/Replay.brres')
		if fileOpened:
			# Import icon texture
			newNode = importTexture(BrawlAPI.RootNode, replayIconImagePath, WiiPixelFormat.CI8)
			newNode.Name = "MenReplayChr." + addLeadingZeros(str(cosmeticId) + "1", 3)
			# Add replay icon to pat0
			anmTexPat = getChildByName(BrawlAPI.RootNode, "AnmTexPat(NW4R)")
			pat0Node = getChildByName(anmTexPat, "MenReplayPreview2_TopN__0")
			addToPat0(BrawlAPI.RootNode, pat0Node.Name, "lambert78", newNode.Name, newNode.Name, int(str(cosmeticId) + "1"), palette=newNode.Name, frameCountOffset=10)
			writeLog("Finished importing replay icon")

# Import CSS icon name
def importCSSIconName(cosmeticId, nameImagePath):
		writeLog("Importing CSS icon name with cosmetic ID " + str(cosmeticId))
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			# Import icon name texture
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [70]")
			newNode = importTexture(node, nameImagePath, WiiPixelFormat.I4)
			newNode.Name = "MenSelchrChrNmS." + addLeadingZeros(str(cosmeticId), 3)
			# Sort textures
			newNode.Parent.SortChildren()
			# Add CSS icon name to CSS
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			anmTexPat = getChildByName(node, "AnmTexPat(NW4R)")
			pat0Nodes = getChildrenByPrefix(anmTexPat, "MenSelchrFace")
			for pat0Node in pat0Nodes:
				addToPat0(node, pat0Node.Name, "Face06", newNode.Name, newNode.Name, int(str(cosmeticId) + "1"), frameCountOffset=10)
			writeLog("Finished importing CSS icon name")
				
# Import name for character select portrait
def importPortraitName(cosmeticId, file):
		writeLog("Importing portrait name with cosmetic ID " + str(cosmeticId))
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			# Import name
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			newNode = importTexture(node, file, WiiPixelFormat.I4)
			newNode.Name = "MenSelchrChrNm." + addLeadingZeros(str(cosmeticId), 2) + '1'
			frameIndex = int(str(cosmeticId) + "1")
			addToPat0(node, "MenSelchrCname4_TopN__0", "Card010", newNode.Name, newNode.Name, frameIndex, frameCountOffset=10, overrideFrameCount=2561)
			addToPat0(node, "MenSelchrCname4_TopN__0", "Card011", newNode.Name, newNode.Name, frameIndex, frameCountOffset=10, overrideFrameCount=2561)	
			writeLog("Finished importing portrait name")

# Import franchise icon into CSS or info
def importFranchiseIcon(franchiseIconId, image, filePath, size):
		writeLog("Importing franchise icon into " + filePath + " with franchise icon ID " + str(franchiseIconId))
		fileNodeName = filePath.split('.')[0].split('/')[-1]
		fileOpened = openFile(MainForm.BuildPath + filePath)
		if fileOpened:
			# Import icon
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			if fileNodeName == "sc_selcharacter":
				# set format based on size: <= 64 should be I4, greater should be I8
				format = WiiPixelFormat.I4 if size <= 64 else WiiPixelFormat.I8
				newNode = importTexture(node, image, format, sizeW=size)
				pat0texNodeName = "Card04"
				pat0NodeName = "MenSelchrCmark4_TopN__0"
			if fileNodeName.startswith("info"):
				newNode = importTexture(node, image, WiiPixelFormat.I4, sizeW=48)
				pat0texNodeName = "lambert110"
				pat0NodeName = "InfMark_TopN__0"
			newNode.Name = "MenSelchrMark." + addLeadingZeros(str(franchiseIconId), 2)
			addToPat0(node, pat0NodeName, pat0texNodeName, newNode.Name, newNode.Name, franchiseIconId, frameCountOffset=1)
			writeLog("Finished importing franchise icon")

# Import BP name into info
def importBPName(cosmeticId, image, filePath):
		writeLog("Importing BP name into " + filePath + " with cosmetic ID " + str(cosmeticId))
		fileOpened = openFile(MainForm.BuildPath + filePath)
		if fileOpened:
			# Import name
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			format = WiiPixelFormat.I4
			newNode = importTexture(node, image, format)
			pat0texNodeName = "Character_Name_Mat"
			pat0NodeName = "InfFace_TopN__0"
			newNode.Name = "MenSelchrChrNmS." + addLeadingZeros(str(cosmeticId) + '1', 3)
			addToPat0(node, pat0NodeName, pat0texNodeName, newNode.Name, newNode.Name, int(str(cosmeticId) + '1'), frameCountOffset=10)
		writeLog("Import BP name finished.")

# Import classic intro file
def importClassicIntro(cosmeticId, filePath):
	writeLog("Importing classic intro file for cosmetic ID " + str(cosmeticId))
	createBackup(getFileInfo(filePath).Name)
	fileOpened = BrawlAPI.OpenFile(filePath)
	if fileOpened:
		# Iterate through all children to find the names we care about and rename them
		children = BrawlAPI.RootNode.GetChildrenRecursive()
		for child in children:
			if child.Name.startswith("ItrSimpleChr"):
				child.Name = "ItrSimpleChr" + addLeadingZeros(str(cosmeticId + 1), 4) + "_TopN"
			if "Ey" not in child.Name and child.Name.startswith("GmSimpleChr"):
				if child.Name.endswith("_nm1"):
					child.Name = "GmSimpleChr" + addLeadingZeros(str(cosmeticId + 1), 2) + "_nm1"
				elif child.Name.endswith("_nm2"):
					child.Name = "GmSimpleChr" + addLeadingZeros(str(cosmeticId + 1), 2) + "_nm2"
				else:
					child.Name = "GmSimpleChr" + addLeadingZeros(str(cosmeticId + 1), 2)
			if child.Name.startswith("GmSimpleChrEy"):
				child.Name = "GmSimpleChrEy" + addLeadingZeros(str(cosmeticId + 1), 2)
		BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/menu/intro/enter/chr' + addLeadingZeros(str(cosmeticId + 1), 4) + '.brres')
		BrawlAPI.ForceCloseFile()
	writeLog("Finished importing classic intro file")

# Add franchise icon to result screen
def importFranchiseIconResult(franchiseIconId, image):
		writeLog("Importing franchise icon into STGRESULT.pac with franchise icon ID " + str(franchiseIconId))
		fileOpened = openFile(MainForm.BuildPath + '/pf/stage/melee/STGRESULT.pac')
		if fileOpened:
			# Import icon
			node = getChildByName(getChildByName(BrawlAPI.RootNode, "2"), "Misc Data [110]")
			newNode = importTexture(node, image, WiiPixelFormat.CI4, sizeW=80)
			newNode.Name = "MenSelchrMark." + addLeadingZeros(str(franchiseIconId), 2)
			# Add 3D model
			modelFolder = getChildByName(node, "3DModels(NW4R)")
			mdl0Node = MDL0Node()
			mdl0Node.Name = "InfResultMark" + addLeadingZeros(str(franchiseIconId), 2) + "_TopN"
			modelFolder.AddChild(mdl0Node)
			mdl0Node.Replace(RESOURCE_PATH + '/InfResultMark##_TopN.mdl0')
			mdl0MatRefNode = getChildByName(getChildByName(getChildByName(mdl0Node, "Materials"), "Mark"), "MenSelchrMark.##")
			mdl0MatRefNode.Name = newNode.Name
			mdl0MatRefNode.Texture = newNode.Name
			mdl0MatRefNode.Palette = newNode.Name
			# Add color sequence
			colorFolder = getChildByName(node, "AnmClr(NW4R)")
			clr0Node = CLR0Node()
			clr0Node.Name = "InfResultMark" + addLeadingZeros(str(franchiseIconId), 2) + "_TopN"
			colorFolder.AddChild(clr0Node)
			clr0Node.Replace(RESOURCE_PATH + '/InfResultMark01_TopN.clr0')
			writeLog("Finished importing franchise icon")

# Update the fighter module file
def updateModule(file, directory, fighterId, fighterName):
		writeLog("Updating module file " + file)
		file = getFileInfo(file)
		BrawlAPI.OpenFile(file.FullName)
		# Get section 8 and export it
		node = getChildByName(BrawlAPI.RootNode, "Section [8]")
		if node:
			writeLog("Modifying Section [8] of module file")
			node.Export(directory.FullName + "/Section [8]")
			BrawlAPI.ForceCloseFile()
			# Get the exported section 8 file
			sectionFile = directory.FullName + "/Section [8]"
			editModule(fighterId, file, sectionFile, [0x00])
		else:
			writeLog("Module does not have Section [8]. Modifying Section [1] instead.")
			# Export section 1 instead
			node = getChildByName(BrawlAPI.RootNode, "Section [1]")
			node.Export(directory.FullName + "/Section [1]")
			rootNode = BrawlAPI.RootNode.Name
			closeModule()
			# Get the exported section 1 file
			sectionFile = directory.FullName + "/Section [1]"
			# Handle Pit module
			if rootNode == 'ft_pit':
				writeLog("Modifying module as patched PM Pit module")
				editModule(fighterId, file, sectionFile, [0xA0, 0x168, 0x1804, 0x8E4C, 0x8F3C, 0xDAE8, 0xDB50, 0xDBAC, 0x15A90, 0x16CC8])
			# Handle Marth module
			if rootNode == 'ft_marth':
				writeLog("Modifying module as Marth module")
				editModule(fighterId, file, sectionFile, [0x98, 0x160, 0x17D8, 0x5724, 0xA430, 0xA498, 0xA4F4])
			# Handle Lucario module
			if rootNode == 'ft_lucario':
				writeLog("Modifying module as Lucario module")
				editModule(fighterId, file, sectionFile, [0x98, 0x160, 0x1804, 0x83F8, 0x8510, 0x963C, 0x9794, 0xD2D0, 0xD338, 0xD394])
			# Handle Sonic module
			if rootNode == 'ft_sonic':
				writeLog("Modifying module as Sonic module")
				editModule(fighterId, file, sectionFile, [0x98, 0x160, 0x1818, 0x8598, 0xEDB8, 0xEE20, 0xEE7C])
		# Back up if already exists
		createBackup(MainForm.BuildPath + '/pf/module/ft_' + fighterName.lower() + '.rel')
		writeLog("Copying module " + file.FullName)
		File.Copy(file.FullName, MainForm.BuildPath + '/pf/module/ft_' + fighterName.lower() + '.rel', 1)
		writeLog("Finished updating module")

# Close module file cleanly
def closeModule():
		while True:
			try:
				BrawlAPI.ForceCloseFile()
			except Exception as e:
				if str(e).strip() == "Collection was modified; enumeration operation may not execute.":
					continue
			break

# Edit module offsets
def editModule(fighterId, moduleFile, sectionFile, offsets):
		writeLog("Editing module offsets")
		# Read the section file and write to it
		with open(sectionFile, mode='r+b') as editFile:
			section = editFile.read()
			for offset in offsets:
				writeLog("Editing offset " + str(offset))
				editFile.seek(int(offset) + 3)
				editFile.write(binascii.unhexlify(fighterId))
			editFile.seek(0)
			sectionModified = editFile.read()
			editFile.close()
		# Read the module file
		with open(moduleFile.FullName,  mode='r+b') as file:
			data = str(file.read())
			file.close()
		# Where the module file matches the section, replace it with our modified section values
		updatedData = data.replace(section, sectionModified)
		with open(moduleFile.FullName, mode='r+b') as file:
			file.seek(0)
			file.write(updatedData)
		writeLog("Replaced module contents")

# Move fighter files to fighter folder
def moveFighterFiles(files, fighterName, originalFighterName=""):
		writeLog("Attempting to move fighter files")
		for file in files:
			file = getFileInfo(file)
			# TODO: rename files based on fighter name?
			if originalFighterName != "":
				path = MainForm.BuildPath + '/pf/fighter/' + fighterName.lower().replace(originalFighterName.lower(), fighterName) + '/' + file.Name.lower().replace(originalFighterName.lower(), fighterName.lower())
			else:
				path = MainForm.BuildPath + '/pf/fighter/' + fighterName.lower() + '/' + file.Name
			# Back up if already exists
			createBackup(path)
			getFileInfo(path).Directory.Create()
			File.Copy(file.FullName, path, 1)
		writeLog("Finished moving fighter files")

# Update fighter .pac to use new Effect.pac ID
def updateEffectId(fighterFile, gfxChangeExe, oldEffectId, newEffectId):
		writeLog("Modifying effect ID for fighter file " + fighterFile.FullName + " to change effect ID " + str(oldEffectId) + " to " + str(newEffectId))
		BrawlAPI.OpenFile(fighterFile.FullName)
		# Rename arc node
		writeLog("Renaming ARC node")
		arcNode = getChildByName(BrawlAPI.RootNode, "ef_custom" + oldEffectId)
		arcNode.Name = "ef_custom" + newEffectId
		# Find and rename traces
		for node in arcNode.Children:
			if node.Name.StartsWith("Texture Data"):
				texFolder = getChildByName(node, "Textures(NW4R)")
				if texFolder:
					for tex0 in texFolder.Children:
						if tex0.Name.StartsWith("TexCustom"):
							tex0.Name = str(tex0.Name.split("Trace")[0]).replace(oldEffectId, newEffectId) + "Trace" + tex0.Name.split("Trace")[1]
		# Export fighter moveset
		writeLog("Exporting fighter moveset")
		moveset = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
		moveset.Export(gfxChangeExe.Directory.FullName + '/moveset.dat')
		# Create traces.txt
		writeLog("Creating traces.txt")
		traceString = ""
		i = 0
		#for trace in traces:
		while i < 9:
			traceString = traceString + str(hex(141 + (int(oldEffectId, 16) * 10) + i)).upper().replace('X', 'x') + ' ' + str(hex(141 + (int(newEffectId, 16) * 10) + i)).upper().replace('X', 'x') + "\n"
			i += 1
		File.WriteAllText(gfxChangeExe.Directory.FullName + '/traces.txt', traceString)
		# Run gfxchange.exe and tracechange.exe
		Directory.SetCurrentDirectory(gfxChangeExe.Directory.FullName)
		writeLog("Running " + gfxChangeExe.FullName)
		p = Process.Start(gfxChangeExe.FullName, 'moveset.dat ' + str("%x" % (int(oldEffectId, 16) + 311)).upper() + ' ' + str("%x" % (int(newEffectId, 16) + 311)).upper())
		p.WaitForExit()
		p.Dispose()
		writeLog("Running " + gfxChangeExe.Directory.FullName + '/tracechange.exe')
		p = Process.Start(gfxChangeExe.Directory.FullName + '/tracechange.exe', 'moveset_gfxported.dat traces.txt')
		p.WaitForExit()
		p.Dispose()
		Directory.SetCurrentDirectory(AppPath)
		writeLog("Importing modified moveset file")
		moveset.Replace(gfxChangeExe.Directory.FullName + '/moveset_gfxported_traceconverted.dat')
		# Save and close file
		BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()
		writeLog("Effect ID update finished")
					

# Soundbank IDs are between 331 and 586, or 14B and 24A in hex
# Update soundbank to use new ID
def updateSoundbankId(fighterFile, sawndReplacerExe, sfxChangeExe, oldSoundbankId, newSoundBankId, addSeven="true"):
		writeLog("Updating soundbank for " + fighterFile.FullName + " to change soundbank ID " + str(oldSoundbankId) + " to " + str(newSoundBankId))
		Directory.SetCurrentDirectory(sawndReplacerExe.Directory.FullName)
		# Set up should go like this: Are your sound bank IDs usually in hex? (If no) Do you usually need to add 7 when naming your soundbanks?
		# Or something like that, basically we should support hex, decimal, and decimal + 7 formats. So in some cases, this may not actually add + 7
		# Actually probably just ask hex/dec and then +7/not +7 for best experience
		modifier = 7 if addSeven == "true" else 0
		writeLog("Running " + sawndReplacerExe.FullName)
		p = Process.Start(sawndReplacerExe.FullName, 'extoex ' + str(hex(int(oldSoundbankId, 16) + modifier)) + ' ' + str(hex(int(newSoundBankId, 16) + modifier)) + ' "' + sfxChangeExe.Directory.FullName + '/sound.txt"')
		p.WaitForExit()
		p.Dispose()
		Directory.SetCurrentDirectory(AppPath)
		writeLog("Exporting moveset file")
		BrawlAPI.OpenFile(fighterFile.FullName)
		moveset = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
		moveset.Export(sfxChangeExe.Directory.FullName + '/moveset.dat')
		Directory.SetCurrentDirectory(sfxChangeExe.Directory.FullName)
		writeLog("Running " + sfxChangeExe.FullName)
		p = Process.Start(sfxChangeExe.FullName, 'moveset.dat ' + 'sound.txt')
		p.WaitForExit()
		p.Dispose
		Directory.SetCurrentDirectory(AppPath)
		writeLog("Importing modified moveset file")
		moveset.Replace(sfxChangeExe.Directory.FullName + '/moveset_sfxconverted.dat')
		BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()
		writeLog("Soundbank ID update finished.")

# Move soundbank to build
# Before P+, soundbanks would be named in decimal + 7. So soundbank 1CB would be 459 + 7 = 466
def moveSoundbank(file, newSoundBankId=""):
		writeLog("Moving soundbank " + file.FullName + " with new soundbank ID of " + str(newSoundBankId))
		if newSoundBankId == "":
			fileName = file.Name
		else:
			fileName = newSoundBankId.upper() + '.sawnd'
		path = MainForm.BuildPath + '/pf/sfx/' + fileName
		# If the soundbank already exists, back it up
		createBackup(path)
		File.Copy(file.FullName, path, 1)
		writeLog("Soundbank move finished.")

# Add character to CSSRoster.dat
def addToRoster(fighterId):
		writeLog("Adding fighter ID " + str(fighterId) + " to CSSRoster.dat")
		changesMade = False
		fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/CSSRoster.dat')
		if fileOpened:
			# Add character to character select
			folder = getChildByName(BrawlAPI.RootNode, "Character Select")
			existingNode = getChildByFighterID(folder, fighterId)
			if existingNode == 0:
				newNode = RSTCEntryNode()
				newNode.FighterID = int(fighterId, 16)
				folder.AddChild(newNode)
				changesMade = True
			# Add character to random select
			folder = getChildByName(BrawlAPI.RootNode, "Random Character List")
			existingNode = getChildByFighterID(folder, fighterId)
			if existingNode == 0:
				newNode = RSTCEntryNode()
				newNode.FighterID = int(fighterId, 16)
				folder.AddChild(newNode)
				changesMade = True
		writeLog("Finished adding to CSSRoster.dat")
		return changesMade

# Add Kirby hat fixes
# Check kirby soundbanks here: http://opensa.dantarion.com/wiki/Soundbanks_(Brawl)
def addKirbyHat(characterName, fighterId, kirbyHatFigherId, kirbyHatExe):
		writeLog("Adding Kirby hat to fighter ID " + str(fighterId) + " using Kirby hat fighter ID " + str(kirbyHatFigherId))
		kirbyHatPath = getFileInfo(kirbyHatExe).DirectoryName
		# Start back up all kirby files
		createBackup(kirbyHatPath + '/codeset.txt')
		createBackup(kirbyHatPath + '/EX_KirbyHats.txt')
		createBackup(MainForm.BuildPath + '/pf/BrawlEx/KirbyHat.kbx')
		createBackup(MainForm.BuildPath + '/pf/module/ft_kirby.rel')
		createBackup(MainForm.BuildPath + '/Source/Extras/KirbyHatEX.asm')
		createBackup(MainForm.BuildPath + '/BOOST.GCT')
		createBackup(MainForm.BuildPath + '/NETBOOST.GCT')
		createBackup(MainForm.BuildPath + '/RSBE01.GCT')
		createBackup(MainForm.BuildPath + '/NETPLAY.GCT')
		#End back up kirby files
		Directory.SetCurrentDirectory(kirbyHatPath)
		writeLog("Reading EX_KirbyHats.txt")
		fileText = File.ReadAllLines(kirbyHatPath + '/EX_KirbyHats.txt')
		matchFound = False
		i = 0
		# Search for a matching fighter ID and if one is found, replace the line
		while i < len(fileText):
			line = fileText[i]
			if line.StartsWith('/') or line.StartsWith('#') or len(line) == 0:
				i += 1
				continue
			# Get the figher ID out of the line
			foundId = line.split(' = ')[1].split(' : ')[0]
			if foundId == '0x' + str(fighterId) or foundId == int(fighterId, 16):
				matchFound = True
				fileText[i] = '"' + characterName + '" = 0x' + fighterId + ' : 0x' + kirbyHatFigherId
			i += 1
		# Write updated file
		writeLog("Writing to EX_KirbyHats.txt")
		if matchFound:
			File.WriteAllLines(kirbyHatPath + '/EX_KirbyHats.txt', fileText)
		else:
			File.AppendAllText(kirbyHatPath + '/EX_KirbyHats.txt', '\n"' + characterName + '" = 0x' + fighterId + ' : 0x' + kirbyHatFigherId)
		# Run exe
		writeLog("Running " + kirbyHatExe)
		p = Process.Start(kirbyHatExe, '1 1 1 0 1')
		p.WaitForExit()
		p.Dispose()
		Directory.SetCurrentDirectory(AppPath)
		writeLog("Add Kirby hat finished.")

# Move Kirby hat files
def moveKirbyHatFiles(files, oldFighterName="", newFighterName=""):
		writeLog("Moving Kirby hat files, oldFighterName=" + oldFighterName + " newFighterName=" + newFighterName)
		for file in files:
			# TODO: rename files based on fighter name?
			file = getFileInfo(file)
			if oldFighterName != "" and newFighterName != "":
				path = MainForm.BuildPath + '/pf/fighter/kirby/' + file.Name.replace(oldFighterName, newFighterName)
			else:
				path = MainForm.BuildPath + '/pf/fighter/kirby/' + file.Name
			getFileInfo(path).Directory.Create()
			# Back up if it exists already
			createBackup(path)
			File.Copy(file.FullName, path, 1)
		writeLog("Move Kirby hat files finished.")

# Add song to tracklist
def addSong(file, songDirectory="Victory!", tracklist="Results"):
		writeLog("Adding victory theme file " + file)
		# Move to strm directory
		file = getFileInfo(file)
		path = MainForm.BuildPath + '/pf/sound/strm/' + songDirectory + '/' + file.Name
		# Back up file if it already exists
		createBackup(path)
		getFileInfo(path).Directory.Create()
		File.Copy(file.FullName, path, 1)
		writeLog("Opening Results.tlst")
		BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist + '.tlst')
		# Back up tracklist
		createBackup(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist + '.tlst')
		# Check if song is already installed
		writeLog("Checking if song already exists")
		for song in BrawlAPI.RootNode.Children:
			if song.SongFileName == songDirectory + '/' + file.Name.split('.')[0]:
				BrawlAPI.ForceCloseFile()
				return song.SongID
		# Calculate song ID
		writeLog("Calculating song ID")
		usedSongIds = getUsedSongIds(BrawlAPI.RootNode)
		currentSongId = 61440
		while currentSongId in usedSongIds:
			currentSongId += 1
		# Add to tracklist file
		writeLog("Adding song ID " + str(currentSongId) + " to" + tracklist + ".tlst")
		newNode = TLSTEntryNode()
		newNode.Name = file.Name.split('.')[0]
		newNode.SongFileName = songDirectory + '/' + file.Name.split('.')[0]
		newNode.Volume = 80
		newNode.Frequency = 40
		newNode.SongID = currentSongId
		BrawlAPI.RootNode.AddChild(newNode)
		BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()
		writeLog("Finished adding victory theme.")
		return currentSongId

# Add fighter to code menu
def addToCodeMenu(fighterName, fighterId, assemblyFunctionExe):
		writeLog("Adding fighter ID " + str(fighterId) + " to code menu")
		assemblyFunctionsPath = getFileInfo(assemblyFunctionExe).DirectoryName
		# Start back up
		createBackup(assemblyFunctionsPath + '/EX_Characters.txt')
		createBackup(assemblyFunctionsPath + '/codeset.txt')
		createBackup(MainForm.BuildPath + '/Source/Project+/CodeMenu.asm')
		createBackup(MainForm.BuildPath + '/pf/menu3/data.cmnu')
		createBackup(MainForm.BuildPath + '/pf/menu3/dnet.cmnu')
		createBackup(MainForm.BuildPath + '/BOOST.GCT')
		createBackup(MainForm.BuildPath + '/NETBOOST.GCT')
		createBackup(MainForm.BuildPath + '/RSBE01.GCT')
		createBackup(MainForm.BuildPath + '/NETPLAY.GCT')
		# End back up
		Directory.SetCurrentDirectory(assemblyFunctionsPath)
		writeLog("Reading EX_Characters.txt")
		fileText = File.ReadAllLines(assemblyFunctionsPath + '/EX_Characters.txt')
		matchFound = False
		i = 0
		# Search for a matching fighter ID and if one is found, replace the line
		while i < len(fileText):
			line = fileText[i]
			if line.StartsWith('/') or line.StartsWith('#') or len(line) == 0:
				i += 1
				continue
			# Get the figher ID out of the line
			foundId = line.split(' = ')[1]
			if foundId == '0x' + str(fighterId) or foundId == int(fighterId, 16):
				matchFound = True
				fileText[i] = '"' + fighterName + '" = 0x' + fighterId
			i += 1
		# Write updated file
		writeLog("Writing updated EX_Characters.txt")
		if matchFound:
			File.WriteAllLines(assemblyFunctionsPath + '/EX_Characters.txt', fileText)
		else:
			File.AppendAllText(assemblyFunctionsPath + '/EX_Characters.txt', '\n"' + fighterName + '" = 0x' + fighterId)
		writeLog("Running " + assemblyFunctionExe)
		p = Process.Start(assemblyFunctionExe, '1 1 0 1')
		p.WaitForExit()
		p.Dispose()
		Directory.SetCurrentDirectory(AppPath)
		writeLog("Add to code menu finished.")

# Function to build GCTs using GCTRealMate
def buildGct():
		writeLog("Building GCT files")
		createBackup(MainForm.BuildPath + '/BOOST.GCT')
		createBackup(MainForm.BuildPath + '/NETBOOST.GCT')
		createBackup(MainForm.BuildPath + '/RSBE01.GCT')
		createBackup(MainForm.BuildPath + '/NETPLAY.GCT')
		if File.Exists(MainForm.BuildPath + '/GCTRealMate.exe'):
			writeLog("Running GCTRealMate.exe")
			boost = ' "' + MainForm.BuildPath + '\\BOOST.txt" ' if File.Exists(MainForm.BuildPath + '\\BOOST.txt') else ""
			rsbe = ' "' + MainForm.BuildPath + '\\RSBE01.txt" ' if File.Exists(MainForm.BuildPath + '\\RSBE01.txt') else ""
			netboost = ' "' + MainForm.BuildPath + '\\NETBOOST.txt" ' if File.Exists(MainForm.BuildPath + '\\NETBOOST.txt') else ""
			netplay = ' "' + MainForm.BuildPath + '\\NETPLAY.txt" ' if File.Exists(MainForm.BuildPath + '\\NETPLAY.txt') else ""
			Directory.SetCurrentDirectory(MainForm.BuildPath)
			p = Process.Start(MainForm.BuildPath + '\\GCTRealMate.exe', '-g -l -q' + boost + rsbe + netboost + netplay)
			p.WaitForExit()
			p.Dispose()
			Directory.SetCurrentDirectory(AppPath)
			writeLog("Finished running GCTRealMate.exe")
		writeLog("Finished building GCT files")

# Helper function to generate a value string for code macros
def getValueString(values, copiedValue=""):
		# Get string out of values
		valueText = ""
		if "(" in copiedValue:
			copiedValue = copiedValue.split('(')[1]
		if ")" in copiedValue:
			copiedValue = copiedValue.split(')')[0]
		for value in values:
			if value == "copy":
				value = copiedValue
			if valueText == "":
				valueText = valueText + str(value)
			else:
				valueText = valueText + ", " + str(value)
		return valueText

# Function to add a code macro to the appropriate code
def addCodeMacro(fighterName, id, macroName, values, position=0, repeat=False, preFindText=""):
		writeLog("Adding ID " + str(id) + " " + macroName + " entry")
		if File.Exists(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm'):
			createBackup(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm')
			# Read CloneEngine.asm
			writeLog("Reading CloneEngine.asm")
			fileText = File.ReadAllLines(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm')
			matchFound = False
			foundMacros = False
			endMacroSearch = False
			insertLines = []
			copiedValue = ""
			foundPreText = False
			i = 0
			# Search for a matching ID and if one is found, replace the line
			newText = []
			writeLog("Searching for macro entry")
			while i < len(fileText):
				line = fileText[i]
				if preFindText != "" and line.strip() == preFindText:
					foundPreText = True
				# Get the fighter ID out of the line
				if str(line).strip().StartsWith('%' + macroName) and ((not preFindText) or foundPreText):
					writeLog("Found macro entries")
					foundMacros = True
					foundId = line.split(',')[position]
					# If it's a matching entry, replace it
					if '0x' + str(id) in foundId:
						writeLog("Found matching entry")
						matchFound = True
						# Get string out of values - here, copied value is just whatever it was originally, since we are overwriting an existing entry
						if "copy" in values:
							copiedValue = fileText[i].split(',')[values.index("copy")]
						valueText = getValueString(values, copiedValue)
						newText.append('\t%' + macroName + '(' + valueText + ')\t#' + fighterName)
					else:
						newText.append(line)
					i += 1
					continue
				# If we reach the end of the macro entries with no match found, set to add one
				elif foundMacros and not endMacroSearch and not matchFound and not str(line).strip().StartsWith('%' + macroName) and ((not preFindText) or foundPreText):
					writeLog("Matching entry not found, will insert new entry")
					insertLines.append(i + len(insertLines))
					if not repeat:
						endMacroSearch = True
					else:
						matchFound = False
						foundMacros = False
						endMacroSearch = False
					newText.append(line)
					i += 1
					continue
				else:
					newText.append(line)
					i += 1
					continue
			# If we didn't find a match, add the line at the position after the last macro
			for insertLine in insertLines:
				writeLog("Inserting new entry")
				# Get string out of values - here, copied value is whatever is one line above
				if "copy" in values:
					copiedValue = newText[insertLine - 1].split(',')[values.index("copy")]
				valueText = getValueString(values, copiedValue)
				newText.insert(insertLine, '\t%' + macroName + '(' + valueText + ')\t#' + fighterName)
			writeLog("Writing updates to macro")
			File.WriteAllLines(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm', newText)
			writeLog("Added macro entry")
		writeLog("Macro entry add finished")

# Update an entry of the throw release point code
def updateThrowRelease(fighterId, fighterName, values):
		writeLog("Updating throw release point for ID " + str(fighterId))
		if File.Exists(MainForm.BuildPath + "/Source/ProjectM/Modifier/ThrowRelease.asm"):
			createBackup(MainForm.BuildPath + "/Source/ProjectM/Modifier/ThrowRelease.asm")
			# Read ThrowRelease.asm
			writeLog("Reading ThrowRelease.asm")
			fileText = File.ReadAllLines(MainForm.BuildPath + "/Source/ProjectM/Modifier/ThrowRelease.asm")
			i = 0
			tableStart = 0
			endComma = "," if fighterId.upper() != "7F" else ""
			while i < len(fileText):
				line = fileText[i]
				if line.StartsWith("ThrowReleaseTable"):
					writeLog("Found throw release table at line " + str(i))
					tableStart = i + 2
				if tableStart > 0 and i == tableStart + int(fighterId, 16):
					writeLog("Found matching EX fighter at position " + str(i))
					fileText[i] = "\t" + values[0] + ",\t\t" + values[1] + endComma + "\t| # " + fighterName
				i += 1
			writeLog("Writing to ThrowRelease.asm")
			File.WriteAllLines(MainForm.BuildPath + "/Source/ProjectM/Modifier/ThrowRelease.asm", fileText)
		writeLog("Finished updating throw release point")

# Import ending .pac files
def importEndingFiles(files, endingId):
		writeLog("Importing ending .pac files")
		for file in files:
			createBackup(MainForm.BuildPath + getFileInfo(file).Name)
			fileOpened = BrawlAPI.OpenFile(file)
			fileName = ""
			texturePrefix = ""
			if fileOpened:
				if BrawlAPI.RootNode.Name.startswith('EndingSimple'):
					fileName = 'EndingSimple' + addLeadingZeros(str(endingId), 2)
					writeLog("Renaming root node to " + fileName)
					BrawlAPI.RootNode.Name = fileName
					texturePrefix = "S"
				elif BrawlAPI.RootNode.Name.startswith('EndingAll'):
					fileName = 'EndingAll' + addLeadingZeros(str(endingId), 2)
					writeLog("Renaming root node to " + fileName)
					BrawlAPI.RootNode.Name = fileName
					texturePrefix = "A"
				node = getChildByName(BrawlAPI.RootNode, 'Model Data [4]')
				if node:
					texFolder = getChildByName(node, 'Textures(NW4R)')
					if texFolder:
						texNodes = getChildrenByPrefix(texFolder, 'MenEndpictures' + texturePrefix)
						if texNodes:
							texNode = texNodes[0]
							writeLog('Renaming TEX0 node to ' + 'MenEndpictures' + texturePrefix + addLeadingZeros(str(endingId), 4))
							texNode.Name = 'MenEndpictures' + texturePrefix + addLeadingZeros(str(endingId), 4)
			BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/menu/intro/ending/' + fileName + '.pac')
		writeLog("Finished importing ending files")

# Import ending movie file
def importEndingMovie(file, fighterName):
		writeLog("Importing ending movie file")
		createBackup(MainForm.BuildPath + getFileInfo(file).Name)
		copyRenameFile(file, 'End_' + fighterName + '.thp', MainForm.BuildPath + '/pf/movie')
		writeLog("Finished importing movie file")

# Update an entry of the ending code
def updateEndingCode(cosmeticConfigId, remove=False, read=False):
		if not read:
			writeLog("Updating ending code for ID " + str(cosmeticConfigId))
		else:
			writeLog("Reading ending code for ID " + str(cosmeticConfigId))
		if File.Exists(MainForm.BuildPath + "/Source/ProjectM/CloneEngine.asm"):
			if not read:
				createBackup(MainForm.BuildPath + "/Source/ProjectM/CloneEngine.asm")
			# Read CloneEngine.asm
			writeLog("Reading CloneEngine.asm")
			fileText = File.ReadAllLines(MainForm.BuildPath + "/Source/ProjectM/CloneEngine.asm")
			i = 0
			valueList = []
			tableStart = 0
			tableEndReached = False
			# Get all of the ending ID things
			while i < len(fileText):
				line = fileText[i]
				if line.StartsWith("ENDINGTABLE:"):
					writeLog("Found ending table at line " + str(i))
					tableStart = i + 2
				if tableStart and i >= tableStart and not tableEndReached:
					values = line.split(',')
					for value in values:
						# Don't count comment lines
						if not value.strip().startswith('|'):
							valueList.append(value.replace('|','').strip())
				if tableStart and i >= tableStart and (len(line) == 0 or line.startswith('#')):
					tableEndReached = True
				i += 1
			# Find the first unused value
			if not remove and not read:
				j = 1
				i = 0
				while i < len(valueList):
					if valueList[i] == str(j):
						j += 1
						i = 0
					else:
						i += 1
				writeLog("Unused ending value " + str(j))
			else:
				j = -1
				writeLog("Setting ending value to -1")
			# Loop again, but this time we are just looking for the position to replace
			i = tableStart
			tableEndReached = False
			# Count starts at -1 because the numbers are zero-indexed
			lineCounter = -1
			notWritten = True
			foundId = ""
			writeLog("Finding position to write")
			while i < len(fileText):
				line = fileText[i]
				splitLine = list(filter(None, line.split('|')[0].strip().split(',')))
				lineCounter = lineCounter + len(splitLine)
				if notWritten and not tableEndReached and lineCounter >= int(cosmeticConfigId, 16):
					writeLog("Found write location on line " + str(i))
					newLine = splitLine
					# Have to subtract 1 because of zero-indexing
					writeLog("Line counter is " + str(lineCounter) + " cosmetic conf ID is " + str(int(cosmeticConfigId, 16)))
					foundId = newLine[(len(newLine) - (lineCounter - int(cosmeticConfigId, 16))) - 1]
					writeLog("Found ID " + foundId)
					if not read:
						newLine[(len(newLine) - (lineCounter - int(cosmeticConfigId, 16))) - 1] = str(j)
						newString = "\t\t"
						for part in newLine:
							newString = newString + part.strip() + (', ' if len(fileText[i + 1]) != 0 else '')
						newString = newString + '|' + fileText[i].split('|')[1]
						fileText[i] = newString
					notWritten = False
				if tableStart and i >= tableStart and (len(line) == 0 or line.startswith('#')):
					tableEndReached = True
				i += 1
			if not read:
				File.WriteAllLines(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm', fileText)
			if not remove and not read:
				returnId = str(j)
			else:
				returnId = foundId.strip()
			if not read:
				writeLog("Finished updating ending code")
			else:
				writeLog("Finished reading ending code")
			return returnId

# Update an entry of the credits music code
def updateCreditsCode(slotId, songId, remove=False, read=False):
		if not read:
			writeLog("Updating credits code for ID " + str(slotId))
		else:
			writeLog("Reading credits code for ID " + str(slotId))
		if File.Exists(MainForm.BuildPath + "/Source/Project+/ResultsMusic.asm"):
			if not read:
				createBackup(MainForm.BuildPath + "/Source/Project+/ResultsMusic.asm")
			# Read ResultsMusic.asm
			writeLog("Reading ResultsMusic.asm")
			fileText = File.ReadAllLines(MainForm.BuildPath + "/Source/Project+/ResultsMusic.asm")
			i = 0
			tableStart = 0
			tableEndReached = False
			# Find the credits table
			while i < len(fileText):
				line = fileText[i]
				if line.StartsWith("ClassicResultsTable:"):
					writeLog("Found credits table at line " + str(i))
					tableStart = i + 2
					break
				i += 1
			# Search for the position to replace
			i = tableStart
			tableEndReached = False
			# Count starts at -1 because the numbers are zero-indexed
			lineCounter = -1
			notWritten = True
			foundId = ""
			if remove:
				songId = "0x0000"
			writeLog("Finding position to write")
			while i < len(fileText):
				line = fileText[i]
				splitLine = list(filter(None, line.split('|')[0].strip().split(',')))
				lineCounter = lineCounter + len(splitLine)
				if notWritten and not tableEndReached and lineCounter >= int(slotId, 16):
					writeLog("Found write location on line " + str(i))
					newLine = splitLine
					# Have to subtract 1 because of zero-indexing
					foundId = newLine[(len(newLine) - (lineCounter - int(slotId, 16))) - 1]
					if not read:
						newLine[(len(newLine) - (lineCounter - int(slotId, 16))) - 1] = str(songId)
						newString = "\t\t"
						for part in newLine:
							newString = newString + part.strip() + (', ' if len(fileText[i + 1]) != 0 else '')
						newString = newString + '|' + fileText[i].split('|')[1]
						fileText[i] = newString
					notWritten = False
				if tableStart and i >= tableStart and (len(line) == 0 or line.startswith('#')):
					tableEndReached = True
				i += 1
			if not read:
				File.WriteAllLines(MainForm.BuildPath + '/Source/Project+/ResultsMusic.asm', fileText)
			if not remove and not read:
				returnId = str(songId)
			else:
				returnId = foundId.strip()
			if not read:
				writeLog("Finished updating credits code")
			else:
				writeLog("Finished reading credits code")
			return returnId
					
#endregion IMPORT FUNCTIONS

#region REMOVE FUNCTIONS
# Functions used by the BrawlInstaller suite to remove elements

# Remove imported CSPs and RSPs for specified cosmetic ID
def removeCSPs(cosmeticId):
		writeLog("Removing CSPs for cosmetic ID " + str(cosmeticId))
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			# Find char_bust_tex_lz77
			arcNode = getChildByName(BrawlAPI.RootNode, "char_bust_tex_lz77")
			# Get CSP brres and remove if it exists
			nodeToRemove = getChildByName(arcNode, "Misc Data [" + str(cosmeticId) + "]")
			if nodeToRemove:
				nodeToRemove.Remove()
		# Get RSP file and delete if it exists
		writeLog("Get RSP file for cosmetic ID")
		rspFile = getFileByName("MenSelchrFaceB" + addLeadingZeros(str(cosmeticId), 2) + "0.brres", Directory.CreateDirectory(MainForm.BuildPath + '/pf/menu/common/char_bust_tex'))
		if rspFile:
			# Back up first
			createBackup(rspFile.FullName)
			writeLog("Deleting RSP file " + rspFile.FullName)
			rspFile.Delete()

# Delete BPs for specified cosmetic ID
def deleteBPs(cosmeticId, fiftyCC="true"):
		writeLog("Deleting BPs for cosmetic ID " + str(cosmeticId))
		# For 50 costume code, we must multiply the cosmetic ID by 50
		newId = (cosmeticId * 50) + 1 if fiftyCC == "true" else int(str(cosmeticId) + "1")
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/info/portrite')
		# Look for files matching naming scheme and delete them
		while newId <= (cosmeticId * 50) + 50:
			bpFile = getFileByName("InfFace" + addLeadingZeros(str(newId), 4 if fiftyCC == "true" else 3) + ".brres", directory)
			if bpFile:
				# Back it up first
				createBackup(bpFile.FullName)
				writeLog("Deleting BP file " + bpFile.FullName)
				bpFile.Delete()
			else:
				# If no matching file exists, just exit
				break
			newId += 1

# Remove CSS icon
def removeCSSIcon(cosmeticId):
		writeLog("Removing CSS icon for cosmetic ID " + str(cosmeticId))
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			# Remove icon texture
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [70]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			nodeName = "MenSelchrChrFace." + addLeadingZeros(str(cosmeticId), 3)
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				# Pass in bool to force remove palette
				textureNode.Remove(True)
			# Remove CSS icon from CSS
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			anmTexPat = getChildByName(node, "AnmTexPat(NW4R)")
			pat0Nodes = getChildrenByPrefix(anmTexPat, "MenSelchrFace")
			for pat0Node in pat0Nodes:
				removeFromPat0(node, pat0Node.Name, "Face02", nodeName, frameCountOffset=10)
		writeLog("Remove CSS icon finished")

# Remove replay icon
def removeReplayIcon(cosmeticId):
		writeLog("Remove replay icon for cosmetic ID " + str(cosmeticId))
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu/collection/Replay.brres')
		if fileOpened:
			texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
			nodeName = "MenReplayChr." + addLeadingZeros(str(cosmeticId) + "1", 3)
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				textureNode.Remove(True)
			# Remove from pat0
			anmTexPat = getChildByName(BrawlAPI.RootNode, "AnmTexPat(NW4R)")
			pat0Node = getChildByName(anmTexPat, "MenReplayPreview2_TopN__0")
			removeFromPat0(BrawlAPI.RootNode, pat0Node.Name, "lambert78", nodeName, frameCountOffset=10)
		writeLog("Remove replay icon finished")

# Remove CSS icon name
def removeCSSIconName(cosmeticId):
		writeLog("Remove CSS icon name for cosmetic ID " + str(cosmeticId))
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			# Remove icon name texture
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [70]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			nodeName = "MenSelchrChrNmS." + addLeadingZeros(str(cosmeticId), 3)
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				# Pass in bool to force remove palette
				textureNode.Remove(True)
			# Remove CSS icon name from CSS
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			anmTexPat = getChildByName(node, "AnmTexPat(NW4R)")
			pat0Nodes = getChildrenByPrefix(anmTexPat, "MenSelchrFace")
			for pat0Node in pat0Nodes:
				removeFromPat0(node, pat0Node.Name, "Face06", nodeName, frameCountOffset=10)
		writeLog("Remove CSS icon name finished")

# Remove portrait name
def removePortraitName(cosmeticId):
		writeLog("Remove portrait name for cosmetic ID " + str(cosmeticId))
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			# Remove name
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			nodeName = "MenSelchrChrNm." + addLeadingZeros(str(cosmeticId), 3) + '1'
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				textureNode.Remove(True)
			removeFromPat0(node, "MenSelchrCname4_TopN__0", "Card010", nodeName, frameCountOffset=10, overrideFrameCount=2561)
			removeFromPat0(node, "MenSelchrCname4_TopN__0", "Card011", nodeName, frameCountOffset=10, overrideFrameCount=2561)
		writeLog("Remove portrait name finished")

# Remove franchise icon from CSS or info
def removeFranchiseIcon(franchiseIconId, filePath):
		writeLog("Remove franchise icon ID " + str(franchiseIconId) + " at filepath " + filePath)
		fileNodeName = filePath.split('.')[0].split('/')[-1]
		fileOpened = openFile(MainForm.BuildPath + filePath)
		if fileOpened:
			# Remove icon
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			nodeName = "MenSelchrMark." + addLeadingZeros(str(franchiseIconId), 2)
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				textureNode.Remove(True)
			if fileNodeName == "sc_selcharacter":
				pat0texNodeName = "Card04"
				pat0NodeName = "MenSelchrCmark4_TopN__0"
			if fileNodeName.startswith("info"):
				pat0texNodeName = "lambert110"
				pat0NodeName = "InfMark_TopN__0"
			removeFromPat0(node, pat0NodeName, pat0texNodeName, nodeName, frameCountOffset=1)
		writeLog("Remove franchise icon finished")

# Remove BP name from info
def removeBPName(cosmeticId, filePath):
		writeLog("Removing BP name with cosmetic ID " + str(cosmeticId) + " at " + filePath)
		fileOpened = openFile(MainForm.BuildPath + filePath)
		if fileOpened:
			# Remove BP name
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			nodeName = "MenSelchrChrNmS."+ addLeadingZeros(str(cosmeticId) + '1', 3)
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				textureNode.Remove(True)
			pat0texNodeName = "Character_Name_Mat"
			pat0NodeName = "InfFace_TopN__0"
			removeFromPat0(node, pat0NodeName, pat0texNodeName, nodeName, frameCountOffset=10)
		writeLog("Remove BP name finished")

# Delete classic intro file
def deleteClassicIntro(cosmeticId):
		writeLog("Deleting classic intro file for cosmetic ID " + str(cosmeticId + 1))
		filePath = MainForm.BuildPath + '/pf/menu/intro/enter/chr' + addLeadingZeros(str(cosmeticId + 1), 4) + '.brres'
		if File.Exists(filePath):
			createBackup(filePath)
			File.Delete(filePath)
		writeLog("Finished deleting classic intro file")

# Remove franchise icon from result screen
def removeFranchiseIconResult(franchiseIconId):
		writeLog("Remove franchise icon ID " + str(franchiseIconId) + " from STGRESULT.pac")
		fileOpened = openFile(MainForm.BuildPath + '/pf/stage/melee/STGRESULT.pac')
		if fileOpened:
			# Remove icon
			node = getChildByName(getChildByName(BrawlAPI.RootNode, "2"), "Misc Data [110]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			textureNode = getChildByName(texFolder, "MenSelchrMark." + addLeadingZeros(str(franchiseIconId), 2))
			if textureNode:
				textureNode.Remove(True)
			# Remove 3D model
			modelFolder = getChildByName(node, "3DModels(NW4R)")
			mdl0Node = getChildByName(modelFolder, "InfResultMark" + addLeadingZeros(str(franchiseIconId), 2) + "_TopN")
			if mdl0Node:
				mdl0Node.Remove()
			# Remove color sequence
			colorFolder = getChildByName(node, "AnmClr(NW4R)")
			clr0Node = getChildByName(colorFolder, "InfResultMark" + addLeadingZeros(str(franchiseIconId), 2) + "_TopN")
			if clr0Node:
				clr0Node.Remove()
		writeLog("Remove franchise icon ID finished")

# Remove stock icons
def removeStockIcons(cosmeticId, tex0BresName, pat0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true"):
		writeLog("Remove stock icons for cosmetic ID " + str(cosmeticId) + " at filepath " + filePath)
		# If info.pac is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + filePath)
		if fileOpened:
			rootNode = BrawlAPI.RootNode
			if rootName != "":
				rootNode = getChildByName(BrawlAPI.RootNode, rootName)
			if tex0BresName != "":
				node = getChildByName(rootNode, tex0BresName)
			else:
				node = rootNode
			# Remove the texture nodes
			texFolder = getChildByName(node, "Textures(NW4R)")
			# End of loop changes depending on if we use 50 CC or not
			newId = (cosmeticId * 50) + 1 if fiftyCC == "true" else int(str(cosmeticId) + "1")
			texNodeNames = []
			cap = ((cosmeticId * 50) + 50) if fiftyCC == "true" else int(str(cosmeticId) + "0") + 10
			while newId <= cap:
				texNode = getChildByName(texFolder, "InfStc." + addLeadingZeros(str(newId), 4 if fiftyCC == "true" else 3))
				if texNode:
					texNodeNames.append(texNode.Name)
					texNode.Remove(True)
				else:
					break
				newId += 1
			if pat0BresName == "":
				return
			pat0BresNode = getChildByName(rootNode, pat0BresName)
			anmTexPat = getChildByName(pat0BresNode, "AnmTexPat(NW4R)")
			if (BrawlAPI.RootNode.Name.StartsWith("sc_selmap")):
				pat0Nodes = [ getChildByName(anmTexPat, "MenSelmapPlayer1_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer2_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer3_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer4_TopN") ]
			else:
				pat0Nodes = [ getChildByName(anmTexPat, "InfStockface_TopN__0") ]
			for pat0Node in pat0Nodes:
				# For each texture we added, add a pat0 entry
				for texNodeName in texNodeNames:
					# Frame count is 9201 with 50 CC, 501 without, and it's 9301 or 601 on sc_selmap
					frameCount = 9201 if fiftyCC == "true" else 501
					if BrawlAPI.RootNode.Name.StartsWith("sc_selmap"):
						frameCount += 100
					removeFromPat0(pat0BresNode, pat0Node.Name, pat0Node.Children[0].Name, texNodeName, frameCountOffset=1, overrideFrameCount=frameCount)
		writeLog("Remove stock icons finished")

# Delete module for specified fighter
def deleteModule(internalName):
		writeLog("Deleting module for fighter name " + internalName)
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/module')
		moduleFile = getFileByName("ft_" + internalName.lower() + ".rel", directory)
		if moduleFile:
			createBackup(moduleFile.FullName)
			moduleFile.Delete()
		writeLog("Delete module complete")

# Delete fighter files for specified fighter
def deleteFighterFiles(internalName):
		writeLog("Deleting fighter files for fighter name " + internalName)
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/fighter')
		fighterDirectory = Directory.GetDirectories(directory.FullName, internalName.lower())
		if fighterDirectory:
			# First back everything up
			for file in Directory.GetFiles(fighterDirectory[0]):
				createBackup(file)
			Directory.Delete(fighterDirectory[0], True)
		writeLog("Delete fighter files complete")

# Delete kirby hat files for specified fighter
def deleteKirbyHatFiles(internalName):
		writeLog("Deleting Kirby hat files for fighter name " + internalName)
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/fighter/kirby')
		kirbyHatFiles = Directory.GetFiles(directory.FullName, "FitKirby" + internalName + "*.pac")
		if kirbyHatFiles:
			i = 0
			while i < len(kirbyHatFiles):
				# Back up file first
				createBackup(kirbyHatFiles[i])
				getFileInfo(kirbyHatFiles[i]).Delete()
				i += 1
		writeLog("Delete Kirby hat files complete")

# Delete the specified soundbank
def deleteSoundbank(soundBankId):
		writeLog("Deleting soundbank ID " + str(soundBankId))
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/sfx')
		soundBank = getFileByName(str(soundBankId).upper() + ".sawnd", directory)
		if soundBank:
			createBackup(soundBank.FullName)
			soundBank.Delete()
		writeLog("Deleting soundbank ID complete")

# Delete EX configs for specified fighter ID
def deleteExConfigs(fighterId, slotConfigId = "", cosmeticConfigId = "", cssSlotConfigId = ""):
		writeLog("Deleting Ex Configs for fighter ID " + fighterId)
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/BrawlEx')
		for folder in Directory.GetDirectories(directory.FullName):
			writeLog("Getting config from " + folder)
			if DirectoryInfo(folder).Name == "SlotConfig" and slotConfigId:
				writeLog("Slot ID " + str(slotConfigId))
				id = slotConfigId
			elif DirectoryInfo(folder).Name == "CosmeticConfig" and cosmeticConfigId:
				writeLog("Cosmetic config ID " + str(cosmeticConfigId))
				id = cosmeticConfigId
			elif DirectoryInfo(folder).Name == "CSSSlotConfig" and cssSlotConfigId:
				writeLog("CSSSlot config ID " + str(cssSlotConfigId))
				id = cssSlotConfigId
			else:
				writeLog("Fighter ID " + str(fighterId))
				id = fighterId
			exConfig = getFileByName(DirectoryInfo(folder).Name.split("Config")[0] + str(id) + ".dat", DirectoryInfo(folder))
			if exConfig:
				createBackup(exConfig.FullName)
				writeLog("Deleting config " + exConfig.FullName)
				exConfig.Delete()
		writeLog("Finished deleting Ex Configs")

# Remove character from CSSRoster.dat
def removeFromRoster(fighterId):
		writeLog("Removing fighter ID " + str(fighterId) + " from CSSRoster.dat")
		fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/CSSRoster.dat')
		if fileOpened:
			# Remove character from character select
			folder = getChildByName(BrawlAPI.RootNode, "Character Select")
			if folder.Children:
				nodeToRemove = getChildByFighterID(folder, fighterId)
				if nodeToRemove:
					nodeToRemove.Remove()
			# Remove character from random select
			folder = getChildByName(BrawlAPI.RootNode, "Random Character List")
			if folder.Children:
				nodeToRemove = getChildByFighterID(folder, fighterId)
				if nodeToRemove:
					nodeToRemove.Remove()
		writeLog("Finished removing fighter from CSSRoster.dat")

# Remove character victory theme
def removeSong(songID, songDirectory='Victory!', tracklist='Results'):
		writeLog("Removing theme with song ID " + str(songID))
		BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist + '.tlst')
		# Back up tracklist file
		createBackup(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist + '.tlst')
		# Remove from tracklist file
		node = BrawlAPI.RootNode
		if node.Children:
			for child in node.Children:
				if child.SongID == songID:
					childNode = child
					break
		if 'childNode' in locals():
			# Get filename
			path = MainForm.BuildPath + '/pf/sound/strm/' + songDirectory
			directory = Directory.CreateDirectory(path)
			brstmFile = getFileByName(childNode.SongFileName.split('/')[1] + ".brstm", directory)
			# Back up song file
			createBackup(brstmFile.FullName)
			# Remove from tracklist
			if childNode:
				writeLog("Removing from" + tracklist + ".tlst")
				childNode.Remove()
			# Delete from directory
			if brstmFile:
				writeLog("Deleting file " + brstmFile.FullName)
				brstmFile.Delete()
		BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()
		writeLog("Finished removing theme")

# Remove kirby hat
def removeKirbyHat(fighterId, kirbyHatExe):
		writeLog("Removing Kirby hat for fighter ID " + str(fighterId))
		kirbyHatPath = getFileInfo(kirbyHatExe).DirectoryName
		# Start back up all kirby files
		createBackup(kirbyHatPath + '/codeset.txt')
		createBackup(kirbyHatPath + '/EX_KirbyHats.txt')
		createBackup(MainForm.BuildPath + '/pf/BrawlEx/KirbyHat.kbx')
		createBackup(MainForm.BuildPath + '/pf/module/ft_kirby.rel')
		createBackup(MainForm.BuildPath + '/Source/Extras/KirbyHatEX.asm')
		createBackup(MainForm.BuildPath + '/BOOST.GCT')
		createBackup(MainForm.BuildPath + '/NETBOOST.GCT')
		createBackup(MainForm.BuildPath + '/RSBE01.GCT')
		createBackup(MainForm.BuildPath + '/NETPLAY.GCT')
		#End back up kirby files
		writeLog("Reading EX_KirbyHats.txt")
		Directory.SetCurrentDirectory(kirbyHatPath)
		fileText = File.ReadAllLines(kirbyHatPath + '/EX_KirbyHats.txt')
		matchFound = False
		i = 0
		# Search for a matching fighter ID and if one is found, keep track of the index
		while i < len(fileText):
			line = fileText[i]
			if line.StartsWith('/') or line.StartsWith('#') or len(line) == 0:
				i += 1
				continue
			# Get the figher ID out of the line
			foundId = line.split(' = ')[1].split(' : ')[0]
			if foundId == '0x' + str(fighterId) or foundId == int(fighterId, 16):
				matchFound = True
				break
			i += 1
		# If there was a match, write the file while skipping that index
		if matchFound:
			newFileText = []
			j = 0
			while j < len(fileText):
				if j != i:
					newFileText.append(fileText[j])
				j += 1
			writeLog("Writing modified EX_KirbyHats.txt")
			File.WriteAllLines(kirbyHatPath + '/EX_KirbyHats.txt', Array[str](newFileText))
			# Run exe
			writeLog("Running " + kirbyHatExe)
			p = Process.Start(kirbyHatExe, '1 1 1 0 1')
			p.WaitForExit()
			p.Dispose()
		Directory.SetCurrentDirectory(AppPath)

# Remove fighter from code menu
def removeFromCodeMenu(fighterId, assemblyFunctionExe):
		writeLog("Removing fighter ID " + str(fighterId) + " from code menu")
		assemblyFunctionsPath = getFileInfo(assemblyFunctionExe).DirectoryName
		# Start back up
		createBackup(assemblyFunctionsPath + '/EX_Characters.txt')
		createBackup(assemblyFunctionsPath + '/codeset.txt')
		createBackup(MainForm.BuildPath + '/Source/Project+/CodeMenu.asm')
		createBackup(MainForm.BuildPath + '/pf/menu3/data.cmnu')
		createBackup(MainForm.BuildPath + '/pf/menu3/dnet.cmnu')
		createBackup(MainForm.BuildPath + '/BOOST.GCT')
		createBackup(MainForm.BuildPath + '/NETBOOST.GCT')
		createBackup(MainForm.BuildPath + '/RSBE01.GCT')
		createBackup(MainForm.BuildPath + '/NETPLAY.GCT')
		# End back up
		writeLog("Reading EX_Characters.txt")
		Directory.SetCurrentDirectory(assemblyFunctionsPath)
		fileText = File.ReadAllLines(assemblyFunctionsPath + '/EX_Characters.txt')
		matchFound = False
		i = 0
		# Search for a matching fighter ID and if one is found, replace the line
		while i < len(fileText):
			line = fileText[i]
			if line.StartsWith('/') or line.StartsWith('#') or len(line) == 0:
				i += 1
				continue
			# Get the figher ID out of the line
			foundId = line.split(' = ')[1]
			if foundId == '0x' + str(fighterId) or foundId == int(fighterId, 16):
				matchFound = True
				break
			i += 1
		# If there was a match, write the file while skipping that index
		if matchFound:
			newFileText = []
			j = 0
			while j < len(fileText):
				if j != i:
					newFileText.append(fileText[j])
				j += 1
			writeLog("Writing updated EX_Characters.txt")
			File.WriteAllLines(assemblyFunctionsPath + '/EX_Characters.txt', Array[str](newFileText))
			# Run the exe
			writeLog("Running " + assemblyFunctionExe)
			p = Process.Start(assemblyFunctionExe, '1 1 0 1')
			p.WaitForExit()
			p.Dispose()
		Directory.SetCurrentDirectory(AppPath)

# Function to remove a code macro from the appropriate code
def removeCodeMacro(id, macroName, position=0, repeat=False, preFindText=""):
		writeLog("Removing ID " + str(id) + " " + macroName + " entry")
		if File.Exists(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm'):
			createBackup(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm')
			# Read CloneEngine.asm
			writeLog("Reading CloneEngine.asm")
			fileText = File.ReadAllLines(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm')
			matchFound = False
			foundMacros = False
			foundPreText = False
			removeLines = []
			i = 0
			# Search for matching ID and if one is found, remove the line
			while i < len(fileText):
				line = fileText[i]
				if preFindText != "" and line.strip() == preFindText:
					foundPreText = True
				# Get the ID out of the entry
				if str(line).strip().StartsWith('%' + macroName) and ((not preFindText) or foundPreText):
					writeLog("Found macro entries")
					foundMacros = True
					foundId = line.split(',')[position]
					if '0x' + str(id) in foundId:
						writeLog("Found matching entry")
						matchFound = True
						removeLines.append(i)
						if not repeat:
							break
					i += 1
				# If we aren't repeating and we hit the end, just exit
				elif not repeat and foundMacros and not matchFound and not str(line).strip().StartsWith("%" + macroName) and ((not preFindText) or foundPreText):
					writeLog("No match found")
					break
				else:
					i += 1
			# If we found a match, iterate through and write all the lines, skipping the matches
			if matchFound:
				j = 0
				newText = []
				while j < len(fileText):
					if j not in removeLines:
						newText.append(fileText[j])
					j += 1
				writeLog("Writing updates to code macro")
				File.WriteAllLines(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm', newText)
				writeLog("Removed code macro entry")
		writeLog(macroName + " remove finished")

# Function to delete ending files
def deleteEndingFiles(endingId):
		writeLog("Deleting ending .pac files for ending ID " + str(endingId))
		if File.Exists(MainForm.BuildPath + '/pf/menu/intro/ending/EndingAll' + str(endingId) + '.pac'):
			writeLog("Deleting EndingAll file")
			createBackup(MainForm.BuildPath + '/pf/menu/intro/ending/EndingAll' + str(endingId) + '.pac')
			File.Delete(MainForm.BuildPath + '/pf/menu/intro/ending/EndingAll' + str(endingId) + '.pac')
		if File.Exists(MainForm.BuildPath + '/pf/menu/intro/ending/EndingSimple' + str(endingId) + '.pac'):
			writeLog("Deleting EndingSimple file")
			createBackup(MainForm.BuildPath + '/pf/menu/intro/ending/EndingSimple' + str(endingId) + '.pac')
			File.Delete(MainForm.BuildPath + '/pf/menu/intro/ending/EndingSimple' + str(endingId) + '.pac')
		writeLog("Finished deleting ending files")

# Function to delete ending movie
def deleteEndingMovie(fighterName):
		writeLog("Deleting ending movie file")
		if File.Exists(MainForm.BuildPath + '/pf/movie/End_' + fighterName + '.thp'):
			createBackup(MainForm.BuildPath + '/pf/movie/End_' + fighterName + '.thp')
			File.Delete(MainForm.BuildPath + '/pf/movie/End_' + fighterName + '.thp')
		writeLog("Finished deleting ending movie file")

# Function to do all the ending remove work
def uninstallEndingFiles(fighterName, fighterId):
		endingId = updateEndingCode(fighterId, True)
		deleteEndingFiles(endingId)
		deleteEndingMovie(fighterName)

# Function to do all the credits remove work
def uninstallCreditsSong(slotId):
		songId = updateCreditsCode(slotId, "0x0000", remove=True)
		removeSong(int(songId, 16), 'Credits', 'Credits')

#endregion REMOVE FUNCTIONS

#region EXTRACT FUNCTIONS

# Extract CSPs
def extractCSPs(cosmeticId):
		writeLog("Extracting CSPs with cosmetic ID " + str(cosmeticId))
		# If RSP file is not already opened, open it
		filePath = MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId) + '0', 3) + '.brres'
		if File.Exists(filePath):
			writeLog("Found file " + filePath)
			fileOpened = openFile(filePath, False)
			if fileOpened:
				texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
				if texFolder:
					i = 1
					for child in texFolder.Children:
						# Export each child to temp folder
						writeLog("Exporting CSP " + child.Name)
						exportPath = createDirectory(AppPath + '/temp/CSPs/' + addLeadingZeros(str(i), 4))
						child.Export(exportPath + '/' + child.Name + '.png')
						# If it doesn't share data, it is either the end of a color smash group, or standalone, so create a new folder
						if not child.SharesData:
							i += 1
				BrawlAPI.ForceCloseFile()
		writeLog("Finished exporting CSPs")

# Extract CSS icon
def extractCSSIcon(cosmeticId, folderName):
		writeLog("Extracting CSS icon with cosmetic ID " + str(cosmeticId) + " to folder " + folderName)
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac', False)
		if fileOpened:
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [70]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			tex0Node = getChildByName(texFolder, "MenSelchrChrFace." + addLeadingZeros(str(cosmeticId), 3))
			nameNode = getChildByName(texFolder, "MenSelchrChrNmS." + addLeadingZeros(str(cosmeticId), 3))
			exportPath = createDirectory(AppPath + '/temp/CSSIcon/' + folderName)
			if node:
				tex0Node.Export(exportPath + '/' + tex0Node.Name + '.png')
			if nameNode:
				exportPath = createDirectory(exportPath + '/Name')
				nameNode.Export(exportPath + '/' + nameNode.Name + '.png')
		writeLog("Finished extracting CSS icon")

# Extract portrait name
def extractPortraitName(cosmeticId, folderName):
		writeLog("Extracting portrait name with cosmetic ID " + str(cosmeticId) + " to folder " + folderName)
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac', False)
		if fileOpened:
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			tex0Node = getChildByName(texFolder, "MenSelchrChrNm." + addLeadingZeros(str(cosmeticId), 2) + '1')
			if tex0Node:
				exportPath = createDirectory(AppPath + '/temp/PortraitName/' + folderName)
				tex0Node.Export(exportPath + '/' + tex0Node.Name + '.png')
		writeLog("Finished extracting portrait name")

# Extract stock icons
def extractStockIcons(cosmeticId, tex0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true"):
		writeLog("Extracting stock icons for " + str(cosmeticId))
		fileOpened = openFile(MainForm.BuildPath + filePath, False)
		if fileOpened:
			rootNode = BrawlAPI.RootNode
			if rootName != "":
				rootNode = getChildByName(BrawlAPI.RootNode, rootName)
			if tex0BresName != "":
				node = getChildByName(rootNode, tex0BresName)
			else:
				node = rootNode
			# Extract the texture nodes
			texFolder = getChildByName(node, "Textures(NW4R)")
			# End of loop changes depending on if we use 50 CC or not
			newId = (cosmeticId * 50) + 1 if fiftyCC == "true" else int(str(cosmeticId) + "1")
			texNodeNames = []
			cap = ((cosmeticId * 50) + 50) if fiftyCC == "true" else int(str(cosmeticId) + "0") + 10
			i = 1
			while newId <= cap:
				texNode = getChildByName(texFolder, "InfStc." + addLeadingZeros(str(newId), 4 if fiftyCC == "true" else 3))
				if texNode:
					texNodeNames.append(texNode.Name)
					exportPath = createDirectory(AppPath + '/temp/StockIcons/' + addLeadingZeros(str(i), 4))
					texNode.Export(exportPath + '/' + texNode.Name + '.png')
					# If it doesn't share data, it is either the end of a color smash group, or standalone, so create a new folder
					if not texNode.SharesData:
						i += 1
				else:
					break
				newId += 1
			writeLog("Finished extracting stock icons")

# Extract franchise icon
def extractFranchiseIcon(franchiseIconId, filePath):
		writeLog("Extracting franchise icon ID " + str(franchiseIconId) + " at filepath " + filePath)
		fileOpened = openFile(MainForm.BuildPath + filePath, False)
		if fileOpened:
			# Extract icon
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			nodeName = "MenSelchrMark." + addLeadingZeros(str(franchiseIconId), 2)
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				exportPath = createDirectory(AppPath + '/temp/FranchiseIcons/Black')
				textureNode.Export(exportPath + '/' + textureNode.Name + '.png')
		writeLog("Finished extracting franchise icon")

# Extract BP name
def extractBPName(cosmeticId, filePath, folderName):
		writeLog("Extracting BP name with cosmetic ID " + str(cosmeticId) + " at " + filePath)
		fileOpened = openFile(MainForm.BuildPath + filePath, False)
		if fileOpened:
			# Extract BP name
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			nodeName = "MenSelchrChrNmS." +addLeadingZeros(str(cosmeticId) + '1', 3)
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				exportPath = createDirectory(AppPath + '/temp/BPs/' + folderName + '/Name')
				textureNode.Export(exportPath + '/' + textureNode.Name + '.png')
		writeLog("Finished extracting BP name")

# Extract Classic intro
def extractClassicIntro(cosmeticId):
		writeLog("Extracting class intro file for cosmetic ID " + str(cosmeticId + 1))
		filePath = MainForm.BuildPath + '/pf/menu/intro/enter/chr' + addLeadingZeros(str(cosmeticId + 1), 4) + '.brres'
		if File.Exists(filePath):
			copyFile(filePath, AppPath + '/temp/ClassicIntro')
		writeLog("Finished extracting classic intro file")

# Extract franchise icon from result
def extractFranchiseIconResult(franchiseIconId):
		writeLog("Extracting franchise icon ID " + str(franchiseIconId) + " from STGRESULT.pac")
		fileOpened = openFile(MainForm.BuildPath + '/pf/stage/melee/STGRESULT.pac', False)
		if fileOpened:
			# Extract icon
			node = getChildByName(getChildByName(BrawlAPI.RootNode, "2"), "Misc Data [110]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			textureNode = getChildByName(texFolder, "MenSelchrMark." + addLeadingZeros(str(franchiseIconId), 2))
			if textureNode:
				exportPath = createDirectory(AppPath + '/temp/FranchiseIcons/Transparent')
				textureNode.Export(exportPath + '/' + textureNode.Name + '.png')
		writeLog("Finished extracting franchise icon")

# Extract BPs
def extractBPs(cosmeticId, folderName, fiftyCC="true"):
		writeLog("Extracting BPs for cosmetic ID " + str(cosmeticId))
		# For 50 costume code, we must multipley the cosmetic ID by 50
		newId = (cosmeticId * 50) + 1 if fiftyCC == "true" else int(str(cosmeticId) + "1")
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/info/portrite')
		# Look for files matching naming scheme and extract them
		while newId <= (cosmeticId * 50) + 50:
			bpFile = getFileByName("InfFace" + addLeadingZeros(str(newId), 4 if fiftyCC == "true" else 3) + ".brres", directory)
			if bpFile:
				fileOpened = openFile(bpFile.FullName, False)
				if fileOpened:
					writeLog("Extracting BP file " + bpFile.FullName)
					texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
					if texFolder:
						if texFolder.Children:
							writeLog("Extracting texture " + texFolder.Children[0].Name)
							exportPath = createDirectory(AppPath + '/temp/BPs/' + folderName)
							texFolder.Children[0].Export(exportPath + '/' + texFolder.Children[0].Name + '.png')
							writeLog("Extracted texture")
					BrawlAPI.ForceCloseFile()
			else:
				# If no matching file exists, just exit
				break
			newId += 1
		writeLog("Finished extracting BPs")

# Extract replay icon
def extractReplayIcon(cosmeticId):
		writeLog("Extract replay icon for cosmetic ID " + str(cosmeticId))
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu/collection/Replay.brres', False)
		if fileOpened:
			texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
			nodeName = "MenReplayChr." + addLeadingZeros(str(cosmeticId) + "1", 3)
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				exportPath = createDirectory(AppPath + '/temp/ReplayIcon')
				textureNode.Export(exportPath + '/' + textureNode.Name + '.png')
		writeLog("Finished extracting replay icon")

# Extract soundbank
def extractSoundbank(soundBankId):
		writeLog("Extracting soundbank ID " + str(soundBankId))
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/sfx')
		soundBank = getFileByName(str(soundBankId).upper() + ".sawnd", directory)
		if soundBank:
			exportPath = createDirectory(AppPath + '/temp/Soundbank')
			copyFile(soundBank.FullName, exportPath)
		writeLog("Extract soundbank ID complete")

# Extract song from tracklist
def extractSong(songID, songDirectory='Victory!', tracklist='Results'):
		writeLog("Extracting theme with song ID " + str(songID))
		fileOpened = openFile(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist + '.tlst', False)
		if fileOpened:
			node = BrawlAPI.RootNode
			if node.Children:
				for child in node.Children:
					if child.SongID == songID:
						childNode = child
						break
			if 'childNode' in locals():
				# Get filename
				path = MainForm.BuildPath + '/pf/sound/strm/' + songDirectory
				directory = Directory.CreateDirectory(path)
				brstmFile = getFileByName(childNode.SongFileName.split('/')[1] + ".brstm", directory)
				if brstmFile:
					writeLog("Extracting file " + brstmFile.FullName)
					exportPath = createDirectory(AppPath + '/temp/VictoryTheme')
					copyFile(brstmFile.FullName, exportPath)
			BrawlAPI.ForceCloseFile()
		writeLog("Finished extracting theme")

# Read a code macro
def readCodeMacro(id, macroName, position=0, preFindText="", filePath='/ProjectM/CloneEngine.asm'):
		writeLog("Reading ID " + str(id) + " " + macroName + " entry")
		if File.Exists(MainForm.BuildPath + '/Source/' + filePath):
			# Read file
			writeLog("Reading " + MainForm.BuildPath + '/Source/' + filePath)
			fileText = File.ReadAllLines(MainForm.BuildPath + '/Source/' + filePath)
			matchFound = False
			foundMacros = False
			foundPreText = False
			i = 0
			foundValues = []
			# Search for matching ID and if one is found, return the values
			while i < len(fileText):
				line = fileText[i]
				if preFindText != "" and line.strip() == preFindText:
					foundPreText = True
				# Get the ID out of the entry
				if str(line).strip().StartsWith('%' + macroName) and ((not preFindText) or foundPreText):
					writeLog("Found macro entries")
					foundId = line.split(',')[position]
					if '0x' + str(id) in foundId:
						writeLog("Found matching entry")
						matchFound = True
						for value in line.split(','):
							if '(' in value:
								value = value.split('(')[1].strip()
							elif ')' in value:
								value = value.split(')')[0].strip()
							foundValues.append(value)
					i += 1
				# If we hit the end, just exit
				elif foundMacros and not matchFound and not str(line).strip().StartsWith("%" + macroName) and ((not preFindText) or foundPreText):
					writeLog("No match found")
					break
				else:
					i += 1
			writeLog(macroName + " read finished")
			return foundValues

# Extract Kirby Hat
def extractKirbyHat(fighterId, internalName):
		writeLog("Extracting Kirby hat for fighter ID " + fighterId)
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/fighter/kirby')
		kirbyHatFiles = Directory.GetFiles(directory.FullName, "FitKirby" + internalName + "*.pac")
		if kirbyHatFiles:
			i = 0
			while i < len(kirbyHatFiles):
				writeLog("Extracting Kirby hat file " + kirbyHatFiles[i])
				exportPath = createDirectory(AppPath + '/temp/KirbyHats')
				copyFile(kirbyHatFiles[i], exportPath)
				i += 1
		kirbyHatId = ""
		kirbyHatMacro = readCodeMacro(fighterId, 'HatFloatFix', 0, filePath='/Extras/KirbyHatEX.asm')
		if kirbyHatMacro and len(kirbyHatMacro) > 1:
			kirbyHatId = kirbyHatMacro[1]
			exportPath = createDirectory(AppPath + '/temp/KirbyHats')
			File.WriteAllText(exportPath + '/FighterID.txt', kirbyHatId)
		writeLog("Extract Kirby hat files complete")

# Extract fighter files from build
def extractFighterFiles(fighterName):
		writeLog("Extracting fighter files")
		path = MainForm.BuildPath + '/pf/fighter/' + fighterName.lower()
		if Directory.Exists(path):
			for file in Directory.GetFiles(path, "*.pac"):
				writeLog("Extracting file " + file)
				exportPath = createDirectory(AppPath + '/temp/Fighter')
				copyFile(file, exportPath)
		writeLog("Finished extracting fighter files")

# Extract module file
def extractModuleFile(internalName):
		writeLog("Extracting module for fighter name " + internalName)
		path = MainForm.BuildPath + '/pf/module'
		if Directory.Exists(MainForm.BuildPath + '/pf/module'):
			directory = DirectoryInfo(path)
			moduleFile = getFileByName("ft_" + internalName.lower() + ".rel", directory)
			if moduleFile:
				exportPath = createDirectory(AppPath + '/temp/Module')
				copyFile(moduleFile.FullName, exportPath)
		writeLog("Finished extracting module")

# Extract EX configs
def extractExConfigs(fighterId, slotConfigId="", cosmeticConfigId="", cssSlotConfigId=""):
		writeLog("Extracting Ex configs for fighter ID " + fighterId)
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/BrawlEx')
		for folder in Directory.GetDirectories(directory.FullName):
			writeLog("Getting config from " + folder)
			if DirectoryInfo(folder).Name == "SlotConfig" and slotConfigId:
				writeLog("Slot ID " + str(slotConfigId))
				id = slotConfigId
			elif DirectoryInfo(folder).Name == "CosmeticConfig" and cosmeticConfigId:
				writeLog("Cosmetic config ID " + str(cosmeticConfigId))
				id = cosmeticConfigId
			elif DirectoryInfo(folder).Name == "CSSSlotConfig" and cssSlotConfigId:
				writeLog("CSSSlot config ID " + str(cssSlotConfigId))
				id = cssSlotConfigId
			else:
				writeLog("Fighter ID " + str(fighterId))
				id = fighterId
			exConfig = getFileByName(DirectoryInfo(folder).Name.split("Config")[0] + str(id) + ".dat", DirectoryInfo(folder))
			if exConfig:
				writeLog("Extracting config " + exConfig.FullName)
				exportPath = createDirectory(AppPath + '/temp/EXConfigs')
				copyFile(exConfig.FullName, exportPath)
		writeLog("Finished extracting Ex configs")

# Extract ending files
def extractEndingFiles(fighterName, cosmeticConfigId):
		endingId = updateEndingCode(cosmeticConfigId, read=True)
		writeLog("Extracting ending .pac files for ending ID " + str(endingId))
		if File.Exists(MainForm.BuildPath + '/pf/menu/intro/ending/EndingAll' + str(endingId) + '.pac'):
			writeLog("Extracting EndingAll file")
			exportPath = createDirectory(AppPath + '/temp/Ending')
			copyFile(MainForm.BuildPath + '/pf/menu/intro/ending/EndingAll' + str(endingId) + '.pac', exportPath)
		if File.Exists(MainForm.BuildPath + '/pf/menu/intro/ending/EndingSimple' + str(endingId) + '.pac'):
			writeLog("Extracting EndingSimple file")
			exportPath = createDirectory(AppPath + '/temp/Ending')
			copyFile(MainForm.BuildPath + '/pf/menu/intro/ending/EndingSimple' + str(endingId) + '.pac', exportPath)
		writeLog("Finished extracting ending files")
		writeLog("Extracting ending movie file")
		if File.Exists(MainForm.BuildPath + '/pf/movie/End_' + fighterName + '.thp'):
			exportPath = createDirectory(AppPath + '/temp/Ending')
			copyFile(MainForm.BuildPath + '/pf/movie/End_' + fighterName + '.thp', exportPath)
		writeLog("Finished extracting ending movie file")

#endregion

#region INSTALLER FUNCTIONS
# Installer functions that check for and remove existing elements before adding

# Install CSPs
def installCSPs(cosmeticId, directory, rspLoading):
		removeCSPs(cosmeticId)
		importCSPs(cosmeticId, directory, rspLoading)

# Install stock icons
def installStockIcons(cosmeticId, directory, tex0BresName, pat0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true"):
		removeStockIcons(cosmeticId, tex0BresName, pat0BresName, rootName, filePath, fiftyCC)
		importStockIcons(cosmeticId, directory, tex0BresName, pat0BresName, rootName, filePath, fiftyCC)

# Install BPs
def installBPs(cosmeticId, images, fiftyCC="true"):
		deleteBPs(cosmeticId)
		createBPs(cosmeticId, images, fiftyCC)

# Install CSS icon
def installCSSIcon(cosmeticId, iconImagePath, format):
		removeCSSIcon(cosmeticId)
		importCSSIcon(cosmeticId, iconImagePath, format)

# Install replay icon
def installReplayIcon(cosmeticId, iconImagePath):
		removeReplayIcon(cosmeticId)
		importReplayIcon(cosmeticId, iconImagePath)
		BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()

# Install CSS icon name
def installCSSIconName(cosmeticId, nameImagePath):
		removeCSSIconName(cosmeticId)
		importCSSIconName(cosmeticId, nameImagePath)

# Install portrait name
def installPortraitName(cosmeticId, file):
		removePortraitName(cosmeticId)
		importPortraitName(cosmeticId, file)

# Install franchise icon into CSS or info
def installFranchiseIcon(franchiseIconId, image, filePath, size=0):
		removeFranchiseIcon(franchiseIconId, filePath)
		importFranchiseIcon(franchiseIconId, image, filePath, size)

# Install BP name into info
def installBPName(cosmeticId, image, filePath):
		removeBPName(cosmeticId, filePath)
		importBPName(cosmeticId, image, filePath)

# Install franchise icon into STGRESULT
def installFranchiseIconResult(franchiseIconId, image):
		removeFranchiseIconResult(franchiseIconId)
		importFranchiseIconResult(franchiseIconId, image)

# Install fighter files
def installFighterFiles(files, fighterName, oldFighterName="", changeFighterName=""):
		if oldFighterName:
			deleteFighterFiles(oldFighterName)
		moveFighterFiles(files, fighterName, changeFighterName)

# Install module file
def installModuleFile(file, directory, fighterId, fighterName, oldFighterName=""):
		if oldFighterName:
			deleteModule(oldFighterName)
		updateModule(file, directory, fighterId, fighterName)

# Install to roster
def installToRoster(fighterId):
		removeFromRoster(fighterId)
		addToRoster(fighterId)
		BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()

# Install Kirby hat
def installKirbyHat(characterName, fighterName, fighterId, kirbyHatFigherId, kirbyHatExe, files, oldFighterName="", newFighterName=""):
		deleteKirbyHatFiles(fighterName)
		addKirbyHat(characterName, fighterId, kirbyHatFigherId, kirbyHatExe)
		moveKirbyHatFiles(files, oldFighterName, newFighterName)

# Install ending files
def installEndingFiles(directory, fighterName, fighterId):
		endingId = updateEndingCode(fighterId)
		importEndingFiles(Directory.GetFiles(directory.FullName, "*.pac"), endingId)
		movieFiles = Directory.GetFiles(directory.FullName, "*.thp")
		if movieFiles:
			importEndingMovie(movieFiles[0], fighterName)

# Install credits theme
def installCreditsTheme(file, slotId):
		creditsThemeId = hexId(addSong(file, 'Credits', 'Credits'))
		updateCreditsCode(slotId, creditsThemeId)

#endregion INSTALLER FUNCTIONS

#region GENERAL FUNCTIONS
# General utility functions for the BrawlInstaller plugin suite

# Unzip fighter zip file and store contents in temporary directory
def unzipFile(filePath):
		writeLog("Unzipping file " + filePath)
		ZipFile.ExtractToDirectory(filePath, Path.Combine(AppPath, "temp"))

# Get info from supplied fighter and cosmetic IDs
def getFighterInfo(fighterConfig, cosmeticConfig, slotConfig):
		writeLog("Getting fighter info")
		fighterName = ""
		soundbankId = 0
		cosmeticId = 0
		franchiseIconId = 0
		songId = 0
		characterName = ""
		if fighterConfig:
			writeLog("Retrieving information from " + fighterConfig)
			BrawlAPI.OpenFile(fighterConfig)
			fighterName = BrawlAPI.RootNode.FighterName
			soundbankId = BrawlAPI.RootNode.SoundBank
			BrawlAPI.ForceCloseFile()
		if cosmeticConfig:
			writeLog("Retrieving information from " + cosmeticConfig)
			BrawlAPI.OpenFile(cosmeticConfig)
			cosmeticId = BrawlAPI.RootNode.CosmeticID
			# Add 1 because the franchise icon ID in the config is 1 less
			franchiseIconId = BrawlAPI.RootNode.FranchiseIconID + 1
			characterName = BrawlAPI.RootNode.CharacterName
			BrawlAPI.ForceCloseFile()
		if slotConfig:
			writeLog("Retrieving information from " + slotConfig)
			BrawlAPI.OpenFile(slotConfig)
			songId = BrawlAPI.RootNode.VictoryTheme
			BrawlAPI.ForceCloseFile()
		writeLog("Get fighter info finished")
		return FighterInfo(fighterName, cosmeticId, franchiseIconId, soundbankId, songId, characterName)

# Check if franchise icon ID is already used
def franchiseIconIdUsed(franchiseIconId):
		writeLog("Checking if franchise icon ID " + str(franchiseIconId) + " is already in use")
		fileOpened = checkOpenFile("sc_selcharacter")
		if fileOpened == 0:
			fileOpened = BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			node = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
			texFolder = getChildByName(node, "Textures(NW4R)")
			franchiseIcon = getChildByName(texFolder, "MenSelchrMark." + str(franchiseIconId))
			if franchiseIcon:
				return franchiseIcon
			else:
				return 0
		writeLog("Franchise icon check complete")

# Restore backup
def restoreBackup(selectedBackup=""):
		writeLog("Restoring backup")
		if selectedBackup:
			backupPath = selectedBackup
		else:
			backupPath = BACKUP_PATH
		writeLog("Selected backup " + backupPath)
		if Directory.Exists(backupPath):
			backupFiles = Directory.GetFiles(backupPath, "*", SearchOption.AllDirectories)
			for file in backupFiles:
				Directory.CreateDirectory(file.replace(backupPath, MainForm.BuildPath).replace(getFileInfo(file).Name, ''))
				File.Copy(file, file.replace(backupPath, MainForm.BuildPath), True)
			BrawlAPI.ShowMessage("Backup restored.", "Success")
		writeLog("Finished restoring backup")

# Archive backup
def archiveBackup():
		writeLog("Archiving backup")
		if Directory.Exists(BACKUP_PATH):
			# If we have >= 9 backups, find the oldest one and delete it
			if len(Directory.GetDirectories(BASE_BACKUP_PATH)) >= 9:
				oldestDir = BACKUP_PATH
				for backup in Directory.GetDirectories(BASE_BACKUP_PATH):
					if Directory.GetCreationTimeUtc(backup) < Directory.GetCreationTimeUtc(oldestDir):
						oldestDir = backup
				Directory.Delete(oldestDir, True)
			# Get current timestamp
			timestamp = str(Directory.GetCreationTimeUtc(BACKUP_PATH)).replace(':', '.').replace('/', '-').replace('\\', '-')
			Directory.CreateDirectory(BACKUP_PATH + ' - ' + timestamp)
			# Copy everything to a new directory with the timestamp
			backupFiles = Directory.GetFiles(BACKUP_PATH, "*", SearchOption.AllDirectories)
			for file in backupFiles:
				Directory.CreateDirectory(file.replace(BACKUP_PATH, BACKUP_PATH + ' - ' + timestamp).replace(getFileInfo(file).Name, ''))
				File.Copy(file, file.replace(BACKUP_PATH, BACKUP_PATH + ' - ' + timestamp), True)
			# Delete the old directory
			Directory.Delete(BACKUP_PATH, True)
		writeLog("Backup archive complete")

# Check if backup folder already exists, and if it does, delete it - should never get here, but on the off chance somehow we do
def backupCheck():
		if Directory.Exists(BACKUP_PATH):
			Directory.Delete(BACKUP_PATH, True)

# Get the name of the module the character's module was cloned from
def getClonedModuleName(filePath):
		BrawlAPI.OpenFile(filePath)
		name = BrawlAPI.RootNode.Name
		closeModule()
		return name

# Get new SFX ID from old SFX ID if we changed soundbanks
def getNewSfxId(sfxId, sfxChangeExe):
		writeLog("Getting new SFX ID for SFX ID " + str(sfxId))
		filePath = getFileInfo(sfxChangeExe).Directory.FullName
		if filePath:
			if File.Exists(filePath + '/sound.txt'):
				fileText = File.ReadAllLines(filePath + '/sound.txt')
				for line in fileText:
					if str(line).split(' ')[0] == sfxId:
						writeLog("Matching SFX ID found at line: " + line + ", new ID is " + str(line).split(' ')[1])
						return str(line).split(' ')[1]
		return ""

#endregion GENERAL FUNCTIONS

#region SETUP FUNCTIONS
def getSettings():
		writeLog("Reading settings file")
		Directory.SetCurrentDirectory(RESOURCE_PATH)
		fileText = File.ReadAllLines(RESOURCE_PATH + '/settings.ini')
		settings = Settings()
		settings.rspLoading = readValueFromKey(fileText, "rspLoading")
		settings.cssIconStyle = readValueFromKey(fileText, "cssIconStyle")
		settings.bpStyle = readValueFromKey(fileText, "bpStyle")
		settings.portraitNameStyle = readValueFromKey(fileText, "portraitNameStyle")
		settings.installPortraitNames = readValueFromKey(fileText, "installPortraitNames")
		settings.franchiseIconSizeCSS = readValueFromKey(fileText, "franchiseIconSizeCSS")
		settings.installStocksToCSS = readValueFromKey(fileText, "installStocksToCSS")
		settings.installStocksToInfo = readValueFromKey(fileText, "installStocksToInfo")
		settings.installStockIconsToResult = readValueFromKey(fileText, "installStockIconsToResult")
		settings.installStocksToStockFaceTex = readValueFromKey(fileText, "installStocksToStockFaceTex")
		settings.installStocksToSSS = readValueFromKey(fileText, "installStocksToSSS")
		settings.fiftyCostumeCode = readValueFromKey(fileText, "fiftyCostumeCode")
		settings.installKirbyHats = readValueFromKey(fileText, "installKirbyHats")
		settings.defaultKirbyHat = readValueFromKey(fileText, "defaultKirbyHat")
		settings.kirbyHatExe = readValueFromKey(fileText, "kirbyHatExe")
		settings.assemblyFunctionsExe = readValueFromKey(fileText, "assemblyFunctionsExe")
		settings.sawndReplaceExe = readValueFromKey(fileText, "sawndReplaceExe")
		settings.sfxChangeExe = readValueFromKey(fileText, "sfxChangeExe")
		settings.soundbankStyle = readValueFromKey(fileText, "soundbankStyle")
		settings.addSevenToSoundbankIds = readValueFromKey(fileText, "addSevenToSoundbankIds")
		settings.addSevenToSoundbankName = readValueFromKey(fileText, "addSevenToSoundbankName")
		settings.installVictoryThemes = readValueFromKey(fileText, "installVictoryThemes")
		settings.useCssRoster = readValueFromKey(fileText, "useCssRoster")
		settings.gfxChangeExe = readValueFromKey(fileText, "gfxChangeExe")
		settings.installBPNames = readValueFromKey(fileText, "installBPNames")
		settings.installSingleplayerCosmetics = readValueFromKey(fileText, "installSingleplayerCosmetics")
		writeLog("Reading settings complete")
		return settings

def getFighterSettings():
		writeLog("Reading fighter settings file")
		fighterSettings = FighterSettings()
		if File.Exists(AppPath + '/temp/FighterSettings.txt'):
			fileText = File.ReadAllLines(AppPath + '/temp/FighterSettings.txt')
			fighterSettings.lucarioBoneId = hexId(readValueFromKey(fileText, "lucarioBoneId"))
			fighterSettings.lucarioKirbyEffectId = hexId(readValueFromKey(fileText, "lucarioKirbyEffectId"))
			fighterSettings.jigglypuffBoneId = hexId(readValueFromKey(fileText, "jigglypuffBoneId"))
			fighterSettings.jigglypuffEFLSId = hexId(readValueFromKey(fileText, "jigglypuffEFLSId"))
			jigglypuffSfxIds = readValueFromKey(fileText, "jigglypuffSfxIds").split(',')
			if jigglypuffSfxIds:
				fighterSettings.jigglypuffSfxIds = []
				for id in jigglypuffSfxIds:
					fighterSettings.jigglypuffSfxIds.append(hexId(id))
			fighterSettings.bowserBoneId = hexId(readValueFromKey(fileText, "bowserBoneId"))
			throwReleasePoint = readValueFromKey(fileText, "throwReleasePoint")
			if throwReleasePoint:
				fighterSettings.throwReleasePoint = []
				for id in throwReleasePoint.split(','):
					fighterSettings.throwReleasePoint.append(id)
			fighterSettings.creditsThemeId = hexId(readValueFromKey(fileText, "creditsThemeId"))
		writeLog("Reading fighter settings complete")
		return fighterSettings

def initialSetup():
		settings = Settings()
		title = "Setup"
		defaultSettings = BrawlAPI.ShowYesNoPrompt("Would you like to use Project+ EX default settings? Only choose this option if you have a Project+ EX build that doesn't have major modifications.", title)
		if defaultSettings:
			settings.rspLoading = "false"
			settings.cssIconStyle = "P+"
			settings.bpStyle = "vBrawl"
			settings.installPortraitNames = "false"
			settings.portraitNameStyle = "vBrawl"
			settings.franchiseIconSizeCSS = 128
			settings.installStocksToCSS = "true"
			settings.installStocksToInfo = "true"
			settings.installStockIconsToResult = "true"
			settings.installStocksToStockFaceTex = "true"
			settings.fiftyCostumeCode = "true"
			settings.soundbankStyle = "hex"
			settings.addSevenToSoundbankName = "false"
			settings.addSevenToSoundbankIds = "true"
			settings.installVictoryThemes = "true"
			settings.useCssRoster = "true"
			settings.installBPNames = "false"
			settings.installSingleplayerCosmetics = "true"
		if not defaultSettings:
			# RSP Loading
			settings.rspLoading = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use RSP loading? (For most builds, the answer is 'No'.)", title))
			BrawlAPI.ShowMessage("You will be prompted to select a CSS icon style. Enter an integer corresponding to the below options:\n1 : Diamond (Project+ style)\n2 : Hexagon (PMEX REMIX style)\n3 : Vanilla Brawl Style\n4 : Project M Style", title)
			# CSS icons
			iconOption = BrawlAPI.UserIntegerInput(title, "Icon Option: ", 1, 1, 4)
			if iconOption == 2:
				settings.cssIconStyle = "REMIX"
			elif iconOption == 3:
				settings.cssIconStyle = "vBrawl"
			elif iconOption == 4:
				settings.cssIconStyle = "PM"
			else:
				settings.cssIconStyle = "P+"
			# BPs
			BrawlAPI.ShowMessage("You will be prompted to select a BP style. Enter an integer corresponding to the below options:\n1 : Vanilla Brawl Style\n2 : PMEX REMIX Style", title)
			bpOption = BrawlAPI.UserIntegerInput(title, "BP Option: ", 1, 1, 2)
			if bpOption == 2:
				settings.bpStyle = "REMIX"
			else:
				settings.bpStyle = "vBrawl"
			# Portrait names
			settings.installPortraitNames = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use names on character select portraits? (For most builds, the answer is 'Yes'. For Project+ builds, the answer is usually 'No'.)", title))
			if settings.installPortraitNames == "true":
				BrawlAPI.ShowMessage("You will be prompted to select a portrait name style. Enter an integer corresponding to the below options:\n1 : Vanilla Brawl Style\n2 : Project M Style", title)
				portraitNameOption = BrawlAPI.UserIntegerInput(title, "Name Option: ", 1, 1, 2)
				if portraitNameOption == 2:
					settings.portraitNameStyle = "PM"
				else:
					settings.portraitNameStyle = "vBrawl"
			else:
				settings.portraitNameStyle = "vBrawl"
			# BP Names
			settings.installBPNames = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use names by the battle portraits during a match? (For most modern builds and Project+ builds, the answer is 'No'. For vBrawl, the answer is probably 'Yes'.)", title))
			BrawlAPI.ShowMessage("You will be prompted to enter a size for franchise icons used on the character select screen. This will apply to both the height and width of these icons.\n\nFor most builds, the size should be 64. For Project+ builds, the size is usually 128.", title)
			# Franchise icon size
			settings.franchiseIconSizeCSS = BrawlAPI.UserIntegerInput(title, "Franchise Icon Size: ", 64, 1, 256)
			# Stock icons
			useStockIcons = BrawlAPI.ShowYesNoPrompt("Does your build use character-specific stock icons anywhere at all? (For most builds, the answer is 'Yes'.)", title)
			if useStockIcons:
				settings.installStocksToCSS = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use character-specific stock icons on the CSS for modes like classic mode? (For most builds, the answer is 'Yes'.)", title))
				settings.installStocksToInfo = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use character-specific stock icons during battle? (For Project M and Project+ builds, the answer is usually 'Yes'. For other builds, the answer is probably 'No'.)", title))
				settings.installStockIconsToResult = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use character-specific stock icons on the results screen? (For most builds, the answer is 'Yes'.)", title))
				settings.installStocksToStockFaceTex = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use character-specific stock icons in the StockFaceText.brres file? (For most builds, the answer is 'Yes'.)", title))
				settings.installStocksToSSS = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use character-specific stock icons on the stage select screen? (For most Project M and Project+ based builds, the answer is 'No'. For vBrawl based builds, the answer is probably 'Yes'.)", title))
			else:
				settings.installStocksToCSS = "false"
				settings.installStocksToInfo = "false"
				settings.installStockIconsToResult = "false"
				settings.installStocksToStockFaceTex = "false"
				settings.installStocksToSSS = "false"
			settings.fiftyCostumeCode = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use the fifty-costume code? (If your build is a Project+EX build or allows 50 costumes, the answer is most likely 'Yes'. Otherwise, the answer is probably 'No'.)", title))
			settings.installSingleplayerCosmetics = BrawlAPI.ShowYesNoPrompt("Would you like to install franchise icons " + " and battle portrait names " if settings.installBPNames else "" + "for single player modes (such as Training, Home Run Contest, etc.)?", title)
		# Kirby hats
		kirbyHatManagerInstalled = BrawlAPI.ShowYesNoPrompt("Do you have QuickLava's Kirby Hat Manager installed into your build?", title)
		if kirbyHatManagerInstalled:
			settings.kirbyHatExe = BrawlAPI.OpenFileDialog("Select your Kirby Hat Manager .exe", "Executable files|*.exe")
			defaultKirbyHat = BrawlAPI.ShowYesNoPrompt("In the event a valid Kirby hat is not found for a fighter you attempt to install, you may set a default Kirby hat to fall back on. This can be any fighter ID from the vanilla Brawl roster. This is highly recommended for P+ EX builds.\n\nWhen in doubt, Lucario's ID (0x21) is recommended for stability.\n\nWould you like to set a default?", title)
			if defaultKirbyHat:
				idEntered = False
				kirbyHatFighterId = 'none'
				while idEntered != True:
					kirbyHatFighterId = BrawlAPI.UserStringInput("Enter your desired default fighter ID")
					# Ensure fighter ID is the hex value
					if kirbyHatFighterId.startswith('0x'):
						kirbyHatFighterId = kirbyHatFighterId
						break
					elif kirbyHatFighterId.isnumeric():
						kirbyHatFighterId = '0x' + str(hex(int(kirbyHatFighterId))).split('0x')[1].upper()
						break
					else:
						BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
						continue
				settings.defaultKirbyHat = kirbyHatFighterId
			else:
				BrawlAPI.ShowMessage("No default Kirby hat will be set. This may lead to instability for Kirby matches in P+ EX builds.", title)
				settings.defaultKirbyHat = 'none'
		else:
			BrawlAPI.ShowMessage("Kirby hats will not be installed. This may lead to instability for P+ EX builds.", title)
			settings.kirbyHatExe = ""
			settings.defaultKirbyHat = 'none'
		# Code menu
		if not defaultSettings:
			useCodeMenu = BrawlAPI.ShowYesNoPrompt("Does your build use the code menu? (For P+ builds, the answer is probably 'Yes.' For other builds, the answer is probably 'No'.)", title)
		else:
			useCodeMenu = True
		if useCodeMenu:
			assemblyFunctionsInstalled = BrawlAPI.ShowYesNoPrompt("Do you have QuickLava's PowerPC Assembly Functions installed into your build?", title)
			if assemblyFunctionsInstalled:
				settings.assemblyFunctionsExe = BrawlAPI.OpenFileDialog("Select your PowerPC Assembly Functions .exe", "Executable files|*.exe")
			else:
				settings.assemblyFunctionsExe = ""
				BrawlAPI.ShowMessage("Fighters will not be installed to the code menu.", title)
		else:
			settings.assemblyFunctionsExe = ""
		
		# Sound porting tools
		soundbankReplacerTools = BrawlAPI.ShowYesNoPrompt("If you have conflicting soundbanks in your build, you can use code's porting tools and QuickLava's sawnd replacer to automatically update soundbank IDs.\n\nDo you have code's sfxchange and QuickLava's sawnd ID replace installed?", title)
		if soundbankReplacerTools:
			settings.sawndReplaceExe = BrawlAPI.OpenFileDialog("Select your lavaSawndIDReplaceAssist .exe", "Executable files|*.exe")
			settings.sfxChangeExe = BrawlAPI.OpenFileDialog("Select your sfxchange .exe", "Executable files|*.exe")
		else:
			settings.sawndReplaceExe = ""
			settings.sfxChangeExe = ""
			BrawlAPI.ShowMessage("Soundbank IDs will not be able to be updated in the event of a conflict.", title)
		# GFX porting tools
		gfxReplacerTools = BrawlAPI.ShowYesNoPrompt("If you have conflicting Effect.pac IDs in your build, you can use code's porting tools to automatically update Effect.pac IDs.\n\nDo you have code's gfxchange.exe installed?", title)
		if gfxReplacerTools:
			settings.gfxChangeExe = BrawlAPI.OpenFileDialog("Select your gfxchange .exe", "Executable files|*.exe")
		else:
			settings.gfxChangeExe = ""
			BrawlAPI.ShowMessage("Effect.pac IDs will not be able to be updated in the event of a conflict.", title)
		if not defaultSettings:
			# Soundbanks
			soundbanksInHex = BrawlAPI.ShowYesNoPrompt("Are your .sawnd files usually named as a hex value? (For modern Project+ builds, the answer is most likely 'Yes'. For older builds, the answer is most likely 'No'.)", title)
			if soundbanksInHex:
				settings.soundbankStyle = "hex"
			else:
				settings.soundbankStyle = "dec"
			settings.addSevenToSoundbankName = boolText(BrawlAPI.ShowYesNoPrompt("When naming your .sawnd files, do you usually have to add 7 to the ID before naming? (For most modern P+ builds, the answer is most likely 'No'.)", title))
			settings.addSevenToSoundbankIds = boolText(BrawlAPI.ShowYesNoPrompt("Do you add 7 to your SFX IDs when calculating them for soundbanks? (For most modern P+ builds, the answer is 'Yes'.)", title))
			settings.installVictoryThemes = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use the modern P+ tracklist system? (For P+ builds, the answer is most likely 'Yes'.)", title))
			# Victory themes
			if settings.installVictoryThemes == "false":
				BrawlAPI.ShowMessage("Victory themes and credits themes can only be installed with the modern tracklist system. Victory themes and credits themes will not be installed.", title)
			# CSSRoster.dat
			settings.useCssRoster = boolText(BrawlAPI.ShowYesNoPrompt("Does your build use a CSSRoster.dat to determine who appears on the character select screen? (For most builds, the answer is 'Yes'.)", title))
		attrs = vars(settings)
		File.WriteAllText(RESOURCE_PATH + '/settings.ini', '\n'.join("%s = %s" % item for item in attrs.items()))
		BrawlAPI.ShowMessage("Setup complete.", title)
		return settings


#endregion SETUP FUNCTIONS

#region CLASSES

class Settings:
		rspLoading = "true"
		cssIconStyle = "P+"
		bpStyle = "vBrawl"
		portraitNameStyle = "PM"
		installPortraitNames = "false"
		franchiseIconSizeCSS = "128"
		installStocksToCSS = "false"
		installStocksToInfo = "false"
		installStockIconsToResult = "false"
		installStocksToStockFaceTex = "false"
		installStocksToSSS = "false"
		fiftyCostumeCode = "true"
		installKirbyHats = "true"
		defaultKirbyHat = "0x21"
		kirbyHatExe = ""
		assemblyFunctionsExe = ""
		sawndReplaceExe = ""
		sfxChangeExe = ""
		soundbankStyle = "hex"
		addSevenToSoundbankIds = "true"
		addSevenToSoundbankName = "false"
		installVictoryThemes = "true"
		useCssRoster = "true"
		gfxChangeExe = ""
		installBPNames = "false"
		installSingleplayerCosmetics = "false"

class FighterSettings:
		lucarioBoneId = ""
		lucarioKirbyEffectId = ""
		jigglypuffBoneId = ""
		jigglypuffEFLSId = ""
		jigglypuffSfxIds = []
		bowserBoneId = ""
		throwReleasePoint = []
		creditsThemeId = ""

class FighterInfo:
		def __init__(self, fighterName, cosmeticId, franchiseIconId, soundbankId, songId, characterName):
			self.fighterName = fighterName
			self.cosmeticId = cosmeticId
			self.franchiseIconId = franchiseIconId
			self.soundbankId = soundbankId
			self.songId = songId
			self.characterName = characterName

#endregion CLASSES