
def jarvis_march(X,k):
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

    #Dicitonary for holding Vertices of each Convex Hull
    Vertices = {}

    #Initialized Jarvis March Parameters for each cluster
    for i in range(k):
        points = np.array([X[j] for j in range(len(X)) if clusters[j]==i])

        #Minimum and Maximum Points
        X_min = np.where(points == points.min())[0][0]
        X_max = np.where(points == points.max())[0][0]

        #Variables for storing values from each loop
        old_point = points[X_min]
        old_vector = vector(points[X_min], points[X_max])
        angles=[]
        CH = []

        #Jarvis March Algorithm
        while np.any(CH == points[X_min]) == False:
            for l in range(len(points)):
                new_angle = angle(old_vector, vector(old_point, points[l]))
                angles.append(new_angle)
        
            new_point = points[(np.where(angles == max(angles)))][0]
            CH.append(new_point)
            old_vector = vector(new_point, old_point)
            old_point = new_point
            angles = []
        CH.append(CH[0])
        Vertices["Cluster %s" %str(i+1)] = CH
    return CH, Vertices
