# SWBF-HUD-Changer

The SWBF HUD Changer is an application focused on changing the HUD of Star Wars Battlefront 2 2005 easily and fast by using Bad Al's [LVLTool](https://github.com/BAD-AL/LVLTool) to ingest and replace all necessary HUD files within the compiled files of the game.

# Features

- Quickly changing the game's HUD by one button click.

- Fixes overlapping HUD issues on custom maps that use their own ingame.lvl.

- Allows the user to use their own custom crosshair in-game.

- Compatible with Anakins Remastered Mod.

# Install

1. Download the newest release [here.](https://github.com/Leonardrx/SWBF-HUD-Changer/releases)

2. Unzip it and run the SWBF-HUD-Changer.exe.

# How to use

### Important
1. Make sure you have no mod installed that already changes the game's HUD, it will most likely cause issues. Sleepkillers Shaderpatch is fully compatible as well as Anakins Remastered Mod.
2. Applying a Crosshair without applying an HUD beforehand will not work.
3. The Programm will automatically detect if you got Anakins Remastered Mod installed.

On the first launch, select your GameData folder. This path will be saved for future use. After selecting it, press on "Change HUD." You can choose from three different HUDs:

- Modernized: A modernized version of the Battlefront 2 HUD inspired by the 2017 Battlefront 2.

- Default optimized for Crosshair: A slightly changed version of the original HUD to look better with a normal crosshair.

- Default (Changeable Crosshair): The original HUD, modified specifically to allow custom Crosshair/Bullseye injection.

Select one of these in the listbox and press on "Apply HUD." This process only takes seconds.

You can now start your game and see if it was applied correctly. 

If you find yourself wanting to use a different crosshair, open up the SWBF HUD Changer and press on "Change Crosshair." Select one of the preinstalled ones and apply your desired one. You can preview them by selecting one and pressing on "Preview." 

### Selecting Mod Maps (only when not using the Remastered Mod)

You may find yourself playing a mod map and seeing the HUD overlapping with the original one. That is caused by the mod map using their own ingame.lvl. 

To solve this press on "Select Mod Maps" in the SWBF HUD Changer and select the mod map that is causing issues and apply. This selection will be saved until you apply a different one. 

Then simply apply the HUD you want again. 

Note that this only works when the mod map has the ingame.lvl file under "abc/data/_LVL_PC."

# Import Your Own Crosshairs (Tutorial for GIMP)

1. Create a new canvas, 128x128 pixels, and make it transparent.

2. Draw your crosshair onto it or paste an image.

3. Export it as a .tga and unselect the RLE compression while exporting.

4. Open the SWBF HUD Changer, go to "Change Crosshair" -> "Import Crosshair," and select the .tga image.

5. This will be saved until you delete it from the listbox.

# Import Your Own HUD Mods

1. Create a folder with a cool name.

2. Paste your 1playerhud.hud there together with the hudtransfroms.hud if you changed it and a .tga image called "hud_bullseye.tga" for the Crossahir. If you added any other assets (only TGA's are supported; msh´s don't work), also paste them there.

3. To get the Crosshair swaping function working use exactly this code and replace it with the Group("player1bullseye") in the 1playerhud.hud file:
```text
Group("player1bullseye")
    {
        EventEnable("initialize")
        PropagateAlpha(0)
        BarBitmap("bullseye")
        {
            FlashyScale(1.000000)
            Bitmap("hud_bullseye")
            BitmapRect(0.025000, 0.025000, "Center", "Center", "Viewport")
            Viewport(1)
            Alpha(1)
            ColorChangeRate(0.001000)
            EventEnable("initialize")
            EventColor("player1.weapon1.target.teamColorBright")

        }
    }
```
4. Open the SWBF HUD Changer, go to "Change HUD" -> "Import HUD," and select the folder.

5. This will be saved until you delete it from the listbox.

Message me on Discord @herbertgarten for a more detailed explanation.

# Restore Vanilla files

The SWBF HUD Changer saves every file that was changed with the tool. To restore the files that were in your GameData folder before any changes were made, just press on "Restore Vanilla."

# Recomendation

Use the different HUDs with the Sleepkiller [Shaderpatch](https://github.com/PrismaticFlower/shaderpatch) for the best experience.

# Future Plans

Increasing Mod compatibility. Especially with Anakins Remastered Mod.

# Feedback and Suggestions

If you have any feedback or suggestions, please send them to me on Discord: @herbertgarten. :)

# Credits

This programm is made possible through Bad Al´s amazing work on the [LVLTool](https://github.com/BAD-AL/LVLTool). Go check it out.

And big thanks to all active members on the Battlefront Competitive League [Discord](https://discord.gg/swbf2) for giving me feedback on the HUD´s I created. Go join it :)

