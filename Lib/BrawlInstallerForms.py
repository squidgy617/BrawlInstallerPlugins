version = "1.6.0"
# BrawlInstallerForms
# Library for forms used by BrawlInstaller

from BrawlInstallerLib import *
from BrawlLib.Internal.Windows.Controls import *
from System.Windows.Forms import *
from System.Drawing import *

#region STAGE LIST

class StageList(Form):

    def __init__(self):
        # Form parameters
        self.Text = 'Stage List'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MaximizeBox = False
        self.MinimumSize = Size(411,400)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.stageSlots = BindingSource()
        self.stageSlots.DataSource = []
        self.netplaySlots = BindingSource()
        self.netplaySlots.DataSource = []
        self.unusedSlots = BindingSource()
        self.unusedSlots.DataSource = []
        pageNumber = 0
        fileOpened = BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/stage/stageslot/')
        if fileOpened:
            pages = getStageList()
            for page in pages:
                pageNumber += 1
                pageSlot = StageSlot('0x00', '00', '00', '0000', '|| PAGE ' + str(pageNumber) + ' ||')
                self.stageSlots.Add(pageSlot)
                for slotId in page:
                    stageIds = getStageIdsByNumber(slotId)
                    stageName = getStageName(stageIds[2:4])
                    stageSlot = StageSlot(slotId, stageIds[2:4], stageIds[4:6], stageIds[2:6], stageName)
                    self.stageSlots.Add(stageSlot)
            pageNumber = 0
            pages = getStageList(True)
            for page in pages:
                pageNumber += 1
                pageSlot = StageSlot('0x00', '00', '00', '0000', '|| PAGE ' + str(pageNumber) + ' ||')
                self.netplaySlots.Add(pageSlot)
                for slotId in page:
                    stageIds = getStageIdsByNumber(slotId)
                    stageName = getStageName(stageIds[2:4])
                    stageSlot = StageSlot(slotId, stageIds[2:4], stageIds[4:6], stageIds[2:6], stageName)
                    self.netplaySlots.Add(stageSlot)

        # Get unused stages
        i = 0
        for stage in getStageIds():
            append = True
            for slot in self.stageSlots:
                if slot.fullId == stage.replace('0x',''):
                    append = False
                    break
            if append and stage != '0xFF64':
                stageName = getStageName(stage[2:4])
                if stageName:
                    unusedSlot = StageSlot(hexId(i), stage[2:4], stage[4:6], stage[2:6], stageName)
                self.unusedSlots.Add(unusedSlot)
            i += 1
        BrawlAPI.ForceCloseFile()

        self.tabControl = TabControl()
        self.tabControl.Dock = DockStyle.Fill

        offlineTab = TabPage()
        offlineTab.Text = 'Standard'
        self.tabControl.Controls.Add(offlineTab)

        netplayTab = TabPage()
        netplayTab.Text = 'Netplay'
        self.tabControl.Controls.Add(netplayTab)

        self.listBox = ListBox()
        self.listBox.Width = 120
        self.listBox.Height = 240
        self.listBox.Location = Point(16, 32)
        self.listBox.DataSource = self.stageSlots
        self.listBox.DisplayMember = "name"
        self.listBox.ValueMember = "fullId"
        self.listBox.DrawMode = DrawMode.OwnerDrawFixed
        self.listBox.DrawItem += self.listBoxDrawItem

        self.netplayListBox = ListBox()
        self.netplayListBox.Width = 120
        self.netplayListBox.Height = 240
        self.netplayListBox.Location = Point(16, 32)
        self.netplayListBox.DataSource = self.netplaySlots
        self.netplayListBox.DisplayMember = "name"
        self.netplayListBox.ValueMember = "fullId"
        self.netplayListBox.DrawMode = DrawMode.OwnerDrawFixed
        self.netplayListBox.DrawItem += self.listBoxDrawItem

        listBoxLabel = Label()
        listBoxLabel.Text = "Current Stages"
        listBoxLabel.Height = 16
        listBoxLabel.Location = Point(16, 8)

        self.unusedListbox = ListBox()
        self.unusedListbox.Width = 120
        self.unusedListbox.Height = 240
        self.unusedListbox.Location = Point(259, 32)
        self.unusedListbox.DataSource = self.unusedSlots
        self.unusedListbox.DisplayMember = "name"
        self.unusedListbox.ValueMember = "fullId"

        unusedListBoxLabel = Label()
        unusedListBoxLabel.Text = "Unused Stages"
        unusedListBoxLabel.Height = 16
        unusedListBoxLabel.Location = Point(259, 8)

        button = Button()
        button.Location = Point(16, 276)
        button.Text = "Edit"
        button.Click += self.buttonPressed

        addButton = Button()
        addButton.Location = Point(16, 304)
        addButton.Text = "Add"
        addButton.Click += self.addButtonPressed

        moveLeftButton = Button()
        moveLeftButton.Location = Point(160, 120)
        moveLeftButton.Text = "←"
        moveLeftButton.Click += self.moveLeftButtonPressed

        moveRightButton = Button()
        moveRightButton.Location = Point(160, 152)
        moveRightButton.Text = "→"
        moveRightButton.Click += self.moveRightButtonPressed

        moveUpButton = Button()
        moveUpButton.Location = Point(136, 31)
        moveUpButton.Text = "↑"
        moveUpButton.Size = Size(16, 32)
        moveUpButton.Click += self.moveUpButtonPressed

        moveDownButton = Button()
        moveDownButton.Location = Point(136, 63)
        moveDownButton.Text = "↓"
        moveDownButton.Size = Size(16, 32)
        moveDownButton.Click += self.moveDownButtonPressed

        saveButton = Button()
        saveButton.Location = Point(304, 276)
        saveButton.Text = "Save"
        saveButton.Click += self.saveButtonPressed

        cancelButton = Button()
        cancelButton.Location = Point(304, 304)
        cancelButton.Text = "Cancel"
        cancelButton.Click += self.cancelButtonPressed

        self.Controls.Add(self.tabControl)

        offlineTab.Controls.Add(listBoxLabel)
        offlineTab.Controls.Add(self.listBox)
        offlineTab.Controls.Add(button)
        offlineTab.Controls.Add(addButton)
        offlineTab.Controls.Add(moveUpButton)
        offlineTab.Controls.Add(moveDownButton)
        offlineTab.Controls.Add(moveLeftButton)
        offlineTab.Controls.Add(moveRightButton)
        offlineTab.Controls.Add(self.unusedListbox)
        offlineTab.Controls.Add(unusedListBoxLabel)
        offlineTab.Controls.Add(saveButton)
        offlineTab.Controls.Add(cancelButton)

        netplayTab.Controls.Add(self.netplayListBox)

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
        if not self.listBox.SelectedItem.name.startswith('|| PAGE '):
            fullId = str(self.listBox.SelectedValue)
            form = StageEditor(fullId)
            result = form.ShowDialog(MainForm.Instance)
            form.Dispose()
            if result == DialogResult.Abort:
                self.DialogResult = DialogResult.Abort
                self.Close()

    def addButtonPressed(self, sender, args):
        newId = self.getFirstAvailableId()
        form = StageEditor(newId, True)
        result = form.ShowDialog(MainForm.Instance)
        if result == DialogResult.OK:
            newSlot = ""
            if form.newSlotNumber > -1:
                newSlot = StageSlot(hexId(form.newSlotNumber), newId[0:2], newId[2:4], newId[0:4], form.alts[0].aslEntry.Name)
                self.unusedSlots.Add(newSlot)
                self.unusedListbox.SelectedItem = newSlot
            BrawlAPI.ShowMessage("Stage added successfully.", "Success")
            form.Dispose()
        elif result == DialogResult.Abort:
            form.Dispose()
            self.DialogResult = DialogResult.Abort
            self.Close()

    def moveLeftButtonPressed(self, sender, args):
        if len(self.unusedSlots) > 0 and not self.unusedListbox.SelectedItem.name.startswith('|| PAGE'):
            self.stageSlots.Add(self.unusedListbox.SelectedItem)
            self.listBox.SelectedItem = self.unusedListbox.SelectedItem
            self.unusedSlots.Remove(self.unusedListbox.SelectedItem)

    def moveRightButtonPressed(self, sender, args):
        if len(self.stageSlots) > 0 and not self.listBox.SelectedItem.name.startswith('|| PAGE'):
            self.unusedSlots.Add(self.listBox.SelectedItem)
            self.unusedListbox.SelectedItem = self.listBox.SelectedItem
            self.stageSlots.Remove(self.listBox.SelectedItem)

    def moveUpButtonPressed(self, sender, args):
        if self.listBox.SelectedIndex == 1 or self.listBox.SelectedItem.name.startswith('|| PAGE'):
            return
        aboveValue = self.stageSlots[self.listBox.SelectedIndex - 1]
        selectedValue = self.stageSlots[self.listBox.SelectedIndex]
        self.stageSlots[self.listBox.SelectedIndex - 1] = selectedValue
        self.stageSlots[self.listBox.SelectedIndex] = aboveValue
        self.listBox.SelectedIndex = self.listBox.SelectedIndex - 1

    def moveDownButtonPressed(self, sender, args):
        if self.listBox.SelectedIndex >= len(self.listBox.Items) - 1 or self.listBox.SelectedItem.name.startswith('|| PAGE'):
            return
        belowValue = self.stageSlots[self.listBox.SelectedIndex + 1]
        selectedValue = self.stageSlots[self.listBox.SelectedIndex]
        self.stageSlots[self.listBox.SelectedIndex + 1] = selectedValue
        self.stageSlots[self.listBox.SelectedIndex] = belowValue
        self.listBox.SelectedIndex = self.listBox.SelectedIndex + 1

    def saveButtonPressed(self, sender, args):
        try:
            updateStageList(self.listBox.Items)
            buildGct()
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
        #self.Controls.Clear()
        #self.__init__()
        self.DialogResult = DialogResult.Cancel
        self.Close()

    def getFirstAvailableId(self):
        stageId = 1
        i = 0
        while True:
            while i < len(self.stageSlots):
                if hexId(stageId).replace('0x', '') == self.stageSlots[i].stageId:
                    stageId += 1
                    i = 0
                i += 1
            break
        cosmeticId = 1
        i = 0
        while True:
            while i < len(self.stageSlots):
                if hexId(cosmeticId).replace('0x', '') == self.stageSlots[i].cosmeticId:
                    cosmeticId += 1
                    i = 0
                i += 1
            break
        return hexId(stageId).replace('0x', '') + hexId(cosmeticId).replace('0x', '')

#endregion

#region EDIT STAGE

class StageEditor(Form):

    def __init__(self, fullId, new=False):
        # Form parameters
        self.Text = 'Edit Stage'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MaximizeBox = False
        self.MinimumSize = Size(250,128)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.cosmetics = getStageCosmetics(fullId[2:4])
        self.alts = BindingSource()
        self.alts.DataSource = getStageAltInfo(fullId[0:2])
        self.addedTracks = BindingSource()
        self.addedTracks.DataSource = []
        #TODO:
        #removing a stage will not remove the pair in TABLE_STAGES, it will just set them to 0xFF64
        #netplay support

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
        self.newSlotNumber = -1

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

        nameLabel = Label()
        nameLabel.Text = "Name:"
        nameLabel.Location = Point(16, 176)
        nameLabel.Height = 16

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
        self.franchiseIconPictureBox.SizeMode = PictureBoxSizeMode.CenterImage
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
        cosmeticsGroupBox.Controls.Add(nameLabel)
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
        aslIndicatorGroupBox.Location = Point(16, 352)
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

        self.trackListBox = ListBox()
        self.trackListBox.Location = Point(16, 216)
        self.trackListBox.DataSource = self.addedTracks
        self.trackListBox.DisplayMember = "filePath"
        self.trackListBox.HorizontalScrollbar = True

        self.trackAddButton = Button()
        self.trackAddButton.Text = "Import BRSTMs"
        self.trackAddButton.Location = Point(16, 320)
        self.trackAddButton.AutoSize = True
        self.trackAddButton.AutoSizeMode = AutoSizeMode.GrowAndShrink
        self.trackAddButton.Click += self.trackAddButtonPressed
        self.trackAddButton.Enabled = True if len(self.alts) > 0 else False

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
        self.tracklistTextBox.DropDownStyle = ComboBoxStyle.DropDown
        self.tracklistTextBox.DataSource = self.tracklistFiles
        self.tracklistTextBox.Text = self.alts[0].tracklist if len(self.alts) > 0 else ""
        self.tracklistTextBox.Location = Point(208, 160)
        self.tracklistTextBox.Width = 160
        self.tracklistTextBox.TextChanged += self.tracklistTextChanged
        self.tracklistTextBox.Enabled = True if len(self.alts) > 0 else False

        tracklistLabel = Label()
        tracklistLabel.Text = "Tracklist:"
        tracklistLabel.Location = Point(104, 160)
        tracklistLabel.TextAlign = ContentAlignment.TopRight

        self.tracklistButton = Button()
        self.tracklistButton.Text = "Browse..."
        self.tracklistButton.Location = Point(376, 159)
        self.tracklistButton.Click += self.tracklistButtonPressed
        self.tracklistButton.Enabled = True if len(self.alts) > 0 else False

        self.tracklistFileBox = TextBox()
        self.tracklistFileBox.Location = Point(208, 184)
        self.tracklistFileBox.Width = 160
        self.tracklistFileBox.ReadOnly = True

        # Soundbank textbox
        self.soundBankTextBox = TextBox()
        self.soundBankTextBox.Text = str(hexId(self.alts[0].soundBank)) if len(self.alts) > 0 else "0xFFFF"
        self.soundBankTextBox.Location = Point(208, 216)
        self.soundBankTextBox.Width = 160
        self.soundBankTextBox.TextChanged += self.soundBankTextChanged
        self.soundBankTextBox.Enabled = True if len(self.alts) > 0 else False

        soundBankLabel = Label()
        soundBankLabel.Text = "Sound Bank:"
        soundBankLabel.Location = Point(104, 216)
        soundBankLabel.TextAlign = ContentAlignment.TopRight

        self.soundBankButton = Button()
        self.soundBankButton.Text = "Browse..."
        self.soundBankButton.Location = Point(376, 215)
        self.soundBankButton.Click += self.soundBankButtonPressed
        self.soundBankButton.Enabled = True if len(self.alts) > 0 else False

        self.soundBankFileBox = TextBox()
        self.soundBankFileBox.Location = Point(208, 240)
        self.soundBankFileBox.Width = 160
        self.soundBankFileBox.ReadOnly = True

        # Effectbank textbox
        self.effectBankTextBox = TextBox()
        self.effectBankTextBox.Text = str(hexId(self.alts[0].effectBank)) if len(self.alts) > 0 else "0xFFFF"
        self.effectBankTextBox.Location = Point(208, 272)
        self.effectBankTextBox.Width = 160
        self.effectBankTextBox.TextChanged += self.effectBankTextChanged
        self.effectBankTextBox.Enabled = True if len(self.alts) > 0 else False

        effectBankLabel = Label()
        effectBankLabel.Text = "Effect Bank:"
        effectBankLabel.Location = Point(104, 272)
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
        saveButton.Location = Point(336, 704)
        saveButton.Click += self.saveButtonPressed
        saveButton.Width = 96

        cancelButton = Button()
        cancelButton.Text = "Cancel"
        cancelButton.Location = Point(440, 704)
        cancelButton.Click += self.cancelButtonPressed
        cancelButton.Width = 96

        parametersGroupBox.Controls.Add(self.stageAltListbox)
        parametersGroupBox.Controls.Add(stageAltAddButton)
        parametersGroupBox.Controls.Add(stageAltRemoveButton)
        parametersGroupBox.Controls.Add(stageAltImportButton)
        parametersGroupBox.Controls.Add(self.stageAltFileBox)
        parametersGroupBox.Controls.Add(self.trackListBox)
        parametersGroupBox.Controls.Add(self.trackAddButton)
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
        parametersGroupBox.Controls.Add(self.tracklistButton)
        parametersGroupBox.Controls.Add(self.tracklistFileBox)
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

        self.setComboBoxes()

    def getTracklists(self):
        tracklistFiles = []
        directory = Directory.CreateDirectory(MainForm.BuildPath + '/pf/sound/tracklist')
        for file in directory.GetFiles("*.tlst"):
            tracklistFiles.append(file.Name.split('.')[0])
        return tracklistFiles

    def setComboBoxes(self):
        if not self.new:
            i = 0
            while i < len(self.cosmetics.franchiseIconList):
                if self.cosmetics.franchiseIconList[i].name == self.cosmetics.franchiseIcon.name:
                    self.franchiseIconDropDown.SelectedIndex = i
                    break
                i += 1
            i = 0
            while i < len(self.cosmetics.stageNameList):
                if self.cosmetics.stageNameList[i].name == self.cosmetics.altName.name:
                    self.altDropDown.SelectedIndex = i
                    break
                i += 1
            i = 0
            while i < len(self.cosmetics.gameLogoList):
                if self.cosmetics.gameLogoList[i].name == self.cosmetics.gameLogo.name:
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
            self.tracklistTextBox.SelectedIndex = -1

    def stageAltChanged(self, sender, args):
        if len(self.alts) > 0:
            self.aslIndicator.TargetNode = self.stageAltListbox.SelectedValue
            self.moduleTextBox.Text = self.stageAltListbox.SelectedItem.module
            self.nameTextBox.Text = self.stageAltListbox.SelectedValue.Name
            self.pacNameTextBox.Text = self.stageAltListbox.SelectedItem.pacName
            self.tracklistTextBox.Text = self.stageAltListbox.SelectedItem.tracklist
            self.soundBankTextBox.Text = str(hexId(self.stageAltListbox.SelectedItem.soundBank))
            self.effectBankTextBox.Text = str(hexId(self.stageAltListbox.SelectedItem.effectBank))
            self.pacNameFileBox.Text = self.stageAltListbox.SelectedItem.pacFile
            self.moduleFileBox.Text = self.stageAltListbox.SelectedItem.moduleFile
            self.tracklistFileBox.Text = self.stageAltListbox.SelectedItem.tracklistFile
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

            for stageEntry in self.removeSlots:
                removeStageEntry(stageEntry)

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
                self.newSlotNumber = addStageId(self.stageId + self.cosmeticId, self.alts[0].aslEntry.Name)
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
        else:
            self.newAltName = ""

    def franchiseIconDropDownChanged(self, sender, args):
        self.franchiseIconPictureBox.Image = Bitmap(self.franchiseIconDropDown.SelectedValue)
        if self.franchiseIconDropDown.SelectedItem.name != self.cosmetics.franchiseIcon.name:
            self.newFranchiseIcon = self.franchiseIconDropDown.SelectedItem.name
        else:
            self.newFranchiseIcon = ""

    def gameLogoDropDownChanged(self, sender, args):
        self.gameLogoPictureBox.Image = Bitmap(self.gameLogoDropDown.SelectedValue)
        if self.gameLogoDropDown.SelectedItem.name != self.cosmetics.gameLogo.name:
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

    def tracklistTextChanged(self, sender, args):
        self.stageAltListbox.SelectedItem.tracklist = self.tracklistTextBox.Text

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

    def tracklistButtonPressed(self, sender, args):
        self.stageAltListbox.SelectedItem.tracklistFile = BrawlAPI.OpenFileDialog("Select your tracklist file", "TLST files|*.tlst")
        if self.stageAltListbox.SelectedItem.tracklistFile:
            fileName = getFileInfo(self.stageAltListbox.SelectedItem.tracklistFile).Name
            self.tracklistTextBox.Text = fileName.split('.')[0]
            self.tracklistFileBox.Text = self.stageAltListbox.SelectedItem.tracklistFile

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
        self.tracklistButton.Enabled = True
        self.soundBankButton.Enabled = True
        self.aslIndicator.Visible = True
        self.trackAddButton.Enabled = True

    def stageAltAddButtonPressed(self, sender, args):
        newAslEntry = ASLSEntryNode()
        newAslEntry.Name = "New_Stage"
        newStageAlt = StageParams(newAslEntry, "", "", "", int("0xFFFF", 16), int("0xFFFF", 16), "")
        self.alts.Add(newStageAlt)
        self.enableControls()

    def stageAltRemoveButtonPressed(self, sender, args):
        if len(self.alts) <= 0:
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
    
    def trackAddButtonPressed(self, sender, args):
        addedTracks = BrawlAPI.OpenMultiFileDialog("Select your BRSTM files", "BRSTM files|*.brstm")
        if addedTracks:
            outputDirectory = BrawlAPI.OpenFolderDialog("Select output directory")
            if outputDirectory:
                for track in addedTracks:
                    self.addedTracks.Add(ImportedFile(track, outputDirectory))

#endregion

#region COSTUME PROMPT

class CostumePrompt(Form):

    def __init__(self):
        # Form parameters
        self.Text = 'Install Costume'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.AutoSize = True
        self.MinimumSize = Size(250,128)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

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

        cssSlotConfigIdPanel.Controls.Add(cssSlotConfigIdLabel)
        cssSlotConfigIdPanel.Controls.Add(self.cssSlotConfigIdTextbox)

        self.fighterIdGroup.Controls.Add(cssSlotConfigIdPanel)
        self.fighterIdGroup.Controls.Add(cosmeticIdPanel)
        self.fighterIdGroup.Controls.Add(fighterIdPanel)

        # Install button
        installButton = Button()
        installButton.Text = "Install"
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
        if not self.cspFiles or not self.bpFiles or not self.stockFiles or not self.costumeFiles:
            proceed = BrawlAPI.ShowYesNoPrompt("You have not added all possible files. Would you like to proceed anyway?", "Files Missing")
            if proceed:
                self.DialogResult = DialogResult.OK
                self.Close()
            else:
                return
        self.DialogResult = DialogResult.OK
        self.Close()

#endregion COSTUME PROMPT

#region CHARACTER FORM

class CharacterForm(Form):

    def __init__(self):
        # Form parameters
        self.Text = 'Install Character'
        self.StartPosition = FormStartPosition.CenterParent
        self.ShowIcon = False
        self.Height = 128
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

#region COSTUME FORM

class CostumeForm(Form):

    def __init__(self, images, skipPositions=[], remove=False):
        # Form parameters
        self.Text = 'Select Costume'
        self.index = 0 # Index of selected costume
        self.labelIndex = 0 # Index displayed on label
        self.Width = 250
        self.Height = 350
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
        self.label.Height = 50
        self.label.Width = 150
        self.label.TextAlign = ContentAlignment.MiddleCenter

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

        # Add controls
        self.Controls.Add(self.pictureBox)
        self.Controls.Add(self.label)
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
        else:
            self.index = self.imageCount - 1
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