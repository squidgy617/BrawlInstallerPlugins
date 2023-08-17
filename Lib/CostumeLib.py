# CostumeLib
# Library for BrawlInstaller's costume functions

from InstallLib import *
from UninstallLib import *
from BrawlInstallerForms import *
from System.Drawing import Bitmap

def promptCostumeInstall(cosmeticsOnly=False):
	try:
		# Get user settings
		if File.Exists(MainForm.BuildPath + '/settings.ini'):
			settings = getSettings()
		else:
			settings = initialSetup()
		if not settings:
			return
		createLogFile()
		backupCheck()

		# User input
		form = CostumePrompt(cosmeticsOnly=cosmeticsOnly)
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.OK:
			cspImages = form.cspFiles
			bpImages = form.bpFiles
			stockImages = form.stockFiles
			costumeFiles = form.costumeFiles
			fighterId = hexId(form.fighterIdTextbox.Text).split('0x')[1].upper()
			cosmeticId = int(hexId(form.cosmeticIdTextbox.Text).replace('0x',''), 16)
			cssSlotConfigId = hexId(form.cssSlotConfigIdTextbox.Text).split('0x')[1].upper()
			updateConfig = form.configCheckbox.Checked
			images = []
			positions = []
			newPositions = []
			skipPositions = []

			# Get costumes
			if File.Exists(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres'):
				BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
				texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
				costumeSet = True
				i = 0
				for node in texFolder.Children:
					if costumeSet:
						images.append(Bitmap(node.GetImage(0)))
						positions.append(i)
						costumeSet = True
					if node.SharesData:
						costumeSet = False
					else:
						costumeSet = True
					i += 1

				newPositions = positions
						
				BrawlAPI.ForceCloseFile()

				# Get the costumes as indicated by stock icons
				stocksChecked = False
				if settings.installStocksToCSS == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "Misc Data [90]", rootName="", filePath='/pf/menu2/sc_selcharacter.pac', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True
				if settings.installStockIconsToResult == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "Misc Data [120]", rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True
				if settings.installStocksToInfo == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "Misc Data [30]", rootName="", filePath='/pf/info2/info.pac', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True
				if settings.installStocksToStockFaceTex == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "", rootName="", filePath='/pf/menu/common/StockFaceTex.brres', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True
				if settings.installStocksToSSS == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "Misc Data [40]", rootName="", filePath='/pf/menu2/sc_selmap.pac', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True

				# Filter out costumes where stock and CSP color smash groups don't match			
				i = 0
				length = len(positions)
				while i < length:
					if positions[i] not in newPositions:
						skipPositions.append(i)
					i += 1

				# Get available IDs
				usedIds = getUsedCostumeIds(cssSlotConfigId)
				availableIds = []
				i = 0
				while i < 50:
					if i not in usedIds:
						availableIds.append(addLeadingZeros(str(i), 2))
					i += 1

				# Show the form
				form = CostumeForm(images=images, skipPositions=skipPositions, availableIds=availableIds, cosmeticsOnly=cosmeticsOnly)
				result = form.ShowDialog(MainForm.Instance)

				if result == DialogResult.OK:
					if form.dropDown.SelectedValue:
						startingId = int(form.dropDown.SelectedValue) if not form.dropDown.SelectedValue.startswith('0x') else int(form.dropDown.SelectedValue, 16)
					else:
						startingId = 0
					if form.action == "replace":
						uninstallCostume(cosmeticId, fighterId, cssSlotConfigId, form.index, skipPositions, skipMessage=True, cosmeticsOnly=cosmeticsOnly, updateConfig=updateConfig)
					installCostume(cosmeticId, fighterId, cssSlotConfigId, form.index, cspImages, bpImages, stockImages, costumeFiles, skipPositions, startingId, cosmeticsOnly=cosmeticsOnly, updateConfig=updateConfig)
				form.Dispose()
			else:
				BrawlAPI.ShowMessage("Cosmetics for this fighter could not be found! Please try a different ID.", "Error")
	except Exception as e:
		if 'progressBar' in locals():
			progressBar.Finish()
		raise e
	
def promptCostumeUninstall(cosmeticsOnly=False):
	try:
		# Get user settings
		if File.Exists(MainForm.BuildPath + '/settings.ini'):
			settings = getSettings()
		else:
			settings = initialSetup()
		if not settings:
			return
		createLogFile()
		backupCheck()

		# User input
		form = CostumePrompt(uninstall=True, cosmeticsOnly=cosmeticsOnly)
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.OK:
			fighterId = hexId(form.fighterIdTextbox.Text).split('0x')[1].upper()
			cosmeticId = int(hexId(form.cosmeticIdTextbox.Text).replace('0x',''), 16)
			cssSlotConfigId = hexId(form.cssSlotConfigIdTextbox.Text).split('0x')[1].upper()
			updateConfig = form.configCheckbox.Checked
		else:
			return
		images = []
		positions = []
		newPositions = []
		skipPositions = []

		# Get costumes
		if File.Exists(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres'):
			BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
			texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
			costumeSet = True
			i = 0
			for node in texFolder.Children:
				if costumeSet:
					images.append(Bitmap(node.GetImage(0)))
					positions.append(i)
					costumeSet = True
				if node.SharesData:
					costumeSet = False
				else:
					costumeSet = True
				i += 1
					
			BrawlAPI.ForceCloseFile()

			# Get the costumes as indicated by stock icons
			stocksChecked = False
			if settings.installStocksToCSS == "true" and not stocksChecked:
				newPositions = checkStockIcons(cosmeticId, "Misc Data [90]", rootName="", filePath='/pf/menu2/sc_selcharacter.pac', fiftyCC=settings.fiftyCostumeCode)
				stocksChecked = True
			if settings.installStockIconsToResult == "true" and not stocksChecked:
				newPositions = checkStockIcons(cosmeticId, "Misc Data [120]", rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC=settings.fiftyCostumeCode)
				stocksChecked = True
			if settings.installStocksToInfo == "true" and not stocksChecked:
				newPositions = checkStockIcons(cosmeticId, "Misc Data [30]", rootName="", filePath='/pf/info2/info.pac', fiftyCC=settings.fiftyCostumeCode)
				stocksChecked = True
			if settings.installStocksToStockFaceTex == "true" and not stocksChecked:
				newPositions = checkStockIcons(cosmeticId, "", rootName="", filePath='/pf/menu/common/StockFaceTex.brres', fiftyCC=settings.fiftyCostumeCode)
				stocksChecked = True
			if settings.installStocksToSSS == "true" and not stocksChecked:
				newPositions = checkStockIcons(cosmeticId, "Misc Data [40]", rootName="", filePath='/pf/menu2/sc_selmap.pac', fiftyCC=settings.fiftyCostumeCode)
				stocksChecked = True

			# Filter out costumes where stock and CSP color smash groups don't match			
			i = 0
			length = len(positions)
			while i < length:
				if positions[i] not in newPositions:
					skipPositions.append(i)
				i += 1

			# Show the form
			form = CostumeForm(images=images, skipPositions=skipPositions, remove=True, cosmeticsOnly=cosmeticsOnly)
			result = form.ShowDialog(MainForm.Instance)

			if result == DialogResult.OK:
				uninstallCostume(cosmeticId, fighterId, cssSlotConfigId, form.index, skipPositions, cosmeticsOnly=cosmeticsOnly, updateConfig=updateConfig)
		else:
			BrawlAPI.ShowMessage("Cosmetics for this fighter could not be found! Please try a different ID.", "Error")
	except Exception as e:
		if 'progressBar' in locals():
			progressBar.Finish()
		raise e