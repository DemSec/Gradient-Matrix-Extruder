from PIL import Image
import numpy as np
import sys

#read an image and return a 2d numpy array of pixels 
def readimage(file):
    im = Image.open(file)
    imgData = np.array(im.getdata()).reshape(im.size[0],im.size[1],3)
    print(type(im))
    print(type(im.size))
    print(im.size)
    print(im.format)
    print(im.mode)
    print(im)
    
    return imgData
    
def main():
    #take image and output file as args
    layer = sys.argv[1]
    matrixOut = sys.argv[2]
    
    data = readimage(layer)
    with open(matrixOut,"w") as f:
        for d in data:
            for p in d:
                #pixels are in gray scale so RGB values are the same [v,v,v] v=0 black v= 255 white
                f.write(str(p[0])+" ")
            f.write("\n")
                
    
main()