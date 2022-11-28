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
        self.MinimumSize = Size(250,128)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.stageSlots = BindingSource()
        self.stageSlots.DataSource = []
        self.unusedSlots = BindingSource()
        self.unusedSlots.DataSource = []
        pageNumber = 0
        fileOpened = BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/stage/stageslot/')
        if fileOpened:
            pages = getStageList()
            for page in pages:
                pageNumber += 1
                pageSlot = StageSlot('0x00', '00', '00', '0000', '--PAGE ' + str(pageNumber) + '--')
                self.stageSlots.Add(pageSlot)
                for slotId in page:
                    stageIds = getStageIdsByNumber(slotId)
                    stageName = getStageName(stageIds[2:4])
                    stageSlot = StageSlot(slotId, stageIds[2:4], stageIds[4:6], stageIds[2:6], stageName)
                    self.stageSlots.Add(stageSlot)

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
                    unusedSlot = StageSlot(hexId(i + 1), stage[2:4], stage[4:6], stage[2:6], stageName)
                self.unusedSlots.Add(unusedSlot)
            i += 1
        BrawlAPI.ForceCloseFile()

        self.listBox = ListBox()
        self.listBox.Width = 120
        self.listBox.Height = 240
        self.listBox.Location = Point(16, 16)
        self.listBox.DataSource = self.stageSlots
        self.listBox.DisplayMember = "name"
        self.listBox.ValueMember = "fullId"

        self.unusedListbox = ListBox()
        self.unusedListbox.Width = 120
        self.unusedListbox.Height = 240
        self.unusedListbox.Location = Point(256, 16)
        self.unusedListbox.DataSource = self.unusedSlots
        self.unusedListbox.DisplayMember = "name"
        self.unusedListbox.ValueMember = "fullId"

        button = Button()
        button.Location = Point(144, 16)
        button.Text = "Edit"
        button.Click += self.buttonPressed

        addButton = Button()
        addButton.Location = Point(144, 48)
        addButton.Text = "Add"
        addButton.Click += self.addButtonPressed

        moveLeftButton = Button()
        moveLeftButton.Location = Point(144, 80)
        moveLeftButton.Text = "<"
        moveLeftButton.Click += self.moveLeftButtonPressed

        moveUpButton = Button()
        moveUpButton.Location = Point(144, 112)
        moveUpButton.Text = "^"
        moveUpButton.Click += self.moveUpButtonPressed

        saveButton = Button()
        saveButton.Location = Point(144, 144)
        saveButton.Text = "Save"
        saveButton.Click += self.saveButtonPressed

        self.Controls.Add(self.listBox)
        self.Controls.Add(button)
        self.Controls.Add(addButton)
        self.Controls.Add(moveLeftButton)
        self.Controls.Add(moveUpButton)
        self.Controls.Add(saveButton)
        self.Controls.Add(self.unusedListbox)
    
    def buttonPressed(self, sender, args):
        if not self.listBox.SelectedItem.name.startswith('--PAGE '):
            fullId = str(self.listBox.SelectedValue)
            form = StageEditor(fullId)
            result = form.ShowDialog(MainForm.Instance)

    def addButtonPressed(self, sender, args):
        #newSlotId = getUnusedSlotId(self.stageSlots)
        #BrawlAPI.ShowMessage(str(newSlotId), "")
        newId = self.getFirstAvailableId()
        #updateStageList(self.stageSlots)
        form = StageEditor(newId, True)
        result = form.ShowDialog(MainForm.Instance)
        if result == DialogResult.OK:
            if form.newSlotNumber > -1:
                self.unusedSlots.Add(StageSlot(hexId(form.newSlotNumber), newId[0:2], newId[2:4], newId[0:4], form.alts[0].aslEntry.Name))
            BrawlAPI.ShowMessage("Stage added successfully.", "Success")
            #self.Controls.Clear()
            #self.__init__()

    def moveLeftButtonPressed(self, sender, args):
        if len(self.unusedSlots) > 0:
            #self.listBox.Add(self.unusedListbox.SelectedItem)
            #self.unusedListbox.Remove(self.unusedListbox.SelectedItem)
            self.stageSlots.Add(self.unusedListbox.SelectedItem)
            self.unusedSlots.Remove(self.unusedListbox.SelectedItem)

    def moveUpButtonPressed(self, sender, args):
        aboveValue = self.stageSlots[self.listBox.SelectedIndex - 1]
        selectedValue = self.stageSlots[self.listBox.SelectedIndex]
        self.stageSlots[self.listBox.SelectedIndex - 1] = selectedValue
        self.stageSlots[self.listBox.SelectedIndex] = aboveValue
        self.listBox.SelectedIndex = self.listBox.SelectedIndex - 1

    def saveButtonPressed(self, sender, args):
        updateStageList(self.listBox.Items)
        buildGct()

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
        self.MinimumSize = Size(250,128)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.AutoSizeMode = AutoSizeMode.GrowAndShrink

        self.cosmetics = getStageCosmetics(fullId[2:4])
        self.alts = BindingSource()
        self.alts.DataSource = getStageAltInfo(fullId[0:2])
        #TODO: Import song BRSTMs (under the param listbox probably, or maybe as part of .tlst upload?), add new param entries/import .param files
        #add new stage slots
        #label cosmetics
        #maybe BRSTMs can be another listbox, lists files from tracklist in build, if you add a file it will show the filepath instead, filepath ones get imported
        #removing a stage will not remove the pair in TABLE_STAGES, it will just set them to 0xFF64
        #run GCTR after all is done
        #do step 4.3 in stage managing guide (incrementing numbers at bottom of thingy)

        # Variables
        self.newIcon = ""
        self.newName = ""
        self.newPreview = ""
        self.newFranchiseIcon = ""
        self.newGameLogo = ""
        self.newAltName = ""
        self.cosmeticId = fullId[2:4]
        self.stageId = fullId[0:2]
        self.new = new
        self.newSlotNumber = -1

        # Cosmetics Groupbox
        cosmeticsGroupBox = GroupBox()
        cosmeticsGroupBox.Location = Point(0,0)
        cosmeticsGroupBox.AutoSize = True
        cosmeticsGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        cosmeticsGroupBox.Text = "Cosmetics"

        # Stage Name
        self.namePictureBox = PictureBox()
        self.namePictureBox.Location = Point(16, 160)
        self.namePictureBox.Width = 208
        self.namePictureBox.Height = 56
        self.namePictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.stageName and not self.new:
            self.namePictureBox.Image = self.cosmetics.stageName

        nameButton = Button()
        nameButton.Text = "Import"
        nameButton.Location = Point(16, 220)
        nameButton.Click += self.nameButtonPressed

        # Stage R-Alt Name
        self.altNamePictureBox = PictureBox()
        self.altNamePictureBox.Location = Point(16, 264)
        self.altNamePictureBox.Width = 208
        self.altNamePictureBox.Height = 56
        self.altNamePictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.altName and not self.new:
            self.altNamePictureBox.Image = self.cosmetics.altName.image

        altLabel = Label()
        altLabel.Text = "Alt Layout Name:"
        altLabel.Location = Point(16, 248)

        self.altDropDown = ComboBox()
        self.altDropDown.DropDownStyle = ComboBoxStyle.DropDown
        self.altDropDown.Location = Point(16, 324)
        self.altDropDown.Width = 208
        self.altDropDown.BindingContext = self.BindingContext
        self.altDropDown.DataSource = self.cosmetics.stageNameList
        self.altDropDown.DisplayMember = "name"
        self.altDropDown.ValueMember = "image"
        self.altDropDown.SelectedValueChanged += self.altDropDownChanged

        # Stage Icon
        self.iconPictureBox = PictureBox()
        self.iconPictureBox.Location = Point(240, 160)
        self.iconPictureBox.Width = 128
        self.iconPictureBox.Height = 112
        self.iconPictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.stageIcon and not self.new:
            self.iconPictureBox.Image = self.cosmetics.stageIcon

        iconButton = Button()
        iconButton.Text = "Import"
        iconButton.Location = Point(240, 276)
        iconButton.Click += self.iconButtonPressed

        # Franchise Icon
        self.franchiseIconPictureBox = PictureBox()
        self.franchiseIconPictureBox.Location = Point(16, 350)
        self.franchiseIconPictureBox.Width = 64
        self.franchiseIconPictureBox.Height = 64
        self.franchiseIconPictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.franchiseIcon and not self.new:
            self.franchiseIconPictureBox.Image = self.cosmetics.franchiseIcon.image

        self.franchiseIconDropDown = ComboBox()
        self.franchiseIconDropDown.DropDownStyle = ComboBoxStyle.DropDown
        self.franchiseIconDropDown.Location = Point(16, 418)
        self.franchiseIconDropDown.BindingContext = self.BindingContext
        self.franchiseIconDropDown.DataSource = self.cosmetics.franchiseIconList
        self.franchiseIconDropDown.DisplayMember = "name"
        self.franchiseIconDropDown.ValueMember = "image"
        self.franchiseIconDropDown.SelectedValueChanged += self.franchiseIconDropDownChanged

        franchiseIconButton = Button()
        franchiseIconButton.Text = "Add"
        franchiseIconButton.Location = Point(16, 442)

        # Game Logo
        self.gameLogoPictureBox = PictureBox()
        self.gameLogoPictureBox.Location = Point(160, 350)
        self.gameLogoPictureBox.Width = 120
        self.gameLogoPictureBox.Height = 56
        self.gameLogoPictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.gameLogo and not self.new:
            self.gameLogoPictureBox.Image = self.cosmetics.gameLogo.image

        self.gameLogoDropDown = ComboBox()
        self.gameLogoDropDown.DropDownStyle = ComboBoxStyle.DropDown
        self.gameLogoDropDown.Location = Point(160, 418)
        self.gameLogoDropDown.BindingContext = self.BindingContext
        self.gameLogoDropDown.DataSource = self.cosmetics.gameLogoList
        self.gameLogoDropDown.DisplayMember = "name"
        self.gameLogoDropDown.ValueMember = "image"
        self.gameLogoDropDown.SelectedValueChanged += self.gameLogoDropDownChanged

        gameLogoButton = Button()
        gameLogoButton.Text = "Add"
        gameLogoButton.Location = Point(160, 442)

        # Stage Preview
        self.previewPictureBox = PictureBox()
        self.previewPictureBox.Location = Point(32, 16)
        self.previewPictureBox.Width = 312
        self.previewPictureBox.Height = 112
        self.previewPictureBox.SizeMode = PictureBoxSizeMode.CenterImage
        if self.cosmetics.stagePreview and not self.new:
            self.previewPictureBox.Image = self.cosmetics.stagePreview

        previewButton = Button()
        previewButton.Text = "Import"
        previewButton.Location = Point(32, 132)
        previewButton.Click += self.previewButtonPressed

        cosmeticsGroupBox.Controls.Add(self.previewPictureBox)
        cosmeticsGroupBox.Controls.Add(previewButton)
        cosmeticsGroupBox.Controls.Add(self.namePictureBox)
        cosmeticsGroupBox.Controls.Add(nameButton)
        cosmeticsGroupBox.Controls.Add(self.iconPictureBox)
        cosmeticsGroupBox.Controls.Add(iconButton)
        cosmeticsGroupBox.Controls.Add(self.altNamePictureBox)
        cosmeticsGroupBox.Controls.Add(altLabel)
        cosmeticsGroupBox.Controls.Add(self.altDropDown)
        cosmeticsGroupBox.Controls.Add(self.franchiseIconPictureBox)
        cosmeticsGroupBox.Controls.Add(self.franchiseIconDropDown)
        cosmeticsGroupBox.Controls.Add(franchiseIconButton)
        cosmeticsGroupBox.Controls.Add(self.gameLogoPictureBox)
        cosmeticsGroupBox.Controls.Add(self.gameLogoDropDown)
        cosmeticsGroupBox.Controls.Add(gameLogoButton)

        # Parameters Groupbox
        parametersGroupBox = GroupBox()
        parametersGroupBox.Location = Point(384, 0)
        parametersGroupBox.AutoSize = True
        parametersGroupBox.AutoSizeMode = AutoSizeMode.GrowAndShrink
        parametersGroupBox.Text = "Parameters"

        # Stage Alt Listbox
        self.stageAltListbox = ListBox()
        self.stageAltListbox.DataSource = self.alts
        self.stageAltListbox.DisplayMember = "aslEntry"
        self.stageAltListbox.ValueMember = "aslEntry"
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
        self.tracklistTextBox = TextBox()
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
        self.aslIndicator.Location = Point(16, 320)
        if len(self.alts) > 0:
            self.aslIndicator.TargetNode = self.alts[0].aslEntry
        else:
            self.aslIndicator.Visible = False

        parametersGroupBox.Controls.Add(self.stageAltListbox)
        parametersGroupBox.Controls.Add(stageAltAddButton)
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
        parametersGroupBox.Controls.Add(self.tracklistButton)
        parametersGroupBox.Controls.Add(self.tracklistFileBox)
        parametersGroupBox.Controls.Add(self.soundBankTextBox)
        parametersGroupBox.Controls.Add(soundBankLabel)
        parametersGroupBox.Controls.Add(self.soundBankButton)
        parametersGroupBox.Controls.Add(self.soundBankFileBox)
        parametersGroupBox.Controls.Add(self.effectBankTextBox)
        parametersGroupBox.Controls.Add(effectBankLabel)
        parametersGroupBox.Controls.Add(self.aslIndicator)

        saveButton = Button()
        saveButton.Text = "Save"
        saveButton.Location = Point(16, 500)
        saveButton.Click += self.saveButtonPressed

        self.Controls.Add(cosmeticsGroupBox)
        self.Controls.Add(parametersGroupBox)
        self.Controls.Add(saveButton)

        self.setComboBoxes()

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

    def saveButtonPressed(self, sender, args):
        if len(self.alts) <= 0:
            BrawlAPI.ShowMessage("You must have at least one stage entry defined to continue!", "Add Stage Entries")
            return
        moveStageFiles(self.alts)
        if self.newIcon or self.newName or self.newPreview or self.newFranchiseIcon or self.newGameLogo or self.newAltName:
            importStageCosmetics(self.cosmeticId, stageIcon=self.newIcon, stageName=self.newName, stagePreview=self.newPreview, franchiseIconName=self.newFranchiseIcon, gameLogoName=self.newGameLogo, altStageName=self.newAltName)
            importStageCosmetics(self.cosmeticId, stageIcon=self.newIcon, stageName=self.newName, stagePreview=self.newPreview, franchiseIconName=self.newFranchiseIcon, gameLogoName=self.newGameLogo, altStageName=self.newAltName, fileName='/pf/menu2/mu_menumain.pac')
        updateStageSlot(self.stageId, self.stageAltListbox.Items)
        updateStageParams(self.stageId, self.stageAltListbox.Items)
        if self.new:
            self.newSlotNumber = addStageId(self.stageId + self.cosmeticId, self.alts[0].aslEntry.Name)
        #self.Controls.Clear()
        #self.__init__(self.stageId + self.cosmeticId)
        self.DialogResult = DialogResult.OK
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

    def stageAltAddButtonPressed(self, sender, args):
        newAslEntry = ASLSEntryNode()
        newAslEntry.Name = "New_Stage"
        newStageAlt = StageParams(newAslEntry, "", "", "", int("0xFFFF", 16), int("0xFFFF", 16), "")
        self.alts.Add(newStageAlt)
        self.enableControls()

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