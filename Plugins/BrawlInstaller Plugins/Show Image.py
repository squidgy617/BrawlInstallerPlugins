__author__ = "Squidgy"
__version__ = "1.4.0"

from BrawlInstallerLib import *
from System.Drawing import Bitmap
from BrawlLib.OpenGL import GLTexture
from BrawlLib.Internal.Windows.Controls import *
from System.Windows.Forms import *

def buttonPressed(self, sender, args):
		self.i += 1
		self.Text = str(self.i)

def main():
		i = 0
		images = Directory.GetFiles("F:\\ryant\Documents\Ryan\Brawl Mods\Character Packages\Test Packages\RockmanX by CaliKingz01\CSPs\\0002", "*.png")
		while True:
			dlg = GLTextureWindow()
			dlg.Text = str(i)
			texture = GLTexture()
			texture.Attach(Bitmap(images[i]))
			#texture.Attach(Bitmap("F:\\ryant\Documents\Ryan\Brawl Mods\Character Packages\Test Packages\RockmanX by CaliKingz01\CSPs\\0002\\0001.png"))
			#control = GLTexturePanel()
			#control.Texture = texture
			#dlg.Controls.Add(control)
			button = Button()
			button.DialogResult = DialogResult.OK
			button.Text = 'BUTTON'
			button.Dock = DockStyle.Top
			#button.Click += buttonPressed(dlg)
			dlg.Controls.Add(button)
			
			# Can use this to see images in the program, maybe?
			#if (child.HasPalette):
			#	texture.Attach(child, child.GetPaletteNode())
			#else:
			#	texture.Attach(child.GetImage(0))
			result = dlg.ShowDialog(MainForm.Instance, texture)
			if result == DialogResult.OK:
				if i + 1 < len(images):
					i += 1
				else:
					i = 0
			else:
				break

main()