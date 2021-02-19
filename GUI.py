import os                             # Locating path
import winreg                         # Reading file extension assosiations
from subprocess import Popen, PIPE    # Opening SolidWorks
import tkinter as tk                  # Creating GUI
from tkinter import filedialog as fd  # Browsing Files
from tkinter import ttk
from tkinter import *
#from PIL import Image                 # Processing Images
import numpy as np                    # Reading Images

# Get SW executable path:
file_ext = ".SLDPRT"
SW_query = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{file_ext}")
SW_path = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{SW_query}\shell\open\command")
print(SW_path)
if SW_path.find("SOLIDWORKS\\") == -1:
   print("SolidWorks not found, please browse to SolidWorks executable.")
else:
   SW_path = SW_path[0:SW_path.find("SOLIDWORKS\\") + 11] + "SLDWORKS.exe"

# Using os.getcwd can be different
# if run from command line from different directory:
workspace_path = os.path.dirname(os.path.realpath(__file__))

input_image_path = ""
output_matrix_path = workspace_path + "\\Output Matrices\\Layer1.txt"
output_STL_path = workspace_path + "\\Output STL\\"
macro_path = workspace_path + "\\Procedural Lens Script.swp"

layer =[]
Imglocation =[]
imgtext = []
button =[]
label =[]
width =[]
widthBox =[]
length =[]
lengthBox =[]
height =[]
heightBox =[]

def browse_image():
   global input_image_path
   input_image_path = fd.askopenfilename()
   location1.insert(0, input_image_path)
   
def add_layer():

    i=len(layer)
    
    layer.append(tk.Label(root, text="Layer "+str(i)).grid(row=0+i*4, column=0))

    imgtext.append(tk.StringVar())
    Imglocation.append(tk.Entry(root, width=50,textvariable=imgtext[i]).grid(row=0+i*4, column=1, columnspan=6))

    button.append(tk.Button(root, text="...", padx=10, pady=5, fg="white", bg="#666666", command=browse_image))
    button[i].grid(row=0+i*4, column=7)

    
    width.append(tk.Label(root, text="Width:").grid(row=3+i*4, column=1))
    widthBox.append(tk.Entry(root, width=4).grid(row=3+i*4, column=2))

    length.append(tk.Label(root, text="Length:").grid(row=3+i*4, column=3))
    lengthBox.append(tk.Entry(root, width=4).grid(row=3+i*4, column=4))

    height.append(tk.Label(root, text="Height:").grid(row=3+i*4, column=5))
    heightBox.append(tk.Entry(root, width=4).grid(row=3+i*4, column=6))
    
    update_footer()
    


def run_macro():
   Popen([SW_path, "/m", macro_path], stdout=PIPE, stderr=PIPE)

# Read image and return a 2d numpy array of pixels
def readimage(file):
   im = Image.open(file)
   img_data = np.array(im.getdata()).reshape(im.size[0],im.size[1],1)
   im.close()

   return img_data

def generate_matrix():
    global imgtext
    for img in imgtext:
       print(img.get())
       '''
       data = readimage(img.get())
       with open(output_matrix_path,"w") as f:
          for d in data:
             for p in d:
                num = str(p[0])
                if len(num) == 3:
                   f.write(num + " ")
                elif len(num) == 2:
                   f.write("0" + num + " ")
                elif len(num) == 1:
                   f.write("00" + num + " ")
                else:
                   print("Number outside of unsigned 8 bit value!")
             f.write("\n")'''
             
        #run_macro()


def update_footer():
    global buttonAdd
    global output
    global outputBox
    global generate
    
    i = len(layer)
    
    buttonAdd.grid(row=3+i*4, column=7)
    output.grid(row=4+i*4, column=0)
    outputBox.grid(row=4+i*4, column=1, columnspan=6)
    generate.grid(row=4+i*4, column=7)

root = tk.Tk()

layersFrame = LabelFrame(root)
canvas = Canvas(layersFrame)

canvas.grid(row=0,column=0,rowspan=30, columnspan=10)

scrollbar = ttk.Scrollbar(layersFrame,orient="vertical",command=canvas.yview)
scrollbar.grid(row =0,column=10,rowspan=30, columnspan=10)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

frame = Frame(canvas)
canvas.create_window((0,0),window=frame,anchor="nw")

NumLayers=4
for i in range(NumLayers):
    layer.append(tk.Label(frame, text="Layer "+str(i)))
    layer[-1].grid(row=0+i*4, column=0)

    imgtext.append(tk.StringVar())
    Imglocation.append(tk.Entry(frame, width=50,textvariable=imgtext[i]))
    Imglocation[-1].grid(row=0+i*4, column=1, columnspan=6)

    button.append(tk.Button(frame, text="...", padx=10, pady=5, fg="white", bg="#666666", command=browse_image))
    button[i].grid(row=0+i*4, column=7)

    #label.append(tk.Label(root, text="RES:").grid(row=0+i*4, column=8))
    
    width.append(tk.Label(frame, text="Width:"))
    width[-1].grid(row=3+i*4, column=1)
    widthBox.append(tk.Entry(frame, width=4))
    width[-1].grid(row=3+i*4, column=2)

    length.append(tk.Label(frame, text="Length:"))
    length[-1].grid(row=3+i*4, column=3)
    lengthBox.append(tk.Entry(frame, width=4))
    lengthBox[-1].grid(row=3+i*4, column=4)

    height.append(tk.Label(frame, text="Height:"))
    height[-1].grid(row=3+i*4, column=5)
    heightBox.append(tk.Entry(frame, width=4))
    heightBox[-1].grid(row=3+i*4, column=6)



output = tk.Label(root, text="Output")
output.grid(row=4+len(layer)*4, column=0)
outputBox = tk.Entry(root, width=50)
outputBox.grid(row=4+len(layer)*4, column=1, columnspan=6)
#outputBox.insert(0, "C:\\Users\\David\\Desktop\\Lens\\Lens.stl")

generate = tk.Button(root, text="Generate", padx=10, pady=5, fg="white", bg="#666666", command=generate_matrix)
generate.grid(row=4+len(layer)*4, column=7)

buttonAdd = tk.Button(root, text=" + ", padx=10, pady=5, fg="white", bg="#666666", command=add_layer)
buttonAdd.grid(row=0, column=9)



   




root.mainloop()
