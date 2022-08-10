__author__ = "Michael Hanley"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Michael Hanley"
__status__ = "Beta"

from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from sys import exit
import geopandas

boundaryLayerSelected = ""
floodLayerSelected = ""
epsgSelected = ""

def convertFloatToString(floatValue):
    '''
    Converts a value to a string, formatted with commas and rounded to four decimal places
    '''
    return str("{:,}".format(round(floatValue,4)))

def getShapefile_Name(shpFilePath):
    return shpFilePath.split("/")[-1].split(".shp")[-2]

def calculateFloodVolume(boundaryLayer_path, floodLayer_path, desiredCRS = None):
    boundaryLayer = geopandas.read_file(boundaryLayer_path)
    floodLayer = geopandas.read_file(floodLayer_path)

    # If no EPSG was specified, try setting it based on the layers
    if desiredCRS == None:
        if boundaryLayer.crs == None:
            if floodLayer.crs == None:
                raise ValueError('No layers have coordinate systems specified! Please specify one to use for the analysis.')
            else:
                desiredCRS = floodLayer.crs
        else:
            desiredCRS = boundaryLayer.crs

    # Set undefined CRSs based on desired CRS
    if floodLayer.crs == None:
        floodLayer = floodLayer.set_crs(desiredCRS)
    if boundaryLayer.crs == None:
        boundaryLayer = boundaryLayer.set_crs(desiredCRS)

    # Project all layers to the same CRS
    floodLayerProjected = floodLayer.to_crs(desiredCRS)
    boundaryProjected = boundaryLayer.to_crs(desiredCRS)

    # Clip the flood layer to the boundary
    floodClipped = geopandas.clip(floodLayerProjected, boundaryProjected, keep_geom_type=True)

    # Add a new field and calculate flood volume
    floodClipped['FLOODVOLUME'] = floodClipped.AREA2D * floodClipped.DEPTH2D * 7.4805

    # Return the total flood volume
    return floodClipped['FLOODVOLUME'].sum()

def calculateFloodVolumeNoBoundary(floodLayer_path):
    floodLayer = geopandas.read_file(floodLayer_path)

    # Add a new field and calculate flood volume
    floodLayer['FLOODVOLUME'] = floodLayer.AREA2D * floodLayer.DEPTH2D * 7.4805

    # Return the total flood volume
    return floodLayer['FLOODVOLUME'].sum()

# Function for clearing the contents of text entry boxes
def clear():
    global floodLayerSelected
    global boundaryLayerSelected
    global epsgSelected
    boundaryLayerSelected = ""
    floodLayerSelected = ""
    epsgSelected = ""
    floodInput_Label.configure(text="Flood Layer Selected:\n" + floodLayerSelected)
    boundaryInput_Label.configure(text="Boundary Layer Selected:\n" + boundaryLayerSelected)
    epsgInput_Entry.delete(0, END)

def performFloodAnalysis():
    global floodLayerSelected
    global boundaryLayerSelected
    global epsgSelected
    global epsgInput_Label
    global epsgInput_Entry
    root.withdraw()
    try:
        epsgSelected = epsgInput_Entry.get()
        if boundaryLayerSelected == "":
            if floodLayerSelected == "":
                Tk().withdraw()
                messagebox.showinfo("No Layers selected", "Please select a layer before continuing.")
                root.deiconify()
                return
            else:
                floodVolume = calculateFloodVolumeNoBoundary(floodLayerSelected)
                r = Tk()
                r.withdraw()
                r.clipboard_clear()
                r.clipboard_append(str(floodVolume))
                r.update()
                r.destroy()
                Tk().withdraw()
                messagebox.showinfo("Flood Volume Calculated: " + getShapefile_Name(floodLayerSelected), \
                    "Flood Volume: " + convertFloatToString(floodVolume) + " Gallons" + \
                    "\nValue copied to clipboard!" + \
                    "\nFlood Layer Selected: " + getShapefile_Name(floodLayerSelected) + \
                    "\nBoundary Layer Selected: None")
                root.deiconify()
                return
        else:
            try:
                if epsgSelected != "":
                    int(epsgSelected)
                if epsgSelected != "" and len(epsgSelected) != 4 and len(epsgSelected) != 5:
                    raise ValueError
            except ValueError:
                Tk().withdraw()
                messagebox.showinfo("Correct EPSG Code", "Something is wrong with the format of the EPSG Code Entered (should be 4-5 digit integer). Please Correct.")
                root.deiconify()
                return
            floodVolume = calculateFloodVolume(boundaryLayerSelected, floodLayerSelected, None if epsgSelected == "" or epsgSelected == None else int(epsgSelected))
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(str(floodVolume))
            r.update()
            r.destroy()
            Tk().withdraw()
            messagebox.showinfo("Flood Volume Calculated: " + getShapefile_Name(floodLayerSelected), \
                "Flood Volume: " + convertFloatToString(floodVolume) + " Gallons" + \
                "\nValue copied to clipboard!" + \
                "\nFlood Layer Selected: " + getShapefile_Name(floodLayerSelected) + \
                "\nBoundary Layer Selected: " + getShapefile_Name(boundaryLayerSelected))
            root.deiconify()
            return
    except Exception as errorMessage:
        Tk().withdraw()
        messagebox.showinfo("Unknown Error", errorMessage)
        exit()

# Function for exiting if the "x" button is clicked
def on_closing():
    exit()

def selectFloodInputLayer():
    global floodLayerSelected
    global floodInput_Label
    root.withdraw()
    Tk().withdraw()
    floodLayerSelected = filedialog.askopenfilename(initialdir = "/",title = "Select Flood Layer File (Must be .shp):",filetypes = (("Shapefiles","*.shp"),("all files","*.*")))
    floodInput_Label.configure(text="Flood Layer Selected:\n" + floodLayerSelected)
    root.deiconify()

def selectBoundaryInputLayer():
    global boundaryLayerSelected
    global boundaryInput_Label
    root.withdraw()
    Tk().withdraw()
    boundaryLayerSelected =  filedialog.askopenfilename(initialdir = "/",title = "Select Boundary Layer File (Must be .shp):",filetypes = (("Shapefiles","*.shp"),("all files","*.*")))
    boundaryInput_Label.configure(text="Boundary Layer Selected:\n" + boundaryLayerSelected)
    root.deiconify()

# create a GUI window
root = Tk()
root.title("Calculate Flood Volume Application")

floodInput_Label = Label(root, text="Flood Layer Selected:\n" + floodLayerSelected)
floodInput_Label.grid(row=0, column=0)
floodInput_Button = Button(root, text="Select Layer", command=selectFloodInputLayer)
floodInput_Button.grid(row=0, column=1)

boundaryInput_Label = Label(root, text="Boundary Layer Selected:\n" + boundaryLayerSelected)
boundaryInput_Label.grid(row=1, column=0)
boundaryInput_Button = Button(root, text="Select Layer", command=selectBoundaryInputLayer)
boundaryInput_Button.grid(row=1, column=1)

epsgInput_Label = Label(root, text="EPSG Selected (Optional):" + epsgSelected)
epsgInput_Label.grid(row=2, column=0)
epsgInput_Entry = Entry(root)
epsgInput_Entry.grid(row=2, column=1)

# create a Submit Button and place into the root window
submit = Button(root, text="Calculate Flooding", command=performFloodAnalysis)
submit.grid(row=3, column=1)

# create a Clear Button and place into the root window
submit = Button(root, text="Clear", command=clear)
submit.grid(row=4, column=1)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()