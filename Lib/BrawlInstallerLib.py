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
from System.Drawing import *
from System.Collections.Generic import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus.STEXNode import VariantType
from System.IO.Compression import ZipFile
from System.Windows.Forms import *

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

TROPHY_SERIES = {
	"Super Smash Bros." : 0,
	"The Subspace Emissary" : 1,
	"Super Mario Bros." : 2,
	"Donkey Kong" : 3,
	"The Legend of Zelda" : 4,
	"Metroid" : 5,
	"Yoshi's Island" : 6,
	"Kirby Super Star" : 7,
	"Star Fox" : 8,
	"Pokemon" : 9,
	"F-Zero" : 10,
	"Mother" : 11,
	"Ice Climber" : 12,
	"Fire Emblem" : 13,
	"Kid Icarus" : 14,
	"WarioWare" : 15,
	"Pikmin" : 16,
	"Animal Crossing" : 17,
	"Game & Watch" : 18,
	"Others" : 19,
	"Metal Gear Solid" : 20,
	"Sonic the Hedgehog" : 21
}

COSTUME_COLOR = {
	"Red" : 0,
	"Blue" : 1,
	"Yellow" : 2,
	"Green" : 3,
	"Purple" : 4,
	"LightBlue" : 5,
	"Pink" : 6,
	"Brown" : 7,
	"Black" : 8,
	"White" : 9,
	"Orange" : 10,
	"Grey" : 11
}

#endregion CONSTANTS

#region HELPER FUNCTIONS
# These are common functions frequently used by parts of the BrawlInstaller plugin suite

# Clear textboxes from a Windows forms group
def clearTextBoxes(groupBox):
		for control in groupBox.Controls:
			if control.GetType() == Panel:
				clearTextBoxes(control)
			elif control.GetType() == TextBox:
				control.Text = ""

# Validate all text boxes in a Windows form group are valid hex IDs
def validateTextBoxes(groupBox):
		validationPassed = True
		for control in groupBox.Controls:
			if control.GetType() == Panel:
				valid = validateTextBoxes(control)
				if not valid:
					validationPassed = False
			elif control.GetType() == TextBox:
				valid = hexId(control.Text)
				control.BackColor = Color.White if valid else Color.LightPink
				if not valid:
					validationPassed = False
		return validationPassed

# Validate a single text box is a valid hex ID
def validateTextBox(textBox):
		validationPassed = True
		valid = hexId(textBox.Text)
		textBox.BackColor = Color.White if valid else Color.LightPink
		if not valid:
			validationPassed = False
		return validationPassed

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

# Get child node by frame index
def getChildByFrameIndex(parentNode, index, getNearest=True):
		prevChild = 0
		if parentNode.Children:
			for child in parentNode.Children:
				if child.FrameIndex == index:
					return child
				if child.FrameIndex > index and getNearest:
					return prevChild
				prevChild = child
		return 0

# Helper function to sort PAT0Entry nodes by FrameIndex
def sortChildrenByFrameIndex(parentNode):
		childList = []
		for child in parentNode.Children:
			childList.append(child)
		for child in childList:
			while child.PrevSibling() is not None and child.FrameIndex < child.PrevSibling().FrameIndex:
				child.MoveUp()

# Helper function to move a node to the bottom of their branch
def moveNodeToEnd(node):
		while node.NextSibling() is not None:
			node.MoveDown()

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
		replace = node.GetType() == TEX0Node
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
		writeLog("Texture " + imageSource + " imported successfully")
		if not replace:
			texFolder = getChildByName(node, "Textures(NW4R)")
			newNode = texFolder.Children[len(texFolder.Children) - 1]
			return newNode
		else:
			return node

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
			pat0texEntryNode = getChildByFrameIndex(pat0texNode, frameIndex, False)
			pat0texEntryNode.Palette = palette
		sortChildrenByFrameIndex(pat0texNode)
		if overrideFrameCount > pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset:
			pat0Node.FrameCount = overrideFrameCount
		elif frameCountOffset != 0:
			pat0Node.FrameCount = pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset
		writeLog("PAT0 entry added successfully")
		return pat0texEntryNode

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
		if File.Exists(destinationPath + '/' + getFileInfo(sourcePath).Name):
			createBackup(destinationPath + '/' + getFileInfo(sourcePath).Name)
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
		if File.Exists(destinationPath + '/' + newName):
			createBackup(destinationPath + '/' + newName)
		File.Copy(sourcePath, destinationPath + '/' + newName, True)

# Helper method to more easily rename files
def renameFile(sourcePath, newName):
		writeLog("Attempting to rename file " + sourcePath + " to " + newName)
		createBackup(sourcePath)
		fileInfo = getFileInfo(sourcePath)
		File.Move(sourcePath, fileInfo.DirectoryName + '/' + newName)

# Return the text version of a boolean value
def boolText(boolVal):
		if boolVal == True:
			return "true"
		else:
			return "false"

# Return the bool version of a text value
def textBool(boolVal):
		if boolVal == "true":
			return True
		else:
			return False

# Ensure an ID is hexadecimal whether it was passed in as decimal or hex
def hexId(id):
		if str(id).startswith('0x'):
			try:
				int(id.replace('0x',''), 16)
			except ValueError:
				return ""
			id = '0x' + addLeadingZeros(str(id).upper().replace('0X', ''), 2)
			return id
		elif str(id).isnumeric():
			id = '0x' + addLeadingZeros(str(hex(int(id))).upper().replace('0X', ''), 2)
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
			# If we have a char_bust_tex in BrawlEx, export there too
			if Directory.Exists(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex'):
					createBackup(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
					newNode.Export(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
			# Set compression back
			newNode.Compression = "ExtendedLZ77"
			# If user has RSP loading on, get rid of changes to this file
			if rspLoading == "true":
				newNode.Remove()
			writeLog("Importing CSPs completed successfully")

# Insert CSPs at specified position
def addCSPs(cosmeticId, images, rspLoading="false", position=0, skipPositions=[]):
		writeLog("Updating CSPs at cosmetic ID " + str(cosmeticId))
		fileOpened = False
		costumeIndex = -1
		if rspLoading == "false":
			fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		else:
			fileOpened = openFile(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
		if fileOpened:
			if rspLoading == "false":
			# Find char_bust_tex_lz77
				arcNode = getChildByName(BrawlAPI.RootNode, "char_bust_tex_lz77")
				bresNode = getChildByName(arcNode, "Misc Data [" + str(cosmeticId) + "]")
			else:
				bresNode = BrawlAPI.RootNode
			if bresNode:
				texFolder = getChildByName(bresNode, "Textures(NW4R)")
				costumeCount = 1
				i = 0
				length = len(texFolder.Children)
				# Count costumes, find position for import
				for child in texFolder.Children:
					if costumeCount >= position and costumeCount - 1 not in skipPositions:
						break
					if not child.SharesData:
						costumeCount += 1
					i += 1
				costumeIndex = i + 1
				# Import images
				if len(images) > 1:
					ColorSmashImport(bresNode, images, 256)
				else:
					importTexture(bresNode, images[0], WiiPixelFormat.CI8, 128, 160)
				# Move CSPs after imported
				for child in texFolder.Children[i:length]:
					moveNodeToEnd(child)
				# Rename everything
				i = len(texFolder.Children) - 1
				while i >= 0:
					texFolder.Children[i].Name = "MenSelchrFaceB." + addLeadingZeros(str((cosmeticId * 10) + (i + 1)), 3)
					i -= 1
			if rspLoading == "false":
				# Export RSP while we're at it
				bresNode.Compression = "None"
				# Back up RSP if it exists
				createBackup(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
				writeLog("Exporting RSPs")
				bresNode.Export(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
				# Set compression back
				bresNode.Compression = "ExtendedLZ77"
			if rspLoading == "true":
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
				# If we have a char_bust_tex in BrawlEx, export there too
				if Directory.Exists(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex'):
					createBackup(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
					copyFile(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres', MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex')
		writeLog("Finished updating CSPs")
		return costumeIndex

# Import stock icons
def importStockIcons(cosmeticId, directory, tex0BresName, pat0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true", firstOnly=False):
		writeLog("Importing stock icons to " + filePath + " with cosmetic ID " + str(cosmeticId))
		# If info.pac is not already opened, open it
		# Check this out: https://github.com/soopercool101/BrawlCrate/blob/b089bf32f0cfb2b5f1e6d729b95da4dd169903f2/BrawlCrate/NodeWrappers/Graphics/TEX0Wrapper.cs#L231
		fileOpened = openFile(MainForm.BuildPath + filePath)
		# Get pat0 and bres files if they exist
		if File.Exists(AppPath + '/temp/pat0.pat0'):
			pat0 = AppPath + '/temp/pat0.pat0'
		else:
			pat0 = None
		if File.Exists(AppPath + '/temp/bres.brres'):
			bres = AppPath + '/temp/bres.brres'
		else:
			bres = None
		# Start stuff
		if fileOpened:
			rootNode = BrawlAPI.RootNode
			if rootName != "":
				rootNode = getChildrenByPrefix(BrawlAPI.RootNode, rootName)[0]
			if tex0BresName != "":
				node = getChildByName(rootNode, tex0BresName)
			else:
				node = rootNode
			texFolder = getChildByName(node, "Textures(NW4R)")
			# Import textures only if we don't already have a bres, or if we are just importing a single stock (for SSE)
			if firstOnly or not bres:
				# Import images and color smash them
				totalImages = []
				for folder in Directory.GetDirectories(directory.FullName):
					writeLog("Importing stock icons from folder " + folder)
					images = Directory.GetFiles(folder, "*.png")
					# Color smash images in folders with multiple
					if len(images) > 1 and not firstOnly:
						writeLog("Color smashing stock icons")
						ColorSmashImport(node, images, 32)
						writeLog("Imported color smashed icons")
					elif len(images) >= 1:
						writeLog("Importing standalone icon")
						importTexture(node, images[0], WiiPixelFormat.CI8, 32, 32)
						writeLog("Imported standalone icon")
					else:
						return 0
					if not firstOnly:
						for image in images:
							totalImages.append(image)
					else:
						totalImages.append(images[0])
						break
				# Rename the texture nodes
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
			else:
				# Get old icons and new icons so we can compare, in case pat0 was not found but bres was
				texNodes = []
				oldTexNodes = []
				for texNode in texFolder.Children:
					oldTexNodes.append(texNode.Name)
				# if the file is a .brres, replace it in the filesystem
				if BrawlAPI.RootNode.Name.endswith(".brres"):
					BrawlAPI.ForceCloseFile()
					copyRenameFile(bres, "StockFaceTex.brres", MainForm.BuildPath + '/pf/menu/common')
					BrawlAPI.OpenFile(MainForm.BuildPath + filePath)
				else:
					node.Replace(bres)
				texFolder = getChildByName(node, "Textures(NW4R)")
				for texNode in texFolder.Children:
					if texNode.Name not in oldTexNodes:
						texNodes.append(texNode)
			# Add to pat0
			if pat0BresName != "":
				pat0BresNode = getChildByName(rootNode, pat0BresName)
				anmTexPat = getChildByName(pat0BresNode, "AnmTexPat(NW4R)")
				if (BrawlAPI.RootNode.Name.StartsWith("sc_selmap")):
					pat0Nodes = [ getChildByName(anmTexPat, "MenSelmapPlayer1_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer2_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer3_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer4_TopN") ]
				else:
					pat0Nodes = [ getChildByName(anmTexPat, "InfStockface_TopN__0") ]
				# Only add pat0 entries if we don't already have a pat0 exported
				if not pat0:
					for pat0Node in pat0Nodes:
						# For each texture we added, add a pat0 entry
						for texNode in texNodes:
							# Frame count is 9201 with 50 CC, 501 without, and it's 9301 or 601 on sc_selmap
							frameCount = 9201 if fiftyCC == "true" else 501
							if BrawlAPI.RootNode.Name.StartsWith("sc_selmap"):
								frameCount += 100
							addToPat0(pat0BresNode, pat0Node.Name, pat0Node.Children[0].Name, texNode.Name, texNode.Name, int(texNode.Name.split('.')[1]), palette=texNode.Name, frameCountOffset=1, overrideFrameCount=frameCount)
					# Export
					if len(pat0Nodes) >= 1:
						pat0Nodes[0].Export(AppPath + '/temp/pat0.pat0')
				else:
					# Replace pat0Nodes with existing export
					for pat0Node in pat0Nodes:
						pat0texNodeName = pat0Node.Children[0].Name
						pat0Node.Replace(pat0)
						pat0Node.Children[0].Name = pat0texNodeName
			# Strip the bres of all but stocks and export it
			if not bres:
				BrawlAPI.SaveFile()
				i = 0
				while i < len(node.Children):
					if node.Children[i].Name == 'Textures(NW4R)' or node.Children[i].Name == 'Palettes(NW4R)':
						i += 1
						continue
					else:
						node.Children[i].Remove()
					i += 1
				for child in node.GetChildrenRecursive():
					if child.GetType() == BRESGroupNode:
						continue
					elif not (child.Name.startswith('InfStc.') and (child.GetType() == TEX0Node or child.GetType() == PLT0Node)):
						child.Remove()
				node.Export(AppPath + '/temp/bres.brres')
				BrawlAPI.ForceCloseFile()
		writeLog("Import stock icons completed")

# Insert stock icons at specified position
def addStockIcons(cosmeticId, images, position, tex0BresName, pat0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true"):
		writeLog("Updating stock icons at cosmetic ID " + str(cosmeticId))
		fileOpened = openFile(MainForm.BuildPath + filePath)
		# Get pat0 and bres files if they exist
		if File.Exists(AppPath + '/temp/pat0.pat0'):
			pat0 = AppPath + '/temp/pat0.pat0'
		else:
			pat0 = None
		if File.Exists(AppPath + '/temp/bres.brres'):
			bres = AppPath + '/temp/bres.brres'
		else:
			bres = None
		# Start stuff
		startId = (cosmeticId * 50) + position - 1 if fiftyCC == "true" else int(str(cosmeticId) + str(position - 1))
		if fileOpened:
			rootNode = BrawlAPI.RootNode
			if rootName != "":
				rootNode = getChildrenByPrefix(BrawlAPI.RootNode, rootName)[0]
			if tex0BresName != "":
				bresNode = getChildByName(rootNode, tex0BresName)
			else:
				bresNode = rootNode
			# Get folders
			texFolder = getChildByName(bresNode, "Textures(NW4R)")
			palFolder = getChildByName(bresNode, "Palettes(NW4R)")
			if not bres:
				# Get ending node
				end = (cosmeticId * (50 if fiftyCC=="true" else 1)) + 50 if fiftyCC=="true" else 10
				i = startId
				while i < end:
					node = getChildByName(texFolder, "InfStc." + addLeadingZeros(str(i), 4 if fiftyCC == "true" else 3))
					if node:
						endId = i + 1
					i += 1
				# Import textures
				if len(images) > 1:
					writeLog("Color smashing stock icons")
					ColorSmashImport(bresNode, images, 32)
					writeLog("Imported color smashed icons")
				elif len(images) >= 1:
					writeLog("Importing standalone icon")
					importTexture(bresNode, images[0], WiiPixelFormat.CI8, 32, 32)
					writeLog("Imported standalone icon")
				else:
					return 0
				# Rename old nodes
				id = endId
				texNodes = []
				increment = len(images)
				while id > startId:
					oldName = 'InfStc.' + addLeadingZeros(str(id), 4 if fiftyCC == "true" else 3)
					foundNode = getChildByName(texFolder, oldName)
					if foundNode:
						foundNode.Name = 'InfStc.' + addLeadingZeros(str(id + increment), 4 if fiftyCC == "true" else 3)
						texNodes.append(foundNode)
					id -= 1
				# Move new textures up and rename them
				imageCount = len(images)
				prevName = "InfStc." + addLeadingZeros(str(startId), 4 if fiftyCC == "true" else 3)
				i = 1
				while imageCount > 0:
					texNode = texFolder.Children[len(texFolder.Children) - imageCount]
					while texNode.PrevSibling() is not None and texNode.PrevSibling().Name != prevName:
						texNode.MoveUp()
					texNode.Name = "InfStc." + addLeadingZeros(str(startId + i), 4 if fiftyCC == "true" else 3)
					i += 1
					prevName = texNode.Name
					if startId + 1 >= endId:
						texNodes.append(texNode)
					imageCount -= 1
			else:
				# Get old icons and new icons so we can compare, in case pat0 was not found but bres was
				texNodes = []
				oldTexNodes = []
				for texNode in texFolder.Children:
					oldTexNodes.append(texNode.Name)
				# if the file is a .brres, replace it in the filesystem
				if BrawlAPI.RootNode.Name.endswith(".brres"):
					BrawlAPI.ForceCloseFile()
					copyRenameFile(bres, "StockFaceTex.brres", MainForm.BuildPath + '/pf/menu/common')
					BrawlAPI.OpenFile(MainForm.BuildPath + filePath)
				else:
					bresNode.Replace(bres)
				texFolder = getChildByName(bresNode, "Textures(NW4R)")
				for texNode in texFolder.Children:
					if texNode.Name not in oldTexNodes:
						texNodes.append(texNode)
			# Add new names to pat0
			if pat0BresName != "":
				pat0BresNode = getChildByName(rootNode, pat0BresName)
				anmTexPat = getChildByName(pat0BresNode, "AnmTexPat(NW4R)")
				if (BrawlAPI.RootNode.Name.StartsWith("sc_selmap")):
					pat0Nodes = [ getChildByName(anmTexPat, "MenSelmapPlayer1_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer2_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer3_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer4_TopN") ]
				else:
					pat0Nodes = [ getChildByName(anmTexPat, "InfStockface_TopN__0") ]
				if not pat0:
					for pat0Node in pat0Nodes:
						# For each texture we added, add a pat0 entry
						for texNode in texNodes:
							# Frame count is 9201 with 50 CC, 501 without, and it's 9301 or 601 on sc_selmap
							frameCount = 9201 if fiftyCC == "true" else 501
							if BrawlAPI.RootNode.Name.StartsWith("sc_selmap"):
								frameCount += 100
							removeFromPat0(pat0BresNode, pat0Node.Name, pat0Node.Children[0].Name, texNode.Name, frameCountOffset=1, overrideFrameCount=frameCount)
							addToPat0(pat0BresNode, pat0Node.Name, pat0Node.Children[0].Name, texNode.Name, texNode.Name, int(texNode.Name.split('.')[1]), palette=texNode.Name, frameCountOffset=1, overrideFrameCount=frameCount)
					# Export
					if len(pat0Nodes) >= 1:
						pat0Nodes[0].Export(AppPath + '/temp/pat0.pat0')
				else:
					# Replace pat0Nodes with existing export
					for pat0Node in pat0Nodes:
						pat0texNodeName = pat0Node.Children[0].Name
						pat0Node.Replace(pat0)
						pat0Node.Children[0].Name = pat0texNodeName
			# Strip the bres of all but stocks and export it
			if not bres:
				BrawlAPI.SaveFile()
				i = 0
				while i < len(bresNode.Children):
					if bresNode.Children[i].Name == 'Textures(NW4R)' or bresNode.Children[i].Name == 'Palettes(NW4R)':
						i += 1
						continue
					else:
						bresNode.Children[i].Remove()
					i += 1
				for child in bresNode.GetChildrenRecursive():
					if child.GetType() == BRESGroupNode:
						continue
					elif not (child.Name.startswith('InfStc.') and (child.GetType() == TEX0Node or child.GetType() == PLT0Node)):
						child.Remove()
				bresNode.Export(AppPath + '/temp/bres.brres')
				BrawlAPI.ForceCloseFile()
		writeLog("Finished stock icons update")

# Create battle portraits frome images
def createBPs(cosmeticId, images, fiftyCC="true", startIndex=1):
		writeLog("Creating BPs for cosmetic ID " + str(cosmeticId))
		# For 50 costume code, we must multiply the cosmetic ID by 50
		newId = (cosmeticId * 50) + startIndex if fiftyCC == "true" else int(str(cosmeticId) + str(startIndex))
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
def modifyExConfigs(files, cosmeticId, fighterId, fighterName, franchiseIconId=-1, useKirbyHat=False, newSoundBankId="", victoryThemeId=0, kirbyHatFighterId=-1, cosmeticConfigId="", cssSlotConfigId="", slotConfigId=""):
		writeLog("Modifying Ex Configs for fighter ID " + str(fighterId))
		if cosmeticConfigId == "":
			cosmeticConfigId = fighterId
		if slotConfigId == "":
			slotConfigId = fighterId
		if cssSlotConfigId == "":
			cssSlotConfigId = fighterId
		# Iterate through each file
		for file in files:
			file = getFileInfo(file)
			BrawlAPI.OpenFile(file.FullName)
			# Update CosmeticID field and rename CosmeticConfig
			if file.Name.lower().StartsWith("cosmetic"):
				writeLog("Updating " + file.Name)
				BrawlAPI.RootNode.CosmeticID = cosmeticId
				if cosmeticConfigId != slotConfigId:
					BrawlAPI.RootNode.HasSecondary = True
					BrawlAPI.RootNode.CharSlot1 = int(slotConfigId, 16)
				else:
					BrawlAPI.RootNode.HasSecondary = False
				if franchiseIconId != -1:
					BrawlAPI.RootNode.FranchiseIconID = franchiseIconId - 1
				# Back up first
				createBackup(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig/' + file.Name.replace(file.Name, "Cosmetic" + cosmeticConfigId + ".dat"))
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig/' + file.Name.replace(file.Name, "Cosmetic" + cosmeticConfigId + ".dat"))
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
				if cssSlotConfigId != cosmeticConfigId:
					BrawlAPI.RootNode.SetCosmeticSlot = True
					BrawlAPI.RootNode.CosmeticSlot = int(cosmeticConfigId, 16)
				else:
					BrawlAPI.RootNode.SetCosmeticSlot = False
				if cssSlotConfigId != slotConfigId:
					BrawlAPI.RootNode.SetPrimarySecondary = True
					BrawlAPI.RootNode.CharSlot1 = int(slotConfigId, 16)
				else:
					BrawlAPI.RootNode.SetPrimarySecondary = False
				# Back up first
				createBackup(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/' + file.Name.replace(file.Name, "CSSSlot" + cssSlotConfigId + ".dat"))
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/' + file.Name.replace(file.Name, "CSSSlot" + cssSlotConfigId + ".dat"))
			# Rename SlotConfig
			if file.Name.lower().StartsWith("slot"):
				writeLog("Updating " + file.Name)
				if victoryThemeId:
					BrawlAPI.RootNode.VictoryTheme = victoryThemeId
				if slotConfigId != fighterId:
					BrawlAPI.RootNode.SetSlot = True
					BrawlAPI.RootNode.CharSlot1 = int(fighterId, 16)
				else:
					BrawlAPI.RootNode.SetSlot = False
				# Back up first
				createBackup(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig/' + file.Name.replace(file.Name, "Slot" + slotConfigId + ".dat"))
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig/' + file.Name.replace(file.Name, "Slot" + slotConfigId + ".dat"))
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
			brresName = "Misc Data [30]" if not fileNodeName.startswith("if_adv_mngr") else "Misc Data [0]"
			node = getChildByName(BrawlAPI.RootNode, brresName)
			if fileNodeName == "sc_selcharacter":
				# set format based on size: <= 64 should be I4, greater should be I8
				format = WiiPixelFormat.I4 if size <= 64 else WiiPixelFormat.I8
				newNode = importTexture(node, image, format, sizeW=size)
				pat0texNodeName = "Card04"
				pat0NodeName = "MenSelchrCmark4_TopN__0"
			if fileNodeName.startswith("info") or fileNodeName.startswith("if_adv_mngr"):
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
			node = getChildByName(getChildrenByPrefix(BrawlAPI.RootNode, "2")[0], "Misc Data [110]")
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
		node.Export(directory.FullName + "/Section [8]")
		sectionFile = directory.FullName + "/Section [8]"
		with open(sectionFile,  mode='r+b') as readFile:
			data = str(binascii.hexlify(readFile.read(3)))
			readFile.close()
		# Ex modules only have 8 sections, so any with more is a different type of module
		if node and data == '000000':
			writeLog("Modifying Section [8] of module file")
			closeModule()
			# Get the exported section 8 file
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
			# TODO: If we add support for any non-EX modules that DO have a Section [8] and DO NOT have extra sections, we will need
			#to add a FighterSetting or something to explicitly specify those modules.
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
			file.close()
		writeLog("Replaced module contents")

# Update the SSE module
def updateSseModule(cssSlotId, unlockStage="end", remove=False, baseCssSlotId=""):
		writeLog("Updating sora_adv_stage.rel for CSSSlot ID " + str(cssSlotId))
		filePath = MainForm.BuildPath + '/pf/module/sora_adv_stage.rel'
		if File.Exists(filePath):
			moduleFile = getFileInfo(filePath)
			fileOpened = openFile(moduleFile.FullName)
			# Get section 8 and export it
			if fileOpened:
				node = getChildByName(BrawlAPI.RootNode, "Section [8]")
				if node:
					writeLog("Modifying Section [8] of module file")
					createDirectory(AppPath + "/temp/SSE")
					node.Export(AppPath + "/temp/SSE/Section [8]")
					closeModule()
					# Get the exported section 8 file
					sectionFile = AppPath + "/temp/SSE/Section [8]"
					# Search for ID
					matchFound = False
					with open(sectionFile, mode='r+b') as editFile:
						# First read the unmodified section file into a variable
						section = editFile.read()
						editFile.seek(0)
						fighterCount = 2 + int(binascii.hexlify(editFile.read(1)), 16)
						editFile.seek(2)
						i = 2
						# Add character only if they are not a sub-character
						if not baseCssSlotId:
							while i < 128:
								value = int(binascii.hexlify(editFile.read(1)), 16)
								# If we find a match, update it
								if value == int(cssSlotId, 16):
									writeLog("Match found at offset " + str(i))
									editFile.seek(i)
									if not remove:
										editFile.write(binascii.unhexlify(cssSlotId))
									else:
										editFile.write(binascii.unhexlify('00'))
										# Move all values after to the left by 1
										movedValues = editFile.read(128 - i)
										editFile.seek(i)
										editFile.write(movedValues)
										# Update the counter
										editFile.seek(0)
										currentValue = int(binascii.hexlify(editFile.read(1)), 16)
										writeLog("Updating fighter count to " + str(currentValue - 1))
										editFile.seek(0)
										editFile.write(binascii.unhexlify(addLeadingZeros("%x" % (currentValue - 1), 2)))
									matchFound = True
									break
								i += 1
							# If we didn't find a match, add an entry
							if not matchFound and not remove:
								writeLog("No match found, updating offset " + str(fighterCount))
								# Update first byte at the end of the fighter count
								editFile.seek(fighterCount)
								editFile.write(binascii.unhexlify(cssSlotId))
								# Update the counter
								editFile.seek(0)
								currentValue = int(binascii.hexlify(editFile.read(1)), 16)
								writeLog("Updating fighter count to " + str(currentValue + 1))
								editFile.seek(0)
								editFile.write(binascii.unhexlify(addLeadingZeros("%x" % (currentValue + 1), 2)))
						else:
							# If it's a sub character, set them up appropriately
							writeLog("Adding sub character to ID " + str(baseCssSlotId) + " with ID " + str(cssSlotId))
							# Position for sub-characters starts at 132, or 0x184 in hex
							position = 132 + int(baseCssSlotId, 16)
							editFile.seek(position)
							if not remove:
								replacement = cssSlotId
							else:
								replacement = baseCssSlotId
							editFile.write(binascii.unhexlify(replacement))
						# Add unlock conditions
						writeLog("Updating unlock stage")
						# IDs start at 2A for unlock stages (first Ex ID), so we subtract 2A to get how far we move
						# multiply by 4 because there are 4 bytes for each of these
						position = 376 + (4 * (int(cssSlotId, 16) - int('2A', 16)))
						editFile.seek(position)
						if remove:
							editFile.write(binascii.unhexlify('00000000'))
						elif unlockStage == "start":
							editFile.write(binascii.unhexlify('00000001'))
						elif unlockStage == "end":
							editFile.write(binascii.unhexlify('00000002'))
						# Save the modified section bytes to a variable
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
						file.close()
					writeLog("Replaced module contents")
				else:
					closeModule()
		writeLog("Finish update sora_adv_stage.rel")

# Import CSS icon for SSE
def importCSSIconSSE(cosmeticId, iconImagePath, nameImagePath=""):
		writeLog("Attempting to import CSS icon to SSE with cosmetic ID" + str(cosmeticId))
		filePath = MainForm.BuildPath + '/pf/menu/adventure/selchrcd_common.brres'
		if File.Exists(filePath):
			# If selchrcd_common is not already opened, open it
			fileOpened = openFile(filePath)
			if fileOpened:
				# Import icon texture
				newNode = importTexture(BrawlAPI.RootNode, iconImagePath, WiiPixelFormat.CMPR)
				newNode.Name = "MenSelchrChrFace." + addLeadingZeros(str(cosmeticId), 3)
				# Sort textures
				newNode.Parent.SortChildren()
				# Add CSS icon to CSS
				anmTexPat = getChildByName(BrawlAPI.RootNode, "AnmTexPat(NW4R)")
				pat0Node = getChildByName(anmTexPat, "MenAdvChrCd0001_TopN__0")
				addToPat0(BrawlAPI.RootNode, pat0Node.Name, "Face02", newNode.Name, newNode.Name, int(str(cosmeticId) + "1"), frameCountOffset=10)
				if nameImagePath:
					# Next, import the name
					writeLog("Importing CSS icon name")
					newNode = importTexture(BrawlAPI.RootNode, nameImagePath, WiiPixelFormat.I4)
					newNode.Name = "MenSelchrChrNmS." + addLeadingZeros(str(cosmeticId), 3)
					# Sort textures
					newNode.Parent.SortChildren()
					# Add CSS icon to CSS
					anmTexPat = getChildByName(BrawlAPI.RootNode, "AnmTexPat(NW4R)")
					pat0Node = getChildByName(anmTexPat, "MenAdvChrCd0001_TopN__0")
					addToPat0(BrawlAPI.RootNode, pat0Node.Name, "Face03", newNode.Name, newNode.Name, int(str(cosmeticId) + "1"), frameCountOffset=10)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		writeLog("Finished importing CSS icon")

# Create newcomer file for SSE
def createNewcomerFile(cosmeticConfigId, iconImagePath):
		writeLog("Creating SSE newcomer file for cosmetic config ID " + str(cosmeticConfigId))
		outputPath = MainForm.BuildPath + '/pf/menu/adventure/comer_tex/tex_face' + addLeadingZeros(str(int(cosmeticConfigId, 16) + 16), 3) + '.brres'
		createBackup(outputPath)
		BrawlAPI.New[BRRESNode]()
		importTexture(BrawlAPI.RootNode, iconImagePath, WiiPixelFormat.CMPR)
		BrawlAPI.SaveFileAs(outputPath)
		BrawlAPI.ForceCloseFile()
		writeLog("Finished creating newcomer file")

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

# Get unavailable costume IDs
def getUsedCostumeIds(cssSlotConfigId):
		writeLog("Checking used costume IDs for " + str(cssSlotConfigId))
		usedCostumes = []
		if File.Exists(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/CSSSlot' + str(cssSlotConfigId) + '.dat'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/CSSSlot' + str(cssSlotConfigId) + '.dat')
			if fileOpened:
				for child in BrawlAPI.RootNode.Children:
					usedCostumes.append(child.CostumeID)
				BrawlAPI.ForceCloseFile()
		writeLog("Finished checking used costume IDs")
		return usedCostumes

# Import costume files to fighter folder
def importCostumeFiles(files, fighterName, cssSlotConfigId, images=[]):
		writeLog("Attempting to move costume files")
		usedIds = getUsedCostumeIds(cssSlotConfigId)
		costumes = []
		j = 0
		for file in files:
			color = 11
			# Get first unused ID
			i = 0
			while i in usedIds:
				i += 1
			id = i
			file = getFileInfo(file)
			if 'Etc' in file.Name or 'Entry' in file.Name or 'Result' in file.Name or 'Final' in file.Name:
				continue
			# If the costume ends in a color, store that, otherwise default to Grey
			colorSet = False
			for key, value in sorted(COSTUME_COLOR.items()):
				if file.Name.endswith(key + '.pac'):
					writeLog("Color ends with " + str(key) + ", setting to " + str(value))
					color = value
					colorSet = True
			if not colorSet:
				if len(images) >= j:
					form = ColorPrompt(Bitmap(images[j]))
					result = form.ShowDialog(MainForm.Instance)
					color = form.selectedColor
			usedIds.append(id)
			costumes.append((id, color))
			# Copy the file
			newFileName = 'Fit' + fighterName + addLeadingZeros(str(id), 2) + '.pac'
			createBackup(MainForm.BuildPath + '/pf/fighter/' + fighterName + '/' + newFileName)
			copyRenameFile(file.FullName, newFileName, MainForm.BuildPath + '/pf/fighter/' + fighterName)
			# Get related files and copy them
			for relatedFile in files:
				relatedFile = getFileInfo(relatedFile)
				relatedFileName = ""
				if 'Final' in relatedFile.Name and relatedFile.Name.replace('Final','') == file.Name:
					relatedFileName = 'Fit' + fighterName + 'Final' + addLeadingZeros(str(id), 2) + '.pac'
				if 'Result' in relatedFile.Name and relatedFile.Name.replace('Result','') == file.Name:
					relatedFileName = 'Fit' + fighterName + 'Result' + addLeadingZeros(str(id), 2) + '.pac'
				if 'Entry' in relatedFile.Name and relatedFile.Name.replace('Entry','') == file.Name:
					relatedFileName = 'Fit' + fighterName + 'Entry' + addLeadingZeros(str(id), 2) + '.pac'
				if 'MotionEtc' in relatedFile.Name and relatedFile.Name.replace('MotionEtc','') == file.Name:
					relatedFileName = 'Fit' + fighterName + 'MotionEtc' + addLeadingZeros(str(id), 2) + '.pac'
				if 'Etc' in relatedFile.Name and relatedFile.Name.replace('Etc','') == file.Name:
					relatedFileName = 'Fit' + fighterName + 'Etc' + addLeadingZeros(str(id), 2) + '.pac'
				if relatedFileName:
					createBackup(MainForm.BuildPath + '/pf/fighter/' + fighterName + '/' + relatedFileName)
					copyRenameFile(relatedFile.FullName, relatedFileName, MainForm.BuildPath + '/pf/fighter/' + fighterName)
			j += 1
		writeLog("Finished importing costume files")
		return costumes

# Add entries to the CSS slot config
def addCssSlots(costumes, position, cssSlotConfigId):
		writeLog("Adding entries to CSS slot config for ID " + str(cssSlotConfigId))
		if File.Exists(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/CSSSlot' + str(cssSlotConfigId) + '.dat'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/CSSSlot' + str(cssSlotConfigId) + '.dat')
			if fileOpened:
				# Add an entry for each costume
				length = len(BrawlAPI.RootNode.Children)
				for costume in costumes:
					writeLog("Adding costume " + str(costume[0]))
					newNode = CSSCEntryNode()
					BrawlAPI.RootNode.AddChild(newNode)
					newNode.CostumeID = costume[0]
					newNode.Color = costume[1]
					writeLog("Added")
					# Move the entry up
					i = length
					while i >= position:
						newNode.MoveUp()
						i -= 1
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		writeLog("Finished adding CSS slot config entries")

# Enable all costumes on a fighter config
def enableAllCostumes(fighterConfigId):
		writeLog("Enabling all costumes for ID " + str(fighterConfigId))
		if File.Exists(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig/Fighter' + str(fighterConfigId) + '.dat'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig/Fighter' + str(fighterConfigId) + '.dat')
			if fileOpened:
				root = BrawlAPI.RootNode
				root.HasCostume00 = True
				root.HasCostume01 = True
				root.HasCostume02 = True
				root.HasCostume03 = True
				root.HasCostume04 = True
				root.HasCostume05 = True
				root.HasCostume06 = True
				root.HasCostume07 = True
				root.HasCostume08 = True
				root.HasCostume09 = True
				root.HasCostume10 = True
				root.HasCostume11 = True
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		writeLog("Finished adding CSS slot config entries")		

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
		fileOpened = False
		if File.Exists(MainForm.BuildPath + '/pf/BrawlEx/CSSRoster.dat'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/CSSRoster.dat')
		elif File.Exists(MainForm.BuildPath + '/pf/BrawlEx/css.bx'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/css.bx')
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
		createBackup(kirbyHatPath + '/ft_kirby.rel')
		createBackup(kirbyHatPath + '/KirbyHat.kbx')
		createBackup(kirbyHatPath + '/KirbyHatEX.asm')
		createBackup(MainForm.BuildPath + '/pf/BrawlEx/KirbyHat.kbx')
		createBackup(MainForm.BuildPath + '/pf/module/ft_kirby.rel')
		createBackup(MainForm.BuildPath + '/Source/Extras/KirbyHatEX.asm')
		createBackup(MainForm.BuildPath + '/BOOST.GCT')
		createBackup(MainForm.BuildPath + '/NETBOOST.GCT')
		createBackup(MainForm.BuildPath + '/RSBE01.GCT')
		createBackup(MainForm.BuildPath + '/NETPLAY.GCT')
		#End back up kirby files
		# Copy necessary files from build if not present
		if not File.Exists(kirbyHatPath + 'ft_kirby.rel'):
			kirbyRel = getFileRecursive("ft_kirby.rel", "ft_kirby.rel")
			if kirbyRel:
				copyFile(kirbyRel, kirbyHatPath)
		if not File.Exists(kirbyHatPath + 'KirbyHat.kbx'):
			kirbyKbx = getFileRecursive("KirbyHat.kbx", "KirbyHat.kbx")
			if kirbyKbx:
				copyFile(kirbyKbx, kirbyHatPath)
		if not File.Exists(kirbyHatPath + 'KirbyHatEX.asm'):
			kirbyAsm = getFileRecursive("KirbyHatEX.asm", "KirbyHatEX.asm")
			if kirbyAsm:
				copyFile(kirbyAsm, kirbyHatPath)
		# End copy necessary files
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
		writeLog("Adding song file " + file)
		# Move to strm directory
		file = getFileInfo(file)
		path = MainForm.BuildPath + '/pf/sound/strm/' + songDirectory + '/' + file.Name
		# Back up file if it already exists
		createBackup(path)
		getFileInfo(path).Directory.Create()
		File.Copy(file.FullName, path, 1)
		writeLog("Opening tracklist " + tracklist)
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
		writeLog("Finished adding song.")
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

# Check if codes from .asm file already exist in build
def checkGct(filePath):
		writeLog("Checking for existing gecko codes")
		codeMatches = []
		if not File.Exists(MainForm.BuildPath + '/log.txt'):
			buildGct()
		if File.Exists(MainForm.BuildPath + '/log.txt'):
			existingLines = File.ReadAllLines(MainForm.BuildPath + '/log.txt')
			newLines = File.ReadAllLines(filePath)
			for existingLine in existingLines:
				for newLine in newLines:
					if existingLine.strip() == newLine.strip() and newLine.strip() not in codeMatches:
						codeMatches.append(newLine.strip())
		writeLog("Finished checking gecko codes")
		return codeMatches

# Install .asm files
def installAsms(asmFiles):
		writeLog("Installing asm files into build")
		codePath = MainForm.BuildPath + '/Source/BrawlInstaller'
		createDirectory(codePath)
		boostText = ""
		if File.Exists(MainForm.BuildPath + '/BOOST.txt'):
			createBackup(MainForm.BuildPath + '/BOOST.txt')
			boostText = File.ReadAllLines(MainForm.BuildPath + '/BOOST.txt')
		for asmFile in asmFiles:
			copyFile(asmFile.FullName, codePath)
			text = '\n.include Source/BrawlInstaller/' + asmFile.Name
			if boostText and (text not in boostText):
				File.AppendAllText(MainForm.BuildPath + '/BOOST.txt', text)
		writeLog("Finished installing asm files")

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
			createBackup(MainForm.BuildPath + '/' + getFileInfo(file).Name)
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
		createBackup(MainForm.BuildPath + '/' + getFileInfo(file).Name)
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

# Add an L-load
def addAltCharacter(cssSlotId, baseCssSlotId):
		writeLog("Updating L-load code to set ID " + str(cssSlotId) + " as L-load for ID " + str(baseCssSlotId))
		path = MainForm.BuildPath + '/Source/ProjectM/CSS.asm'
		foundId = ""
		if File.Exists(path):
			createBackup(path)
			# Read CSS.asm
			writeLog("Reading CSS.asm")
			fileText = File.ReadAllLines(path)
			i = 0
			tableStart = 0
			# Find the l-load table
			while i < len(fileText):
				line = fileText[i]
				if line.startswith(".GOTO->Table_Skip"):
					writeLog("Found table at line " + str(i))
					tableStart = i + 2
					break
				i += 1
			# Search for position to replace
			i = tableStart
			tableEndReached = False
			# Count starts at -1 because the numbers are zero-indexed
			lineCounter = -1
			notWritten = True
			writeLog("Finding position to write")
			while i < len(fileText):
				line = fileText[i]
				splitLine = list(filter(None, line.split('|')[0].strip().split(',')))
				lineCounter = lineCounter + len(splitLine)
				if notWritten and not tableEndReached and lineCounter >= int(baseCssSlotId, 16):
					writeLog("Found write location on line " + str(i))
					newLine = splitLine
					# Have to subtract 1 because of zero-indexing
					foundId = newLine[(len(newLine) - (lineCounter - int(baseCssSlotId, 16))) - 1]
					newLine[(len(newLine) - (lineCounter - int(baseCssSlotId, 16))) - 1] = '0x' + addLeadingZeros(str(cssSlotId), 2)
					newString = ""
					for part in newLine:
						newString = newString + part.strip() + (', ' if part.strip() != '0x7F' else '')
					if len(fileText[i].split('|')) > 1:
						newString = newString + '|' + fileText[i].split('|')[1]
					fileText[i] = newString
					notWritten = False
				if tableStart and i >= tableStart and (len(line)) == 0 or line.startswith('Table_Skip:'):
					tableEndReached = True
				i += 1
			File.WriteAllLines(path, fileText)
			writeLog("Finished updating L-load code")
		return foundId

# Get name used in trophy code
def getSlotTrophyInfo(slotId):
		writeLog("Getting trophy info for slot ID " + str(slotId))
		if File.Exists(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm'):
			#createBackup(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm')
			fileText = File.ReadAllLines(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm')
			# First find the line that tells us where the code is
			i = 0
			name = ""
			trophyId = ""
			# Searching for slot ID
			while i < len(fileText):
				if fileText[i].startswith('op b 0x34 @ $806E29DC'):
					# We found the starting line, now look through the .aliases
					j = i
					aliasesDone = False
					foundAliases = False
					while aliasesDone == False:
						# If we get to the bottom of the aliases, start search
						if fileText[j].startswith('.alias') and not foundAliases:
							foundAliases = True
						# If we get to the top of the aliases, stop search
						if foundAliases and not fileText[j].startswith('.alias'):
							aliasesDone = True
							break
						# If we find a matching slot ID line, get the name associated
						if foundAliases and 'Slot' in fileText[j] and fileText[j].split('=')[1].strip() == '0x' + str(slotId):
							name = fileText[j].split('.alias')[1].split('=')[0].split('_Slot')[0].strip()
							break
						j -= 1
					# Next get the trophy ID
					j = i
					aliasesDone = False
					foundAliases = False
					while aliasesDone == False:
						# If we get to the bottom of the aliases, start search
						if fileText[j].startswith('.alias') and not foundAliases:
							foundAliases = True
						# If we get to the top of the aliases, stop search
						if foundAliases and not fileText[j].startswith('.alias'):
							aliasesDone = True
							break
						# If we find a matching name, get the trophy ID associated
						if foundAliases and fileText[j].split('=')[0].split('.alias')[1].strip() == name + '_Trophy':
							trophyId = fileText[j].split('=')[1].strip()
							break
						j -= 1
				i += 1
			writeLog("Finished get trophy info")
			return [ name, trophyId ]

# Update trophy code
def updateTrophyCode(slotId, trophyId, fighterName, remove=False):
		writeLog("Updating trophy code for " + str(slotId))
		# Get alias name prefix and trophy ID
		trophyInfo = getSlotTrophyInfo(slotId)
		if trophyInfo[1] != "":
			fighterName = trophyInfo[0]
		if File.Exists(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm'):
			createBackup(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm')
			fileText = File.ReadAllLines(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm')
			i = 0
			newFileText = []
			foundSlotAlias = False
			foundTrophyAlias = False
			classicTrophyStart = False
			allStarTrophyStart = False
			foundClassicLine = False
			foundAllStarLine = False
			lastAlias = -1
			# Read through the text
			while i < len(fileText):
				# Every time we find an alias line, store it's position as the last one we've found
				if fileText[i].startswith('.alias'):
					lastAlias = i
				# When we find the line that starts the Classic trophy load, set a boolean indicating such
				if fileText[i].startswith('HOOK @ $806E29D0'):
					classicTrophyStart = True
				# When we find the line that starts the All Star trophy load, set a boolean indicating such
				if fileText[i].startswith('HOOK @ $806E47D8'):
					allStarTrophyStart = True
				# If we find a match to our slot alias, store it
				if fileText[i].startswith('.alias ' + trophyInfo[0] + '_Slot'):
					foundSlotAlias = True
					if not remove:
						newFileText.append(fileText[i])
				# If we find a match to our trophy alias, update it
				elif fileText[i].startswith('.alias ' + trophyInfo[0] + '_Trophy') and 'AllStar' not in fileText[i]:
					foundTrophyAlias = True
					if not remove:
						newFileText.append('.alias ' + trophyInfo[0] + '_Trophy = ' + trophyId)
				# If we hit the line after the aliases, add them as needed
				elif fileText[i].startswith('op b 0x34 @ $806E29DC'):
					if not foundSlotAlias and not remove:
						newFileText.insert(lastAlias + 1, '.alias ' + fighterName + '_Slot = 0x' + str(slotId))
					if not foundTrophyAlias and not remove:
						newFileText.insert(lastAlias + 1, '.alias ' + fighterName + '_Trophy = ' + trophyId)
					newFileText.append(fileText[i])
				# If we find a matching Classic trophy, store that
				elif classicTrophyStart and fileText[i].strip().startswith('li r29,') and fighterName + '_Trophy' in fileText[i] and fighterName + '_Slot' in fileText[i]:
					if not remove:
						newFileText.append(fileText[i])
					foundClassicLine = True
				# If we find a matching All-Star trophy, store that
				elif allStarTrophyStart and fileText[i].strip().startswith('li r26,') and fighterName + '_Trophy' in fileText[i] and fighterName + '_Slot' in fileText[i]:
					if not remove:
						newFileText.append(fileText[i])
					foundAllStarLine = True
				# If we hit the end of the Classic trophies and no classic trophy found, write it
				elif classicTrophyStart and fileText[i].strip().startswith('li r29, 0x1') and not foundClassicLine and not remove:
					newFileText.append('\tli r29, ' + fighterName + '_Trophy;\tcmpwi r28, ' + fighterName + "_Slot;\tbeq+ GotTrophy\t# if it's " + fighterName + "'s slot")
					newFileText.append(fileText[i])
					classicTrophyStart = False
				# If we hit the end of the All Star trophies and no trophy found, write it
				elif allStarTrophyStart and fileText[i].strip().startswith('li r26, 0x5D') and not foundAllStarLine and not remove:
					newFileText.append('\tli r26, ' + fighterName + '_Trophy;\tcmpwi r28, ' + fighterName + "_Slot;\tbeq+ GotTrophy\t# if it's " + fighterName + "'s slot")
					newFileText.append(fileText[i])
					allStarTrophyStart = False
				# If just a normal line, append as normal
				else:
					newFileText.append(fileText[i])
				i += 1
			File.WriteAllLines(MainForm.BuildPath + '/Source/ProjectM/CloneEngine.asm', newFileText)
		writeLog("Finished update trophy code")

# Add trophy to game
def addTrophy(name, gameIcon1, gameIcon2, trophyName, gameName1, gameName2, description, seriesIndex, trophyId=-1):
		writeLog("Adding trophy " + name + " to common3.pac")
		# First check for existing trophy entry
		nameIndex = -1
		gameIndex = -1
		descriptionIndex = -1
		trophyExists = False
		if trophyId != -1:
			writeLog("Getting current trophy values")
			if File.Exists(MainForm.BuildPath + '/pf/system/common3.pac'):
				fileOpened = openFile(MainForm.BuildPath + '/pf/system/common3.pac')
				if fileOpened:
					tyDataNode = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
					tyDataList = getChildByName(tyDataNode, "tyDataList")
					for trophyNode in tyDataList.Children:
						if trophyNode.Id == trophyId:
							nameIndex = trophyNode.NameIndex
							gameIndex = trophyNode.GameIndex
							descriptionIndex = trophyNode.DescriptionIndex
							trophyExists = True
					BrawlAPI.ForceCloseFile()
		# Add name and game names
		writeLog("Adding trophy name " + trophyName + " and game names " + gameName1 + " " + gameName2)
		if File.Exists(MainForm.BuildPath + '/pf/toy/fig/ty_fig_name_list.msbin'):
			# When we do remove, we'll have to adjust the trophy IDs of every trophy after it... unless we keep the blank
			# Should be easy to do, when you remove one, check the code file for any IDs larger than the removed ID, and decrement them
			fileOpened = openFile(MainForm.BuildPath + '/pf/toy/fig/ty_fig_name_list.msbin')
			if fileOpened:
				BrawlAPI.RootNode.Export(AppPath + '/temp/ty_fig_name_list.txt')
				fileText = File.ReadAllLines(AppPath + '/temp/ty_fig_name_list.txt')
				newFileText = []
				i = 0
				id = -1
				textWritten1 = False
				textWritten2 = False
				for line in fileText:
					if nameIndex != -1 and i == nameIndex:
						newFileText.append(trophyName)
						textWritten1 = True
						nameIndex = i
						i += 1
					elif gameIndex != -1 and i == gameIndex:
						newFileText.append(gameName1 + (("<br/>" + gameName2) if gameName2 != "" else ""))
						textWritten2 = True
						gameIndex = i
						i += 1
					else:
						newFileText.append(fileText[i])
						i += 1
				if not textWritten1:
					newFileText.append(trophyName)
					nameIndex = i
				if not textWritten2:
					newFileText.append(gameName1 + (("<br/>" + gameName2) if gameName2 != "" else ""))
					gameIndex = i + 1
				File.WriteAllLines(AppPath + '/temp/ty_fig_name_list.txt', newFileText)
				BrawlAPI.RootNode.Replace(AppPath + '/temp/ty_fig_name_list.txt')
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		# Next add description
		writeLog("Adding trophy description")
		if File.Exists(MainForm.BuildPath + '/pf/toy/fig/ty_fig_ext_list.msbin'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/toy/fig/ty_fig_ext_list.msbin')
			if fileOpened:
				BrawlAPI.RootNode.Export(AppPath + '/temp/ty_fig_ext_list.txt')
				fileText = File.ReadAllLines(AppPath + '/temp/ty_fig_ext_list.txt')
				newFileText = []
				i = 0
				textWritten = False
				for line in fileText:
					if descriptionIndex != -1 and i == descriptionIndex:
						newFileText.append("<color=E6E6E6FF>" + description + "</end>")
						textWritten = True
						i += 1
					else:
						newFileText.append(fileText[i])
						i += 1
				if not textWritten:
					newFileText.append("<color=E6E6E6FF>" + description + "</end>")
					descriptionIndex = i
				File.WriteAllLines(AppPath + '/temp/ty_fig_ext_list.txt', newFileText)
				BrawlAPI.RootNode.Replace(AppPath + '/temp/ty_fig_ext_list.txt')
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		# Add trophy
		if not trophyExists:
			if File.Exists(MainForm.BuildPath + '/pf/system/common3.pac'):
				fileOpened = openFile(MainForm.BuildPath + '/pf/system/common3.pac')
				if fileOpened:
					tyDataNode = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
					tyDataList = getChildByName(tyDataNode, "tyDataList")
					# Get first available ID
					i = 0
					id = 631
					while i < len(tyDataList.Children):
						if tyDataList.Children[i].Id == id:
							id += 1
							i = 0
						else:
							i += 1
					trophyNode = TyDataListEntryNode()
					trophyNode.Name = name
					trophyNode.Id = id
					trophyNode.BRRES = name
					trophyNode.ThumbnailIndex = id
					trophyNode.GameIcon1 = gameIcon1
					trophyNode.GameIcon2 = gameIcon2
					trophyNode.NameIndex = nameIndex
					trophyNode.GameIndex = gameIndex
					trophyNode.DescriptionIndex = descriptionIndex
					trophyNode.SeriesIndex = seriesIndex
					trophyNode.CategoryIndex = 23
					trophyNode.Unknown0x34 = 1
					trophyNode.Unknown0x38 = 1
					trophyNode.Unknown0x40 = 1
					trophyNode.Unknown0x44 = 1
					trophyNode.Unknown0x50 = -0.13
					trophyNode.Unknown0x54 = 0.72
					trophyNode.Unknown0x58 = 1.23
					trophyNode.Unknown0x5C = 1.25
					tyDataList.AddChild(trophyNode)
					trophyId = id
					# After adding our trophy, move the <null> trophy to the end of the list
					nullNode = getChildByName(tyDataList, "<null>")
					moveNodeToEnd(nullNode)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		writeLog("Finished add trophy")
		return trophyId

# Add trophy thumbnail
def importTrophyThumbnail(imagePath, trophyId):
		writeLog("Importing trophy thumbnail at " + imagePath + " for trophy ID " + str(trophyId))
		if File.Exists(MainForm.BuildPath + '/pf/menu/collection/Figure.brres'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/menu/collection/Figure.brres')
			if fileOpened:
				newNode = importTexture(BrawlAPI.RootNode, imagePath, WiiPixelFormat.CMPR)
				newNode.Name = 'MenCollDisply01.' + str(trophyId)
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		writeLog("Finished import trophy thumbnail")

# Add trophy model
def importTrophyModel(modelPath):
		writeLog("Importing trophy model at " + modelPath)
		if File.Exists(modelPath):
			copyFile(modelPath, MainForm.BuildPath + '/pf/toy/fig')

# Assign SSE continue screen trophy
def updateTrophySSE(slotId, trophyId, remove=False):
		writeLog("Updating trophy module file for slot ID " + str(slotId))
		filePath = MainForm.BuildPath + '/pf/module/sora_adv_menu_game_over.rel'
		if File.Exists(filePath):
			moduleFile = getFileInfo(filePath)
			fileOpened = openFile(moduleFile.FullName)
			# Get section 8 and export it
			if fileOpened:
				node = getChildByName(BrawlAPI.RootNode, "Section [8]")
				if node:
					writeLog("Modifying Section [8] of module file")
					createDirectory(AppPath + "/temp/SSE/Trophy")
					node.Export(AppPath + "/temp/SSE/Trophy/Section [8]")
					closeModule()
					# Get the exported section 8 file
					sectionFile = AppPath + "/temp/SSE/Trophy/Section [8]"
					with open(sectionFile, mode='r+b') as editFile:
						# First read the unmodified section file into a variable
						section = editFile.read()
						writeLog("Updating trophy ID")
						position = (4 * (int(slotId, 16) - int('32', 16)))
						editFile.seek(position)
						if not remove:
							editFile.write(binascii.unhexlify(addLeadingZeros(str(trophyId), 8)))
						else:
							editFile.write(binascii.unhexlify('00000001'))
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
						file.close()
					writeLog("Replaced file contents")
				else:
					closeModule()
		writeLog("Finished updating SSE trophy")
					
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
		# Repeat if char_bust_tex in BrawlEx
		if Directory.Exists(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex'):
			rspFile = getFileByName("MenSelchrFaceB" + addLeadingZeros(str(cosmeticId), 2) + "0.brres", Directory.CreateDirectory(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex'))
			if rspFile:
				# Back up first
				createBackup(rspFile.FullName)
				writeLog("Deleting RSP file " + rspFile.FullName)
				rspFile.Delete()

# Remove CSPs at specified position
def subtractCSPs(cosmeticId, rspLoading="false", position=0, skipPositions=[]):
		writeLog("Removing CSPs for position " + str(position) + " for cosmetic ID " + str(cosmeticId))
		fileOpened = "false"
		costumeStart = -1
		costumeEnd = -1
		if rspLoading == "false":
			fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		else:
			fileOpened = openFile(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
		if fileOpened:
			if rspLoading == "false":
			# Find char_bust_tex_lz77
				arcNode = getChildByName(BrawlAPI.RootNode, "char_bust_tex_lz77")
				bresNode = getChildByName(arcNode, "Misc Data [" + str(cosmeticId) + "]")
			else:
				bresNode = BrawlAPI.RootNode
			if bresNode:
				texFolder = getChildByName(bresNode, "Textures(NW4R)")
				costumeCount = 1
				i = 0
				nodesToRemove = []
				length = len(texFolder.Children)
				# Loop through and remove the ones we want
				for child in texFolder.Children:
					if costumeCount >= position:
						if costumeStart == -1:
							costumeStart = i + 1
						if costumeEnd == -1:
							nodesToRemove.append(child)
					if not child.SharesData:
						if costumeStart != -1 and costumeEnd == -1 and costumeCount not in skipPositions:
							costumeEnd = i + 1
						costumeCount += 1
					i += 1
				# Remove
				i = 0
				while i < len(nodesToRemove):
					nodesToRemove[i].Remove(True)
					i += 1
				# Rename everything
				i = 0
				for child in texFolder.Children:
					i += 1
					child.Name = 'MenSelchrFaceB.' + addLeadingZeros(str((cosmeticId * 10) + i), 3)
			if rspLoading == "false":
				# Export RSP while we're at it
				bresNode.Compression = "None"
				# Back up RSP if it exists
				createBackup(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
				writeLog("Exporting RSPs")
				bresNode.Export(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
				# Set compression back
				bresNode.Compression = "ExtendedLZ77"
			if rspLoading == "true":
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
				# If we have a char_bust_tex in BrawlEx, copy there too
				if Directory.Exists(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex'):
					if File.Exists(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres'):
						createBackup(MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
						copyFile(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres', MainForm.BuildPath + '/pf/BrawlEx/char_bust_tex')
		writeLog("Finished updating CSPs")
		costumeRange = []
		costumeRange.append(costumeStart)
		costumeRange.append(costumeEnd)
		return costumeRange

# Remove stock icons at specified position
def subtractStockIcons(cosmeticId, startIndex, tex0BresName, pat0BresName, endIndex=-1, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true"):
		writeLog("Removing stock icons for position " + str(startIndex) + " for cosmetic ID " + str(cosmeticId))
		startId = (cosmeticId * 50) + startIndex - 1 if fiftyCC == "true" else int(str(cosmeticId) + str(startIndex - 1))
		fileOpened = openFile(MainForm.BuildPath + filePath)
		if fileOpened:
			rootNode = BrawlAPI.RootNode
			if rootName != "":
				rootNode = getChildrenByPrefix(BrawlAPI.RootNode, rootName)[0]
			if tex0BresName != "":
				bresNode = getChildByName(rootNode, tex0BresName)
			else:
				bresNode = rootNode
			# Get folders
			texFolder = getChildByName(bresNode, "Textures(NW4R)")
			palFolder = getChildByName(bresNode, "Palettes(NW4R)")
			if endIndex != -1:
				endId = (cosmeticId * 50) + endIndex if fiftyCC == "true" else int(str(cosmeticId) + str(endIndex))
			# Get ending node
			else:
				end = (cosmeticId * (50 if fiftyCC=="true" else 1)) + 50 if fiftyCC=="true" else 10
				i = startId
				while i < end:
					node = getChildByName(texFolder, "InfStc." + addLeadingZeros(str(i), 4 if fiftyCC == "true" else 3))
					if node:
						endId = i + 1
					i += 1
			# Remove nodes
			i = startId + 1
			while i <= endId:
				nodeToRemove = getChildByName(texFolder, "InfStc." + addLeadingZeros(str(i), 4 if fiftyCC == "true" else 3))
				if nodeToRemove:
					nodeToRemove.Remove(True)
				i += 1
			# Rename nodes
			i = endId
			j = startId
			lastId = -1
			newEnd = (cosmeticId * 50) + 50 if fiftyCC == "true" else int(str(cosmeticId) + str(10))
			while i < newEnd:
				nodeToRename = getChildByName(texFolder, "InfStc." + addLeadingZeros(str(i), 4 if fiftyCC == "true" else 3))
				if nodeToRename:
					nodeToRename.Name = "InfStc." + addLeadingZeros(str(j), 4 if fiftyCC == "true" else 3)
					lastId = j
				j += 1
				i += 1
			# Remove excess pat0 entries
			if pat0BresName == "":
				return
			pat0BresNode = getChildByName(rootNode, pat0BresName)
			anmTexPat = getChildByName(pat0BresNode, "AnmTexPat(NW4R)")
			if (BrawlAPI.RootNode.Name.StartsWith("sc_selmap")):
				pat0Nodes = [ getChildByName(anmTexPat, "MenSelmapPlayer1_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer2_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer3_TopN"), getChildByName(anmTexPat, "MenSelmapPlayer4_TopN") ]
			else:
				pat0Nodes = [ getChildByName(anmTexPat, "InfStockface_TopN__0") ]
			for pat0Node in pat0Nodes:
				if lastId != -1:
					i = lastId + 1
				else:
					i = startId + 1
				while i < newEnd:
					# Frame count is 9201 with 50 CC, 501 without, and it's 9301 or 601 on sc_selmap
					frameCount = 9201 if fiftyCC == "true" else 501
					if BrawlAPI.RootNode.Name.StartsWith("sc_selmap"):
						frameCount += 100
					nodeName = "InfStc." + addLeadingZeros(str(i), 4 if fiftyCC == "true" else 3)
					removeFromPat0(pat0BresNode, pat0Node.Name, pat0Node.Children[0].Name, nodeName, frameCountOffset=1, overrideFrameCount=frameCount)
					i += 1
		writeLog("Finished remove stock icons")

# Delete BPs for specified cosmetic ID
def deleteBPs(cosmeticId, fiftyCC="true", startIndex=1, endIndex=-1):
		writeLog("Deleting BPs for cosmetic ID " + str(cosmeticId))
		# For 50 costume code, we must multiply the cosmetic ID by 50
		newId = (cosmeticId * 50) + startIndex if fiftyCC == "true" else int(str(cosmeticId) + str(startIndex))
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/info/portrite')
		# Look for files matching naming scheme and delete them
		if endIndex == -1:
			endIndex = 50 if fiftyCC=="true" else 10
		while newId <= (cosmeticId * (50 if fiftyCC=="true" else 1)) + endIndex:
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
			brresName = "Misc Data [30]" if not fileNodeName.startswith("if_adv_mngr") else "Misc Data [0]"
			node = getChildByName(BrawlAPI.RootNode, brresName)
			texFolder = getChildByName(node, "Textures(NW4R)")
			nodeName = "MenSelchrMark." + addLeadingZeros(str(franchiseIconId), 2)
			textureNode = getChildByName(texFolder, nodeName)
			if textureNode:
				textureNode.Remove(True)
			if fileNodeName == "sc_selcharacter":
				pat0texNodeName = "Card04"
				pat0NodeName = "MenSelchrCmark4_TopN__0"
			if fileNodeName.startswith("info") or fileNodeName.startswith("if_adv_mngr"):
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
			node = getChildByName(getChildrenByPrefix(BrawlAPI.RootNode, "2")[0], "Misc Data [110]")
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
				rootNode = getChildrenByPrefix(BrawlAPI.RootNode, rootName)[0]
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
		fileOpened = False
		if File.Exists(MainForm.BuildPath + '/pf/BrawlEx/CSSRoster.dat'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/CSSRoster.dat')
		elif File.Exists(MainForm.BuildPath + '/pf/BrawlEx/css.bx'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/css.bx')
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
			BrawlAPI.SaveFile()
			BrawlAPI.ForceCloseFile()
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
			if '/' in childNode.SongFileName:
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
		# Copy necessary files from build if not present
		if not File.Exists(kirbyHatPath + 'ft_kirby.rel'):
			kirbyRel = getFileRecursive("ft_kirby.rel", "ft_kirby.rel")
			if kirbyRel:
				copyFile(kirbyRel, kirbyHatPath)
		if not File.Exists(kirbyHatPath + 'KirbyHat.kbx'):
			kirbyKbx = getFileRecursive("KirbyHat.kbx", "KirbyHat.kbx")
			if kirbyKbx:
				copyFile(kirbyKbx, kirbyHatPath)
		if not File.Exists(kirbyHatPath + 'KirbyHatEX.asm'):
			kirbyAsm = getFileRecursive("KirbyHatEX.asm", "KirbyHatEX.asm")
			if kirbyAsm:
				copyFile(kirbyAsm, kirbyHatPath)
		# End copy necessary files
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
def uninstallCreditsSong(slotId, removeTheme=True):
		songId = updateCreditsCode(slotId, "0x0000", remove=True)
		if removeTheme:
			removeSong(int(songId, 16), 'Credits', 'Credits')

# Remove CSS icon for SSE
def removeCSSIconSSE(cosmeticId):
		writeLog("Attempting to remove CSS icon from SSE with cosmetic ID " + str(cosmeticId))
		filePath = MainForm.BuildPath + '/pf/menu/adventure/selchrcd_common.brres'
		if File.Exists(filePath):
			# If selchrcd_common is not already opened, open it
			fileOpened = openFile(filePath)
			if fileOpened:
				# Remove icon texture
				writeLog("Removing icon texture")
				texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
				if texFolder:
					tex0Node = getChildByName(texFolder, "MenSelchrChrFace." + addLeadingZeros(str(cosmeticId), 3))
					if tex0Node:
						tex0Node.Remove()
					nameTex0Node = getChildByName(texFolder, "MenSelchrChrNmS." + addLeadingZeros(str(cosmeticId), 3))
					if nameTex0Node:
						nameTex0Node.Remove()
				# Remove icon from pat0
				writeLog("Removing icon pat0")
				anmTexPat = getChildByName(BrawlAPI.RootNode, "AnmTexPat(NW4R)")
				if anmTexPat:
					pat0Node = getChildByName(anmTexPat, "MenAdvChrCd0001_TopN__0")
					removeFromPat0(BrawlAPI.RootNode, pat0Node.Name, "Face02", "MenSelchrChrFace." + addLeadingZeros(str(cosmeticId), 3), frameCountOffset=10)
					removeFromPat0(BrawlAPI.RootNode, pat0Node.Name, "Face03", "MenSelchrChrNmS." + addLeadingZeros(str(cosmeticId), 3), frameCountOffset=10)
			BrawlAPI.SaveFile()
			BrawlAPI.ForceCloseFile()
		writeLog("Finished removing CSS icon")

# Delete newcomer file
def deleteNewcomerFile(cosmeticConfigId):
		writeLog("Deleting SSE newcomer file for cosmetic config ID " + str(cosmeticConfigId))
		path = MainForm.BuildPath + '/pf/menu/adventure/comer_tex/tex_face' + addLeadingZeros(str(int(cosmeticConfigId, 16) + 16), 3) + '.brres'
		if File.Exists(path):
			createBackup(path)
			file = getFileInfo(path)
			file.Delete()
		writeLog("Finished delete SSE newcomer file")

# Remove trophy
def removeTrophy(trophyId):
		writeLog("Removing trophy with ID " + str(trophyId))
		nameIndex = -1
		gameIndex = -1
		descriptionIndex = -1
		brresName = ""
		nodeToRemove = ""
		# Remove from trophy list
		if File.Exists(MainForm.BuildPath + '/pf/system/common3.pac'):
				fileOpened = openFile(MainForm.BuildPath + '/pf/system/common3.pac')
				if fileOpened:
					tyDataNode = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
					tyDataList = getChildByName(tyDataNode, "tyDataList")
					for trophyNode in tyDataList.Children:
						if trophyNode.Id == trophyId:
							nameIndex = trophyNode.NameIndex
							gameIndex = trophyNode.GameIndex
							descriptionIndex = trophyNode.DescriptionIndex
							brresName = trophyNode.BRRES
							nodeToRemove = trophyNode
							break
					nodeToRemove.Remove()
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()
		# Remove name and game names
		if File.Exists(MainForm.BuildPath + '/pf/toy/fig/ty_fig_name_list.msbin'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/toy/fig/ty_fig_name_list.msbin')
			if fileOpened:
				createDirectory(AppPath + '/temp')
				BrawlAPI.RootNode.Export(AppPath + '/temp/ty_fig_name_list.txt')
				fileText = File.ReadAllLines(AppPath + '/temp/ty_fig_name_list.txt')
				i = 0
				newFileText = []
				for line in fileText:
					if nameIndex != -1 and i == nameIndex:
						i += 1
						continue
					if gameIndex != -1 and i == gameIndex:
						i += 1
						continue
					else:
						newFileText.append(fileText[i])
						i += 1
				File.WriteAllLines(AppPath + '/temp/ty_fig_name_list.txt', newFileText)
				BrawlAPI.RootNode.Replace(AppPath + '/temp/ty_fig_name_list.txt')
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		# Remove description
		createDirectory(AppPath + '/temp')
		if File.Exists(MainForm.BuildPath + '/pf/toy/fig/ty_fig_ext_list.msbin'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/toy/fig/ty_fig_ext_list.msbin')
			if fileOpened:
				BrawlAPI.RootNode.Export(AppPath + '/temp/ty_fig_ext_list.txt')
				fileText = File.ReadAllLines(AppPath + '/temp/ty_fig_ext_list.txt')
				newFileText = []
				i = 0
				for line in fileText:
					if descriptionIndex != -1 and i == descriptionIndex:
						i += 1
						continue
					else:
						newFileText.append(fileText[i])
						i += 1
				File.WriteAllLines(AppPath + '/temp/ty_fig_ext_list.txt', newFileText)
				BrawlAPI.RootNode.Replace(AppPath + '/temp/ty_fig_ext_list.txt')
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		# Update indexes for any trophies that had greater indexes than the removed one
		if File.Exists(MainForm.BuildPath + '/pf/system/common3.pac'):
				fileOpened = openFile(MainForm.BuildPath + '/pf/system/common3.pac')
				if fileOpened:
					tyDataNode = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
					tyDataList = getChildByName(tyDataNode, "tyDataList")
					for trophyNode in tyDataList.Children:
						if nameIndex != -1 and trophyNode.NameIndex > nameIndex:
							trophyNode.NameIndex -= 1
						if gameIndex != -1 and trophyNode.GameIndex > gameIndex:
							trophyNode.GameIndex -= 1
						if descriptionIndex != -1 and trophyNode.DescriptionIndex > descriptionIndex:
							trophyNode.DescriptionIndex -= 1
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()
		writeLog("Finished remove trophy")
		return brresName

# Remove trophy thumbnail
def removeTrophyThumbnail(trophyId):
		writeLog("Removing trophy thumbnail for trophy ID " + str(trophyId))
		if File.Exists(MainForm.BuildPath + '/pf/menu/collection/Figure.brres'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/menu/collection/Figure.brres')
			if fileOpened:
				texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
				if texFolder:
					node = getChildByName(texFolder, "MenCollDisply01." + str(trophyId))
					if node:
						node.Remove()
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		writeLog("Finished remove trophy thumbnail")

# Delete trophy model
def deleteTrophyModel(bresName):
		writeLog("Deleting trophy model with name " + bresName)
		createBackup(MainForm.BuildPath + '/pf/toy/fig/' + bresName + '.brres')
		if File.Exists(MainForm.BuildPath + '/pf/toy/fig/' + bresName + '.brres'):
			File.Delete(MainForm.BuildPath + '/pf/toy/fig/' + bresName + '.brres')
		writeLog("Finished delete trophy model")

# Do all steps to uninstall a trophy
def uninstallTrophy(slotId, uninstallFromSse):
		trophyIdHex = getSlotTrophyInfo(slotId)[1]
		bresName = ""
		if trophyIdHex:
			trophyIdInt = int(trophyIdHex.replace('0x', ''), 16)
		else:
			trophyIdInt = -1
		# 630 is last vanilla trophy ID, so only remove if it's NOT a vanilla trophy
		if trophyIdInt > 630:
			bresName = removeTrophy(trophyIdInt)
			removeTrophyThumbnail(trophyIdInt)
			updateTrophyCode(slotId, hexId(trophyIdInt), "", True)
		if bresName and trophyIdInt > 630:
			deleteTrophyModel(bresName)
		if uninstallFromSse and trophyIdInt > 630:
			updateTrophySSE(slotId, hexId(trophyIdInt).replace('0x', ''), True)

# Remove an L-load code entry
def removeAltCharacter(cssSlotId):
		writeLog("Updating L-load code to remove ID " + str(cssSlotId) + " as alt character")
		path = MainForm.BuildPath + '/Source/ProjectM/CSS.asm'
		foundId = ""
		if File.Exists(path):
			createBackup(path)
			# Read CSS.asm
			writeLog("Reading CSS.asm")
			fileText = File.ReadAllLines(path)
			i = 0
			tableStart = 0
			# Find the l-load table
			while i < len(fileText):
				line = fileText[i]
				if line.startswith(".GOTO->Table_Skip"):
					writeLog("Found table at line " + str(i))
					tableStart = i + 2
					break
				i += 1
			# Search for position to replace
			i = tableStart
			tableEndReached = False
			writeLog("Finding position to write")
			lineCounter = 0
			while i < len(fileText):
				line = fileText[i]
				splitLine = list(filter(None, line.split('|')[0].strip().split(',')))
				lineCounter = lineCounter + len(splitLine)
				if tableStart and i >= tableStart and (len(line)) == 0 or line.startswith('Table_Skip:'):
					writeLog("Reached table end")
					tableEndReached = True
				if not tableEndReached:
					newLine = splitLine
					newString = ""
					j = 0
					while j < len(newLine):
						if newLine[j].strip() == '0x' + addLeadingZeros(cssSlotId, 2) and '0x' + addLeadingZeros(str("%x" % ((lineCounter - len(newLine)) + j)).upper(), 2) != '0x' + cssSlotId:
							foundId = '0x' + addLeadingZeros(str("%x" % ((lineCounter - len(newLine)) + j)).upper(), 2)
							writeLog("Found ID " + str(foundId))
						newValue = '0x' + addLeadingZeros(str("%x" % ((lineCounter - len(newLine)) + j)).upper(), 2)
						newString = newString + newValue + (', ' if newValue != '0x7F' else '')
						j += 1
					if len(fileText[i].split('|')) > 1:
						newString = newString + '|' + fileText[i].split('|')[1]
					fileText[i] = newString
				i += 1
			File.WriteAllLines(path, fileText)
			writeLog("Finished updating L-load code")
			return foundId

# Remove entries to the CSS slot config
def removeCssSlots(startIndex, endIndex, cssSlotConfigId):
		writeLog("Removing entries from CSS slot config for ID " + str(cssSlotConfigId))
		if File.Exists(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/CSSSlot' + str(cssSlotConfigId) + '.dat'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/CSSSlot' + str(cssSlotConfigId) + '.dat')
			if fileOpened:
				# Add an entry for each costume
				i = startIndex - 1
				costumeIds = []
				while i < endIndex:
					writeLog("i is " + str(i))
					costumeIds.append(BrawlAPI.RootNode.Children[startIndex - 1].CostumeID)
					BrawlAPI.RootNode.Children[startIndex - 1].Remove()
					i += 1
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		writeLog("Finished removing CSS slot config entries")
		return costumeIds	

# Delete costumes corresponding to CSS slot config IDs
def deleteCostumeFiles(costumeIds, fighterName):
		writeLog("Attempting to delete costume files")
		if Directory.Exists(MainForm.BuildPath + '/pf/fighter/' + fighterName):
			for id in costumeIds:
				costumeFiles = Directory.GetFiles(MainForm.BuildPath + '/pf/fighter/' + fighterName, "*" + addLeadingZeros(str(id), 2) + ".pac")
				for file in costumeFiles:
					createBackup(file)
					File.Delete(file)
		writeLog("Finished delete costume files")

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
			if tex0Node:
				tex0Node.Export(exportPath + '/' + tex0Node.Name + '.png')
			if nameNode:
				exportPath = createDirectory(exportPath + '/Name')
				nameNode.Export(exportPath + '/' + nameNode.Name + '.png')
		writeLog("Finished extracting CSS icon")

# Extract CSS icon
def extractCSSIconSSE(cosmeticId):
		writeLog("Extracting CSS icon with cosmetic ID " + str(cosmeticId) + " to folder vBrawl")
		if File.Exists(MainForm.BuildPath + '/pf/menu/adventure/selchrcd_common.brres'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/menu/adventure/selchrcd_common.brres', False)
			if fileOpened:
				texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
				tex0Node = getChildByName(texFolder, "MenSelchrChrFace." + addLeadingZeros(str(cosmeticId), 3))
				nameNode = getChildByName(texFolder, "MenSelchrChrNmS." + addLeadingZeros(str(cosmeticId), 3))
				exportPath = createDirectory(AppPath + '/temp/CSSIcon/vBrawl')
				if tex0Node:
					tex0Node.Export(exportPath + '/' + tex0Node.Name + '.png')
				if nameNode:
					exportPath = createDirectory(exportPath + '/Name')
					nameNode.Export(exportPath + '/' + nameNode.Name + '.png')
				BrawlAPI.ForceCloseFile()
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
			node = getChildByName(getChildrenByPrefix(BrawlAPI.RootNode, "2")[0], "Misc Data [110]")
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
		while ((newId <= (cosmeticId * 50) + 50) if fiftyCC == "true" else (newId <= cosmeticId + 10)):
			if File.Exists(MainForm.BuildPath + '/pf/info/portrite/' + "InfFace" + addLeadingZeros(str(newId), 4 if fiftyCC == "true" else 3) + ".brres"):
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
								texFolder.Children[0].Export(exportPath + '/' + bpFile.Name.replace('.brres','') + '.png')
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
def extractSong(songID, songDirectory='Victory!', tracklist='Results', exportFolder='VictoryTheme'):
		writeLog("Extracting theme with song ID " + str(songID))
		success = False
		if File.Exists(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist + '.tlst'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist + '.tlst', False)
			if fileOpened:
				node = BrawlAPI.RootNode
				if node.Children:
					for child in node.Children:
						if child.SongID == songID:
							childNode = child
							break
				if 'childNode' in locals():
					if '/' in childNode.SongFileName:
						# Get filename
						path = MainForm.BuildPath + '/pf/sound/strm/' + childNode.SongFileName.split('/')[0]
						directory = Directory.CreateDirectory(path)
						brstmFile = getFileByName(childNode.SongFileName.split('/')[1] + ".brstm", directory)
						if brstmFile:
							writeLog("Extracting file " + brstmFile.FullName)
							exportPath = createDirectory(AppPath + '/temp/' + exportFolder)
							copyFile(brstmFile.FullName, exportPath)
							success = True
				BrawlAPI.ForceCloseFile()
		writeLog("Finished extracting theme")
		return success

# Read a code macro
def readCodeMacro(id, macroName, position=0, preFindText="", filePath='/ProjectM/CloneEngine.asm', returnPosition=0):
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
			if foundValues and len(foundValues) >= returnPosition:
				return foundValues[returnPosition].strip()
			else:
				return ""

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
		kirbyHatId = readCodeMacro(fighterId, 'HatFloatFix', 0, filePath='/Extras/KirbyHatEX.asm', returnPosition=1)
		if kirbyHatId:
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

# Extract credits song
def extractCreditsSong(slotId):
		writeLog("Extracting credits song for slot ID " + str(slotId))
		songFound = False
		songId = updateCreditsCode(slotId, "", read=True)
		if songId:
			songFound = extractSong(int(songId, 16), 'Credits', 'Credits', 'CreditsTheme')
		if songFound:
			return 0
		else:
			return songId

# Get throw release points
def readThrowRelease(fighterId):
		writeLog("Reading throw release point for ID " + str(fighterId))
		returnValues = []
		if File.Exists(MainForm.BuildPath + '/Source/ProjectM/Modifier/ThrowRelease.asm'):
			# Read ThrowRelease.asm
			writeLog("Reading ThrowRelease.asm")
			fileText = File.ReadAllLines(MainForm.BuildPath + "/Source/ProjectM/Modifier/ThrowRelease.asm")
			i = 0
			tableStart = 0
			while i < len(fileText):
				line = fileText[i]
				if line.StartsWith("ThrowReleaseTable"):
					writeLog("Found throw release table at line " + str(i))
					tableStart = i + 2
				if tableStart > 0 and i == tableStart + int(fighterId, 16):
					writeLog("Found matching EX fighter at position " + str(i))
					value = line.split('|')[0]
					returnValues.append(value.split(',')[0].strip())
					returnValues.append(value.split(',')[1].strip())
					break
				i += 1
		writeLog("Finished reading throw release point")
		return returnValues

# Get trophy settings
def extractTrophy(slotId):
		trophyInfo = getSlotTrophyInfo(slotId)
		if trophyInfo and len(trophyInfo) > 1:
			if trophyInfo[1] != "":
				trophyId = int(trophyInfo[1].replace('0x', ''), 16)
			else:
				trophyId = ""
		else:
			trophyId = ""
		if trophyId:
			trophySettings = TrophySettings()
			trophySettingsWrite = False
			writeLog("Extracting trophy with ID " + str(trophyId))
			nameIndex = -1
			gameIndex = -1
			descriptionIndex = -1
			brresName = ""
			# Extract from trophy list
			if File.Exists(MainForm.BuildPath + '/pf/system/common3.pac'):
				fileOpened = openFile(MainForm.BuildPath + '/pf/system/common3.pac', False)
				if fileOpened:
					tyDataNode = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
					tyDataList = getChildByName(tyDataNode, "tyDataList")
					for trophyNode in tyDataList.Children:
						if trophyNode.Id == trophyId:
							nameIndex = trophyNode.NameIndex
							gameIndex = trophyNode.GameIndex
							descriptionIndex = trophyNode.DescriptionIndex
							brresName = trophyNode.BRRES
							trophySettings.gameIcon1 = trophyNode.GameIcon1
							trophySettings.gameIcon2 = trophyNode.GameIcon2
							trophySettings.seriesIndex = trophyNode.SeriesIndex
							trophySettingsWrite = True
							break
					BrawlAPI.ForceCloseFile()
			# Extract name and game names
			writeLog("Extracting trophy name and game names")
			if File.Exists(MainForm.BuildPath + '/pf/toy/fig/ty_fig_name_list.msbin'):
				fileOpened = openFile(MainForm.BuildPath + '/pf/toy/fig/ty_fig_name_list.msbin', False)
				if fileOpened:
					createDirectory(AppPath + '/temp')
					BrawlAPI.RootNode.Export(AppPath + '/temp/ty_fig_name_list.txt')
					fileText = File.ReadAllLines(AppPath + '/temp/ty_fig_name_list.txt')
					i = 0
					for line in fileText:
						if nameIndex != -1 and i == nameIndex:
							trophySettings.trophyName = line
							trophySettingsWrite = True
						if gameIndex != -1 and i == gameIndex:
							gameNames = line.split('<br/>')
							if gameNames:
								trophySettings.gameName1 = gameNames[0]
								trophySettingsWrite = True
								if len(gameNames) > 1:
									trophySettings.gameName2 = gameNames[1]
									trophySettingsWrite = True
						i += 1
					File.Delete(AppPath + '/temp/ty_fig_name_list.txt')
					BrawlAPI.ForceCloseFile()
			# Extract description
			writeLog("Extracting trophy description")
			createDirectory(AppPath + '/temp')
			if File.Exists(MainForm.BuildPath + '/pf/toy/fig/ty_fig_ext_list.msbin'):
				fileOpened = openFile(MainForm.BuildPath + '/pf/toy/fig/ty_fig_ext_list.msbin', False)
				if fileOpened:
					BrawlAPI.RootNode.Export(AppPath + '/temp/ty_fig_ext_list.txt')
					fileText = File.ReadAllLines(AppPath + '/temp/ty_fig_ext_list.txt')
					newFileText = []
					i = 0
					for line in fileText:
						if descriptionIndex != -1 and i == descriptionIndex:
							trophySettings.description = line.replace('<color=E6E6E6FF>', '').replace('</end>', '')
							trophySettingsWrite = True
						i += 1
					File.Delete(AppPath + '/temp/ty_fig_ext_list.txt')
					BrawlAPI.ForceCloseFile()
			# Extract thumbnail
			writeLog("Extracting trophy thumbnail")
			if File.Exists(MainForm.BuildPath + '/pf/menu/collection/Figure.brres'):
				fileOpened = openFile(MainForm.BuildPath + '/pf/menu/collection/Figure.brres', False)
				if fileOpened:
					texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
					if texFolder:
						node = getChildByName(texFolder, "MenCollDisply01." + str(trophyId))
						if node:
							createDirectory(AppPath + '/temp/Trophy')
							node.Export(AppPath + '/temp/Trophy/' + node.Name + '.png')
					BrawlAPI.ForceCloseFile()
			# Extract model
			writeLog("Extracting trophy model")
			if brresName:
				if File.Exists(MainForm.BuildPath + '/pf/toy/fig/' + brresName + '.brres'):
					createDirectory(AppPath + '/temp/Trophy')
					copyFile(MainForm.BuildPath + '/pf/toy/fig/' + brresName + '.brres', AppPath + '/temp/Trophy')
			# Write settings
			if trophySettingsWrite:
				attrs = vars(trophySettings)
				createDirectory(AppPath + '/temp/Trophy')
				File.WriteAllText(AppPath + '/temp/Trophy/TrophySettings.txt', '\n'.join("%s = %s" % item for item in attrs.items()))
			writeLog("Finished extracting trophy")
		return trophyId

#endregion

#region INSTALLER FUNCTIONS
# Installer functions that check for and remove existing elements before adding

# Install CSPs
def installCSPs(cosmeticId, directory, rspLoading):
		removeCSPs(cosmeticId)
		importCSPs(cosmeticId, directory, rspLoading)

# Install stock icons
def installStockIcons(cosmeticId, directory, tex0BresName, pat0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true", firstOnly=False):
		removeStockIcons(cosmeticId, tex0BresName, pat0BresName, rootName, filePath, fiftyCC)
		importStockIcons(cosmeticId, directory, tex0BresName, pat0BresName, rootName, filePath, fiftyCC, firstOnly)

# Install BPs
def installBPs(cosmeticId, images, fiftyCC="true"):
		deleteBPs(cosmeticId)
		createBPs(cosmeticId, images, fiftyCC)

# Install CSS icon
def installCSSIcon(cosmeticId, iconImagePath, format):
		removeCSSIcon(cosmeticId)
		importCSSIcon(cosmeticId, iconImagePath, format)

# Install CSS icon SSE
def installCssIconSSE(cosmeticId, iconImagePath, nameImagePath):
		removeCSSIconSSE(cosmeticId)
		importCSSIconSSE(cosmeticId, iconImagePath, nameImagePath)

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

# Install trophy
def installTrophy(slotId, brresPath, thumbnailPath, fighterName, trophySettings, installToSse):
		trophyIdHex = getSlotTrophyInfo(slotId)[1]
		if trophyIdHex:
			trophyIdInt = int(trophyIdHex.replace('0x', ''), 16)
		else:
			trophyIdInt = -1
		if File.Exists(brresPath):
			bresName = getFileInfo(brresPath).Name.replace('.brres','')
			deleteTrophyModel(bresName)
			importTrophyModel(brresPath)
			returnedTrophyId = addTrophy(bresName, trophySettings.gameIcon1, trophySettings.gameIcon2, trophySettings.trophyName, trophySettings.gameName1, trophySettings.gameName2, trophySettings.description, trophySettings.seriesIndex, trophyIdInt)
			if File.Exists(thumbnailPath):
				removeTrophyThumbnail(returnedTrophyId)
				importTrophyThumbnail(thumbnailPath, returnedTrophyId)
			updateTrophyCode(slotId, hexId(returnedTrophyId), fighterName)
		if installToSse == "true":
			updateTrophySSE(slotId, hexId(returnedTrophyId).replace('0x', ''))

# Assign trophy ID for existing trophies
def assignTrophy(slotId, trophyId, fighterName, installToSse):
		writeLog("Assigning trophy ID " + str(trophyId) + " to slot ID " + str(slotId))
		updateTrophyCode(slotId, hexId(trophyId), fighterName)
		if installToSse == "true":
			updateTrophySSE(slotId, hexId(trophyId).replace('0x', ''))
		writeLog("Finished assigning trophy ID")

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
		fighterId = ""
		slotConfigId = ""
		cosmeticConfigId = ""
		cssSlotConfigId = ""
		if fighterConfig:
			writeLog("Retrieving information from " + fighterConfig)
			BrawlAPI.OpenFile(fighterConfig)
			fighterName = BrawlAPI.RootNode.FighterName
			soundbankId = BrawlAPI.RootNode.SoundBank
			fighterId = getFileInfo(fighterConfig).Name.replace('Fighter','').replace('.dat','')
			BrawlAPI.ForceCloseFile()
		if cosmeticConfig:
			writeLog("Retrieving information from " + cosmeticConfig)
			BrawlAPI.OpenFile(cosmeticConfig)
			cosmeticId = BrawlAPI.RootNode.CosmeticID
			# Add 1 because the franchise icon ID in the config is 1 less
			franchiseIconId = BrawlAPI.RootNode.FranchiseIconID + 1
			characterName = BrawlAPI.RootNode.CharacterName
			cosmeticConfigId = getFileInfo(cosmeticConfig).Name.replace('Cosmetic','').replace('.dat','')
			BrawlAPI.ForceCloseFile()
		if slotConfig:
			writeLog("Retrieving information from " + slotConfig)
			BrawlAPI.OpenFile(slotConfig)
			songId = BrawlAPI.RootNode.VictoryTheme
			slotConfigId = getFileInfo(slotConfig).Name.replace('Slot','').replace('.dat','')
			BrawlAPI.ForceCloseFile()
		writeLog("Get fighter info finished")
		return FighterInfo(fighterId, fighterName, cosmeticId, franchiseIconId, soundbankId, songId, characterName, slotConfigId, cosmeticConfigId, cssSlotConfigId)

# From a fighter config, get fighter info
def getfighterConfigInfo(fighterConfig):
		fighterName = ""
		soundbankId = 0
		fighterId = ""
		if File.Exists(fighterConfig):
			BrawlAPI.OpenFile(fighterConfig)
			fighterName = BrawlAPI.RootNode.FighterName
			soundbankId = BrawlAPI.RootNode.SoundBank
			fighterId = getFileInfo(fighterConfig).Name.replace('Fighter','').replace('.dat','')
			BrawlAPI.ForceCloseFile()
		return FighterConfigInfo(fighterName, fighterId, soundbankId)

# From a cosmetic config, get cosmetic info
def getCosmeticConfigInfo(cosmeticConfig):
		writeLog("Getting cosmetic config info for path " + cosmeticConfig)
		cosmeticId = 0
		franchiseIconId = 0
		characterName = ""
		redirect = False
		redirectId = 0
		cosmeticConfigId = ""
		configFile = MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig/Cosmetic' + getFileInfo(cosmeticConfig).Name.replace('Fighter','').replace('Cosmetic','')
		if File.Exists(configFile):
			writeLog("File " + configFile + "found")
			BrawlAPI.OpenFile(configFile)
			cosmeticId = BrawlAPI.RootNode.CosmeticID
			# Add 1 because the franchise icon ID in the config is 1 less
			franchiseIconId = BrawlAPI.RootNode.FranchiseIconID + 1
			characterName = BrawlAPI.RootNode.CharacterName
			redirect = BrawlAPI.RootNode.HasSecondary
			redirectId = BrawlAPI.RootNode.CharSlot1
			cosmeticConfigId = getFileInfo(configFile).Name.replace('Cosmetic','').replace('.dat','')
			BrawlAPI.ForceCloseFile()
		writeLog("Finished getting cosmetic config info")
		return CosmeticConfigInfo(cosmeticId, cosmeticConfigId, franchiseIconId, characterName, redirect, redirectId)

# From a CSSSlot config, get CSSSlot config info
def getCssSlotConfigInfo(cssSlotConfig):
		writeLog("Getting CSSSlot config info for path " + cssSlotConfig)
		redirect = False
		redirectId = 0
		cssSlotConfigId = ""
		configFile = MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/CSSSlot' + getFileInfo(cssSlotConfig).Name.replace('Fighter','').replace('CSSSlot','')
		if File.Exists(configFile):
			writeLog("File " + configFile + "found")
			BrawlAPI.OpenFile(configFile)
			redirect = BrawlAPI.RootNode.SetPrimarySecondary
			redirectId = BrawlAPI.RootNode.CharSlot1
			cssSlotConfigId = getFileInfo(configFile).Name.replace('CSSSlot','').replace('.dat','')
			BrawlAPI.ForceCloseFile()
		writeLog("Finished getting CSSSlot config info")
		return CssSlotConfigInfo(cssSlotConfigId, redirect, redirectId)

# From a slot config, get slot info
def getSlotConfigInfo(slotConfig):
		writeLog("Getting slot config info for path " + slotConfig)
		songId = 0
		redirect = False
		redirectId = 0
		slotConfigId = ""
		configFile = MainForm.BuildPath + '/pf/BrawlEx/SlotConfig/Slot' + getFileInfo(slotConfig).Name.replace('Fighter','').replace('Slot','')
		if File.Exists(configFile):
			writeLog("File " + configFile + "found")
			BrawlAPI.OpenFile(configFile)
			songId = BrawlAPI.RootNode.VictoryTheme
			redirect = BrawlAPI.RootNode.SetSlot
			redirectId = hexId(BrawlAPI.RootNode.CharSlot1)
			slotConfigId = getFileInfo(configFile).Name.replace('Slot','').replace('.dat','')
			BrawlAPI.ForceCloseFile()
		writeLog("Finished getting slot config info")
		return SlotConfigInfo(slotConfigId, songId, redirect, redirectId)

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

# Recursively search for a specific file
def getFileRecursive(searchString, preferredFileName):
	returnFile = ""
	if Directory.Exists(MainForm.BuildPath):
		files = Directory.GetFiles(MainForm.BuildPath, searchString, SearchOption.AllDirectories)
		if len(files) > 0:
			for file in files:
				if getFileInfo(file).Name == preferredFileName:
					returnFile = file
			if not returnFile:
				returnFile = files[0]
	return returnFile

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

# Copy list of ImportedFile objects into build
def importFiles(fileList):
		writeLog("Importing files into build")
		for file in fileList:
			if File.Exists(file.filePath):
				copyFile(file.filePath, file.outputPath)
		writeLog("Finished importing files")

# Increment index on BP names within specific range
def incrementBPNames(cosmeticId, startIndex, endIndex=-1, increment=1, fiftyCC="true"):
		writeLog("Adjusting index of BPs for cosmetic ID " + str(cosmeticId))
		# For 50 costume code, we must multiply the cosmetic ID by 50
		directory = MainForm.BuildPath + '/pf/info/portrite'
		startId = (cosmeticId * 50) + startIndex if fiftyCC == "true" else int(str(cosmeticId) + str(startIndex))
		endId = -1
		if endIndex != -1:
			endId = (cosmeticId * 50) + endIndex if fiftyCC == "true" else int(str(cosmeticId) + str(endIndex))
			writeLog("End ID " + str(endId))
		else:
			# If no endIndex is provided, we will search through and find the last file in the character range
			end = (cosmeticId * (50 if fiftyCC=="true" else 1)) + 50 if fiftyCC=="true" else 10
			i = startId
			while i < end:
				writeLog("On ID " + str(i))
				if File.Exists(directory + '/InfFace' + addLeadingZeros(str(i), 4 if fiftyCC == "true" else 3) + '.brres'):
					endId = i + 1
				i += 1
		if endId == -1:
			endId = startId + increment
		# We work backwards or forwards depending on if we are incrementing or decrementing - this prevents us from overwriting files before they can be renamed
		if increment > -1:
			id = endId
			while id >= startId:
				path = directory + '/InfFace' + addLeadingZeros(str(id), 4 if fiftyCC == "true" else 3) + '.brres'
				# If the file exists already, make a backup (probably will never hit this because of the delete coming first on install but just in case)
				createBackup(path)
				if File.Exists(path):
					copyRenameFile(path, 'InfFace' + addLeadingZeros(str(id + increment), 4 if fiftyCC == "true" else 3) + '.brres', directory)
					File.Delete(path)
				id -= 1
		else:
			id = startId
			while id < endId:
				path = directory + '/InfFace' + addLeadingZeros(str(id), 4 if fiftyCC == "true" else 3) + '.brres'
				# If the file exists already, make a backup (probably will never hit this because of the delete coming first on install but just in case)
				createBackup(path)
				if File.Exists(path):
					copyRenameFile(path, 'InfFace' + addLeadingZeros(str(id + increment), 4 if fiftyCC == "true" else 3) + '.brres', directory)
					File.Delete(path)
				id += 1
		writeLog("Finished adjusting BP indexes")

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

# Check if a config with the specified ID exists
def searchForExConfig(configName, id):
		writeLog("Searching for config " + configName + " with ID " + str(id))
		id = id.replace('0x', '')
		if Directory.Exists(MainForm.BuildPath + '/pf/BrawlEx/' + configName + 'Config'):
			for file in Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/' + configName + 'Config', "*.dat"):
				foundId = getFileInfo(file).Name.replace(configName, '').replace('.dat', '')
				if foundId == id:
					writeLog("Found config with ID " + str(id))
					return True
		writeLog("No ID found")
		return False

# Check if any configs at all with specified ID exist
def searchAllExConfigs(id):
		if searchForExConfig('Fighter', id):
			return True
		if searchForExConfig('Cosmetic', id):
			return True
		if searchForExConfig('CSSSlot', id):
			return True
		if searchForExConfig('Slot', id):
			return True
		return False

# Get info for all fighters in a build
def getAllFighterInfo():
		try:
			# Set up progressbar
			progressCounter = 0
			totalFiles = len(Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig')) + len(Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig')) + len(Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig')) + len(Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig'))
			progressBar = ProgressWindow(MainForm.Instance, "Gathering Ex configs...", "Gathering Ex configs", False)
			progressBar.Begin(0, totalFiles, progressCounter)

			# Get fighter config info
			fighterConfigInfo = []
			for file in Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig'):
				fighterConfigInfo.append(getfighterConfigInfo(file))
				progressCounter += 1
				progressBar.Update(progressCounter)
			# Get slot config info
			slotConfigInfo = []
			for file in Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig'):
				slotConfigInfo.append(getSlotConfigInfo(file))
				progressCounter += 1
				progressBar.Update(progressCounter)
			# Get cosmetic config info
			cosmeticConfigInfo = []
			for file in  Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig'):
				cosmeticConfigInfo.append(getCosmeticConfigInfo(file))
				progressCounter += 1
				progressBar.Update(progressCounter)
			# Get CSS slot config info
			cssSlotConfigInfo = []
			for file in Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig'):
				cssSlotConfigInfo.append(getCssSlotConfigInfo(file))
				progressCounter += 1
				progressBar.Update(progressCounter)
			progressBar.Finish()

			# Set up progressbar
			progressCounter = 0
			progressBar = ProgressWindow(MainForm.Instance, "Joining Ex configs...", "Joining Ex configs", False)
			progressBar.Begin(0, len(fighterConfigInfo), progressCounter)

			# Starting with fighter config, find matching configs and add them to list
			exConfigs = []
			for fighterConfig in fighterConfigInfo:
				matchFound = False
				fighterConfigPath = MainForm.BuildPath + '/pf/BrawlEx/FighterConfig/Fighter' + fighterConfig.fighterId + '.dat'
				info = []
				# Search for matching slot configs
				for slotConfig in slotConfigInfo:
					# Check for redirects
					if slotConfig.redirect and hexId(slotConfig.redirectId) == '0x' + fighterConfig.fighterId:
						info.append(fighterConfig)
						info.append(slotConfig)
						matchFound = True
						break
				# If no redirect is found, try just using the fighter config's actual ID
				if not matchFound:
					info.append(fighterConfig)
					info.append(getSlotConfigInfo(fighterConfigPath))
				# Search for matching cosmetic configs
				matchFound = False
				for cosmeticConfig in cosmeticConfigInfo:
					if cosmeticConfig.redirect and hexId(cosmeticConfig.redirectId) == '0x' + info[1].slotConfigId:
						info.append(cosmeticConfig)
						matchFound = True
						break
				if not matchFound:
					info.append(getCosmeticConfigInfo(fighterConfigPath))
				# Search for matching CSS slot configs
				matchFound = False
				for cssSlotConfig in cssSlotConfigInfo:
					if cssSlotConfig.redirect and hexId(cssSlotConfig.redirectId) == '0x' + info[1].slotConfigId:
						info.append(cssSlotConfig)
						matchFound = True
						break
				if not matchFound:
					info.append(getCssSlotConfigInfo(fighterConfigPath))
				newFighterInfo = FighterInfo(info[0].fighterId, info[0].fighterName, info[2].cosmeticId, info[2].franchiseIconId, info[0].soundbankId, info[1].songId, info[2].characterName, info[1].slotConfigId, info[2].cosmeticConfigId, info[3].cssSlotConfigId)
				exConfigs.append(newFighterInfo)
				progressCounter += 1
				progressBar.Update(progressCounter)
			progressBar.Finish()
			return exConfigs
		except Exception as e:
			if 'progressBar' in locals():
				progressBar.Finish()
			raise e

#endregion GENERAL FUNCTIONS

#region SETUP FUNCTIONS
def getSettings():
		writeLog("Reading settings file")
		fileText = File.ReadAllLines(MainForm.BuildPath + '/settings.ini')
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
		settings.gfxChangeExe = readValueFromKey(fileText, "gfxChangeExe")
		settings.installBPNames = readValueFromKey(fileText, "installBPNames")
		settings.installSingleplayerCosmetics = readValueFromKey(fileText, "installSingleplayerCosmetics")
		settings.installToSse = readValueFromKey(fileText, "installToSse")
		settings.sseUnlockStage = readValueFromKey(fileText, "sseUnlockStage")
		settings.installTrophies = readValueFromKey(fileText, "installTrophies")
		settings.customStageLists = readValueFromKey(fileText, "customStageLists")
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
				if jigglypuffSfxIds[0]:
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
			fighterSettings.trophyId = hexId(readValueFromKey(fileText, "trophyId"))
		writeLog("Reading fighter settings complete")
		return fighterSettings

def getTrophySettings():
	writeLog("Reading trophy settings file")
	trophySettings = TrophySettings()
	if File.Exists(AppPath + '/temp/Trophy/TrophySettings.txt'):
		fileText = File.ReadAllLines(AppPath + '/temp/Trophy/TrophySettings.txt')
		trophySettings.trophyName = readValueFromKey(fileText, "trophyName")
		trophySettings.description = readValueFromKey(fileText, "description")
		trophySettings.gameIcon1 = readValueFromKey(fileText, "gameIcon1")
		if trophySettings.gameIcon1:
			trophySettings.gameIcon1 = int(trophySettings.gameIcon1)
		else:
			trophySettings.gameIcon1 = 0
		trophySettings.gameIcon2 = readValueFromKey(fileText, "gameIcon2")
		if trophySettings.gameIcon2:
			trophySettings.gameIcon2 = int(trophySettings.gameIcon2)
		else:
			trophySettings.gameIcon2 = 0
		trophySettings.gameName1 = readValueFromKey(fileText, "gameName1")
		trophySettings.gameName2 = readValueFromKey(fileText, "gameName2")
		trophySettings.seriesIndex = readValueFromKey(fileText, "seriesIndex")
		if trophySettings.seriesIndex:
			trophySettings.seriesIndex = int(trophySettings.seriesIndex)
		else:
			trophySettings.seriesIndex = 0
	writeLog("Finished reading trophy settings file")
	return trophySettings
		
# Check for matching color smash groups in stock icons
def checkStockIcons(cosmeticId, tex0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true"):
		writeLog("Checking stock icons at cosmetic ID " + str(cosmeticId))
		fileOpened = openFile(MainForm.BuildPath + filePath, False)
		startId = (cosmeticId * 50) + 1 if fiftyCC == "true" else int(str(cosmeticId) + str(1))
		endId = (cosmeticId * (50 if fiftyCC=="true" else 1)) + 50 if fiftyCC=="true" else 10
		positions = []
		if fileOpened:
			rootNode = BrawlAPI.RootNode
			if rootName != "":
				rootNode = getChildByName(BrawlAPI.RootNode, rootName)
			if tex0BresName != "":
				node = getChildByName(rootNode, tex0BresName)
			else:
				node = rootNode
			texFolder = getChildByName(node, "Textures(NW4R)")
			costumeSet = True
			i = startId
			j = 0
			while i < endId:
				node = getChildByName(texFolder, "InfStc." + addLeadingZeros(str(i), 4 if fiftyCC == "true" else 3))
				if node:
					if costumeSet:
						positions.append(j)
						costumeSet = True
					if node.SharesData:
						costumeSet = False
					else:
						costumeSet = True
				i += 1
				j += 1
			BrawlAPI.ForceCloseFile()
		writeLog("Finished checking stock icons")
		return positions

# Check for conflicts on ex config IDs
def idConflictCheck(fighterId, cosmeticId, slotConfigId, cosmeticConfigId, cssSlotConfigId):
		# Standardize the formats for all the IDs
		if fighterId:
			fighterId = hexId(fighterId).replace('0x', '').upper()
		if cosmeticId:
			cosmeticId = int(hexId(cosmeticId).replace('0x', ''), 16)
		if slotConfigId:
			slotConfigId = hexId(slotConfigId).replace('0x', '').upper()
		if cosmeticConfigId:
			cosmeticConfigId = hexId(cosmeticConfigId).replace('0x', '').upper()
		if cssSlotConfigId:
			cssSlotConfigId = hexId(cssSlotConfigId).replace('0x', '').upper()
		# If slot config ID wasn't passed, check all ex configs for a conflict, otherwise just check fighter configs
		if not slotConfigId:
			existingFighterConfig = searchAllExConfigs(fighterId)
		else:
			existingFighterConfig = searchForExConfig('Fighter', fighterId)
		# If any configs are blank, default to fighter ID
		if not slotConfigId:
			slotConfigId = fighterId
		if not cosmeticConfigId:
			cosmeticConfigId = fighterId
		if not cssSlotConfigId:
			cssSlotConfigId = fighterId
		returnText = "The following IDs are already in use:\n"
		conflictFound = False
		# Check fighter config
		if existingFighterConfig:
			conflictFound = True
			returnText += "\nFighter ID"
		# Check cosmetic ID
		if cosmeticId:
			existingFile = Directory.GetFiles(MainForm.BuildPath + '/pf/menu/common/char_bust_tex', "MenSelchrFaceB" + addLeadingZeros(str(cosmeticId), 2) + "0.brres")
			if existingFile:
				conflictFound = True
				returnText += "\nCosmetic ID"
		# Check cosmetic config
		if cosmeticConfigId != fighterId:
			existingCosmeticConfig = searchForExConfig('Cosmetic', cosmeticConfigId)
			if existingCosmeticConfig:
				conflictFound = True
				returnText += "\nCosmetic Config ID"
		# Check slot config
		if slotConfigId != fighterId:
			existingSlotConfig = searchForExConfig('Slot', slotConfigId)
			if existingSlotConfig:
				conflictFound = True
				returnText += "\nSlot Config ID"
		# Check CSS slot config
		if cssSlotConfigId != fighterId:
			existingCssSlotConfig = searchForExConfig('CSSSlot', cssSlotConfigId)
			if existingCssSlotConfig:
				conflictFound = True
				returnText += "\nCSS Slot Config ID"
		if conflictFound:
			return returnText
		else:
			return ""

def initialSetup():
		if File.Exists(RESOURCE_PATH + '/settings.ini'):
			copyFile(RESOURCE_PATH + '/settings.ini', MainForm.BuildPath)
			File.Delete(RESOURCE_PATH + '/settings.ini')
			settings = getSettings()
			return settings
		if File.Exists(MainForm.BuildPath + '/settings.ini'):
			settings = getSettings()
			return settings
		else:
			BrawlAPI.ShowMessage("Settings were not found. Please open the build settings menu (Plugins > BrawlInstaller Plugins > Settings) and configure your settings to continue.", "No Settings Found")
			return None

#endregion SETUP FUNCTIONS

#region CLASSES

class Settings:
		rspLoading = "false"
		cssIconStyle = "P+"
		bpStyle = "vBrawl"
		portraitNameStyle = "PM"
		installPortraitNames = "false"
		franchiseIconSizeCSS = "128"
		installStocksToCSS = "true"
		installStocksToInfo = "true"
		installStockIconsToResult = "true"
		installStocksToStockFaceTex = "true"
		installStocksToSSS = "false"
		fiftyCostumeCode = "true"
		installKirbyHats = "true"
		defaultKirbyHat = "0x21"
		kirbyHatExe = getFileRecursive("lavaKirbyHatManager*.exe", "lavaKirbyHatManager - OFFLINE.exe")
		assemblyFunctionsExe = getFileRecursive("PowerPC Assembly Functions*.exe", "PowerPC Assembly Functions (Dolphin).exe")
		sawndReplaceExe = getFileRecursive("lavaSawndIDReplaceAssist*.exe", "lavaSawndIDReplaceAssist.exe")
		sfxChangeExe = getFileRecursive("sfxchange*.exe", "sfxchange.exe")
		soundbankStyle = "hex"
		addSevenToSoundbankIds = "true"
		addSevenToSoundbankName = "false"
		installVictoryThemes = "true"
		gfxChangeExe = getFileRecursive("gfxchange*.exe", "gfxchange.exe")
		installBPNames = "false"
		installSingleplayerCosmetics = "false"
		installToSse = "false"
		sseUnlockStage = "end"
		installTrophies = "false"
		customStageLists = ""

class FighterSettings:
		lucarioBoneId = ""
		lucarioKirbyEffectId = ""
		jigglypuffBoneId = ""
		jigglypuffEFLSId = ""
		jigglypuffSfxIds = []
		bowserBoneId = ""
		throwReleasePoint = []
		creditsThemeId = ""
		trophyId = ""

class TrophySettings:
		trophyName = ""
		description = ""
		gameIcon1 = 0
		gameIcon2 = 0
		gameName1 = ""
		gameName2 = ""
		seriesIndex = 0

class FighterInfo:
		def __init__(self, fighterId, fighterName, cosmeticId, franchiseIconId, soundbankId, songId, characterName, slotConfigId, cosmeticConfigId, cssSlotConfigId):
			self.fighterId = fighterId
			self.fighterName = fighterName
			self.cosmeticId = cosmeticId
			self.franchiseIconId = franchiseIconId
			self.soundbankId = soundbankId
			self.songId = songId
			self.characterName = characterName
			self.slotConfigId = slotConfigId
			self.cosmeticConfigId = cosmeticConfigId
			self.cssSlotConfigId = cssSlotConfigId

class FighterConfigInfo:
		def __init__(self, fighterName, fighterId, soundbankId):
			self.fighterName = fighterName
			self.fighterId = fighterId
			self.soundbankId = soundbankId

class CosmeticConfigInfo:
		def __init__(self, cosmeticId, cosmeticConfigId, franchiseIconId, characterName, redirect, redirectId):
			self.cosmeticId = cosmeticId
			self.cosmeticConfigId = cosmeticConfigId
			self.franchiseIconId = franchiseIconId
			self.characterName = characterName
			self.redirect = redirect
			self.redirectId = redirectId

class CssSlotConfigInfo:
		def __init__(self, cssSlotConfigId, redirect, redirectId):
			self.cssSlotConfigId = cssSlotConfigId
			self.redirect = redirect
			self.redirectId = redirectId

class SlotConfigInfo:
		def __init__(self, slotConfigId, songId, redirect, redirectId):
			self.slotConfigId = slotConfigId
			self.songId = songId
			self.redirect = redirect
			self.redirectId = redirectId

class StageSlot:
		def __init__(self, slotId, stageId, cosmeticId, fullId, name):
			self.slotId = slotId
			self.stageId = stageId
			self.cosmeticId = cosmeticId
			self.fullId = fullId
			self.name = name

class StageCosmetics:
		def __init__(self, stageIcon, stagePreview, stageName, franchiseIcon, gameLogo, altName, stageNameList=None, franchiseIconList=None, gameLogoList=None):
			self.stageIcon = stageIcon
			self.stagePreview = stagePreview
			self.stageName = stageName
			self.franchiseIcon = franchiseIcon
			self.gameLogo = gameLogo
			self.altName = altName
			self.stageNameList = stageNameList
			self.franchiseIconList = franchiseIconList
			self.gameLogoList = gameLogoList

class StageParams:
		def __init__(self, aslEntry, pacName, tracklist, module, soundBank, effectBank, originalName, pacFile="", moduleFile="", tracklistFile="", soundBankFile="", paramFile="", originalPacName="", originalModule="", originalTracklist="", originalSoundBank=""):
			self.aslEntry = aslEntry
			self.pacName = pacName
			self.tracklist = tracklist
			self.module = module
			self.soundBank = soundBank
			self.effectBank = effectBank
			self.originalName = originalName
			self.pacFile = pacFile
			self.moduleFile = moduleFile
			self.tracklistFile = tracklistFile
			self.soundBankFile = soundBankFile
			self.paramFile = paramFile
			self.originalPacName = originalPacName
			self.originalModule = originalModule
			self.originalTracklist = originalTracklist
			self.originalSoundBank = originalSoundBank

class ImageNode:
		def __init__(self, name, image):
			self.name = name
			self.image = image

class ImportedFile:
		def __init__(self, filePath, outputPath):
			self.filePath = filePath
			self.outputPath = outputPath

class Song:
		def __init__(self, songNode, name, brstmFile="", originalBrstm=""):
			self.songNode = songNode
			self.brstmFile = brstmFile
			self.originalBrstm = originalBrstm

#endregion CLASSES

#region COLOR PROMPT

class ColorPrompt(Form):

	def __init__(self, image):
		# Form parameters
		self.Text = 'Select Color'
		self.StartPosition = FormStartPosition.CenterParent
		self.ShowIcon = False
		self.AutoSize = True
		self.MinimumSize = Size(250,250)
		self.FormBorderStyle = FormBorderStyle.FixedSingle
		self.AutoSizeMode = AutoSizeMode.GrowAndShrink

		# Form vars
		self.selectedColor = 0

		# Picturebox
		pictureBox = PictureBox()
		pictureBox.Dock = DockStyle.Top
		pictureBox.SizeMode = PictureBoxSizeMode.CenterImage
		pictureBox.Image = image
		pictureBox.Size = Size(128, 160)

		# Combobox
		self.comboBoxGroup = GroupBox()
		self.comboBoxGroup.Height = 60
		self.comboBoxGroup.Dock = DockStyle.Bottom
		self.comboBoxGroup.TabIndex = 1

		comboBoxPanel = Panel()
		comboBoxPanel.Location = Point(16, 16)
		comboBoxPanel.TabIndex = 1
		self.comboBox = ComboBox()
		self.comboBox.Dock = DockStyle.Fill
		self.comboBox.DropDownStyle = ComboBoxStyle.DropDownList
		self.comboBox.DisplayMember = "Key"
		self.comboBox.ValueMember = "Value"
		for object in COSTUME_COLOR:
			self.comboBox.Items.Add(object)

		comboBoxPanel.Controls.Add(self.comboBox)

		self.comboBoxGroup.Controls.Add(comboBoxPanel)

		# Confirm button
		confirmButton = Button()
		confirmButton.Text = "Set Color"
		confirmButton.Dock = DockStyle.Bottom
		confirmButton.Click += self.confirmButtonPressed

		self.Controls.Add(self.comboBoxGroup)
		self.Controls.Add(confirmButton)
		self.Controls.Add(pictureBox)

	def confirmButtonPressed(self, sender, args):
		if self.comboBox.SelectedItem:
			self.selectedColor = COSTUME_COLOR[self.comboBox.SelectedItem]
		else:
			self.selectedColor = 11
		self.DialogResult = DialogResult.OK
		self.Close()

#endregion

#region STAGES

# Get list of stages
def getStageList(path="/Source/Project+/StageFiles.asm"):
		writeLog("Reading stage list for path " + path)
		fileText = File.ReadAllLines(MainForm.BuildPath + path)
		tables = []
		tableStarts = []
		# Find the tables
		i = 0
		while i < len(fileText):
			line = fileText[i]
			if line.StartsWith("TABLE_") and "STAGES" not in line:
				writeLog("Found stage table at line " + str(i))
				tableStarts.append(i + 2)
			i += 1
		# Get all values in each table
		for tableStart in tableStarts:
			i = tableStart
			tableValues = []
			while i < len(fileText):
				line = fileText[i]
				if len(line) <= 0 or line.startswith('TABLE'):
					break
				splitLine = list(filter(None, line.replace('|','').split('#')[0].strip().split(',')))
				for item in splitLine:
					tableValues.append(item.strip())
				i += 1
			tables.append(tableValues)
		writeLog("Finished getting stage list")
		return tables

# Write new stage list
def updateStageList(stageList, path="/Source/Project+/StageFiles.asm"):
		writeLog("Updating stage list")
		file = MainForm.BuildPath + path
		createBackup(file)
		newText = []
		stopWriting = False
		# Create tables
		tables = []
		for item in stageList:
			if item.name.startswith("|| PAGE "):
				tables.append([])
		# Populate tables
		i = -1
		for item in stageList:
			if item.name.startswith("|| PAGE "):
				i += 1
				continue
			tables[i].append(item)
		fileText = File.ReadAllLines(file)
		for line in fileText:
			if line.startswith(".GOTO->SkipStageTables"):
				newText.append(line + "\n\n")
				stopWriting = True
				i = 0
				for table in tables:
					i += 1
					newText.append("\nTABLE_" + str(i) + ":")
					if len(table) > 0:
						newText.append("\tbyte[" + str(len(table)) + "] |")
					j = 0
					for slot in table:
						newText.append(slot.slotId + ("," if j < len(table) - 1 else "") + "\t| # " + slot.name)
						j += 1
					newText.append("\n")
			elif line.startswith('byte '):
				if '@ $806B929C' in line:
					newLine = 'byte ' + addLeadingZeros(str(len(tables[0])), 2) + ' @ $806B929C # Page 1'
				elif '@ $806B92A4' in line:
					newLine = 'byte ' + addLeadingZeros(str(len(tables[1])), 2) + ' @ $806B92A4 # Page 2'
				elif '@ $80496002' in line:
					newLine = 'byte ' + addLeadingZeros(str(len(tables[2])), 2) + ' @ $80496002 # Page 3'
				elif '@ $80496003' in line:
					newLine = 'byte ' + addLeadingZeros(str(len(tables[3])), 2) + ' @ $80496003 # Page 4 (Unused)'
				elif '@ $80496004' in line:
					newLine = 'byte ' + addLeadingZeros(str(len(tables[4])), 2) + ' @ $80496004 # Page 5 (Unused)'
				elif '@ $800AF673' in line:
					newLine = 'byte ' + addLeadingZeros(str(len(tables[0]) + len(tables[1]) + len(tables[2]) + len(tables[3]) + len(tables[4])), 2) + ' @ $800AF673 # Stage Count'
				else:
					newLine = line
				newText.append(newLine)
			elif not stopWriting:
				newText.append(line)
			elif line.startswith("TABLE_STAGES:"):
				stopWriting = False
				newText.append(line)
		File.WriteAllLines(file, newText)
		writeLog("Finished updating stage list")

# Get first unused slot ID
def getUnusedSlotId(slotList):
	writeLog("Getting first available slot ID")
	i = 0
	newSlotId = 0
	while True:
		while i < len(slotList):
			if hexId(newSlotId) == slotList[i].slotId.strip():
				newSlotId += 1
				i = 0
			i += 1
		break
	return hexId(newSlotId)

# Get stage IDs
def getStageIds(path="/Source/Project+/StageFiles.asm"):
		writeLog("Getting stage IDs")
		fileText = File.ReadAllLines(MainForm.BuildPath + path)
		tableValues = []
		tableStart = 0
		# Find the stages table
		i = 0
		while i < len(fileText):
			line = fileText[i]
			if line.startswith("TABLE_STAGES:"):
				writeLog("Found stages table at line " + str(i))
				tableStart = i + 3
				break
			i += 1
		# Get all values in table
		i = tableStart
		while i < len(fileText):
			line = fileText[i]
			if len(line) <= 0 or line.startswith('TABLE'):
				break
			splitLine = list(filter(None, line.replace('|','').split('#')[0].strip().split(',')))
			for item in splitLine:
				tableValues.append(item.strip())
			i += 1
		writeLog("Got stage IDs")
		return tableValues

# Add stage ID pair to table
def addStageId(fullId, stageName, path="/Source/Project+/StageFiles.asm"):
		writeLog("Updating stage IDs")
		file = MainForm.BuildPath + path
		createBackup(file)
		fileText = File.ReadAllLines(file)
		tableStart = 0
		tableValues = []
		# Find the stages table
		i = 0
		while i < len(fileText):
			line = fileText[i]
			if line.startswith("TABLE_STAGES:"):
				writeLog("Found stages table at line " + str(i))
				tableStart = i + 3
				break
			i += 1
		# Get to end of table
		i = tableStart
		while i < len(fileText):
			line = fileText[i]
			if len(line) <= 0 or line.startswith('TABLE'):
				break
			# Get a running list of IDs while we're at it (mostly for length check purposes later)
			splitLine = list(filter(None, line.replace('|','').split('#')[0].strip().split(',')))
			for item in splitLine:
				tableValues.append(item)
			i += 1
		line = fileText[i - 1]
		ids = list(filter(None, line.replace('|','').split('#')[0].strip().split(',')))
		if len(ids) < 4:
			splitLine = line.split('|')
			newLine = splitLine[0].strip() + ',\t0x' + fullId + "\t| "+ splitLine[1] + ", " + stageName
			fileText[i - 1] = newLine
		else:
			splitLine = line.split('|')
			fileText[i - 1] = splitLine[0].rstrip() + ",\t|" + splitLine[1]
			newLine = '0x' + fullId + '\t| #' + stageName
			fileText[i] = newLine
		# Update counter
		counterLine = tableStart - 1
		fileText[counterLine] = "half[" + str(len(tableValues) + 1) + "] |\t# Stage Count + 2"
		File.WriteAllLines(file, fileText)
		writeLog("Finished updating stage IDs")
		return len(tableValues)

# Remove stage ID pair from table
# This function is a mess, please do not look too close at it
def removeStageId(fullId, path="/Source/Project+/StageFiles.asm"):
		writeLog("Removing stage ID " + str(fullId))
		file = MainForm.BuildPath + path
		createBackup(file)
		fileText = File.ReadAllLines(file)
		tableStart = 0
		tableLines = []
		tableValues = []
		# Find the stages table
		i = 0
		while i < len(fileText):
			line = fileText[i]
			if line.startswith("TABLE_STAGES:"):
				writeLog("Found stages table at line " + str(i))
				tableStart = i + 3
				break
			i += 1
		# Get all table lines
		writeLog("Getting all table lines")
		i = tableStart
		while i < len(fileText):
			line = fileText[i]
			if len(line) <= 0 or line.startswith('TABLE'):
				break
			# Get a running list of IDs while we're at it (mostly for length check purposes later)
			checkLine = list(filter(None, line.split('|')[0].strip().split(',')))
			for item in checkLine:
				tableValues.append(item)
			# Store the whole line
			tableLines.append(line)
			i += 1
		k = 0
		while k < len(tableLines):
			splitLine = list(filter(None, tableLines[k].split('|')[0].strip().split(',')))
			i = 0
			# Check for stage ID on this line and replace if found
			found = False
			while i < len(splitLine):
				if splitLine[i].strip() == '0x' + fullId:
					splitLine[i] = '0xFF64'
					found = True
					break
				i += 1
			# If we found a match, update the comments to change stage name to NONE
			if found and '|' in tableLines[k]:
				commentLine = list(filter(None, tableLines[k].split('|')[1].strip().split(',')))
				if i <= len(commentLine):
					commentLine[i] = 'NOTHING'
			else:
				commentLine = ""
			if found:
				writeLog("Found match")
				newLine = ""
				j = 0
				while j < len(splitLine):
					newLine += splitLine[j].strip() + ("," if j != len(splitLine) - 1 else "") + "\t"
					j += 1
				newLine += "| "
				j = 0
				while j < len(commentLine):
					newLine += (commentLine[j].strip() if j <= len(commentLine) else "NOTHING") + ("," if j != len(commentLine) - 1 else "") + " "
					j += 1
				tableLines[k] = newLine
			k += 1
		# Write text
		writeLog("Writing text")
		writeText = []
		i = 0
		while i < len(fileText):
			if i == tableStart - 1:
				writeText.append("half[" + str(len(tableValues) - 1) + "] |\t# Stage Count + 2")
				i += 1
				continue
			elif i == tableStart:
				for tableLine in tableLines:
					writeText.append(tableLine)
				while len(fileText[i]) > 0 and not fileText[i].startswith('TABLE'):
					i += 1
			line = fileText[i]
			writeText.append(line)
			i += 1
		File.WriteAllLines(file, writeText)
		writeLog("Finished removing stage ID")

# Remove stage slot entirely
def removeStageSlot(stageSlots, stageLists):
	writeLog("Removing stage slots")
	for stageSlot in stageSlots:
		writeLog("Removing stage slot " + stageSlot.name)
		stageId = stageSlot.fullId[0:2]
		cosmeticId = stageSlot.fullId[2:4]
		removeFranchiseIcon = BrawlAPI.ShowYesNoPrompt("Would you like to remove " + stageSlot.name + "'s franchise icon?\n\nNOTE: Only do this if no other stages use the franchise icon.", "Remove Franchise Icon?")
		removeGameLogo = BrawlAPI.ShowYesNoPrompt("Would you like to remove " + stageSlot.name + "'s game icon?\n\nNOTE: Only do this if no other stages use the game icon.", "Remove Game Icon?")
		stageAlts = getStageAltInfo(stageId)
		removeStageEntry(stageAlts, forceDelete=True)
		removeStageCosmetics(cosmeticId, removeFranchiseIcon=removeFranchiseIcon, removeGameLogo=removeGameLogo)
		removeStageCosmetics(cosmeticId, 'pf/menu2/mu_menumain.pac', removeFranchiseIcon=removeFranchiseIcon, removeGameLogo=removeGameLogo)
		fileOpened = checkOpenFile('sc_selmap')
		if not fileOpened:
			fileOpened = checkOpenFile('mu_menumain')
		if fileOpened:
			BrawlAPI.SaveFile()
			BrawlAPI.ForceCloseFile()
		for stageList in stageLists:
			removeStageId(stageSlot.fullId, stageList)
		writeLog("Finished removing stage slot")

# Get stage IDs for specific stage number
def getStageIdsByNumber(stageNumber, path="/Source/Project+/StageFiles.asm"):
		writeLog("Getting stage ID by slot ID " + str(stageNumber))
		stageIds = getStageIds(path)
		i = 0
		for stageId in stageIds:
			if hexId(i) == stageNumber:
				writeLog("Found stage ID " + str(stageId))
				return stageId.strip()
			i += 1
		writeLog("No stage ID found")
		return -1

# Get stage name by stage ID
def getStageName(stageId):
		writeLog("Getting stage name by stage ID " + str(stageId))
		fileOpened = checkOpenFile("stageslot")
		if not fileOpened:
			fileOpened = BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/stage/stageslot/')
		if fileOpened:
			folder = getChildByName(BrawlAPI.RootNode, str(stageId).replace('0x', ''))
			if folder:
				node = folder.Children[0]
				if node:
					writeLog("Found stage name " + str(node.Name))
					return node.Name
			BrawlAPI.ForceCloseFile()
		writeLog("Finished getting stage name")

# Get stage cosmetics by cosmetic ID
def getStageCosmetics(cosmeticId):
		writeLog("Getting cosmetics for stage with cosmetic ID " + str(cosmeticId))
		stageIcon = 0
		stagePreview = 0
		stageName = 0
		franchiseIcon = 0
		gameLogo = 0
		altName = 0
		stageNameList = []
		franchiseIconList = []
		gameLogoList = []
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selmap.pac', False)
		if fileOpened:
			bresNode = getChildByName(BrawlAPI.RootNode, "Misc Data [80]")
			if bresNode:
				anmTexPatFolder = getChildByName(bresNode, "AnmTexPat(NW4R)")
				texFolder = getChildByName(bresNode, "Textures(NW4R)")
				if anmTexPatFolder and texFolder:
					# Icon
					iconTextureName = getTextureByFrameIndex(anmTexPatFolder, "MenSelmapIcon", "iconM", int(cosmeticId, 16))
					texNode = getChildByName(texFolder, iconTextureName)
					if texNode:
						stageIcon = Bitmap(texNode.GetImage(0))
					else:
						stageIcon = ""
					# Preview
					previewTextureName = getTextureByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "basebgM", int(cosmeticId, 16))
					texNode = getChildByName(texFolder, previewTextureName)
					if texNode:
						stagePreview = Bitmap(texNode.GetImage(0))
					else:
						stagePreview = ""
					# Name
					nameTextureName = getTextureByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "pasted__stnameM", int(cosmeticId, 16))
					texNode = getChildByName(texFolder, nameTextureName)
					if texNode:
						stageName = Bitmap(texNode.GetImage(0))
					else:
						stageName = ""
					# Franchise Icon
					franchiseIconTextureName = getTextureByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "lambert113", int(cosmeticId, 16))
					texNode = getChildByName(texFolder, franchiseIconTextureName)
					if texNode:
						franchiseIcon = ImageNode(texNode.Name, Bitmap(texNode.GetImage(0)))
					else:
						franchiseIcon = ""
					# Game Logo
					gameLogoTextureName = getTextureByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "pasted__stnamelogoM", int(cosmeticId, 16))
					texNode = getChildByName(texFolder, gameLogoTextureName)
					if texNode:
						gameLogo = ImageNode(texNode.Name, Bitmap(texNode.GetImage(0)))
					else:
						gameLogo = ""
					# R-alt Name
					altNameTextureName = getTextureByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "pasted__stnameM_start", int(cosmeticId, 16))
					texNode = getChildByName(texFolder, altNameTextureName)
					if texNode:
						altName = ImageNode(texNode.Name, Bitmap(texNode.GetImage(0)))
					else:
						altName = ""
					# Stage Names
					for child in texFolder.Children:
						if child.Name.startswith('MenSelmapFrontStname.'):
							stageNameList.append(ImageNode(child.Name, child.GetImage(0)))
						if child.Name.startswith('MenSelchrMark.'):
							franchiseIconList.append(ImageNode(child.Name, child.GetImage(0)))
						if child.Name.startswith('MenSelmapMark.'):
							gameLogoList.append(ImageNode(child.Name, child.GetImage(0)))
			BrawlAPI.ForceCloseFile()
		writeLog("Finished getting cosmetics")
		return StageCosmetics(stageIcon, stagePreview, stageName, franchiseIcon, gameLogo, altName, stageNameList, franchiseIconList, gameLogoList)

# Get the texture associated with a pat0 entry by input frame index
def getTextureByFrameIndex(patFolder, pat0Name, entryName, frameIndex):
		writeLog("Getting textures for pat0 entry with frame index " + str(frameIndex))
		pat0 = getChildByName(patFolder, pat0Name)
		if pat0:
			pat0Entry = getChildByName(pat0, entryName).Children[0]
			if pat0Entry:
				frame = getChildByFrameIndex(pat0Entry, frameIndex)
				if frame != False:
					textureName = frame.Texture
					return textureName
		return 0

# Get a pat0 entry by frame index
def getPat0ByFrameIndex(patFolder, pat0Name, entryName, frameIndex):
		writeLog("Getting pat0 entry with frame index " + str(frameIndex))
		pat0 = getChildByName(patFolder, pat0Name)
		if pat0:
			pat0Entry = getChildByName(pat0, entryName).Children[0]
			if pat0Entry:
				frame = getChildByFrameIndex(pat0Entry, frameIndex, False)
				if frame:
					return frame
		return 0

# Get the ASLEntry nodes for all stage alts for a single stage slot
def getStageAlts(stageId):
		writeLog("Getting all stage alts for stage with ID " + str(stageId))
		if File.Exists(MainForm.BuildPath + '/pf/stage/stageslot/' + str(stageId) + '.asl'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/stage/stageslot/' + str(stageId) + '.asl', False)
			if fileOpened:
				writeLog("Found stage slot")
				nodes = BrawlAPI.RootNode.Children
				BrawlAPI.ForceCloseFile()
				return nodes
		writeLog("Couldn't find stage slot")
		return []

# Get unused stages
def getUnusedStageSlots(stageSlots, path="/Source/Project+/StageFiles.asm"):
		writeLog("Getting unused stage slots")
		i = 0
		unusedSlots = []
		for stage in getStageIds(path):
			append = True
			for slot in stageSlots:
				if slot.fullId == stage.replace('0x',''):
					append = False
					break
			if append and stage != '0xFF64':
				stageName = getStageName(stage[2:4])
				if stageName:
					unusedSlot = StageSlot(hexId(i), stage[2:4], stage[4:6], stage[2:6], stageName)
					unusedSlots.append(unusedSlot)
			i += 1
		writeLog("Finished getting unused stage slots")
		return unusedSlots

# Get stage params for stage
def getStageParams(aslEntry, filePath=""):
		writeLog("Getting stage params for stage " + str(aslEntry.Name))
		if filePath:
			file = filePath
		else:
			file = MainForm.BuildPath + '/pf/stage/stageinfo/' + aslEntry.Name + '.param'
		if File.Exists(file):
			fileOpened = openFile(file, False)
			if fileOpened:
				writeLog("Found stage params")
				rootNode = BrawlAPI.RootNode
				params = StageParams(aslEntry, rootNode.StageName, rootNode.TrackList, rootNode.Module, rootNode.SoundBank, rootNode.EffectBank, aslEntry.Name, originalPacName=rootNode.StageName, originalModule=rootNode.Module, originalTracklist=rootNode.TrackList, originalSoundBank=rootNode.SoundBank)
				BrawlAPI.ForceCloseFile()
				return params
		writeLog("Couldn't find stage params")
		return 0

# Get all info for all stage alts
def getStageAltInfo(stageId):
		writeLog("Getting all stage info for stage ID " + str(stageId))
		stageAlts = getStageAlts(stageId)
		stageParamList = []
		for alt in stageAlts:
			params = getStageParams(alt)
			stageParamList.append(params)
		return stageParamList

# Get unused stage texture name
def getStageTextureName(prefix, cosmeticId, texFolder, new=False):
		writeLog("Getting texture name for cosmetic ID " + str(cosmeticId))
		foundName = getChildByName(texFolder, prefix + addLeadingZeros(str(int(cosmeticId, 16)), 2))
		if foundName and not new:
			return foundName.Name
		else:
			i = 0
			newCosmeticId = 1
			while True:
				while i < len(texFolder.Children):
					if texFolder.Children[i].Name == prefix + addLeadingZeros(str(newCosmeticId), 2):
						newCosmeticId += 1
						i = 0
					i += 1
				break
			return prefix + addLeadingZeros(str(newCosmeticId), 2)
		
# Generic functiont to add stage cosmetics
def addStageCosmetic(cosmeticId, image, anmTexPatFolder, texFolder, bresNode, prefix, pat0Name, entryName, format):
		pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, pat0Name, entryName, int(cosmeticId, 16))
		if not pat0Entry:
			textureName = getStageTextureName(prefix, cosmeticId, texFolder)
			pat0Entry = addToPat0(bresNode, pat0Name, entryName, textureName, textureName, int(cosmeticId, 16), textureName)
			if prefix == "MenSelmapIcon.":
				newPat0 = addToPat0(bresNode, pat0Name, entryName, textureName, textureName, int(cosmeticId, 16) + 400, textureName)
			if prefix == "MenSelmapFrontStname.":
				addToPat0(bresNode, pat0Name, "pasted__stnameshadowM", textureName, textureName, int(cosmeticId, 16), textureName)
			if prefix == "MenSelmapPrevbase.":
				addToPat0(bresNode, pat0Name, "basebgMShadow", textureName, textureName, int(cosmeticId, 16), textureName)
		else:
			textureName = pat0Entry.Texture
		texNode = getChildByName(texFolder, textureName)
		newNode = importTexture(texNode if texNode else bresNode, image, format)
		newNode.Name = textureName

# Import stage cosmetics
def importStageCosmetics(cosmeticId, stageIcon="", stageName="", stagePreview="", franchiseIconName="", gameLogoName="", altStageName="", franchiseIcons=[], gameLogos=[], fileName='/pf/menu2/sc_selmap.pac'):
		writeLog("Importing stage cosmetics for cosmetic ID " + str(cosmeticId))
		if File.Exists(MainForm.BuildPath + fileName):
			fileOpened = openFile(MainForm.BuildPath + fileName)
			if fileOpened:
				if BrawlAPI.RootNode.Name.startswith("sc_selmap"):
					bresNode = getChildByName(BrawlAPI.RootNode, "Misc Data [80]")
				else:
					bresNode = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
				if bresNode:
					anmTexPatFolder = getChildByName(bresNode, "AnmTexPat(NW4R)")
					texFolder = getChildByName(bresNode, "Textures(NW4R)")
					if anmTexPatFolder and texFolder:
						if stageIcon:
							addStageCosmetic(cosmeticId, stageIcon, anmTexPatFolder, texFolder, bresNode, "MenSelmapIcon.", "MenSelmapIcon", "iconM", WiiPixelFormat.CI8)
						if stageName:
							addStageCosmetic(cosmeticId, stageName, anmTexPatFolder, texFolder, bresNode, "MenSelmapFrontStname.", "MenSelmapPreview", "pasted__stnameM", WiiPixelFormat.I4)
						if stagePreview:
							addStageCosmetic(cosmeticId, stagePreview, anmTexPatFolder, texFolder, bresNode, "MenSelmapPrevbase.", "MenSelmapPreview", "basebgM", WiiPixelFormat.CMPR)
						if franchiseIcons:
							for franchiseIcon in franchiseIcons:
								franchiseIconName = getStageTextureName('MenSelchrMark.', '00', texFolder, True)
								franchiseNode = importTexture(bresNode, franchiseIcon, WiiPixelFormat.I4, 64, 64)
								franchiseNode.Name = franchiseIconName
						if gameLogos:
							for gameLogo in gameLogos:
								gameLogoName = getStageTextureName('MenSelmapMark.', '00', texFolder, True)
								if fileName == '/pf/menu2/sc_selmap.pac':
									gameLogoNode = importTexture(bresNode, gameLogo, WiiPixelFormat.IA4)
									gameLogoNode.Name = gameLogoName
						if franchiseIconName:
							pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "lambert113", int(cosmeticId, 16))
							if not pat0Entry:
								pat0Entry = addToPat0(bresNode, "MenSelmapPreview", "lambert113", franchiseIconName, franchiseIconName, int(cosmeticId, 16))
							else:
								pat0Entry.Texture = franchiseIconName
						if gameLogoName:
							pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "pasted__stnamelogoM", int(cosmeticId, 16))
							if not pat0Entry:
								pat0Entry = addToPat0(bresNode, "MenSelmapPreview", "pasted__stnamelogoM", gameLogoName, gameLogoName, int(cosmeticId, 16))
							else:
								pat0Entry.Texture = gameLogoName
						if altStageName:
							pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "pasted__stnameM_start", int(cosmeticId, 16))
							if not pat0Entry:
								pat0Entry = addToPat0(bresNode, "MenSelmapPreview", "pasted__stnameM_start", altStageName, altStageName, int(cosmeticId, 16))
							else:
								pat0Entry.Texture = altStageName
							pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "pasted__stnameshadowM_start", int(cosmeticId, 16))
							if not pat0Entry:
								pat0Entry = addToPat0(bresNode, "MenSelmapPreview", "pasted__stnameshadowM_start", altStageName, altStageName, int(cosmeticId, 16))
							else:
								pat0Entry.Texture = altStageName
						texFolder.SortChildren()
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		writeLog("Finished importing stage cosmetics")

# Remove stage cosmetics
def removeStageCosmetics(cosmeticId, fileName='/pf/menu2/sc_selmap.pac', removeFranchiseIcon=False, removeGameLogo=False):
		writeLog("Removing stage cosmetics for cosmetic ID " + str(cosmeticId))
		if File.Exists(MainForm.BuildPath + fileName):
			fileOpened = openFile(MainForm.BuildPath + fileName)
			if fileOpened:
				cosmeticId = int(cosmeticId, 16)
				if BrawlAPI.RootNode.Name.startswith("sc_selmap"):
					bresNode = getChildByName(BrawlAPI.RootNode, "Misc Data [80]")
				else:
					bresNode = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
				if bresNode:
					removeTexNodes = []
					anmTexPatFolder = getChildByName(bresNode, "AnmTexPat(NW4R)")
					texFolder = getChildByName(bresNode, "Textures(NW4R)")
					if anmTexPatFolder and texFolder:
						pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapIcon", "iconM", cosmeticId)
						if pat0Entry:
							removeTexNodes.append(pat0Entry.Texture)
							pat0Entry.Remove()
						pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapIcon", "iconM", cosmeticId + 400)
						if pat0Entry:
							pat0Entry.Remove()
						pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "pasted__stnameM", cosmeticId)
						if pat0Entry:
							removeTexNodes.append(pat0Entry.Texture)
							pat0Entry.Remove()
						pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "pasted__stnameshadowM", cosmeticId)
						if pat0Entry:
							pat0Entry.Remove()
						pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "basebgM", cosmeticId)
						if pat0Entry:
							removeTexNodes.append(pat0Entry.Texture)
							pat0Entry.Remove()
						pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "basebgMShadow", cosmeticId)
						if pat0Entry:
							pat0Entry.Remove()
						if removeFranchiseIcon:
							pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "lambert113", cosmeticId)
							if pat0Entry:
								removeTexNodes.append(pat0Entry.Texture)
								pat0Entry.Remove()
						if removeGameLogo:
							pat0Entry = getPat0ByFrameIndex(anmTexPatFolder, "MenSelmapPreview", "pasted__stnamelogoM", cosmeticId)
							if pat0Entry:
								removeTexNodes.append(pat0Entry.Texture)
								pat0Entry.Remove()
						for nodeName in removeTexNodes:
							texNode = getChildByName(texFolder, nodeName)
							texNode.Remove(True)
		writeLog("Finished removing cosmetics")

# Update stage slot
def updateStageSlot(stageId, stageParamList):
		writeLog("Updating stage slot for stage ID " + str(stageId))
		if File.Exists(MainForm.BuildPath + '/pf/stage/stageslot/' + str(stageId) + '.asl'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/stage/stageslot/' + str(stageId) + '.asl')
		else: 
			fileOpened = BrawlAPI.New[ASLSNode]()
			BrawlAPI.RootNode.Name = str(stageId)
		if fileOpened:
			i = 0
			while i < len(BrawlAPI.RootNode.Children):
				BrawlAPI.RootNode.Children[i].Remove()
			i = 0
			while i < len(stageParamList):
				BrawlAPI.RootNode.AddChild(ASLSEntryNode())
				if BrawlAPI.RootNode.Children[i] != stageParamList[i].aslEntry:
					BrawlAPI.RootNode.Children[i].Name = stageParamList[i].aslEntry.Name
					BrawlAPI.RootNode.Children[i].ButtonFlags = stageParamList[i].aslEntry.ButtonFlags
				i += 1
			BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/stage/stageslot/' + str(stageId) + '.asl')
			BrawlAPI.ForceCloseFile()
		writeLog("Finished updating stage slot")

# Update stage params
def updateStageParams(stageId, stageParamList):
		writeLog("Updating stage params for stage ID " + str(stageId))
		new = False
		for stageParam in stageParamList:
			if stageParam.originalName and File.Exists(MainForm.BuildPath + '/pf/stage/stageinfo/' + stageParam.originalName + '.param'):
				if stageParam.originalName != stageParam.aslEntry.Name:
					renameFile(MainForm.BuildPath + '/pf/stage/stageinfo/' + stageParam.originalName + '.param', stageParam.aslEntry.Name + '.param')
			if stageParam.paramFile:
				copyRenameFile(stageParam.paramFile, stageParam.aslEntry.Name + '.param', MainForm.BuildPath + '/pf/stage/stageinfo')
			if File.Exists(MainForm.BuildPath + '/pf/stage/stageinfo/' + stageParam.aslEntry.Name + '.param'):
				fileOpened = openFile(MainForm.BuildPath + '/pf/stage/stageinfo/' + stageParam.aslEntry.Name + '.param')
			else:
				fileOpened = BrawlAPI.New[STEXNode]()
				BrawlAPI.RootNode.Name = stageParam.aslEntry.Name
				new = True
			if fileOpened:
				BrawlAPI.RootNode.StageName = stageParam.pacName
				BrawlAPI.RootNode.TrackList = stageParam.tracklist
				BrawlAPI.RootNode.Module = stageParam.module
				BrawlAPI.RootNode.SoundBank = stageParam.soundBank
				BrawlAPI.RootNode.EffectBank = stageParam.effectBank
				if new:
					BrawlAPI.RootNode.SubstageVarianceType = VariantType.None
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/stage/stageinfo/' + stageParam.aslEntry.Name + '.param')
				BrawlAPI.ForceCloseFile()
		writeLog("Finished updating stage params")

# Move stage files into build
def moveStageFiles(stageParamList, brstmFiles=[]):
		writeLog("Moving stage files into build")
		for stageParam in stageParamList:
			if stageParam.pacFile:
				if File.Exists(stageParam.pacFile):
					if not File.Exists(MainForm.BuildPath + "/pf/stage/melee/" + getFileInfo("STG" + stageParam.pacName.upper() + ".pac").Name):
						if stageParam.pacName:
							copyRenameFile(stageParam.pacFile, "STG" + stageParam.pacName.upper() + ".pac", MainForm.BuildPath + '/pf/stage/melee')
						else:
							copyFile(stageParam.pacFile, MainForm.BuildPath + '/pf/stage/melee')
			if stageParam.moduleFile:
				if File.Exists(stageParam.moduleFile):
					if not File.Exists(MainForm.BuildPath + "/pf/module/" + getFileInfo(stageParam.moduleFile).Name):
						if stageParam.module:
							copyRenameFile(stageParam.moduleFile, stageParam.module, MainForm.BuildPath + '/pf/module')
						else:
							copyFile(stageParam.moduleFile, MainForm.BuildPath + '/pf/module')
			if stageParam.tracklistFile:
				if File.Exists(stageParam.tracklistFile):
					if not File.Exists(MainForm.BuildPath + "/pf/sound/tracklist/" + getFileInfo(stageParam.tracklist + ".tlst").Name):
						if stageParam.tracklist:
							copyRenameFile(stageParam.tracklistFile, stageParam.tracklist + ".tlst", MainForm.BuildPath + '/pf/sound/tracklist')
						else:
							copyFile(stageParam.tracklistFile, MainForm.BuildPath + '/pf/sound/tracklist')
			if stageParam.soundBankFile:
				if File.Exists(stageParam.soundBankFile):
					if stageParam.soundBank and hexId(stageParam.soundBank) != "0xFFFF":
						fileName = addLeadingZeros(hexId(stageParam.soundBank).replace('0x', ''), 3) + '_' + stageParam.aslEntry.Name + ".sawnd"
						if not File.Exists(MainForm.BuildPath + "/pf/sfx/" + fileName):
							copyRenameFile(stageParam.soundBankFile, fileName.Replace(fileName.split('_')[0], addLeadingZeros(hexId(stageParam.soundBank).replace('0x', ''), 3)), MainForm.BuildPath + '/pf/sfx')
					elif hexId(stageParam.soundBank != "0xFFFF"):
						fileName = getFileInfo(stageParam.soundBankFile).Name
						if not File.Exists(MainForm.BuildPath + "/pf/sfx/" + fileName):
							copyFile(stageParam.soundBankFile, MainForm.BuildPath + '/pf/sfx')
			if stageParam.paramFile:
				if File.Exists(stageParam.paramFile):
					if not File.Exists(MainForm.BuildPath + "/pf/stage/stageinfo/" + getFileInfo(stageParam.aslEntry.Name + ".param").Name):
						if stageParam.aslEntry:
							copyRenameFile(stageParam.paramFile, stageParam.aslEntry.Name + '.param', MainForm.BuildPath + '/pf/stage/stageinfo')
						else:
							copyFile(stageParam.paramFile, MainForm.BuildPath + '/pf/stage/stageinfo')
		writeLog("Finished moving stage files")

# Remove stage entry
def removeStageEntry(stageParams, deleteParam=True, forceDelete=False):
		writeLog("Removing stage entries")
		title = "Remove file?"
		removePac = False
		removeModule = False
		removeTracklist = False
		removeSoundbank = False
		reviewedFiles = []
		for stageParam in stageParams:
			messageText = "Would you like to remove the following file from " + stageParam.aslEntry.Name + "?:\n"
			if (stageParam.originalPacName and stageParam.originalPacName != stageParam.pacName) or forceDelete:
				pacFile = MainForm.BuildPath + '/pf/stage/melee/' + "STG" + stageParam.originalPacName + ".pac"
				if File.Exists(pacFile) and pacFile not in reviewedFiles:
					removePac = BrawlAPI.ShowYesNoPrompt(messageText + "STG" + stageParam.originalPacName + ".pac", title)
					reviewedFiles.append(pacFile)
				elif pacFile in reviewedFiles:
					removePac = False
			if (stageParam.originalModule and stageParam.originalModule != stageParam.module) or forceDelete:
				moduleFile = MainForm.BuildPath + '/pf/module/' + stageParam.originalModule
				if File.Exists(moduleFile) and moduleFile not in reviewedFiles:
					removeModule = BrawlAPI.ShowYesNoPrompt(messageText + stageParam.originalModule, title)
					reviewedFiles.append(moduleFile)
				elif moduleFile in reviewedFiles:
					removeModule = False
			if (stageParam.originalSoundBank and stageParam.originalSoundBank != stageParam.soundBank) or forceDelete:
				directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/sfx')
				files = directory.GetFiles(addLeadingZeros(str(hexId(stageParam.originalSoundBank)).replace('0x',''), 3) + "*.sawnd")
				if len(files) > 0:
					if files[0].FullName not in reviewedFiles:
						removeSoundbank = BrawlAPI.ShowYesNoPrompt(messageText + files[0].Name, title)
						reviewedFiles.append(files[0].FullName)
					elif files[0].FullName in reviewedFiles:
						removeSoundbank = False
				else:
					removeSoundbank = False
			if removePac:
				File.Delete(pacFile)
			if removeModule:
				File.Delete(moduleFile)
			if removeTracklist:
				File.Delete(tracklistFile)
			if removeSoundbank:
				File.Delete(files[0].FullName)
			if deleteParam:
				if stageParam.originalName:
					paramFile = MainForm.BuildPath + '/pf/stage/stageinfo/' + stageParam.originalName + ".param"
					if File.Exists(paramFile):
						File.Delete(paramFile)
		writeLog("Finished removing stage entries")


#endregion STAGES

#region MUSIC

# Get all tracklists
def getTracklists(netplay=False):
	tracklists = []
	if not netplay:
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/sound/tracklist')
	else:
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/sound/netplaylist')
	for file in directory.GetFiles("*.tlst"):
		tracklists.append(file)
	return tracklists

# Get all nodes from a tracklist file
def getTracklistSongs(tracklistFile):
	songNodes = []
	if File.Exists(tracklistFile):
		fileOpened = openFile(tracklistFile, False)
		if fileOpened:
			for node in BrawlAPI.RootNode.Children:
				newSongNode = Song(node, node.Name, originalBrstm=node.rstmPath)
				songNodes.append(newSongNode)
			BrawlAPI.ForceCloseFile()
	return songNodes

# Update tracklist
def updateTracklist(tracklistFile, songs, netplay=False):
	writeLog("Updating tracklist file " + tracklistFile)
	new = False
	newName = ""
	if not netplay:
		tracklistPath = MainForm.BuildPath + '/pf/sound/tracklist/'
	else:
		tracklistPath = MainForm.BuildPath + '/pf/sound/netplaylist/'
	if File.Exists(tracklistFile):
		fileOpened = openFile(tracklistFile)
	else:
		new = True
		fileOpened = BrawlAPI.New[TLSTNode]()
	if fileOpened:
		i = 0
		rootNode = BrawlAPI.RootNode
		while len(rootNode.Children) > 0:
			rootNode.Children[i].Remove()
		for song in songs:
			rootNode.AddChild(song.songNode)
			if song.brstmFile:
				createBackup(song.songNode.rstmPath)
				File.Copy(song.brstmFile, song.songNode.rstmPath)
		if not new:
			BrawlAPI.SaveFile()
		else:
			newName = BrawlAPI.UserStringInput("Enter the name for your new tracklist")
			createBackup(tracklistPath + newName.split('.tlst')[0] + '.tlst')
			BrawlAPI.SaveFileAs(tracklistPath + newName.split('.tlst')[0] + '.tlst')
		BrawlAPI.ForceCloseFile()
	writeLog("Finished updating tracklist file")
	return newName

# Delete brstms
def deleteBrstms(brstmFiles):
	writeLog("Deleting brstm files")
	reviewedFiles = []
	title = "Delete file?"
	for brstmFile in brstmFiles:
		message = "Would you like to delete the file " + brstmFile + "?\n\nNOTE: Only do this if the file isn't used by other tracklists."
		if File.Exists(brstmFile) and brstmFile not in reviewedFiles:
			reviewedFiles.append(brstmFile)
			removeBrstm = BrawlAPI.ShowYesNoPrompt(message, title)
			if removeBrstm:
				createBackup(brstmFile)
				File.Delete(brstmFile)
	writeLog("Finished deleting brstm files")

# Get song ID
def getSongIdFromSongList(songs):
	writeLog("Getting first unused song IDs")
	currentSongId = 61440
	i = 0
	while i < len(songs):
		if songs[i].songNode.SongID == currentSongId:
			currentSongId += 1
			i = 0
			continue
		else:
			i += 1
	return currentSongId

# Delete tracklist and possibly associated BRSTMs
def deleteTracklist(tracklistFile):
	removeFiles = []
	if File.Exists(tracklistFile.FullName):
		writeLog("Deleting tracklist file " + tracklistFile.FullName)
		fileOpened = openFile(tracklistFile.FullName)
		if fileOpened:
			for node in BrawlAPI.RootNode.Children:
				removeFiles.append(node.rstmPath)
			BrawlAPI.ForceCloseFile()
			deleteBrstms(removeFiles)
		File.Delete(tracklistFile.FullName)
		writeLog("Finished deleting tracklist file")

#endregion MUSIC