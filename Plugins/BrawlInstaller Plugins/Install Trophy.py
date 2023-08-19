__author__ = "Squidgy"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
		# Initial checks
		if str(BrawlAPI.RootNode) != "None":
			BrawlAPI.CloseFile()
		if not MainForm.BuildPath:
			BrawlAPI.ShowMessage("Build path must be set. This can be done by navigating to Tools > Settings > General and setting the 'Default Build Path' to the path to your build's root folder.", "Build Path Not Set")
			return
		if not Directory.Exists(MainForm.BuildPath + '/pf/'):
			BrawlAPI.ShowMessage("Build path does not appear to be valid. Please change your build path by going to 'Tools > Settings' and modifying the 'Default Build Path' field.\n\nYour build path should contain a folder named 'pf' within it.", "Invalid Build Path")
			return

		settings = initialSetup()
		if not settings:
			return
		
		form = TrophyForm()
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.OK:
			# Get name for trophy code
			if form.trophyControl.trophyModelControl.textBox.textBox.Text and File.Exists(form.trophyControl.trophyModelControl.textBox.textBox.Text):
				fileInfo = getFileInfo(form.trophyControl.trophyModelControl.textBox.textBox.Text)
				fighterName = fileInfo.Name.replace(fileInfo.Extension, "")
			else:
				fighterName = ""
			# Get trophy settings
			trophySettings = TrophySettings()
			trophySettings.trophyName = form.trophyControl.trophyNameControl.textBox.Text
			trophySettings.description = form.trophyControl.trophyDescriptionControl.textBox.Text.replace('\r\n', '<br/>')
			if form.trophyControl.trophyCategoryControl.dropDown.SelectedItem:
				trophySettings.categoryIndex = TROPHY_CATEGORIES[form.trophyControl.trophyCategoryControl.dropDown.SelectedItem]
			else:
				trophySettings.categoryIndex = 0
			if form.trophyControl.gameIcon1Control.dropDown.SelectedItem:
				trophySettings.gameIcon1 = TROPHY_GAME_ICONS[form.trophyControl.gameIcon1Control.dropDown.SelectedItem]
			else:
				trophySettings.gameIcon1 = 0
			if form.trophyControl.gameIcon2Control.dropDown.SelectedItem:
				trophySettings.gameIcon2 = TROPHY_GAME_ICONS[form.trophyControl.gameIcon2Control.dropDown.SelectedItem]
			else:
				trophySettings.gameIcon2 = 0
			trophySettings.gameName1 = form.trophyControl.gameName1Control.textBox.Text
			if form.trophyControl.gameName2Control.textBox.Text:
				trophySettings.gameName2 = form.trophyControl.gameName2Control.textBox.Text
			if form.trophyControl.trophySeriesControl.dropDown.SelectedItem:
				trophySettings.seriesIndex = TROPHY_SERIES[form.trophyControl.trophySeriesControl.dropDown.SelectedItem]
			else:
				trophySettings.seriesIndex = 19
			trophyIdHex = hexId(form.trophyIdBox.textBox.Text) if form.trophyIdBox.textBox.Text else None
			thumbnailId = int(hexId(form.thumbnailIdBox.textBox.Text).replace('0x', ''), 16)
			# Install trophy
			try:
				createLogFile()
				backupCheck()
				# If temporary directory already exists, delete it to prevent duplicate files
				if Directory.Exists(TEMP_PATH):
					Directory.Delete(TEMP_PATH, 1)
				createDirectory(TEMP_PATH)
				trophyId = installTrophy(hexId(form.slotIdBox.textBox.Text).replace('0x', '') if form.slotIdBox.textBox.Text else "", form.trophyControl.trophyModelControl.textBox.textBox.Text, form.trophyControl.trophyImageControl.Images[0], fighterName, trophySettings, settings.installToSse, trophyIdHex=trophyIdHex, thumbnailId=thumbnailId)
				BrawlAPI.ShowMessage("Trophy installed with ID " + str(trophyId), "Success")
			except Exception as e:
				writeLog("ERROR " + str(e))
				if 'progressBar' in locals():
					progressBar.Finish()
				BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
				BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
				restoreBackup()
				archiveBackup()
		form.Dispose()

main()