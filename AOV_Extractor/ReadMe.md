# AOV Extractor - ReadMe

Welcome! This Python script was written with the intention of making the process of extracting AOVs from Render files and creating their respective Shuffle Nodes easier.

## What this tool does?

This **AOV Extractor** tool creates shuffles nodes of all the AOVs present in your render file (exr) in just a click, assigns proper labels to them, maps the shuffle mappings correctly, including the float/int AOVs that get read into "other" category in Nuke by default, and lays them out neatly, thus saving your time on creating these nodes one by one and manually mapping them. 

## How to install/use this tool inside Nuke?

It is recommended to follow the instructions given in the following link which takes you to the official Nuke Reference Documentation on How to Install Plug-ins
[https://learn.foundry.com/nuke/developers/140/pythonreference/installing_plugins.html](https://learn.foundry.com/nuke/developers/140/pythonreference/installing_plugins.html)

Assuming that you have read the above documentation and created the directories to hold your plugins, init.py file and menu.py file, the following steps should help you add this tool to your existing toolset.
* The **aov_extract.py** is the Python script that goes into your **python** directory in Nuke Home Folder ( which is generally **C:\Users\<your_user_name>\.nuke** on Windows, and **/Users/<your_user_name>/.nuke** on Linux )
* The following set of codes, when added to your menu.py file will help create a Menu Item in your Nuke Window and add this tool under it, for quick usage
  ```
  import aov_extract

  menubar = nuke.menu("Nuke")             #might change based on the existing variable name you may have given to nuke.menu("Nuke")
  m = menubar.addMenu("My Python Tools")  #the same variable name has to be replaced here in the place of "menubar" if you have a different variable; you can name the Menu as you like instead of the "My Pyhton tools" given here

  m.addCommand("Extract all AOVs","aov_extract.performExtractAOV()","","nuke_aov_extract.png")  #you may leave the last argument empty ("") meant for the icon image, if you don't have one
  ```
* On starting a new Session of Nuke, you will notice the new Menu Item that you creaeted on Top, and on clicking it, you'll see this tool in Drop down.
* Now, you can read an exr Render using a **'Read' node**, click on it, and click on this tool from the Menu Shelf.
* Bingo, you'll have all your AOVs extracted into your Node Graph!

## Progress on this Tool
This current version is only the first version (v1.0.0) and it works only with EXRs for now. It has been tested on a fixed number of AOVs (mostly the common ones like 'P', 'Pz/Depth', 'N', 'Oc', 'rgb', 'diffuse', 'specular', 'metallic', 'specrough', etc), while progress is being made to expand the range of AOVs it can extract.
Also, there is a possibility of getting an **easy-to-use GUI using PySide2** to facilitate selection of AOVs from all the existing AOVs and displaying them intact in the GUI. These updaetes will follow in the future. 
