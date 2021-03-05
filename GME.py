import tkinter as tk                  # GUI
from tkinter import filedialog as fd  # Browsing files
import os                             # Locating path
import winreg                         # Reading file extension assosiations
from subprocess import Popen, PIPE    # Opening SolidWorks
from PIL import Image                 # Reading and processing images
from math import ceil, isnan          # Ceiling, IsNaN
import numpy as np
import h5py

# Get SW executable path:
file_ext = ".SLDPRT"
SW_query = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{file_ext}")
SW_path = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{SW_query}\shell\open\command")
if SW_path.find("SOLIDWORKS\\") != -1:
   SW_path = SW_path[0 : SW_path.find("SOLIDWORKS\\") + 11] + "SLDWORKS.exe"


# Using os.getcwd can be different if run from
# command line from different directory, so use this instead:
workspace_dir = os.path.dirname(os.path.realpath(__file__))

# Technically, paths can be directories,
# but here I use 'path' to signify 'filepath'
i_matrix_name = "index_profile"
i_matrix_extension = ".npy"
i_matrix_dir = workspace_dir + "\\Input Matrix\\"
i_matrix_path = i_matrix_dir + i_matrix_name + i_matrix_extension
o_matrix_dir = workspace_dir + "\\Output Matrices\\"
VBA_macro_path = workspace_dir + "\\Square Grid.swp"

def browse_npy():
   global i_matrix_path, i_matrix_name, i_matrix_extension
   # Note: FileDialog like 'askopenfilename' accepts **options:
   # parent, title, initialdir, initialfile, filetypes, defaultextension, multiple
   # Note: filetypes = a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
   i_matrix_path = fd.askopenfilename(initialdir = i_matrix_dir, filetypes = [('','.npy'),('','.h5py')])
   i_matrix_name = i_matrix_path.split('/')[-1].split('.')[0]
   i_matrix_extension = i_matrix_path.split('.')[-1]
   # TODO: update i_matrix_dir
   inputBox.delete(0,300)
   inputBox.insert(0, i_matrix_path)


def run_macro():
   # TODO: Avoid opening new solidworks process if one exists
   Popen([SW_path, "/m", VBA_macro_path], stdout = PIPE, stderr = PIPE)


def generate_matrix():
   if (i_matrix_extension == ".npy"):
      matrix = np.load(i_matrix_path)
   elif (i_matrix_extension == ".h5py"):
      matrix = h5py.File(i_matrix_path, 'r')
   output_path = o_matrix_dir + i_matrix_name + ".txt"

   # print(matrix.shape)
   # print(np.min(matrix))
   f = open(output_path, "w")
   for y in matrix[len(matrix)//2,::60,::60]:
      for x in y:
         if isnan(x):
            num = 0
         else:
            num = round((x - 1.38) * 100 / 0.12)
         f.write(format(num, '02') + ' ')
      f.write("\n")
   f.close()
   run_macro()


# GUI root element
root = tk.Tk()

root.title("Gradient Matrix Extruder")

inputLabel = tk.Label(root, text="Input NPY")
inputLabel.grid(row=0, column=0)

inputBox = tk.Entry(root, width=80)
inputBox.grid(row=0, column=1, columnspan=3)
inputBox.insert(0, i_matrix_path)

browse = tk.Button(root, text="Browse", padx=10, pady=5, fg="white", bg="#666666", command=browse_npy)
browse.grid(row=0, column=4)

generate = tk.Button(root, text="Generate", padx=10, pady=5, fg="white", bg="#666666", command=generate_matrix)
generate.grid(row=0, column=5)

root.mainloop()

