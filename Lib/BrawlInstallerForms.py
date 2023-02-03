# BrawlInstallerForms
# Library for forms used by BrawlInstaller

from BrawlInstallerLib import *
from BrawlLib.Internal.Windows.Controls import *
from System.Windows.Forms import *
from System.Drawing import *
from BrawlLib.CustomLists import *

#region FUNCTIONS

# General function to show the ID form
def showIdForm(title="Enter ID", buttonText="Select", idType="fighter", labelText="Fighter ID:", customList=[]):
        form = IdEntryForm(title, buttonText, idType, labelText, customList)
        result = form.ShowDialog(MainForm.Instance)
        id = ""
        if result == DialogResult.OK:
            id = hexId(form.idTextbox.Text).replace('0x', '')
        form.Dispose()
        return id

# General function to show ID picker
def showIdPicker(idType="fighter", customList=[]):
        form = IdPicker(idType, customList)
        id = ""
        result = form.ShowDialog(MainForm.Instance)
        if result == DialogResult.OK:
            id = form.idBox.Text
        form.Dispose()
        return id

# General function to show image ID picker
# imageTypes: cosmetic, franchise
def showImageIdPicker(imageType="cosmetic"):
        id = ""
        if imageType == "cosmetic":
            imageNodes = getCosmeticNodes()
        elif imageType == "franchise":
            imageNodes = getFranchiseIconNodes()
        labelText = "Cosmetic ID:" if imageType == "cosmetic" else "Icon ID:"
        form = ImageIdPicker(imageNodes, labelText)
        result = form.ShowDialog(MainForm.Instance)
        if result == DialogResult.OK:
            id = form.idBox.Text
        form.Dispose()
        return id

#endregion FUNCTIONS

#region ID PICKER

def getTracklistNodes(tracklist):
    songNodes = []
    if File.Exists(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist):
        opened = BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/sound/tracklist/' + tracklist)
        if opened:
            for node in BrawlAPI.RootNode.Children:
                songNodes.append(node)
            BrawlAPI.ForceCloseFile()
    return songNodes

class IdPicker(Form):

    # OPTIONS: fighter, cosmetic, slot, cssSlot, victoryTheme, creditsTheme, custom
    def __init__(self, option="fighter", customList=[]):
        # Form parameters
        self.Text = 'ID Picker'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.MinimumSize = Size(267,344)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.option = option
        self.musicMode = True if option == "victoryTheme" or option == "creditsTheme" else False

        self.idListBox = ListBox()
        self.idListBox.Width = 120
        self.idListBox.Height = 240
        self.idListBox.Location = Point(16, 16)
        if not FighterNameGenerators.generated:
            FighterNameGenerators.GenerateLists()
        if option == "cosmetic":
            self.idListBox.DataSource = FighterNameGenerators.cosmeticIDList
        elif option == "slot":
            self.idListBox.DataSource = FighterNameGenerators.slotIDList
        elif option == "cssSlot":
            self.idListBox.DataSource = FighterNameGenerators.cssSlotIDList
        elif option == "victoryTheme":
            self.idListBox.DataSource = getTracklistNodes('Results.tlst')
        elif option == "creditsTheme":
            self.idListBox.DataSource = getTracklistNodes('Credits.tlst')
        elif option == "custom":
            self.idListBox.DataSource = customList
        else:
            self.idListBox.DataSource = FighterNameGenerators.fighterIDList
        self.idListBox.SelectedValueChanged += self.idListBoxValueChanged
        self.idListBox.HorizontalScrollbar = True

        self.idBox = TextBox()
        self.idBox.Location = Point(208, 16) if not self.musicMode else Point(156, 32)
        self.idBox.ReadOnly = True
        if not self.musicMode:
            self.idBox.Width = 32

        label = Label()
        if option == "cosmetic":
            label.Text = "Cosmetic ID:"
        elif option == "slot":
            label.Text = "Slot ID:"
        elif option == "cssSlot":
            label.Text = "CSSSlot ID:"
        elif option == "fighter":
            label.Text = "Fighter ID:"
        elif option == "victoryTheme" or option == "creditsTheme":
            label.Text = "Song ID:"
        else:
            label.Text = "ID:"
        label.TextAlign = ContentAlignment.TopRight
        label.Location = Point(104, 16)

        okButton = Button()
        okButton.Text = "Select"
        okButton.Dock = DockStyle.Bottom
        okButton.Click += self.okButtonPressed

        cancelButton = Button()
        cancelButton.Text = "Cancel"
        cancelButton.Dock = DockStyle.Bottom
        cancelButton.Click += self.cancelButtonPressed

        self.Controls.Add(self.idListBox)
        self.Controls.Add(self.idBox)
        self.Controls.Add(label)
        self.Controls.Add(okButton)
        self.Controls.Add(cancelButton)

    def idListBoxValueChanged(self, sender, args):
        if not self.musicMode and not self.option == "custom":
            self.idBox.Text = str(hexId(self.idListBox.SelectedItem.ID))
        elif self.option == "custom":
            self.idBox.Text = str(hexId(self.idListBox.SelectedValue))
        else:
            self.idBox.Text = str(hexId(self.idListBox.SelectedItem.SongID))

    def okButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.OK
        self.Close()

    def cancelButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Close()

#endregion ID PICKER

#region IMAGE ID PICKER

def getCosmeticNodes():
    imageNodes = []
    if Directory.Exists(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/'):
        opened = BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/')
        if opened:
            for node in BrawlAPI.RootNode.Children:
                imageNode = ImageNode(node.Name.replace('0.brres', ''), Bitmap(node.GetImage(0)))
                imageNodes.append(imageNode)
            BrawlAPI.ForceCloseFile()
    return imageNodes

def getFranchiseIconNodes():
    imageNodes = []
    if File.Exists(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac'):
        opened = BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/menu2/sc_selcharacter.pac')
        if opened:
            bresNode = getChildByName(BrawlAPI.RootNode, "Misc Data [30]")
            if bresNode:
                texFolder = getChildByName(bresNode, "Textures(NW4R)")
                if texFolder:
                    for node in texFolder.Children:
                        if node.Name.startswith('MenSelchrMark.'):
                            imageNode = ImageNode(node.Name, Bitmap(node.GetImage(0)))
                            imageNodes.append(imageNode)
            BrawlAPI.ForceCloseFile()
    return imageNodes

class ImageIdPicker(Form):

    def __init__(self, imageNodes, labelText="Cosmetic ID:"):
        # Form parameters
        self.Text = 'Image ID Picker'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.MinimumSize = Size(267,344)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.imageListBox = ListBox()
        self.imageListBox.Width = 120
        self.imageListBox.Height = 240
        self.imageListBox.Location = Point(16, 16)
        self.imageListBox.DataSource = imageNodes
        self.imageListBox.DisplayMember = "name"
        self.imageListBox.ValueMember = "image"
        self.imageListBox.SelectedValueChanged += self.imageListBoxValueChanged
        self.imageListBox.HorizontalScrollbar = True

        self.idBox = TextBox()
        self.idBox.Location = Point(208, 16)
        self.idBox.ReadOnly = True
        self.idBox.Width = 32

        label = Label()
        label.Text = labelText
        label.TextAlign = ContentAlignment.TopRight
        label.Location = Point(104, 16)

        self.imageBox = PictureBox()
        self.imageBox.Location = Point(144, 64)
        self.imageBox.SizeMode = PictureBoxSizeMode.CenterImage
        self.imageBox.Size = Size(128, 160)

        okButton = Button()
        okButton.Text = "Select"
        okButton.Dock = DockStyle.Bottom
        okButton.Click += self.okButtonPressed

        cancelButton = Button()
        cancelButton.Text = "Cancel"
        cancelButton.Dock = DockStyle.Bottom
        cancelButton.Click += self.cancelButtonPressed

        self.Controls.Add(self.imageListBox)
        self.Controls.Add(self.idBox)
        self.Controls.Add(label)
        self.Controls.Add(self.imageBox)
        self.Controls.Add(okButton)
        self.Controls.Add(cancelButton)

    def imageListBoxValueChanged(self, sender, args):
        self.idBox.Text = str(int(self.imageListBox.SelectedItem.name.replace('MenSelchrFaceB', '').replace("MenSelchrMark.", "")))
        self.imageBox.Image = self.imageListBox.SelectedItem.image

    def okButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.OK
        self.Close()

    def cancelButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Close()

#endregion ID PICKER

#region MUSIC LIST

class MusicList(Form):

    def __init__(self):
        # Form parameters
        self.Text = 'Tracklists'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.MinimumSize = Size(267,344)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.tracklists = BindingSource()
        self.tracklists.DataSource = getTracklists()
        self.netplaylists = BindingSource()
        self.netplaylists.DataSource = getTracklists(True)

        self.tabControl = TabControl()
        self.tabControl.Dock = DockStyle.Fill

        offlineTab = TabPage()
        offlineTab.Text = 'Standard'
        self.tabControl.Controls.Add(offlineTab)

        netplayTab = TabPage()
        netplayTab.Text = 'Netplay'
        self.tabControl.Controls.Add(netplayTab)

        self.tracklistBox = ListBox()
        self.tracklistBox.Width = 120
        self.tracklistBox.Height = 240
        self.tracklistBox.Location = Point(16, 32)
        self.tracklistBox.DataSource = self.tracklists
        self.tracklistBox.DisplayMember = "Name"
        self.tracklistBox.ValueMember = "FullName"

        self.netplaylistBox = ListBox()
        self.netplaylistBox.Width = 120
        self.netplaylistBox.Height = 240
        self.netplaylistBox.Location = Point(16, 32)
        self.netplaylistBox.DataSource = self.netplaylists
        self.netplaylistBox.DisplayMember = "Name"
        self.netplaylistBox.ValueMember = "FullName"

        editButton = Button()
        editButton.Location = Point(152, 32)
        editButton.Text = "Edit"
        editButton.Click += self.editButtonPressed

        netplayEditButton = Button()
        netplayEditButton.Location = Point(152, 32)
        netplayEditButton.Text = "Edit"
        netplayEditButton.Click += self.editButtonPressed

        addButton = Button()
        addButton.Location = Point(152, 60)
        addButton.Text = "Add"
        addButton.Click += self.addButtonPressed

        netplayAddButton = Button()
        netplayAddButton.Location = Point(152, 60)
        netplayAddButton.Text = "Add"
        netplayAddButton.Click += self.addButtonPressed

        deleteButton = Button()
        deleteButton.Location = Point(152, 116)
        deleteButton.Text = "Delete"
        deleteButton.Click += self.deleteButtonPressed

        okButton = Button()
        okButton.Location = Point(152, 248)
        okButton.Text = "OK"
        okButton.Click += self.okButtonPressed

        copyButton = Button()
        copyButton.Location = Point(152, 144)
        copyButton.Text = "Copy to Netplay"
        copyButton.Height = 35
        copyButton.Click += self.copyButtonPressed

        netplayCopyButton = Button()
        netplayCopyButton.Location = Point(152, 144)
        netplayCopyButton.Text = "Copy to Offline"
        netplayCopyButton.Height = 35
        netplayCopyButton.Click += self.copyButtonPressed

        netplayDeleteButton = Button()
        netplayDeleteButton.Location = Point(152, 116)
        netplayDeleteButton.Text = "Delete"
        netplayDeleteButton.Click += self.deleteButtonPressed

        netplayOkButton = Button()
        netplayOkButton.Location = Point(152, 248)
        netplayOkButton.Text = "OK"
        netplayOkButton.Click += self.okButtonPressed

        importButton = Button()
        importButton.Location = Point(152, 88)
        importButton.Text = "Import"
        importButton.Click += self.importButtonPressed

        netplayImportButton = Button()
        netplayImportButton.Location = Point(152, 88)
        netplayImportButton.Text = "Import"
        netplayImportButton.Click += self.importButtonPressed

        listBoxLabel = Label()
        listBoxLabel.Text = "Tracklists"
        listBoxLabel.Height = 16
        listBoxLabel.Location = Point(16, 8)

        netplayListBoxLabel = Label()
        netplayListBoxLabel.Text = "Tracklists"
        netplayListBoxLabel.Height = 16
        netplayListBoxLabel.Location = Point(16, 8)

        offlineTab.Controls.Add(self.tracklistBox)
        offlineTab.Controls.Add(listBoxLabel)
        offlineTab.Controls.Add(editButton)
        offlineTab.Controls.Add(addButton)
        offlineTab.Controls.Add(importButton)
        offlineTab.Controls.Add(deleteButton)
        offlineTab.Controls.Add(copyButton)
        offlineTab.Controls.Add(okButton)

        netplayTab.Controls.Add(self.netplaylistBox)
        netplayTab.Controls.Add(netplayListBoxLabel)
        netplayTab.Controls.Add(netplayEditButton)
        netplayTab.Controls.Add(netplayAddButton)
        netplayTab.Controls.Add(netplayImportButton)
        netplayTab.Controls.Add(netplayDeleteButton)
        netplayTab.Controls.Add(netplayCopyButton)
        netplayTab.Controls.Add(netplayOkButton)

        self.Controls.Add(self.tabControl)

    def editButtonPressed(self, sender, args):
        try:
            netplay = False if self.tabControl.SelectedIndex == 0 else True
            if self.tabControl.SelectedIndex == 0:
                tracklistFile = self.tracklistBox.SelectedValue
            else:
                tracklistFile = self.netplaylistBox.SelectedValue
            form = TracklistEditor(tracklistFile, netplay)
            result = form.ShowDialog(MainForm.Instance)
            form.Dispose()
            if result == DialogResult.Abort:
                self.DialogResult = DialogResult.Abort
                self.Close()
            if result == DialogResult.OK:
                self.refreshListbox()
                self.setSelectedItem(form.newName)
                form.Dispose()
        except Exception as e:
            writeLog("ERROR " + str(e))
            if 'progressBar' in locals():
                progressBar.Finish()
            BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
            BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
            self.DialogResult = DialogResult.Abort
            self.Close()
    
    def addButtonPressed(self, sender, args):
        try:
            netplay = False if self.tabControl.SelectedIndex == 0 else True
            form = TracklistEditor("", netplay)
            result = form.ShowDialog(MainForm.Instance)
            form.Dispose()
            if result == DialogResult.Abort:
                self.DialogResult = DialogResult.Abort
                self.Close()
            if result == DialogResult.OK:
                self.refreshListbox()
                self.setSelectedItem(form.newName)
                form.Dispose()
                BrawlAPI.ShowMessage("Tracklist created successfully.", "Success")
        except Exception as e:
            writeLog("ERROR " + str(e))
            if 'progressBar' in locals():
                progressBar.Finish()
            BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
            BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
            self.DialogResult = DialogResult.Abort
            self.Close()

    def deleteButtonPressed(self, sender, args):
        try:
            result = BrawlAPI.ShowYesNoPrompt("Are you sure you want to delete this tracklist? This is a file operation and cannot be undone without restoring a backup.", "Delete tracklist?")
            if result:
                if self.tabControl.SelectedIndex == 0:
                    if File.Exists(self.tracklistBox.SelectedItem.FullName):
                        deleteTracklist(self.tracklistBox.SelectedItem)
                else:
                    if File.Exists(self.netplaylistBox.SelectedItem.FullName):
                        deleteTracklist(self.netplaylistBox.SelectedItem)
                self.refreshListbox()
        except Exception as e:
            writeLog("ERROR " + str(e))
            if 'progressBar' in locals():
                progressBar.Finish()
            BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
            BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
            self.DialogResult = DialogResult.Abort
            self.Close()

    def importButtonPressed(self, sender, args):
        try:
            newFile = BrawlAPI.OpenFileDialog("Select your tracklist file", "TLST files|*.tlst")
            result = True
            if newFile:
                if self.tabControl.SelectedIndex == 0:
                    file = getFileInfo(newFile)
                    destinationPath = MainForm.BuildPath + '/pf/sound/tracklist/'
                    filePath = destinationPath + file.Name
                    folderName = "tracklist"
                else:
                    file = getFileInfo(newFile)
                    destinationPath = MainForm.BuildPath + '/pf/sound/netplaylist/'
                    filePath = destinationPath + file.Name
                    folderName = "netplaylist"
                if File.Exists(filePath):
                    result = BrawlAPI.ShowYesNoPrompt("A file with that name already exists in the " + folderName + " folder. Would you like to replace it?", "Overwrite?")
                if result:
                    copyFile(file.FullName, destinationPath)
                    self.refreshListbox()
                    self.setSelectedItem(file.Name.split('.tlst')[0])
                    BrawlAPI.ShowMessage("File imported successfully.", "Success")
        except Exception as e:
            writeLog("ERROR " + str(e))
            if 'progressBar' in locals():
                progressBar.Finish()
            BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
            BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
            self.DialogResult = DialogResult.Abort
            self.Close()

    def okButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.OK
        self.Close()

    def copyButtonPressed(self, sender, args):
        try:
            result = True
            if self.tabControl.SelectedIndex == 0:
                file = self.tracklistBox.SelectedItem
                destinationPath = MainForm.BuildPath + '/pf/sound/netplaylist/'
                filePath = destinationPath + file.Name
                folderName = "netplaylist"
            else:
                file = self.netplaylistBox.SelectedItem
                destinationPath = MainForm.BuildPath + '/pf/sound/tracklist/'
                filePath = destinationPath + file.Name
                folderName = "tracklist"
            if File.Exists(filePath):
                result = BrawlAPI.ShowYesNoPrompt("A file with that name already exists in the " + folderName + " folder. Would you like to replace it?", "Overwrite?")
            if result:
                copyFile(file.FullName, destinationPath)
                self.refreshListbox()
                BrawlAPI.ShowMessage("File copied successfully.", "Success")
        except Exception as e:
            writeLog("ERROR " + str(e))
            if 'progressBar' in locals():
                progressBar.Finish()
            BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
            BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
            self.DialogResult = DialogResult.Abort
            self.Close()

    def setSelectedItem(self, name):
        if name:
            i = 0
            if self.tabControl.SelectedIndex == 0:
                while i < len(self.tracklistBox.Items):
                    if self.tracklistBox.Items[i].Name == name + '.tlst':
                        self.tracklistBox.SelectedItem = self.tracklistBox.Items[i]
                        break
                    i += 1
            else:
                while i < len(self.netplaylistBox.Items):
                    if self.netplaylistBox.Items[i].Name == name + '.tlst':
                        self.netplaylistBox.SelectedItem = self.netplaylistBox.Items[i]
                        break
                    i += 1
    
    def refreshListbox(self):
        tracklistIndex = 0
        if len(self.tracklistBox.Items) > 0 and self.tracklistBox.SelectedIndex:
            tracklistIndex = self.tracklistBox.SelectedIndex
        self.tracklistBox.DataSource = None
        self.tracklists = getTracklists()
        self.tracklistBox.DataSource = self.tracklists
        if len(self.tracklistBox.Items) > 0 and self.tabControl.SelectedIndex == 0:
            if tracklistIndex < len(self.tracklistBox.Items):
                self.tracklistBox.SelectedIndex = tracklistIndex
            else:
                self.tracklistBox.SelectedIndex = len(self.tracklistBox.Items) - 1
        netplayIndex = 0
        if len(self.netplaylistBox.Items) > 0 and self.netplaylistBox.SelectedIndex:
            netplayIndex = self.netplaylistBox.SelectedIndex
        self.netplaylistBox.DataSource = None
        self.netplaylists = getTracklists(True)
        self.netplaylistBox.DataSource = self.netplaylists
        if len(self.netplaylistBox.Items) > 0 and self.tabControl.SelectedIndex == 1:
            if netplayIndex < len(self.netplaylistBox.Items):
                self.netplaylistBox.SelectedIndex = netplayIndex
            else:
                self.netplaylistBox.SelectedIndex = len(self.netplaylistBox.Items) - 1

#endregion

#region TRACKLIST EDITOR

class TracklistEditor(Form):

    def __init__(self, tracklistFile, netplay=False):
        # Form parameters
        self.Text = 'Tracklist Editor'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.MinimumSize = Size(411,400)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.tracklistFile = tracklistFile
        self.songs = BindingSource()
        if self.tracklistFile:
            self.songs.DataSource = getTracklistSongs(self.tracklistFile)
        else:
            newTlstEntry = TLSTEntryNode()
            newTlstEntry.Name = "New_Song"
            newTlstEntry.SongID = 61440
            self.songs.DataSource = [ Song(newTlstEntry, newTlstEntry.Name)]

        self.removeBrstms = []
        self.newName = ""
        self.netplay = netplay

        self.songListBox = ListBox()
        self.songListBox.Width = 120
        self.songListBox.Height = 240
        self.songListBox.Location = Point(16, 32)
        self.songListBox.DataSource = self.songs
        self.songListBox.ValueMember = "songNode"
        self.songListBox.SelectedValueChanged += self.songChanged

        addButton = Button()
        addButton.Text = "+"
        addButton.Location = Point(16, 272)
        addButton.Width = 16
        addButton.Height = 16
        addButton.Click += self.addButtonPressed

        removeButton = Button()
        removeButton.Text = "-"
        removeButton.Location = Point(32, 272)
        removeButton.Width = 16
        removeButton.Height = 16
        removeButton.Click += self.removeButtonPressed

        importButton = Button()
        importButton.Text = "Import"
        importButton.Location = Point(16, 292)
        importButton.Click += self.importButtonPressed

        listBoxLabel = Label()
        listBoxLabel.Text = "Songs"
        listBoxLabel.Height = 16
        listBoxLabel.Location = Point(16, 8)

        self.nameTextBox = TextBox()
        self.nameTextBox.Location = Point(248, 32)
        self.nameTextBox.TextChanged += self.nameTextChanged

        nameLabel = Label()
        nameLabel.Text = "Name:"
        nameLabel.Location = Point(136, 32)
        nameLabel.Height = 16
        nameLabel.TextAlign = ContentAlignment.TopRight

        self.songTextBox = TextBox()
        self.songTextBox.Location = Point(248, 64)
        self.songTextBox.TextChanged += self.songTextChanged

        songLabel = Label()
        songLabel.Text = "Song File Name:"
        songLabel.Location = Point(136, 64)
        songLabel.Height = 16
        songLabel.TextAlign = ContentAlignment.TopRight

        self.songFileBox = TextBox()
        self.songFileBox.Location = Point(248, 88)
        self.songFileBox.ReadOnly = True

        songFileButton = Button()
        songFileButton.Location = Point(355, 63)
        songFileButton.Text = "Browse..."
        songFileButton.Click += self.songFileButtonPressed

        self.volumeBar = TrackBar()
        self.volumeBar.Minimum = 0
        self.volumeBar.Maximum = 127
        self.volumeBar.Location = Point(248, 128)
        self.volumeBar.TickFrequency = 9
        self.volumeBar.TickStyle = TickStyle.BottomRight
        self.volumeBar.SmallChange = 1
        self.volumeBar.LargeChange = 9
        self.volumeBar.ValueChanged += self.volumeBarChanged

        volumeLabel = Label()
        volumeLabel.Text = "Volume:"
        volumeLabel.Location = Point(136, 128)
        volumeLabel.Height = 16
        volumeLabel.TextAlign = ContentAlignment.TopRight

        self.volumeText = NumericUpDown()
        self.volumeText.Location = Point(360, 128)
        self.volumeText.Width = 48
        self.volumeText.Maximum = 127
        self.volumeText.Minimum = 0
        self.volumeText.TextChanged += self.volumeTextChanged

        self.frequencyBar = TrackBar()
        self.frequencyBar.Minimum = 0
        self.frequencyBar.Maximum = 100
        self.frequencyBar.Location = Point(248, 176)
        self.frequencyBar.TickFrequency = 10
        self.frequencyBar.TickStyle = TickStyle.BottomRight
        self.frequencyBar.SmallChange = 1
        self.frequencyBar.LargeChange = 10
        self.frequencyBar.ValueChanged += self.frequencyBarChanged

        frequencyLabel = Label()
        frequencyLabel.Text = "Frequency:"
        frequencyLabel.Location = Point(136, 176)
        frequencyLabel.Height = 16
        frequencyLabel.TextAlign = ContentAlignment.TopRight

        self.frequencyText = NumericUpDown()
        self.frequencyText.Location = Point(360, 176)
        self.frequencyText.Width = 48
        self.frequencyText.Maximum = 100
        self.frequencyText.Minimum = 0
        self.frequencyText.TextChanged += self.frequencyTextChanged

        self.songDelayText = NumericUpDown()
        self.songDelayText.Location = Point(248, 224)
        self.songDelayText.Width = 48
        self.songDelayText.Minimum = -1
        self.songDelayText.TextChanged += self.songDelayTextChanged

        songDelayLabel = Label()
        songDelayLabel.Location = Point(136, 224)
        songDelayLabel.Height = 16
        songDelayLabel.Text = "Delay:"
        songDelayLabel.TextAlign = ContentAlignment.TopRight

        self.songSwitchText = NumericUpDown()
        self.songSwitchText.Location = Point(360, 224)
        self.songSwitchText.Width = 48
        self.songSwitchText.Minimum = 0
        self.songSwitchText.TextChanged += self.songSwitchTextChanged

        songSwitchLabel = Label()
        songSwitchLabel.Location = Point(248, 224)
        songSwitchLabel.Height = 16
        songSwitchLabel.Text = "Switch:"
        songSwitchLabel.TextAlign = ContentAlignment.TopRight

        self.stockPinchCheckbox = CheckBox()
        self.stockPinchCheckbox.Location = Point(248, 256)
        self.stockPinchCheckbox.Text = "Disable Stock Pinch?"
        self.stockPinchCheckbox.Height = 32
        self.stockPinchCheckbox.CheckedChanged += self.stockPinchCheckChanged

        self.audioPlayer = AudioPlaybackPanel()
        self.audioPlayer.Location = Point(32, 328)
        if len(self.songs) > 0:
            self.audioPlayer.TargetSource = self.songs[0].songNode
        self.audioPlayer.Visible = False

        saveButton = Button()
        saveButton.Location = Point(256, 466)
        saveButton.Text = "Save and Close"
        saveButton.Width = 96
        saveButton.Click += self.saveButtonPressed

        cancelButton = Button()
        cancelButton.Text = "Cancel"
        cancelButton.Location = Point(360, 466)
        cancelButton.Click += self.cancelButtonPressed
        cancelButton.Width = 96

        self.Controls.Add(self.songListBox)
        self.Controls.Add(listBoxLabel)
        self.Controls.Add(addButton)
        self.Controls.Add(removeButton)
        self.Controls.Add(importButton)
        self.Controls.Add(self.nameTextBox)
        self.Controls.Add(nameLabel)
        self.Controls.Add(self.songTextBox)
        self.Controls.Add(songLabel)
        self.Controls.Add(songFileButton)
        self.Controls.Add(self.songFileBox)
        self.Controls.Add(self.volumeBar)
        self.Controls.Add(volumeLabel)
        self.Controls.Add(self.volumeText)
        self.Controls.Add(frequencyLabel)
        self.Controls.Add(self.frequencyBar)
        self.Controls.Add(self.frequencyText)
        self.Controls.Add(self.songDelayText)
        self.Controls.Add(songDelayLabel)
        self.Controls.Add(self.songSwitchText)
        self.Controls.Add(songSwitchLabel)
        self.Controls.Add(self.stockPinchCheckbox)
        self.Controls.Add(saveButton)
        self.Controls.Add(cancelButton)
        self.Controls.Add(self.audioPlayer)

        # Tooltips
        toolTip = ToolTip()
        toolTip.SetToolTip(listBoxLabel, "The songs in this tracklist")
        toolTip.SetToolTip(nameLabel, "The name of the song as it appears in-game")
        toolTip.SetToolTip(songLabel, "The folder and filename for this song e.g. a song called Mario in the Super Mario folder would be written as Super Mario/Mario")
        toolTip.SetToolTip(volumeLabel, "The volume the song plays at in-game")
        toolTip.SetToolTip(frequencyLabel, "The frequency the song will appear in-game")
        toolTip.SetToolTip(songDelayLabel, "The number of frames to wait before playing the song on match start")
        toolTip.SetToolTip(songSwitchLabel, "The time (in frames) remaining in a match to switch to another track, if one is set")
        toolTip.SetToolTip(self.stockPinchCheckbox, "If checked, alternate track will play without players being low on stocks during a match, if one is set")

    def songChanged(self, sender, args):
        self.audioPlayer.TargetSource = self.songListBox.SelectedValue
        self.setAudioPlayerVisibility()
        self.songTextBox.Text = self.songListBox.SelectedValue.SongFileName
        self.nameTextBox.Text = self.songListBox.SelectedValue.Name
        self.volumeBar.Value = self.songListBox.SelectedValue.Volume
        self.volumeText.Text = str(self.songListBox.SelectedValue.Volume)
        self.frequencyBar.Value = self.songListBox.SelectedValue.Frequency
        self.frequencyText.Text = str(self.songListBox.SelectedValue.Frequency)
        self.songDelayText.Text = str(self.songListBox.SelectedValue.SongDelay)
        self.songSwitchText.Text = str(self.songListBox.SelectedValue.SongSwitch)
        self.stockPinchCheckbox.Checked = self.songListBox.SelectedValue.DisableStockPinch
        self.songFileBox.Text = self.songListBox.SelectedItem.brstmFile
    
    def setAudioPlayerVisibility(self):
        if not self.songListBox.SelectedValue.SongFileName:
            self.audioPlayer.Visible = False
        elif '/' not in self.songListBox.SelectedValue.SongFileName:
            self.audioPlayer.Visible = False
        elif not File.Exists(MainForm.BuildPath + '/pf/sound/strm/' + self.songListBox.SelectedValue.SongFileName + '.brstm'):
            self.audioPlayer.Visible = False
        else:
            self.audioPlayer.Visible = True

    def nameTextChanged(self, sender, args):
        if self.songListBox.SelectedValue:
            self.songListBox.SelectedValue.Name = self.nameTextBox.Text

    def initializeAudioPlayer(self):
        self.audioPlayer.Dispose()
        self.audioPlayer = AudioPlaybackPanel()
        self.audioPlayer.Location = Point(32, 328)
        self.audioPlayer.TargetSource = self.songs[self.songListBox.SelectedIndex].songNode
        self.setAudioPlayerVisibility()
        self.Controls.Add(self.audioPlayer)

    def songTextChanged(self, sender, args):
        if self.songListBox.SelectedValue:
            self.songListBox.SelectedValue.SongFileName = self.songTextBox.Text
            if not self.songListBox.SelectedItem.originalBrstm:
                self.songListBox.SelectedItem.originalBrstm = self.songListBox.SelectedValue.rstmPath
            self.initializeAudioPlayer()

    def volumeBarChanged(self, sender, args):
        self.volumeText.Text = str(self.volumeBar.Value)
        if self.songListBox.SelectedValue:
            self.songListBox.SelectedValue.Volume = self.volumeBar.Value
    
    def volumeTextChanged(self, sender, args):
        if int(self.volumeText.Text) > self.volumeText.Maximum:
            self.volumeText.Text = str(self.volumeText.Maximum)
        if int(self.volumeText.Text) <= self.volumeText.Minimum:
            self.volumeText.Text = str(self.volumeText.Minimum)
        self.volumeBar.Value = int(self.volumeText.Text)
        if self.songListBox.SelectedValue:
            self.songListBox.SelectedValue.Volume = int(self.volumeText.Text)

    def frequencyBarChanged(self, sender, args):
        self.frequencyText.Text = str(self.frequencyBar.Value)
        if self.songListBox.SelectedValue:
            self.songListBox.SelectedValue.Frequency = self.frequencyBar.Value
    
    def frequencyTextChanged(self, sender, args):
        if int(self.frequencyText.Text) > self.frequencyText.Maximum:
            self.frequencyText.Text = str(self.frequencyText.Maximum)
        if int(self.frequencyText.Text) <= self.frequencyText.Minimum:
            self.frequencyText.Text = str(self.frequencyText.Minimum)
        self.frequencyBar.Value = int(self.frequencyText.Text)
        if self.songListBox.SelectedValue:
            self.songListBox.SelectedValue.Frequency = int(self.frequencyText.Text)

    def songDelayTextChanged(self, sender, args):
        if self.songListBox.SelectedValue:
            self.songListBox.SelectedValue.SongDelay = int(self.songDelayText.Text)

    def songSwitchTextChanged(self, sender, args):
        if self.songListBox.SelectedValue:
            self.songListBox.SelectedValue.SongSwitch = int(self.songSwitchText.Text)

    def stockPinchCheckChanged(self, sender, args):
        if self.songListBox.SelectedValue:
            self.songListBox.SelectedValue.DisableStockPinch = self.stockPinchCheckbox.Checked

    def cancelButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Close()

    def songFileButtonPressed(self, sender, args):
        if self.songListBox.SelectedValue:
            brstmFile = BrawlAPI.OpenFileDialog("Select your BRSTM file", "BRSTM files|*.brstm")
            brstmFolder = ""
            brstmPath = MainForm.BuildPath + '\\pf\\sound\\strm\\'
            newFile = ""
            if brstmFile:
                while True:
                    brstmFolder = BrawlAPI.OpenFolderDialog("Select the folder you would like to place this BRSTM file")
                    if brstmFolder:
                        if brstmPath in brstmFolder:
                            newFile = brstmFolder.replace(brstmPath, '') + '/' + getFileInfo(brstmFile).Name.split('.brstm')[0]
                            break
                        else:
                            BrawlAPI.ShowMessage("This folder is not in the strm folder in your build! Please choose a folder in the correct location.", "Incorrect Folder Placement")
                    else:
                        break
            self.songListBox.SelectedValue.SongFileName = newFile
            if not File.Exists(self.songListBox.SelectedValue.rstmPath):
                self.songListBox.SelectedItem.brstmFile = brstmFile
                self.songFileBox.Text = brstmFile
            self.songTextBox.Text = newFile

    def saveButtonPressed(self, sender, args):
        try:
            self.newName = updateTracklist(self.tracklistFile, self.songs, self.netplay)
            for song in self.songListBox.Items:
                if song.originalBrstm and song.originalBrstm != song.songNode.rstmPath:
                    self.removeBrstms.append(song.originalBrstm)
            deleteBrstms(self.removeBrstms)
            self.DialogResult = DialogResult.OK
            self.Close()
        except Exception as e:
            writeLog("ERROR " + str(e))
            if 'progressBar' in locals():
                progressBar.Finish()
            BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
            BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
            self.DialogResult = DialogResult.Abort
            self.Close()

    def addButtonPressed(self, sender, args):
        newSong = TLSTEntryNode()
        newSong.SongID = getSongIdFromSongList(self.songs)
        newSong.Name = "New_Song"
        newSong.Volume = 80
        newSong.Frequency = 40
        song = Song(newSong, newSong.Name)
        self.songs.Add(song)
        self.songListBox.SelectedItem = song

    def removeButtonPressed(self, sender, args):
        if len(self.songs) > 1:
            self.removeBrstms.append(self.songListBox.SelectedItem.originalBrstm)
            self.songs.Remove(self.songListBox.SelectedItem)

    def importButtonPressed(self, sender, args):
        files = BrawlAPI.OpenMultiFileDialog("Select your BRSTM files", "BRSTM files|*.brstm")
        brstmPath = MainForm.BuildPath + '\\pf\\sound\\strm\\'
        brstmFolder = ""
        while True:
            brstmFolder = BrawlAPI.OpenFolderDialog("Select the folder you would like to place these BRSTM files")
            if brstmFolder:
                if brstmPath in brstmFolder:
                    break
                else:
                    BrawlAPI.ShowMessage("This folder is not in the strm folder in your build! Please choose a folder in the correct location.", "Incorrect Folder Placement")
            else:
                break
        for brstmFile in files:
            newFile = ""
            fileInfo = getFileInfo(brstmFile)
            if brstmFile:
                if brstmPath in brstmFolder:
                    newFile = brstmFolder.replace(brstmPath, '') + '/' + getFileInfo(brstmFile).Name.split('.brstm')[0]
            newSong = TLSTEntryNode()
            newSong.SongID = getSongIdFromSongList(self.songs)
            newSong.Name = fileInfo.Name.split('.brstm')[0]
            newSong.Volume = 80
            newSong.Frequency = 40
            song = Song(newSong, newSong.Name)
            if not File.Exists(brstmPath + newFile + '.brstm'):
                song.brstmFile = brstmFile
            song.songNode.SongFileName = newFile
            self.songs.Add(song)
            self.songListBox.SelectedItem = song

#endregion

#region STAGE LIST

class StageList(Form):

    def __init__(self, stageLists):
        # Form parameters
        self.Text = 'Stage List'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.MinimumSize = Size(411,432)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.stageLists = stageLists

        self.length = len(self.stageLists)

        self.stageSlots = [None] * self.length
        self.unusedSlots = [None] * self.length
        self.removeSlots = []
        fileOpened = False

        # Get stage lists
        i = 0
        while i < self.length:
            self.stageSlots[i] = BindingSource()
            self.stageSlots[i].DataSource = []

            pageNumber = 0
            if not fileOpened:
                fileOpened = BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/stage/stageslot/')
            if fileOpened:
                pages = getStageList(self.stageLists[i])
                for page in pages:
                    pageNumber += 1
                    pageSlot = StageSlot('0x00', '00', '00', '0000', '|| PAGE ' + str(pageNumber) + ' ||')
                    self.stageSlots[i].Add(pageSlot)
                    for slotId in page:
                        stageIds = getStageIdsByNumber(slotId, self.stageLists[i])
                        stageName = getStageName(stageIds[2:4])
                        stageSlot = StageSlot(slotId, stageIds[2:4], stageIds[4:6], stageIds[2:6], stageName)
                        self.stageSlots[i].Add(stageSlot)

            self.unusedSlots[i] = BindingSource()
            self.unusedSlots[i].DataSource = getUnusedStageSlots(self.stageSlots[i], self.stageLists[i])
            i += 1
        BrawlAPI.ForceCloseFile()

        # Set up controls
        self.tabControl = TabControl()
        self.tabControl.Dock = DockStyle.Fill

        tabs = [None] * self.length

        self.listBox = [None] * self.length
        listBoxLabel = [None] * self.length
        self.unusedListbox = [None] * self.length
        unusedListBoxLabel = [None] * self.length
        button = [None] * self.length
        addButton = [None] * self.length
        removeButton = [None] * self.length
        moveLeftButton = [None] * self.length
        moveRightButton = [None] * self.length
        moveUpButton = [None] * self.length
        moveDownButton = [None] * self.length
        saveButton = [None] * self.length
        cancelButton = [None] * self.length

        i = 0
        while i < self.length:

            if self.stageLists[i] == '/Source/Project+/StageFiles.asm' or self.stageLists[i] == '/Source/Project+/StageTable.asm':
                tabPageName = 'Standard'
            elif self.stageLists[i] == '/Source/Netplay/Net-StageFiles.asm':
                tabPageName = 'Netplay'
            elif File.Exists(MainForm.BuildPath + self.stageLists[i]):
                tabPageName = getFileInfo(MainForm.BuildPath + self.stageLists[i]).Name.replace('.asm','')
            else:
                tabPageName = self.stageLists[i]

            tabs[i] = TabPage()
            tabs[i].Text = tabPageName

            self.tabControl.Controls.Add(tabs[i])

            self.listBox[i] = ListBox()
            self.listBox[i].Width = 120
            self.listBox[i].Height = 240
            self.listBox[i].Location = Point(16, 32)
            self.listBox[i].DataSource = self.stageSlots[i]
            self.listBox[i].DisplayMember = "name"
            self.listBox[i].ValueMember = "fullId"
            self.listBox[i].DrawMode = DrawMode.OwnerDrawFixed
            self.listBox[i].DrawItem += self.listBoxDrawItem

            listBoxLabel[i] = Label()
            listBoxLabel[i].Text = "Current Stages"
            listBoxLabel[i].Height = 16
            listBoxLabel[i].Location = Point(16, 8)

            self.unusedListbox[i] = ListBox()
            self.unusedListbox[i].Width = 120
            self.unusedListbox[i].Height = 240
            self.unusedListbox[i].Location = Point(259, 32)
            self.unusedListbox[i].DataSource = self.unusedSlots[i]
            self.unusedListbox[i].DisplayMember = "name"
            self.unusedListbox[i].ValueMember = "fullId"

            unusedListBoxLabel[i] = Label()
            unusedListBoxLabel[i].Text = "Unused Stages"
            unusedListBoxLabel[i].Height = 16
            unusedListBoxLabel[i].Location = Point(259, 8)

            button[i] = Button()
            button[i].Location = Point(16, 276)
            button[i].Text = "Edit"
            button[i].Click += self.buttonPressed

            addButton[i] = Button()
            addButton[i].Location = Point(16, 332)
            addButton[i].Text = "Add"
            addButton[i].Click += self.addButtonPressed

            removeButton[i] = Button()
            removeButton[i].Location = Point(16, 304)
            removeButton[i].Text = "Delete"
            removeButton[i].Click += self.removeButtonPressed

            moveLeftButton[i] = Button()
            moveLeftButton[i].Location = Point(160, 120)
            moveLeftButton[i].Text = "←"
            moveLeftButton[i].Click += self.moveLeftButtonPressed

            moveRightButton[i] = Button()
            moveRightButton[i].Location = Point(160, 152)
            moveRightButton[i].Text = "→"
            moveRightButton[i].Click += self.moveRightButtonPressed

            moveUpButton[i] = Button()
            moveUpButton[i].Location = Point(136, 31)
            moveUpButton[i].Text = "↑"
            moveUpButton[i].Size = Size(16, 32)
            moveUpButton[i].Click += self.moveUpButtonPressed

            moveDownButton[i] = Button()
            moveDownButton[i].Location = Point(136, 63)
            moveDownButton[i].Text = "↓"
            moveDownButton[i].Size = Size(16, 32)
            moveDownButton[i].Click += self.moveDownButtonPressed

            saveButton[i] = Button()
            saveButton[i].Location = Point(304, 304)
            saveButton[i].Text = "Save"
            saveButton[i].Click += self.saveButtonPressed

            cancelButton[i] = Button()
            cancelButton[i].Location = Point(304, 332)
            cancelButton[i].Text = "Close"
            cancelButton[i].Click += self.cancelButtonPressed

            i += 1

        # Add controls to tabs

        self.Controls.Add(self.tabControl)
        i = 0
        while i < self.length:

            tabs[i].Controls.Add(listBoxLabel[i])
            tabs[i].Controls.Add(self.listBox[i])
            tabs[i].Controls.Add(button[i])
            tabs[i].Controls.Add(removeButton[i])
            tabs[i].Controls.Add(addButton[i])
            tabs[i].Controls.Add(moveUpButton[i])
            tabs[i].Controls.Add(moveDownButton[i])
            tabs[i].Controls.Add(moveLeftButton[i])
            tabs[i].Controls.Add(moveRightButton[i])
            tabs[i].Controls.Add(self.unusedListbox[i])
            tabs[i].Controls.Add(unusedListBoxLabel[i])
            tabs[i].Controls.Add(saveButton[i])
            tabs[i].Controls.Add(cancelButton[i])

            # Tooltips
            toolTip = ToolTip()
            toolTip.SetToolTip(listBoxLabel[i], "Stage slots currently in stage list")
            toolTip.SetToolTip(unusedListBoxLabel[i], "Stage slots not added to stage list")

            i += 1

    def listBoxDrawItem(self, sender, args):
        args.DrawBackground()
        if sender.Items[args.Index].name.startswith("|| PAGE"):
            font = Font("Arial", 10, FontStyle.Bold)
        else:
            font = args.Font
        selected = args.ForeColor == SystemColors.HighlightText
        args.Graphics.DrawString(sender.Items[args.Index].name, font, Brushes.Black if not selected else Brushes.White, args.Bounds, StringFormat.GenericDefault)
        args.DrawFocusRectangle
        
    def buttonPressed(self, sender, args):
        if self.listBox[self.tabControl.SelectedIndex].SelectedItem.name.startswith('|| PAGE '):
            return
        else:
            fullId = str(self.listBox[self.tabControl.SelectedIndex].SelectedValue)
        form = StageEditor(fullId)
        result = form.ShowDialog(MainForm.Instance)
        form.Dispose()
        if result == DialogResult.Abort:
            self.DialogResult = DialogResult.Abort
            self.Close()

    def removeButtonPressed(self, sender, args):
        index = self.tabControl.SelectedIndex
        if self.listBox[index].SelectedItem.name.startswith('|| PAGE '):
            return
        else:
            toRemove = self.listBox[index].SelectedItem
            self.removeSlots.append(self.listBox[index].SelectedItem)
            for stageSlotList in self.stageSlots:
                i = 0
                while i < len(stageSlotList):
                    if stageSlotList[i].fullId == toRemove.fullId:
                        stageSlotList.Remove(stageSlotList[i])
                    i += 1
            for stageSlotList in self.unusedSlots:
                i = 0
                while i < len(stageSlotList):
                    if stageSlotList[i].fullId == toRemove.fullId:
                        stageSlotList.Remove(stageSlotList[i])
                    i += 1

    def addButtonPressed(self, sender, args):
        newId = self.getFirstAvailableId()
        form = StageEditor(newId, True, self.stageLists)
        result = form.ShowDialog(MainForm.Instance)
        if result == DialogResult.OK:
            newSlot = None
            if form.newSlotNumber != []:
                i = 0
                while i < len(form.newSlotNumber):
                    newSlot = StageSlot(hexId(form.newSlotNumber[i]), newId[0:2], newId[2:4], newId[0:4], form.alts[0].aslEntry.Name)
                    self.unusedSlots[i].Add(newSlot)
                    self.unusedListbox[i].SelectedItem = newSlot
                    i += 1
            BrawlAPI.ShowMessage("Stage added successfully.", "Success")
            form.Dispose()
        elif result == DialogResult.Abort:
            form.Dispose()
            self.DialogResult = DialogResult.Abort
            self.Close()

    def moveLeftButtonPressed(self, sender, args):
        index = self.tabControl.SelectedIndex
        if len(self.unusedSlots[index]) > 0 and not self.unusedListbox[index].SelectedItem.name.startswith('|| PAGE'):
            self.stageSlots[index].Add(self.unusedListbox[index].SelectedItem)
            self.listBox[index].SelectedItem = self.unusedListbox[index].SelectedItem
            self.unusedSlots[index].Remove(self.unusedListbox[index].SelectedItem)

    def moveRightButtonPressed(self, sender, args):
        index = self.tabControl.SelectedIndex
        if len(self.stageSlots[index]) > 0 and not self.listBox[index].SelectedItem.name.startswith('|| PAGE'):
            self.unusedSlots[index].Add(self.listBox[index].SelectedItem)
            self.unusedListbox[index].SelectedItem = self.listBox[index].SelectedItem
            self.stageSlots[index].Remove(self.listBox[index].SelectedItem)

    def moveUpButtonPressed(self, sender, args):
        i = self.tabControl.SelectedIndex
        if self.listBox[i].SelectedIndex == 1 or self.listBox[i].SelectedItem.name.startswith('|| PAGE'):
            return
        aboveValue = self.stageSlots[i][self.listBox[i].SelectedIndex - 1]
        selectedValue = self.stageSlots[i][self.listBox[i].SelectedIndex]
        self.stageSlots[i][self.listBox[i].SelectedIndex - 1] = selectedValue
        self.stageSlots[i][self.listBox[i].SelectedIndex] = aboveValue
        self.listBox[i].SelectedIndex = self.listBox[i].SelectedIndex - 1

    def moveDownButtonPressed(self, sender, args):
        i = self.tabControl.SelectedIndex
        if self.listBox[i].SelectedIndex >= len(self.listBox[i].Items) - 1 or self.listBox[i].SelectedItem.name.startswith('|| PAGE'):
            return
        belowValue = self.stageSlots[i][self.listBox[i].SelectedIndex + 1]
        selectedValue = self.stageSlots[i][self.listBox[i].SelectedIndex]
        self.stageSlots[i][self.listBox[i].SelectedIndex + 1] = selectedValue
        self.stageSlots[i][self.listBox[i].SelectedIndex] = belowValue
        self.listBox[i].SelectedIndex = self.listBox[i].SelectedIndex + 1

    def saveButtonPressed(self, sender, args):
        try:
            if len(self.removeSlots) > 0:
                removeStageSlot(self.removeSlots, self.stageLists)
            for slot in self.removeSlots:
                if File.Exists(MainForm.BuildPath + "/pf/stage/stageslot/" + addLeadingZeros(slot.stageId.strip().replace('0x',''), 2) + ".asl"):
                    File.Delete(MainForm.BuildPath + "/pf/stage/stageslot/" + addLeadingZeros(slot.stageId.strip().replace('0x',''), 2) + ".asl")
            i = 0
            while i < self.length:
                updateStageList(self.listBox[i].Items, self.stageLists[i])
                i += 1
            buildGct()
            self.removeSlots = []
            BrawlAPI.ShowMessage("Saved successfully.", "Success")
        except Exception as e:
            writeLog("ERROR " + str(e))
            if 'progressBar' in locals():
                progressBar.Finish()
            BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
            BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
            self.DialogResult = DialogResult.Abort
            self.Close()

    def cancelButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Close()

    def getFirstAvailableId(self):
        # Compile stage IDs
        usedStageIds = []
        for stageList in self.stageSlots:
            for stageSlot in stageList:
                usedStageIds.append(stageSlot.stageId)
        for stageList in self.unusedSlots:
            for stageSlot in stageList:
                usedStageIds.append(stageSlot.stageId)
        for stageSlot in self.removeSlots:
            usedStageIds.append(stageSlot.stageId)
        # Get first available
        stageId = 1
        while hexId(stageId).replace('0x','') in usedStageIds:
            stageId += 1
        # Compile cosmetic IDs
        usedCosmeticIds = []
        for stageList in self.stageSlots:
            for stageSlot in stageList:
                usedCosmeticIds.append(stageSlot.cosmeticId)
        for stageList in self.unusedSlots:
            for stageSlot in stageList:
                usedCosmeticIds.append(stageSlot.cosmeticId)
        for stageSlot in self.removeSlots:
            usedCosmeticIds.append(stageSlot.cosmeticId)
        # Get first available
        cosmeticId = 1
        while hexId(cosmeticId).replace('0x','') in usedCosmeticIds:
            cosmeticId += 1
        return hexId(stageId).replace('0x', '') + hexId(cosmeticId).replace('0x', '')

#endregion

#region EDIT STAGE

class StageEditor(Form):

    def __init__(self, fullId, new=False, stageLists=['/Source/Project+/StageFiles.asm', '/Source/Netplay/Net-StageFiles.asm']):
        # Form parameters
        self.Text = 'Edit Stage'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.MinimumSize = Size(250,128)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.cosmetics = getStageCosmetics(fullId[2:4])
        self.alts = BindingSource()
        self.alts.DataSource = getStageAltInfo(fullId[0:2])
        self.addedTracks = BindingSource()
        self.addedTracks.DataSource = []

        self.stageLists = stageLists

        # Variables
        self.newIcon = ""
        self.newName = ""
        self.newPreview = ""
        self.newFranchiseIcon = ""
        self.newGameLogo = ""
        self.newAltName = ""
        self.addedFranchiseIcons = []
        self.addedGameLogos = []
        self.removeSlots = []
        self.cosmeticId = fullId[2:4]
        self.stageId = fullId[0:2]
        self.new = new
        self.newSlotNumber = []

        self.franchiseIconList = BindingSource()
        self.franchiseIconList.DataSource = self.cosmetics.franchiseIconList

        self.gameLogoList = BindingSource()
        self.gameLogoList.DataSource = self.cosmetics.gameLogoList

        self.tracklistFiles = self.getTracklists()

        # Cosmetics Groupbox
        cosmeticsGroupBox = GroupBox()
        cosmeticsGroupBox.Location = Point(0,0)
        cosmeticsGroupBox.AutoSize = True
        cosmeticsGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        cosmeticsGroupBox.Text = "Cosmetics"

        # Stage Name
        self.namePictureBox = PictureBox()
        self.namePictureBox.Location = Point(16, 192)
        self.namePictureBox.Width = 208
        self.namePictureBox.Height = 56
        self.namePictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.stageName and not self.new:
            self.namePictureBox.Image = self.cosmetics.stageName

        nameImageLabel = Label()
        nameImageLabel.Text = "Name:"
        nameImageLabel.Location = Point(16, 176)
        nameImageLabel.Height = 16

        nameButton = Button()
        nameButton.Text = "Import"
        nameButton.Location = Point(16, 252)
        nameButton.Click += self.nameButtonPressed

        # Stage R-Alt Name
        self.altNamePictureBox = PictureBox()
        self.altNamePictureBox.Location = Point(16, 296)
        self.altNamePictureBox.Width = 208
        self.altNamePictureBox.Height = 56
        self.altNamePictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.altName and not self.new:
            self.altNamePictureBox.Image = self.cosmetics.altName.image

        altLabel = Label()
        altLabel.Text = "Alt Layout Name:"
        altLabel.Location = Point(16, 280)

        self.altDropDown = ComboBox()
        self.altDropDown.DropDownStyle = ComboBoxStyle.DropDownList
        self.altDropDown.Location = Point(16, 356)
        self.altDropDown.Width = 208
        self.altDropDown.BindingContext = self.BindingContext
        self.altDropDown.DataSource = self.cosmetics.stageNameList
        self.altDropDown.DisplayMember = "name"
        self.altDropDown.ValueMember = "image"
        self.altDropDown.SelectedValueChanged += self.altDropDownChanged

        # Stage Icon
        self.iconPictureBox = PictureBox()
        self.iconPictureBox.Location = Point(240, 192)
        self.iconPictureBox.Width = 128
        self.iconPictureBox.Height = 112
        self.iconPictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.stageIcon and not self.new:
            self.iconPictureBox.Image = self.cosmetics.stageIcon

        iconLabel = Label()
        iconLabel.Text = "Icon:"
        iconLabel.Location = Point(240, 176)
        iconLabel.Height = 16

        iconButton = Button()
        iconButton.Text = "Import"
        iconButton.Location = Point(240, 308)
        iconButton.Click += self.iconButtonPressed

        # Franchise Icon
        self.franchiseIconPictureBox = PictureBox()
        self.franchiseIconPictureBox.Location = Point(16, 398)
        self.franchiseIconPictureBox.Width = 64
        self.franchiseIconPictureBox.Height = 64
        self.franchiseIconPictureBox.SizeMode = PictureBoxSizeMode.StretchImage
        if self.cosmetics.franchiseIcon and not self.new:
            self.franchiseIconPictureBox.Image = self.cosmetics.franchiseIcon.image

        franchiseIconLabel = Label()
        franchiseIconLabel.Text = "Franchise Icon:"
        franchiseIconLabel.Location = Point(16, 382)
        franchiseIconLabel.Height = 16

        self.franchiseIconDropDown = ComboBox()
        self.franchiseIconDropDown.DropDownStyle = ComboBoxStyle.DropDownList
        self.franchiseIconDropDown.Location = Point(16, 466)
        self.franchiseIconDropDown.BindingContext = self.BindingContext
        self.franchiseIconDropDown.DataSource = self.franchiseIconList
        self.franchiseIconDropDown.DisplayMember = "name"
        self.franchiseIconDropDown.ValueMember = "image"
        self.franchiseIconDropDown.SelectedValueChanged += self.franchiseIconDropDownChanged

        franchiseIconButton = Button()
        franchiseIconButton.Text = "Add"
        franchiseIconButton.Location = Point(16, 490)
        franchiseIconButton.Click += self.franchiseIconButtonPressed

        # Game Logo
        self.gameLogoPictureBox = PictureBox()
        self.gameLogoPictureBox.Location = Point(160, 398)
        self.gameLogoPictureBox.Width = 120
        self.gameLogoPictureBox.Height = 56
        self.gameLogoPictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.gameLogo and not self.new:
            self.gameLogoPictureBox.Image = self.cosmetics.gameLogo.image

        gameLogoLabel = Label()
        gameLogoLabel.Text = "Game Icon:"
        gameLogoLabel.Location = Point(160, 382)
        gameLogoLabel.Height = 16

        self.gameLogoDropDown = ComboBox()
        self.gameLogoDropDown.DropDownStyle = ComboBoxStyle.DropDownList
        self.gameLogoDropDown.Location = Point(160, 466)
        self.gameLogoDropDown.BindingContext = self.BindingContext
        self.gameLogoDropDown.DataSource = self.gameLogoList
        self.gameLogoDropDown.DisplayMember = "name"
        self.gameLogoDropDown.ValueMember = "image"
        self.gameLogoDropDown.SelectedValueChanged += self.gameLogoDropDownChanged

        gameLogoButton = Button()
        gameLogoButton.Text = "Add"
        gameLogoButton.Location = Point(160, 490)
        gameLogoButton.Click += self.gameLogoButtonPressed

        # Stage Preview
        self.previewPictureBox = PictureBox()
        self.previewPictureBox.Location = Point(32, 32)
        self.previewPictureBox.Width = 312
        self.previewPictureBox.Height = 112
        self.previewPictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.stagePreview and not self.new:
            self.previewPictureBox.Image = self.cosmetics.stagePreview

        previewLabel = Label()
        previewLabel.Text = "Preview:"
        previewLabel.Location = Point(32, 16)
        previewLabel.Height = 16

        previewButton = Button()
        previewButton.Text = "Import"
        previewButton.Location = Point(32, 148)
        previewButton.Click += self.previewButtonPressed

        cosmeticsGroupBox.Controls.Add(previewLabel)
        cosmeticsGroupBox.Controls.Add(self.previewPictureBox)
        cosmeticsGroupBox.Controls.Add(previewButton)
        cosmeticsGroupBox.Controls.Add(self.namePictureBox)
        cosmeticsGroupBox.Controls.Add(nameImageLabel)
        cosmeticsGroupBox.Controls.Add(nameButton)
        cosmeticsGroupBox.Controls.Add(iconLabel)
        cosmeticsGroupBox.Controls.Add(self.iconPictureBox)
        cosmeticsGroupBox.Controls.Add(iconButton)
        cosmeticsGroupBox.Controls.Add(self.altNamePictureBox)
        cosmeticsGroupBox.Controls.Add(altLabel)
        cosmeticsGroupBox.Controls.Add(self.altDropDown)
        cosmeticsGroupBox.Controls.Add(franchiseIconLabel)
        cosmeticsGroupBox.Controls.Add(self.franchiseIconPictureBox)
        cosmeticsGroupBox.Controls.Add(self.franchiseIconDropDown)
        cosmeticsGroupBox.Controls.Add(franchiseIconButton)
        cosmeticsGroupBox.Controls.Add(gameLogoLabel)
        cosmeticsGroupBox.Controls.Add(self.gameLogoPictureBox)
        cosmeticsGroupBox.Controls.Add(self.gameLogoDropDown)
        cosmeticsGroupBox.Controls.Add(gameLogoButton)

        # Parameters Groupbox
        parametersGroupBox = GroupBox()
        parametersGroupBox.Location = Point(384, 0)
        parametersGroupBox.AutoSize = True
        parametersGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        parametersGroupBox.Text = "Parameters"

        aslIndicatorGroupBox = GroupBox()
        aslIndicatorGroupBox.Location = Point(16, 304)
        aslIndicatorGroupBox.AutoSize = True
        aslIndicatorGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        aslIndicatorGroupBox.Text = "Button Combination"

        # Stage Alt Listbox
        self.stageAltListbox = ListBox()
        self.stageAltListbox.DisplayMember = "aslEntry"
        self.stageAltListbox.ValueMember = "aslEntry"
        self.stageAltListbox.DataSource = self.alts
        self.stageAltListbox.BindingContext = self.BindingContext
        self.stageAltListbox.Location = Point(16, 16)
        self.stageAltListbox.Width = 120
        self.stageAltListbox.Height = 120
        self.stageAltListbox.SelectedValueChanged += self.stageAltChanged

        stageAltAddButton = Button()
        stageAltAddButton.Text = "+"
        stageAltAddButton.Location = Point(16, 128)
        stageAltAddButton.Width = 16
        stageAltAddButton.Height = 16
        stageAltAddButton.Click += self.stageAltAddButtonPressed

        stageAltRemoveButton = Button()
        stageAltRemoveButton.Text = "-"
        stageAltRemoveButton.Location = Point(32, 128)
        stageAltRemoveButton.Width = 16
        stageAltRemoveButton.Height = 16
        stageAltRemoveButton.Click += self.stageAltRemoveButtonPressed

        stageAltImportButton = Button()
        stageAltImportButton.Text = "Import Params"
        stageAltImportButton.Location = Point(16, 152)
        stageAltImportButton.Click += self.stageAltImportButtonPressed
        stageAltImportButton.AutoSize = True
        stageAltImportButton.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.stageAltFileBox = TextBox()
        self.stageAltFileBox.Location = Point(16, 184)
        self.stageAltFileBox.Width = 120
        self.stageAltFileBox.ReadOnly = True

        # Name textbox
        self.nameTextBox = TextBox()
        self.nameTextBox.Text = self.alts[0].aslEntry.Name if len(self.alts) > 0 else ""
        self.nameTextBox.Location = Point(208, 16)
        self.nameTextBox.Width = 160
        self.nameTextBox.TextChanged += self.nameTextChanged
        self.nameTextBox.Enabled = True if len(self.alts) > 0 else False

        nameLabel = Label()
        nameLabel.Text = "Name:"
        nameLabel.Location = Point(104, 16)
        nameLabel.TextAlign = ContentAlignment.TopRight

        # PAC Name textbox
        self.pacNameTextBox = TextBox()
        self.pacNameTextBox.Text = self.alts[0].pacName if len(self.alts) > 0 else ""
        self.pacNameTextBox.Location = Point(208, 48)
        self.pacNameTextBox.Width = 160
        self.pacNameTextBox.TextChanged += self.pacNameTextChanged
        self.pacNameTextBox.Enabled = True if len(self.alts) > 0 else False

        pacNameLabel = Label()
        pacNameLabel.Text = "PAC File:"
        pacNameLabel.Location = Point(104, 48)
        pacNameLabel.TextAlign = ContentAlignment.TopRight

        self.pacNameButton = Button()
        self.pacNameButton.Text = "Browse..."
        self.pacNameButton.Location = Point(376, 47)
        self.pacNameButton.Click += self.pacNameButtonPressed
        self.pacNameButton.Enabled = True if len(self.alts) > 0 else False

        self.pacNameFileBox = TextBox()
        self.pacNameFileBox.Location = Point(208, 72)
        self.pacNameFileBox.Width = 160
        self.pacNameFileBox.ReadOnly = True

        # Module textbox
        self.moduleTextBox = TextBox()
        self.moduleTextBox.Text = self.alts[0].module if len(self.alts) > 0 else ""
        self.moduleTextBox.Location = Point(208, 104)
        self.moduleTextBox.Width = 160
        self.moduleTextBox.TextChanged += self.moduleTextChanged
        self.moduleTextBox.Enabled = True if len(self.alts) > 0 else False

        moduleLabel = Label()
        moduleLabel.Text = "Module:"
        moduleLabel.Location = Point(104, 104)
        moduleLabel.TextAlign = ContentAlignment.TopRight

        self.moduleButton = Button()
        self.moduleButton.Text = "Browse..."
        self.moduleButton.Location = Point(376, 103)
        self.moduleButton.Click += self.moduleButtonPressed
        self.moduleButton.Enabled = True if len(self.alts) > 0 else False

        self.moduleFileBox = TextBox()
        self.moduleFileBox.Location = Point(208, 128)
        self.moduleFileBox.Width = 160
        self.moduleFileBox.ReadOnly = True

        # Tracklist textbox
        self.tracklistTextBox = ComboBox()
        self.tracklistTextBox.BindingContext = self.BindingContext
        self.tracklistTextBox.DropDownStyle = ComboBoxStyle.DropDownList
        self.tracklistTextBox.DataSource = self.tracklistFiles
        self.tracklistTextBox.Location = Point(208, 160)
        self.tracklistTextBox.Width = 160
        self.tracklistTextBox.SelectedValueChanged += self.tracklistDropDownChanged
        self.tracklistTextBox.Enabled = True if len(self.alts) > 0 else False

        tracklistLabel = Label()
        tracklistLabel.Text = "Tracklist:"
        tracklistLabel.Location = Point(104, 160)
        tracklistLabel.TextAlign = ContentAlignment.TopRight

        # Soundbank textbox
        self.soundBankTextBox = TextBox()
        self.soundBankTextBox.Text = str(hexId(self.alts[0].soundBank)) if len(self.alts) > 0 else "0xFFFF"
        self.soundBankTextBox.Location = Point(208, 192)
        self.soundBankTextBox.Width = 160
        self.soundBankTextBox.TextChanged += self.soundBankTextChanged
        self.soundBankTextBox.Enabled = True if len(self.alts) > 0 else False

        soundBankLabel = Label()
        soundBankLabel.Text = "Sound Bank:"
        soundBankLabel.Location = Point(104, 192)
        soundBankLabel.TextAlign = ContentAlignment.TopRight

        self.soundBankButton = Button()
        self.soundBankButton.Text = "Browse..."
        self.soundBankButton.Location = Point(376, 191)
        self.soundBankButton.Click += self.soundBankButtonPressed
        self.soundBankButton.Enabled = True if len(self.alts) > 0 else False

        self.soundBankFileBox = TextBox()
        self.soundBankFileBox.Location = Point(208, 215)
        self.soundBankFileBox.Width = 160
        self.soundBankFileBox.ReadOnly = True

        # Effectbank textbox
        self.effectBankTextBox = TextBox()
        self.effectBankTextBox.Text = str(hexId(self.alts[0].effectBank)) if len(self.alts) > 0 else "0x0032"
        self.effectBankTextBox.Location = Point(208, 247)
        self.effectBankTextBox.Width = 160
        self.effectBankTextBox.TextChanged += self.effectBankTextChanged
        self.effectBankTextBox.Enabled = True if len(self.alts) > 0 else False

        effectBankLabel = Label()
        effectBankLabel.Text = "Effect Bank:"
        effectBankLabel.Location = Point(104, 247)
        effectBankLabel.TextAlign = ContentAlignment.TopRight

        # Button Checkboxes
        self.aslIndicator = ASLIndicator()
        self.aslIndicator.Location = Point(16, 16)
        if len(self.alts) > 0:
            self.aslIndicator.TargetNode = self.alts[0].aslEntry
        else:
            self.aslIndicator.Visible = False
        aslIndicatorGroupBox.Controls.Add(self.aslIndicator)

        saveButton = Button()
        saveButton.Text = "Save and Close"
        saveButton.Location = Point(336, 656)
        saveButton.Click += self.saveButtonPressed
        saveButton.Width = 96

        cancelButton = Button()
        cancelButton.Text = "Cancel"
        cancelButton.Location = Point(440, 656)
        cancelButton.Click += self.cancelButtonPressed
        cancelButton.Width = 96

        parametersGroupBox.Controls.Add(self.stageAltListbox)
        parametersGroupBox.Controls.Add(stageAltAddButton)
        parametersGroupBox.Controls.Add(stageAltRemoveButton)
        parametersGroupBox.Controls.Add(stageAltImportButton)
        parametersGroupBox.Controls.Add(self.stageAltFileBox)
        parametersGroupBox.Controls.Add(self.nameTextBox)
        parametersGroupBox.Controls.Add(nameLabel)
        parametersGroupBox.Controls.Add(self.pacNameTextBox)
        parametersGroupBox.Controls.Add(pacNameLabel)
        parametersGroupBox.Controls.Add(self.pacNameButton)
        parametersGroupBox.Controls.Add(self.pacNameFileBox)
        parametersGroupBox.Controls.Add(self.moduleTextBox)
        parametersGroupBox.Controls.Add(moduleLabel)
        parametersGroupBox.Controls.Add(self.moduleButton)
        parametersGroupBox.Controls.Add(self.moduleFileBox)
        parametersGroupBox.Controls.Add(self.tracklistTextBox)
        parametersGroupBox.Controls.Add(tracklistLabel)
        parametersGroupBox.Controls.Add(self.soundBankTextBox)
        parametersGroupBox.Controls.Add(soundBankLabel)
        parametersGroupBox.Controls.Add(self.soundBankButton)
        parametersGroupBox.Controls.Add(self.soundBankFileBox)
        parametersGroupBox.Controls.Add(self.effectBankTextBox)
        parametersGroupBox.Controls.Add(effectBankLabel)
        parametersGroupBox.Controls.Add(aslIndicatorGroupBox)
        parametersGroupBox.Controls.Add(saveButton)
        parametersGroupBox.Controls.Add(cancelButton)

        self.Controls.Add(cosmeticsGroupBox)
        self.Controls.Add(parametersGroupBox)

        # Tooltips
        toolTip = ToolTip()
        toolTip.SetToolTip(previewLabel, "The stage preview that displays on the stage select screen")
        toolTip.SetToolTip(nameImageLabel, "The name of the stage that shows on the stage select screen")
        toolTip.SetToolTip(iconLabel, "The stage icon that shows on the stage select screen")
        toolTip.SetToolTip(altLabel, "The name for the alternate stage layout that displays on the stage select screen")
        toolTip.SetToolTip(franchiseIconLabel, "The franchise icon for the stage that displays on the stage select screen")
        toolTip.SetToolTip(gameLogoLabel, "The game icon for the stage that displays on the stage select screen")
        toolTip.SetToolTip(nameLabel, "The internal name to use for this stage entry")
        toolTip.SetToolTip(pacNameLabel, "The name used in the .pac file for this stage entry, e.g. PeachCastle if your pac is STGPEACHCASTLE.pac")
        toolTip.SetToolTip(moduleLabel, "The name of the module file used by the stage entry, including the .rel extension")
        toolTip.SetToolTip(tracklistLabel, "The tracklist file to use for this stage entry")
        toolTip.SetToolTip(soundBankLabel, "The ID, in hexadecimal (e.g. 0x21) format, of the soundbank to use for this stage entry")
        toolTip.SetToolTip(effectBankLabel, "The ID, in hexadecimal (e.g. 0x21) format, of the effect bank to use for this stage entry")
        toolTip.SetToolTip(aslIndicatorGroupBox, "The button combination that must be held when selected on the stage select screen to play this stage entry")

        self.setComboBoxes()

    def getTracklists(self):
        tracklistFiles = []
        directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/sound/tracklist')
        for file in directory.GetFiles("*.tlst"):
            tracklistFiles.append(file.Name.split('.tlst')[0])
        return tracklistFiles

    def setComboBoxes(self):
        if not self.new:
            i = 0
            while i < len(self.cosmetics.franchiseIconList):
                if self.cosmetics.franchiseIcon and self.cosmetics.franchiseIconList[i].name == self.cosmetics.franchiseIcon.name:
                    self.franchiseIconDropDown.SelectedIndex = i
                    break
                i += 1
            i = 0
            while i < len(self.cosmetics.stageNameList):
                if self.cosmetics.altName and self.cosmetics.stageNameList[i].name == self.cosmetics.altName.name:
                    self.altDropDown.SelectedIndex = i
                    break
                i += 1
            i = 0
            while i < len(self.cosmetics.gameLogoList):
                if self.cosmetics.gameLogo and self.cosmetics.gameLogoList[i].name == self.cosmetics.gameLogo.name:
                    self.gameLogoDropDown.SelectedIndex = i
                    break
                i += 1
            i = 0
            while i < len(self.tracklistFiles):
                if self.tracklistFiles[i] == self.stageAltListbox.SelectedItem.tracklist:
                    self.tracklistTextBox.SelectedIndex = i
                    break
                i += 1
        else:
            self.franchiseIconDropDown.SelectedIndex = 0
            self.franchiseIconPictureBox.Image = Bitmap(self.franchiseIconDropDown.SelectedValue)
            self.newFranchiseIcon = self.franchiseIconDropDown.SelectedItem.name
            self.altDropDown.SelectedIndex = 0
            self.altNamePictureBox.Image = Bitmap(self.altDropDown.SelectedValue)
            self.newAltName = self.altDropDown.SelectedItem.name
            self.gameLogoDropDown.SelectedIndex = 0
            self.gameLogoPictureBox.Image = Bitmap(self.gameLogoDropDown.SelectedValue)
            self.newGameLogo = self.gameLogoDropDown.SelectedItem.name
            self.tracklistTextBox.SelectedIndex = 0

    def stageAltChanged(self, sender, args):
        if len(self.alts) > 0:
            self.aslIndicator.TargetNode = self.stageAltListbox.SelectedValue
            self.moduleTextBox.Text = self.stageAltListbox.SelectedItem.module
            self.nameTextBox.Text = self.stageAltListbox.SelectedValue.Name
            self.pacNameTextBox.Text = self.stageAltListbox.SelectedItem.pacName
            self.tracklistTextBox.SelectedItem = self.stageAltListbox.SelectedItem.tracklist
            self.soundBankTextBox.Text = str(hexId(self.stageAltListbox.SelectedItem.soundBank))
            self.effectBankTextBox.Text = str(hexId(self.stageAltListbox.SelectedItem.effectBank))
            self.pacNameFileBox.Text = self.stageAltListbox.SelectedItem.pacFile
            self.moduleFileBox.Text = self.stageAltListbox.SelectedItem.moduleFile
            self.soundBankFileBox.Text = self.stageAltListbox.SelectedItem.soundBankFile
            self.stageAltFileBox.Text = self.stageAltListbox.SelectedItem.paramFile

    def validate(self):
        validationText = ""
        if not (self.previewPictureBox.Image and self.namePictureBox.Image and self.iconPictureBox.Image):
            validationText += "\nYou must set images for the stage preview, name, and icon."
        if len(self.alts) <= 0:
            validationText += "\nYou must have at least one stage entry defined."
        elif len(self.alts) > 0:
            missingParams = False
            for alt in self.alts:
                if not (alt.aslEntry.Name and alt.pacName and alt.module and alt.tracklist and alt.soundBank and alt.effectBank):
                    missingParams = True
            if missingParams:
                validationText += "\nSome stage entries are missing parameters. Please ensure all parameter fields are filled in for all stage entries."
        return validationText

    def saveButtonPressed(self, sender, args):
        try:
            validationText = self.validate()
            if validationText:
                BrawlAPI.ShowMessage("The following errors were found:\n" + validationText + "\n\nPlease resolve these issues to continue.", "Validation Failed")
                return
            # Set up progressbar
            progressCounter = 0
            progressBar = ProgressWindow(MainForm.Instance, "Saving...", "Saving Stage", False)
            progressBar.Begin(0, 5, progressCounter)

            removeStageEntry(self.removeSlots)
            removeStageEntry(self.alts, False)

            progressCounter += 1
            progressBar.Update(progressCounter)

            moveStageFiles(self.alts)

            progressCounter += 1
            progressBar.Update(progressCounter)
            if self.newIcon or self.newName or self.newPreview or self.newFranchiseIcon or self.newGameLogo or self.newAltName:
                importStageCosmetics(self.cosmeticId, stageIcon=self.newIcon, stageName=self.newName, stagePreview=self.newPreview, franchiseIconName=self.newFranchiseIcon, gameLogoName=self.newGameLogo, altStageName=self.newAltName, franchiseIcons=self.addedFranchiseIcons, gameLogos=self.addedGameLogos)
                importStageCosmetics(self.cosmeticId, stageIcon=self.newIcon, stageName=self.newName, stagePreview=self.newPreview, franchiseIconName=self.newFranchiseIcon, gameLogoName=self.newGameLogo, altStageName=self.newAltName, franchiseIcons=self.addedFranchiseIcons, gameLogos=self.addedGameLogos, fileName='/pf/menu2/mu_menumain.pac')
            progressCounter += 1
            progressBar.Update(progressCounter)
            updateStageSlot(self.stageId, self.stageAltListbox.Items)
            updateStageParams(self.stageId, self.stageAltListbox.Items)
            progressCounter += 1
            progressBar.Update(progressCounter)
            if self.addedTracks:
                importFiles(self.addedTracks)
            if self.new:
                for stageList in self.stageLists:
                    newSlotNumber = addStageId(self.stageId + self.cosmeticId, self.alts[0].aslEntry.Name, stageList)
                    self.newSlotNumber.append(newSlotNumber)
            buildGct()
            progressCounter += 1
            progressBar.Update(progressCounter)
            progressBar.Finish()
            self.DialogResult = DialogResult.OK
            self.Close()
        except Exception as e:
            writeLog("ERROR " + str(e))
            if 'progressBar' in locals():
                progressBar.Finish()
            BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
            BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
            self.DialogResult = DialogResult.Abort
            self.Close()

    def cancelButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Close()

    def iconButtonPressed(self, sender, args):
        self.newIcon = BrawlAPI.OpenFileDialog("Select your stage icon image", "PNG files|*.png")
        if self.newIcon:
            self.iconPictureBox.Image = Bitmap(self.newIcon)

    def nameButtonPressed(self, sender, args):
        self.newName = BrawlAPI.OpenFileDialog("Select your stage name image", "PNG files|*.png")
        if self.newName:
            self.namePictureBox.Image = Bitmap(self.newName) 

    def previewButtonPressed(self, sender, args):
        self.newPreview = BrawlAPI.OpenFileDialog("Select your stage preview image", "PNG files|*.png")
        if self.newPreview:
            self.previewPictureBox.Image = Bitmap(self.newPreview) 

    def altDropDownChanged(self, sender, args):
        self.altNamePictureBox.Image = Bitmap(self.altDropDown.SelectedValue)
        if self.altDropDown.SelectedItem.name != self.cosmetics.altName.name:
            self.newAltName = self.altDropDown.SelectedItem.name
        elif not self.cosmetics.altName:
            self.newAltName = self.altDropDown.SelectedItem.name
        else:
            self.newAltName = ""

    def franchiseIconDropDownChanged(self, sender, args):
        self.franchiseIconPictureBox.Image = Bitmap(self.franchiseIconDropDown.SelectedValue)
        if self.cosmetics.franchiseIcon and self.franchiseIconDropDown.SelectedItem.name != self.cosmetics.franchiseIcon.name:
            self.newFranchiseIcon = self.franchiseIconDropDown.SelectedItem.name
        elif not self.cosmetics.franchiseIcon:
            self.newFranchiseIcon = self.franchiseIconDropDown.SelectedItem.name
        else:
            self.newFranchiseIcon = ""

    def gameLogoDropDownChanged(self, sender, args):
        self.gameLogoPictureBox.Image = Bitmap(self.gameLogoDropDown.SelectedValue)
        if self.cosmetics.gameLogo and self.gameLogoDropDown.SelectedItem.name != self.cosmetics.gameLogo.name:
            self.newGameLogo = self.gameLogoDropDown.SelectedItem.name
        elif not self.cosmetics.gameLogo:
            self.newGameLogo = self.gameLogoDropDown.SelectedItem.name
        else:
            self.newGameLogo = ""

    def getUnusedTextureName(self, prefix, imageNodes):
        for imageNode in imageNodes:
            i = 0
            newId = 1
            while True:
                while i < len(imageNodes):
                    if imageNodes[i].name == prefix + addLeadingZeros(str(newId), 2):
                        newId += 1
                        i = 0
                    i += 1
                break
            return prefix + addLeadingZeros(str(newId), 2)

    def franchiseIconButtonPressed(self, sender, args):
        newTexture = BrawlAPI.OpenFileDialog("Select your franchise icon PNG file", "PNG files|*.png")
        if newTexture:
            textureName = self.getUnusedTextureName('MenSelchrMark.', self.cosmetics.franchiseIconList)
            newImageNode = ImageNode(textureName, Bitmap(newTexture))
            self.franchiseIconList.Add(newImageNode)
            self.addedFranchiseIcons.Add(newTexture)
            self.franchiseIconDropDown.SelectedItem = newImageNode

    def gameLogoButtonPressed(self, sender, args):
        newTexture = BrawlAPI.OpenFileDialog("Select your game icon PNG file", "PNG files|*.png")
        if newTexture:
            textureName = self.getUnusedTextureName('MenSelmapMark.', self.cosmetics.gameLogoList)
            newImageNode = ImageNode(textureName, Bitmap(newTexture))
            self.gameLogoList.Add(newImageNode)
            self.addedGameLogos.Add(newTexture)
            self.gameLogoDropDown.SelectedItem = newImageNode

    def nameTextChanged(self, sender, args):
        self.stageAltListbox.SelectedValue.Name = self.nameTextBox.Text

    def pacNameTextChanged(self, sender, args):
        self.stageAltListbox.SelectedItem.pacName = self.pacNameTextBox.Text

    def moduleTextChanged(self, sender, args):
        self.stageAltListbox.SelectedItem.module = self.moduleTextBox.Text

    def tracklistDropDownChanged(self, sender, args):
        if len(self.stageAltListbox.Items) > 0:
            self.stageAltListbox.SelectedItem.tracklist = self.tracklistTextBox.SelectedValue

    def soundBankTextChanged(self, sender, args):
        if hexId(self.soundBankTextBox.Text):
            self.stageAltListbox.SelectedItem.soundBank = int(self.soundBankTextBox.Text.replace('0x', ''), 16)

    def effectBankTextChanged(self, sender, args):
        if hexId(self.effectBankTextBox.Text):
            self.stageAltListbox.SelectedItem.effectBank = int(self.effectBankTextBox.Text.replace('0x', ''), 16)

    def pacNameButtonPressed(self, sender, args):
        self.stageAltListbox.SelectedItem.pacFile = BrawlAPI.OpenFileDialog("Select your stage PAC file", "PAC files|*.pac")
        if self.stageAltListbox.SelectedItem.pacFile:
            fileName = getFileInfo(self.stageAltListbox.SelectedItem.pacFile).Name
            self.pacNameTextBox.Text = fileName.replace('STG', '').split('.')[0]
            self.pacNameFileBox.Text = self.stageAltListbox.SelectedItem.pacFile

    def moduleButtonPressed(self, sender, args):
        self.stageAltListbox.SelectedItem.moduleFile = BrawlAPI.OpenFileDialog("Select your stage module file", "REL files|*.rel")
        if self.stageAltListbox.SelectedItem.moduleFile:
            fileName = getFileInfo(self.stageAltListbox.SelectedItem.moduleFile).Name
            self.moduleTextBox.Text = fileName
            self.moduleFileBox.Text = self.stageAltListbox.SelectedItem.moduleFile

    def soundBankButtonPressed(self, sender, args):
        self.stageAltListbox.SelectedItem.soundBankFile = BrawlAPI.OpenFileDialog("Select your sawnd file", "SAWND files|*.sawnd")
        if self.stageAltListbox.SelectedItem.soundBankFile:
            fileName = getFileInfo(self.stageAltListbox.SelectedItem.soundBankFile).Name
            self.soundBankTextBox.Text = '0x' + fileName.split('_')[0]
            self.soundBankFileBox.Text = self.stageAltListbox.SelectedItem.soundBankFile

    def enableControls(self):
        self.nameTextBox.Enabled = True
        self.pacNameTextBox.Enabled = True
        self.moduleTextBox.Enabled = True
        self.tracklistTextBox.Enabled = True
        self.soundBankTextBox.Enabled = True
        self.effectBankTextBox.Enabled = True
        self.pacNameButton.Enabled = True
        self.moduleButton.Enabled = True
        self.soundBankButton.Enabled = True
        self.aslIndicator.Visible = True

    def stageAltAddButtonPressed(self, sender, args):
        newAslEntry = ASLSEntryNode()
        newAslEntry.Name = "New_Stage"
        newStageAlt = StageParams(newAslEntry, "", "Battlefield", "", int("0xFFFF", 16), int("0x0032", 16), "")
        self.alts.Add(newStageAlt)
        self.enableControls()
        self.stageAltListbox.SelectedIndex = len(self.alts) - 1

    def stageAltRemoveButtonPressed(self, sender, args):
        if len(self.alts) <= 1:
            return
        self.removeSlots.append(self.stageAltListbox.SelectedItem)
        self.alts.Remove(self.stageAltListbox.SelectedItem)

    def stageAltImportButtonPressed(self, sender, args):
        file = BrawlAPI.OpenFileDialog("Select your stage parameter file", "PARAM files|*.param")
        if file:
            newAslEntry = ASLSEntryNode()
            newAslEntry.Name = getFileInfo(file).Name.split('.')[0]
            newStageAlt = getStageParams(newAslEntry, file)
            newStageAlt.paramFile = file
            self.stageAltFileBox.Text = file
            self.alts.Add(newStageAlt)
            self.enableControls()

#endregion

#region COSTUME PROMPT

class CostumePrompt(Form):

    def __init__(self, uninstall=False):
        # Form parameters
        self.Text = 'Install Costume' if not uninstall else 'Uninstall Costume'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.AutoSize = True
        self.MinimumSize = Size(250,128)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.uninstall = uninstall

        # Form vars
        self.cspFiles = []
        self.bpFiles = []
        self.stockFiles = []
        self.costumeFiles = []

        # File Picker boxes
        self.fileGroup = GroupBox()
        self.fileGroup.Height = 192
        self.fileGroup.Dock = DockStyle.Top
        self.fileGroup.TabIndex = 1
        self.fileGroup.Visible = not self.uninstall

        # CSPs
        cspPanel = Panel()
        cspPanel.Location = Point(16, 16)
        cspPanel.TabIndex = 1
        cspPanel.Height = 32
        cspLabel = Label()
        cspLabel.Location = Point(0, 0)
        cspLabel.Text = "CSPs:"
        cspLabel.Width = 64
        self.cspListBox = ListBox()
        self.cspListBox.Width = 80
        self.cspListBox.Height = 32
        self.cspListBox.Location = Point(64, 0)
        cspButton = Button()
        cspButton.Location = Point(152, 0)
        cspButton.Text = "..."
        cspButton.Size = Size(24,24)
        cspButton.Click += self.cspButtonPressed

        cspPanel.Controls.Add(cspLabel)
        cspPanel.Controls.Add(self.cspListBox)
        cspPanel.Controls.Add(cspButton)

        # BPs
        bpPanel = Panel()
        bpPanel.Location = Point(16, 64)
        bpPanel.TabIndex = 2
        bpPanel.Height = 32
        bpLabel = Label()
        bpLabel.Location = Point(0, 0)
        bpLabel.Text = "BPs:"
        bpLabel.Width = 64
        self.bpListBox = ListBox()
        self.bpListBox.Width = 80
        self.bpListBox.Height = 32
        self.bpListBox.Location = Point(64, 0)
        bpButton = Button()
        bpButton.Location = Point(152, 0)
        bpButton.Text = "..."
        bpButton.Size = Size(24,24)
        bpButton.Click += self.bpButtonPressed

        bpPanel.Controls.Add(bpLabel)
        bpPanel.Controls.Add(self.bpListBox)
        bpPanel.Controls.Add(bpButton)

        # Stocks
        stockPanel = Panel()
        stockPanel.Location = Point(16, 112)
        stockPanel.TabIndex = 3
        stockPanel.Height = 32
        stockLabel = Label()
        stockLabel.Location = Point(0, 0)
        stockLabel.Text = "Stocks:"
        stockLabel.Width = 64
        self.stockListBox = ListBox()
        self.stockListBox.Width = 80
        self.stockListBox.Height = 32
        self.stockListBox.Location = Point(64, 0)
        stockButton = Button()
        stockButton.Location = Point(152, 0)
        stockButton.Text = "..."
        stockButton.Size = Size(24,24)
        stockButton.Click += self.stockButtonPressed

        stockPanel.Controls.Add(stockLabel)
        stockPanel.Controls.Add(self.stockListBox)
        stockPanel.Controls.Add(stockButton)

        # Costume Files
        costumePanel = Panel()
        costumePanel.Location = Point(16, 160)
        costumePanel.TabIndex = 4
        costumePanel.Height = 32
        costumeLabel = Label()
        costumeLabel.Location = Point(0, 0)
        costumeLabel.Text = "PAC Files:"
        costumeLabel.Width = 64
        self.costumeListBox = ListBox()
        self.costumeListBox.Width = 80
        self.costumeListBox.Height = 32
        self.costumeListBox.Location = Point(64, 0)
        costumeButton = Button()
        costumeButton.Location = Point(152, 0)
        costumeButton.Text = "..."
        costumeButton.Size = Size(24,24)
        costumeButton.Click += self.costumeButtonPressed

        costumePanel.Controls.Add(costumeLabel)
        costumePanel.Controls.Add(self.costumeListBox)
        costumePanel.Controls.Add(costumeButton)

        self.fileGroup.Controls.Add(cspPanel)
        self.fileGroup.Controls.Add(bpPanel)
        self.fileGroup.Controls.Add(stockPanel)
        self.fileGroup.Controls.Add(costumePanel)

        # Fighter ID box
        self.fighterIdGroup = GroupBox()
        self.fighterIdGroup.Height = 128
        self.fighterIdGroup.Dock = DockStyle.Top
        self.fighterIdGroup.TabIndex = 2

        fighterIdPanel = Panel()
        fighterIdPanel.Location = Point(16, 16)
        fighterIdPanel.TabIndex = 1
        fighterIdLabel = Label()
        fighterIdLabel.Dock = DockStyle.Left
        fighterIdLabel.Text = "Fighter ID:"
        self.fighterIdTextbox = TextBox()
        self.fighterIdTextbox.Dock = DockStyle.Right

        fighterIdButton = Button()
        fighterIdButton.Text = "..."
        fighterIdButton.Size = Size(25, self.fighterIdTextbox.ClientSize.Height + 2)
        fighterIdButton.Location = Point(self.fighterIdTextbox.ClientSize.Width - fighterIdButton.Width, -1)
        fighterIdButton.Cursor = Cursors.Default
        fighterIdButton.Click += self.fighterIdButtonPressed

        self.fighterIdTextbox.Controls.Add(fighterIdButton)

        fighterIdPanel.Controls.Add(fighterIdLabel)
        fighterIdPanel.Controls.Add(self.fighterIdTextbox)

        cosmeticIdPanel = Panel()
        cosmeticIdPanel.Location = Point(16, 48)
        cosmeticIdPanel.TabIndex = 2
        cosmeticIdLabel = Label()
        cosmeticIdLabel.Dock = DockStyle.Left
        cosmeticIdLabel.Text = "Cosmetic ID:"
        self.cosmeticIdTextbox = TextBox()
        self.cosmeticIdTextbox.Dock = DockStyle.Right

        cosmeticIdButton = Button()
        cosmeticIdButton.Text = "..."
        cosmeticIdButton.Size = Size(25, self.cosmeticIdTextbox.ClientSize.Height + 2)
        cosmeticIdButton.Location = Point(self.cosmeticIdTextbox.ClientSize.Width - cosmeticIdButton.Width, -1)
        cosmeticIdButton.Cursor = Cursors.Default
        cosmeticIdButton.Click += self.cosmeticIdButtonPressed

        self.cosmeticIdTextbox.Controls.Add(cosmeticIdButton)

        cosmeticIdPanel.Controls.Add(cosmeticIdLabel)
        cosmeticIdPanel.Controls.Add(self.cosmeticIdTextbox)

        cssSlotConfigIdPanel = Panel()
        cssSlotConfigIdPanel.Location = Point(16, 80)
        cssSlotConfigIdPanel.TabIndex = 3
        cssSlotConfigIdLabel = Label()
        cssSlotConfigIdLabel.Dock = DockStyle.Left
        cssSlotConfigIdLabel.Text = "CSS Slot ID:"
        self.cssSlotConfigIdTextbox = TextBox()
        self.cssSlotConfigIdTextbox.Dock = DockStyle.Right

        cssSlotIdButton = Button()
        cssSlotIdButton.Text = "..."
        cssSlotIdButton.Size = Size(25, self.cssSlotConfigIdTextbox.ClientSize.Height + 2)
        cssSlotIdButton.Location = Point(self.cssSlotConfigIdTextbox.ClientSize.Width - cssSlotIdButton.Width, -1)
        cssSlotIdButton.Cursor = Cursors.Default
        cssSlotIdButton.Click += self.cssSlotIdButtonPressed

        self.cssSlotConfigIdTextbox.Controls.Add(cssSlotIdButton)

        cssSlotConfigIdPanel.Controls.Add(cssSlotConfigIdLabel)
        cssSlotConfigIdPanel.Controls.Add(self.cssSlotConfigIdTextbox)

        self.fighterIdGroup.Controls.Add(cssSlotConfigIdPanel)
        self.fighterIdGroup.Controls.Add(cosmeticIdPanel)
        self.fighterIdGroup.Controls.Add(fighterIdPanel)

        # Install button
        installButton = Button()
        installButton.Text = "Install" if not self.uninstall else "Uninstall"
        installButton.Dock = DockStyle.Bottom
        installButton.Click += self.installButtonPressed

        # Tooltips
        toolTip = ToolTip()
        toolTip.SetToolTip(fighterIdLabel, "Fighter ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(cosmeticIdLabel, "Cosmetic ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(cssSlotConfigIdLabel, "CSS slot config ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(cspLabel, "CSP images for your costume")
        toolTip.SetToolTip(bpLabel, "BP images for your costume")
        toolTip.SetToolTip(stockLabel, "Stock icon images for your costume")
        toolTip.SetToolTip(costumeLabel, "Costume .pac files for your costume")
        

        # Add controls
        self.Controls.Add(installButton)
        self.Controls.Add(self.fileGroup)
        self.Controls.Add(self.fighterIdGroup)

    def fighterIdButtonPressed(self, sender, args):
        id = showIdPicker()
        if id:
            self.fighterIdTextbox.Text = id

    def cssSlotIdButtonPressed(self, sender, args):
        id = showIdPicker("cssSlot")
        if id:
            self.cssSlotConfigIdTextbox.Text = id

    def cosmeticIdButtonPressed(self, sender, args):
        id = showImageIdPicker("cosmetic")
        if id:
            self.cosmeticIdTextbox.Text = id

    def cspButtonPressed(self, sender, args):
        self.cspFiles = BrawlAPI.OpenMultiFileDialog("Select CSPs", "PNG files|*.png")
        if self.cspFiles:
            self.cspListBox.Items.Clear()
            for file in self.cspFiles:
                self.cspListBox.Items.Add(getFileInfo(file).Name)

    def bpButtonPressed(self, sender, args):
        self.bpFiles = BrawlAPI.OpenMultiFileDialog("Select BPs", "PNG files|*.png")
        if self.bpFiles:
            self.bpListBox.Items.Clear()
            for file in self.bpFiles:
                self.bpListBox.Items.Add(getFileInfo(file).Name)

    def stockButtonPressed(self, sender, args):
        self.stockFiles = BrawlAPI.OpenMultiFileDialog("Select stock icons", "PNG files|*.png")
        if self.stockFiles:
            self.stockListBox.Items.Clear()
            for file in self.stockFiles:
                self.stockListBox.Items.Add(getFileInfo(file).Name)

    def costumeButtonPressed(self, sender, args):
        self.costumeFiles = BrawlAPI.OpenMultiFileDialog("Select costume .pac files", "PAC files|*.pac")
        if self.costumeFiles:
            self.costumeListBox.Items.Clear()
            for file in self.costumeFiles:
                self.costumeListBox.Items.Add(getFileInfo(file).Name)

    def installButtonPressed(self, sender, args):
        valid = validateTextBoxes(self.fighterIdGroup)
        if not valid:
            BrawlAPI.ShowMessage("One or more fields contain invalid values. Please ensure all IDs are in either decimal (e.g. 33) or hexadecimal (e.g. 0x21) format.", "Validation Error")
            return
        if (not self.cspFiles or not self.bpFiles or not self.stockFiles or not self.costumeFiles) and not self.uninstall:
            proceed = BrawlAPI.ShowYesNoPrompt("You have not added all possible files. Would you like to proceed anyway?", "Files Missing")
            if proceed:
                self.DialogResult = DialogResult.OK
                self.Close()
            else:
                return
        self.DialogResult = DialogResult.OK
        self.Close()

#endregion COSTUME PROMPT

#region SETTINGS FORM

class SettingsForm(Form):

    def __init__(self):
        # Form parameters
        self.Text = 'Build Settings'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.Height = 128
        self.AutoSize = True
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.MinimumSize = Size(250,128)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        if File.Exists(MainForm.BuildPath + '/settings.ini'):
            self.settings = getSettings()
        else:
            self.settings = Settings()

        self.customStageLists = BindingSource()
        if len(self.settings.customStageLists.split(',')) > 0 and self.settings.customStageLists.split(',')[0] != "" :
            self.customStageLists.DataSource = self.settings.customStageLists.split(',')
        else:
            self.customStageLists.DataSource = []

        # Cosmetic settings group
        cosmeticGroupBox = GroupBox()
        cosmeticGroupBox.Location = Point(0,0)
        cosmeticGroupBox.Text = "Cosmetic Settings"
        cosmeticGroupBox.AutoSize = True
        cosmeticGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink

        # RSP Loading
        self.rspCheck = CheckBox()
        self.rspCheck.Text = "RSP Loading"
        self.rspCheck.Location = Point(16, 16)
        self.rspCheck.Width = 90

        # Fifty Costume Code
        self.fiftyCCCheck = CheckBox()
        self.fiftyCCCheck.Text = "50CC"
        self.fiftyCCCheck.Location = Point(112, 16)

        # CSS Icon Style
        cssIconGroup = GroupBox()
        cssIconGroup.Location = Point(4, 48)
        cssIconGroup.Text = "CSS Icon Style"
        cssIconGroup.AutoSize = True
        cssIconGroup.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.pPlusRadioButton = RadioButton()
        self.pPlusRadioButton.Text = "P+"
        self.pPlusRadioButton.Location = Point(16, 16)
        self.pPlusRadioButton.Width = 48
        self.pPlusRadioButton.Checked = True

        self.vBrawlRadioButton = RadioButton()
        self.vBrawlRadioButton.Text = "vBrawl"
        self.vBrawlRadioButton.Location = Point(64, 16)
        self.vBrawlRadioButton.Width = 64

        self.PMRadioButton = RadioButton()
        self.PMRadioButton.Text = "PM"
        self.PMRadioButton.Location = Point(128, 16)
        self.PMRadioButton.Width = 48

        self.remixRadioButton = RadioButton()
        self.remixRadioButton.Text = "REMIX"
        self.remixRadioButton.Location = Point(176, 16)
        self.remixRadioButton.Width = 64

        cssIconGroup.Controls.Add(self.pPlusRadioButton)
        cssIconGroup.Controls.Add(self.vBrawlRadioButton)
        cssIconGroup.Controls.Add(self.PMRadioButton)
        cssIconGroup.Controls.Add(self.remixRadioButton)

        # BP Style
        bpGroup = GroupBox()
        bpGroup.Location = Point(4, 112)
        bpGroup.Text = "BP Style"
        bpGroup.AutoSize = True
        bpGroup.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.vBrawlBPRadioButton = RadioButton()
        self.vBrawlBPRadioButton.Text = "vBrawl"
        self.vBrawlBPRadioButton.Location = Point(16, 16)
        self.vBrawlBPRadioButton.Width = 64
        self.vBrawlBPRadioButton.Checked = True

        self.remixBPRadioButton = RadioButton()
        self.remixBPRadioButton.Text = "REMIX"
        self.remixBPRadioButton.Location = Point(80, 16)
        self.remixBPRadioButton.Width = 64

        bpGroup.Controls.Add(self.vBrawlBPRadioButton)
        bpGroup.Controls.Add(self.remixBPRadioButton)

        # Portrait Name Style
        nameGroup = GroupBox()
        nameGroup.Location = Point(4, 176)
        nameGroup.Text = "Portrait Name Style"
        nameGroup.AutoSize = True
        nameGroup.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.vBrawlNameRadioButton = RadioButton()
        self.vBrawlNameRadioButton.Text = "vBrawl"
        self.vBrawlNameRadioButton.Location = Point(16, 16)
        self.vBrawlNameRadioButton.Width = 64
        self.vBrawlNameRadioButton.Checked = True

        self.PMNameRadioButton = RadioButton()
        self.PMNameRadioButton.Text = "PM"
        self.PMNameRadioButton.Location = Point(80, 16)
        self.PMNameRadioButton.Width = 64

        nameGroup.Controls.Add(self.vBrawlNameRadioButton)
        nameGroup.Controls.Add(self.PMNameRadioButton)

        # Replay Icon Style
        replayGroup = GroupBox()
        replayGroup.Location = Point(nameGroup.Location.X, nameGroup.Location.Y + nameGroup.Height/2 + 16)
        replayGroup.Text = "Replay Icon Style"
        replayGroup.AutoSize = True
        replayGroup.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.vBrawlReplayRadioButton = RadioButton()
        self.vBrawlReplayRadioButton.Text = "vBrawl"
        self.vBrawlReplayRadioButton.Location = Point(16, 16)
        self.vBrawlReplayRadioButton.Width = 64
        self.vBrawlReplayRadioButton.Checked = True

        self.pPlusReplayRadioButton = RadioButton()
        self.pPlusReplayRadioButton.Text = "P+"
        self.pPlusReplayRadioButton.Location = Point(80, 16)
        self.pPlusReplayRadioButton.Width = 64

        replayGroup.Controls.Add(self.vBrawlReplayRadioButton)
        replayGroup.Controls.Add(self.pPlusReplayRadioButton)

        # Stock locations
        stockGroupBox = GroupBox()
        stockGroupBox.AutoSize = True
        stockGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        stockGroupBox.Location = Point(replayGroup.Location.X, replayGroup.Location.Y + replayGroup.Height/2 + 16)
        stockGroupBox.Text = "Stock Icon Install Locations"

        self.stockCssCheckbox = CheckBox()
        self.stockCssCheckbox.Text = "Character Select"
        self.stockCssCheckbox.Location = Point(16, 16)
        self.stockCssCheckbox.Width = 112

        self.stockSssCheckbox = CheckBox()
        self.stockSssCheckbox.Text = "Stage Select"
        self.stockSssCheckbox.Location = Point(128, 16)
        self.stockSssCheckbox.Width = 112

        self.stockResultCheckbox = CheckBox()
        self.stockResultCheckbox.Text = "Result Screen"
        self.stockResultCheckbox.Location = Point(16, 40)
        self.stockResultCheckbox.Width = 112

        self.stockRotationCheckbox = CheckBox()
        self.stockRotationCheckbox.Text = "Rotation Mode"
        self.stockRotationCheckbox.Location = Point(128, 40)
        self.stockRotationCheckbox.Width = 112

        self.stockBattleCheckbox = CheckBox()
        self.stockBattleCheckbox.Text = "Battle UI"
        self.stockBattleCheckbox.Location = Point(16, 64)
        self.stockBattleCheckbox.Width = 112
        
        stockGroupBox.Controls.Add(self.stockCssCheckbox)
        stockGroupBox.Controls.Add(self.stockSssCheckbox)
        stockGroupBox.Controls.Add(self.stockResultCheckbox)
        stockGroupBox.Controls.Add(self.stockRotationCheckbox)
        stockGroupBox.Controls.Add(self.stockBattleCheckbox)

        # Other cosmetic install options
        self.portraitNameCheckBox = CheckBox()
        self.portraitNameCheckBox.Text = "Install Portrait Names"
        self.portraitNameCheckBox.Width = 140
        self.portraitNameCheckBox.Location = Point(16, stockGroupBox.Location.Y + stockGroupBox.Height + 4)

        self.bpNameCheckbox = CheckBox()
        self.bpNameCheckbox.Text = "Install BP Names"
        self.bpNameCheckbox.Width = 140
        self.bpNameCheckbox.Location = Point(16, self.portraitNameCheckBox.Location.Y + 24)

        self.singlePlayerCheckBox = CheckBox()
        self.singlePlayerCheckBox.Text = "Install Single Player Cosmetics"
        self.singlePlayerCheckBox.Width = 200
        self.singlePlayerCheckBox.Location = Point(16, self.bpNameCheckbox.Location.Y + 24)

        self.franchiseIconSizeLabel = Label()
        self.franchiseIconSizeLabel.Location = Point(16, self.singlePlayerCheckBox.Location.Y + 24)
        self.franchiseIconSizeLabel.Text = "Franchise Icon Size:"
        self.franchiseIconSizeLabel.Width = 112

        self.franchiseIconSizeText = NumericUpDown()
        self.franchiseIconSizeText.Location = Point(128, self.franchiseIconSizeLabel.Location.Y)
        self.franchiseIconSizeText.Width = 48
        self.franchiseIconSizeText.Maximum = 256
        self.franchiseIconSizeText.Minimum = 0

        cosmeticGroupBox.Controls.Add(self.rspCheck)
        cosmeticGroupBox.Controls.Add(self.fiftyCCCheck)
        cosmeticGroupBox.Controls.Add(cssIconGroup)
        cosmeticGroupBox.Controls.Add(bpGroup)
        cosmeticGroupBox.Controls.Add(nameGroup)
        cosmeticGroupBox.Controls.Add(replayGroup)
        cosmeticGroupBox.Controls.Add(stockGroupBox)
        cosmeticGroupBox.Controls.Add(self.portraitNameCheckBox)
        cosmeticGroupBox.Controls.Add(self.bpNameCheckbox)
        cosmeticGroupBox.Controls.Add(self.singlePlayerCheckBox)
        cosmeticGroupBox.Controls.Add(self.franchiseIconSizeLabel)
        cosmeticGroupBox.Controls.Add(self.franchiseIconSizeText)

        # Stage Settings group
        self.stageGroupBox = GroupBox()
        self.stageGroupBox.Location = Point(0, 525)
        self.stageGroupBox.Text = "Custom Stage Lists"
        self.stageGroupBox.AutoSize = True
        self.stageGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.stageListBox = ListBox()
        self.stageListBox.Width = 120
        self.stageListBox.Height = 80
        self.stageListBox.Location = Point(16, 16)
        self.stageListBox.DataSource = []
        self.stageListBox.HorizontalScrollbar = True

        stageListAddButton = Button()
        stageListAddButton.Text = "+"
        stageListAddButton.Size = Size(16,16)
        stageListAddButton.Location = Point(138, 15)
        stageListAddButton.Click += self.stageListAddButtonPressed

        stageListRemoveButton = Button()
        stageListRemoveButton.Text = "-"
        stageListRemoveButton.Size = Size(16,16)
        stageListRemoveButton.Location = Point(138, 32)
        stageListRemoveButton.Click += self.stageListRemoveButtonPressed

        self.stageGroupBox.Controls.Add(self.stageListBox)
        self.stageGroupBox.Controls.Add(stageListAddButton)
        self.stageGroupBox.Controls.Add(stageListRemoveButton)

        pPlusDefaultsButton = Button()
        pPlusDefaultsButton.Text = "P+Ex Defaults"
        pPlusDefaultsButton.Location = Point(4, 640)
        pPlusDefaultsButton.Width = 90
        pPlusDefaultsButton.Click += self.pPlusDefaultsButtonPressed

        remixDefaultsButton = Button()
        remixDefaultsButton.Text = "REMIX Defaults"
        remixDefaultsButton.Location = Point(98, 640)
        remixDefaultsButton.Width = 95
        remixDefaultsButton.Click += self.remixDefaultsButtonPressed

        # Configuration settings group
        configGroupBox = GroupBox()
        configGroupBox.Location = Point(264,0)
        configGroupBox.Text = "Configuration Settings"
        configGroupBox.AutoSize = True
        configGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink

        # Kirby group
        kirbyGroupBox = GroupBox()
        kirbyGroupBox.Location = Point(16, 16)
        kirbyGroupBox.Text = "Kirby Hats"
        kirbyGroupBox.AutoSize = True
        kirbyGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.kirbyExeFileBox = TextBox()
        self.kirbyExeFileBox.Location = Point(76, 16)
        self.kirbyExeFileBox.Width = 160
        self.kirbyExeFileBox.ReadOnly = True

        kirbyExeLabel = Label()
        kirbyExeLabel.Text = "lKHM .exe:"
        kirbyExeLabel.Location = Point(4, 16)
        kirbyExeLabel.TextAlign = ContentAlignment.TopRight
        kirbyExeLabel.Width = 64

        kirbyExeButton = Button()
        kirbyExeButton.Text = "Browse..."
        kirbyExeButton.Location = Point(240, 15)
        kirbyExeButton.Click += self.kirbyExeButtonPressed

        defaultKirbyHatLabel = Label()
        defaultKirbyHatLabel.Text = "Default Kirby Hat ID:"
        defaultKirbyHatLabel.Location = Point(4, 48)
        defaultKirbyHatLabel.TextAlign = ContentAlignment.TopRight
        defaultKirbyHatLabel.Width = 112

        self.defaultKirbyHatText = TextBox()
        self.defaultKirbyHatText.Location = Point(120, 48)

        defaultKirbyHatButton = Button()
        defaultKirbyHatButton.Text = "..."
        defaultKirbyHatButton.Size = Size(25, self.defaultKirbyHatText.ClientSize.Height + 2)
        defaultKirbyHatButton.Location = Point(self.defaultKirbyHatText.ClientSize.Width - defaultKirbyHatButton.Width, -1)
        defaultKirbyHatButton.Cursor = Cursors.Default
        defaultKirbyHatButton.Click += self.defaultKirbyHatButtonPressed

        self.defaultKirbyHatText.Controls.Add(defaultKirbyHatButton)

        self.installKirbyHatCheckbox = CheckBox()
        self.installKirbyHatCheckbox.Text = "Install Kirby Hats"
        self.installKirbyHatCheckbox.Location = Point(self.defaultKirbyHatText.Location.X + self.defaultKirbyHatText.Width + 16, self.defaultKirbyHatText.Location.Y)
        self.installKirbyHatCheckbox.Height = 28

        kirbyGroupBox.Controls.Add(kirbyExeLabel)
        kirbyGroupBox.Controls.Add(self.kirbyExeFileBox)
        kirbyGroupBox.Controls.Add(kirbyExeButton)
        kirbyGroupBox.Controls.Add(defaultKirbyHatLabel)
        kirbyGroupBox.Controls.Add(self.defaultKirbyHatText)
        kirbyGroupBox.Controls.Add(self.installKirbyHatCheckbox)

        # Code menu group
        codeMenuGroupBox = GroupBox()
        codeMenuGroupBox.Location = Point(16, 112)
        codeMenuGroupBox.Text = "Code Menu"
        codeMenuGroupBox.AutoSize = True
        codeMenuGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.codeMenuFileBox = TextBox()
        self.codeMenuFileBox.Location = Point(76, 16)
        self.codeMenuFileBox.Width = 160
        self.codeMenuFileBox.ReadOnly = True

        codeMenuLabel = Label()
        codeMenuLabel.Text = "PowerPC\n.exe:"
        codeMenuLabel.Location = Point(4, 16)
        codeMenuLabel.TextAlign = ContentAlignment.TopRight
        codeMenuLabel.Width = 64

        codeMenuButton = Button()
        codeMenuButton.Text = "Browse..."
        codeMenuButton.Location = Point(240, 15)
        codeMenuButton.Click += self.codeMenuButtonPressed

        codeMenuGroupBox.Controls.Add(self.codeMenuFileBox)
        codeMenuGroupBox.Controls.Add(codeMenuLabel)
        codeMenuGroupBox.Controls.Add(codeMenuButton)

        # Soundbank group
        soundbankGroupBox = GroupBox()
        soundbankGroupBox.Location = Point(16, 176)
        soundbankGroupBox.Text = "Soundbanks"
        soundbankGroupBox.AutoSize = True
        soundbankGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.sawndReplaceExeText = TextBox()
        self.sawndReplaceExeText.Location = Point(76, 16)
        self.sawndReplaceExeText.Width = 160
        self.sawndReplaceExeText.ReadOnly = True

        sawndReplaceExeLabel = Label()
        sawndReplaceExeLabel.Text = "lSIDRA\n.exe:"
        sawndReplaceExeLabel.Location = Point(4, 16)
        sawndReplaceExeLabel.TextAlign = ContentAlignment.TopRight
        sawndReplaceExeLabel.Width = 64

        sawndReplaceExeButton = Button()
        sawndReplaceExeButton.Text = "Browse..."
        sawndReplaceExeButton.Location = Point(240, 15)
        sawndReplaceExeButton.Click += self.sawndReplaceExeButtonPressed

        self.sfxChangeExeText = TextBox()
        self.sfxChangeExeText.Location = Point(76, 48)
        self.sfxChangeExeText.Width = 160
        self.sfxChangeExeText.ReadOnly = True

        sfxChangeExeLabel = Label()
        sfxChangeExeLabel.Text = "sfxchange\n.exe:"
        sfxChangeExeLabel.Location = Point(4, 48)
        sfxChangeExeLabel.TextAlign = ContentAlignment.TopRight
        sfxChangeExeLabel.Width = 64

        sfxChangeExeButton = Button()
        sfxChangeExeButton.Text = "Browse..."
        sfxChangeExeButton.Location = Point(240, 47)
        sfxChangeExeButton.Click += self.sfxChangeExeButtonPressed

        soundbankFormatGroup = GroupBox()
        soundbankFormatGroup.Location = Point(16, 80)
        soundbankFormatGroup.Text = "Soundbank Format"
        soundbankFormatGroup.AutoSize = True
        soundbankFormatGroup.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.decimalRadioButton = RadioButton()
        self.decimalRadioButton.Text = "Decimal"
        self.decimalRadioButton.Location = Point(16, 16)
        self.decimalRadioButton.Width = 64
        self.decimalRadioButton.Checked = True

        self.hexRadioButton = RadioButton()
        self.hexRadioButton.Text = "Hex"
        self.hexRadioButton.Location = Point(80, 16)
        self.hexRadioButton.Width = 64

        soundbankFormatGroup.Controls.Add(self.decimalRadioButton)
        soundbankFormatGroup.Controls.Add(self.hexRadioButton)

        self.incrementSoundbankIdCheck = CheckBox()
        self.incrementSoundbankIdCheck.Text = "Increment Soundbank IDs by 7"
        self.incrementSoundbankIdCheck.Width = 196
        self.incrementSoundbankIdCheck.Location = Point(16, 144)

        self.incrementSoundbankNameCheck = CheckBox()
        self.incrementSoundbankNameCheck.Text = "Increment Soundbank names by 7"
        self.incrementSoundbankNameCheck.Width = 196
        self.incrementSoundbankNameCheck.Location = Point(16, 164)

        soundbankGroupBox.Controls.Add(self.sawndReplaceExeText)
        soundbankGroupBox.Controls.Add(sawndReplaceExeLabel)
        soundbankGroupBox.Controls.Add(sawndReplaceExeButton)
        soundbankGroupBox.Controls.Add(self.sfxChangeExeText)
        soundbankGroupBox.Controls.Add(sfxChangeExeLabel)
        soundbankGroupBox.Controls.Add(sfxChangeExeButton)
        soundbankGroupBox.Controls.Add(soundbankFormatGroup)
        soundbankGroupBox.Controls.Add(self.incrementSoundbankIdCheck)
        soundbankGroupBox.Controls.Add(self.incrementSoundbankNameCheck)

        # GFX group
        gfxGroupBox = GroupBox()
        gfxGroupBox.Location = Point(16, 390)
        gfxGroupBox.Text = "Effect Banks"
        gfxGroupBox.AutoSize = True
        gfxGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.gfxChangeExeText = TextBox()
        self.gfxChangeExeText.Location = Point(76, 16)
        self.gfxChangeExeText.Width = 160
        self.gfxChangeExeText.ReadOnly = True

        gfxChangeExeLabel = Label()
        gfxChangeExeLabel.Text = "gfxchange\n.exe:"
        gfxChangeExeLabel.Location = Point(4, 16)
        gfxChangeExeLabel.TextAlign = ContentAlignment.TopRight
        gfxChangeExeLabel.Width = 64

        gfxChangeExeButton = Button()
        gfxChangeExeButton.Text = "Browse..."
        gfxChangeExeButton.Location = Point(240, 15)
        gfxChangeExeButton.Click += self.gfxChangeExeButtonPressed

        gfxGroupBox.Controls.Add(self.gfxChangeExeText)
        gfxGroupBox.Controls.Add(gfxChangeExeLabel)
        gfxGroupBox.Controls.Add(gfxChangeExeButton)

        # Other settings
        otherGroupBox = GroupBox()
        otherGroupBox.Location = Point(16, 450)
        otherGroupBox.Text = "Misc Settings"
        otherGroupBox.AutoSize = True
        otherGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.sseCheck = CheckBox()
        self.sseCheck.Text = "Install Fighters to SSE"
        self.sseCheck.Location = Point(16, 16)
        self.sseCheck.Width = 138
        
        self.victoryThemeCheck = CheckBox()
        self.victoryThemeCheck.Text = "Install Victory Themes"
        self.victoryThemeCheck.Location = Point(16, 36)
        self.victoryThemeCheck.Width = 138

        self.trophyCheck = CheckBox()
        self.trophyCheck.Text = "Install Trophies"
        self.trophyCheck.Location = Point(160, 16)
        self.trophyCheck.Width = 138

        # SSE Unlock Stage
        sseGroup = GroupBox()
        sseGroup.Location = Point(4, 68)
        sseGroup.Text = "SSE Unlock Stage"
        sseGroup.AutoSize = True
        sseGroup.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.unlockStartRadioButton = RadioButton()
        self.unlockStartRadioButton.Text = "Start"
        self.unlockStartRadioButton.Location = Point(16, 16)
        self.unlockStartRadioButton.Width = 64
        self.unlockStartRadioButton.Checked = True

        self.unlockEndRadioButton = RadioButton()
        self.unlockEndRadioButton.Text = "End"
        self.unlockEndRadioButton.Location = Point(80, 16)
        self.unlockEndRadioButton.Width = 64

        sseGroup.Controls.Add(self.unlockStartRadioButton)
        sseGroup.Controls.Add(self.unlockEndRadioButton)

        otherGroupBox.Controls.Add(self.sseCheck)
        otherGroupBox.Controls.Add(self.trophyCheck)
        otherGroupBox.Controls.Add(self.victoryThemeCheck)
        otherGroupBox.Controls.Add(sseGroup)
        
        configGroupBox.Controls.Add(kirbyGroupBox)
        configGroupBox.Controls.Add(codeMenuGroupBox)
        configGroupBox.Controls.Add(soundbankGroupBox)
        configGroupBox.Controls.Add(gfxGroupBox)
        configGroupBox.Controls.Add(otherGroupBox)

        self.cancelButton = Button()
        self.cancelButton.Text = "Close"
        self.cancelButton.Location = Point(525, 640)
        self.cancelButton.Click += self.cancelButtonPressed

        saveButton = Button()
        saveButton.Text = "Save"
        saveButton.Location = Point(445, 640)
        saveButton.Click += self.saveButtonPressed

        self.Controls.Add(cosmeticGroupBox)
        self.Controls.Add(self.stageGroupBox)
        self.Controls.Add(pPlusDefaultsButton)
        self.Controls.Add(remixDefaultsButton)
        self.Controls.Add(configGroupBox)
        self.Controls.Add(saveButton)
        self.Controls.Add(self.cancelButton)

        # Tooltips
        toolTip = ToolTip()
        toolTip.SetToolTip(self.rspCheck, "Whether or not your build uses RSP (result-screen portrait) loading. For most builds, this should be unchecked.")
        toolTip.SetToolTip(self.fiftyCCCheck, "Whether or not your build uses 50CC (fifty-costume code) naming conventions. If your build is P+Ex or allows 50 costumes, this should be checked.")
        toolTip.SetToolTip(cssIconGroup, "The style of character select screen icons used in your build.")
        toolTip.SetToolTip(self.pPlusRadioButton, "Select this if your build uses P+ style icons. These are diamond shaped icons featured in Project+ and P+Ex.")
        toolTip.SetToolTip(self.remixRadioButton, "Select this if your build uses PMEX REMIX style icons. These are hexagonal icons featured PMEX REMIX.")
        toolTip.SetToolTip(self.PMRadioButton, "Select this if your build uses Project M style icons. These are rectangular icons with a purple background featured in Project M.")
        toolTip.SetToolTip(self.vBrawlRadioButton, "Select this if your build uses vanilla Brawl style icons. These are rectangular icons with a blue background featured in Brawl.")
        toolTip.SetToolTip(bpGroup, "The style of battle portraits used in your build.")      
        toolTip.SetToolTip(self.vBrawlBPRadioButton, "Select this if your build uses vanilla Brawl style battle portraits. These are square portraits.")
        toolTip.SetToolTip(self.remixBPRadioButton, "Select this if your build uses PMEX REMIX style battle portraits. These are portraits with a hexagonal background.") 
        toolTip.SetToolTip(nameGroup, "The style of names used on portraits displayed on the character select screen. If your build doesn't use these, this setting will have no effect.") 
        toolTip.SetToolTip(self.vBrawlNameRadioButton, "Select this if your build uses vanilla Brawl style portrait names.") 
        toolTip.SetToolTip(self.PMNameRadioButton, "Select this if your build uses Project M style portrait names.") 
        toolTip.SetToolTip(replayGroup, "The style of icons displayed on the replay screen.")
        toolTip.SetToolTip(self.vBrawlReplayRadioButton, "Select this if your build uses vanilla Brawl style replay icons.")
        toolTip.SetToolTip(self.pPlusReplayRadioButton, "Select this if your build uses Project+ style replay icons.")
        toolTip.SetToolTip(stockGroupBox, "The locations where character-specific stock icons are used in your build.") 
        toolTip.SetToolTip(self.stockCssCheckbox, "Check this if your build uses stock icons on the character select screen for modes like Classic mode. When checked, stock icons will be installed to sc_selcharacter.pac.") 
        toolTip.SetToolTip(self.stockSssCheckbox, "Check this if your build uses stock icons on the stage select screen. When checked, stock icons will be installed to sc_selmap.pac.") 
        toolTip.SetToolTip(self.stockResultCheckbox, "Check this if your build uses stock icons on the match result screen. When checked, stock icons will be installed to STGRESULT.pac.") 
        toolTip.SetToolTip(self.stockRotationCheckbox, "Check this if your build uses stock icons in modes like Rotation mode. When checked, stock icons will be installed to StockFaceTex.brres.") 
        toolTip.SetToolTip(self.stockBattleCheckbox, "Check this if your build uses stock icons during matches. When checked, stock icons will be installed to info.pac.") 
        toolTip.SetToolTip(self.portraitNameCheckBox, "Check this if your build displays names on the portraits displayed on the character select screen.") 
        toolTip.SetToolTip(self.bpNameCheckbox, "Check this if your build displays names beneath the portraits used in a match.") 
        toolTip.SetToolTip(self.singlePlayerCheckBox, "Check this if you would like franchise icons and battle portrait names (if used) to be installed into single-player modes like Classic mode.") 
        toolTip.SetToolTip(self.franchiseIconSizeLabel, "This determines both the height and width of franchise icons displayed behind character portraits on the character select screen. For vBrawl, this is 64. For P+, it is 128.") 
        toolTip.SetToolTip(self.stageGroupBox, "This is a list of .asm files containing custom stage lists used in your build. You can add new entries by clicking the '+'. Most builds do not use this.") 
        toolTip.SetToolTip(kirbyExeLabel, "The path to your preferred version of lavaKirbyHatManager .exe. Should be placed in your build. Required for Kirby hats to work on P+Ex builds.") 
        toolTip.SetToolTip(defaultKirbyHatLabel, "The fighter ID to default to for Kirby hats when no Kirby hat is provided. Must be in either hex (0x21) or decimal (33) format. If left blank, Kirby hats will be set to none by default.")
        toolTip.SetToolTip(self.installKirbyHatCheckbox, "Whether or not you would like to install Kirby hats when available. If unchecked, Kirby hats will never be installed when installing a character, regardless of other settings.") 
        toolTip.SetToolTip(codeMenuLabel, "The path to your preferred version of QuickLava's PowerPC Assembly Functions .exe. Should be placed in your build. Required for fighters to be added to the code menu.") 
        toolTip.SetToolTip(sawndReplaceExeLabel, "The path to lavaSawndIDReplaceAssist.exe. Required to resolve soundbank conflicts during character installs.") 
        toolTip.SetToolTip(sfxChangeExeLabel, "The path to Codes' sfxchange.exe. Required to resolve soundbank conflicts during character installs.") 
        toolTip.SetToolTip(soundbankFormatGroup, "The naming format for soundbanks used by your build.") 
        toolTip.SetToolTip(self.decimalRadioButton, "Select this if your build uses soundbanks named in decimal format. Used in older builds.") 
        toolTip.SetToolTip(self.hexRadioButton, "Select this if your build uses soundbanks named in hexadecimal format. Used in most modern builds such as P+Ex and REMIX.") 
        toolTip.SetToolTip(self.incrementSoundbankIdCheck, "Check this if SFX IDs need to be incremented by 7 when converted using QuickLava and Codes' tools. For most modern builds, this should be checked.") 
        toolTip.SetToolTip(self.incrementSoundbankNameCheck, "Check this if soundbanks in your build are named as their soundbank ID plus 7. In most modern builds, this should be unchecked.") 
        toolTip.SetToolTip(gfxChangeExeLabel, "The path to Codes' gfxchange.exe. Required to resolve Effect.pac ID conflicts during character installation.") 
        toolTip.SetToolTip(self.sseCheck, "Check this if you would like fighters to be installed to SSE mode. Only use this if your build supports Subspace Emissary Ex, which is included in the latest P+Ex release.") 
        toolTip.SetToolTip(self.trophyCheck, "Check this if you would like to install trophies with fighters when they are available. While adding trophies appears to be stable, some behaviors are still unknown, so this is considered experimental.")
        toolTip.SetToolTip(self.victoryThemeCheck, "Check this if you would like to install victory and credits themes with fighters when they are available. Only check this if your build uses the modern P+ tracklist system. Most modern builds do.")
        toolTip.SetToolTip(sseGroup, "These settings determine when added characters are unlocked in SSE mode by default.") 
        toolTip.SetToolTip(self.unlockStartRadioButton, "Select this if you would like added characters to be unlocked in SSE mode from the start by default.")  
        toolTip.SetToolTip(self.unlockEndRadioButton, "Select this if you would like added characters to be unlocked after completing SSE mode by default.")  

        self.initializeControls()

    def initializeControls(self):
        self.rspCheck.Checked = textBool(self.settings.rspLoading)
        self.fiftyCCCheck.Checked = textBool(self.settings.fiftyCostumeCode)
        self.pPlusRadioButton.Checked = self.settings.cssIconStyle == "P+"
        self.vBrawlRadioButton.Checked = self.settings.cssIconStyle == "vBrawl"
        self.PMRadioButton.Checked = self.settings.cssIconStyle == "PM"
        self.remixRadioButton.Checked = self.settings.cssIconStyle == "REMIX"
        self.vBrawlBPRadioButton.Checked = self.settings.bpStyle == "vBrawl"
        self.remixBPRadioButton.Checked = self.settings.bpStyle == "REMIX"
        self.vBrawlNameRadioButton.Checked = self.settings.portraitNameStyle == "vBrawl"
        self.PMNameRadioButton.Checked = self.settings.portraitNameStyle == "PM"
        if self.settings.replayIconStyle:
            self.vBrawlReplayRadioButton.Checked = self.settings.replayIconStyle == "vBrawl"
            self.pPlusReplayRadioButton.Checked = self.settings.replayIconStyle == "P+"
        self.stockCssCheckbox.Checked = textBool(self.settings.installStocksToCSS)
        self.stockSssCheckbox.Checked = textBool(self.settings.installStocksToSSS)
        self.stockResultCheckbox.Checked = textBool(self.settings.installStockIconsToResult)
        self.stockRotationCheckbox.Checked = textBool(self.settings.installStocksToStockFaceTex)
        self.stockBattleCheckbox.Checked = textBool(self.settings.installStocksToInfo)
        self.portraitNameCheckBox.Checked = textBool(self.settings.installPortraitNames)
        self.bpNameCheckbox.Checked = textBool(self.settings.installBPNames)
        self.singlePlayerCheckBox.Checked = textBool(self.settings.installSingleplayerCosmetics)
        self.franchiseIconSizeText.Text = self.settings.franchiseIconSizeCSS
        self.kirbyExeFileBox.Text = self.settings.kirbyHatExe
        self.defaultKirbyHatText.Text = self.settings.defaultKirbyHat
        self.installKirbyHatCheckbox.Checked = textBool(self.settings.installKirbyHats)
        self.codeMenuFileBox.Text = self.settings.assemblyFunctionsExe
        self.sawndReplaceExeText.Text = self.settings.sawndReplaceExe
        self.sfxChangeExeText.Text = self.settings.sfxChangeExe
        self.hexRadioButton.Checked = self.settings.soundbankStyle == "hex"
        self.decimalRadioButton.Checked = self.settings.soundbankStyle == "dec"
        self.incrementSoundbankIdCheck.Checked = textBool(self.settings.addSevenToSoundbankIds)
        self.incrementSoundbankNameCheck.Checked = textBool(self.settings.addSevenToSoundbankName)
        self.gfxChangeExeText.Text = self.settings.gfxChangeExe
        self.sseCheck.Checked = textBool(self.settings.installToSse)
        self.trophyCheck.Checked = textBool(self.settings.installTrophies)
        self.victoryThemeCheck.Checked = textBool(self.settings.installVictoryThemes)
        self.unlockStartRadioButton.Checked = self.settings.sseUnlockStage == "start"
        self.unlockEndRadioButton.Checked = self.settings.sseUnlockStage == "end"
        self.stageListBox.DataSource = self.customStageLists

    def pPlusDefaultsButtonPressed(self, sender, args):
        settings = Settings()
        settings.rspLoading = "false"
        settings.cssIconStyle = "P+"
        settings.bpStyle = "vBrawl"
        settings.installPortraitNames = "false"
        settings.portraitNameStyle = "vBrawl"
        settings.replayIconStyle = "P+"
        settings.franchiseIconSizeCSS = str(128)
        settings.installStocksToCSS = "true"
        settings.installStocksToInfo = "true"
        settings.installStockIconsToResult = "true"
        settings.installStocksToStockFaceTex = "true"
        settings.fiftyCostumeCode = "true"
        settings.soundbankStyle = "hex"
        settings.addSevenToSoundbankName = "false"
        settings.addSevenToSoundbankIds = "true"
        settings.installVictoryThemes = "true"
        settings.installBPNames = "false"
        settings.installSingleplayerCosmetics = "true"
        settings.installKirbyHats = "true"

        self.settings = settings
        self.initializeControls()

    def remixDefaultsButtonPressed(self, sender, args):
        settings = Settings()
        settings.rspLoading = "true"
        settings.cssIconStyle = "REMIX"
        settings.bpStyle = "REMIX"
        settings.installPortraitNames = "true"
        settings.portraitNameStyle = "PM"
        settings.replayIconStyle = "P+"
        settings.franchiseIconSizeCSS = str(64)
        settings.installStocksToCSS = "false"
        settings.installStocksToInfo = "false"
        settings.installStockIconsToResult = "false"
        settings.installStocksToStockFaceTex = "false"
        settings.fiftyCostumeCode = "true"
        settings.soundbankStyle = "hex"
        settings.addSevenToSoundbankName = "false"
        settings.addSevenToSoundbankIds = "true"
        settings.installVictoryThemes = "true"
        settings.installBPNames = "false"
        settings.installSingleplayerCosmetics = "false"
        settings.installKirbyHats = "true"

        self.settings = settings
        self.initializeControls()

    def stageListAddButtonPressed(self, sender, args):
        newFile = BrawlAPI.OpenFileDialog("Select your stagelist ASM file", "ASM files|*.asm")
        if newFile:
            self.customStageLists.Add(newFile)

    def stageListRemoveButtonPressed(self, sender, args):
        if len(self.stageListBox.Items) > 0 and self.stageListBox.SelectedItem:
            self.customStageLists.Remove(self.stageListBox.SelectedItem)

    def cancelButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Close()

    def defaultKirbyHatButtonPressed(self, sender, args):
        id = showIdPicker()
        if id:
            self.defaultKirbyHatText.Text = id

    def kirbyExeButtonPressed(self, sender, args):
        while True:
            kirbyHatExe = BrawlAPI.OpenFileDialog("Select your Kirby Hat Manager .exe", "Executable files|*.exe")
            if kirbyHatExe:
                if DirectoryInfo(MainForm.BuildPath).FullName not in getFileInfo(kirbyHatExe).DirectoryName:
                    BrawlAPI.ShowMessage("Lava's Kirby hat manager must be in your build folder! Please move it to the correct directory and try again.", "Please place in build folder")
                else:
                    self.kirbyExeFileBox.Text = kirbyHatExe
                    break
            else:
                break

    def codeMenuButtonPressed(self, sender, args):
        while True:
            exe = BrawlAPI.OpenFileDialog("Select your PowerPC Assembly Functions .exe", "Executable files|*.exe")
            if exe:
                if DirectoryInfo(MainForm.BuildPath).FullName not in getFileInfo(exe).DirectoryName:
                    BrawlAPI.ShowMessage("PowerPC Assembly Functions must be in your build folder! Please move it to the correct directory and try again.", "Please place in build folder")
                else:
                    self.codeMenuFileBox.Text = exe
                    break
            else:
                break

    def sawndReplaceExeButtonPressed(self, sender, args):
        exe = BrawlAPI.OpenFileDialog("Select your lavaSawndIDReplaceAssist .exe", "Executable files|*.exe")
        if exe:
            self.sawndReplaceExeText.Text = exe

    def sfxChangeExeButtonPressed(self, sender, args):
        exe = BrawlAPI.OpenFileDialog("Select your sfxchange.exe", "Executable files|*.exe")
        if exe:
            self.sfxChangeExeText.Text = exe

    def gfxChangeExeButtonPressed(self, sender, args):
        exe = BrawlAPI.OpenFileDialog("Select your gfxchange.exe", "Executable files|*.exe")
        if exe:
            self.gfxChangeExeText.Text = exe
    
    def saveButtonPressed(self, sender, args):
        if self.defaultKirbyHatText.Text.strip() != "":
            valid = validateTextBox(self.defaultKirbyHatText)
            if not valid:
                BrawlAPI.ShowMessage("Default Kirby hat field contains invalid values. Please ensure the ID is in either decimal (e.g. 33) or hexadecimal (e.g. 0x21) format.", "Validation Error")
                return
        else:
            self.defaultKirbyHatText.BackColor = Color.White
        settings = Settings()
        settings.rspLoading = boolText(self.rspCheck.Checked)
        settings.fiftyCostumeCode = boolText(self.fiftyCCCheck.Checked)
        if self.pPlusRadioButton.Checked:
            settings.cssIconStyle = "P+"
        elif self.vBrawlRadioButton.Checked:
            settings.cssIconStyle = "vBrawl"
        elif self.PMRadioButton.Checked:
            settings.cssIconStyle = "PM"
        elif self.remixRadioButton.Checked:
            settings.cssIconStyle = "REMIX"
        if self.remixBPRadioButton.Checked:
            settings.bpStyle = "REMIX"
        elif self.vBrawlBPRadioButton.Checked:
            settings.bpStyle = "vBrawl"
        if self.vBrawlNameRadioButton.Checked:
            settings.portraitNameStyle = "vBrawl"
        elif self.PMNameRadioButton.Checked:
            settings.portraitNameStyle = "PM"
        if self.vBrawlReplayRadioButton.Checked:
            settings.replayIconStyle = "vBrawl"
        elif self.pPlusReplayRadioButton.Checked:
            settings.replayIconStyle = "P+"
        settings.installStocksToCSS = boolText(self.stockCssCheckbox.Checked)
        settings.installStocksToSSS = boolText(self.stockSssCheckbox.Checked)
        settings.installStockIconsToResult = boolText(self.stockResultCheckbox.Checked)
        settings.installStocksToStockFaceTex = boolText(self.stockRotationCheckbox.Checked)
        settings.installStocksToInfo = boolText(self.stockBattleCheckbox.Checked)
        settings.installPortraitNames = boolText(self.portraitNameCheckBox.Checked)
        settings.installBPNames = boolText(self.bpNameCheckbox.Checked)
        settings.installSingleplayerCosmetics = boolText(self.singlePlayerCheckBox.Checked)
        settings.franchiseIconSizeCSS = self.franchiseIconSizeText.Text
        settings.kirbyHatExe = self.kirbyExeFileBox.Text
        settings.installKirbyHats = boolText(self.installKirbyHatCheckbox.Checked)
        settings.defaultKirbyHat = hexId(self.defaultKirbyHatText.Text) if self.defaultKirbyHatText.Text.strip() != "" else "none"
        settings.assemblyFunctionsExe = self.codeMenuFileBox.Text
        settings.sawndReplaceExe = self.sawndReplaceExeText.Text
        settings.sfxChangeExe = self.sfxChangeExeText.Text
        if self.hexRadioButton.Checked:
            settings.soundbankStyle = "hex"
        elif self.decimalRadioButton.Checked:
            settings.soundbankStyle = "dec"
        settings.addSevenToSoundbankIds = boolText(self.incrementSoundbankIdCheck.Checked)
        settings.addSevenToSoundbankName = boolText(self.incrementSoundbankNameCheck.Checked)
        settings.gfxChangeExe = self.gfxChangeExeText.Text
        settings.installToSse = boolText(self.sseCheck.Checked)
        settings.installTrophies = boolText(self.trophyCheck.Checked)
        settings.installVictoryThemes = boolText(self.victoryThemeCheck.Checked)
        if self.unlockStartRadioButton.Checked:
            settings.sseUnlockStage = "start"
        elif self.unlockEndRadioButton.Checked:
            settings.sseUnlockStage = "end"
        stageListSetting = ""
        i = 0
        while i < len(self.customStageLists):
            stageListSetting += str(self.customStageLists[i])
            if i != len(self.customStageLists) - 1:
                stageListSetting += ","
            i += 1
        settings.customStageLists = stageListSetting
        attrs = vars(settings)
        File.WriteAllText(MainForm.BuildPath + '/settings.ini', '\n'.join("%s = %s" % item for item in attrs.items()))
        BrawlAPI.ShowMessage("Settings saved.", "Success")

#endregion

#region CHARACTER FORM

class CharacterForm(Form):

    def __init__(self):
        # Form parameters
        self.Text = 'Install Character'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.Height = 128
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.AutoSize = True
        self.MinimumSize = Size(250,128)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        # Radio buttons
        radioButtonGroup = GroupBox()
        radioButtonGroup.Dock = DockStyle.Top
        radioButtonGroup.Height = 48
        radioButtonGroup.TabIndex = 1
        self.rb1 = RadioButton()
        self.rb1.Location = Point(16, 16)
        self.rb1.Text = "Auto"
        self.rb1.Size = Size(64, 16)
        self.rb1.Checked = True
        self.rb1.CheckedChanged += self.autoChecked
        self.rb2 = RadioButton()
        self.rb2.Location = Point(80, 16)
        self.rb2.Text = "Fighter ID"
        self.rb2.Size = Size(72, 16)
        self.rb2.CheckedChanged += self.fighterIdChecked
        self.rb3 = RadioButton()
        self.rb3.Location = Point(160, 16)
        self.rb3.Text = "All IDs"
        self.rb3.Size = Size(64, 16)
        self.rb3.CheckedChanged += self.allConfigChecked
        radioButtonGroup.Controls.Add(self.rb1)
        radioButtonGroup.Controls.Add(self.rb2)
        radioButtonGroup.Controls.Add(self.rb3)

        # Fighter ID box
        self.fighterIdGroup = GroupBox()
        self.fighterIdGroup.Height = 80
        self.fighterIdGroup.Dock = DockStyle.Top
        self.fighterIdGroup.TabIndex = 2

        fighterIdPanel = Panel()
        fighterIdPanel.Location = Point(16, 16)
        fighterIdPanel.TabIndex = 1
        fighterIdLabel = Label()
        fighterIdLabel.Dock = DockStyle.Left
        fighterIdLabel.Text = "Fighter ID:"
        self.fighterIdTextbox = TextBox()
        self.fighterIdTextbox.Dock = DockStyle.Right

        fighterIdButton = Button()
        fighterIdButton.Text = "..."
        fighterIdButton.Size = Size(25, self.fighterIdTextbox.ClientSize.Height + 2)
        fighterIdButton.Location = Point(self.fighterIdTextbox.ClientSize.Width - fighterIdButton.Width, -1)
        fighterIdButton.Cursor = Cursors.Default
        fighterIdButton.Click += self.fighterIdButtonPressed

        self.fighterIdTextbox.Controls.Add(fighterIdButton)

        fighterIdPanel.Controls.Add(fighterIdLabel)
        fighterIdPanel.Controls.Add(self.fighterIdTextbox)

        cosmeticIdPanel = Panel()
        cosmeticIdPanel.Location = Point(16, 48)
        cosmeticIdPanel.TabIndex = 2
        cosmeticIdLabel = Label()
        cosmeticIdLabel.Dock = DockStyle.Left
        cosmeticIdLabel.Text = "Cosmetic ID:"
        self.cosmeticIdTextbox = TextBox()
        self.cosmeticIdTextbox.Dock = DockStyle.Right

        cosmeticIdButton = Button()
        cosmeticIdButton.Text = "..."
        cosmeticIdButton.Size = Size(25, self.cosmeticIdTextbox.ClientSize.Height + 2)
        cosmeticIdButton.Location = Point(self.cosmeticIdTextbox.ClientSize.Width - cosmeticIdButton.Width, -1)
        cosmeticIdButton.Cursor = Cursors.Default
        cosmeticIdButton.Click += self.cosmeticIdButtonPressed

        self.cosmeticIdTextbox.Controls.Add(cosmeticIdButton)

        cosmeticIdPanel.Controls.Add(cosmeticIdLabel)
        cosmeticIdPanel.Controls.Add(self.cosmeticIdTextbox)

        self.fighterIdGroup.Controls.Add(cosmeticIdPanel)
        self.fighterIdGroup.Controls.Add(fighterIdPanel)

        self.fighterIdGroup.Visible = False

        # Config IDs box
        self.configIdGroup = GroupBox()
        self.configIdGroup.Height = 128
        self.configIdGroup.Dock = DockStyle.Top
        self.configIdGroup.TabIndex = 3
        
        cosmeticConfigIdPanel = Panel()
        cosmeticConfigIdPanel.Location = Point(16, 16)
        cosmeticConfigIdPanel.TabIndex = 1
        cosmeticConfigIdLabel = Label()
        cosmeticConfigIdLabel.Dock = DockStyle.Left
        cosmeticConfigIdLabel.Text = "Cosmetic Config ID:"
        self.cosmeticConfigIdTextbox = TextBox()
        self.cosmeticConfigIdTextbox.Dock = DockStyle.Right

        cosmeticConfigIdButton = Button()
        cosmeticConfigIdButton.Text = "..."
        cosmeticConfigIdButton.Size = Size(25, self.cosmeticConfigIdTextbox.ClientSize.Height + 2)
        cosmeticConfigIdButton.Location = Point(self.cosmeticConfigIdTextbox.ClientSize.Width - cosmeticConfigIdButton.Width, -1)
        cosmeticConfigIdButton.Cursor = Cursors.Default
        cosmeticConfigIdButton.Click += self.cosmeticConfigIdButtonPressed

        self.cosmeticConfigIdTextbox.Controls.Add(cosmeticConfigIdButton)

        cosmeticConfigIdPanel.Controls.Add(cosmeticConfigIdLabel)
        cosmeticConfigIdPanel.Controls.Add(self.cosmeticConfigIdTextbox)

        slotConfigIdPanel = Panel()
        slotConfigIdPanel.Location = Point(16, 48)
        slotConfigIdPanel.TabIndex = 2
        slotConfigIdLabel = Label()
        slotConfigIdLabel.Dock = DockStyle.Left
        slotConfigIdLabel.Text = "Slot Config ID:"
        self.slotConfigIdTextbox = TextBox()
        self.slotConfigIdTextbox.Dock = DockStyle.Right

        slotConfigIdButton = Button()
        slotConfigIdButton.Text = "..."
        slotConfigIdButton.Size = Size(25, self.slotConfigIdTextbox.ClientSize.Height + 2)
        slotConfigIdButton.Location = Point(self.slotConfigIdTextbox.ClientSize.Width - slotConfigIdButton.Width, -1)
        slotConfigIdButton.Cursor = Cursors.Default
        slotConfigIdButton.Click += self.slotConfigIdButtonPressed

        self.slotConfigIdTextbox.Controls.Add(slotConfigIdButton)

        slotConfigIdPanel.Controls.Add(slotConfigIdLabel)
        slotConfigIdPanel.Controls.Add(self.slotConfigIdTextbox)

        cssSlotConfigIdPanel = Panel()
        cssSlotConfigIdPanel.Location = Point(16, 80)
        cssSlotConfigIdPanel.TabIndex = 3
        cssSlotConfigIdLabel = Label()
        cssSlotConfigIdLabel.Dock = DockStyle.Left
        cssSlotConfigIdLabel.Text = "CSS Slot Config ID:"
        self.cssSlotConfigIdTextbox = TextBox()
        self.cssSlotConfigIdTextbox.Dock = DockStyle.Right

        cssSlotConfigIdButton = Button()
        cssSlotConfigIdButton.Text = "..."
        cssSlotConfigIdButton.Size = Size(25, self.cssSlotConfigIdTextbox.ClientSize.Height + 2)
        cssSlotConfigIdButton.Location = Point(self.cssSlotConfigIdTextbox.ClientSize.Width - cssSlotConfigIdButton.Width, -1)
        cssSlotConfigIdButton.Cursor = Cursors.Default
        cssSlotConfigIdButton.Click += self.cssSlotConfigIdButtonPressed

        self.cssSlotConfigIdTextbox.Controls.Add(cssSlotConfigIdButton)

        cssSlotConfigIdPanel.Controls.Add(cssSlotConfigIdLabel)
        cssSlotConfigIdPanel.Controls.Add(self.cssSlotConfigIdTextbox)

        self.configIdGroup.Controls.Add(cssSlotConfigIdPanel)
        self.configIdGroup.Controls.Add(slotConfigIdPanel)
        self.configIdGroup.Controls.Add(cosmeticConfigIdPanel)

        self.configIdGroup.Visible = False

        # Checkbox
        checkboxPanel = Panel()
        checkboxPanel.Dock = DockStyle.Top
        checkboxPanel.Height = 48
        checkboxPanel.TabIndex = 4
        self.checkbox = CheckBox()
        self.checkbox.Text = "Sub Character?"
        self.checkbox.Location = Point(16, 16)
        self.checkbox.CheckedChanged += self.checkBoxChanged

        checkboxPanel.Controls.Add(self.checkbox)

        # Sub character box
        self.subCharacterGroup = GroupBox()
        self.subCharacterGroup.Height = 48
        self.subCharacterGroup.Dock = DockStyle.Top
        self.subCharacterGroup.TabIndex = 5

        subCharacterPanel = Panel()
        subCharacterPanel.Location = Point(16, 16)
        subCharacterLabel = Label()
        subCharacterLabel.Dock = DockStyle.Left
        subCharacterLabel.Text = "Base CSS Slot ID:"
        self.subCharacterTextbox = TextBox()
        self.subCharacterTextbox.Dock = DockStyle.Right

        subCharacterButton = Button()
        subCharacterButton.Text = "..."
        subCharacterButton.Size = Size(25, self.subCharacterTextbox.ClientSize.Height + 2)
        subCharacterButton.Location = Point(self.subCharacterTextbox.ClientSize.Width - subCharacterButton.Width, -1)
        subCharacterButton.Cursor = Cursors.Default
        subCharacterButton.Click += self.subCharacterButtonPressed

        self.subCharacterTextbox.Controls.Add(subCharacterButton)

        subCharacterPanel.Controls.Add(subCharacterLabel)
        subCharacterPanel.Controls.Add(self.subCharacterTextbox)

        self.subCharacterGroup.Controls.Add(subCharacterPanel)

        self.subCharacterGroup.Visible = False

        # Install button
        installButton = Button()
        installButton.Text = "Install"
        installButton.Dock = DockStyle.Bottom
        installButton.Click += self.installButtonPressed
        
        # Tooltips
        toolTip = ToolTip()
        toolTip.SetToolTip(fighterIdLabel, "Fighter ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(cosmeticIdLabel, "Cosmetic ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(cosmeticConfigIdLabel, "Cosmetic config ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(slotConfigIdLabel, "Slot config ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(cssSlotConfigIdLabel, "CSS slot config ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(self.checkbox, "When enabled, character will be installed as a sub character")
        toolTip.SetToolTip(subCharacterLabel, "The CSS slot config ID of the base character for this fighter")
        toolTip.SetToolTip(self.rb1, "All IDs will be selected automatically")      
        toolTip.SetToolTip(self.rb2, "Manually specify fighter ID and cosmetic ID")
        toolTip.SetToolTip(self.rb3, "Manually specify all Ex config IDs") 

        # Add controls
        self.Controls.Add(installButton)
        self.Controls.Add(self.subCharacterGroup)
        self.Controls.Add(checkboxPanel)
        self.Controls.Add(self.configIdGroup)
        self.Controls.Add(self.fighterIdGroup)
        self.Controls.Add(radioButtonGroup)

    def autoChecked(self, sender, args):
        self.configIdGroup.Visible = False
        self.fighterIdGroup.Visible = False
        clearTextBoxes(self.configIdGroup)
        clearTextBoxes(self.fighterIdGroup)

    def fighterIdChecked(self, sender, args):
        self.fighterIdGroup.Visible = False
        self.configIdGroup.Visible = False
        self.configIdGroup.Visible = True
        self.configIdGroup.Visible = False
        self.fighterIdGroup.Visible = True 
        clearTextBoxes(self.configIdGroup)   

    def allConfigChecked(self, sender, args):
        self.fighterIdGroup.Visible = False
        self.configIdGroup.Visible = False
        self.configIdGroup.Visible = True
        self.fighterIdGroup.Visible = True

    def checkBoxChanged(self, sender, args):
        if self.checkbox.Checked:
            self.subCharacterGroup.Visible = True
        else:
            self.subCharacterGroup.Visible = False
            clearTextBoxes(self.subCharacterGroup)

    def fighterIdButtonPressed(self, sender, args):
        id = showIdPicker()
        if id:
            self.fighterIdTextbox.Text = id

    def cosmeticIdButtonPressed(self, sender, args):
        id = showImageIdPicker("cosmetic")
        if id:
            self.cosmeticIdTextbox.Text = id

    def cosmeticConfigIdButtonPressed(self, sender, args):
        id = showIdPicker("cosmetic")
        if id:
            self.cosmeticConfigIdTextbox.Text = id

    def slotConfigIdButtonPressed(self, sender, args):
        id = showIdPicker("slot")
        if id:
            self.slotConfigIdTextbox.Text = id

    def cssSlotConfigIdButtonPressed(self, sender, args):
        id = showIdPicker("cssSlot")
        if id:
            self.cssSlotConfigIdTextbox.Text = id

    def subCharacterButtonPressed(self, sender, args):
        id = showIdPicker("cssSlot")
        if id:
            self.subCharacterTextbox.Text = id

    def installButtonPressed(self, sender, args):
        validationPassed = True
        if self.rb2.Checked or self.rb3.Checked:
            valid = validateTextBoxes(self.fighterIdGroup)
            if not valid:
                validationPassed = False
        if self.rb3.Checked:
            valid = validateTextBoxes(self.configIdGroup)
            if not valid:
                validationPassed = False
        if self.checkbox.Checked:
            valid = validateTextBoxes(self.subCharacterGroup)
            if not valid:
                validationPassed = False
        if validationPassed == True:
            conflictText = idConflictCheck(self.fighterIdTextbox.Text, self.cosmeticIdTextbox.Text, self.slotConfigIdTextbox.Text, self.cosmeticConfigIdTextbox.Text, self.cssSlotConfigIdTextbox.Text)
            if conflictText:
                overwrite = BrawlAPI.ShowYesNoPrompt(conflictText + '\n\n Would you like to overwrite existing IDs?', 'Conflicts Found')
                if not overwrite:
                    return
            self.DialogResult = DialogResult.OK
            self.Close()
        else:
            BrawlAPI.ShowMessage("One or more fields contain invalid values. Please ensure all IDs are in either decimal (e.g. 33) or hexadecimal (e.g. 0x21) format.", "Validation Error")

#endregion CHARACTER FORM

#region SINGLE ID FORM

class IdEntryForm(Form):
    # idTypes: fighter, cosmetic, slot, cssSlot, cosmeticImage, franchiseImage
    def __init__(self, title="Enter ID", buttonText="Select", idType="fighter", labelText = "Fighter ID:", customList=[]):
        # Form parameters
        self.Text = title
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.Height = 128
        self.AutoSize = True
        self.MinimumSize = Size(250,128)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.idType = idType
        self.customList = customList

        # Fighter ID box
        self.idGroup = GroupBox()
        self.idGroup.Height = 80
        self.idGroup.Dock = DockStyle.Top
        self.idGroup.TabIndex = 2

        idPanel = Panel()
        idPanel.Location = Point(16, 16)
        idPanel.TabIndex = 1
        idLabel = Label()
        idLabel.Dock = DockStyle.Left
        idLabel.Text = labelText
        self.idTextbox = TextBox()
        self.idTextbox.Dock = DockStyle.Right

        idButton = Button()
        idButton.Text = "..."
        idButton.Size = Size(25, self.idTextbox.ClientSize.Height + 2)
        idButton.Location = Point(self.idTextbox.ClientSize.Width - idButton.Width, -1)
        idButton.Cursor = Cursors.Default
        idButton.Click += self.idButtonPressed

        self.idGroup.Controls.Add(idPanel)

        self.idTextbox.Controls.Add(idButton)

        idPanel.Controls.Add(idLabel)
        idPanel.Controls.Add(self.idTextbox)

        # Button
        button = Button()
        button.Text = buttonText
        button.Dock = DockStyle.Bottom
        button.Click += self.buttonPressed

         # Add controls
        self.Controls.Add(button)
        self.Controls.Add(self.idGroup)

    def idButtonPressed(self, sender, args):
        if "Image" not in self.idType:
            id = showIdPicker(self.idType, self.customList)
        else:
            id = showImageIdPicker(self.idType.replace("Image", ""))
        if id:
            self.idTextbox.Text = id

    def buttonPressed(self, sender, args):
        validationPassed = True
        valid = validateTextBoxes(self.idGroup)
        if not valid:
            validationPassed = False
        if validationPassed == True:
            self.DialogResult = DialogResult.OK
            self.Close()
        else:
            BrawlAPI.ShowMessage("One or more fields contain invalid values. Please ensure all IDs are in either decimal (e.g. 33) or hexadecimal (e.g. 0x21) format.", "Validation Error")

#endregion SINGLE ID FORM

#region COSTUME FORM

class CostumeForm(Form):

    def __init__(self, images, skipPositions=[], remove=False, availableIds=[]):
        # Form parameters
        self.Text = 'Select Costume'
        self.index = 0 # Index of selected costume
        self.labelIndex = 0 # Index displayed on label
        self.Width = 250
        self.Height = 360
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False

        # The action that will be performed
        self.action = ""

        self.skipPositions = skipPositions
        self.length = 0 # Actual count of costumes
        i = 0
        while i < len(images):
            if i not in skipPositions:
                self.length += 1
            i += 1

        # Costume label
        self.label = Label()
        self.label.Text = "Costume %s" % (self.labelIndex + 1)
        self.label.Dock = DockStyle.Bottom
        self.label.Height = 24
        self.label.Width = 150
        self.label.TextAlign = ContentAlignment.MiddleCenter

        dropDownGroup = GroupBox()
        dropDownGroup.Dock = DockStyle.Bottom
        dropDownGroup.Height = 64
        dropDownGroup.Visible = not remove

        dropDownLabel = Label()
        dropDownLabel.Anchor = AnchorStyles.Bottom
        dropDownLabel.TextAlign = ContentAlignment.MiddleCenter
        dropDownLabel.Location = Point(dropDownGroup.Width/2 - (dropDownLabel.Width)/2, 16)
        dropDownLabel.Text = "Starting ID"
        dropDownLabel.Height = 16

        self.dropDown = ComboBox()
        self.dropDown.Anchor = AnchorStyles.Bottom
        self.dropDown.Width = 64
        self.dropDown.Location = Point(dropDownGroup.Width/2 - (self.dropDown.Width)/2, 32)
        self.dropDown.DropDownStyle = ComboBoxStyle.DropDownList
        self.dropDown.DataSource = availableIds if len(availableIds) > 0 else ['00']

        dropDownGroup.Controls.Add(dropDownLabel)
        dropDownGroup.Controls.Add(self.dropDown)

        # Store number of images and images
        self.imageCount = len(images)
        self.images = images

        # Right arrow button
        rightButton = Button()
        rightButton.Text = ">"
        rightButton.Dock = DockStyle.Right
        rightButton.Width = 30

        rightButton.Click += self.rightButtonPressed

        # Left arrow button
        leftButton = Button()
        leftButton.Text = "<"
        leftButton.Dock = DockStyle.Left
        leftButton.Width = 30

        leftButton.Click += self.leftButtonPressed

        # Picturebox
        self.pictureBox = PictureBox()
        self.pictureBox.Dock = DockStyle.Fill
        self.image = self.images[self.index]
        self.pictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        self.pictureBox.Image = self.image

        # Insert Before
        beforeButton = Button()
        beforeButton.Text = "Insert Before"
        beforeButton.Dock = DockStyle.Bottom

        beforeButton.Click += self.beforeButtonPressed

        # Insert After
        afterButton = Button()
        afterButton.Text = "Insert After"
        afterButton.Dock = DockStyle.Bottom

        afterButton.Click += self.afterButtonPressed

        # Replace
        replaceButton = Button()
        replaceButton.Text = "Replace"
        replaceButton.Dock = DockStyle.Bottom

        replaceButton.Click += self.replaceButtonPressed

        # Uninstall
        uninstallButton = Button()
        uninstallButton.Text = "Uninstall"
        uninstallButton.Dock = DockStyle.Bottom

        uninstallButton.Click += self.uninstallButtonPressed

        # Tooltips
        toolTip = ToolTip()
        toolTip.SetToolTip(dropDownLabel, "The starting costume .pac ID for the costumes to be installed with. The first costume will use this ID and subsequent costumes will use the next available ID.")

        # Add controls
        self.Controls.Add(self.pictureBox)
        self.Controls.Add(self.label)
        self.Controls.Add(dropDownGroup)
        self.Controls.Add(rightButton)
        self.Controls.Add(leftButton)
        if not remove:
            self.Controls.Add(beforeButton)
            self.Controls.Add(afterButton)
            self.Controls.Add(replaceButton)
        else:
            self.Controls.Add(uninstallButton)

    def rightButtonPressed(self, sender, args):
        if self.index < self.imageCount - 1:
            self.index += 1
            while self.index in self.skipPositions:
                self.index += 1
            if self.index > self.imageCount - 1:
                self.index = 0
        else:
            self.index = 0
        if self.labelIndex < self.length - 1:
            self.labelIndex += 1
        else:
            self.labelIndex = 0
        self.image = self.images[self.index]
        self.pictureBox.Image = self.image
        self.label.Text = "Costume %s" % (self.labelIndex + 1)

    def leftButtonPressed(self, sender, args):
        if self.index > 0:
            self.index -= 1
            while self.index in self.skipPositions:
                self.index -= 1
            if self.index < 0:
                self.index = 0
        else:
            self.index = self.imageCount - 1
            while self.index in self.skipPositions:
                self.index -= 1
            if self.index < 0:
                self.index = 0
        if self.labelIndex > 0:
            self.labelIndex -= 1
        else:
            self.labelIndex = self.length - 1
        self.image = self.images[self.index]
        self.pictureBox.Image = self.image
        self.label.Text = "Costume %s" % (self.labelIndex + 1)

    def beforeButtonPressed(self, sender, args):
        self.action = "insert"
        self.index += 1
        self.DialogResult = DialogResult.OK
        self.Close()
        
    def afterButtonPressed(self, sender, args):
        self.action = "insert"
        self.index += 2
        self.DialogResult = DialogResult.OK
        self.Close()

    def replaceButtonPressed(self, sender, args):
        self.action = "replace"
        self.index += 1
        self.DialogResult = DialogResult.OK
        self.Close()

    def uninstallButtonPressed(self, sender, args):
        self.action = "remove"
        self.index += 1
        self.DialogResult = DialogResult.OK
        self.Close()

#endregion COSTUME FORM

#region PACKAGE CHARACTER FORM

class PackageCharacterForm(Form):

    def __init__(self, zipFile=""):
        # Form parameters
        self.Text = 'Package Character'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MinimizeBox = False
        self.MaximizeBox = False
        #self.MinimumSize = Size(267,344)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.costumeGroups = BindingSource()
        self.costumeGroups.DataSource = []
        self.zipFile = zipFile

        # Cosmetics Groupbox
        self.cosmeticsGroupBox = GroupBox()
        self.cosmeticsGroupBox.Location = Point(0,0)
        self.cosmeticsGroupBox.AutoSize = True
        self.cosmeticsGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.cosmeticsGroupBox.Text = "Cosmetics"
        self.cosmeticsGroupBox.Click += self.toggleGroupBox

        #region CSP and Stocks

        # CSP Groupbox
        self.cspGroupBox = GroupBox()
        self.cspGroupBox.Location = Point(0,16)
        self.cspGroupBox.AutoSize = True
        self.cspGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.cspGroupBox.Text = "CSPs and Stocks"
        self.cspGroupBox.Click += self.toggleGroupBox

        cspCostumeLabel = Label()
        cspCostumeLabel.Text = "Groups:"
        cspCostumeLabel.Location = Point(16, 16)
        cspCostumeLabel.Height = 16
        cspCostumeLabel.Width = 80

        self.cspCostumeListBox = ListBox()
        self.cspCostumeListBox.Width = 80
        self.cspCostumeListBox.Height = 120
        self.cspCostumeListBox.Location = Point(cspCostumeLabel.Location.X, cspCostumeLabel.Location.Y + 16)
        self.cspCostumeListBox.HorizontalScrollbar = True
        self.cspCostumeListBox.DataSource = self.costumeGroups
        self.cspCostumeListBox.DisplayMember = "costumeGroup"
        self.cspCostumeListBox.SelectedValueChanged += self.cspCostumeChanged

        cspCostumeButton = Button()
        cspCostumeButton.Text = "+"
        cspCostumeButton.Size = Size(16, 16)
        cspCostumeButton.Location = Point(self.cspCostumeListBox.Location.X + self.cspCostumeListBox.Width + 4, self.cspCostumeListBox.Location.Y)
        cspCostumeButton.Click += self.cspCostumeButtonPressed

        cspCostumeRemoveButton = Button()
        cspCostumeRemoveButton.Text = "-"
        cspCostumeRemoveButton.Size = Size(16, 16)
        cspCostumeRemoveButton.Location = Point(cspCostumeButton.Location.X, cspCostumeButton.Location.Y + cspCostumeButton.Height + 4)
        cspCostumeRemoveButton.Click += self.cspCostumeRemoveButtonPressed

        self.cspListBox = ListBox()
        self.cspListBox.Width = 80
        self.cspListBox.Height = 120
        self.cspListBox.Location = Point(cspCostumeButton.Location.X + cspCostumeButton.Width + 16, cspCostumeButton.Location.Y)
        self.cspListBox.HorizontalScrollbar = True
        self.cspListBox.DisplayMember = "name"
        self.cspListBox.SelectedValueChanged += self.cspChanged

        cspLabel = Label()
        cspLabel.Text = "Colors:"
        cspLabel.Location = Point(self.cspListBox.Location.X, self.cspListBox.Location.Y - 16)
        cspLabel.Height = 16

        self.addColorButton = Button()
        self.addColorButton.Text = "+"
        self.addColorButton.Size = Size(16, 16)
        self.addColorButton.Location = Point(self.cspListBox.Location.X + self.cspListBox.Width + 4, self.cspListBox.Location.Y)
        self.addColorButton.Enabled = self.cspCostumeListBox.SelectedItem
        self.addColorButton.Click += self.addColorButtonPressed

        self.removeColorButton = Button()
        self.removeColorButton.Text = "-"
        self.removeColorButton.Size = Size(16, 16)
        self.removeColorButton.Location = Point(self.addColorButton.Location.X, self.addColorButton.Location.Y + self.addColorButton.Height + 4)
        self.removeColorButton.Enabled = self.cspCostumeListBox.SelectedItem
        self.removeColorButton.Click += self.removeColorButtonPressed

        self.cspPictureBox = PictureBox()
        self.cspPictureBox.Location = Point(self.addColorButton.Location.X + self.addColorButton.Width + 16, self.addColorButton.Location.Y)
        self.cspPictureBox.Size = Size(64, 80)
        self.cspPictureBox.SizeMode = PictureBoxSizeMode.StretchImage

        cspPictureBoxLabel = Label()
        cspPictureBoxLabel.Text = "CSP:"
        cspPictureBoxLabel.Width = 32
        cspPictureBoxLabel.Location = Point(self.cspPictureBox.Location.X, self.cspPictureBox.Location.Y - 16)

        self.cspButton = Button()
        self.cspButton.Text = "Browse..."
        self.cspButton.Location = Point(self.cspPictureBox.Location.X, self.cspPictureBox.Location.Y + self.cspPictureBox.Height + 4)
        self.cspButton.Enabled = len(self.cspCostumeListBox.Items) > 0
        self.cspButton.Click += self.cspButtonPressed

        self.cspHdPictureBox = PictureBox()
        self.cspHdPictureBox.Location = Point(self.cspPictureBox.Location.X + self.cspPictureBox.Width + 16, self.cspPictureBox.Location.Y)
        self.cspHdPictureBox.Size = Size(64, 80)
        self.cspHdPictureBox.SizeMode = PictureBoxSizeMode.StretchImage

        cspHdPictureBoxLabel = Label()
        cspHdPictureBoxLabel.Text = "HD CSP:"
        cspHdPictureBoxLabel.Location = Point(self.cspHdPictureBox.Location.X, self.cspHdPictureBox.Location.Y - 16)

        self.cspHdButton = Button()
        self.cspHdButton.Text = "Browse..."
        self.cspHdButton.Location = Point(self.cspHdPictureBox.Location.X, self.cspHdPictureBox.Location.Y + self.cspHdPictureBox.Height + 4)
        self.cspHdButton.Enabled = len(self.cspCostumeListBox.Items) > 0
        self.cspHdButton.Click += self.cspHdButtonPressed

        stockPictureBoxLabel = Label()
        stockPictureBoxLabel.Text = "Stock:"
        stockPictureBoxLabel.Width = 36
        stockPictureBoxLabel.Height = 16
        stockPictureBoxLabel.Location = Point(self.cspButton.Location.X, self.cspButton.Location.Y + self.cspButton.Height + 16)

        self.stockPictureBox = PictureBox()
        self.stockPictureBox.Location = Point(stockPictureBoxLabel.Location.X, stockPictureBoxLabel.Location.Y + 16)
        self.stockPictureBox.Size = Size(32, 32)
        self.stockPictureBox.SizeMode = PictureBoxSizeMode.StretchImage

        self.stockButton = Button()
        self.stockButton.Text = "Browse..."
        self.stockButton.Location = Point(self.stockPictureBox.Location.X, self.stockPictureBox.Location.Y + self.stockPictureBox.Height + 4)
        self.stockButton.Enabled = len(self.cspCostumeListBox.Items) > 0
        self.stockButton.Click += self.stockButtonPressed

        self.stockHdPictureBox = PictureBox()
        self.stockHdPictureBox.Location = Point(self.stockPictureBox.Location.X + self.stockButton.Width + 4, self.stockPictureBox.Location.Y)
        self.stockHdPictureBox.Size = Size(32, 32)
        self.stockHdPictureBox.SizeMode = PictureBoxSizeMode.StretchImage

        stockHdPictureBoxLabel = Label()
        stockHdPictureBoxLabel.Text = "HD Stock:"
        stockHdPictureBoxLabel.Height = 16
        stockHdPictureBoxLabel.Location = Point(self.stockHdPictureBox.Location.X, self.stockHdPictureBox.Location.Y - 16)

        self.stockHdButton = Button()
        self.stockHdButton.Text = "Browse..."
        self.stockHdButton.Location = Point(self.stockHdPictureBox.Location.X, self.stockHdPictureBox.Location.Y + self.stockHdPictureBox.Height + 4)
        self.stockHdButton.Enabled = len(self.cspCostumeListBox.Items) > 0
        self.stockHdButton.Click += self.stockHdButtonPressed

        self.cspGroupBox.Controls.Add(cspCostumeLabel)
        self.cspGroupBox.Controls.Add(self.cspCostumeListBox)
        self.cspGroupBox.Controls.Add(self.cspListBox)
        self.cspGroupBox.Controls.Add(self.addColorButton)
        self.cspGroupBox.Controls.Add(self.removeColorButton)
        self.cspGroupBox.Controls.Add(cspCostumeButton)
        self.cspGroupBox.Controls.Add(cspCostumeRemoveButton)
        self.cspGroupBox.Controls.Add(cspLabel)
        self.cspGroupBox.Controls.Add(self.cspPictureBox)
        self.cspGroupBox.Controls.Add(self.cspButton)
        self.cspGroupBox.Controls.Add(cspPictureBoxLabel)
        self.cspGroupBox.Controls.Add(self.cspHdPictureBox)
        self.cspGroupBox.Controls.Add(self.cspHdButton)
        self.cspGroupBox.Controls.Add(cspHdPictureBoxLabel)
        self.cspGroupBox.Controls.Add(stockPictureBoxLabel)
        self.cspGroupBox.Controls.Add(self.stockPictureBox)
        self.cspGroupBox.Controls.Add(self.stockButton)
        self.cspGroupBox.Controls.Add(stockHdPictureBoxLabel)
        self.cspGroupBox.Controls.Add(self.stockHdPictureBox)
        self.cspGroupBox.Controls.Add(self.stockHdButton)

        #endregion CSPs and Stocks
        
        #region BPs

        bpTabNames = ["vBrawl", "REMIX"]

        # BP Groupbox
        self.bpGroupBox = GroupBox()
        self.bpGroupBox.AutoSize = True
        self.bpGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.bpGroupBox.MinimumSize = Size(350, 250)
        self.bpGroupBox.MaximumSize = Size(350, 250)
        self.bpGroupBox.Text = "BPs"
        self.bpGroupBox.Click += self.toggleGroupBox

        self.bpTabControl = TabControl()
        self.bpTabControl.Dock = DockStyle.Fill

        bpTabs = [None] * len(bpTabNames)
        bpListBoxLabels = [None] * len(bpTabNames)
        self.bpListBoxes = [None] * len(bpTabNames)
        bpAddButtons = [None] * len(bpTabNames)
        bpRemoveButtons = [None] * len(bpTabNames)
        self.bpPictureBoxes = [None] * len(bpTabNames)
        bpPictureBoxLabels = [None] * len(bpTabNames)
        self.bpButtons = [None] * len(bpTabNames)
        self.bpHdButtons = [None] * len(bpTabNames)
        self.bpHdPictureBoxes = [None] * len(bpTabNames)
        bpHdPictureBoxLabels = [None] * len(bpTabNames)
        self.bps = [None] * len(bpTabNames)
        self.bpNameImage = [None] * len(bpTabNames)
        bpNameLabels = [None] * len(bpTabNames)
        self.bpNamePictureBoxes = [None] * len(bpTabNames)
        self.bpNameButtons = [None] * len(bpTabNames)
        self.bpNameHdImage = [None] * len(bpTabNames)
        self.bpNameHdPictureBoxes = [None] * len(bpTabNames)
        bpNameHdLabels = [None] * len(bpTabNames)
        self.bpNameHdButtons = [None] * len(bpTabNames)

        i = 0
        while i < len(bpTabs):
            self.bps[i] = BindingSource()
            self.bps[i].DataSource = []

            # Tabs
            bpTabs[i] = TabPage()
            bpTabs[i].Text = bpTabNames[i]
            bpTabs[i].Name = bpTabNames[i]
            bpTabs[i].Anchor = (AnchorStyles.Bottom | AnchorStyles.Top | AnchorStyles.Right | AnchorStyles.Left)

            # Labels
            bpListBoxLabels[i] = Label()
            bpListBoxLabels[i].Text = "BPs:"
            bpListBoxLabels[i].Location = Point(16, 4)
            bpListBoxLabels[i].Height = 16
            bpListBoxLabels[i].Width = 80

            # Listboxes
            self.bpListBoxes[i] = ListBox()
            self.bpListBoxes[i].Width = 80
            self.bpListBoxes[i].Height = 120
            self.bpListBoxes[i].Location = Point(bpListBoxLabels[i].Location.X, bpListBoxLabels[i].Location.Y + bpListBoxLabels[i].Height)
            self.bpListBoxes[i].HorizontalScrollbar = True
            self.bpListBoxes[i].DataSource = self.bps[i]
            self.bpListBoxes[i].DisplayMember = "name"
            self.bpListBoxes[i].SelectedValueChanged += self.bpChanged

            # Add Buttons
            bpAddButtons[i] = Button()
            bpAddButtons[i].Text = "+"
            bpAddButtons[i].Size = Size(16, 16)
            bpAddButtons[i].Location = Point(self.bpListBoxes[i].Location.X + self.bpListBoxes[i].Width + 4, self.bpListBoxes[i].Location.Y)
            bpAddButtons[i].Click += self.addBpButtonPressed

            # Remove Buttons
            bpRemoveButtons[i] = Button()
            bpRemoveButtons[i].Text = "-"
            bpRemoveButtons[i].Size = Size(16, 16)
            bpRemoveButtons[i].Location = Point(bpAddButtons[i].Location.X, bpAddButtons[i].Location.Y + bpAddButtons[i].Height + 4)
            bpRemoveButtons[i].Click += self.removeBpButtonPressed

            # BP Picture Boxes
            self.bpPictureBoxes[i] = PictureBox()
            self.bpPictureBoxes[i].Location = Point(bpAddButtons[i].Location.X + bpAddButtons[i].Width + 16, bpAddButtons[i].Location.Y)
            self.bpPictureBoxes[i].Size = Size(48, 56)
            self.bpPictureBoxes[i].SizeMode = PictureBoxSizeMode.StretchImage

            # Labels
            bpPictureBoxLabels[i] = Label()
            bpPictureBoxLabels[i].Text = "BP:"
            bpPictureBoxLabels[i].Location = Point(self.bpPictureBoxes[i].Location.X, self.bpPictureBoxes[i].Location.Y - 16)
            bpPictureBoxLabels[i].Height = 16
            bpPictureBoxLabels[i].Width = 80

            # BP Buttons
            self.bpButtons[i] = Button()
            self.bpButtons[i].Text = "Browse..."
            self.bpButtons[i].Location = Point(self.bpPictureBoxes[i].Location.X, self.bpPictureBoxes[i].Location.Y + self.bpPictureBoxes[i].Height + 4)
            self.bpButtons[i].Click += self.bpButtonPressed

            # BP HD
            self.bpHdPictureBoxes[i] = PictureBox()
            self.bpHdPictureBoxes[i].Location = Point(self.bpPictureBoxes[i].Location.X + self.bpButtons[i].Width + 4, self.bpPictureBoxes[i].Location.Y)
            self.bpHdPictureBoxes[i].Size = Size(48, 56)
            self.bpHdPictureBoxes[i].SizeMode = PictureBoxSizeMode.StretchImage

            bpHdPictureBoxLabels[i] = Label()
            bpHdPictureBoxLabels[i].Text = "HD BP:"
            bpHdPictureBoxLabels[i].Location = Point(self.bpHdPictureBoxes[i].Location.X, self.bpHdPictureBoxes[i].Location.Y - 16)
            bpHdPictureBoxLabels[i].Height = 16
            bpHdPictureBoxLabels[i].Width = 80

            self.bpHdButtons[i] = Button()
            self.bpHdButtons[i].Text = "Browse..."
            self.bpHdButtons[i].Location = Point(self.bpHdPictureBoxes[i].Location.X, self.bpHdPictureBoxes[i].Location.Y + self.bpHdPictureBoxes[i].Height + 4)
            self.bpHdButtons[i].Click += self.bpHdButtonPressed

            # BP Name
            self.bpNameImage[i] = ""
            bpNameLabels[i] = Label()
            bpNameLabels[i].Text = "BP Name:"
            bpNameLabels[i].Location = Point(self.bpButtons[i].Location.X, self.bpButtons[i].Location.Y + self.bpButtons[i].Height + 16)
            bpNameLabels[i].Height = 16
            bpNameLabels[i].Width = 80

            self.bpNamePictureBoxes[i] = PictureBox()
            self.bpNamePictureBoxes[i].Location = Point(bpNameLabels[i].Location.X, bpNameLabels[i].Location.Y + bpNameLabels[i].Height + 16)
            self.bpNamePictureBoxes[i].Size = Size(72, 12)
            self.bpNamePictureBoxes[i].SizeMode = PictureBoxSizeMode.StretchImage

            self.bpNameButtons[i] = Button()
            self.bpNameButtons[i].Text = "Browse..."
            self.bpNameButtons[i].Location = Point(self.bpNamePictureBoxes[i].Location.X, self.bpNamePictureBoxes[i].Location.Y + self.bpNamePictureBoxes[i].Height + 4)
            self.bpNameButtons[i].Click += self.bpNameButtonPressed
            
            # BP Name HD
            self.bpNameHdImage[i] = ""
            self.bpNameHdPictureBoxes[i] = PictureBox()
            self.bpNameHdPictureBoxes[i].Location = Point(self.bpNamePictureBoxes[i].Location.X + self.bpNameButtons[i].Width + 4, self.bpNamePictureBoxes[i].Location.Y)
            self.bpNameHdPictureBoxes[i].Size = Size(72, 12)
            self.bpNameHdPictureBoxes[i].SizeMode = PictureBoxSizeMode.StretchImage

            bpNameHdLabels[i] = Label()
            bpNameHdLabels[i].Text = "HD BP Name:"
            bpNameHdLabels[i].Location = Point(self.bpNameHdPictureBoxes[i].Location.X, bpNameLabels[i].Location.Y)
            bpNameHdLabels[i].Height = 16
            bpNameHdLabels[i].Width = 80

            self.bpNameHdButtons[i] = Button()
            self.bpNameHdButtons[i].Text = "Browse..."
            self.bpNameHdButtons[i].Location = Point(self.bpNameHdPictureBoxes[i].Location.X, self.bpNameHdPictureBoxes[i].Location.Y + 16)
            self.bpNameHdButtons[i].Click += self.bpNameHdButtonPressed

            # Add to page
            bpTabs[i].Controls.Add(bpListBoxLabels[i])
            bpTabs[i].Controls.Add(self.bpListBoxes[i])
            bpTabs[i].Controls.Add(bpAddButtons[i])
            bpTabs[i].Controls.Add(bpRemoveButtons[i])
            bpTabs[i].Controls.Add(self.bpPictureBoxes[i])
            bpTabs[i].Controls.Add(bpPictureBoxLabels[i])
            bpTabs[i].Controls.Add(self.bpButtons[i])
            bpTabs[i].Controls.Add(self.bpHdPictureBoxes[i])
            bpTabs[i].Controls.Add(bpHdPictureBoxLabels[i])
            bpTabs[i].Controls.Add(self.bpHdButtons[i])
            bpTabs[i].Controls.Add(bpNameLabels[i])
            bpTabs[i].Controls.Add(self.bpNamePictureBoxes[i])
            bpTabs[i].Controls.Add(self.bpNameButtons[i])
            bpTabs[i].Controls.Add(self.bpNameHdPictureBoxes[i])
            bpTabs[i].Controls.Add(bpNameHdLabels[i])
            bpTabs[i].Controls.Add(self.bpNameHdButtons[i])

            # Add to control
            self.bpTabControl.Controls.Add(bpTabs[i])
            i += 1

        self.bpGroupBox.Controls.Add(self.bpTabControl)

        #endregion BPs

        self.cssGroupBox = GroupBox()
        self.cssGroupBox.AutoSize = True
        self.cssGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.cssGroupBox.MinimumSize = Size(350, 250)
        self.cssGroupBox.MaximumSize = Size(350, 250)
        self.cssGroupBox.Text = "CSS Icons"
        self.cssGroupBox.Click += self.toggleGroupBox

        cssTabNames = ["vBrawl", "PM", "P+", "REMIX"]
        cssImageObjects = [ImageObject("CSS Icon", Size(64,64)), ImageObject("HD CSS Icon", Size(64,64)), ImageObject("Name", Size(56,24)), ImageObject("HD Name", Size(56,24))]

        self.cssTabControl = TabImageControl(cssTabNames, cssImageObjects)
        
        self.cssGroupBox.Controls.Add(self.cssTabControl)

        self.replayGroupBox = GroupBox()
        self.replayGroupBox.AutoSize = True
        self.replayGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.replayGroupBox.MinimumSize = Size(225, 125)
        self.replayGroupBox.MaximumSize = Size(225, 125)
        self.replayGroupBox.Text = "Replay Icons"
        self.replayGroupBox.Click += self.toggleGroupBox

        replayTabNames = ["vBrawl", "P+"]
        replayImageObjects = [ImageObject("Replay Icon", Size(64,24)), ImageObject("HD Replay Icon", Size(64,24))]

        self.replayTabControl = TabImageControl(replayTabNames, replayImageObjects)
        
        self.replayGroupBox.Controls.Add(self.replayTabControl)

        self.portraitNameGroupBox = GroupBox()
        self.portraitNameGroupBox.AutoSize = True
        self.portraitNameGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.portraitNameGroupBox.MinimumSize = Size(315, 150)
        self.portraitNameGroupBox.MaximumSize = Size(315, 150)
        self.portraitNameGroupBox.Text = "Portrait Name"
        self.portraitNameGroupBox.Click += self.toggleGroupBox

        portraitTabNames = ["vBrawl", "PM"]
        portraitNameImageObjects = [ImageObject("Name", Size(144,32)), ImageObject("HD Name", Size(144,32))]

        self.portraitNameTabControl = TabImageControl(portraitTabNames, portraitNameImageObjects)
        
        self.portraitNameGroupBox.Controls.Add(self.portraitNameTabControl)

        self.franchiseIconGroupBox = GroupBox()
        self.franchiseIconGroupBox.AutoSize = True
        self.franchiseIconGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.franchiseIconGroupBox.Text = "Franchise Icon"
        self.franchiseIconGroupBox.Click += self.toggleGroupBox

        franchiseIconImageObjects = [ImageObject("Black", Size(64,64)), ImageObject("Transparent", Size(64,64))]

        self.franchiseIconImageControl = ImageControl(franchiseIconImageObjects)
        self.franchiseIconImageControl.Location = Point(16, 16)

        self.franchiseModelControl = FileControl("Select your franchise icon model file", "MDL0 files|*.mdl0", "Model")
        self.franchiseModelControl.Location = Point(self.franchiseIconImageControl.Location.X, self.franchiseIconImageControl.Location.Y + self.franchiseIconImageControl.Height)
        
        self.franchiseIconGroupBox.Controls.Add(self.franchiseIconImageControl)
        self.franchiseIconGroupBox.Controls.Add(self.franchiseModelControl)

        self.cosmeticsGroupBox.Controls.Add(self.cspGroupBox)
        self.cosmeticsGroupBox.Controls.Add(self.bpGroupBox)
        self.cosmeticsGroupBox.Controls.Add(self.cssGroupBox)
        self.cosmeticsGroupBox.Controls.Add(self.replayGroupBox)
        self.cosmeticsGroupBox.Controls.Add(self.portraitNameGroupBox)
        self.cosmeticsGroupBox.Controls.Add(self.franchiseIconGroupBox)

        self.readmeGroupBox = GroupBox()
        self.readmeGroupBox.AutoSize = True
        self.readmeGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.readmeGroupBox.Text = "README"
        self.readmeGroupBox.Click += self.toggleGroupBox

        self.readmeControl = LabeledTextBox("Body", multiline=True, size=Size(500,80))
        self.readmeControl.Location = Point(4,16)

        self.readmeGroupBox.Controls.Add(self.readmeControl)

        # Fighter Files Groupbox
        self.fighterGroupBox = GroupBox()
        self.fighterGroupBox.AutoSize = True
        self.fighterGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.fighterGroupBox.Text = "Fighter Files"
        self.fighterGroupBox.Click += self.toggleGroupBox

        self.mainFighterGroupBox = GroupBox()
        self.mainFighterGroupBox.AutoSize = True
        self.mainFighterGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.mainFighterGroupBox.Text = "Main Fighter Files"
        self.mainFighterGroupBox.Click += self.toggleGroupBox

        self.pacFilesControl = MultiFileControl("Select your fighter pac files", labelText="PAC Files")
        self.pacFilesControl.Location = Point(16, 16)

        self.exConfigsControl = MultiFileControl("Select your fighter ex config files", "DAT files|*.dat", "Ex Configs")
        self.exConfigsControl.Location = Point(self.pacFilesControl.Location.X + self.pacFilesControl.Width, self.pacFilesControl.Location.Y)

        self.moduleControl = FileControl("Select your fighter module file", "REL files|*.rel", "Module")
        self.moduleControl.Location = Point(self.pacFilesControl.Location.X, self.pacFilesControl.Location.Y + self.pacFilesControl.Height + 32)
        
        self.mainFighterGroupBox.Controls.Add(self.pacFilesControl)
        self.mainFighterGroupBox.Controls.Add(self.exConfigsControl)
        self.mainFighterGroupBox.Controls.Add(self.moduleControl)

        # Kirby hats
        self.kirbyHatGroupBox = GroupBox()
        self.kirbyHatGroupBox.AutoSize = True
        self.kirbyHatGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.kirbyHatGroupBox.Text = "Kirby Hat"
        self.kirbyHatGroupBox.Click += self.toggleGroupBox

        self.kirbyHatFilesControl = MultiFileControl("Select your Kirby hat PAC files", "PAC files|*.pac", "Kirby Hat Files")
        self.kirbyHatFilesControl.Location = Point(16,16)

        self.kirbyHatTextBox = LabeledTextBox("Kirby Hat ID", "fighter")
        self.kirbyHatTextBox.Location = Point(self.kirbyHatFilesControl.Location.X, self.kirbyHatFilesControl.Location.Y + self.kirbyHatFilesControl.Height + 32)

        self.kirbyHatGroupBox.Controls.Add(self.kirbyHatFilesControl)
        self.kirbyHatGroupBox.Controls.Add(self.kirbyHatTextBox)

        # Sound/Music
        self.soundGroupBox = GroupBox()
        self.soundGroupBox.AutoSize = True
        self.soundGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.soundGroupBox.Text = "Sound"
        self.soundGroupBox.Click += self.toggleGroupBox

        self.soundBankControl = FileControl("Select your soundbank file", "SAWND files|*.sawnd", "Soundbank")
        self.soundBankControl.Location = Point(16, 16)

        self.victoryThemeControl = FileControl("Select your victory theme file", "BRSTM files|*.brstm", "Victory\nTheme")
        self.victoryThemeControl.Location = Point(self.soundBankControl.Location.X, self.soundBankControl.Location.Y + 32)

        self.creditsThemeControl = FileControl("Select your credits theme file", "BRSTM files|*.brstm", "Credits\nTheme")
        self.creditsThemeControl.Location = Point(self.victoryThemeControl.Location.X, self.victoryThemeControl.Location.Y + 32)

        self.soundGroupBox.Controls.Add(self.soundBankControl)
        self.soundGroupBox.Controls.Add(self.victoryThemeControl)
        self.soundGroupBox.Controls.Add(self.creditsThemeControl)

        # Intro/Ending
        self.classicGroupBox = GroupBox()
        self.classicGroupBox.AutoSize = True
        self.classicGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.classicGroupBox.Text = "Classic Mode"
        self.classicGroupBox.Click += self.toggleGroupBox

        self.introControl = FileControl("Select your classic intro file", "BRRES files|*.brres", "Classic\nIntro")
        self.introControl.Location = Point(16,16)

        self.endingControl = MultiFileControl("Select your ending PAC files", "PAC files|*.pac", "Ending PAC Files", Size(100, 60))
        self.endingControl.Location = Point(self.introControl.Location.X, self.introControl.Location.Y + 32)
        
        self.endingMovieControl = FileControl("Select your ending THP file", "THP files|*.thp", "Ending\nMovie")
        self.endingMovieControl.Location = Point(self.endingControl.Location.X, self.endingControl.Location.Y + 112)

        self.classicGroupBox.Controls.Add(self.introControl)
        self.classicGroupBox.Controls.Add(self.endingControl)
        self.classicGroupBox.Controls.Add(self.endingMovieControl)

        self.fighterGroupBox.Controls.Add(self.mainFighterGroupBox)
        self.fighterGroupBox.Controls.Add(self.kirbyHatGroupBox)
        self.fighterGroupBox.Controls.Add(self.soundGroupBox)
        self.fighterGroupBox.Controls.Add(self.classicGroupBox)

        # Misc Groupbox
        self.miscGroupBox = GroupBox()
        self.miscGroupBox.AutoSize = True
        self.miscGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.miscGroupBox.Text = "Misc"
        self.miscGroupBox.Click += self.toggleGroupBox

        self.codeGroupBox = GroupBox()
        self.codeGroupBox.AutoSize = True
        self.codeGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.codeGroupBox.Text = "Code Settings"
        self.codeGroupBox.Click += self.toggleGroupBox

        self.creditsIdControl = LabeledTextBox("Credits\nTheme ID", "creditsTheme")
        self.creditsIdControl.Location = Point(4, 16)

        self.trophyIdControl = LabeledTextBox("Trophy ID")
        self.trophyIdControl.Location = Point(self.creditsIdControl.Location.X, self.creditsIdControl.Location.Y + 32)

        self.throwRelease1Control = LabeledTextBox("Throw\nRelease 1")
        self.throwRelease1Control.Location = Point(self.trophyIdControl.Location.X, self.trophyIdControl.Location.Y + 32)
        
        self.throwRelease2Control = LabeledTextBox("Throw\nRelease 2")
        self.throwRelease2Control.Location = Point(self.throwRelease1Control.Location.X, self.throwRelease1Control.Location.Y + 32)

        self.asmControl = MultiFileControl("Select your Gecko code ASM files", "ASM files|*.asm", "ASM Files")
        self.asmControl.Location = Point(self.throwRelease2Control.Location.X + 16, self.throwRelease2Control.Location.Y + 32)

        # Fighter specific codes

        # Lucario
        self.lucarioGroupBox = GroupBox()
        self.lucarioGroupBox.AutoSize = False
        self.lucarioGroupBox.Size = Size(128, 16)
        self.lucarioGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.lucarioGroupBox.Text = "Lucario"
        self.lucarioGroupBox.Location = Point(self.asmControl.Location.X - 16, self.asmControl.Location.Y + self.asmControl.Height + 32)
        self.lucarioGroupBox.Click += self.toggleGroupBox

        self.lucarioBoneControl = LabeledTextBox("Bone ID")
        self.lucarioBoneControl.Location = Point(4,16)

        self.lucarioKirbyEffectControl = LabeledTextBox("Kirby\nEffect ID")
        self.lucarioKirbyEffectControl.Location = Point(self.lucarioBoneControl.Location.X, self.lucarioBoneControl.Location.Y + 32)

        self.lucarioGroupBox.Controls.Add(self.lucarioBoneControl)
        self.lucarioGroupBox.Controls.Add(self.lucarioKirbyEffectControl)

        # Jigglypuff
        self.jigglypuffGroupBox = GroupBox()
        self.jigglypuffGroupBox.AutoSize = False
        self.jigglypuffGroupBox.Size = Size(128, 16)
        self.jigglypuffGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.jigglypuffGroupBox.Text = "JigglyPuff"
        self.jigglypuffGroupBox.Click += self.toggleGroupBox

        self.jigglypuffBoneControl = LabeledTextBox("Bone ID")
        self.jigglypuffBoneControl.Location = Point(4,16)

        self.jigglypuffEflsControl = LabeledTextBox("EFLS ID")
        self.jigglypuffEflsControl.Location = Point(self.jigglypuffBoneControl.Location.X, self.jigglypuffBoneControl.Location.Y + 32)

        jigglypuffSfxLabel = Label()
        jigglypuffSfxLabel.Height = 16
        jigglypuffSfxLabel.Text = "SFX IDs:"
        jigglypuffSfxLabel.Location = Point(self.jigglypuffEflsControl.Location.X, self.jigglypuffEflsControl.Location.Y + 32)

        self.jigglypuffGroupBox.Controls.Add(self.jigglypuffBoneControl)
        self.jigglypuffGroupBox.Controls.Add(self.jigglypuffEflsControl)
        self.jigglypuffGroupBox.Controls.Add(jigglypuffSfxLabel)

        self.jigglypuffSfxIdBox = [None] * 4
        i = 0
        while i < 4:
            y = jigglypuffSfxLabel.Location.Y + 16 if i == 0 else self.jigglypuffSfxIdBox[i-1].Location.Y + 32
            self.jigglypuffSfxIdBox[i] = TextBox()
            self.jigglypuffSfxIdBox[i].Location = Point(jigglypuffSfxLabel.Location.X + 16, y)
            
            self.jigglypuffGroupBox.Controls.Add(self.jigglypuffSfxIdBox[i])
            i += 1

        # Bowser
        self.bowserGroupBox = GroupBox()
        self.bowserGroupBox.AutoSize = False
        self.bowserGroupBox.Size = Size(128, 16)
        self.bowserGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.bowserGroupBox.Text = "Bowser"
        self.bowserGroupBox.Click += self.toggleGroupBox

        self.bowserBoneControl = LabeledTextBox("Bone ID")
        self.bowserBoneControl.Location = Point(4,16)

        self.bowserGroupBox.Controls.Add(self.bowserBoneControl)

        self.codeGroupBox.Controls.Add(self.creditsIdControl)
        self.codeGroupBox.Controls.Add(self.trophyIdControl)
        self.codeGroupBox.Controls.Add(self.throwRelease1Control)
        self.codeGroupBox.Controls.Add(self.throwRelease2Control)
        self.codeGroupBox.Controls.Add(self.asmControl)
        self.codeGroupBox.Controls.Add(self.lucarioGroupBox)
        self.codeGroupBox.Controls.Add(self.jigglypuffGroupBox)
        self.codeGroupBox.Controls.Add(self.bowserGroupBox)

        self.trophyGroupBox = GroupBox()
        self.trophyGroupBox.AutoSize = True
        self.trophyGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.trophyGroupBox.Text = "Trophy Settings"
        self.trophyGroupBox.Click += self.toggleGroupBox

        self.trophyNameControl = LabeledTextBox("Name")
        self.trophyNameControl.Location = Point(4,16)
        self.trophyNameControl.textBox.Enabled = False

        self.trophyCheckBox = CheckBox()
        self.trophyCheckBox.Text = "Include Trophy?"
        self.trophyCheckBox.Location = Point(self.trophyNameControl.Location.X + self.trophyNameControl.Width + 32, self.trophyNameControl.Location.Y)
        self.trophyCheckBox.CheckedChanged += self.trophyCheckChanged

        self.trophyDescriptionControl = LabeledTextBox("Description", multiline=True)
        self.trophyDescriptionControl.Location = Point(self.trophyNameControl.Location.X, self.trophyNameControl.Location.Y + 32)
        self.trophyDescriptionControl.textBox.Enabled = False

        self.gameIcon1Control = LabeledDropDown("Game\nIcon 1", TROPHY_GAME_ICONS)
        self.gameIcon1Control.Location = Point(self.trophyDescriptionControl.Location.X, self.trophyDescriptionControl.Location.Y + self.trophyDescriptionControl.Height)
        self.gameIcon1Control.dropDown.Enabled = False

        self.gameIcon2Control = LabeledDropDown("Game\nIcon 2", TROPHY_GAME_ICONS)
        self.gameIcon2Control.Location = Point(self.gameIcon1Control.Location.X, self.gameIcon1Control.Location.Y + 32)
        self.gameIcon2Control.dropDown.Enabled = False

        self.gameName1Control = LabeledTextBox("Game\nName 1")
        self.gameName1Control.Location = Point(self.gameIcon2Control.Location.X, self.gameIcon2Control.Location.Y + 32)
        self.gameName1Control.textBox.Enabled = False

        self.gameName2Control = LabeledTextBox("Game\nName 2")
        self.gameName2Control.Location = Point(self.gameName1Control.Location.X, self.gameName1Control.Location.Y + 32)
        self.gameName2Control.textBox.Enabled = False

        self.trophySeriesControl = LabeledDropDown("Series", TROPHY_SERIES)
        self.trophySeriesControl.Location = Point(self.gameName2Control.Location.X, self.gameName2Control.Location.Y + 32)
        self.trophySeriesControl.dropDown.Enabled = False

        self.trophyModelControl = FileControl("Select your trophy brres file", "BRRES files|*.brres", "Model")
        self.trophyModelControl.Location = Point(self.trophySeriesControl.Location.X, self.trophySeriesControl.Location.Y + 32)
        self.trophyModelControl.Enabled = False

        self.trophyImageControl = ImageControl([ImageObject("Thumbnail",Size(56,48)), ImageObject("HD Thumbnail",Size(56,48))])
        self.trophyImageControl.Location = Point(self.trophyModelControl.Location.X, self.trophyModelControl.Location.Y + 32)
        self.trophyImageControl.Enabled = False

        self.trophyGroupBox.Controls.Add(self.trophyNameControl)
        self.trophyGroupBox.Controls.Add(self.trophyCheckBox)
        self.trophyGroupBox.Controls.Add(self.trophyDescriptionControl)
        self.trophyGroupBox.Controls.Add(self.gameIcon1Control)
        self.trophyGroupBox.Controls.Add(self.gameIcon2Control)
        self.trophyGroupBox.Controls.Add(self.gameName1Control)
        self.trophyGroupBox.Controls.Add(self.gameName2Control)
        self.trophyGroupBox.Controls.Add(self.trophySeriesControl)
        self.trophyGroupBox.Controls.Add(self.trophyModelControl)
        self.trophyGroupBox.Controls.Add(self.trophyImageControl)

        self.miscGroupBox.Controls.Add(self.codeGroupBox)
        self.miscGroupBox.Controls.Add(self.trophyGroupBox)

        self.openButton = Button()
        self.openButton.Text = "Open"
        self.openButton.Click += self.openButtonPressed

        self.saveButton = Button()
        self.saveButton.Text = "Save"
        self.saveButton.Click += self.saveButtonPressed

        self.saveAsButton = Button()
        self.saveAsButton.Text = "Save As..."
        self.saveAsButton.Click += self.saveAsButtonPressed

        self.cancelButton = Button()
        self.cancelButton.Text = "Cancel"
        self.cancelButton.Click += self.cancelButtonPressed

        self.Controls.Add(self.cosmeticsGroupBox)
        self.Controls.Add(self.readmeGroupBox)
        self.Controls.Add(self.fighterGroupBox)
        self.Controls.Add(self.miscGroupBox)
        self.Controls.Add(self.openButton)
        self.Controls.Add(self.cancelButton)
        self.Controls.Add(self.saveButton)
        self.Controls.Add(self.saveAsButton)
        
        self.recalculateGroupLocations()
        self.Load += self.openCharacterPackage
        
        #region TOOLTIPS

        toolTip = ToolTip()
        toolTip.SetToolTip(cspCostumeLabel, "The color smash groups for your character's stock icons and CSPs.")
        toolTip.SetToolTip(cspLabel, "The different colors within the selected color smash group.")
        toolTip.SetToolTip(cspPictureBoxLabel, "The portrait for your character as it appears on the character selection screen.")
        toolTip.SetToolTip(cspHdPictureBoxLabel, "The HD CSP.")
        toolTip.SetToolTip(stockPictureBoxLabel, "The stock icons for your character.")
        toolTip.SetToolTip(stockHdPictureBoxLabel, "The HD stock icons.")
        i = 0
        while i < len(self.bpTabControl.TabPages):
            toolTip.SetToolTip(bpListBoxLabels[i], "List of BPs in the package.")
            toolTip.SetToolTip(bpPictureBoxLabels[i], "The portrait that appears in battle.")
            toolTip.SetToolTip(bpHdPictureBoxLabels[i], "The HD BP.")
            toolTip.SetToolTip(bpNameLabels[i], "The name that appears beneath BPs in battle.")
            toolTip.SetToolTip(bpNameHdLabels[i], "The HD BP name.")
            i += 1
        i = 0
        while i < len(self.cssTabControl.tabControl.TabPages):
            toolTip.SetToolTip(self.cssTabControl.controls[i].label[0], "The icon that appears on the character select screen.")
            toolTip.SetToolTip(self.cssTabControl.controls[i].label[1], "The HD CSS icon.")
            toolTip.SetToolTip(self.cssTabControl.controls[i].label[2], "The name that appears on icons on the character select screen.")
            toolTip.SetToolTip(self.cssTabControl.controls[i].label[3], "The HD CSS icon name.")
            i += 1
        i = 0
        while i < len(self.replayTabControl.tabControl.TabPages):
            toolTip.SetToolTip(self.replayTabControl.controls[i].label[0], "The icon that appears in the replay icon.")
            toolTip.SetToolTip(self.replayTabControl.controls[i].label[1], "The HD replay icon.")
            i += 1
        i = 0
        while i < len(self.portraitNameTabControl.tabControl.TabPages):
            toolTip.SetToolTip(self.portraitNameTabControl.controls[i].label[0], "The name that appears on the portrait on the character select screen.")
            toolTip.SetToolTip(self.portraitNameTabControl.controls[i].label[1], "The HD portrait name.")
            i += 1
        toolTip.SetToolTip(self.franchiseIconImageControl.label[0], "Franchise icon with a black background.")
        toolTip.SetToolTip(self.franchiseIconImageControl.label[1], "Franchise icon with a transparent background.")
        toolTip.SetToolTip(self.franchiseModelControl.textBox.label, "Franchise icon model for results screen.")
        toolTip.SetToolTip(self.readmeGroupBox, "Text of README file if you wish to include one in your character package.")
        toolTip.SetToolTip(self.pacFilesControl.label, "Fighter PAC files.")
        toolTip.SetToolTip(self.exConfigsControl.label, "Fighter Ex config files.")
        toolTip.SetToolTip(self.moduleControl.textBox.label, "Fighter module file.")
        toolTip.SetToolTip(self.kirbyHatFilesControl.label, "Fighter Kirby hat files, if included.")
        toolTip.SetToolTip(self.kirbyHatTextBox.label, "The ID of the fighter (in hex or decimal format) whose Kirby hat the new hat is based on.")
        toolTip.SetToolTip(self.soundBankControl.textBox.label, "The soundbank file for the fighter.")
        toolTip.SetToolTip(self.victoryThemeControl.textBox.label, "The victory theme to use for the fighter.")
        toolTip.SetToolTip(self.creditsThemeControl.textBox.label, "The classic mode credits theme to use for the fighter.")
        toolTip.SetToolTip(self.introControl.textBox.label, "The .brres file for the character's classic mode intro.")
        toolTip.SetToolTip(self.endingControl.label, "The .pac files for the character's classic mode ending.")
        toolTip.SetToolTip(self.endingMovieControl.textBox.label, "The .thp file for the character's classic mode ending movie.")
        toolTip.SetToolTip(self.creditsIdControl.label, "The song ID (in hex or decimal format) to use for your character's credits theme. Only set if using a vanilla theme.")
        toolTip.SetToolTip(self.trophyIdControl.label, "The trophy ID (in hex or decimal format) to use for your character's trophy. Only set if using a vanilla trophy.")
        toolTip.SetToolTip(self.throwRelease1Control.label, "The first value for your fighter's throw release point.")
        toolTip.SetToolTip(self.throwRelease2Control.label, "The second value for your fighter's throw release point.")
        toolTip.SetToolTip(self.asmControl.label, "Any ASM files with Gecko codes to include with your fighter.")
        toolTip.SetToolTip(self.lucarioGroupBox, "Values for Lucario-specific Gecko codes used in some builds. Only set for Lucario clones.")
        toolTip.SetToolTip(self.lucarioBoneControl.label, "The bone ID to use for the code 'Lucario Clone Aura Sphere Bone ID Fix'.")
        toolTip.SetToolTip(self.lucarioKirbyEffectControl.label, "The GFX ID to use for the code 'Kirby Lucario Clone Aura Sphere GFX Fix'.")
        toolTip.SetToolTip(self.jigglypuffGroupBox, "Values for Jigglypuff-specific Gecko codes used in some builds. Only set for Jigglypuff clones.")
        toolTip.SetToolTip(self.jigglypuffBoneControl.label, "The bone ID to use for the code 'Jigglypuff Clone Rollout Bone Fix'.")
        toolTip.SetToolTip(self.jigglypuffEflsControl.label, "The EFLS ID to use for the code 'Jigglypuff Clone Rollout Max Charge GFX Fix'.")
        toolTip.SetToolTip(jigglypuffSfxLabel, "The SFX IDs to use for the code 'Jigglypuff Clone Rollout SFX Fix', in order as they would appear in the code.")
        toolTip.SetToolTip(self.bowserGroupBox, "Values for Bowser-specific Gecko codes used in some builds. Only set for Bowser clones.")
        toolTip.SetToolTip(self.bowserBoneControl.label, "The bone ID used for the code 'Bowser Clone Fire Breath Bone Fix'.")
        toolTip.SetToolTip(self.trophyNameControl.label, "The name to display when viewing the trophy.")
        toolTip.SetToolTip(self.trophyCheckBox, "Check if you would like to include a trophy with the character package. Leave unchecked otherwise.")
        toolTip.SetToolTip(self.trophyDescriptionControl.label, "The description to display when viewing the trophy.")
        toolTip.SetToolTip(self.gameIcon1Control.label, "The first console the character appeared on.")
        toolTip.SetToolTip(self.gameIcon2Control.label, "The last console the character appeared on.")
        toolTip.SetToolTip(self.gameName1Control.label, "The first game the character appeared in.")
        toolTip.SetToolTip(self.gameName2Control.label, "The last game the character appeared in.")
        toolTip.SetToolTip(self.trophySeriesControl.label, "The series the character comes from.")
        toolTip.SetToolTip(self.trophyModelControl.textBox.label, "The .brres file containing the trophy's model.")
        toolTip.SetToolTip(self.trophyImageControl.label[0], "The thumbnail for the trophy that appears in the gallery.")
        toolTip.SetToolTip(self.trophyImageControl.label[1], "The HD trophy thumbnail.")

        #endregion TOOLTIPS

    def createPackage(self, path):
        if Directory.Exists(PACK_PATH):
            Directory.Delete(PACK_PATH, 1)
        if len(self.costumeGroups) > 0:
            i = 1
            for costumeGroup in self.costumeGroups:
                j = 1
                for costume in costumeGroup.costumeObjects:
                    if costume.csp:
                        copyRenameFile(costume.csp, addLeadingZeros(str(j), 4) + '.png', PACK_PATH + '\\CSPs\\' + addLeadingZeros(str(i), 4))
                    if costume.cspHd:
                        copyRenameFile(costume.cspHd, addLeadingZeros(str(j), 4) + '.png', PACK_PATH + '\\CSPs\\' + addLeadingZeros(str(i), 4) + '\\HD')
                    if costume.stock:
                        copyRenameFile(costume.stock, addLeadingZeros(str(j), 4) + '.png', PACK_PATH + '\\StockIcons\\' + addLeadingZeros(str(i), 4))
                    if costume.stockHd:
                        copyRenameFile(costume.stockHd, addLeadingZeros(str(j), 4) + '.png', PACK_PATH + '\\StockIcons\\' + addLeadingZeros(str(i), 4) + '\\HD')
                    j += 1
                i += 1
        if len(self.bpTabControl.TabPages) > 0:
            i = 0
            while i < len(self.bpTabControl.TabPages):
                j = 1
                for bpObject in self.bps[i]:
                    if bpObject.bp:
                        copyRenameFile(bpObject.bp, addLeadingZeros(str(j), 4) + '.png', PACK_PATH + '\\BPs\\' + self.bpTabControl.TabPages[i].Text)
                    if bpObject.bpHd:
                        copyRenameFile(bpObject.bpHd, addLeadingZeros(str(j), 4) + '.png', PACK_PATH + '\\BPs\\' + self.bpTabControl.TabPages[i].Text + '\\HD')
                    j += 1
                if self.bpNameImage[i]:
                    copyRenameFile(self.bpNameImage[i], 'Name.png', PACK_PATH + '\\BPs\\' + self.bpTabControl.TabPages[i].Text + '\\Name')
                if self.bpNameHdImage[i]:
                    copyRenameFile(self.bpNameHdImage[i], 'Name.png', PACK_PATH + '\\BPs\\' + self.bpTabControl.TabPages[i].Text + '\\Name\\HD')
                i += 1
        if len(self.cssTabControl.tabControl.TabPages) > 0:
            i = 0
            while i < len(self.cssTabControl.tabControl.TabPages):
                if len(self.cssTabControl.controls[i].Images) > 0 and self.cssTabControl.controls[i].Images[0]:
                    copyRenameFile(self.cssTabControl.controls[i].Images[0], 'Icon.png', PACK_PATH + '\\CSSIcon\\' + self.cssTabControl.tabControl.TabPages[i].Text)
                if len(self.cssTabControl.controls[i].Images) > 1 and self.cssTabControl.controls[i].Images[1]:
                    copyRenameFile(self.cssTabControl.controls[i].Images[1], 'Icon.png', PACK_PATH + '\\CSSIcon\\' + self.cssTabControl.tabControl.TabPages[i].Text + '\\HD')
                if len(self.cssTabControl.controls[i].Images) > 2 and self.cssTabControl.controls[i].Images[2]:
                    copyRenameFile(self.cssTabControl.controls[i].Images[2], 'Name.png', PACK_PATH + '\\CSSIcon\\' + self.cssTabControl.tabControl.TabPages[i].Text + '\\Name')
                if len(self.cssTabControl.controls[i].Images) > 3 and self.cssTabControl.controls[i].Images[3]:
                    copyRenameFile(self.cssTabControl.controls[i].Images[3], 'Name.png', PACK_PATH + '\\CSSIcon\\' + self.cssTabControl.tabControl.TabPages[i].Text + '\\Name\\HD')
                i += 1
        if len(self.replayTabControl.tabControl.TabPages) > 0:
            i = 0
            while i < len(self.replayTabControl.tabControl.TabPages):
                if len(self.replayTabControl.controls[i].Images) > 0 and self.replayTabControl.controls[i].Images[0]:
                    copyRenameFile(self.replayTabControl.controls[i].Images[0], 'Icon.png', PACK_PATH + '\\ReplayIcon\\' + self.replayTabControl.tabControl.TabPages[i].Text)
                if len(self.replayTabControl.controls[i].Images) > 1 and self.replayTabControl.controls[i].Images[1]:
                    copyRenameFile(self.replayTabControl.controls[i].Images[1], 'Icon.png', PACK_PATH + '\\ReplayIcon\\' + self.replayTabControl.tabControl.TabPages[i].Text + '\\HD')
                i += 1
        if len(self.portraitNameTabControl.tabControl.TabPages) > 0:
            i = 0
            while i < len(self.portraitNameTabControl.tabControl.TabPages):
                if len(self.portraitNameTabControl.controls[i].Images) > 0 and self.portraitNameTabControl.controls[i].Images[0]:
                    copyRenameFile(self.portraitNameTabControl.controls[i].Images[0], 'Name.png', PACK_PATH + '\\PortraitName\\' + self.portraitNameTabControl.tabControl.TabPages[i].Text)
                if len(self.portraitNameTabControl.controls[i].Images) > 1 and self.portraitNameTabControl.controls[i].Images[1]:
                    copyRenameFile(self.portraitNameTabControl.controls[i].Images[1], 'Name.png', PACK_PATH + '\\PortraitName\\' + self.portraitNameTabControl.tabControl.TabPages[i].Text + '\\HD')
                i += 1
        if self.franchiseIconImageControl.Images[0]:
            copyRenameFile(self.franchiseIconImageControl.Images[0], 'Icon.png', PACK_PATH + '\\FranchiseIcons\\Black')
        if self.franchiseIconImageControl.Images[1]:
            copyRenameFile(self.franchiseIconImageControl.Images[1], 'Icon.png', PACK_PATH + '\\FranchiseIcons\\Transparent')
        if self.franchiseModelControl.textBox.textBox.Text:
            copyRenameFile(self.franchiseModelControl.textBox.textBox.Text, 'Model.mdl0', PACK_PATH + '\\FranchiseIcons\\Model')
        for file in self.pacFilesControl.files:
            copyFile(file.FullName, PACK_PATH + '\\Fighter')
        for file in self.exConfigsControl.files:
            copyFile(file.FullName, PACK_PATH + '\\ExConfigs')
        if self.moduleControl.textBox.textBox.Text:
            copyFile(self.moduleControl.textBox.textBox.Text, PACK_PATH + '\\Module')
        for file in self.kirbyHatFilesControl.files:
            copyFile(file.FullName, PACK_PATH + '\\KirbyHats')
        if self.kirbyHatTextBox.textBox.Text:
            Directory.CreateDirectory(PACK_PATH + '\\KirbyHats')
            File.WriteAllText(PACK_PATH + '\\KirbyHats\\FighterID.txt', self.kirbyHatTextBox.textBox.Text)
        if self.soundBankControl.textBox.textBox.Text:
            copyFile(self.soundBankControl.textBox.textBox.Text, PACK_PATH + '\\Soundbank')
        if self.victoryThemeControl.textBox.textBox.Text:
            copyFile(self.victoryThemeControl.textBox.textBox.Text, PACK_PATH + '\\VictoryTheme')
        if self.creditsThemeControl.textBox.textBox.Text:
            copyFile(self.creditsThemeControl.textBox.textBox.Text, PACK_PATH + '\\CreditsTheme')
        if self.introControl.textBox.textBox.Text:
            copyFile(self.introControl.textBox.textBox.Text, PACK_PATH + '\\ClassicIntro')
        for file in self.endingControl.files:
            copyFile(file.FullName, PACK_PATH + '\\Ending')
        if self.endingMovieControl.textBox.textBox.Text:
            copyFile(self.endingMovieControl.textBox.textBox.Text, PACK_PATH + '\\Ending')
        for file in self.asmControl.files:
            copyFile(file.FullName, PACK_PATH + '\\Codes')
        if self.readmeControl.textBox.Text:
            Directory.CreateDirectory(PACK_PATH)
            File.WriteAllText(PACK_PATH + '\\README.txt', self.readmeControl.textBox.Text)
        # Fighter settings
        fighterSettings = FighterSettings()
        if self.creditsIdControl.textBox.Text:
            fighterSettings.creditsThemeId = self.creditsIdControl.textBox.Text
        if self.trophyIdControl.textBox.Text:
            fighterSettings.trophyId = self.trophyIdControl.textBox.Text
        if self.throwRelease1Control.textBox.Text and self.throwRelease2Control.textBox.Text:
            fighterSettings.throwReleasePoint = self.throwRelease1Control.textBox.Text + ',' + self.throwRelease2Control.textBox.Text
        # Lucario
        if self.lucarioBoneControl.textBox.Text:
            fighterSettings.lucarioBoneId = self.lucarioBoneControl.textBox.Text
        if self.lucarioKirbyEffectControl.textBox.Text:
            fighterSettings.lucarioKirbyEffectId = self.lucarioKirbyEffectControl.textBox.Text
        # Jigglypuff
        if self.jigglypuffBoneControl.textBox.Text:
            fighterSettings.jigglypuffBoneId = self.jigglypuffBoneControl.textBox.Text
        if self.jigglypuffEflsControl.textBox.Text:
            fighterSettings.jigglypuffEFLSId = self.jigglypuffEflsControl.textBox.Text
        i = 0
        jigglypuffSfxIds = ""
        while i < len(self.jigglypuffSfxIdBox):
            if self.jigglypuffSfxIdBox[i].Text:
                jigglypuffSfxIds += self.jigglypuffSfxIdBox[i].Text + ("," if i < 3 else "")
            else:
                jigglypuffSfxIds = ""
                break
            i += 1
        if jigglypuffSfxIds:
            fighterSettings.jigglypuffSfxIds = jigglypuffSfxIds
        # Bowser
        if self.bowserBoneControl.textBox.Text:
            fighterSettings.bowserBoneId = self.bowserBoneControl.textBox.Text
        attrs = vars(fighterSettings)
        writeString = '\n'.join("%s = %s" % item for item in attrs.items())
        if writeString:
            File.WriteAllText(PACK_PATH + '\\FighterSettings.txt', writeString)
        # Trophy
        if self.trophyCheckBox.Checked:
            Directory.CreateDirectory(PACK_PATH + '\\Trophy')
            trophySettings = TrophySettings()
            trophySettings.trophyName = self.trophyNameControl.textBox.Text
            trophySettings.description = self.trophyDescriptionControl.textBox.Text.replace('\r\n', '<br/>')
            if self.gameIcon1Control.dropDown.SelectedItem:
                trophySettings.gameIcon1 = str(TROPHY_GAME_ICONS[self.gameIcon1Control.dropDown.SelectedItem])
            else:
                trophySettings.gameIcon1 = str(0)
            if self.gameIcon2Control.dropDown.SelectedItem:
                trophySettings.gameIcon2 = str(TROPHY_GAME_ICONS[self.gameIcon2Control.dropDown.SelectedItem])
            else:
                trophySettings.gameIcon2 = str(0)
            trophySettings.gameName1 = self.gameName1Control.textBox.Text
            if self.gameName2Control.textBox.Text:
                trophySettings.gameName2 = self.gameName2Control.textBox.Text
            if self.trophySeriesControl.dropDown.SelectedItem:
                trophySettings.seriesIndex = str(TROPHY_SERIES[self.trophySeriesControl.dropDown.SelectedItem])
            else:
                trophySettings.seriesIndex = str(19)
            attrs = vars(trophySettings)
            writeString = '\n'.join("%s = %s" % item for item in attrs.items())
            if writeString:
                File.WriteAllText(PACK_PATH + '\\Trophy\\TrophySettings.txt', writeString)
            if self.trophyModelControl.textBox.textBox.Text:
                copyFile(self.trophyModelControl.textBox.textBox.Text, PACK_PATH + '\\Trophy')
            if self.trophyImageControl.Images[0]:
                copyRenameFile(self.trophyImageControl.Images[0], 'TrophyIcon.png', PACK_PATH + '\\Trophy')
            if self.trophyImageControl.Images[1]:
                copyRenameFile(self.trophyImageControl.Images[1], 'TrophyIcon.png', PACK_PATH + '\\Trophy\\HD')
        # Create zip
        if File.Exists(path):
            File.Delete(path)
        ZipFile.CreateFromDirectory(PACK_PATH, path)
        if Directory.Exists(PACK_PATH):
            Directory.Delete(PACK_PATH, 1)
        BrawlAPI.ShowMessage("Character package created at " + path, "Success")

    def saveButtonPressed(self, sender, args):
        self.createPackage(self.zipFile)

    def saveAsButtonPressed(self, sender, args):
        saveDialog = SaveFileDialog()
        saveDialog.Filter = "ZIP File|*.zip"
        saveDialog.Title = "Save character package"
        result = saveDialog.ShowDialog()
        if result == DialogResult.OK and saveDialog.FileName:
            self.createPackage(saveDialog.FileName)
            saveDialog.Dispose()

    def cancelButtonPressed(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Close()

    def openCharacterPackage(self, sender, args):
        if self.zipFile:
            file = self.zipFile
            if Directory.Exists(TEMP_PATH):
                Directory.Delete(TEMP_PATH, 1)
            unzipFile(file)
            if Directory.Exists(TEMP_PATH):
                # CSPs
                if Directory.Exists(TEMP_PATH + '\\CSPs'):
                    i = 0
                    for directory in Directory.GetDirectories(TEMP_PATH + '\\CSPs'):
                        group = self.addCostumeGroup(i)
                        images = Directory.GetFiles(directory, "*.png")
                        self.updateImages("", "csp", images, group)
                        if Directory.Exists(directory + '\\HD'):
                            hdImages = Directory.GetFiles(directory + '\\HD', "*.png")
                            self.updateImages("", "cspHd", hdImages, group)
                        i += 1
                # Stocks
                if Directory.Exists(TEMP_PATH + '\\StockIcons'):
                    i = 0
                    for directory in Directory.GetDirectories(TEMP_PATH + '\\StockIcons'):
                        group = self.addCostumeGroup(i)
                        images = Directory.GetFiles(directory, "*.png")
                        self.updateImages("", "stock", images, group)
                        if Directory.Exists(directory + '\\HD'):
                            hdImages = Directory.GetFiles(directory + '\\HD', "*.png")
                            self.updateImages("", "stockHd", hdImages, group)
                        i += 1
                # BPs
                if Directory.Exists(TEMP_PATH + '\\BPs'):
                    for directory in Directory.GetDirectories(TEMP_PATH + '\\BPs'):
                        name = DirectoryInfo(directory).Name
                        index = self.bpTabControl.TabPages.IndexOfKey(name)
                        if index > -1:
                            images = Directory.GetFiles(directory, "*.png")
                            self.updateBpImages("", "bp", images, index)
                            if Directory.Exists(directory + '\\HD'):
                                hdImages = Directory.GetFiles(directory + '\\HD', "*.png")
                                self.updateBpImages("", "bpHd", hdImages, index)
                            if Directory.Exists(directory + '\\Name'):
                                nameImage = Directory.GetFiles(directory + '\\Name', "*.png")
                                if nameImage and len(nameImage) > 0:
                                    self.bpNameImage[index] = nameImage[0]
                                    self.bpNamePictureBoxes[index].Image = createBitmap(self.bpNameImage[index])
                                if Directory.Exists(directory + '\\Name\\HD'):
                                    nameHdImage = Directory.GetFiles(directory + '\\Name\\HD', "*.png")
                                    if nameHdImage and len(nameHdImage) > 0:
                                        self.bpNameHdImage[index] = nameHdImage[0]
                                        self.bpNameHdPictureBoxes[index].Image = createBitmap(self.bpNameHdImage[index])
                # CSS Icons
                if Directory.Exists(TEMP_PATH + '\\CSSIcon'):
                    for directory in Directory.GetDirectories(TEMP_PATH + '\\CSSIcon'):
                        name = DirectoryInfo(directory).Name
                        index = self.cssTabControl.tabControl.TabPages.IndexOfKey(name)
                        if index > -1:
                            images = Directory.GetFiles(directory, "*.png")
                            if images and len(images) > 0:
                                self.cssTabControl.controls[index].Images[0] = images[0]
                                self.cssTabControl.controls[index].pictureBox[0].Image = createBitmap(images[0])
                            if Directory.Exists(directory + '\\HD'):
                                hdImages = Directory.GetFiles(directory + '\\HD', "*.png")
                                if hdImages and len(hdImages) > 0:
                                    self.cssTabControl.controls[index].Images[1] = hdImages[0]
                                    self.cssTabControl.controls[index].pictureBox[1].Image = createBitmap(hdImages[0])
                            if Directory.Exists(directory + '\\Name'):
                                nameImages = Directory.GetFiles(directory + '\\Name', "*.png")
                                if nameImages and len(nameImages) > 0:
                                    self.cssTabControl.controls[index].Images[2] = nameImages[0]
                                    self.cssTabControl.controls[index].pictureBox[2].Image = createBitmap(nameImages[0])
                                if Directory.Exists(directory + '\\Name\\HD'):
                                    nameHdImages = Directory.GetFiles(directory + '\\Name\\HD', "*.png")
                                    if nameHdImages and len(nameHdImages) > 0:
                                        self.cssTabControl.controls[index].Images[3] = nameHdImages[0]
                                        self.cssTabControl.controls[index].pictureBox[3].Image = createBitmap(nameHdImages[0])
                # Replay Icons
                if Directory.Exists(TEMP_PATH + '\\ReplayIcon'):
                    # To support legacy character packages, first check the root folder for replay icon
                    index = self.replayTabControl.tabControl.TabPages.IndexOfKey("P+")
                    if index > -1:
                        image = Directory.GetFiles(TEMP_PATH + '\\ReplayIcon', "*.png")
                        if image and len(image) > 0:
                            self.replayTabControl.controls[index].Images[0] = image[0]
                            self.replayTabControl.controls[index].pictureBox[0].Image = createBitmap(image[0])
                        if Directory.Exists(TEMP_PATH + '\\ReplayIcon\\HD'):
                            hdImage = Directory.GetFiles(TEMP_PATH + '\\ReplayIcon\\HD', "*.png")
                            if hdImage and len(hdImage) > 0:
                                self.replayTabControl.controls[index].Images[1] = hdImage[0]
                                self.replayTabControl.controls[index].pictureBox[1].Image = createBitmap(hdImage[0])
                        # Modern implementation
                        for directory in Directory.GetDirectories(TEMP_PATH + '\\ReplayIcon'):
                            name = DirectoryInfo(directory).Name
                            index = self.replayTabControl.tabControl.TabPages.IndexOfKey(name)
                            if index > -1:
                                image = Directory.GetFiles(directory, "*.png")
                                if image and len(image) > 0:
                                    self.replayTabControl.controls[index].Images[0] = image[0]
                                    self.replayTabControl.controls[index].pictureBox[0].Image = createBitmap(image[0])
                                if Directory.Exists(directory + '\\HD'):
                                    hdImage = Directory.GetFiles(directory + '\\HD', "*.png")
                                    if hdImage and len(hdImage) > 0:
                                        self.replayTabControl.controls[index].Images[1] = hdImage[0]
                                        self.replayTabControl.controls[index].pictureBox[1].Image = createBitmap(hdImage[0])
                # Portrait Name
                if Directory.Exists(TEMP_PATH + '\\PortraitName'):
                    for directory in Directory.GetDirectories(TEMP_PATH + '\\PortraitName'):
                        name = DirectoryInfo(directory).Name
                        index = self.portraitNameTabControl.tabControl.TabPages.IndexOfKey(name)
                        if index > -1:
                            image = Directory.GetFiles(directory, "*.png")
                            if image and len(image) > 0:
                                self.portraitNameTabControl.controls[index].Images[0] = image[0]
                                self.portraitNameTabControl.controls[index].pictureBox[0].Image = createBitmap(image[0])
                            if Directory.Exists(directory + '\\HD'):
                                hdImage = Directory.GetFiles(directory + '\\HD', "*.png")
                                if hdImage and len(hdImage) > 0:
                                    self.portraitNameTabControl.controls[index].Images[1] = hdImage[0]
                                    self.portraitNameTabControl.controls[index].pictureBox[1].Image = createBitmap(hdImage[0])
                # Franchise Icon
                if Directory.Exists(TEMP_PATH + '\\FranchiseIcons'):
                    for directory in Directory.GetDirectories(TEMP_PATH + '\\FranchiseIcons'):
                        name = DirectoryInfo(directory).Name
                        index = -1
                        if name == "Black":
                            index = 0
                        elif name == "Transparent":
                            index = 1
                        if index > -1:
                            image = Directory.GetFiles(directory, "*.png")
                            if image and len(image) > 0:
                                self.franchiseIconImageControl.Images[index] = image[0]
                                self.franchiseIconImageControl.pictureBox[index].Image = createBitmap(image[0])
                        if name == "Model":
                            file = Directory.GetFiles(directory, "*.mdl0")
                            if file and len(file) > 0:
                                self.franchiseModelControl.textBox.textBox.Text = file[0]
                if File.Exists(TEMP_PATH + '\\README.txt'):
                    self.readmeControl.textBox.Text = File.ReadAllText(TEMP_PATH + '\\README.txt')
                # Fighter
                if Directory.Exists(TEMP_PATH + '\\Fighter'):
                    self.pacFilesControl.files.DataSource = getFileInfos(Directory.GetFiles(TEMP_PATH + '\\Fighter', "*.pac"))
                if Directory.Exists(TEMP_PATH + '\\ExConfigs'):
                    self.exConfigsControl.files.DataSource = getFileInfos(Directory.GetFiles(TEMP_PATH + '\\ExConfigs', "*.dat"))
                if Directory.Exists(TEMP_PATH + '\\Module'):
                    file = Directory.GetFiles(TEMP_PATH + '\\Module', "*.rel")
                    if file and len(file) > 0:
                        self.moduleControl.textBox.textBox.Text = file[0]
                if Directory.Exists(TEMP_PATH + '\\KirbyHats'):
                    self.kirbyHatFilesControl.files.DataSource = getFileInfos(Directory.GetFiles(TEMP_PATH + '\\KirbyHats', "*.pac"))
                    if File.Exists(TEMP_PATH + '\\KirbyHats\\FighterID.txt'):
                        self.kirbyHatTextBox.textBox.Text = File.ReadAllText(TEMP_PATH + '\\KirbyHats\\FighterID.txt')
                if Directory.Exists(TEMP_PATH + '\\Soundbank'):
                    file = Directory.GetFiles(TEMP_PATH + '\\Soundbank')
                    if file and len(file) > 0:
                        self.soundBankControl.textBox.textBox.Text = file[0]
                if Directory.Exists(TEMP_PATH + '\\Soundbank'):
                    file = Directory.GetFiles(TEMP_PATH + '\\Soundbank', "*.sawnd")
                    if file and len(file) > 0:
                        self.soundBankControl.textBox.textBox.Text = file[0]
                if Directory.Exists(TEMP_PATH + '\\VictoryTheme'):
                    file = Directory.GetFiles(TEMP_PATH + '\\VictoryTheme', "*.brstm")
                    if file and len(file) > 0:
                        self.victoryThemeControl.textBox.textBox.Text = file[0]
                if Directory.Exists(TEMP_PATH + '\\CreditsTheme'):
                    file = Directory.GetFiles(TEMP_PATH + '\\CreditsTheme', "*.brstm")
                    if file and len(file) > 0:
                        self.creditsThemeControl.textBox.textBox.Text = file[0]
                if Directory.Exists(TEMP_PATH + '\\ClassicIntro'):
                    file = Directory.GetFiles(TEMP_PATH + '\\ClassicIntro', "*.brres")
                    if file and len(file) > 0:
                        self.introControl.textBox.textBox.Text = file[0]
                if Directory.Exists(TEMP_PATH + '\\Ending'):
                    self.endingControl.files.DataSource = getFileInfos(Directory.GetFiles(TEMP_PATH + '\\Ending', "*.pac"))
                    file = Directory.GetFiles(TEMP_PATH + '\\Ending', "*.thp")
                    if file and len(file) > 0:
                        self.endingMovieControl.textBox.textBox.Text = file[0]
                # Fighter settings
                fighterSettings = getFighterSettings()
                if fighterSettings:
                    self.creditsIdControl.textBox.Text = fighterSettings.creditsThemeId
                    self.trophyIdControl.textBox.Text = fighterSettings.trophyId
                    if len(fighterSettings.throwReleasePoint) == 2:
                        self.throwRelease1Control.textBox.Text = fighterSettings.throwReleasePoint[0]
                        self.throwRelease2Control.textBox.Text = fighterSettings.throwReleasePoint[1]
                    self.lucarioBoneControl.textBox.Text = fighterSettings.lucarioBoneId
                    self.lucarioKirbyEffectControl.textBox.Text = fighterSettings.lucarioKirbyEffectId
                    self.jigglypuffBoneControl.textBox.Text = fighterSettings.jigglypuffBoneId
                    self.jigglypuffEflsControl.textBox.Text = fighterSettings.jigglypuffEFLSId
                    if len(fighterSettings.jigglypuffSfxIds) == len(self.jigglypuffSfxIdBox):
                        i = 0
                        while i < len(self.jigglypuffSfxIdBox):
                            self.jigglypuffSfxIdBox[i].Text = fighterSettings.jigglypuffSfxIds[i]
                            i += 1
                    self.bowserBoneControl.textBox.Text = fighterSettings.bowserBoneId
                    if Directory.Exists(TEMP_PATH + '\\Codes'):
                        self.asmControl.files.DataSource = getFileInfos(Directory.GetFiles(TEMP_PATH + '\\Codes', "*.asm"))
                # Trophy Settings
                if Directory.Exists(TEMP_PATH + '\\Trophy'):
                    trophySettings = getTrophySettings()
                    if trophySettings:
                        self.trophyCheckBox.Checked = True
                        self.trophyNameControl.textBox.Text = trophySettings.trophyName
                        self.trophyDescriptionControl.textBox.Text = trophySettings.description.replace('<br/>', '\r\n')
                        if trophySettings.gameIcon1:
                            selectItemByValue(self.gameIcon1Control.dropDown, TROPHY_GAME_ICONS, int(trophySettings.gameIcon1))
                        if trophySettings.gameIcon2:
                            selectItemByValue(self.gameIcon2Control.dropDown, TROPHY_GAME_ICONS, int(trophySettings.gameIcon2))
                        self.gameName1Control.textBox.Text = trophySettings.gameName1
                        self.gameName2Control.textBox.Text = trophySettings.gameName2
                        if trophySettings.seriesIndex:
                            selectItemByValue(self.trophySeriesControl.dropDown, TROPHY_SERIES, int(trophySettings.seriesIndex))
                        file = Directory.GetFiles(TEMP_PATH + '\\Trophy', "*.brres")
                        if file and len(file) > 0:
                            self.trophyModelControl.textBox.textBox.Text = file[0]
                        image = Directory.GetFiles(TEMP_PATH + '\\Trophy', "*.png")
                        if image and len(image) > 0:
                            self.trophyImageControl.Images[0] = image[0]
                            self.trophyImageControl.pictureBox[0].Image = createBitmap(image[0])
                        if Directory.Exists(TEMP_PATH + '\\Trophy\\HD'):
                            image = Directory.GetFiles(TEMP_PATH + '\\Trophy\\HD', "*.png")
                            if image and len(image) > 0:
                                self.trophyImageControl.Images[1] = image[0]
                                self.trophyImageControl.pictureBox[1].Image = createBitmap(image[0])

    def openButtonPressed(self, sender, args):
        file = BrawlAPI.OpenFileDialog("Select a character package .zip file", "ZIP files|*.zip")
        if file:
            self.zipFile = file
            self.DialogResult = DialogResult.Retry
            self.Close()

    def trophyCheckChanged(self, sender, args):
        self.trophyNameControl.textBox.Enabled = sender.Checked
        self.trophyDescriptionControl.textBox.Enabled = sender.Checked
        self.gameIcon1Control.dropDown.Enabled = sender.Checked
        self.gameIcon2Control.dropDown.Enabled = sender.Checked
        self.gameName1Control.textBox.Enabled = sender.Checked
        self.gameName2Control.textBox.Enabled = sender.Checked
        self.trophySeriesControl.dropDown.Enabled = sender.Checked
        self.trophyModelControl.Enabled = sender.Checked
        self.trophyImageControl.Enabled = sender.Checked

    def cspCostumeChanged(self, sender, args):
        if self.cspCostumeListBox.SelectedItem:
            self.cspListBox.DataSource = self.cspCostumeListBox.SelectedItem.costumeObjects
            self.cspListBox.DisplayMember = "name"
            if self.cspListBox.SelectedItem and self.cspListBox.SelectedItem.csp:
                self.cspPictureBox.Image = createBitmap(self.cspListBox.SelectedItem.csp)
            else:
                self.cspPictureBox.Image = None
        self.addColorButton.Enabled = self.cspCostumeListBox.SelectedItem != None
        self.removeColorButton.Enabled = self.cspCostumeListBox.SelectedItem != None

    def cspChanged(self, sender, args):
        buttonsEnabled = self.cspCostumeListBox.SelectedItem != None
        self.cspButton.Enabled = buttonsEnabled
        self.cspHdButton.Enabled = buttonsEnabled
        self.stockButton.Enabled= buttonsEnabled
        self.stockHdButton.Enabled = buttonsEnabled
        if self.cspListBox.SelectedValue:
            if self.cspListBox.SelectedValue.csp:
                self.cspPictureBox.Image = createBitmap(self.cspListBox.SelectedValue.csp)
            else:
                self.cspPictureBox.Image = None
            if self.cspListBox.SelectedValue.cspHd:
                self.cspHdPictureBox.Image = createBitmap(self.cspListBox.SelectedValue.cspHd) 
            else:
                self.cspHdPictureBox.Image = None
            if self.cspListBox.SelectedValue.stock:
                self.stockPictureBox.Image = createBitmap(self.cspListBox.SelectedValue.stock)
            else:
                self.stockPictureBox.Image = None
            if self.cspListBox.SelectedValue.stockHd:
                self.stockHdPictureBox.Image = createBitmap(self.cspListBox.SelectedValue.stockHd)
            else:
                self.stockHdPictureBox.Image = None
        else:
            self.cspPictureBox.Image = None
            self.cspHdPictureBox.Image = None
            self.stockPictureBox.Image = None
            self.stockHdPictureBox.Image = None

    def bpChanged(self, sender, args):
        index = self.bpTabControl.SelectedIndex
        if self.bpListBoxes[index].SelectedValue:
            if self.bpListBoxes[index].SelectedValue.bp:
                self.bpPictureBoxes[index].Image = createBitmap(self.bpListBoxes[index].SelectedValue.bp)
            else:
                self.bpPictureBoxes[index].Image = None
            if self.bpListBoxes[index].SelectedValue.bpHd:
                self.bpHdPictureBoxes[index].Image = createBitmap(self.bpListBoxes[index].SelectedValue.bpHd)
            else:
                self.bpHdPictureBoxes[index].Image = None
        else:
            self.bpPictureBoxes[index].Image = None
            self.bpHdPictureBoxes[index].Image = None

    def cspCostumeButtonPressed(self, sender, args):
        self.addCostumeGroup()

    def addCostumeGroup(self, index):
        if len(self.costumeGroups) <= index:
            newGroup = CostumeGroup("Costume " + str(index + 1), BindingSource())
            self.costumeGroups.Add(newGroup)
            buttonsEnabled = len(self.cspCostumeListBox.Items) > 0 and self.cspCostumeListBox.SelectedItem != None
            self.cspButton.Enabled = buttonsEnabled
            self.cspHdButton.Enabled = buttonsEnabled
            self.stockButton.Enabled = buttonsEnabled
            self.stockHdButton.Enabled= buttonsEnabled
        else:
            newGroup = self.costumeGroups[index]
        return newGroup

    def cspCostumeRemoveButtonPressed(self, sender, args):
        if len(self.costumeGroups) > 0:
            i = 0
            j = 0
            while i < len(self.costumeGroups):
                if self.costumeGroups[i] == self.cspCostumeListBox.SelectedItem:
                    i += 1
                    continue
                self.costumeGroups[i].costumeGroup = "Costume " + str(j + 1)
                j += 1
                i += 1
            self.costumeGroups.Remove(self.cspCostumeListBox.SelectedItem)
            buttonsEnabled = len(self.cspCostumeListBox.Items) > 0 and self.cspCostumeListBox.SelectedItem != None
            self.cspButton.Enabled = buttonsEnabled
            self.cspHdButton.Enabled = buttonsEnabled
            self.stockButton.Enabled = buttonsEnabled
            self.stockHdButton.Enabled= buttonsEnabled

    def addColorButtonPressed(self, sender, args):
        if self.cspCostumeListBox.SelectedItem:
            self.cspCostumeListBox.SelectedItem.costumeObjects.Add(CostumeObject(name="Color " + str(len(self.cspCostumeListBox.SelectedItem.costumeObjects) + 1)))
            self.cspListBox.DisplayMember = "name"

    def addBpButtonPressed(self, sender, args):
        self.bps[self.bpTabControl.SelectedIndex].Add(BpObject(name="Image " + str(len(self.bpListBoxes[self.bpTabControl.SelectedIndex].Items) + 1)))

    def removeBpButtonPressed(self, sender, args):
        index = self.bpTabControl.SelectedIndex
        if self.bpListBoxes[index].SelectedItem:
            if len(self.bpListBoxes[index].Items) > 0:
                i = 0
                j = 0
                while i < len(self.bpListBoxes[index].Items):
                    if self.bpListBoxes[index].Items[i] == self.bpListBoxes[index].SelectedItem:
                        i += 1
                        continue
                    self.bpListBoxes[index].Items[i].name = "Image " + str(j + 1)
                    j += 1
                    i += 1
                self.bps[index].Remove(self.bpListBoxes[index].SelectedItem)

    def removeColorButtonPressed(self, sender, args):
        if self.cspCostumeListBox.SelectedItem:
            if len(self.cspCostumeListBox.SelectedItem.costumeObjects) > 0:
                i = 0
                j = 0
                while i < len(self.cspListBox.Items):
                    if self.cspListBox.Items[i] == self.cspListBox.SelectedItem:
                        i += 1
                        continue
                    self.cspListBox.Items[i].name = "Color " + str(j + 1)
                    j += 1
                    i += 1
                self.cspCostumeListBox.SelectedItem.costumeObjects.Remove(self.cspListBox.SelectedItem)
                self.cspListBox.DisplayMember = "name"

    # imageType - csp, cspHd, stock, stockHd
    def updateImages(self, dialogText, imageType, images="", costume=None):
        auto = True
        if not images:
            images = BrawlAPI.OpenMultiFileDialog(dialogText, "PNG files|*.png")
        if not costume:
            auto = False
            costume = self.cspCostumeListBox.SelectedItem
        if images:
            if len(images) == 1 and self.cspListBox.SelectedItem and not auto:
                if imageType == "csp":
                    self.cspListBox.SelectedItem.csp = images[0]
                elif imageType == "cspHd":
                    self.cspListBox.SelectedItem.cspHd = images[0]
                elif imageType == "stock":
                    self.cspListBox.SelectedItem.stock = images[0]
                elif imageType == "stockHd":
                    self.cspListBox.SelectedItem.stockHd = images[0]
            else:
                i = 0
                while i < len(images):
                    if i < len(costume.costumeObjects):
                        if imageType == "csp":
                            costume.costumeObjects[i].csp = images[i]
                        elif imageType == "cspHd":
                            costume.costumeObjects[i].cspHd = images[i]
                        elif imageType == "stock":
                            costume.costumeObjects[i].stock = images[i]
                        elif imageType == "stockHd":
                            costume.costumeObjects[i].stockHd = images[i]
                    else:
                        costume.costumeObjects.Add(CostumeObject(name="Color " + str(len(costume.costumeObjects) + 1), csp=images[i] if imageType == "csp" else "", cspHd=images[i] if imageType == "cspHd" else "", stock=images[i] if imageType == "stock" else "", stockHd=images[i] if imageType == "stockHd" else ""))
                        self.cspListBox.DisplayMember = "name"
                    i += 1
            if imageType == "csp":
                self.cspPictureBox.Image = createBitmap(self.cspListBox.SelectedItem.csp)
            elif imageType == "cspHd":
                self.cspHdPictureBox.Image = createBitmap(self.cspListBox.SelectedItem.cspHd)
            elif imageType == "stock":
                self.stockPictureBox.Image = createBitmap(self.cspListBox.SelectedItem.stock)
            elif imageType == "stockHd":
                self.stockHdPictureBox.Image = createBitmap(self.cspListBox.SelectedItem.stockHd)

    # imageType - bp, bpHd, bpName, bpNameHd
    def updateBpImages(self, dialogText, imageType, images="", index=-1):
        if index < 0:
            index = self.bpTabControl.SelectedIndex
        if not images:
            images = BrawlAPI.OpenMultiFileDialog(dialogText, "PNG files|*.png")
        if images and len(images) > 0:
            if len(images) == 1 and self.bpListBoxes[index].SelectedItem:
                if imageType == "bp":
                    self.bpListBoxes[index].SelectedItem.bp = images[0]
                elif imageType == "bpHd":
                    self.bpListBoxes[index].SelectedItem.bpHd = images[0]
            else:
                i = 0
                while i < len(images):
                    if i < len(self.bpListBoxes[index].Items):
                        if imageType == "bp":
                            self.bpListBoxes[index].Items[i].bp = images[i]
                        elif imageType == "bpHd":
                            self.bpListBoxes[index].Items[i].bpHd = images[i]
                    else:
                        self.bps[index].Add(BpObject(name="Image " + str(len(self.bpListBoxes[index].Items) + 1), bp=images[i] if imageType == "bp" else "", bpHd=images[i] if imageType == "bpHd" else ""))
                    i += 1
            if imageType == "bp":
                self.bpPictureBoxes[index].Image = createBitmap(self.bpListBoxes[index].SelectedItem.bp)
            elif imageType == "bpHd":
                self.bpHdPictureBoxes[index].Image = createBitmap(self.bpListBoxes[index].SelectedItem.bpHd)

    def bpButtonPressed(self, sender, args):
        self.updateBpImages("Select your SD BP images", "bp")

    def bpHdButtonPressed(self, sender, args):
        self.updateBpImages("Select your HD BP images", "bpHd")

    def cspButtonPressed(self, sender, args):
        self.updateImages("Select your SD CSP images", "csp")

    def cspHdButtonPressed(self, sender, args):
        self.updateImages("Select your HD CSP images", "cspHd")

    def stockButtonPressed(self, sender, args):
        self.updateImages("Select your SD stock images", "stock")

    def stockHdButtonPressed(self, sender, args):
        self.updateImages("Select your HD stock images", "stockHd")

    def bpNameButtonPressed(self, sender, args):
        index = self.bpTabControl.SelectedIndex
        self.bpNameImage[index] = BrawlAPI.OpenFileDialog("Select your SD BP name image", "PNG files|*.png")
        self.bpNamePictureBoxes[index].Image = createBitmap(self.bpNameImage[index])

    def bpNameHdButtonPressed(self, sender, args):
        index = self.bpTabControl.SelectedIndex
        self.bpNameHdImage[index] = BrawlAPI.OpenFileDialog("Select your HD BP name image", "PNG files|*.png")
        self.bpNameHdPictureBoxes[index].Image = createBitmap(self.bpNameHdImage[index])

    def toggleGroupBox(self, sender, args):
        collapsed = False
        if args.Location.X < 128 and args.Location.Y < 20:
            if sender.AutoSize:
                sender.AutoSize = False
                if sender.MinimumSize:
                    sender.MinimumSize = Size(128, 16)
                    sender.Size = Size(128, 16)
                collapsed = True
            else:
                sender.AutoSize = True
                # If box has maximum size, will be expanded to maximum size
                if sender.MaximumSize:
                    sender.MinimumSize = sender.MaximumSize
        self.recalculateGroupLocations()
        return collapsed

    def recalculateGroupLocations(self):
        self.cspGroupBox.Location = Point(0,16)
        self.bpGroupBox.Location = Point(self.cspGroupBox.Location.X, self.cspGroupBox.Location.Y + self.cspGroupBox.Height + 4)
        self.cssGroupBox.Location = Point(self.bpGroupBox.Location.X, self.bpGroupBox.Location.Y + self.bpGroupBox.Height + 4)
        x = max(self.cspGroupBox.Location.X + self.cspGroupBox.Width, self.bpGroupBox.Location.X + self.bpGroupBox.Width, self.cssGroupBox.Location.X + self.cssGroupBox.Width)
        self.replayGroupBox.Location = Point(x + 16, self.cspGroupBox.Location.Y)
        self.portraitNameGroupBox.Location = Point(x + 16, self.replayGroupBox.Location.Y + self.replayGroupBox.Height + 4)
        self.franchiseIconGroupBox.Location = Point(x + 16, self.portraitNameGroupBox.Location.Y + self.portraitNameGroupBox.Height + 4)
        self.readmeGroupBox.Location = Point(self.cosmeticsGroupBox.Location.X, self.cosmeticsGroupBox.Location.Y + self.cosmeticsGroupBox.Height + 4)
        x = max(self.cosmeticsGroupBox.Location.X + self.cosmeticsGroupBox.Width, self.readmeGroupBox.Location.X + self.readmeGroupBox.Width)
        self.fighterGroupBox.Location = Point(x + 16, self.cosmeticsGroupBox.Location.Y)
        self.mainFighterGroupBox.Location = Point(4, 16)
        self.kirbyHatGroupBox.Location = Point(self.mainFighterGroupBox.Location.X, self.mainFighterGroupBox.Location.Y + self.mainFighterGroupBox.Height + 4)
        self.soundGroupBox.Location = Point(self.kirbyHatGroupBox.Location.X, self.kirbyHatGroupBox.Location.Y + self.kirbyHatGroupBox.Height + 4)
        self.classicGroupBox.Location = Point(self.soundGroupBox.Location.X, self.soundGroupBox.Location.Y + self.soundGroupBox.Height + 4)
        self.miscGroupBox.Location = Point(self.fighterGroupBox.Location.X + self.fighterGroupBox.Width + 16, self.fighterGroupBox.Location.Y)
        self.codeGroupBox.Location = Point(4, 16)
        self.jigglypuffGroupBox.Location = Point(self.lucarioGroupBox.Location.X, self.lucarioGroupBox.Location.Y + self.lucarioGroupBox.Height + 4)
        self.bowserGroupBox.Location = Point(self.jigglypuffGroupBox.Location.X, self.jigglypuffGroupBox.Location.Y + self.jigglypuffGroupBox.Height + 4)
        self.trophyGroupBox.Location = Point(self.codeGroupBox.Location.X, self.codeGroupBox.Location.Y + self.codeGroupBox.Height + 4)
        y = max(self.cosmeticsGroupBox.Location.Y + self.cosmeticsGroupBox.Height, self.fighterGroupBox.Location.Y + self.fighterGroupBox.Height, self.miscGroupBox.Location.Y + self.miscGroupBox.Height, self.readmeGroupBox.Location.Y + self.readmeGroupBox.Height)
        self.openButton.Location = Point(self.cosmeticsGroupBox.Location.X + 4, y + 4)
        self.cancelButton.Location = Point(self.miscGroupBox.Location.X + self.miscGroupBox.Width - self.saveButton.Width, self.openButton.Location.Y)
        self.saveButton.Location = Point(self.cancelButton.Location.X - self.cancelButton.Width - 4, self.cancelButton.Location.Y)
        self.saveAsButton.Location = Point(self.saveButton.Location.X - self.saveButton.Width - 4, self.saveButton.Location.Y)

#endregion PACKAGE CHARACTER FORM

#region CLASSES AND CONTROLS

class CostumeGroup:
        def __init__(self, costumeGroup, costumeObjects):
            self.costumeGroup = costumeGroup
            self.costumeObjects = costumeObjects

class CostumeObject:
        def __init__(self, name="", csp="", cspHd="", stock="", stockHd=""):
            self.name = name
            self.csp = csp
            self.cspHd = cspHd
            self.stock = stock
            self.stockHd = stockHd

class BpObject:
        def __init__(self, name="", bp="", bpHd=""):
            self.name = name
            self.bp = bp
            self.bpHd = bpHd

class ImageObject:
        def __init__(self, label="Label", size=Size(64, 64)):
            self.label = label
            self.size = size

# A textbox with a label
class LabeledTextBox(UserControl):
        def __init__(self, labelText, idButtonType="", multiline=False, size=Size(100,120)):
            self.AutoSize = True
            self.AutoSizeMode = AutoSizeMode.GrowAndShrink
            self.idButtonType = idButtonType

            self.textBox = TextBox()
            self.textBox.Location = Point(64, 0)
            if multiline:
                self.textBox.Multiline = True
                self.textBox.ScrollBars = ScrollBars.Vertical
                self.textBox.AcceptsReturn = True
                self.textBox.WordWrap = True
                self.textBox.Size = size

            self.label = Label()
            self.label.Text = labelText + ":"
            self.label.Location = Point(self.textBox.Location.X - self.textBox.Width, self.textBox.Location.Y)
            self.label.TextAlign = ContentAlignment.TopRight

            idButton = Button()
            idButton.Text = "..."
            idButton.Size = Size(25, self.textBox.ClientSize.Height + 2)
            idButton.Location = Point(self.textBox.ClientSize.Width - idButton.Width, -1)
            idButton.Cursor = Cursors.Default
            idButton.Click += self.idButtonPressed

            if self.idButtonType:
                self.textBox.Controls.Add(idButton)

            self.Controls.Add(self.textBox)
            self.Controls.Add(self.label)

        def idButtonPressed(self, sender, args):
            id = showIdPicker(self.idButtonType)
            if id:
                self.textBox.Text = id

# A dropdown with a label
class LabeledDropDown(UserControl):
        def __init__(self, labelText, dataSource):
            self.AutoSize = True
            self.AutoSizeMode = AutoSizeMode.GrowAndShrink

            self.dropDown = ComboBox()
            self.dropDown.Location = Point(64, 0)
            self.dropDown.DropDownStyle = ComboBoxStyle.DropDownList
            self.dropDown.DisplayMember = "Key"
            self.dropDown.ValueMember = "Value"
            for object in dataSource:
                self.dropDown.Items.Add(object)

            self.label = Label()
            self.label.Text = labelText + ":"
            self.label.Location = Point(self.dropDown.Location.X - self.dropDown.Width, self.dropDown.Location.Y)
            self.label.TextAlign = ContentAlignment.TopRight

            self.Controls.Add(self.dropDown)
            self.Controls.Add(self.label)

# A control for importing a single file
class FileControl(UserControl):
        def __init__(self, title="Select your file", filter="PAC files|*.pac", labelText="File"):
            self.AutoSize = True
            self.AutoSizeMode = AutoSizeMode.GrowAndShrink
            self.title = title
            self.filter = filter

            self.textBox = LabeledTextBox(labelText)
            self.textBox.textBox.ReadOnly = True

            button = Button()
            button.Text = "Browse..."
            button.Location = Point(self.textBox.Location.X + self.textBox.Width + 16, self.textBox.Location.Y)
            button.Click += self.buttonPressed

            self.Controls.Add(self.textBox)
            self.Controls.Add(button)

        def buttonPressed(self, sender, args):
            file = BrawlAPI.OpenFileDialog(self.title, self.filter)
            if file:
                self.textBox.textBox.Text = file

# A control for importing multiple files
class MultiFileControl(UserControl):
        def __init__(self, title="Select your files", filter="PAC files|*.pac", labelText="Files", size=Size(100, 120)):
            self.AutoSize = True
            self.AutoSizeMode = AutoSizeMode.GrowAndShrink
            self.title = title
            self.filter = filter

            self.files = BindingSource()
            self.files.DataSource = []

            self.label = Label()
            self.label.Text = labelText + ":"
            self.label.Location = Point(0, 0)
            self.label.Height = 16

            self.listBox = ListBox()
            self.listBox.Size = size
            self.listBox.Location = Point(self.label.Location.X, self.label.Location.Y + 16)
            self.listBox.HorizontalScrollbar = True
            self.listBox.DataSource = self.files
            self.listBox.DisplayMember = "Name"
            self.listBox.ValueMember = "FullName"

            button = Button()
            button.Text = "Browse..."
            button.Location = Point(self.listBox.Location.X, self.listBox.Location.Y + self.listBox.Height)
            button.Click += self.buttonPressed

            self.Controls.Add(self.label)
            self.Controls.Add(self.listBox)
            self.Controls.Add(button)

        def buttonPressed(self, sender, args):
            files = BrawlAPI.OpenMultiFileDialog(self.title, self.filter)
            if files and len(files) > 0:
                self.files.DataSource = []
                for file in files:
                    self.files.Add(getFileInfo(file))
                #self.files.DataSource = files

class TabImageControl(UserControl):
    def __init__(self, tabNames, imageObjects):
        self.Dock = DockStyle.Fill
        self.tabControl = TabControl()
        self.tabControl.Dock = DockStyle.Fill

        tabs = [None] * len(tabNames)
        self.controls = [None] * len(tabNames)

        i = 0
        while i < len(tabs):
            # Tabs
            tabs[i] = TabPage()
            tabs[i].Text = tabNames[i]
            tabs[i].Name = tabNames[i]
            tabs[i].Anchor = (AnchorStyles.Bottom | AnchorStyles.Top | AnchorStyles.Right | AnchorStyles.Left)
            
            self.controls[i] = ImageControl(imageObjects)
            self.controls[i].Location = Point(4,4)

            tabs[i].Controls.Add(self.controls[i])

            # Add to control
            self.tabControl.Controls.Add(tabs[i])
            i += 1

        self.Controls.Add(self.tabControl)

# A control for importing multiple images. Pass in a number of ImageObjects to customize appearance.
class ImageControl(UserControl):
        def __init__(self, imageObjects):
            self.AutoSize = True
            self.AutoSizeMode = AutoSizeMode.GrowAndShrink

            count = len(imageObjects)

            self.label = [None] * count
            self.pictureBox = [None] * count
            button = [None] * count

            # Access the image paths by referencing this property for the desired index
            self.Images = [None] * count

            i = 0
            rowTracker = 0
            while i < count:
                self.label[i] = Label()
                self.label[i].Text = imageObjects[i].label + ":"
                if i == 0:
                    self.label[i].Location = Point(0, 0)
                elif rowTracker == 1:
                    x = max([self.label[i-1].Location.X + self.label[i-1].Width, self.pictureBox[i-1].Location.X + self.pictureBox[i-1].Width, button[i-1].Location.X + button[i-1].Width])
                    self.label[i].Location = Point(x + 4, self.label[i-1].Location.Y)
                else:
                    self.label[i].Location = Point(self.label[i-2].Location.X, button[i-2].Location.Y + button[i-2].Height + 16)
                self.label[i].Height = 16
                self.label[i].Width = 90

                self.pictureBox[i] = PictureBox()
                self.pictureBox[i].Location = Point(self.label[i].Location.X, self.label[i].Location.Y + self.label[i].Height + 4)
                self.pictureBox[i].Size = imageObjects[i].size
                self.pictureBox[i].SizeMode = PictureBoxSizeMode.StretchImage

                button[i] = Button()
                button[i].Text = "Browse..."
                button[i].Location = Point(self.pictureBox[i].Location.X, self.pictureBox[i].Location.Y + self.pictureBox[i].Height + 4)
                button[i].TabIndex = i
                button[i].Click += self.buttonPressed

                self.Controls.Add(self.label[i])
                self.Controls.Add(self.pictureBox[i])
                self.Controls.Add(button[i])

                i += 1
                if rowTracker < 1:
                    rowTracker += 1
                else:
                    rowTracker = 0
        
        def buttonPressed(self, sender, args):
            image = BrawlAPI.OpenFileDialog("Select image file", "PNG files|*.png")
            if image:
                self.pictureBox[sender.TabIndex].Image = createBitmap(image)
                self.Images[sender.TabIndex] = image

#endregion