# BrawlInstaller Plugins

[**DEMO VIDEO**](https://youtu.be/V6-cjuVhC80) (from an older version)

A BrawlCrate plugin suite for easy installation of Brawl mods into BrawlEX builds. Currently supports automatic installation of entire characters, including their cosmetics, as long as they are packaged in a .zip file with the correct structure.

This tool was made possible by:
- Soopercool101, Kryal, BlackJax96, and libertyernie for BrawlLib, BrawlBox, and BrawlCrate. Extra thanks to Soopercool101 for making additions to BrawlCrate to support features needed for the BrawlInstaller plugins.
- markymawk, for their basic guide to writing plug-ins and for their plug-ins which served as a great learning resource.
- Kapedani and Hatyaro, for helping with some coding challenges.
- QuickLava and codes, for the various tools they created that these plugins are able to interact with.
- KingJigglypuff for providing detailed information on currently supported non-Ex modules.
- CaliKingz01, who provided the PSA for X to use as an example character package.
- Shy, who created the cosmetics used for X.
- Project+ EX and all the documentation provided and linked within KingJigglypuff's [P+Ex Release Document](https://docs.google.com/document/d/1mAoVGymOkL3FwiMxfEt1V24qxnAWiO8I66G3zlU0ij8/edit?usp=sharing). Learning these processes thoroughly was necessary for creating these plugins.
- The Brawl modding community and [Custom Brawl Modding discord](https://discord.gg/GbxJhbv), for being a great source of knowledge on all things Brawl-modding.

Currently this plugin performs all the necessary installation to get an EX character fully working in Versus mode. Characters will most likely work in other modes such as Classic, All-Star, etc. but may have broken cosmetics. Full support for modes outside of Versus Mode will be implemented in a future update.

If you find any bugs or issues with the plugins, please submit them as an issue here on GitHub or message me about it directly on discord @ Squidgy#9561

# Installation
## Prerequisites
In order for these plugins to function correctly, you will need a few things:
- The latest version of [BrawlCrate](https://github.com/soopercool101/BrawlCrate). You should also ensure you have your build path set to your build's root folder by navigating to Tools > Settings > General and modifying the "Default Build Path" there.
- The latest version of Python. You can download this at [python.org](https://www.python.org/). Also ensure your Python path is set within BrawlCrate by navigating to Tools > Settings > BrawlAPI and setting the "Installation Path" field under "Python".
- A BrawlEx build of Super Smash Bros. Brawl. It is strongly recommended to use these plugins with a build of [Project+ EX](https://docs.google.com/document/d/1mAoVGymOkL3FwiMxfEt1V24qxnAWiO8I66G3zlU0ij8/edit?usp=sharing), although it should technically be able to support other BrawlEx builds as well.
- **(OPTIONAL)** The latest version of [QuickLava's Kirby Hat Manager](https://github.com/QuickLava/lavaKirbyHatManager). You will want to ensure this is installed in your build's root folder (should be in the same directory as the /pf/ folder). **This is necessary if you want Kirby hats to function correctly on P+ EX builds.**
- **(OPTIONAL)** The latest version of [QuickLava's fork of the P+ EX code menu](https://github.com/QuickLava/PowerPC-Assembly-Functions). You will want to ensure this is installed in your build's root folder (should be in the same directory as the /pf/ folder). **This is necessary if you want your character added to the code menu.**
- **(OPTIONAL)** The latest version of [QuickLava's Sawnd ID Replace Assist](https://github.com/QuickLava/lavaSawndIDReplaceAssist). This can be anywhere on your computer. **This is necessary if you want to be able to change soundbank IDs in the event of a conflict.**
- **(OPTIONAL)** The latest version of Codes' "Porting_Tools.zip", which is linked in the [official BrawlEx Guide for P+ EX](https://docs.google.com/document/d/1ZoL_qDcwUpUXg82cKaUp-6D_AcfpFctoW6GXFY74_0k/edit#). This can be anywhere on your computer. **This is necessary if you want to be able to change soundbank IDs or Effect.pac IDs in the event of a conflict.**
- If you're trying to use the Install Character plugin, you'll need a proper character package .zip file. You can find an example package using CaliKingz01's RockmanX PSA and Shy's cosmetics [here](https://github.com/squidgy617/BrawlInstallerPlugins#template-packages).

## Setup
For initial installation, you can set this repo as a subscription in BrawlCrate by navigating to Tools > Settings > Updater, clicking "Manage Subscriptions", and pasting this link: https://github.com/squidgy617/BrawlInstallerPlugins. If you set this up in BrawlCrate, the plugins will update automatically when you launch BrawlCrate. Alternatively, you can download the release manually and extract the contents to your BrawlCrate installation's "BrawlAPI" folder.

**NOTE:** While the plugins create backups of your files during execution, I do recommend that you back up your build's files before installing mods with these plugins. While the plugins try to do everything without creating issues in your build, they do not clean up loose files added and I cannot guarantee you will not run into issues, especially if you configure your settings incorrectly. I recommend setting up a git repository for your build [like this template](https://github.com/jlambert360/PPlus-Build-Template) for an easy method of source control. With the automatic backup functionality, this is less necessary, but still a good idea.

# Quick Start Guide

**LINK**: [Newbie's Guide to the BrawlInstaller Plugins](https://docs.google.com/document/d/1RcAqzS9IHzQcrtHKspC7qbBB0he9_H69GB6BGLXduJw/edit?usp=sharing)

If you're just looking to get started in using these plugins to package and install character mods, you can use this guide to get started. It's designed to hopefully get both newbies to modding, as well as people who are just new to the plugins, get started with creating and installing character packages.

# Character Packages

The Install Character plugin works by extracting files from a "Character Package", a .zip file containing the fighter's files, cosmetics, etc. with a particular directory structure.

If you wish to add a character with the installer plugin, the character **must** be packaged in the correct way. This can be done manually (recommended that you use one of [these templates](https://github.com/squidgy617/BrawlInstallerPlugins#template-packages)) or by using the [Package Character](
https://github.com/squidgy617/BrawlInstallerPlugins#package-character) plugin in this suite.

Ideally, mod creators should create good character packages for you to use with this plugin, but if no package exists, anybody can create one using the previously mentioned plugin or templates.

## Template Packages
**DOWNLOAD:** [Rockman X (by CaliKingz01) Example Package](https://www.mediafire.com/file/qnx8p14ivsb3rxo/RockmanX_by_CaliKingz01.zip/file)

**DOWNLOAD:** [Empty Template Package](https://www.mediafire.com/file/xd1212mwl5aq6tk/Template.zip/file)

These sample packages give an example of what a proper character package should look like. In both examples, every folder contains text files with additional instructions on how they should be used.

# Plugins

Each plugin can be accessed from the Plugins menu in BrawlCrate by hovering over the "BrawlInstaller Plugins" option. Plugins may prompt the user for input. When plugins prompt the user to enter IDs such as fighter IDs or cosmetic IDs, these IDs can almost always be entered as either a hex value (e.g. "0x21") or an integer value (e.g. "33") - the plugins will convert them as needed.

On first run of any plugin, the user will be prompted to [configure their settings](https://github.com/squidgy617/BrawlInstallerPlugins#configure-settings) if they have not done so already.

All plugins attempt to create backups of files that they modify, replace, or delete. These backups are stored in `/Backups/` in the BrawlCrate root directory. The plugins will also create a log of the work they are doing. The most recent log file created by one of the plugins can be found in `/Logs/log.txt` in the BrawlCrate root folder.

## Configure Settings
**Usage:** Plugins menu > BrawlInstaller Plugins > Configure Settings

This plugin prompts the user for input on various settings that are used by all of the plugins in this suite. Users should respond to prompts to the best of their knowledge. If the user is tasked with entering an ID, typically they may enter it in either hexadecimal (e.g. "0x21") or decimal (e.g. "33") format. After setting configuration is complete, a settings.ini file will be created in the "Resources/BrawlInstaller" folder in the BrawlCrate directory.

For a detailed breakdown of the settings configured by this plugin, see the section on the [settings.ini](https://github.com/squidgy617/BrawlInstallerPlugins#settingsini) file.

## Install Character
**Usage:** Plugins menu > BrawlInstaller Plugins > Install Character

This plugin allows you to select the files for a Brawl character packaged in a .zip file and automatically performs all the necessary work to add the character to your build. It is primarily designed for installing brand-new characters to a build, but it also attempts to resolve issues if you attempt to overwrite an existing character within a build as well.

When used, the plugin will first prompt you to select a .zip file of your character package. It will then prompt you to enter a fighter ID followed by a cosmetic ID. If the fighter comes with a franchise icon, it will also ask if you wish to install it and prompt you for a franchise icon ID if you elect to do so. If the user elects not to install a franchise icon, they may enter an alternate franchise icon ID for the fighter to use instead. If the fighter comes with a victory theme, it will also ask if you wish to install it and, if you elect not to, it will ask if you wish to enter an alternative victory theme ID. All IDs can be entered in either hexadecimal (e.g. "0x21") or decimal (e.g. "33") format.

If an existing fighter ID is input, the user will be prompted to either overwrite the existing fighter files or enter another fighter ID. If existing fighter files are overwritten, the plugin will attempt to remove files associated with that fighter ID before installing, though it will not remove existing cosmetics. This should only be used when reinstalling the same character over a specific ID - if you are trying to remove another character and replace them, you should use the "Uninstall Character" plugin first instead. Overwriting an existing character will not account for any redirects in their config files.

If an existing cosmetic ID is input, the user will be prompted to either overwrite the existing cosmetics or enter another cosmetic ID. If existing cosmetics are overwritten, the plugin will attempt to remove all cosmetics associated with that ID before installing.

If the fighter has the same internal name as an existing fighter, the user will be prompted to either overwrite the files or input a different fighter name. If files are overwritten, the plugin will remove the old files and replace them with the contents of the character package.

If the fighter has the same soundbank ID as one that already exists in the build and you have QuickLava's Sawnd ID Replace Assist and Codes' porting tools, you will be prompted to change the soundbank ID for the fighter, in which case you will want to enter the soundbank ID as it would appear in your fighter's config file. If you elect not to do this, the old soundbank will be overwritten. If you do not have these tools, you may only choose to overwrite, or else installation will be aborted.

If the fighter has the same Effect.pac ID as one that already exists in the build and you have Codes' porting tools, you will be prompted to change the Effect.pac ID for the fighter, in which case you will want to enter the Effect.pac ID as it would appear in the fighter's moveset (e.g. "0x2A" as it would appear in "ef_custom2A"). If you elect not to do this, the old Effect.pac ID will continue to be used, which could create conflicts unless you are just reinstalling an existing character. If you do not have these tools, this part of the process will be skipped and the old Effect.pac ID will always be used.

After the initial setup is finished, the plugin will install the character's files based on the user's [configured settings](https://github.com/squidgy617/BrawlInstallerPlugins#configure-settings). Files will be moved to the appropriate destinations in the user's build and modifications will be made to both the fighter files and build files as necessary to add the character to the roster. The fighter will automatically be added to the end of the character select screen if the user's build has a CSSRoster.dat. Cosmetic files such as stock icons and CSPs are imported in alphabetical order, so mod authors should ensure their files are named appropriately.

The installer primarily supports Ex modules currently, but also supports a few other modules, including: Lucario's module, Marth's module, Sonic's module, and Pit's patched Project M module.

If the user has QuickLava's Kirby Hat manager installed, the plugin will add an entry (or modify an existing entry if one exists for the supplied ID) to the EX_KirbyHats.txt file and run the Kirby Hat manager.

If the user has QuickLava's Code Menu fork installed, the plugin will add an entry (or modify an existing entry if one exists for the supplied ID) to the EX_Characters.txt file and run the code menu .exe.

Once fighter installation has completed, the user will receive a message indicating a successful installation, and then they may use their updated build as they please.

The plugin attempts to back up any files in your build before modifying, replacing, or deleting them, and these backups are then stored in the `/Backups/` directory in your BrawlCrate root folder. If an error occurs during execution, an error message is displayed and the backups are restored automatically. However, any files that were *added* to the build during execution are not cleaned up, so keep that in mind.

## Uninstall Character
**Usage:** Plugins menu > BrawlInstaller Plugins > Uninstall Character

This plugin allows you to enter a fighter ID for a character you wish to uninstall from your build. Like other prompts, the fighter ID can be entered in either hexadecimal (e.g. "0x21") or decimal (e.g. "33") format. The user will also be prompted on whether or not they want to uninstall the fighter's victory theme or franchise icon.

After the user has input their selections, the plugin will attempt to remove all existing files and cosmetics associated with the supplied fighter ID. It will also remove the fighter's entry from CSSRoster.dat if the user's build uses it.

If the user has QuickLava's Kirby Hat manager installed, the plugin will remove any existing entry from EX_KirbyHats.txt and then run the hat manager.

If the user has QuickLava's Code Menu fork installed, the plugin will remove any existing entry from EX_Characters.txt and then run the code menu .exe.

After the fighter is successfully uninstalled, the user will receive a message indicating such, and then they may use their updated build as they please.

The plugin attempts to back up any files in your build before modifying, replacing, or deleting them, and these backups are then stored in the `/Backups/` directory in your BrawlCrate root folder. If an error occurs during execution, an error message is displayed and the backups are restored automatically. However, any files that were *added* to the build during execution are not cleaned up, so keep that in mind.

## Package Character
**Usage:** Plugins menu > BrawlInstaller Plugins > Package Character

This plugin allows you to package a character into a .zip file with the correct directory structure to be installed via the "Install Character" plugin. When run, the plugin will give the user various prompts to browse their computer for files for their character such as cosmetics, EX configs, and other character files. If the user does not have the files requested, they can simply select "Cancel" instead of choosing a file, but users should bear in mind that some files, such as EX configs and fighter files, are essential and not supplying them will make the character package not work properly.

All images packaged with the character should be the size they are expected to be in-game, with the exception of franchise icons which will be resized upon character installation.

When selecting multiple files, they will be read into the plugin in the order that you select them in. The plugin will automatically rename cosmetic files such as stock icons, battle portraits, and CSPs to ensure they are in alphabetical order so the installer plugins will order them correctly.

While the character installer plugin attempts to modify files as needed, users should ensure their .pac files are named using the same name as what is listed in the fighter's FighterConfig file.

For CSPs and stock icons, users will be repeatedly prompted to select files. Each set of CSPs or stock icons selected is considered a group and will be color smashed on installation. Once the user has selected all of the image groups they want they may simply respond "No" to the onscreen prompt to move on to the next section.

If the user has Kirby hat files to package with the fighter, they will be prompted to enter a fighter ID for the Kirby hat. This is the fighter ID that the modded Kirby hat is cloned from, so for example if the Kirby hat is based on Lucario's, it should use Lucario's fighter ID of 0x21. As with most ID fields, this prompt accepts both hexadecimal and decimal formats.

After the user has selected all files, they will be prompted to select an output directory and to enter a name for the file. The character package will be output to the directory chosen by the user as "{name}.zip", where {name} is the name the user entered. They will then receive a message indicated successful package creation, and this .zip can be used with the "Install Character" plugin to install the character to a build.

## Output Fighter Info To Text
**Usage:** Plugins menu > BrawlInstaller Plugins > Output Fighter Info To Text

This plugin will iterate through all of the EX configs in your build and print the fighter ID, name, cosmetic ID, franchise icon ID, soundbank ID, and victory theme ID of each fighter found to a fighter_info.txt file located in your `/BrawlAPI/Resources/BrawlInstaller/` directory in the BrawlCrate root folder. This can be useful if you need a reference for what IDs are available.

All IDs printed are in decimal format.

## Restore Backup

This plugin allows you to restore backups created when running the other plugins, such as installing or uninstalling characters. The plugins attempt to create backups of any file they modify, delete, or replace during execution, and these backups can be found in the `/Backups/` folder in your BrawlCrate root directory. The last nine backups are stored - older backups are deleted when one of the plugins attempt to back something up.

When this plulgin is run, it will first check if any backups exist. If they do not, it simply displays a message and ends execution. If backups are found, the user will be displayed a list of options and prompted to enter a number associated with one of the backups in the list. Whichever backup the user selects will be restored to the user's build by copying every file within to it's respective directory into the build. Once execution completes, a message will be displayed indicating such.

# settings.ini

After [configuring settings](https://github.com/squidgy617/BrawlInstallerPlugins#configure-settings), a settings.ini file is generated that the BrawlInstaller plugins use to determine various behaviors.

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
- **gfxChangeExe** - [*Values : a .exe path*] : The direct path to the .exe file for Codes' gfxchange.exe tool to run when changing Effect.pac IDs. This should be in the same directory as Codes' tracechange.exe, which will also be run in the event of Effect.pac ID conflicts.
- **installBPNames** - [*Values : true, false*] : Whether or not battle portrait nameplates should be installed to `info.pac`.

# Planned Features
These are some features that are planned for eventual implementation in the plugin suite, if they are feasible.
- Importing necessary files for single player modes such as Classic, All-Star, Home Run Contest, etc.
- Automatic updating of P+ EX codes that require character IDs
- Allow redirection of EX config IDs
- Automatic HD texture renaming and importing for Dolphin (hopefully)
- Support for Subspace Emissary EX
- Costume Installer plugin
- Stage Installer plugin
- Plugin to extract character packages from an existing build
