import numpy as np

def plusplus(XY,k):

    #Eucledian distance function
    def dist(a, b, ax=1):
        a = a.astype(np.double)
        b = b.astype(np.double)
        return(np.linalg.norm(a-b, axis=ax))

    #Define probabilities proportional to distance
    def weight_prob(Distances):
        probability = []
        for i in range(len(Distances)):
            probability += [Distances[i]/np.sum(Distances)]
        return probability

    #Initialize variable for holding algorithm values
    idx = np.random.choice(np.arange(len(XY)))
    old_centroid = XY[idx]
    distances = []
    centroids = []
    
    for i in range(k):
        centroids += [old_centroid]
        XY = np.delete(XY,idx,axis=0)
        distances += [dist(old_centroid,j,None)**2 for j in XY]
        probabilities = weight_prob(distances)
        idx = np.random.choice(np.arange(len(XY)),p=probabilities)
        old_centroid = XY[idx]
        distances = []
    
    return np.asarray(centroids)
