import tkinter as tk                  # GUI
from tkinter import filedialog as fd  # Browsing files
import os                             # Locating path
import winreg                         # Reading file extension assosiations
from subprocess import Popen, PIPE    # Opening SolidWorks
from math import ceil, isnan          # Ceiling, IsNaN
import numpy as np
import h5py
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys

def browse_sld():
   global SW_path
   # Note: FileDialog like 'askopenfilename' accepts **options:
   # parent, title, initialdir, initialfile, filetypes, defaultextension, multiple
   # Note: filetypes = a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
   SW_path = fd.askopenfilename(filetypes = [('','.exe')])
   print("SolidWorks path: " + SW_path)
'''
# Get SW executable path:
SW_ext = ".SLDPRT"
SW_query = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{SW_ext}")
SW_path = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{SW_query}\shell\open\command")
print("SW query result: " + SW_path)
if SW_path.find("SOLIDWORKS\\") != -1:
   SW_path = SW_path[0 : SW_path.find("SOLIDWORKS\\") + 11] + "SLDWORKS.exe"
   print("SolidWorks found: " + SW_path)
else:
   print("SolidWorks not found, please browse to SLDWORKS.exe")
   browse_sld()

# Using os.getcwd can be different if run from
# command line from different directory, so use this instead:
workspace_dir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
print("Workspace directory: " + workspace_dir)

# Technically, paths can be directories,
# but here I use 'path' to signify 'filepath'
i_matrix_name = "index_profile"
i_matrix_ext = "npy"
i_matrix_dir = workspace_dir + "/Input Matrix/"
i_matrix_path = i_matrix_dir + i_matrix_name + "." + i_matrix_ext
o_matrix_dir = workspace_dir + "/Output Matrices/"
VBA_macro_path = workspace_dir + "/Square Grid.swp"
matrix = np.matrix
matrix_downscaled = np.matrix
matrix_shape = (1,1,1)
'''
def browse_npy():
   global i_matrix_path, i_matrix_name, i_matrix_ext
   # Note: FileDialog like 'askopenfilename' accepts **options:
   # parent, title, initialdir, initialfile, filetypes, defaultextension, multiple
   # Note: filetypes = a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
   i_matrix_path = fd.askopenfilename(initialdir = i_matrix_dir, filetypes = [('','.npy'),('','.h5py')])
   i_matrix_name = i_matrix_path.split('/')[-1].split('.')[0]
   i_matrix_ext = i_matrix_path.split('.')[-1]
   # TODO: update i_matrix_dir
   load_matrix()

def load_matrix():
   global matrix, matrix_shape, matrix_downscaled
   print("Loading matrix from file: " + i_matrix_path)
   print("Matrix file extension: " + i_matrix_ext)
   browseEntry.delete(0,300)
   browseEntry.insert(0, i_matrix_path)
   if (i_matrix_ext == "npy"):
      matrix = np.load(i_matrix_path)
   elif (i_matrix_ext == "h5py"):
      matrix = h5py.File(i_matrix_path, 'r')
   matrix_shape = np.shape(matrix)
   #show_matrix()
   (Z,Y,X) = matrix_shape
   layer = float(layerEntry.get())
   grid = float(gridEntry.get())
   matrix_downscaled = matrix[::round(Z/layer),::round(Y/grid),::round(X/grid)]
   print(matrix_downscaled.shape)
   generate_matrix()
   show_matrix_downscaled()

def run_macro():
   # TODO: Avoid opening new solidworks process if one exists
   Popen([SW_path, "/m", VBA_macro_path], stdout = PIPE, stderr = PIPE)


def generate_matrix():
   # print(matrix.shape)
   # print(np.min(matrix))

   # TODO: Replace downsampling with down-averaging
   # TODO: Multi-layer on z-axis
   i = 0
   for z in matrix_downscaled:
      output_path = o_matrix_dir + "Layer" + str(i) + ".txt"
      f = open(output_path, "w")
      for y in z:
         for x in y:
            if isnan(x):
               num = 0
            else:
               num = round((x - 1.38) * 100 / 0.12)
            f.write(format(num, '02') + ' ')
         f.write("\n")
      f.close()
      i += 1

def show_matrix():
   z_slice = 1  # slice along Z to plot
   plt.imshow(matrix[z_slice, :, :], origin='lower')  # plotting a z-axis cross section
   plt.colorbar()
   plt.figure()
   plt.imshow(matrix[:, int(matrix.shape[1]/2), :], origin='lower')  # plotting a ZX cross section down the center
   plt.colorbar()

   plt.show()


def show_matrix_downscaled():
   z_slice = 1  # slice along Z to plot
   plt.imshow(matrix_downscaled[z_slice, ::1, ::1], origin='lower')  # plotting a z-axis cross section
   plt.colorbar()
   plt.figure()
   plt.imshow(matrix_downscaled[::1, int(matrix_downscaled.shape[1]/2), ::1], origin='lower')  # plotting a ZX cross section down the center
   plt.colorbar()

   plt.show()


def layer_changed(event):
   # TODO: the value doesn't update until after pressing key
   layer = float(layerEntry.get())

def grid_changed(event):
   # TODO: the value doesn't update until after pressing key
   grid = float(gridEntry.get())

def width_changed(event):
   # TODO: the value doesn't update until after pressing key
   width = float(widthEntry.get())
   (Z,Y,X) = matrix_shape
   (Z,Y,X) = (Z/X*width,Y/X*width,width)
   lengthEntry.delete(0,10)
   lengthEntry.insert(0, "{:.2f}".format(Y))
   heightEntry.delete(0,10)
   heightEntry.insert(0, "{:.2f}".format(Z))

def length_changed(event):
   # TODO: the value doesn't update until after pressing key
   length = float(lengthEntry.get())
   (Z,Y,X) = matrix_shape
   (Z,Y,X) = (Z/Y*length,length,X/Y*length)
   widthEntry.delete(0,10)
   widthEntry.insert(0, "{:.2f}".format(X))
   heightEntry.delete(0,10)
   heightEntry.insert(0, "{:.2f}".format(Z))

def height_changed(event):
   # TODO: the value doesn't update until after pressing key
   height = float(heightEntry.get())
   (Z,Y,X) = matrix_shape
   (Z,Y,X) = (height,Y/Z*height,X/Z*height)
   widthEntry.delete(0,10)
   widthEntry.insert(0, "{:.2f}".format(X))
   lengthEntry.delete(0,10)
   lengthEntry.insert(0, "{:.2f}".format(Y))

# GUI root element
root = tk.Tk()
controll_frame= tk.Frame(root) 
veiw_frame= tk.Frame(root)


top_frame = tk.Frame(controll_frame)
mid_frame = tk.Frame(controll_frame)
botom_frame= tk.Frame(controll_frame)

root.title("Gradient Matrix Extruder")

#top row

browseLabel = tk.Label(veiw_frame, text="Input Matrix:", pady=10)
browseLabel.pack(side = tk.LEFT)

browseEntry = tk.Entry(veiw_frame, width=80)
browseEntry.pack(side = tk.LEFT)

browseButton = tk.Button(veiw_frame, text="Browse", padx=10, pady=10, fg="white", bg="#666666", command=browse_npy)
browseButton.pack(side = tk.LEFT)

generateButton = tk.Button(veiw_frame, text="Generate", padx=10, pady=10, fg="white", bg="#666666", command=run_macro)
generateButton.pack(side = tk.LEFT)

veiw_frame.pack(side = tk.TOP)


matALabel = tk.Label(mid_frame, text="Mat. A:", pady=10)
matALabel.pack(sid = tk.LEFT, padx=10, pady=10)

matAEntry = tk.Entry(mid_frame, width=10)
matAEntry.pack(side = tk.LEFT,padx=10, pady=10)

matBLabel = tk.Label(mid_frame, text="Mat. B:", pady=10)
matBLabel.pack(side = tk.LEFT,padx=10, pady=10)

matBEntry = tk.Entry(mid_frame, width=10)
matBEntry.pack(side = tk.LEFT,padx=10, pady=10)

layerLabel = tk.Label(mid_frame, text="Layer:", pady=10)
layerLabel.pack(side = tk.LEFT,padx=10, pady=10)

layerEntry = tk.Entry(mid_frame, width=10)
layerEntry.bind('<Return>',layer_changed)
layerEntry.pack(side = tk.LEFT,padx=10, pady=10)

gridLabel = tk.Label(mid_frame, text="Grid:", pady=10)
gridLabel.pack(side = tk.LEFT,padx=10, pady=10)

gridEntry = tk.Entry(mid_frame, width=10)
gridEntry.bind('<Return>',grid_changed)
gridEntry.pack(side = tk.LEFT,padx=10, pady=10)

mid_frame.pack(side = tk.TOP)


#botum entry boxes

widthLabel = tk.Label(botom_frame, text="Width:", pady=10)
widthLabel.pack(side = tk.LEFT,padx=10, pady=10)

widthEntry = tk.Entry(botom_frame, width=10)
widthEntry.bind('<Return>',width_changed)
widthEntry.pack(side = tk.LEFT,padx=10, pady=10)

lengthLabel = tk.Label(botom_frame, text="Length:", pady=10)
lengthLabel.pack(side = tk.LEFT,padx=10, pady=10)

lengthEntry = tk.Entry(botom_frame, width=10)
lengthEntry.bind('<Return>',length_changed)
lengthEntry.pack(side = tk.LEFT,padx=10, pady=10)

heightLabel = tk.Label(botom_frame, text="Height:", pady=10)
heightLabel.pack(side = tk.LEFT,padx=10, pady=10)

heightEntry = tk.Entry(botom_frame, width=10)
heightEntry.bind('<Return>',height_changed)
heightEntry.pack(side = tk.LEFT,padx=10, pady=10)

botom_frame.pack(side = tk.BOTTOM)
controll_frame.pack(side = tk.TOP,fill=tk.BOTH)
veiw_frame.pack(side = tk.BOTTOM)
# try:
#    load_matrix()
# except Exception:
#    print("No matrix found, please browse for file")

root.mainloop()




