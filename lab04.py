from skimage import data,io,filters,morphology,feature,color,measure
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from PIL import Image,ImageFilter,ImageOps
import numpy as np
"""
images=[]
for i in range(6):
    images.append(0)
for i in range(6):
    images[i]=Image.open('planes/samolot0'+str(i)+'.jpg')"""

#im = images[0]
#for i in range(6):


i=0
i=str(i)
im = Image.open('planes/samolot0'+i+'.jpg')
im = ImageOps.grayscale(im)
im = im.filter(ImageFilter.GaussianBlur)
im = im.filter(ImageFilter.MedianFilter)
im = im.filter(ImageFilter.FIND_EDGES)
im = im.filter(ImageFilter.MedianFilter)
im.save('new'+i+'.png')
print("zapisano plik "+i)


#images=[feature.canny(image) for image in images]
#arr=[np.asarray(image) for image in images]
#x=np.asarray(images[0])




