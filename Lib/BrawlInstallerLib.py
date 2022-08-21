version = "1.0"
# BrawlInstallerLib
# Functions used by BrawlInstaller plugins

import binascii
import clr
clr.AddReference("System.Drawing")
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

# TODO: Rename files when importing for most things

#region CONSTANTS

RESOURCE_PATH = AppPath + '/BrawlAPI/BrawlInstaller Resources'

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
		for file in directory.GetFiles():
			if file.Name == name:
				return file
		return 0

# Helper function that gets a directory from a base directory by specified name
def getDirectoryByName(name, baseDirectory):
		for directory in baseDirectory:
			if directory.Name == name:
				return directory
		return 0

# Helper function that gets names of all files in the provided directory
def getFileNames(directory):
		files = directory.GetFiles()
		fileNames = [0] * len(files)
		for i, file in enumerate(files):
			fileNames[i] = file.FullName
		return Array[str](fileNames)

# Helper function that imports a texture automatically without prompting the user
def importTexture(node, imageSource, format, sizeW=0, sizeH=0):
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
		IDs = []
		for track in parentNode.Children:
			if track.SongID >= 61440: #0xF000 
				IDs.append(track.SongID)
		return IDs

# Helper function to get children where the first characters match what is passed in
def getChildrenByPrefix(parentNode, prefix):
		matches = []
		for child in parentNode.Children:
			if child.Name.StartsWith(prefix):
				matches.append(child)
		return matches

# Helper function to add a new pat0TexEntry to specified pat0
def addToPat0(parentNode, pat0NodeName, pat0texNodeName, name, texture, frameIndex, palette="", frameCountOffset=0, overrideFrameCount=0, tex0Override=""):
		pat0Node = getChildByName(getChildByName(parentNode, "AnmTexPat(NW4R)"), pat0NodeName)
		# Add to pat0texNode
		tex0 = "Texture0" if tex0Override == "" else tex0Override
		pat0texNode = getChildByName(getChildByName(pat0Node, pat0texNodeName), tex0)
		pat0texEntryNode = PAT0TextureEntryNode()
		pat0texEntryNode.FrameIndex = frameIndex
		pat0texEntryNode.Name = name
		pat0texEntryNode.Texture = texture
		pat0texNode.AddChild(pat0texEntryNode)
		# Palette gets screwed up for some reason if we don't do it this way
		if palette != "":
			pat0texEntryNode = getChildByName(pat0texNode, name)
			pat0texEntryNode.Palette = palette
		if overrideFrameCount > pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset:
			pat0Node.FrameCount = overrideFrameCount
		elif frameCountOffset != 0:
			pat0Node.FrameCount = pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset
		sortChildrenByFrameIndex(pat0texNode)

# Helper function to remove pat0TexEntry from specified pat0
def removeFromPat0(parentNode, pat0NodeName, pat0texNodeName, name, frameCountOffset=0, overrideFrameCount=0, tex0Override=""):
		pat0Node = getChildByName(getChildByName(parentNode, "AnmTexPat(NW4R)"), pat0NodeName)
		# Remove from pat0texNode
		tex0 = "Texture0" if tex0Override == "" else tex0Override
		pat0texNode = getChildByName(getChildByName(pat0Node, pat0texNodeName), tex0)
		pat0texEntryNode = getChildByName(pat0texNode, name)
		if pat0texEntryNode:
			pat0texEntryNode.Remove()
		if overrideFrameCount > pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset:
			pat0Node.FrameCount = overrideFrameCount
		elif frameCountOffset != 0:
			pat0Node.FrameCount = pat0texNode.Children[len(pat0texNode.Children) - 1].FrameIndex + frameCountOffset

# Get value of key from settings
def readValueFromKey(settings, key):
		# Search for a matching key and if one is found, return value
		for line in settings:
			if line.StartsWith(';') or len(line) == 0:
				continue
			if line.split(' = ')[0] == key:
				return line.split(' = ')[1]
		return 0

# Check if fighter ID is already in use
def getFighterConfig(fighterId):
		fighterConfigs = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig', 'Fighter' + str(fighterId) + '.dat')
		if fighterConfigs:
			return fighterConfigs[0]
		else:
			return 0

# Check if cosmetic ID is already in use
def getCosmeticConfig(fighterId):
		cosmeticConfigs = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig', 'Cosmetic' + str(fighterId) + '.dat')
		if cosmeticConfigs:
			return cosmeticConfigs[0]
		else:
			return 0

# Check if slot ID is already in use
def getSlotConfig(fighterId):
		slotConfigs = Directory.GetFiles(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig', 'Slot' + str(fighterId) + '.dat')
		if slotConfigs:
			return slotConfigs[0]
		else:
			return 0

# Get song name from Results.tlst by song ID
def getSongNameById(songId):
		BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/sound/tracklist/Results.tlst')
		for song in BrawlAPI.RootNode.Children:
			if song.SongID == songId:
				BrawlAPI.ForceCloseFile()
				return song.SongFileName.split('Victory!/')[1]
		BrawlAPI.ForceCloseFile()
		return 0

# Get the victory theme of a fighter by their ID
def getVictoryThemeByFighterId(fighterId):
		slotConfig = getSlotConfig(fighterId)
		if slotConfig:
			BrawlAPI.OpenFile(slotConfig)
			songId = BrawlAPI.RootNode.VictoryTheme
			BrawlAPI.ForceCloseFile()
			songName = getSongNameById(songId)
			return songName
		return 0

# Get the victory theme ID of a fighter by their ID
def getVictoryThemeIDByFighterId(fighterId):
		slotConfig = getSlotConfig(fighterId)
		if slotConfig:
			BrawlAPI.OpenFile(slotConfig)
			songId = BrawlAPI.RootNode.VictoryTheme
			BrawlAPI.ForceCloseFile()
			return songId
		return 0

# Helper method to more easily copy files
def copyFile(sourcePath, destinationPath):
		Directory.CreateDirectory(destinationPath)
		File.Copy(sourcePath, destinationPath + '/' + FileInfo(sourcePath).Name)

# Helper method to create a backup of the provided file with correct folder structure
def createBackup(sourcePath):
		fullPath = AppPath + '/backup/' + sourcePath.replace(MainForm.BuildPath, '')
		path = fullPath.replace(FileInfo(sourcePath).Name, '')
		Directory.CreateDirectory(path)
		File.Copy(sourcePath, fullPath, True)

# Helper method to check if a file is open, and if it is not, open it and create a backup
def openFile(filePath):
		nodeName = FileInfo(filePath).Name.split('.')[0]
		fileOpened = checkOpenFile(nodeName)
		if fileOpened == 0:
			createBackup(filePath)
			fileOpened = BrawlAPI.OpenFile(filePath)
		return fileOpened

# Helper method to more easily copy and rename files
def copyRenameFile(sourcePath, newName, destinationPath):
		Directory.CreateDirectory(destinationPath)
		File.Copy(sourcePath, destinationPath + '/' + newName)

# Return the text version of a boolean value
def boolText(boolVal):
		if boolVal == True:
			return "true"
		else:
			return "false"

#endregion HELPER FUNCTIONS

#region IMPORT FUNCTIONS
# Functions used by the BrawlInstaller suite to add elements to a build

# Import CSPs
def importCSPs(cosmeticId, directory, rspLoading="false"):
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
			newNode.Export(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + str(cosmeticId) + '0.brres')
			# Set compression back
			newNode.Compression = "ExtendedLZ77"
			# If user has RSP loading on, get rid of changes to this file
			if rspLoading == "true":
				newNode.Remove()

# Import stock icons
def importStockIcons(cosmeticId, directory, tex0BresName, pat0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true"):
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
				images = Directory.GetFiles(folder, "*.png")
				# Color smash images in folders with multiple
				if len(images) > 1:
					ColorSmashImport(node, images, 256)
				else:
					importTexture(node, images[0], WiiPixelFormat.CI8, 32, 32)
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

# Create battle portraits frome images
def createBPs(cosmeticId, images, fiftyCC="true"):
		# For 50 costume code, we must multiply the cosmetic ID by 50
		newId = (cosmeticId * 50) + 1 if fiftyCC == "true" else int(str(cosmeticId) + "1")
		# Create a BP file for each texture
		for image in images:
			outputPath = MainForm.BuildPath + '/pf/info/portrite/InfFace' + addLeadingZeros(str(newId), 4 if fiftyCC == "true" else 3) + '.brres'
			BrawlAPI.New[BRRESNode]()
			importTexture(BrawlAPI.RootNode, image, WiiPixelFormat.CI8)
			BrawlAPI.SaveFileAs(outputPath)
			newId += 1
		BrawlAPI.ForceCloseFile()

# Update and move EX config files
def modifyExConfigs(files, cosmeticId, fighterId, fighterName, franchiseIconId=-1, useKirbyHat=False, newSoundBankId="", victoryThemeId=0, kirbyHatFighterId=-1):
		# Iterate through each file
		for file in files:
			file = FileInfo(file)
			BrawlAPI.OpenFile(file.FullName)
			# Update CosmeticID field and rename CosmeticConfig
			if file.Name.lower().StartsWith("cosmetic"):
				BrawlAPI.RootNode.CosmeticID = cosmeticId
				if franchiseIconId != -1:
					BrawlAPI.RootNode.FranchiseIconID = franchiseIconId - 1
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/CosmeticConfig/' + file.Name.replace(file.Name, "Cosmetic" + fighterId + ".dat"))
			# Rename FighterConfig 
			if file.Name.lower().StartsWith("fighter"):
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
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/FighterConfig/' + file.Name.replace(file.Name, "Fighter" + fighterId + ".dat"))
			# Rename CSSSlotConfig 
			if file.Name.lower().StartsWith("cssslot"):
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/CSSSlotConfig/' + file.Name.replace(file.Name, "CSSSlot" + fighterId + ".dat"))
			# Rename SlotConfig
			if file.Name.lower().StartsWith("slot"):
				if victoryThemeId:
					BrawlAPI.RootNode.VictoryTheme = victoryThemeId
				BrawlAPI.SaveFileAs(MainForm.BuildPath + '/pf/BrawlEx/SlotConfig/' + file.Name.replace(file.Name, "Slot" + fighterId + ".dat"))
			BrawlAPI.ForceCloseFile()

# Import CSS icon
def importCSSIcon(cosmeticId, iconImagePath, format):
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

# Import replay icon
def importReplayIcon(cosmeticId, replayIconImagePath):
		# If sc_selcharacter is not already opened, open it
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu/collection/Replay.brres')
		if fileOpened:
			# Import icon texture
			newNode = importTexture(BrawlAPI.RootNode, replayIconImagePath, WiiPixelFormat.CI8)
			newNode.Name = "MenReplayChr." + addLeadingZeros(str(cosmeticId) + "1", 3)
			# Add replay icon to pat0
			anmTexPat = getChildByName(BrawlAPI.RootNode, "AnmTexPat(NW4R)")
			pat0Node = getChildByName(anmTexPat, "MenReplayPreview2_TopN__0")
			addToPat0(BrawlAPI.RootNode, pat0Node.Name, "lambert78", newNode.Name, newNode.Name, int(str(cosmeticId) + "1"), palette=newNode.Name, frameCountOffset=10, tex0Override="Texture1")

# Import CSS icon name
def importCSSIconName(cosmeticId, nameImagePath):
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
				
# Import name for character select portrait
def importPortraitName(cosmeticId, file):
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

# Import franchise icon into CSS or info
def importFranchiseIcon(franchiseIconId, image, filePath, size):
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
			if fileNodeName == "info":
				newNode = importTexture(node, image, WiiPixelFormat.I4, sizeW=48)
				pat0texNodeName = "lambert110"
				pat0NodeName = "InfMark_TopN__0"
			newNode.Name = "MenSelchrMark." + addLeadingZeros(str(franchiseIconId), 2)
			addToPat0(node, pat0NodeName, pat0texNodeName, newNode.Name, newNode.Name, franchiseIconId, frameCountOffset=1)

# Add franchise icon to result screen
def importFranchiseIconResult(franchiseIconId, image):
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

# Update the module file with fighter ID
def updateModule(file, directory, fighterId, fighterName):
		file = FileInfo(file)
		BrawlAPI.OpenFile(file.FullName)
		# Get section 8 and export it
		node = getChildByName(BrawlAPI.RootNode, "Section [8]")
		node.Export(directory.FullName + "/Section [8]")
		BrawlAPI.ForceCloseFile()
		# Get the exported section 8 file
		sectionFile = directory.FullName + "/Section [8]"
		# Read the section 8 file and write to it
		with open(sectionFile, mode='r+b') as editFile:
			section8 = editFile.read()
			editFile.seek(3)
			editFile.write(binascii.unhexlify(fighterId))
			editFile.seek(0)
			section8Modified = editFile.read()
			editFile.close()
		# Read the module file
		with open(file.FullName,  mode='r+b') as moduleFile:
			data = str(moduleFile.read())
			moduleFile.close()
		# Where the module file matches section 8, replace it with our modified section 8 values
		updatedData = data.replace(section8, section8Modified)
		with open(file.FullName, mode='r+b') as moduleFile:
			moduleFile.seek(0)
			moduleFile.write(updatedData)
		File.Copy(file.FullName, MainForm.BuildPath + '/pf/module/ft_' + fighterName.lower() + '.rel', 1)

# Move fighter files to fighter folder
def moveFighterFiles(files, fighterName, originalFighterName=""):
		for file in files:
			file = FileInfo(file)
			# TODO: rename files based on fighter name?
			if originalFighterName != "":
				path = MainForm.BuildPath + '/pf/fighter/' + fighterName.lower().replace(originalFighterName.lower(), fighterName) + '/' + file.Name.lower().replace(originalFighterName.lower(), fighterName.lower())
			else:
				path = MainForm.BuildPath + '/pf/fighter/' + fighterName.lower() + '/' + file.Name
			FileInfo(path).Directory.Create()
			File.Copy(file.FullName, path, 1)

# Soundbank IDs are between 331 and 586, or 14B and 24A in hex
def updateSoundbankId(fighterFile, sawndReplacerExe, sfxChangeExe, oldSoundbankId, newSoundBankId, addSeven="true"):
		Directory.SetCurrentDirectory(sawndReplacerExe.Directory.FullName)
		# Set up should go like this: Are your sound bank IDs usually in hex? (If no) Do you usually need to add 7 when naming your soundbanks?
		# Or something like that, basically we should support hex, decimal, and decimal + 7 formats. So in some cases, this may not actually add + 7
		# Actually probably just ask hex/dec and then +7/not +7 for best experience
		modifier = 7 if addSeven == "true" else 0
		p = Process.Start(sawndReplacerExe.FullName, 'extoex ' + str(hex(int(oldSoundbankId, 16) + modifier)) + ' ' + str(hex(int(newSoundBankId, 16) + modifier)) + ' "' + sfxChangeExe.Directory.FullName + '/sound.txt"')
		p.WaitForExit()
		p.Dispose()
		Directory.SetCurrentDirectory(AppPath)
		BrawlAPI.OpenFile(fighterFile.FullName)
		moveset = getChildByName(BrawlAPI.RootNode, "Misc Data [0]")
		moveset.Export(sfxChangeExe.Directory.FullName + '/moveset.dat')
		Directory.SetCurrentDirectory(sfxChangeExe.Directory.FullName)
		p = Process.Start(sfxChangeExe.FullName, 'moveset.dat ' + 'sound.txt')
		p.WaitForExit()
		p.Dispose
		Directory.SetCurrentDirectory(AppPath)
		moveset.Replace(sfxChangeExe.Directory.FullName + '/moveset_sfxconverted.dat')
		BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()

# Move soundbank to build
# Before P+, soundbanks would be named in decimal + 7. So soundbank 1CB would be 459 + 7 = 466
def moveSoundbank(file, newSoundBankId=""):
		if newSoundBankId == "":
			fileName = file.Name
		else:
			fileName = newSoundBankId.upper() + '.sawnd'
		path = MainForm.BuildPath + '/pf/sfx/' + fileName
		File.Copy(file.FullName, path, 1)

# Add character to CSSRoster.dat
def addToRoster(fighterId):
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
		return changesMade

# Add Kirby hat fixes
# Check kirby soundbanks here: http://opensa.dantarion.com/wiki/Soundbanks_(Brawl)
def addKirbyHat(characterName, fighterName, fighterId, kirbyHatFigherId, kirbyHatExe):
		kirbyHatPath = FileInfo(kirbyHatExe).DirectoryName
		Directory.SetCurrentDirectory(kirbyHatPath)
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
		if matchFound:
			File.WriteAllLines(kirbyHatPath + '/EX_KirbyHats.txt', fileText)
		else:
			File.AppendAllText(kirbyHatPath + '/EX_KirbyHats.txt', '\n"' + characterName + '" = 0x' + fighterId + ' : 0x' + kirbyHatFigherId)
		# Run exe
		p = Process.Start(kirbyHatExe, '1 1 1 1 1 -q')
		p.WaitForExit()
		p.Dispose()
		Directory.SetCurrentDirectory(AppPath)

# Move Kirby hat files
def moveKirbyHatFiles(files, oldFighterName="", newFighterName=""):
		for file in files:
			# TODO: rename files based on fighter name?
			file = FileInfo(file)
			if oldFighterName != "" and newFighterName != "":
				path = MainForm.BuildPath + '/pf/fighter/kirby/' + file.Name.replace(oldFighterName, newFighterName)
			else:
				path = MainForm.BuildPath + '/pf/fighter/kirby/' + file.Name
			FileInfo(path).Directory.Create()
			File.Copy(file.FullName, path, 1)

# Add character victory theme
def addVictoryTheme(file):
		# Move to strm directory
		file = FileInfo(file)
		path = MainForm.BuildPath + '/pf/sound/strm/Victory!/' + file.Name
		FileInfo(path).Directory.Create()
		File.Copy(file.FullName, path, 1)
		BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/sound/tracklist/Results.tlst')
		# Check if song is already installed
		for song in BrawlAPI.RootNode.Children:
			if song.SongFileName == 'Victory!/' + file.Name.split('.')[0]:
				BrawlAPI.ForceCloseFile()
				return song.SongID
		# Calculate song ID
		usedSongIds = getUsedSongIds(BrawlAPI.RootNode)
		currentSongId = 61440
		while currentSongId in usedSongIds:
			currentSongId += 1
		# Add to tracklist file
		newNode = TLSTEntryNode()
		newNode.Name = file.Name.split('.')[0]
		newNode.SongFileName = 'Victory!/' + file.Name.split('.')[0]
		newNode.Volume = 80
		newNode.Frequency = 40
		newNode.SongID = currentSongId
		BrawlAPI.RootNode.AddChild(newNode)
		BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()
		return currentSongId

# Add fighter to code menu
def addToCodeMenu(fighterName, fighterId, assemblyFunctionExe):
		assemblyFunctionsPath = FileInfo(assemblyFunctionExe).DirectoryName
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
				fileText[i] = '"' + fighterName + '" = 0x' + fighterId
			i += 1
		# Write updated file
		if matchFound:
			File.WriteAllLines(assemblyFunctionsPath + '/EX_Characters.txt', fileText)
		else:
			File.AppendAllText(assemblyFunctionsPath + '/EX_Characters.txt', '\n"' + fighterName + '" = 0x' + fighterId)
		p = Process.Start(assemblyFunctionExe, '1 1 1 1 -q')
		p.WaitForExit()
		p.Dispose()
		Directory.SetCurrentDirectory(AppPath)

#endregion IMPORT FUNCTIONS

#region REMOVE FUNCTIONS
# Functions used by the BrawlInstaller suite to remove elements

# Remove imported CSPs and RSPs for specified cosmetic ID
def removeCSPs(cosmeticId):
		fileOpened = openFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
		if fileOpened:
			# Find char_bust_tex_lz77
			arcNode = getChildByName(BrawlAPI.RootNode, "char_bust_tex_lz77")
			# Get CSP brres and remove if it exists
			nodeToRemove = getChildByName(arcNode, "Misc Data [" + str(cosmeticId) + "]")
			if nodeToRemove:
				nodeToRemove.Remove()
		# Get RSP file and delete if it exists
		rspFile = getFileByName("MenSelchrFaceB" + addLeadingZeros(str(cosmeticId), 3) + "0.brres", Directory.CreateDirectory(MainForm.BuildPath + '/pf/menu/common/char_bust_tex'))
		if rspFile:
			rspFile.Delete()

# Delete BPs for specified cosmetic ID
def deleteBPs(cosmeticId, fiftyCC="true"):
		# For 50 costume code, we must multiply the cosmetic ID by 50
		newId = (cosmeticId * 50) + 1 if fiftyCC == "true" else int(str(cosmeticId) + "1")
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/info/portrite')
		# Look for files matching naming scheme and delete them
		while newId <= (cosmeticId * 50) + 50:
			bpFile = getFileByName("InfFace" + addLeadingZeros(str(newId), 4 if fiftyCC == "true" else 3) + ".brres", directory)
			if bpFile:
				bpFile.Delete()
			else:
				# If no matching file exists, just exit
				break
			newId += 1

# Remove CSS icon
def removeCSSIcon(cosmeticId):
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

# Remove replay icon
def removeReplayIcon(cosmeticId):
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
			removeFromPat0(BrawlAPI.RootNode, pat0Node.Name, "lambert78", nodeName, frameCountOffset=10, tex0Override="Texture1")

# Remove CSS icon name
def removeCSSIconName(cosmeticId):
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

# Remove portrait name
def removePortraitName(cosmeticId):
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

# Remove franchise icon from CSS or info
def removeFranchiseIcon(franchiseIconId, filePath):
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
			if fileNodeName == "info":
				pat0texNodeName = "lambert110"
				pat0NodeName = "InfMark_TopN__0"
			removeFromPat0(node, pat0NodeName, pat0texNodeName, nodeName, frameCountOffset=1)

# Remove franchise icon from result screen
def removeFranchiseIconResult(franchiseIconId):
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

# Remove stock icons
def removeStockIcons(cosmeticId, tex0BresName, pat0BresName, rootName="", filePath='/pf/info2/info.pac', fiftyCC="true"):
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

# Delete module for specified fighter
def deleteModule(internalName):
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/module')
		moduleFile = getFileByName("ft_" + internalName.lower() + ".rel", directory)
		if moduleFile:
			moduleFile.Delete()

# Delete fighter files for specified fighter
def deleteFighterFiles(internalName):
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/fighter')
		fighterDirectory = Directory.GetDirectories(directory.FullName, internalName.lower())
		if fighterDirectory:
			Directory.Delete(fighterDirectory[0], True)

# Delete kirby hat files for specified fighter
def deleteKirbyHatFiles(internalName):
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/fighter/kirby')
		kirbyHatFiles = Directory.GetFiles(directory.FullName, "FitKirby" + internalName + "*.pac")
		if kirbyHatFiles:
			i = 0
			while i < len(kirbyHatFiles):
				FileInfo(kirbyHatFiles[i]).Delete()
				i += 1

# Delete the specified soundbank
def deleteSoundbank(soundBankId):
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/sfx')
		soundBank = getFileByName(str(soundBankId).upper() + ".sawnd", directory)
		if soundBank:
			soundBank.Delete()

# Delete EX configs for specified fighter ID
def deleteExConfigs(fighterId):
		directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/BrawlEx')
		for folder in Directory.GetDirectories(directory.FullName):
			exConfig = getFileByName(DirectoryInfo(folder).Name.split("Config")[0] + str(fighterId) + ".dat", DirectoryInfo(folder))
			if exConfig:
				exConfig.Delete()

# Remove character from CSSRoster.dat
def removeFromRoster(fighterId):
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

# Remove character victory theme
def removeVictoryTheme(songID):
		BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/sound/tracklist/Results.tlst')
		# Remove from tracklist file
		node = BrawlAPI.RootNode
		if node.Children:
			for child in node.Children:
				if child.SongID == songID:
					childNode = child
					break
		# Get filename
		path = MainForm.BuildPath + '/pf/sound/strm/Victory!'
		directory = Directory.CreateDirectory(path)
		brstmFile = getFileByName(childNode.SongFileName.split('/')[1] + ".brstm", directory)
		# Remove from tracklist
		if childNode:
			childNode.Remove()
		# Delete from directory
		if brstmFile:
			brstmFile.Delete()
		BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()

# Remove kirby hat
def removeKirbyHat(fighterId, kirbyHatExe):
		kirbyHatPath = FileInfo(kirbyHatExe).DirectoryName
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
			File.WriteAllLines(kirbyHatPath + '/EX_KirbyHats.txt', Array[str](newFileText))
			# Run exe
			p = Process.Start(kirbyHatExe, '1 1 1 1 1 -q')
			p.WaitForExit()
			p.Dispose()
		Directory.SetCurrentDirectory(AppPath)

# Remove fighter from code menu
def removeFromCodeMenu(fighterId, assemblyFunctionExe):
		assemblyFunctionsPath = FileInfo(assemblyFunctionExe).DirectoryName
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
			File.WriteAllLines(assemblyFunctionsPath + '/EX_Characters.txt', Array[str](newFileText))
			# Run the exe
			p = Process.Start(assemblyFunctionExe, '1 1 1 1 -q')
			p.WaitForExit()
			p.Dispose()
		Directory.SetCurrentDirectory(AppPath)

#endregion REMOVE FUNCTIONS

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
		addKirbyHat(characterName, fighterName, fighterId, kirbyHatFigherId, kirbyHatExe)
		moveKirbyHatFiles(files, oldFighterName, newFighterName)

#endregion INSTALLER FUNCTIONS

#region GENERAL FUNCTIONS
# General utility functions for the BrawlInstaller plugin suite

# Unzip fighter zip file and store contents in temporary directory
def unzipFile(filePath):
		args = 'x -y -bsp0 -bso0 -bd "' + filePath + '" -o"' + AppPath + '/temp"'
		p = Process.Start(RESOURCE_PATH + '/7za.exe', args)
		p.WaitForExit()
		p.Dispose()

# Get info from supplied fighter and cosmetic IDs
def getFighterInfo(fighterConfig, cosmeticConfig, slotConfig):
		fighterName = ""
		soundbankId = 0
		cosmeticId = 0
		franchiseIconId = 0
		songId = 0
		characterName = ""
		if fighterConfig:
			BrawlAPI.OpenFile(fighterConfig)
			fighterName = BrawlAPI.RootNode.FighterName
			soundbankId = BrawlAPI.RootNode.SoundBank
			BrawlAPI.ForceCloseFile()
		if cosmeticConfig:
			BrawlAPI.OpenFile(cosmeticConfig)
			cosmeticId = BrawlAPI.RootNode.CosmeticID
			# Add 1 because the franchise icon ID in the config is 1 less
			franchiseIconId = BrawlAPI.RootNode.FranchiseIconID + 1
			characterName = BrawlAPI.RootNode.CharacterName
			BrawlAPI.ForceCloseFile()
		if slotConfig:
			BrawlAPI.OpenFile(slotConfig)
			songId = BrawlAPI.RootNode.VictoryTheme
			BrawlAPI.ForceCloseFile()
		return FighterInfo(fighterName, cosmeticId, franchiseIconId, soundbankId, songId, characterName)

# Check if franchise icon ID is already used
def franchiseIconIdUsed(franchiseIconId):
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

#endregion GENERAL FUNCTIONS

#region SETUP FUNCTIONS
def getSettings():
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
		return settings

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
				BrawlAPI.ShowMessage("Victory themes can only be installed with the modern tracklist system. Victory themes will not be installed.", title)
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

class FighterInfo:
		def __init__(self, fighterName, cosmeticId, franchiseIconId, soundbankId, songId, characterName):
			self.fighterName = fighterName
			self.cosmeticId = cosmeticId
			self.franchiseIconId = franchiseIconId
			self.soundbankId = soundbankId
			self.songId = songId
			self.characterName = characterName

#endregion CLASSES