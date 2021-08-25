# Gradient Matrix Extruder (GME)
Software tool used for generation of magnetically permeable RF lens models via Blender.

The program requires an installation of Blender on the computer which the software tool uses to function. If the program is unable to locate blender automatically, the request to locate "blender.exe" will be prompted on startup.

"Input Matrix/" directory stores the ".npy" array and the script that generates it. The directory is not required to function, as the program has the capability to browse for an array anywhere on the computer.

Pressing the "Browse" button requests for a location of a ".npy" or ".h5py" array. Selecting an array displays its preview in two orientations.

Entry cells marked "Mat. A" and "Mat. B" set the index of refraction for the two filaments used during the print. It is important to re-generate the lens after a filament change to match the index of refraction used in the 3D printer. The entry inputs are interchangeable, the program will always assume the material with the higher index of refraction is the positive channel.

Entry cells marked "Grid" and "Layer" control the amount of divisions/voxels there are in X+Y and Z plane respectively.

Entry cells marked "Width", "Length" and "Height" control the final dimensions of the lens. Pressing "Enter" or "Return" with the cursor in any one of these cells will scale the other two dimensions according to the ratio of the supplied 3D array. Supplying an original scaling ratio of dimensions is not required, however, as the program supports stretching of the dimentions.

Pressing "Generate" updates "Settings.ini" file with the user-supplied parameters and opens the blender file, currently named "Square Grid.blend". If the blender file is already open, the "Generate" button will only update the "Settings.ini" file.

Once the blender file is open, there is one more user input needed to generate and export the STLs. Press ▶ in blender to run the script which could take 1-2 minutes.

The output of positive and negative channels are saved in the "Output STLs/" directory, overwriting the previous files.

In the blender's scene collections panel, activate Positive and Negative collections to see the channels.

The newest version of GME comes with averaging down-scaling replacing the old method of sampling down-scaling. The down-scaling function comes with the option to enable/disable treating NaN as a zero which impacts the final average of the positive channel voxel in any given cell.

Closing the GME tool will also close the open blender file.

Running "Build.bat" packages the binary python script into an executable into "dist/" directory and copies "Square Grid.blend" file into "dist/" directory.
