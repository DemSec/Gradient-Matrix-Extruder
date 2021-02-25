import os                             # Locating path
import winreg                         # Reading file extension assosiations
from subprocess import Popen, PIPE    # Opening SolidWorks
import tkinter as tk                  # Creating GUI
from tkinter import filedialog as fd  # Browsing Files
from PIL import Image                 # Processing Images
import numpy as np                    # Reading Images
from math import ceil                 # ceil()

# Get SW executable path:
file_ext = ".SLDPRT"
SW_query = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{file_ext}")
SW_path = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{SW_query}\shell\open\command")
if SW_path.find("SOLIDWORKS\\") == -1:
   print("SolidWorks not found, please browse to SolidWorks executable.")
else:
   SW_path = SW_path[0:SW_path.find("SOLIDWORKS\\") + 11] + "SLDWORKS.exe"

# Using os.getcwd can be different if run from
# command line from different directory, so use this instead:
workspace_dir = os.path.dirname(os.path.realpath(__file__))

# Technically, paths can be directories,
# but here I use 'path' to signify 'filepath'
i_image_dir = workspace_dir + "\\Input BMP\\"
i_image_path = ""
i_image_name = ""
o_matrix_dir = workspace_dir + "\\Output Matrices\\"
o_STL_dir = workspace_dir + "\\Output STL\\"
VBA_macro_path = workspace_dir + "\\Procedural Lens Script.swp"

divisions = 20

def browse_image():
   global i_image_path, i_image_name
   # Note: FileDialog like 'askopenfilename' accepts **options:
   # parent, title, initialdir, initialfile, filetypes, defaultextension, multiple
   # Note: filetypes = a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
   i_image_path = fd.askopenfilename(initialdir=i_image_dir, filetypes=[('','.bmp')])
   i_image_name = i_image_path.split('/')[-1].split('.')[0]
   location1.insert(0, i_image_dir)


def run_macro():
   # TODO: Opens a new SolidWorks process even if one already exists, fix
   Popen([SW_path, "/m", VBA_macro_path], stdout=PIPE, stderr=PIPE)


def readimage_old(file):
   im = Image.open(file)
   img_data = np.array(im.getdata()).reshape(im.size[0],im.size[1],1)
   im.close()
   return img_data


def readimage(file):
   im = Image.open(file)
   return im.convert('RGB')


def generate_matrix_old():
   global i_image_dir
   data = readimage_old(i_image_dir)
   print(len(data))     # Number of columns (x)
   print(len(data[0]))  # Number of rows (y)
   with open(o_matrix_dir,"w") as f:
      for d in range(len(data[0])):
         for p in range(len(data)):
            num = data[d,p,0]
            text = format(num, '08b') + " "
            f.write(text)
         f.write("\n")
   f.close()
   #run_macro()


def generate_matrix():
   im = readimage(i_image_path)
   output_path = o_matrix_dir + i_image_name + ".txt"
   f = open(output_path,"w")

   diameter = im.height if im.height > im.width else im.width
   pix_per_div = diameter / divisions
   hor_divisions = im.width / diameter * divisions
   ver_divisions = im.height / diameter * divisions
   for y in range(ver_divisions):
      for x in range(hor_divisions):
         _sum = 0
         for j in range(ceil(pix_per_div)):
            for i in range(ceil(pix_per_div)):
               x * pix_per_div
               R, G, B = im.getpixel((ceil(x*divisions+i),ceil(y*divisions+j)))
               _sum += R + G + B
         ave = round(_sum / 3 / pix_per_div ^ 2 * 99 / 255)
         num = str(ave)
         f.write(format(num, '02') + ' ')
      f.write("\n")
   """
   for y in range(img.height):
      for x in range(img.width):
         R, G, B = img.getpixel((x,y))
         num = (R + G + B) // 3 * 99 // 256
         f.write(format(num, '02') + ' ')
      f.write("\n")
   """
   f.close()
   #run_macro()


root = tk.Tk()

layer1 = tk.Label(root, text="Layer 1")
#layer2 = tk.Label(root, text="Layer 2")
#layer3 = tk.Label(root, text="Layer 3")

layer1.grid(row=0, column=0)
#layer2.grid(row=1, column=0)
#layer3.grid(row=2, column=0)

location1 = tk.Entry(root, width=50)
#location2 = tk.Entry(root, width=50)
#location3 = tk.Entry(root, width=50)

location1.grid(row=0, column=1, columnspan=6)
#location2.grid(row=1, column=1, columnspan=6)
#location3.grid(row=2, column=1, columnspan=6)

#location1.insert(0, "C:\\Users\\David\\Desktop\\Lens\\Layer1.bmp")
#location2.insert(0, "C:\\Users\\David\\Desktop\\Lens\\Layer2.bmp")
#location3.insert(0, "C:\\Users\\David\\Desktop\\Lens\\Layer3.bmp")

button1 = tk.Button(root, text="...", padx=10, pady=5, fg="white", bg="#666666", command=browse_image)
#button2 = tk.Button(root, text="...", padx=10, pady=5, fg="white", bg="#666666")
#button3 = tk.Button(root, text="...", padx=10, pady=5, fg="white", bg="#666666")

button1.grid(row=0, column=7)
#button2.grid(row=1, column=7)
#button3.grid(row=2, column=7)

label1 = tk.Label(root, text="RES:")
#label2 = tk.Label(root, text="RES:")
#label3 = tk.Label(root, text="RES:")

label1.grid(row=0, column=8)
#label2.grid(row=1, column=8)
#label3.grid(row=2, column=8)

res1 = tk.Entry(root, width=4)
#res2 = tk.Entry(root, width=4)
#res3 = tk.Entry(root, width=4)

res1.grid(row=0, column=9)
#res2.grid(row=1, column=9)
#res3.grid(row=2, column=9)

res1.insert(0, "100")
#res2.insert(0, "50")
#res3.insert(0, "20")


buttonAdd = tk.Button(root, text=" + ", padx=10, pady=5, fg="white", bg="#666666")
buttonAdd.grid(row=3, column=7)

width = tk.Label(root, text="Width:")
width.grid(row=3, column=1)
widthBox = tk.Entry(root, width=4)
widthBox.grid(row=3, column=2)

length = tk.Label(root, text="Length:")
length.grid(row=3, column=3)
lengthBox = tk.Entry(root, width=4)
lengthBox.grid(row=3, column=4)

height = tk.Label(root, text="Height:")
height.grid(row=3, column=5)
heightBox = tk.Entry(root, width=4)
heightBox.grid(row=3, column=6)

output = tk.Label(root, text="Output")
output.grid(row=4, column=0)
outputBox = tk.Entry(root, width=50)
outputBox.grid(row=4, column=1, columnspan=6)
#outputBox.insert(0, "C:\\Users\\David\\Desktop\\Lens\\Lens.stl")

generate = tk.Button(root, text="Generate", padx=10, pady=5, fg="white", bg="#666666", command=generate_matrix)
generate.grid(row=4, column=7)

#openFile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#666666")
#openFile.pack()

#runApps = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#666666")
#runApps.pack()

root.mainloop()
