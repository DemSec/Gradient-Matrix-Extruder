from tkinter import *                 # GUI
from tkinter import ttk               # scrollbar
import os                             # Locating path
import winreg                         # Reading file extension assosiations
from subprocess import Popen, PIPE    # Opening SolidWorks
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
   
   
def generate_matrix():
    global imgtext
    for img in imgtext:
       print(img.get())
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
             f.write("\n")
             
       run_macro()
        
        
def run_macro():
   Popen([SW_path, "/m", macro_path], stdout=PIPE, stderr=PIPE)

# Read image and return a 2d numpy array of pixels
def readimage(file):
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
