__author__ = "Squidgy"

from BrawlInstallerLib import *
from BrawlInstallerForms import *

def main():
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

		settings = None
		stageLists = []

		if File.Exists(MainForm.BuildPath + '/settings.ini'):
			settings = getSettings()

		if File.Exists(MainForm.BuildPath + '/Source/Project+/StageFiles.asm'):
			stageListEntries = getStageList('/Source/Project+/StageFiles.asm')
			if len(stageListEntries) > 0:
				stageLists.append('/Source/Project+/StageFiles.asm')
		if File.Exists(MainForm.BuildPath + '/Source/Netplay/Net-StageFiles.asm'):
			stageListEntries = getStageList('/Source/Netplay/Net-StageFiles.asm')
			if len(stageListEntries) > 0:
				stageLists.append('/Source/Netplay/Net-StageFiles.asm')

		if settings:
			if settings.customStageLists:
				customStageLists = settings.customStageLists.split(',')
				for stageList in customStageLists:
					if File.Exists(MainForm.BuildPath + stageList.replace(MainForm.BuildPath, '')):
						stageListEntries = getStageList(stageList.replace(MainForm.BuildPath, ''))
						if len(stageListEntries) > 0:
							stageLists.append(stageList.replace(MainForm.BuildPath, ''))

		if len(stageLists) <= 0:
			BrawlAPI.ShowMessage('No stage lists could be found. If your build uses a custom style of stage lists, please run the "Configure Settings" plugin to set up stagelist paths.', 'No Stage Lists Found')
			return

		form = StageList(stageLists)
		result = form.ShowDialog(MainForm.Instance)
		if result == DialogResult.Abort:
			restoreBackup()
			archiveBackup()
		else:
			archiveBackup()

main()