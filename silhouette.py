import numpy as np

def silhouette(points):

    #Eucledian Distance Function
    def dist(a, b, ax=1):
        return np.linalg.norm(a-b, axis=ax)

    a={}
    inside={}
    for idx, pts in points.items():
        for i in pts:
            intraclust = [dist(j,pts) for j in pts]
            inside[idx]=[]
            inside[idx]+=intraclust
            a[idx] = np.sum(intraclust[idx])/(len(intraclust[idx])-1)


    b={}  
    outside=[]
    for idx, pts in points.items():
        for idx2, pts2 in points.items():
            if idx != idx2:
                for i in pts:
                    extraclust = [dist(i,j,ax=None) for j in pts2]
                    b[idx] = np.sum(extraclust)/(len(extraclust))
        outside=[]
                        
    silhouette={}
    avg =[]
    for i in range(len(a)):
        silhouette[i]=(b[i]-a[i])/np.max([b[i],a[i]])
        avg += [(b[i]-a[i])/np.max([b[i],a[i]])] 
    avg = np.mean(avg)

    return avg, silhouette
    
