#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from PIL import Image

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True)
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):

            img[:, i] = gradient(v,0)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

def hsv2rgb(h, s, v):
    #h: 0-359, s: 0-1, v: 0-1
    if s==0: return (v,v,v) #greyscale

    main_color = v * s
    sec_color = main_color * (1-abs(((h/60)%2)-1))
    temp = v - main_color
    sec = sec_color+temp

    if h < 60:  return(v,sec,temp) #b>g
    if h < 120: return(sec,v,temp) #b<g
    if h < 180: return(temp,v,sec) #g>r
    if h < 240: return(temp,sec,v) #g<r
    if h < 300: return(sec,temp,v) #b<r
    return(v,temp,sec)             #b>r

def gradient_rgb_bw(v,s):
    return (v,v,v)


def gradient_rgb_gbr(v,s):
    if v <= 0.5: return (0,1-(2*v),v*2)
    return ((v-0.5)*2,0,1-((v-0.5)*2))



def gradient_rgb_gbr_full(v,s):
    if v<=0.25: return(0,1,v*4)
    if v<=0.50: return(0,1-(v-0.25)*4,1)
    if v<=0.75: return ((v-0.5)*4,0,1)
    return(1,0,1-(v-0.75)*4)

def gradient_rgb_wb_custom(v,s):
    if v <= 1/7: return(1,1-v*7,1)
    if v <= 2/7: return(1-(v-1/7)*7,0,1)
    if v <= 3/7: return(0,(v-2/7)*7,1)
    if v <= 4/7: return(0,1,1-(v-3/7)*7)
    if v <= 5/7: return((v-4/7)*7,1,0)
    if v <= 6/7: return(1,1-(v-5/7),0)
    return(1-(v-6/7)*7,0,0)

def gradient_hsv_bw(v,s):
    return hsv2rgb(0, 0, v)

def gradient_hsv_gbr(v,s):
    return hsv2rgb((v*240)+120, 1, 1)

def gradient_hsv_unknown(v,s):
    #120->0 [o]
    return hsv2rgb(120*(1-v), 0.5, 1)

def gradient_hsv_custom(v,s):
    #240 1 1 -> 240   0 1
    if v <= 1/4: return hsv2rgb(240,1-4*v,1)
    #60 0 1 -> 60 1 1
    if v <= 1/2: return hsv2rgb(60,4*v-1,1)
    #60 1 1 -> 60 0 0
    if v <= 3/4: return hsv2rgb(60,1-4*(v-1/2),1-4*(v-1/2))
    #120   0 0 -> 120 1 1
    return hsv2rgb(120,(v-3/4)*4,(v-3/4)*4)

def map_gradient(v,s):
    t=0 #lighter
    if s != 0: t=0.005
    if v <= 5/20: return hsv2rgb(120,0.8-t,0.5+s/20) #ciemnycielony 120
    if v <= 15/20: return hsv2rgb(120, 0.8-t, 0.5+(v-0.25)+s/20) #zielony 120
    if v <= 99/100: return hsv2rgb(120-((v-0.75)/24*6000), 0.8-t, 1+s/20) #¿ó³ty 60
    #if v <= 4/5: return hsv2rgb(60-150*(v-0.6), 0.8, 1) #pomarañczowy 30
    return hsv2rgb(60-200*(v-(99/100)), 0.8-t, 1+s/20) # pom 30

##########################################################
#estimate=[]
#for i in range(0,10):
#    estimate.append(0)
#
#est2 = []
#for i in range(0, 10):
#    est2.append(0)
#
#def esti2(v):
#    for i in range(0,10):
#        if v < (0.9+((i+1)/100)) :
#            est2[i]=est2[i]+1
#            return
#
#def estimating(v):
#    for i in range (0,10):
#        if v < ((i+1)/10):
#            estimate[i]=estimate[i]+1
#            return
#############################################################

shade = []
for i in range (500):
    shade.append([0])
for i in range (498):
    for j in range (500):
        shade[j].append(0)


#file downloaded from
#http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/kolorowanie_mapy/big.dem

with open('big.dem','r') as file:
    x=file.readline().split(' ')
    x[-1]=x[-1][:-2]
    print(x)
    h=int(x[0])
    w=int(x[1])
    l=int(x[2])
    lines=[]
    total=[]

    for line in file:
        line=line.split(' ')
        line=line[1:-2]
        line=[float(temp) for temp in line]
        for point in line:
            lines.append(point/100)
        total.append(lines)
        lines=[]
    print(len(total))
    print(len(total[0]))
    tet=0
    print(len(shade[0]))
    print(len(shade))
    #shadows/light from left 45[o]
    for i in range (0,len(shade)):
        for j in range (0,(len(shade[0])-3)):
            a=total[i][j]
            b=total[i][j+1]
            c=total[i][j+2]
            if abs(b-a)>0.00001:
                shade[i][j+1]=shade[i][j+1]+b-a
            if abs(c-b)>0.00001:
                shade[i][j+1]=shade[i][j+1]+c-b

    m=[]
    n=[]
    for i in range(0,len(total)):
        for j in range(0,len(total[0])):

            m.append(map_gradient(total[i][j],shade[i][j]))
        n.append(m)
        m=[]

    n=np.asarray(n)
    im = plt.imshow(n, aspect='auto')
    im.set_extent([500, 0, 0, 500])
    plt.savefig('map.pdf')





if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom, map_gradient)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
