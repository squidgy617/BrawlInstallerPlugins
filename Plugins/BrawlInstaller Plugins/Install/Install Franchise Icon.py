__author__ = "Squidgy"
__version__ = "1.5.0"

from BrawlInstallerLib import *
from InstallLib import *

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

			# Get user settings
			if File.Exists(MainForm.BuildPath + '/settings.ini'):
				settings = getSettings()
			else:
				settings = initialSetup()
			# If temporary directory already exists, delete it to prevent duplicate files
			if Directory.Exists(AppPath + '/temp'):
				Directory.Delete(AppPath + '/temp', 1)

			# Prompt to select images
			franchiseIconBlack = BrawlAPI.OpenFileDialog("Select franchise icon with black background", "PNG files|*.PNG")
			franchiseIconTransparent = BrawlAPI.OpenFileDialog("Select franchise icon with transparent background", "PNG files|*.PNG")

			# Franchise Icon ID prompt
			franchiseIconUsed = True
			while franchiseIconUsed:
				franchiseIconId = int(showIdPrompt("Enter your desired franchise icon ID").replace('0x', ''), 16)
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

			# Set up progressbar
			progressCounter = 0
			progressBar = ProgressWindow(MainForm.Instance, "Installing Franchise Icon...", "Installing Franchise Icon", False)
			progressBar.Begin(0, 4, progressCounter)

			# Install to sc_selcharacter
			if franchiseIconBlack:
				installFranchiseIcon(franchiseIconId, franchiseIconBlack, '/pf/menu2/sc_selcharacter.pac', int(settings.franchiseIconSizeCSS))
			fileOpened = checkOpenFile("sc_selcharacter")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# info.pac
			if franchiseIconBlack:
				installFranchiseIcon(franchiseIconId, franchiseIconBlack, '/pf/info2/info.pac')
			fileOpened = checkOpenFile("info")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# Single player modes
			if settings.installSingleplayerCosmetics == "true":
				for file in Directory.GetFiles(MainForm.BuildPath + '/pf/info2/', "*.pac"):
					fileName = getFileInfo(file).Name
					if fileName != "info.pac":
						if franchiseIconBlack:
							installFranchiseIcon(franchiseIconId, franchiseIconBlack, '/pf/info2/' + fileName)
						fileOpened = checkOpenFile(fileName.split('.pac')[0])
						if fileOpened:
							BrawlAPI.SaveFile()
							BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# STGRESULT
			if franchiseIconTransparent:
				installFranchiseIconResult(franchiseIconId, franchiseIconTransparent)
			fileOpened = checkOpenFile("STGRESULT")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# SSE
			if settings.installToSse == "true":
				if franchiseIconBlack:
					installFranchiseIcon(franchiseIconId, franchiseIconBlack, '/pf/menu2/if_adv_mngr.pac')
				fileOpened = checkOpenFile("if_adv_mngr")
				if fileOpened:
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)
			progressBar.Finish()

			# Delete temporary directory
			if Directory.Exists(AppPath + '/temp'):
				Directory.Delete(AppPath + '/temp', 1)
			archiveBackup()
			BrawlAPI.ShowMessage("Franchise icon installed successfully.", "Success")

		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()


main()