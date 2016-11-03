from skimage import data,filters,morphology,color,exposure
from PIL import Image
import numpy as np
#list of images
imgs = ['planes/samolot17.jpg','planes/samolot01.jpg',
        'planes/samolot10.jpg','planes/samolot07.jpg',
        'planes/samolot08.jpg','planes/samolot09.jpg']
###########################
#load images
images=[0,0,0,0,0,0]
for i in range(6):
    images[i] = data.imread(imgs[i])
##############################
#concatenating images
def concat(i1,i2,x):
    h1,w1 = i1.shape[:2]
    h2,w2 = i2.shape[:2]
    if x == 0: #horizontal
        maxh = np.max([h1,h2])
        w = w1+w2
        new = np.zeros(shape=(maxh,w), dtype=np.uint8)
        new[:h1,:w1]=i1
        new[:h2,w1:w1+w2]=i2
        return new
    if x == 1: #vertical
        maxw = np.max([w1,w2])
        h=h1+h2
        new = np.zeros(shape=(h,maxw), dtype = np.uint8)
        new[:h1,:w1]=i1
        new[h1:h1+h2,:w2]=i2
        return new


def supp(img):
    q1=np.percentile(img,25)
    q2=np.median(img)
    q3=np.percentile(img,75)
    return(q1,q2,q3)

def sup2(img):
    (a,b,c)=supp(img)
    h,w=img.shape[:2]
    for row in range(h):
        for value in range(w):
            if img[row][value] < a: img[row][value]=63
            elif img[row][value] < b: img[row][value]= 126
            elif img[row][value] < c: img[row][value] = 200
            else: img[row][value] = 255
    return img

def tresh(img,r):
    h,w=img.shape[:2]
    for row in range(h):
        for value in range(w):
            if img[row][value] < r: img[row][value] = 0;
            elif img[row][value] >= r: img[row][value] = 255;
    return img

##############################
#set variables
tre=137
dil=2
#process images
for i in range(6):
    images[i] = color.rgb2grey(images[i]).copy() #data in range 0-1
    images[i] = filters.gaussian(images[i], 1).copy()
    images[i] = exposure.rescale_intensity(images[i], out_range=(0,255)).copy()
    images[i] = tresh(images[i], tre).copy()
    images[i] = filters.roberts(images[i]).copy()
    for k in range(dil): images[i] = morphology.dilation(images[i])
##############################
#concatenate and write effects to file
image=concat(concat(concat(images[0],images[1],0),concat(images[2],images[3],0),1),concat(images[4],images[5],0),1)
Image.fromarray(image).save('test.jpg')
##############################
