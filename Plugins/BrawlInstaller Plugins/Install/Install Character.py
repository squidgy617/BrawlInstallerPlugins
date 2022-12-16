__author__ = "Squidgy"
__version__ = "1.7.0"

from InstallLib import *
from UninstallLib import *
from BrawlInstallerForms import *

def autoInstall(baseCssSlotId, zipfile):
		# Get first available ID - start at 3F (63 in dec), first available Ex ID
		id = 63
		while True:
			# These IDs are reserved for SSE characters so skip them
			if id == 72 or id == 73 or id == 74:
				id += 1
				continue
			foundId = searchForExConfig('Fighter', hexId(id))
			if foundId:
				id += 1
				continue
			foundId = searchForExConfig('Cosmetic', hexId(id))
			if foundId:
				id += 1
				continue
			foundId = searchForExConfig('CSSSlot', hexId(id))
			if foundId:
				id += 1
				continue
			foundId = searchForExConfig('Slot', hexId(id))
			if foundId:
				id += 1
				continue
			break
		
		# Commented out for 242 character code builds
		# Max ID is 7F (127 in hex)
		#if id > 127:
		#	id = 127

		id = hexId(id).replace('0x', '')

		# Get the first available cosmetic ID
		# Start at 52, first available ID after random
		cosmeticId = 52
		if Directory.Exists(MainForm.BuildPath + '/pf/menu/common/char_bust_tex'):
			while True:
				for file in Directory.GetFiles(MainForm.BuildPath + '/pf/menu/common/char_bust_tex', "*.brres"):
					# This ID causes stock icons to show incorrectly in SSE, so skip it
					if cosmeticId == 62:
						cosmeticId += 1
						continue
					foundId = int(getFileInfo(file).Name.replace('MenSelchrFaceB', '').replace('0.brres', ''))
					if foundId == cosmeticId:
						cosmeticId += 1
						continue
				break

		# Get first available franchise icon ID
		franchiseIconId = 0
		if File.Exists(MainForm.BuildPath + '/pf/info2/info.pac'):
			fileOpened = openFile(MainForm.BuildPath + '/pf/info2/info.pac', False)
			if fileOpened:
				bresNode = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
				if bresNode:
					texFolder = getChildByName(bresNode, "Textures(NW4R)")
					if texFolder:
						while True:
							foundNode = getChildByName(texFolder, "MenSelchrMark." + addLeadingZeros(str(franchiseIconId), 2))
							if foundNode:
								franchiseIconId += 1
								continue
							break
				BrawlAPI.ForceCloseFile()
		installCharacter(id, cosmeticId, franchiseIconId, True, baseCssSlotId=baseCssSlotId, zipfile=zipfile)

def main():
		try: 
			if str(BrawlAPI.RootNode) != "None":
				BrawlAPI.CloseFile()
			if not MainForm.BuildPath:
				BrawlAPI.ShowMessage("Build path must be set. This can be done by navigating to Tools > Settings > General and setting the 'Default Build Path' to the path to your build's root folder.", "Build Path Not Set")
				return
			if not Directory.Exists(MainForm.BuildPath + '/pf/'):
				BrawlAPI.ShowMessage("Build path does not appear to be valid. Please change your build path by going to 'Tools > Settings' and modifying the 'Default Build Path' field.\n\nYour build path should contain a folder named 'pf' within it.", "Invalid Build Path")
				return
			createLogFile()
			backupCheck()
			zipfile = BrawlAPI.OpenFileDialog("Select fighter zip file", "Zip files|*.zip")
			if not zipfile:
				return
			form = CharacterForm()
			result = form.ShowDialog(MainForm.Instance)
			if result == DialogResult.OK:
				if form.rb1.Checked:
					baseCssSlotId = hexId(form.subCharacterTextbox.Text).replace('0x','')
					autoInstall(baseCssSlotId, zipfile)
				else:
					fighterId = hexId(form.fighterIdTextbox.Text).replace('0x','')
					if form.cosmeticIdTextbox.Text:
						cosmeticId = int(hexId(form.cosmeticIdTextbox.Text).replace('0x', ''), 16)
					else:
						cosmeticId = ""
					cosmeticConfigId = hexId(form.cosmeticConfigIdTextbox.Text).replace('0x','')
					slotConfigId = hexId(form.slotConfigIdTextbox.Text).replace('0x','')
					cssSlotConfigId = hexId(form.cssSlotConfigIdTextbox.Text).replace('0x','')
					baseCssSlotId = hexId(form.subCharacterTextbox.Text).replace('0x','')
					installCharacter(fighterId, cosmeticId, cosmeticConfigId=cosmeticConfigId, slotConfigId=slotConfigId, cssSlotConfigId=cssSlotConfigId, baseCssSlotId=baseCssSlotId, zipfile=zipfile)	

		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()

main()