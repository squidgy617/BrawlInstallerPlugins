__author__ = "Squidgy"
__version__ = "1.4.0"

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
			backupCheck()

			#cosmeticId = showIdPrompt("Enter cosmetic ID")
			images = BrawlAPI.OpenMultiFileDialog("Select CSPs", "PNG files|*.png")
			#bpImages = BrawlAPI.OpenMultiFileDialog("Select BPs", "PNG files|*.png")
			#stockImages = BrawlAPI.OpenMultiFileDialog("Select stocks", "PNG files|*.png")
			costumeFiles = BrawlAPI.OpenMultiFileDialog("Select costume .pac files", "PAC files|*.pac")
			
			index = addCSPs(0, images, "false", 2)
			
			#indexes = subtractCSPs(0, "true", 2)
			
			# If we did any work in sc_selcharacter, save and close it
			fileOpened = checkOpenFile("sc_selcharacter")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			#incrementBPNames(0, index, increment=len(bpImages), fiftyCC="true")
			#createBPs(0, bpImages, startIndex=index)
			#addStockIcons(0, stockImages, index, "Misc Data [120]", "Misc Data [110]", rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC="true")
			fileOpened = checkOpenFile("STGRESULT")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			costumes = importCostumeFiles(costumeFiles, 'mario', '00')
			addCssSlots(costumes, index, '00')

			#deleteBPs(0, startIndex=indexes[0], endIndex=indexes[1])
			#incrementBPNames(0, startIndex=indexes[1], increment = -1 * ((indexes[1] - indexes[0]) + 1))
			#subtractStockIcons(0, indexes[0], "Misc Data [120]", "Misc Data [110]", endIndex=indexes[1], rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC="true")
			fileOpened = checkOpenFile("STGRESULT")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()
		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()



main()