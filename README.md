# BrawlInstaller Plugins

[**DEMO VIDEO**](https://youtu.be/V6-cjuVhC80) (from an older version)

A BrawlCrate plugin suite for easy installation of Brawl mods into BrawlEX builds. Currently supports automatic installation of entire characters, including their cosmetics, as long as they are packaged in a .zip file with the correct structure.

This tool was made possible by:
- Soopercool101, Kryal, BlackJax96, and libertyernie for BrawlLib, BrawlBox, and BrawlCrate. Extra thanks to Soopercool101 for making additions to BrawlCrate to support features needed for the BrawlInstaller plugins.
- markymawk, for their basic guide to writing plug-ins and for their plug-ins which served as a great learning resource.
- Kapedani, for providing files and assistance with Subspace Emissary Ex implementation.
- QuickLava and codes, for the various tools they created that these plugins are able to interact with.
- KingJigglypuff for providing detailed information on currently supported non-Ex modules.
- CaliKingz01, who provided the PSA for X to use as an example character package.
- Shy, who created the cosmetics used for X.
- Hatyaro, for helping with some coding challenges.
- Project+ EX and all the documentation provided and linked within KingJigglypuff's [P+Ex Release Document](https://docs.google.com/document/d/1mAoVGymOkL3FwiMxfEt1V24qxnAWiO8I66G3zlU0ij8/edit?usp=sharing). Learning these processes thoroughly was necessary for creating these plugins.
- The Brawl modding community and [Custom Brawl Modding discord](https://discord.gg/GbxJhbv), for being a great source of knowledge on all things Brawl-modding.

Currently this plugin performs all the necessary installation to get an EX character fully playable in all modes, including Subspace Emissary, so long as your build supports Subspace Emissary Ex.

If you find any bugs or issues with the plugins, please submit them as an issue here on GitHub or message me about it directly on discord @ Squidgy#9561

## Features
- Install or uninstall fully playable characters and costumes into a build of Super Smash Bros. Brawl in just a few clicks.
- Extract characters from a build as fully installable packages - either individually or en masse.
- Installed characters playable in all modes, including support for [Subspace Emissary Ex](https://github.com/Sammi-Husky/BrawlEx/releases).
- Automatic detection and handling of conflicts on fighter IDs, names, soundbanks, Effect.pac IDs, and more.
- Numerous settings to support many different kinds of builds.
- Tools to easily list IDs already in use in a build.
- Automatic backup and restore features in case of unintended results.
- Logging features to help diagnose issues when they are encountered.
- Support for Ex modules and several non-Ex modules (Lucario, Marth, Sonic, and Pit's patched PM module).

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
- **(OPTIONAL)** The latest version of [Kapedani's Subspace Emissary Ex](https://github.com/Sammi-Husky/BrawlEx/releases). This can be installed over your P+Ex build's root directory. **This is only necessary if you are not on the latest P+Ex version and would like to install your characters into Subspace Emissary mode.** If you want additional CSS slots for SSE, you can also download a basic expanded CSS [here](https://www.mediafire.com/file/b509fjbg3l3buqj/Expanded_SSE_CSS.zip/file).
- If you're trying to use the Install Character plugin, you'll need a proper character package .zip file. You can find an example package using CaliKingz01's RockmanX PSA and Shy's cosmetics [here](https://github.com/squidgy617/BrawlInstallerPlugins#template-packages).

## Setup
For initial installation, you can set this repo as a subscription in BrawlCrate by navigating to Tools > Settings > Updater, clicking "Manage Subscriptions", and pasting this link: https://github.com/squidgy617/BrawlInstallerPlugins. If you set this up in BrawlCrate, the plugins will update automatically when you launch BrawlCrate. Alternatively, you can download the release manually and extract the contents to your BrawlCrate installation's "BrawlAPI" folder.

The plugins create backups of your files during execution, but they do not clean up loose files added and I cannot guarantee you will not run into issues, especially if you configure your settings incorrectly. While loose files shouldn't cause an issue, if you want an extra safety net, I recommend setting up a git repository for your build [like this template](https://github.com/jlambert360/PPlus-Build-Template) for an easy method of source control. With the automatic backup functionality, this is not really necessary, but still a good idea.

# Quick Start Guide

**LINK**: [Newbie's Guide to the BrawlInstaller Plugins](https://docs.google.com/document/d/1RcAqzS9IHzQcrtHKspC7qbBB0he9_H69GB6BGLXduJw/edit?usp=sharing)

If you're just looking to get started in using these plugins to package and install character mods, you can use this guide to get started. It's designed to hopefully get both newbies to modding, as well as people who are just new to the plugins, get started with creating and installing character packages.

# Character Packages

The Install Character plugin works by extracting files from a "Character Package", a .zip file containing the fighter's files, cosmetics, etc. with a particular directory structure.

If you wish to add a character with the installer plugin, the character **must** be packaged in the correct way. This can be done manually (recommended that you use one of [these templates](https://github.com/squidgy617/BrawlInstallerPlugins#template-packages)) or by using the [Package Character](
https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Plugins#package-character) plugin in this suite. Character packages can also be extracted from a build using the [Extract Character](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Plugins#extract-character) plugin.

Ideally, mod creators should create good character packages for you to use with this plugin, but if no package exists, anybody can create one using the previously mentioned plugin or templates.

Character packages can also come with a FighterSettings.txt file that declares various parameters for the fighter, usually for modifying Gecko codes. See the [FighterSettings.txt](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Character-Packages#fightersettingstxt) section for more details.

## Template Packages
**DOWNLOAD:** [Rockman X (by CaliKingz01) Example Package](https://www.mediafire.com/file/qnx8p14ivsb3rxo/RockmanX_by_CaliKingz01.zip/file)

**DOWNLOAD:** [Empty Template Package](https://www.mediafire.com/file/xd1212mwl5aq6tk/Template.zip/file)

These sample packages give an example of what a proper character package should look like. In both examples, every folder contains text files with additional instructions on how they should be used.

## [FighterSettings.txt](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Character-Packages#fightersettingstxt)
Character packages can include a text file specifying certain parameters to use during installation. Click the above link to see detailed documentation on these parameters.

# [Plugins](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Plugins)

Click the above link to see detailed documentation on all of the plugins included in this suite.

# [settings.ini](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Settings)

BrawlInstaller supports a wide variety of different settings that enable users to customize it to fit their build. Click the above link to see detailed documentation on all of these settings.

# FAQ
<details>
<summary><b>There are errors/crashes when my fighter is in a battle with Kirby.</b></summary>

The first and most common cause of this issue is not setting up QuickLava's Kirby Hat Manager correctly. Ensure it is installed into your build folder and that you have moved the required files into the folder for the application.

Assuming you have QuickLava's Kirby Hat Manager set up correctly, this is not something BrawlInstaller can account for, but is actually a known issue with the KirbyHatEx system. The system is still not entirely stable, and not everything is known about how the hats interact with different fighters and IDs. Most likely, the cause is either an incompatibility with your character, your chosen ID, the chosen base fighter ID for the Kirby hat, or a combination of the three. If you run into Kirby-related issues, try uninstalling your character and reinstalling them to a different fighter ID or installing them with a different base fighter ID for their Kirby hat.
</details>

<details>
<summary><b>I added my character but don't see them on the character select screen/SSE character select.</b></summary>

This usually means one of two things - one, your build is not configured to use CSSRoster.dat, or two, you ran out of animated CSS slots in your build. If you're using P+Ex, the roster will only automatically expand up to a certain number of slots, and other builds may not even have the roster automatically expanding. In such a case, you'll have to expand it manually, which can be done in a similar manner to the steps outlined in [this guide](https://docs.google.com/document/d/1NN7X98xdoatzcnKabUq6TIhZrPTda84RmFp1La16GiQ/edit).

For your SSE CSS, you can either follow the steps outlined in [this guide](https://docs.google.com/document/d/1bwzccf8lhwVu3ZAv8oLBXM3qSXODmbu1kqIv7obosto/edit) (see sections Altering the Number of CSS Icons per Row and Editing the Subspace CSS Animation) or you can download a very basic expanded SSE CSS [here](https://www.mediafire.com/file/b509fjbg3l3buqj/Expanded_SSE_CSS.zip/file). This expanded CSS supports up to 72 slots.
</details>

<details>
  <summary><b>My character's costumes and portraits don't match up.</b></summary>
  
  This usually means you packaged your character incorrectly. Ensure that that the entries in the fighter's CSSSlotConfig and their cosmetics are in the correct order, and ensure that the CSSSlotConfig entries point to the right .pac files.
  
</details>

<details>
  <summary><b>I get an error about "color smashing", and/or the character portraits in game look messed up.</b></summary>
  
  This usually means you provided bad cosmetics, or you put cosmetics together in a folder when they shouldn't have been. Verify that all of your folders in the "CSPs" and "StockIcons" directories of your character package contain only cosmetics that are recolors of each other, and ensure any provided images are the right size and are color smashable.
  
</details>

# Planned Features
These are some features that are planned for eventual implementation in the plugin suite, if they are feasible.
- Automatic HD texture renaming and importing for Dolphin (hopefully)
- Stage Installer plugin
- Extract vanilla characters from builds
