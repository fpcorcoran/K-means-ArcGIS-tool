import arcpy
import numpy as np

"""
Compute The K-means cluster centroids.
"""
def k_means(X, k):

    #Eucledian Distance function 
    def dist(a, b, ax=1):
        return np.linalg.norm(a-b, axis=ax)

    #NumPy Vector Between Two Points
    def vector(a,b):
        one = np.array([a[0], a[1]])
        two = np.array([b[0], b[1]])
        return two-one

    #Angle Between Two Vectors
    def angle(v1, v2):
        cos = np.dot(v1, v2)
        sin = np.linalg.norm(np.cross(v1, v2))
        return np.arctan2(sin, cos)
    
    #Randomly Initialize k number of points 
    Cx, Cy = rand.randint(int(np.min(x)), int(np.max(x)), size=k), rand.randint(np.min(y), np.max(y), size=k) 
    Cxy = np.array(list(zip(Cx, Cy)), dtype=np.float32)

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
            points = np.array([X[j] for j in range(len(X)) if clusters[j]==i])
            Cxy[i] = np.mean(points, axis=0)
        error = dist(Cxy, C_old, None)
        
    return Cxy
