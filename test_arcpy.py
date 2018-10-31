"""
THIS SCRIPT IDENTIFIES THE K-MEANS CLUSTER CENTROIDS OF A SHAPEFILE.

To create an ArcToolbox tool with which to execute this script, do the following.
1   In  ArcMap > Catalog > Toolboxes > My Toolboxes, either select an existing toolbox
    or right-click on My Toolboxes and use New > Toolbox to create (then rename) a new one.
2   Drag (or use ArcToolbox > Add Toolbox to add) this toolbox to ArcToolbox.
3   Right-click on the toolbox in ArcToolbox, and use Add > Script to open a dialog box.
4   In this Add Script dialog box, use Label to name the tool being created, and press Next.
5   In a new dialog box, browse to the .py file to be invoked by this tool, and press Next.
6   In the next dialog box, press Finish.

        DISPLAY NAME        DATA TYPE           PROPERTY>DIRECTION>VALUE    PROPERTY>DEFAULT>VALUE
        Input Shapefile     Feature Layer       Input                       
        K                   Long                Input                       3 (Or any integer value)
        Optimize K?         Boolean             Input                       (optional)
        Output Centroids    Shapefile           Output                      
        Output Clusters     Shapefile           Output                      
        Output Zones        Shapefile           Output                      
        
7   To later revise any of this, right-click to the tool's name and select Properties.
"""

import sys, arcpy
import numpy as np
import numpy.random as rand
from copy import deepcopy

arcpy.env.overwriteOutput=True

#Get Parameters (original dataset, number of clusters, spatial reference)
input_points = arcpy.GetParameterAsText(0)
k = int(arcpy.GetParameterAsText(1))
k_optimized = arcpy.GetParameterAsText(2)
spatial_ref = arcpy.Describe(input_points).spatialReference
output_centroids = arcpy.GetParameterAsText(3)
output_clustered = arcpy.GetParameterAsText(4)
output_convexhull = arcpy.GetParameterAsText(5)

#Organize Data as X/Y Coordinates
x = arcpy.da.TableToNumPyArray(input_points, "SHAPE@X").astype(float)
y = arcpy.da.TableToNumPyArray(input_points, "SHAPE@Y").astype(float)
X = np.array(list(zip(x,y)))

#Check for Optimization
if str(k_optimized)=='true':
    arcpy.AddMessage("K Optimization Feature Still in Production")

#Control for Error in K input
if k > len(X):
    arcpy.AddError("ERROR: K must be less than or equal to number of points")
    quit()

"""
Define Functions for K-Means Clustering and Jarvis March.
"""

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

"""
Compute The K-means cluster centroids.
"""

try:
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

except Exception as e:
    arcpy.AddError("\n"+"Error Computing Centroids: \n\n\t"+e.message+"\n")

"""
Compute the Convex Hull using Jarvis March
"""

try:
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
    arcpy.AddMessage(Vertices)
    
except Exception as e:
    exc_tb = sys.exc_info()[2] #Get Line Number
    arcpy.AddError("\n"+"Error Computing Convex Hull: "+e.message+"\n"+"Line:"+str(exc_tb.tb_lineno))

"""
Output Centroids, Clustered Data, Convex Hull
"""

try:    
    #Initialize File Containing Centroids
    CentroidFile = [] 
    Pointfile = arcpy.Point()
    
    #Assign centroid points to X/Y of new shape file
    for pts in Cxy:
        Pointfile.X = float(pts[0])
        Pointfile.Y = float(pts[1])
        pointGeometry = arcpy.PointGeometry(Pointfile,
                                            spatial_ref,
                                            "True")
        CentroidFile.append(pointGeometry)
        
    Polygons = {}
    for i in range(k):
        array = arcpy.Array()
        for pts in Vertices["Cluster %s" %str(i+1)]:
            point = arcpy.Point()
            point.X = float(pts[0])
            point.Y = float(pts[1])
            array.add(point)
        Polygons["Cluster %s" %i] = arcpy.Polygon(array)
        
        
            
    #Create Shapefiles (Centroids & Clusters)
    arcpy.CopyFeatures_management(CentroidFile, output_centroids)
    arcpy.CopyFeatures_management(input_points, output_clustered)
    
    #New Field Containing Cluster Number
    arcpy.AddField_management(output_clustered, "Clust_Num", "SHORT", 5, 5)
    update_records = arcpy.UpdateCursor(output_clustered)

    i = 0
    for NextRecord in update_records:
        NextRecord.setValue("Clust_Num", clusters[i]+1)
        update_records.updateRow(NextRecord)
        i+=1

    del NextRecord
    del update_records


except Exception as e:
    exc_tb = sys.exc_info()[2] #Get Line Number
    arcpy.AddError('\n'
                   +"Error in Outputing File: \n\n\t"+"In line "
                   +str(exc_tb.tb_lineno)+": "+str(e.message)+"\n")  

