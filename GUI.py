import tkinter as tk
from tkinter import filedialog, Text
import os
from subprocess import Popen, PIPE


args = ["X:\\Programs\\SolidWorks\\SOLIDWORKS\\SLDWORKS.exe", "/m", "D:\\David\\Desktop\\Senior Design\\Procedural Lens\\Procedural Lens Script.swp"]
Popen(args, stdout=PIPE, stderr=PIPE)

root = tk.Tk()

layer1 = tk.Label(root, text="Layer 1")
layer2 = tk.Label(root, text="Layer 2")
layer3 = tk.Label(root, text="Layer 3")

layer1.grid(row=0, column=0)
layer2.grid(row=1, column=0)
layer3.grid(row=2, column=0)

location1 = tk.Entry(root, width=50)
location2 = tk.Entry(root, width=50)
location3 = tk.Entry(root, width=50)

location1.grid(row=0, column=1, columnspan=6)
location2.grid(row=1, column=1, columnspan=6)
location3.grid(row=2, column=1, columnspan=6)

location1.insert(0, "C:\\Users\\David\\Desktop\\Lens\\Layer1.bmp")
location2.insert(0, "C:\\Users\\David\\Desktop\\Lens\\Layer2.bmp")
location3.insert(0, "C:\\Users\\David\\Desktop\\Lens\\Layer3.bmp")

button1 = tk.Button(root, text="...", padx=10, pady=5, fg="white", bg="#666666")
button2 = tk.Button(root, text="...", padx=10, pady=5, fg="white", bg="#666666")
button3 = tk.Button(root, text="...", padx=10, pady=5, fg="white", bg="#666666")

button1.grid(row=0, column=7)
button2.grid(row=1, column=7)
button3.grid(row=2, column=7)

label1 = tk.Label(root, text="RES:")
label2 = tk.Label(root, text="RES:")
label3 = tk.Label(root, text="RES:")

label1.grid(row=0, column=8)
label2.grid(row=1, column=8)
label3.grid(row=2, column=8)

res1 = tk.Entry(root, width=4)
res2 = tk.Entry(root, width=4)
res3 = tk.Entry(root, width=4)

res1.grid(row=0, column=9)
res2.grid(row=1, column=9)
res3.grid(row=2, column=9)

res1.insert(0, "100")
res2.insert(0, "50")
res3.insert(0, "20")


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
outputBox.insert(0, "C:\\Users\\David\\Desktop\\Lens\\Lens.stl")

generate = tk.Button(root, text="Generate", padx=10, pady=5, fg="white", bg="#666666")
generate.grid(row=4, column=7)



#openFile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#666666")
#openFile.pack()

#runApps = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#666666")
#runApps.pack()

root.mainloop()

