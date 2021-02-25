import tkinter as tk                  # GUI
#from tkinter import Label, Entry, Frame, Button, ttk, LEFT, TOP, RIGHT
from tkinter import filedialog as fd  # Browsing Files
import os                             # Locating path
import winreg                         # Reading file extension assosiations
from subprocess import Popen, PIPE    # Opening SolidWorks
#import numpy as np                   # Reading Images
from PIL import Image                 # Processing Images
from math import ceil                 # Ceiling funciton

# Get SW executable path:
file_ext = ".SLDPRT"
SW_query = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{file_ext}")
SW_path = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{SW_query}\shell\open\command")
print(SW_path)
if SW_path.find("SOLIDWORKS\\") == -1:
   print("SolidWorks not found, please browse to SolidWorks executable.")
else:
   SW_path = SW_path[0 : SW_path.find("SOLIDWORKS\\") + 11] + "SLDWORKS.exe"

# Using os.getcwd can be different if run from
# command line from different directory, so use this instead:
workspace_dir = os.path.dirname(os.path.realpath(__file__))

# Technically, paths can be directories,
# but here I use 'path' to signify 'filepath'
i_image_dir = workspace_dir + "\\Input BMP\\"
i_image_path = workspace_dir + "\\Input BMP\\Layer1.bmp"
i_image_name = "Layer1"
o_matrix_dir = workspace_dir + "\\Output Matrices\\"
o_STL_dir = workspace_dir + "\\Output STL\\"
VBA_macro_path = workspace_dir + "\\Procedural Lens Script.swp"

divisions = 20

layer = []
Imglocation = []
imgtext = []
button = []
label = []
width = []
widthBox = []
length = []
lengthBox = []
height = []
heightBox = []


def browse_image():
   global i_image_path, i_image_name
   # Note: FileDialog like 'askopenfilename' accepts **options:
   # parent, title, initialdir, initialfile, filetypes, defaultextension, multiple
   # Note: filetypes = a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
   i_image_path = fd.askopenfilename(initialdir = i_image_dir, filetypes = [('','.bmp')])
   i_image_name = i_image_path.split('/')[-1].split('.')[0]
   #location1.insert(0, i_image_dir)


def run_macro():
   # TODO: Opens a new SolidWorks process even if one already exists, fix
   Popen([SW_path, "/m", VBA_macro_path], stdout = PIPE, stderr = PIPE)


def add_layer():

   i = len(layer)

   layer.append(tk.Label(frame, text = "Layer " + str(i)))
   layer[-1].pack(padx = 10, pady=10)

   fileFrame = tk.Frame(frame)
   fileFrame.pack(side = tk.TOP)

   imgtext.append(tk.StringVar())
   Imglocation.append(tk.Entry(fileFrame, width = 50, textvariable = imgtext[i]))
   Imglocation[-1].pack(side = tk.LEFT, padx = 10, pady = 5)

   button.append(tk.Button(fileFrame, text="...", padx = 10, pady = 5, fg = "white", bg = "#666666", command = browse_image))
   button[i].pack(side = tk.RIGHT, padx = 10, pady = 5)

   #label.append(tk.Label(root, text="RES:").grid(row=0+i*4, column=8))
   dimentionFrame = tk.Frame(frame)
   dimentionFrame.pack(side = tk.TOP)

   width.append(tk.Label(dimentionFrame, text = "Width:"))
   width[-1].pack(side = tk.LEFT, padx = 10, pady = 10)
   widthBox.append(tk.Entry(dimentionFrame, width = 4))
   widthBox[-1].pack(side = tk.LEFT, padx = 10, pady = 10)

   length.append(tk.Label(dimentionFrame, text = "Length:"))
   length[-1].pack(side = tk.LEFT, padx = 10, pady = 10)
   lengthBox.append(tk.Entry(dimentionFrame, width = 4))
   lengthBox[-1].pack(side = tk.LEFT, padx = 10, pady = 10)

   height.append(tk.Label(dimentionFrame, text = "Height:"))
   height[-1].pack(side = tk.LEFT, padx = 10, pady = 10)
   heightBox.append(tk.Entry(dimentionFrame, width = 4))
   heightBox[-1].pack(side = tk.LEFT, padx = 10, pady = 10)


def readimage(file):
   im = Image.open(file)
   return im.convert('RGB')


def generate_matrix_reduced():
   im = readimage(i_image_path)
   output_path = o_matrix_dir + i_image_name + ".txt"
   f = open(output_path, "w")
   diameter = im.height if im.height > im.width else im.width
   pix_per_div = diameter / divisions
   hor_divisions = im.width / diameter * divisions
   ver_divisions = im.height / diameter * divisions
   for y in range(ver_divisions):
      for x in range(hor_divisions):
         _sum = 0
         pixel_amount = 0
         #pixel_amount = max((x + 1) * pix_per_div, im.width) - x * pix_per_div
         for j in range(ceil(pix_per_div)):
            for i in range(ceil(pix_per_div)):
               R, G, B = im.getpixel((x*divisions+i,y*divisions+j))
               _sum += R + G + B
               pixel_amount += 1
         ave = round(_sum / 3 / pixel_amount * 99 / 255)
         num = str(ave)
         f.write(format(num, '02') + ' ')
      f.write("\n")
   f.close()


def generate_matrix():
   im = readimage(i_image_path)
   output_path = o_matrix_dir + i_image_name + ".txt"
   f = open(output_path, "w")
   for y in range(im.height):
      for x in range(im.width):
         R, G, B = im.getpixel((x, y))
         num = (R + G + B) // 3 * 99 // 256
         f.write(format(num, '02') + ' ')
      f.write("\n")
   f.close()


# GUI root element
root = tk.Tk()

layerFrame = tk.LabelFrame(root)
commandFrame = tk.Frame(root)
commandFrame.pack(side = tk.BOTTOM, fill = "both", expand = "yes", padx = 10, pady = 10)
layerFrame.pack(fill = "both", expand = "yes", padx = 10, pady = 10)

canvas = tk.Canvas(layerFrame)

canvas.pack(side = tk.LEFT, fill = "both", expand = "yes")

sb = tk.Scrollbar(layerFrame, orient="vertical", command=canvas.yview)

sb.pack(side = tk.RIGHT, fill="y")
canvas.configure(yscrollcommand = sb.set)

canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox('all')))

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window = frame, anchor = "nw")

NumLayers = 4
for i in range(NumLayers):
   add_layer()

# Command frame elements that don't need to be replicated
output = tk.Label(commandFrame, text = "Output")
output.pack(side = tk.LEFT, padx = 10, pady = 10)

outputBox = tk.Entry(commandFrame, width = 50)
outputBox.pack(side= tk.LEFT, padx = 10, pady = 10)

generate = tk.Button(commandFrame, text = "Generate", padx = 10, pady = 5, fg = "white", bg = "#666666", command = generate_matrix)
generate.pack(side = tk.LEFT, padx = 10, pady = 10)

buttonAdd = tk.Button(commandFrame, text = " + ", padx = 10, pady = 5, fg = "white", bg = "#666666", command = add_layer)
buttonAdd.pack(side = tk.LEFT, padx = 10, pady = 10)

root.mainloop()

