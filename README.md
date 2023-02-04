# BrawlInstaller Plugins

[**DEMO VIDEO**](https://youtu.be/V6-cjuVhC80) (from an older version)

A BrawlCrate plugin suite for easy installation of Brawl mods into BrawlEX builds. Currently supports automatic installation of entire characters, including their cosmetics, as long as they are packaged in a .zip file with the correct structure.

Currently this plugin performs all the necessary installation to get an EX character fully playable in all modes, including Subspace Emissary, so long as your build supports Subspace Emissary Ex.

If you find any bugs or issues with the plugins, please submit them as an issue here on GitHub or message me about it directly on discord @ Squidgy#9561

## Features
- Install or uninstall fully playable characters and costumes into a build of Super Smash Bros. Brawl in just a few clicks.
- Add, edit, and manage stages and music for your build using intuitive forms.
- Extract characters from a build as fully installable packages - either individually or en masse.
- Installed characters playable in all modes, including support for [Subspace Emissary Ex](https://github.com/Sammi-Husky/BrawlEx/releases).
- Automatic detection and handling of conflicts on fighter IDs, names, soundbanks, Effect.pac IDs, and more.
- Numerous settings to support many different kinds of builds.
- Tools to easily list IDs already in use in a build.
- Automatic backup and restore features in case of unintended results.
- Logging features to help diagnose issues when they are encountered.
- Support for Ex modules and several non-Ex modules (Lucario, Marth, Sonic, and Pit's patched PM module).

# Installation
## Simple Installation
1. If you do not already have BrawlCrate, download and install the [latest release](https://github.com/soopercool101/BrawlCrate/releases/latest).
2. Navigate to the [latest BrawlInstaller release](https://github.com/squidgy617/BrawlInstallerPlugins/releases/latest) and download the `BrawlInstaller.Tools.Setup.exe`. Run this installer and follow the on-screen instructions.
3. In BrawlCrate, navigate to `Tools > Settings > General` and modify the `Default Build Path` to match the path you chose for the tools in step 2.
4. In BrawlCrate, navigate to `Tools > Settings > BrawlAPI` and ensure the `Installation Path` field under `Python` is set to the correct path.
5. In BrawlCrate, navigate to `Tools > Settings > Updater`, click `Manage Subscriptions`, and paste this link: `https://github.com/squidgy617/BrawlInstallerPlugins`. If you set this up in BrawlCrate, the plugins will update automatically when you launch BrawlCrate.
6. Restart BrawlCrate.

Once you have completed these steps, you are ready to begin using the BrawlInstaller plugins.

Additionally, it's recommended to set up a git repository for your build [like this template](https://github.com/jlambert360/PPlus-Build-Template) for an easy method of source control. BrawlInstaller does create automatic backups, so this is not necessary, but still recommended.

<details>

<summary><h2>Manual Installation</h2></summary>

If you would prefer to install everything used by BrawlInstaller manually, you can follow these directions.

<b>Prerequisites</b>

In order for these plugins to function correctly, you will need a few things:
- The latest version of [BrawlCrate](https://github.com/soopercool101/BrawlCrate). You should also ensure you have your build path set to your build's root folder by navigating to Tools > Settings > General and modifying the "Default Build Path" there.
- The latest version of Python. You can download this at [python.org](https://www.python.org/). Also ensure your Python path is set within BrawlCrate by navigating to Tools > Settings > BrawlAPI and setting the "Installation Path" field under "Python".
- A BrawlEx build of Super Smash Bros. Brawl. It is strongly recommended to use these plugins with a build of [Project+ EX](https://docs.google.com/document/d/1mAoVGymOkL3FwiMxfEt1V24qxnAWiO8I66G3zlU0ij8/edit?usp=sharing), although it should technically be able to support other BrawlEx builds as well.
- **(OPTIONAL)** The latest version of [QuickLava's Kirby Hat Manager](https://github.com/QuickLava/lavaKirbyHatManager). You will want to ensure this is installed in your build's root folder (should be in the same directory as the /pf/ folder). **This is necessary if you want Kirby hats to function correctly on P+ EX builds.** You do not need to download this when using a build such as REMIX which already comes with it. If you install this, you will also need the [Microsoft Visual C++ Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=52685).
- **(OPTIONAL)** The latest version of [QuickLava's fork of the P+ EX code menu](https://github.com/QuickLava/PowerPC-Assembly-Functions). You will want to ensure this is installed in your build's root folder (should be in the same directory as the /pf/ folder). **This is necessary if you want your character added to the code menu.** You do not need to download this when using a build such as REMIX which already comes with it. You also should not use this if your build is designed around a different code menu. If you install this, you will also need the [Microsoft Visual C++ Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=52685).
- **(OPTIONAL)** The latest version of [QuickLava's Sawnd ID Replace Assist](https://github.com/QuickLava/lavaSawndIDReplaceAssist). This can be anywhere on your computer. **This is necessary if you want to be able to change soundbank IDs in the event of a conflict.**
- **(OPTIONAL)** The latest version of Codes' "Porting_Tools.zip", which is linked in the [official BrawlEx Guide for P+ EX](https://docs.google.com/document/d/1ZoL_qDcwUpUXg82cKaUp-6D_AcfpFctoW6GXFY74_0k/edit#). This can be anywhere on your computer. **This is necessary if you want to be able to change soundbank IDs or Effect.pac IDs in the event of a conflict.**
- **(OPTIONAL)** The latest version of [Kapedani's Subspace Emissary Ex](https://github.com/Sammi-Husky/BrawlEx/releases). This can be installed over your P+Ex build's root directory. **This is only necessary if you are not on the latest P+Ex version and would like to install your characters into Subspace Emissary mode.** If you want additional CSS slots for SSE, you can also download a basic expanded CSS [here](https://www.mediafire.com/file/b509fjbg3l3buqj/Expanded_SSE_CSS.zip/file).
- If you're trying to use the Install Character plugin, you'll need a proper character package .zip file. You can find an example package using CaliKingz01's RockmanX PSA and Shy's cosmetics [here](https://github.com/squidgy617/BrawlInstallerPlugins#template-packages). You can also find a variety of character packages uploaded [here](http://forums.kc-mm.com/Gallery/BrawlView.php?ByUserID=28848&Moderated=All).

<b>Setup</b>

For initial installation, you can set this repo as a subscription in BrawlCrate by navigating to Tools > Settings > Updater, clicking "Manage Subscriptions", and pasting this link: https://github.com/squidgy617/BrawlInstallerPlugins. If you set this up in BrawlCrate, the plugins will update automatically when you launch BrawlCrate. Alternatively, you can download the release manually and extract the contents to your BrawlCrate installation's "BrawlAPI" folder.

The plugins create backups of your files during execution, however, I cannot guarantee you will not run into issues, especially if you configure your settings incorrectly. If you want an extra safety net, I recommend setting up a git repository for your build [like this template](https://github.com/jlambert360/PPlus-Build-Template) for an easy method of source control. With the automatic backup functionality, this is not really necessary, but still a good idea.

</details>

# Guides

- [Configuring Settings](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Configuring-Settings)
- [Packaging Characters](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Packaging-Characters)
- [Managing Characters](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Managing-Characters)
- [Managing Costumes](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Managing-Costumes)
- [Managing Music](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Managing-Music)
- [Managing Stages](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Managing-Stages)
- [Newbie's Guide to the BrawlInstaller Plugins](https://docs.google.com/document/d/1RcAqzS9IHzQcrtHKspC7qbBB0he9_H69GB6BGLXduJw/edit?usp=sharing) (OUTDATED)

# Character Packages

**Character Packages available [here](http://forums.kc-mm.com/Gallery/BrawlView.php?ByUserID=28848&Moderated=All).**

The Install Character plugin works by extracting files from a "Character Package", a .zip file containing the fighter's files, cosmetics, etc. with a particular directory structure.

Character packages can be created manually or automatically using the "Package Character" plugin. There are also a few template packages that you can use to create your own. For more information, visit [the wiki page](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Character-Packages).

Ideally, mod creators should create good character packages for you to use with this plugin, but if no package exists, anybody can create one using the previously mentioned plugin or templates.

# [Plugins](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Plugins)

Click the above link to see detailed documentation on all of the plugins included in this suite.

# FAQ
<details>
<summary><b>There are errors/crashes when my fighter is in a battle with Kirby.</b></summary>

The first and most common cause of this issue is not setting up QuickLava's Kirby Hat Manager correctly. Ensure it is installed into your build folder and that you have moved the required files into the folder for the application.

Assuming you have QuickLava's Kirby Hat Manager set up correctly, this is not something BrawlInstaller can account for, but is actually a known issue with the KirbyHatEx system. The system is still not entirely stable, and not everything is known about how the hats interact with different fighters and IDs. Most likely, the cause is either an incompatibility with your character, your chosen ID, the chosen base fighter ID for the Kirby hat, or a combination of the three. If you run into Kirby-related issues, try uninstalling your character and reinstalling them to a different fighter ID or installing them with a different base fighter ID for their Kirby hat.

Alternatively to the above, you can simply disable installing Kirby hats in your build settings to avoid this issue. In P+Ex builds, this may cause instability if your build does not contain the following code, so add it to your build if you do not have it:
```
####################################################
Temporary Hatless Clone Kirby Inhale Fix [DukeItOut]
####################################################
HOOK @ $80814664
{
    lis r12, 0x817C            # based on 8084DC7C, where r5 is r28 + 1088. r28 in P+EX is 817C7C00
    ori r12, r12, 0x8040
    lbzx r0, r12, r27
    cmpwi r0, 0
    bne hasHat
    li r3, 0        # force to fail
hasHat:    
    lwz r0, 0x14(r1)
}
```

</details>

<details>
<summary><b>I added my character but don't see them on the character select screen/SSE character select, or their position on the screen is incorrect.</b></summary>

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

<details>
  <summary><b>I get errors with the code menu/strange behavior after installing a character.</b></summary>
  
  Usually this means the build you have uses a code menu that is not compatible with BrawlInstaller. BrawlInstaller only supports QuickLava's code menu. If you are using a build with it's own code menu that is not configured the same way as QuickLava's, you will need to make code menu edits manually, and likely you should set BrawlInstaller not to make code menu changes.
  
</details>

<details>
  <summary><b>The stage/music manager doesn't work for me.</b></summary>
  
  The most likely reason for this is that your build does not use the modern Project+ tracklist and stage systems. Only the Project+ tracklist and stage systems are supported by BrawlInstallers stage and music managers. Most modern builds use this system, but some older builds may not.
  
</details>

<details>
  <summary><b>I don't see a certain character's IDs when using the ID picker.</b></summary>
  
  For character IDs to show in the ID pickers, you need to [modify the ID list](https://github.com/squidgy617/BrawlInstallerPlugins/wiki/Using-ID-Pickers#modifying-id-lists) used by BrawlCrate. For Ex builds, you might want to consider doing this for your Ex characters. For base P+ builds, the only character that will not appear by default. You can add him by adding the following line to `FighterList.txt` located in the `CustomLists` folder in your BrawlCrate directory:

`       |0x35   |0x2D       |0x2A       |0x2F       |Knuckles        |Knuckles (Project+ Only) // IDs are based on P+`
  
</details>

<details>
  <summary><b>Opening my character package with the "Package Character" plugin doesn't work.</b></summary>
  
  Most likely, this is due to the structure of your character package being invalid. Try comparing the package to one of the template packages to get an idea of where everything needs to be, or start fresh using the form to create your package to ensure everything is structured right automatically.
  
</details>

# Credits
This tool was made possible by:
- Soopercool101, Kryal, BlackJax96, and libertyernie for BrawlLib, BrawlBox, and BrawlCrate. Extra thanks to Soopercool101 for making additions to BrawlCrate to support features needed for the BrawlInstaller plugins.
- markymawk, for their basic guide to writing plug-ins and for their plug-ins which served as a great learning resource, as well as their stage and music managing guides for Project+ which were a valuable resource.
- Kapedani, for providing files and assistance with Subspace Emissary Ex implementation.
- QuickLava and codes, for the various tools they created that these plugins are able to interact with.
- KingJigglypuff for providing detailed information on currently supported non-Ex modules.
- CaliKingz01, who provided the PSA for X to use as an example character package.
- Shy, who created the cosmetics used for X.
- Hatyaro, for helping with some coding challenges.
- The Project+ team, for the advancements made to Brawl modding that made this all possible.
- Project+ EX and all the documentation provided and linked within KingJigglypuff's [P+Ex Release Document](https://docs.google.com/document/d/1mAoVGymOkL3FwiMxfEt1V24qxnAWiO8I66G3zlU0ij8/edit?usp=sharing). Learning these processes thoroughly was necessary for creating these plugins.
- The Brawl modding community and [Custom Brawl Modding discord](https://discord.gg/GbxJhbv), for being a great source of knowledge on all things Brawl-modding.

# Planned Features
These are some features that are planned for eventual implementation in the plugin suite, if they are feasible.
- Automatic HD texture renaming and importing for Dolphin (hopefully)
