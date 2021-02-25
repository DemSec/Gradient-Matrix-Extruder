from tkinter import *                 # GUI
from tkinter import ttk               # scrollbar
import os                             # Locating path
import winreg                         # Reading file extension assosiations
from subprocess import Popen, PIPE    # Opening SolidWorks
#from PIL import Image                 # Processing Images
import numpy as np                    # Reading Images
from math import ceil                 # ceil()

# Get SW executable path:
file_ext = ".SLDPRT"
SW_query = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{file_ext}")
SW_path = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Classes\{SW_query}\shell\open\command")
print(SW_path)
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
        
        
def add_layer():
    
    i=len(layer)
    
    layer.append(Label(frame, text="Layer "+str(i)))
    layer[-1].pack(padx = 10, pady=10)
    
    fileFrame = Frame(frame)
    fileFrame.pack(side=TOP)

    imgtext.append(StringVar())
    Imglocation.append(Entry(fileFrame, width=50,textvariable=imgtext[i]))
    Imglocation[-1].pack(side=LEFT,padx = 10, pady=5)

    button.append(Button(fileFrame, text="...", padx=10, pady=5, fg="white", bg="#666666", command=browse_image))
    button[i].pack(side=RIGHT,padx = 10, pady=5)

    #label.append(tk.Label(root, text="RES:").grid(row=0+i*4, column=8))
    dimentionFrame = Frame(frame)
    dimentionFrame.pack(side=TOP)
    
    width.append(Label(dimentionFrame, text="Width:"))
    width[-1].pack(side=LEFT,padx = 10, pady=10)
    widthBox.append(Entry(dimentionFrame, width=4))
    widthBox[-1].pack(side=LEFT,padx = 10, pady=10)

    length.append(Label(dimentionFrame, text="Length:"))
    length[-1].pack(side=LEFT,padx = 10, pady=10)
    lengthBox.append(Entry(dimentionFrame, width=4))
    lengthBox[-1].pack(side=LEFT,padx = 10, pady=10)

    height.append(Label(dimentionFrame, text="Height:"))
    height[-1].pack(side=LEFT,padx = 10, pady=10)
    heightBox.append(Entry(dimentionFrame, width=4))
    heightBox[-1].pack(side=LEFT,padx = 10, pady=10)





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


#GUI root element
root = Tk()

layerFrame=LabelFrame(root)
commandFrame=Frame(root)
commandFrame.pack(side=BOTTOM,fill="both",expand="yes",padx=10,pady=10)
layerFrame.pack(fill="both",expand="yes",padx=10,pady=10)

canvas = Canvas(layerFrame)

canvas.pack(side=LEFT,fill="both",expand="yes")

sb = ttk.Scrollbar(layerFrame,orient="vertical",command=canvas.yview)

sb.pack(side=RIGHT,fill="y")
canvas.configure(yscrollcommand=sb.set)

canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

frame = Frame(canvas)
canvas.create_window((0,0),window=frame,anchor="nw")

NumLayers=4
for i in range(NumLayers):
    add_layer()
    

#command frame elements that dont need to be replicated
output = Label(commandFrame, text="Output")
output.pack(side=LEFT,padx=10,pady=10)

outputBox = Entry(commandFrame, width=50)
outputBox.pack(side=LEFT,padx=10,pady=10)

generate = Button(commandFrame, text="Generate", padx=10, pady=5, fg="white", bg="#666666", command=generate_matrix)
generate.pack(side=LEFT,padx=10,pady=10)

buttonAdd = Button(commandFrame, text=" + ", padx=10, pady=5, fg="white", bg="#666666", command=add_layer)
buttonAdd.pack(side=LEFT,padx=10,pady=10)

root.mainloop()

