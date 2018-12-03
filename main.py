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

import arcpy
import numpy as np
from jarvis_march import jarvis_march
from k_means_mod import k_means
from kmeansplusplus import plusplus
from silhouette import silhouette

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
    try:
        k_max = 20
        Silhouettes=[]
        for K in range(2,k_max):
            arcpy.AddMessage("Testing K = "+str(K))
            Centroids = plusplus(X,K)
            Cxy, points = k_means(X,K,Centroids)
            average, sils = silhouette(points)
            Silhouettes.append(average)
        arcpy.AddMessage('\r'+'\n'+"Average Silhouette Values:"+'\n'+'\r')
        arcpy.AddMessage(Silhouettes)
        
    except Exception as e:
        exc_tb = sys.exc_info()[2] #Get Line Number
        arcpy.AddError('\n'
                       +"Error Optimizing K: \n\n\t"+"In line "
                       +str(exc_tb.tb_lineno)+": "+str(e.message)+"\n")
else:      
    #Control for Error in K input
    if k > len(X):
        arcpy.AddError("ERROR: K must be less than or equal to number of points")
        quit()

    try:
        arcpy.AddMessage("Initializing Cluster Centroids...")
        Centroids = plusplus(X, k)
        arcpy.AddMessage("Adjusting Centroid Locations...")
        Cxy, points = k_means(X, k, Centroids)
        
    except Exception as e:
        exc_tb = sys.exc_info()[2] #Get Line Number
        arcpy.AddError('\n'
                       +"Error Computing Centroids: \n\n\t"+"In line "
                       +str(exc_tb.tb_lineno)+": "+str(e.message)+"\n")

    try:
        arcpy.AddMessage("Computing Average Silhouette Value...")
        average, sils = silhouette(points)

    except Exception as e:
        exc_tb = sys.exc_info()[2] #Get Line Number
        arcpy.AddError('\n'
                       +"Error Computing Silhouette: \n\n\t"+"In line "
                       +str(exc_tb.tb_lineno)+": "+str(e.message)+"\n")  

    arcpy.AddMessage(average)
    arcpy.AddMessage(sils)
