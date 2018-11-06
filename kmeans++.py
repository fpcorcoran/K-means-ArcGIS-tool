#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 18:57:00 2018

@author: forrest
"""

import numpy as np
import matplotlib.pyplot as plt

x =[0,10,3,4,22,100,110,25,98,17,7,120,101,95,120,109,101,0,7,15]
y = [9,2,4,100,40,68,2,10,101,115,0,98,100,95,0,8,15,99,115,99]

XY = np.array(list(zip(x,y)))

k = 4

def dist(a, b, ax=1):
    a = a.astype(np.double)
    b = b.astype(np.double)
    return(np.linalg.norm(a-b, axis=ax))

def kmeans_plusplus(XY,k):

    def weight_prob(Distances):
        probability = []
        for i in range(len(Distances)):
            probability += [Distances[i]/np.sum(Distances)]
        return probability
    
    idx = np.random.choice(np.arange(len(XY)))
    old_centroid = XY[idx]
    distances = []
    centroids = []
    i=0
    while i < k:
        distances += [dist(old_centroid,j,None)**2 for j in XY]
        probabilities = weight_prob(distances)
        
        idx = np.random.choice(np.arange(len(XY)),p=probabilities)
        if np.all(centroids != XY[idx]):
            centroids += [old_centroid]
            old_centroid = XY[idx]
            i+=1  
        distances = []
    
    return centroids

centroids = kmeans_plusplus(XY,k)
    
print(centroids)

Cx = []
Cy = []
for pts in centroids:
    Cx += [pts[0]]
    Cy += [pts[1]]
    
plt.scatter(x,y,c='b')
plt.scatter(Cx,Cy,c='r')
