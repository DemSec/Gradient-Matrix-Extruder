import tkinter as tk                    # GUI
from tkinter import filedialog as fd    # Browsing files
from tkinter import ttk                 # StringVar
from tkinter.messagebox import showinfo # MessageBox
import os                               # Locating path
import winreg                           # Reading file extension assosiations
from subprocess import Popen, PIPE      # Opening Blender
from math import ceil, isnan            # Ceiling, IsNaN
import numpy as np                      # Numpy 3D array/matrix
import h5py                             # Alternative to numpy array

# import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('TkAgg')
# from numpy import MAXDIMS, arange, sin, pi
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# import sys

def browse_blender():
   global blender_path
   # Note: FileDialog like 'askopenfilename' accepts **options:
   # parent, title, initialdir, initialfile, filetypes, defaultextension, multiple
   # Note: filetypes = a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
   blender_path = fd.askopenfilename(filetypes = [('','.exe')])
   print("Blender path: " + blender_path)

def browse_npy():
   global i_matrix_path, i_matrix_name, i_matrix_ext, i_matrix_dir
   # Note: FileDialog like 'askopenfilename' accepts **options:
   # parent, title, initialdir, initialfile, filetypes, defaultextension, multiple
   # Note: filetypes = a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
   i_matrix_path = fd.askopenfilename(initialdir = i_matrix_dir, filetypes = [('','.npy'),('','.h5py')])
   i_matrix_name = i_matrix_path.split('/')[-1].split('.')[0]
   i_matrix_ext = i_matrix_path.split('.')[-1]
   i_matrix_dir = i_matrix_path[0 : i_matrix_path.rfind('/') + 1]
   browseEntry.delete(0,300)
   browseEntry.insert(0, i_matrix_path)
   load_matrix()

def load_settings():
   global i_matrix_path, MatA, MatB, width, length, height, layer, grid
   print("Loading settings: " + i_settings_path)
   # read settings
   with open(i_settings_path) as f:
      settings = f.read().splitlines()
   # set settings
   for line, text in enumerate(settings):
      if line == 0:
         i_matrix_path = text
      elif text.find("MatA") != -1:
         MatA = float(text.split("=")[1])
      elif text.find("MatB") != -1:
         MatB = float(text.split("=")[1])
      elif text.find("width") != -1:
         width = float(text.split("=")[1])
      elif text.find("length") != -1:
         length = float(text.split("=")[1])
      elif text.find("height") != -1:
         height = float(text.split("=")[1])
      elif text.find("layer") != -1:
         layer = float(text.split("=")[1])
      elif text.find("grid") != -1:
         grid = float(text.split("=")[1])

def save_settings():
   global MatA, MatB, width, length, height, grid
   f = open(i_settings_path, "w")
   f.write(i_matrix_path + "\n")
   MatA = float(matAEntry.get())
   MatB = float(matBEntry.get())
   width = float(widthEntry.get())
   length = float(lengthEntry.get())
   height = float(heightEntry.get())
   layer = float(layerEntry.get())
   grid = float(gridEntry.get())
   f.write("MatA="   + str(MatA)   + "\n")
   f.write("MatB="   + str(MatB)   + "\n")
   f.write("width="  + str(width)  + "\n")
   f.write("length=" + str(length) + "\n")
   f.write("height=" + str(height) + "\n")
   f.write("layer="  + str(layer)  + "\n")
   f.write("grid="   + str(grid)   + "\n")
   f.close()
   print("Saved settings: " + i_settings_path)

def load_matrix():
   global matrix, matrix_shape, matrix_downscaled
   print("Loading matrix from file: " + i_matrix_path)
   print("Matrix file extension: " + i_matrix_ext)
   if (i_matrix_ext == "npy"):
      matrix = np.load(i_matrix_path)
   elif (i_matrix_ext == "h5py"):
      matrix = h5py.File(i_matrix_path, 'r')
   matrix_shape = np.shape(matrix)
   # show_matrix()
   # (Z,Y,X) = matrix_shape
   # layer = float(layerEntry.get())
   # grid = float(gridEntry.get())
   # matrix_downscaled = matrix[::round(Z/layer),::round(Y/grid),::round(X/grid)]
   # print(matrix_downscaled.shape)
   # generate_matrix()
   # show_matrix_downscaled()

def run_macro():
   # save settings:
   save_settings()
   # TODO: Avoid opening new blender process if one exists
   Popen([blender_path, blender_macro_path], stdout = PIPE, stderr = PIPE)


# def show_matrix():
#    z_slice = 1  # slice along Z to plot
#    plt.imshow(matrix[z_slice, :, :], origin='lower')  # plotting a z-axis cross section
#    plt.colorbar()
#    plt.figure()
#    plt.imshow(matrix[:, int(matrix.shape[1]/2), :], origin='lower')  # plotting a ZX cross section down the center
#    plt.colorbar()

#    plt.show()


# def show_matrix_downscaled():
#    z_slice = 1  # slice along Z to plot
#    plt.imshow(matrix_downscaled[z_slice, ::1, ::1], origin='lower')  # plotting a z-axis cross section
#    plt.colorbar()
#    plt.figure()
#    plt.imshow(matrix_downscaled[::1, int(matrix_downscaled.shape[1]/2), ::1], origin='lower')  # plotting a ZX cross section down the center
#    plt.colorbar()

#    plt.show()


def layer_changed(event):
   global layer
   # TODO: the value doesn't update until after pressing key
   layer = float(layerEntry.get())

def grid_changed(event):
   global grid
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



# ==================================== MAIN ====================================

# get Blender executable path:
blender_ext = ".blend"
blender_query = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{blender_ext}")
blender_path = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{blender_query}\shell\open\command")
print("Blender query result: " + blender_path)
if blender_path.find("Blender\\") != -1:
   blender_path = blender_path[1 : blender_path.find("Blender\\") + 8] + "blender.exe"
   print("Blender found: " + blender_path)
else:
   print("Blender not found, please browse to Blender.exe")
   browse_blender()


# Note: using os.getcwd can be different if run from
#       command line from different directory, so use this instead:
# get workspace directory
workspace_dir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + "/"
print("Workspace directory: " + workspace_dir)

# Note: technically, paths can be directories,
#       but here 'path' signifies 'filepath'
#       and 'dir' signifies 'directory'.

# Settings.txt file is expected in the workspace directory
i_settings_file = "Settings.txt"
i_settings_path = workspace_dir + i_settings_file


i_matrix_name = "index_profile"
i_matrix_ext = "npy"
i_matrix_dir = workspace_dir + "Input Matrix/"
i_matrix_path = i_matrix_dir + i_matrix_name + "." + i_matrix_ext
o_matrix_dir = workspace_dir + "Output Matrices/"
blender_macro_path = workspace_dir + "Square Grid.blend"

# set default values
matrix = np.matrix
matrix_downscaled = np.matrix
matrix_shape = (1,1,1)
width, length, height = 10, 10, 10
layer, grid = 10, 10
MatA, MatB = 1, 2

# load settings, if any
load_settings()

# load the matrix, if any
load_matrix()

# GUI root element
root = tk.Tk()
controll_frame= tk.Frame(root)
veiw_frame= tk.Frame(root)

top_frame = tk.Frame(controll_frame)
mid_frame = tk.Frame(controll_frame)
botom_frame= tk.Frame(controll_frame)

root.title("Gradient Matrix Extruder")

# top row

browseLabel = tk.Label(veiw_frame, text="Input Matrix:", pady=10)
browseLabel.pack(side = tk.LEFT)

browseEntry = tk.Entry(veiw_frame, width=80)
browseEntry.pack(side = tk.LEFT)
browseEntry.insert(0, i_matrix_path)

browseButton = tk.Button(veiw_frame, text="Browse", padx=10, pady=10, fg="white", bg="#666666", command=browse_npy)
browseButton.pack(side = tk.LEFT)

generateButton = tk.Button(veiw_frame, text="Generate", padx=10, pady=10, fg="white", bg="#666666", command=run_macro)
generateButton.pack(side = tk.LEFT)

veiw_frame.pack(side = tk.TOP)


matALabel = tk.Label(mid_frame, text="Mat. A:", pady=10)
matALabel.pack(sid = tk.LEFT, padx=10, pady=10)

matAEntry = tk.Entry(mid_frame, width=10)
matAEntry.pack(side = tk.LEFT,padx=10, pady=10)
matAEntry.insert(0, "{:.2f}".format(MatA))

matBLabel = tk.Label(mid_frame, text="Mat. B:", pady=10)
matBLabel.pack(side = tk.LEFT,padx=10, pady=10)

matBEntry = tk.Entry(mid_frame, width=10)
matBEntry.pack(side = tk.LEFT,padx=10, pady=10)
matBEntry.insert(0, "{:.2f}".format(MatB))

layerLabel = tk.Label(mid_frame, text="Layer:", pady=10)
layerLabel.pack(side = tk.LEFT,padx=10, pady=10)

layerEntry = tk.Entry(mid_frame, width=10)
layerEntry.bind('<Return>',layer_changed)
layerEntry.pack(side = tk.LEFT,padx=10, pady=10)
layerEntry.insert(0, "{:.2f}".format(layer))

gridLabel = tk.Label(mid_frame, text="Grid:", pady=10)
gridLabel.pack(side = tk.LEFT,padx=10, pady=10)

gridEntry = tk.Entry(mid_frame, width=10)
gridEntry.bind('<Return>',grid_changed)
gridEntry.pack(side = tk.LEFT,padx=10, pady=10)
gridEntry.insert(0, "{:.2f}".format(grid))

mid_frame.pack(side = tk.TOP)

# botom entry boxes

widthLabel = tk.Label(botom_frame, text="Width:", pady=10)
widthLabel.pack(side = tk.LEFT,padx=10, pady=10)

widthEntry = tk.Entry(botom_frame, width=10)
widthEntry.bind('<Return>',width_changed)
widthEntry.pack(side = tk.LEFT,padx=10, pady=10)
widthEntry.insert(0, "{:.2f}".format(width))

lengthLabel = tk.Label(botom_frame, text="Length:", pady=10)
lengthLabel.pack(side = tk.LEFT,padx=10, pady=10)

lengthEntry = tk.Entry(botom_frame, width=10)
lengthEntry.bind('<Return>',length_changed)
lengthEntry.pack(side = tk.LEFT,padx=10, pady=10)
lengthEntry.insert(0, "{:.2f}".format(length))

heightLabel = tk.Label(botom_frame, text="Height:", pady=10)
heightLabel.pack(side = tk.LEFT,padx=10, pady=10)

heightEntry = tk.Entry(botom_frame, width=10)
heightEntry.bind('<Return>',height_changed)
heightEntry.pack(side = tk.LEFT,padx=10, pady=10)
heightEntry.insert(0, "{:.2f}".format(height))

botom_frame.pack(side = tk.BOTTOM)
controll_frame.pack(side = tk.TOP,fill=tk.BOTH)
veiw_frame.pack(side = tk.BOTTOM)

# TODO: Restrict entry input characters to numbers and .

root.mainloop()




