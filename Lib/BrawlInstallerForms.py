version = "1.5.0"
# BrawlInstallerForms
# Library for forms used by BrawlInstaller

from BrawlInstallerLib import *
from BrawlLib.Internal.Windows.Controls import *
from System.Windows.Forms import *
from System.Drawing import *

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
        rb1 = RadioButton()
        rb1.Location = Point(16, 16)
        rb1.Text = "Auto"
        rb1.Size = Size(64, 16)
        rb1.Checked = True
        rb1.CheckedChanged += self.autoChecked
        rb2 = RadioButton()
        rb2.Location = Point(80, 16)
        rb2.Text = "Fighter ID"
        rb2.Size = Size(72, 16)
        rb2.CheckedChanged += self.fighterIdChecked
        rb3 = RadioButton()
        rb3.Location = Point(160, 16)
        rb3.Text = "All IDs"
        rb3.Size = Size(64, 16)
        rb3.CheckedChanged += self.allConfigChecked
        radioButtonGroup.Controls.Add(rb1)
        radioButtonGroup.Controls.Add(rb2)
        radioButtonGroup.Controls.Add(rb3)

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
        fighterIdTextbox = TextBox()
        fighterIdTextbox.Dock = DockStyle.Right

        fighterIdPanel.Controls.Add(fighterIdLabel)
        fighterIdPanel.Controls.Add(fighterIdTextbox)

        cosmeticIdPanel = Panel()
        cosmeticIdPanel.Location = Point(16, 48)
        cosmeticIdPanel.TabIndex = 2
        cosmeticIdLabel = Label()
        cosmeticIdLabel.Dock = DockStyle.Left
        cosmeticIdLabel.Text = "Cosmetic ID:"
        cosmeticIdTextbox = TextBox()
        cosmeticIdTextbox.Dock = DockStyle.Right

        cosmeticIdPanel.Controls.Add(cosmeticIdLabel)
        cosmeticIdPanel.Controls.Add(cosmeticIdTextbox)

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
        cosmeticConfigIdTextbox = TextBox()
        cosmeticConfigIdTextbox.Dock = DockStyle.Right

        cosmeticConfigIdPanel.Controls.Add(cosmeticConfigIdLabel)
        cosmeticConfigIdPanel.Controls.Add(cosmeticConfigIdTextbox)

        slotConfigIdPanel = Panel()
        slotConfigIdPanel.Location = Point(16, 48)
        slotConfigIdPanel.TabIndex = 2
        slotConfigIdLabel = Label()
        slotConfigIdLabel.Dock = DockStyle.Left
        slotConfigIdLabel.Text = "Slot Config ID:"
        slotConfigIdTextbox = TextBox()
        slotConfigIdTextbox.Dock = DockStyle.Right

        slotConfigIdPanel.Controls.Add(slotConfigIdLabel)
        slotConfigIdPanel.Controls.Add(slotConfigIdTextbox)

        cssSlotConfigIdPanel = Panel()
        cssSlotConfigIdPanel.Location = Point(16, 80)
        cssSlotConfigIdPanel.TabIndex = 3
        cssSlotConfigIdLabel = Label()
        cssSlotConfigIdLabel.Dock = DockStyle.Left
        cssSlotConfigIdLabel.Text = "CSS Slot Config ID:"
        cssSlotConfigIdTextbox = TextBox()
        cssSlotConfigIdTextbox.Dock = DockStyle.Right

        cssSlotConfigIdPanel.Controls.Add(cssSlotConfigIdLabel)
        cssSlotConfigIdPanel.Controls.Add(cssSlotConfigIdTextbox)

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
        subCharacterTextbox = TextBox()
        subCharacterTextbox.Dock = DockStyle.Right

        subCharacterPanel.Controls.Add(subCharacterLabel)
        subCharacterPanel.Controls.Add(subCharacterTextbox)

        self.subCharacterGroup.Controls.Add(subCharacterPanel)

        self.subCharacterGroup.Visible = False

        # Install button
        installButton = Button()
        installButton.Text = "Install"
        installButton.Dock = DockStyle.Bottom
        
        # Tooltips
        toolTip = ToolTip()
        toolTip.SetToolTip(fighterIdLabel, "Fighter ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(cosmeticIdLabel, "Cosmetic ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(cosmeticConfigIdLabel, "Cosmetic config ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(slotConfigIdLabel, "Slot config ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(cssSlotConfigIdLabel, "CSS slot config ID in decimal (33) or hexadecimal (0x21) format")
        toolTip.SetToolTip(self.checkbox, "When enabled, character will be installed as a sub character")
        toolTip.SetToolTip(subCharacterLabel, "The CSS slot config ID of the base character for this fighter")
        toolTip.SetToolTip(rb1, "All IDs will be selected automatically")      
        toolTip.SetToolTip(rb2, "Manually specify fighter ID and cosmetic ID")
        toolTip.SetToolTip(rb3, "Manually specify all Ex config IDs") 

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