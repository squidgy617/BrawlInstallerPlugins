# BrawlInstaller Plugins
A BrawlCrate plugin suite for easy installation of Brawl mods into BrawlEX builds. Currently supports automatic installation of entire characters, including their cosmetics, as long as they are packaged in a .zip file with the correct structure.

This tool was made possible by:
- Soopercool101, Kryal, BlackJax96, and libertyernie for BrawlLib, BrawlBox, and BrawlCrate. Extra thanks to Soopercool101 for making additions to BrawlCrate to support features needed for the BrawlInstaller plugins.
- markymawk, for their basic guide to writing plug-ins and for their plug-ins which served as a great learning resource.
- Kapedani and Hatyaro, for helping with some coding challenges.
- QuickLava and codes, for the various tools they created that these plugins are able to interact with.
- CaliKingz01, who provided the PSA for X to use as an example character package.
- Project+ EX and all the documentation provided and linked within KingJigglypuff's [P+Ex Release Document](https://docs.google.com/document/d/1mAoVGymOkL3FwiMxfEt1V24qxnAWiO8I66G3zlU0ij8/edit?usp=sharing). Learning these processes thoroughly was necessary for creating these plugins.
- The Brawl modding community and [Custom Brawl Modding discord](https://discord.gg/GbxJhbv), for being a great source of knowledge on all things Brawl-modding.

# Installation
## Prerequisites
In order for these plugins to function correctly, you will need a few things:
- The latest version of [BrawlCrate](https://github.com/soopercool101/BrawlCrate). As of release, you may need to be on BrawlCrate Canary for the plugins to function properly. To do this, open BrawlCrate and navigate to Tools > Settings > Updater, then check the "Opt into BrawlCrate Canary (Experimental) updates" box. You should also ensure you have your build path set to your build's root folder by navigating to Tools > Settings > General and modifying the "Default Build Path" there.
- The latest version of Python. You can download this at [python.org](https://www.python.org/). Also ensure your Python path is set within BrawlCrate by navigating to Tools > Settings > BrawlAPI and setting the "Installation Path" field under "Python".
- A BrawlEx build of Super Smash Bros. Brawl. It is strongly recommended to use these plugins with a build of [Project+ EX](https://docs.google.com/document/d/1mAoVGymOkL3FwiMxfEt1V24qxnAWiO8I66G3zlU0ij8/edit?usp=sharing), although it should technically be able to support other BrawlEx builds as well.
- **(OPTIONAL)** The latest version of [QuickLava's Kirby Hat Manager](https://github.com/QuickLava/lavaKirbyHatManager). You will want to ensure this is installed in your build's root folder (should be in the same directory as the /pf/ folder). **This is necessary if you want Kirby hats to function correctly on P+ EX builds.**
- **(OPTIONAL)** The latest version of [QuickLava's fork of the P+ EX code menu](https://github.com/QuickLava/PowerPC-Assembly-Functions). You will want to ensure this is installed in your build's root folder (should be in the same directory as the /pf/ folder). **This is necessary if you want your character added to the code menu.**
- **(OPTIONAL)** The latest version of [QuickLava's Sawnd porting utility](https://github.com/QuickLava/lavaSawndPortingUtility). This can be anywhere on your computer. **This is necessary if you want to be able to change soundbank IDs in the event of a conflict.**
- **(OPTIONAL)** The latest version of Codes' "Porting_Tools.zip", which is linked in the [official BrawlEx Guide for P+ EX](https://docs.google.com/document/d/1ZoL_qDcwUpUXg82cKaUp-6D_AcfpFctoW6GXFY74_0k/edit#). This can be anywhere on your computer. **This is necessary if you want to be able to change soundbank IDs in the event of a conflict.**

## Setup
For initial installation, you should download the release manually and extract the contents to your BrawlCrate installation's "BrawlAPI" folder. After initial installation, you can set this repo as a subscription in BrawlCrate by navigating to Tools > Settings > Updater, clicking "Manage Subscriptions", and pasting this link: https://github.com/squidgy617/BrawlInstallerPlugins. If you set this up in BrawlCrate, the plugins will update automatically when you launch BrawlCrate.

**NOTE:** It is **_strongly recommended_** that you back up your build's files before installing mods with these plugins. While the plugins try to do everything without creating issues in your build, I cannot guarantee you will not run into issues, especially if you configure your settings incorrectly. I recommend setting up a git repository for your build [like this template](https://github.com/jlambert360/PPlus-Build-Template) for an easy method of source control.

# Plugins

Each plugin can be accessed from the Plugins menu in BrawlCrate by hovering over the "BrawlInstaller Plugins" option. Plugins may prompt the user for input. When plugins prompt the user to enter IDs such as fighter IDs or cosmetic IDs, these IDs can almost always be entered as either a hex value (e.g. "0x21") or an integer value (e.g. "33") - the plugins will convert them as needed.

On first run of any plugin, the user will be prompted to [configure their settings](https://github.com/squidgy617/BrawlInstallerPlugins/edit/master/README.md#configure-settings) if they have not done so already.

## Configure Settings
**Usage:** Plugins menu > BrawlInstaller Plugins > Configure Settings

This plugin prompts the user for input on various settings that are used by all of the plugins in this suite. Users should respond to prompts to the best of their knowledge. If the user is tasked with entering an ID, typically they may enter it in either hexadecimal (e.g. "0x21") or decimal (e.g. "33") format. After setting configuration is complete, a settings.ini file will be created in the "BrawlInstaller Resources" folder in the BrawlCrate directory.

For a detailed breakdown of the settings configured by this plugin, see the section on the [settings.ini](https://github.com/squidgy617/BrawlInstallerPlugins/edit/master/README.md#settingsini) file.

## Install Character
**Usage:** Plugins menu > BrawlInstaller Plugins > Install Character

This plugin allows you to select the files for a Brawl character packaged in a .zip file and automatically performs all the necessary work to add the character to your build. It is primarily designed for installing brand-new characters to a build, but it also attempts to resolve issues if you attempt to overwrite an existing character within a build as well.

When used, the plugin will first prompt you to select a .zip file of your character package. It will then prompt you to enter a fighter ID followed by a cosmetic ID. If the fighter comes with a franchise icon, it will also ask if you wish to install it and prompt you for a franchise icon ID if you elect to do so. If the user elects not to install a franchise icon, they may enter an alternate franchise icon ID for the fighter to use instead. If the fighter comes with a victory theme, it will also ask if you wish to install it and, if you elect not to, it will ask if you wish to enter an alternative victory theme ID. All IDs can be entered in either hexadecimal (e.g. "0x21") or decimal (e.g. "33") format.

If an existing fighter ID is input, the user will be prompted to either overwrite the existing fighter files or enter another fighter ID. If existing fighter files are overwritten, the plugin will attempt to remove files associated with that fighter ID before installing, though it will not remove existing cosmetics.

If an existing cosmetic ID is input, the user will be prompted to either overwrite the existing cosmetics or enter another cosmetic ID. If existing cosmetics are overwritten, the plugin will attempt to remove all cosmetics associated with that ID before installing.

If the fighter has the same internal name as an existing fighter, the user will be prompted to either overwrite the files or input a different fighter name. If files are overwritten, the plugin will remove the old files and replace them with the contents of the character package.

If the fighter has the same soundbank ID as one that already exists in the build and you have QuickLava's Sawnd porting utility and Codes' porting tools, you will be prompted to change the soundbank ID for the fighter, in which case you will want to enter the soundbank ID as it would appear in your fighter's config file. If you elect not to do this, the old soundbank will be overwritten. If you do not have these, tools, you may only choose to overwrite, or else installation will be aborted.

After the initial setup is finished, the plugin will install the character's files based on the user's [configured settings](https://github.com/squidgy617/BrawlInstallerPlugins/edit/master/README.md#configure-settings). Files will be moved to the appropriate destinations in the user's build and modifications will be made to both the fighter files and build files as necessary to add the character to the roster. The fighter will automatically be added to the end of the character select screen if the user's build has a CSSRoster.dat.

If the user has QuickLava's Kirby Hat manager installed, the plugin will add an entry (or modify an existing entry if one exists for the supplied ID) to the EX_KirbyHats.txt file and run the Kirby Hat manager.

If the user has QuickLava's Code Menu fork installed, the plugin will add an entry (or modify an existing entry if one exists for the supplied ID) to the EX_Characters.txt file and run the code menu .exe.

Once fighter installation has completed, the user will receive a message indicating a successful installation, and then they may use their updated build as they please.

## Uninstall Character
**Usage:** Plugins menu > BrawlInstaller Plugins > Uninstall Character

This plugin allows you to enter a fighter ID for a character you wish to uninstall from your build. Like other prompts, the fighter ID can be entered in either hexadecimal (e.g. "0x21") or decimal (e.g. "33") format. The user will also be prompted on whether or not they want to uninstall the fighter's victory theme or franchise icon.

After the user has input their selections, the plugin will attempt to remove all existing files and cosmetics associated with the supplied fighter ID. It will also remove the fighter's entry from CSSRoster.dat if the user's build uses it.

If the user has QuickLava's Kirby Hat manager installed, the plugin will remove any existing entry from EX_KirbyHats.txt and then run the hat manager.

If the user has QuickLava's Code Menu fork installed, the plugin will remove any existing entry from EX_Characters.txt and then run the code menu .exe.

After the fighter is successfully uninstalled, the user will receive a message indicating such, and then they may use their updated build as they please.

## Package Character
**Usage:** Plugins menu > BrawlInstaller Plugins > Package Character

This plugin allows you to package a character into a .zip file with the correct directory structure to be installed via the "Install Character" plugin. When run, the plugin will give the user various prompts to browse their computer for files for their character such as cosmetics, EX configs, and other character files. If the user does not have the files requested, they can simply select "Cancel" instead of choosing a file, but users should bear in mind that some files, such as EX configs and fighter files, are essential and not supplying them will make the character package not work properly.

All images packaged with the character should be the size they are expected to be in-game, with the exception of franchise icons which will be resized upon character installation.

While the character installer plugin attempts to modify files as needed, users should ensure their .pac files are named using the same name as what is listed in the fighter's FighterConfig file.

For CSPs and stock icons, users will be repeatedly prompted to select files. Each set of CSPs or stock icons selected is considered a group and will be color smashed on installation. Once the user has selected all of the image groups they want they may simply respond "No" to the onscreen prompt to move on to the next section.

If the user has Kirby hat files to package with the fighter, they will be prompted to enter a fighter ID for the Kirby hat. This is the fighter ID that the modded Kirby hat is cloned from, so for example if the Kirby hat is based on Lucario's, it should use Lucario's fighter ID of 0x21. As with most ID fields, this prompt accepts both hexadecimal and decimal formats.

After the user has selected all files, they will be prompted to select an output directory and to enter a name for the file. The character package will be output to the directory chosen by the user as "{name}.zip", where {name} is the name the user entered. They will then receive a message indicated successful package creation, and this .zip can be used with the "Install Character" plugin to install the character to a build.

# settings.ini

After [configuring settings](https://github.com/squidgy617/BrawlInstallerPlugins/edit/master/README.md#configure-settings), a settings.ini file is generated that the BrawlInstaller plugins use to determine various behaviors.

The settings currently supported by the BrawlInstaller plugins are as follows:
- **rspLoading** - [*Values: true, false*] : Whether or not the build uses RSP (result-screen portrait) loading. If this is set to `true`, character select portraits will not be installed to the build's `sc_selcharacter.pac`, and will instead only be installed as result-screen portraits in `/pf/menu/common/char_bust_tex/`.
- **cssIconStyle** - [*Values: P+, PM, REMIX, vBrawl*] : The style of CSS icon that will be installed into your build. When installing a character package, the plugin will attempt to find a CSS icon that matches your preferred style. If one cannot be found, CSS icon installation will be skipped and must be performed manually.
- **bpStyle** - [*Values: vBrawl, REMIX*] : The style of battle portrait that will be installed into your build. When installing a character package, the plugin will attempt to find a folder of battle portraits that matches your preferred style. If such a folder cannot be found, the plugin defaults to vBrawl battle portraits.
- **installPortraitNames** - [*Values: true, false*] : Whether or not character selection portrait names should be installed when installing a character package. These are the names displayed over the character's portrait when they are selectd on the character select screen. If this is set to true, portrait names will be installed, otherwise they will not.
- **portraitNameStyle** - [*Values: PM, vBrawl*] : The style of portrait name to install when installing character packages. When installing a character package, the plugin will attempt to find a portrait name that matches your preferred style. If one cannot be found, portrait name installation will be skipped and must be performend manually.
- **franchiseIconSizeCSS** - [*Values: any integer*] : The size in pixels of franchise icons on the character select screen.
- **installStocksToCSS** - [*Values: true, false*] : Whether or not stock icons should be installed to `sc_selcharacter.pac`.
- **installStocksToInfo** - [*Values: true, false*] : Whether or not stock icons should be installed to `info.pac`.
- **installStockIconsToResult** - [*Values : true, false*] : Whether or not stock icons should be installed to `STGRESULT.pac`.
- **installStocksToSTockFaceTex** - [*Values : true, false*] : Whether or not stock icons should be installed to `StockFaceTex.brres`.
- **installStocksToSSS** - [*Values : true, false*] : Whether or not stock icons should be installed to `sc_selmap.pac`.
- **fiftyCostumeCode** - [*Values : true, false*] : Whether or not the build uses the fifty costume code. If set to `true`, cosmetics will be named to match the naming scheme supported by the fifty costume code, otherwise they will be named according to vanilla Brawl standards.
- **kirbyHatExe** - [*Values : a .exe path*] : The direct path to the .exe file for QuickLava's Kirby hat manager to run when installing Kirby hats.
- **defaultKirbyHat** - [*Values : fighter ID in hex format, none*] : The hexadecimal fighter ID that Kirby hats should default to in the event that a valid Kirby hat cannot be found. If set to a hexadecimal value, this ID will be used to automatically set up a Kirby hat based on the one that corresponds to that fighter (e.g. a value of 0x21 will cause packages that are missing Kirby hats to generate a new Kirby hat that is a copy of Lucario's). If set to `none`, Kirby hat installation will be skipped entirely and the fighter's Kirby hat value will be set to "None".
- **assemblyFunctionsExe** - [*Values : a .exe path*] : The direct path to the .exe file for QuickLava's Code Menu to run when adding a character to the code menu.
- **sawndReplaceExe** - [*Values : a .exe path*] : The direct path to the .exe file for QuickLava's Sawnd Porting tool to run when changing soundbank IDs.
- **sfxChangeExe** - [*Values : a .exe path*] : The direct path to the .exe file for Codes' sfxchange.exe tool to run when changing soundbank IDs.
- **soundbankStyle** - [*Values : hex, dec*] : The naming convention used for soundbanks in your build. The plugin will use this setting to determine how soundbanks imported into your build should be named. If it is set to `hex`, soundbanks will be named after their soundbank ID in hexadecimal format. If set to `dec`, soundbanks will be named after their soundbank ID in decimal format.
- **addSevenToSoundbankName** - [*Values : true, false*] : Whether 7 should be added to soundbank IDs when naming soundbanks. If this is set to `true`, all soundbanks will be named as the ID provided + 7. If set to `false`, all soundbanks will be named only as the ID provided.
- **addSevenToSoundBankIds** - [*Values : true, false*] : Whether 7 should be added to SFX IDs within soundbanks when converting them using QuickLava and Codes' tools. If this is set to `true`, soundbank IDs passed to QuickLava's tool will have 7 added to them. If this is set to `false`, soundbank IDs will be passed to QuickLava's tool unmodified.
- **installVictoryThemes** - [*Values : true, false*] : Whether victory themes should be installed to the build or not when installing character packages. This primarily exists in case of builds that do not use the P+ tracklist system. If this is set to `false`, victory themes will not be installed.
- **useCssRoster** - [*Values : true, false*] : Whether or not the build uses CSSRoster.dat to determine the roster available on the character select screen. If this is set to `true`, CSSRoster.dat will be updated to display newly installed character packages. If set to `false`, characters will not be added to the CSS.
