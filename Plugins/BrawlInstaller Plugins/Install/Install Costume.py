__author__ = "Squidgy"
__version__ = "1.4.0"

from InstallLib import *
from CostumeForm import *
from System.Drawing import Bitmap

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

			# User input
			# TODO: Improved form
			cspImages = BrawlAPI.OpenMultiFileDialog("Select CSPs", "PNG files|*.png")
			bpImages = BrawlAPI.OpenMultiFileDialog("Select BPs", "PNG files|*.png")
			stockImages = BrawlAPI.OpenMultiFileDialog("Select stocks", "PNG files|*.png")
			costumeFiles = BrawlAPI.OpenMultiFileDialog("Select costume .pac files", "PAC files|*.pac")
			fighterId = showIdPrompt("Enter fighter's ID")
			fighterId = fighterId.split('0x')[1].upper()
			cosmeticId = showIdPrompt("Enter fighter's cosmetic ID")
			cosmeticId = int(cosmeticId, 16)
			cssSlotConfigId = showIdPrompt("Enter fighter's CSS slot config ID")
			cssSlotConfigId = cssSlotConfigId.split('0x')[1].upper()

			# TODO: check stock icons too, cross-examine to determine actual available costume IDs
			if File.Exists(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres'):
				BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
				texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
				costumeSet = True
				images = []
				for node in texFolder.Children:
					if costumeSet:
						images.append(Bitmap(node.GetImage(0)))
						costumeSet = True
					if node.SharesData:
						costumeSet = False
					else:
						costumeSet = True
						
				BrawlAPI.ForceCloseFile()

				form = CostumeForm(images=images)
				result = form.ShowDialog(MainForm.Instance)
				if result == DialogResult.OK:
					installCostume(cosmeticId, fighterId, cssSlotConfigId, form.index, cspImages, bpImages, stockImages, costumeFiles)
			else:
				BrawlAPI.ShowMessage("Cosmetics for this fighter could not be found! Please try a different ID.", "Error")

		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()



main()