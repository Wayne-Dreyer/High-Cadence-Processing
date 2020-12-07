1. REQUIREMENTS
Display - 1920x1080 Resolution

1.1. COMPILATION
Created exe files are OS dependent. If an exe file is not present for your OS, we recommend using the following command in pyinstaller:
pyinstaller Main.py --onefile
It may take some time. The file will be created in a folder called 'dist' and will be named 'Main'.
If you do not have pyinstaller and need to install it, you can do so with the following command:
python3 -m pip install pyinstaller
If you do not wish to use an exe file, you can instead run Main.py as you would run any python3 script.
In order to compile the program into an exe, or to run the script without using an exe, you will need the following packages:
-TkInter
-Astropy
-Matplotlib
How to install these packages will depend on your OS.

2. USAGE
The executable file can be run by double-clicking on it. It may take a moment to start up.
When the program is opened, you will be taken to the Menu screen.

2.1. MENU
From the Menu, you may enter an image file (.fit format) and a signal-noise ratio. Increasing the signal-noise ratio will result in less detections.
You can click the 'View Image' button to display the image from the selected image file.
There are 6 flags the program can be run with: Photoplot, Publication, Check Pixels, Simulate, Create Zoomed Image and Orbits.
Photoplot is for performing slice plots.
Publication is for creating an image with overlay markers labelling the candidate detections.
Check Pixels is for creating a zoomed in image at a user-defined location.
Create Zoomed Image is for creating zoomed in images at each candidate location.
Orbits is for comparing the locations of candidates to the locations of orbiting objects.
After entering the input data and selecting a flag, you can click 'Run' to begin processing.
On some devices, there will also be a 'Limit Resources' button.

2.2. PHOTOPLOT
When running with Photoplot, you will be taken to the Photometry window.
By clicking the 'Select Slice' button and then clicking a point on the image, you can create a slice.
This will prompt you to enter the star name and brightness, the width of the slice can also be modified from the default of 50.
You can remove slices with the 'Undo Slice' button, when “Undo Slice” is greyed out there are no slices to undo.
When you are done, you can click the 'Continue' button to continue to the Output window, data from the selected slices can be found in the Output window.

2.3. PUBLICATION
When running with Publication, an image with candidate detections labelled will be generated. If a label is unreadable due to other labels being placed on top of it or in close proximity to it, please use the zoom tool if need be to clarify those points of interest.
You will be taken to the Output window with the output displayed.

2.4. CHECK PIXELS
When running with Check Pixels, you will be prompted to enter the coordinates of the point to zoom to, as well as a zoom factor.
The coordinates specify the x-y pixel coordinates to centre the zoom on.
The zoom factor specifies the magnification of the zoom.
If the point is close to the edge the image will always be padded from the bottom and the right to ensure the selected pixel is centered in the plot.
You will be taken to the Output window with the zoomed image displayed.

2.5. CREATE ZOOMED IMAGE
When running with Create Zoomed Image, you will be prompted to enter a zoom factor.
This will specify the magnification of the zoom.
A series of images will be generated, centred on each candidate, using the given zoom factor.
In the Output window, each image will appear in a separate tab. This functionality works in a similar way to “Check Pixels”

2.6. ORBITS
When running with Orbits, you will be prompted to give a TLE file and a WCS file.
For TLE, the program supports both TLE and 3LE formats.
For WCS, a .fits file is required.
The date used for calculations is taken from the image file header.
Generates a plot which contains the positions of all detected candidates (RA and Dec form) and the tracks of any orbiting objects (calculated once per second) within the near vicinity (within 2 degrees) over a period of 120 seconds.
The rectangle in the middle of the screen is the bounds of the original image (converted to RA and Dec form). The red dots are the positions of all candidate detections and the green dots are generated from the orbiting objects.
If a 3LE file has been used instead of a TLE file, the names of orbiting objects will be displayed on the plot. Due to the nature of not knowing where an orbits track will be in the image, the name of the object is quite likely to be overlapped by the name of another object. Please use the zoom tool to be able to read it more clearly if need be.

2.7. OUTPUT
After completing the process of any flag, the Output window will be displayed.
Generated images will be displayed in the centre.
The toolbar in the bottom left allows for image manipulation (Reset View/Pan/Zoom).
For flags that generate output data other than the image, the Output window has a 'Show Calculated Output' button.
Clicking 'Show Calculated Output' will show output text, and give a button for saving output data to file.
For flags that do not generate output data other than the image, the 'Show Calculated Output' button is replaced with the button to save data to file.


3. FURTHER DEVELOPMENT
The Project Directory includes all code. It is included in case you wish to pursue further development.
All code is in Python3