# Water IO III/VC

## Overview

Water IO III/VC is an addon for Blender 4.0 that allows users to import and export the *GTA III* and *Vice City* `waterpro.dat` files. This tool enables you to visualize the water grid, adjust its properties, and export it back to the `.dat` format for use in the games.

The tool supports the binary `waterpro.dat` format used in *GTA III* and *VC*, which contains water height and visibility data. With this addon, users can import, modify, and export the water data directly in Blender.

## Features

* **Import `waterpro.dat`** – Imports the binary `waterpro.dat` file used in *GTA III* and *VC*, reading the water heights and visibility map.
* **Export `waterpro.dat`** – Allows users to export the modified water data back to the `waterpro.dat` binary format.
* **Visualize Water Grid** – Displays the water grid in Blender’s 3D view, where each grid cell represents a water height and visibility setting.
* **Automatic Material Assignment** – Each water level is assigned a material, which helps visually differentiate different levels of the water grid.
* **Blender UI Panel** – A sidebar panel in Blender’s interface for easy access to the import and export functions.

## How to Use

1. **Install the addon**:

   * Download the `.zip` file and install it via Blender’s preferences.
   * Go to `Edit > Preferences > Add-ons > Install` and select the `.zip` file containing the addon.

2. **Import a Water File**:

   * Open the **Water IO III/VC** panel by navigating to `View3D > Sidebar > Water IO III`.
   * Click the "Import waterpro.dat" button to open the file browser. Select the `waterpro.dat` file from *GTA III* or *VC*.
   * The water grid will be displayed in Blender, with each cell corresponding to a specific water level.

3. **Modify the Water Grid**:

   * You can adjust the height and visibility of each water cell in the 3D view.
   * Use Blender's standard editing tools to manipulate the grid as needed.

4. **Export the Water Data**:

   * After making the necessary adjustments, click the "Export waterpro.dat" button to save the updated water data.
   * Choose the destination and file name for the new `waterpro.dat` file.

5. **Usage in Games**:

   * The exported `waterpro.dat` file can be used in *GTA III* or *Vice City* to modify the water behavior in the game.

## Key Concepts

* **Water Grid**: The water data in *GTA III* and *VC* is organized into a grid of cells. Each cell has a height value representing the water level, and a visibility map that determines if the water is visible at that location.
* **Materials**: Each water level is given a distinct material in Blender, which makes it easy to visually differentiate the levels when working with the water grid.

## Preview
GTA III
![Screenshot 2025-05-08 113255](https://github.com/user-attachments/assets/2a165d7a-77f8-43c5-bcee-98e52b5aaf3d)


GTA VC
![Screenshot 2025-05-08 113221](https://github.com/user-attachments/assets/ea8a8c24-7bb5-4ba5-8e7d-44292f170ace)
