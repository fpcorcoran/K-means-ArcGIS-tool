import numpy as np
from copy import deepcopy

"""
Compute The K-means cluster centroids.
"""
def k_means(X, k, Centroids):

    #Eucledian Distance function 
    def dist(a, b, ax=1):
        return np.linalg.norm(a-b, axis=ax)
    
    #Initiate Centroids from ++ algorithm
    Cxy = Centroids

    #Initialize array for containing previous centroid locations
    C_old = np.zeros(Cxy.shape)

    #Initialize array for assigning points to clusters based on distance
    clusters = np.zeros(len(X))

    #Initialize Error Parameter (distance between previous and new cluster centroids
    error = dist(Cxy, C_old, None)

    #K-Means Clustering Algorithm
    while error >= 0.001:
        #Assignment
        for i in range(len(X)):
            clusters[i] = np.argmin(dist(X[i], Cxy))

        C_old = deepcopy(Cxy)
        
        #Update
        for i in range(k):
            if np.isnan(Cxy[i]).any() == True:
                Cxy[i] = np.array(list(zip(Cx[i]*1.25,Cy[i]*1.25)))
            else:
                points = np.array([X[j] for j in range(len(X)) if clusters[j]==i])
                Cxy[i] = np.mean(points, axis=0)   
        error = dist(Cxy, C_old, None).astype(np.double)

    return Cxy
