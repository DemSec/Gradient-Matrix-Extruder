import os                             # Locating path
import winreg                         # Reading file extension assosiations
from subprocess import Popen, PIPE    # Opening SolidWorks
import tkinter as tk                  # Creating GUI
from tkinter import filedialog as fd  # Browsing Files
from PIL import Image                 # Processing Images
import numpy as np                    # Reading Images

# Get SW executable path:
file_ext = ".SLDPRT"
SW_query = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{file_ext}")
SW_path = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{SW_query}\shell\open\command")
if SW_path.find("SOLIDWORKS\\") == -1:
   print("SolidWorks not found, please browse to SolidWorks executable.")
else:
   SW_path = SW_path[0:SW_path.find("SOLIDWORKS\\") + 11] + "SLDWORKS.exe"

input_image_path = ""
output_matrix_path = os.getcwd() + "\\Output.txt"
output_STL_path = os.getcwd() + "\\Output STL\\"
#SW_path = "X:\\Programs\\SolidWorks\\SOLIDWORKS\\SLDWORKS.exe"
macro_path = os.path.dirname(os.path.realpath(__file__)) + "\\Procedural Lens Script.swp"

def browse_image1():
   global input_image_path
   input_image_path = fd.askopenfilename()
   location1.insert(0, input_image_path)

def run_macro():
   Popen([SW_path, "/m", macro_path], stdout=PIPE, stderr=PIPE)

#read an image and return a 2d numpy array of pixels
def readimage(file):
   im = Image.open(file)
   img_data = np.array(im.getdata()).reshape(im.size[0],im.size[1],1)
   #print(type(im))
   #print(type(im.size))
   #print(im.size)
   #print(im.format)
   #print(im.mode)
   #print(im)
   im.close()

   return img_data

def generate():
   global input_image_path
   data = readimage(input_image_path)
   #print(outputPath)
   with open(output_matrix_path,"w") as f:
      for d in data:
         for p in d:
            num = str(p[0])
            if len(num) == 3:
               #pixels are in gray scale so RGB values are the same [v,v,v] v=0 black v= 255 white
               f.write(num + " ")
            elif len(num) == 2:
               f.write("0" + num + " ")
            elif len(num) == 1:
               f.write("00" + num + " ")
            else:
               print("Number outside of unsigned 8 bit value!")
         f.write("\n")
   #Popen(args, stdout=PIPE, stderr=PIPE)

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

button1 = tk.Button(root, text="...", padx=10, pady=5, fg="white", bg="#666666", command=browse_image1)
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

generate = tk.Button(root, text="Generate", padx=10, pady=5, fg="white", bg="#666666", command=generate)
generate.grid(row=4, column=7)

#openFile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#666666")
#openFile.pack()

#runApps = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#666666")
#runApps.pack()

root.mainloop()
