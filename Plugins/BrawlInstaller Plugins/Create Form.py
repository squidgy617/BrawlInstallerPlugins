__author__ = "Squidgy"
__version__ = "1.4.0"

from BrawlInstallerLib import *
from System.Drawing import Bitmap
from BrawlLib.OpenGL import GLTexture
from BrawlLib.Internal.Windows.Controls import *
from System.Windows.Forms import *

class CountForm(Form):

    def __init__(self):
        self.Text = 'Counter Demo'

        self.label = Label()
        self.label.Text = "Counter 0"
        self.label.Dock = DockStyle.Bottom
        self.label.Height = 50
        self.label.Width = 250

        self.count = 0

        button = Button()
        button.Text = "Start Counter"
        button.Dock = DockStyle.Top

        button.Click += self.buttonPressed

        pictureBox = PictureBox()
        pictureBox.Dock = DockStyle.Fill
        pictureBox.Image = Bitmap("F:\\ryant\Documents\Ryan\Brawl Mods\Character Packages\Test Packages\RockmanX by CaliKingz01\CSPs\\0002\\0001.png")

        self.Controls.Add(pictureBox)
        self.Controls.Add(self.label)
        self.Controls.Add(button)

    def buttonPressed(self, sender, args):
        self.count += 1
        self.label.Text = "Count %s" % self.count

def main():
		form = CountForm()
		form.ShowDialog(MainForm.Instance)

main()