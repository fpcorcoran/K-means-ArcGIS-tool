# K-means-ArcGIS-tool
This repository contains tool for K means clustering of point shape files in ArcGIS. The tool is optimized using the K means ++ algorithm.
In addition, it includes a tool for calculating the convex hull of each cluster of points, as well as a feature for calculating the average silhouette score of different values of K (still in progress). 

This project was created as part of the requirements for my Geospatial Software Design class at the University of Pennsylvania.The goal of the project is to provide a simple and easy to use clustering tool in ArcGIS, that could be used on point type shapefiles.

Some potential applications of this tool include incident analysis, such as traffic accidents and crime, analysis of well served areas by services such as Airbnb, McDonalds, etc., and many others.


This tool is by no means complete, and will be validated and added to an ArcGIS toolbox in the near future for easier distribution and use.
In the mean time, the files can be cloned and tested by adding the main.py script to a toolbox in ArcGIS. This same script also contains instructions on parameterizing the script.

