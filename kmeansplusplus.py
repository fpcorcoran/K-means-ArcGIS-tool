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
    
    i=0
    while i < k:
        #find squared distances from previous centroid, create probabilities
        distances += [dist(old_centroid,j,None)**2 for j in XY]
        probabilities = weight_prob(distances)

        #Choose new centroid based on probability, controlling for duplicates
        idx = np.random.choice(np.arange(len(XY)),p=probabilities)
        if np.all(centroids != XY[idx]):
            centroids += [old_centroid]
            old_centroid = XY[idx]
            i+=1  
        distances = []
    
    return np.asarray(centroids)
