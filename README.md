# InfoWorks ICM Flood Volume Calculator
App for easily calculating flood volumes (in gallons) for 2D Zones layers exported from InfoWorks ICM. Optionally, the flood volume can be calculated within a polygon boundary.

## Features
- Easily calculate flood volumes using 2D Zone layers exported from InfoWorks ICM.
- Can be calculated within a boundary, or across the entire modeled area.
- Will automatically handle coordinate systems, or a coordinate system can be specified and all layers will be projected to it.

## Dependencies
- Miniconda 3
- Windows Operating System

## How to Install
1. If you don't already have Miniconda 3 installed, [you can install it from here](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe). Make sure to install for all users on the computer.
2. [Download the code here](https://github.com/mjh92794/InfoWorks-ICM-Flood-Volume-Calculator/archive/refs/heads/main.zip) and unzip the folder.
3. Double click the file "condaInstaller.bat" and follow the prompts in the window that appears (you may have to type "y" on some prompts to install the required libraries). This will create a new conda environment with the required libraries and save a desktop shortcut to run the program.
4. On your desktop, double click the file "Flood Volume Calculator" to run the application.

## How to Use
1. Before exporting the flood layer in InfoWorks ICM, change the units to "MGD":
   - Go to Tools > Options > Units
   - Click the "MGD" Button
   - Click "OK"
2. In InfoWorks ICM, export the 2D Zones layer from a model run to a shapefile:
   - Right click the model run icon in the Master Database pane, and click Export > Results to SHP
     - Check the "Use ArcGIS 10 compatibility" box
     - Set the units to "User"
     - Check the "Export selected tables only" box
     - Click the "Tables" button, and make sure "2D Elements" is checked
     - Click "OK"
   - Set the desired time varying results options (if you only want the maxima, set the dropdown to "None" and check "Export Maxima")
   - Click "OK"
3. On your desktop, double click the file "Flood Volume Calculator" to run the application.
4. For the flood layer, click "Select Layer"
   - In the folder selection dialogue that appears, navigate to and select the shapefile that was just exported. It should be called "2D Zones.shp"
5. Optionally, if you'd only like to calculate the flood volume within a polygon boundary - For the boundary layer, click "Select Layer"
   - In the folder selection dialogue that appears, navigate to and select the boundary shapefile.
6. Optionally, type the EPSG code for the coordinate system to be used. If a coordinate system is already defined for the layers, they will be projected to the coordinate system entered here.
7. Click "Calculate Flooding". A window will appear showing the total flood volume in gallons, and this value will be copied to the clipboard for use in other applications.
