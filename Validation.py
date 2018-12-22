import arcpy
class ToolValidator():
  
  def __init__(self):
    import arcpy
    self.params = arcpy.GetParameterInfo()
    return

  def initializeParameters(self):
    # SET DEFAULT TITLE
    self.params[1].value = 3
    self.params[2].value = False
    self.params[3].symbology = "C:\Users\fpcor\Desktop\K-Means-Clustering\centroids.lyr"
    self.params[4].symbology = "C:\Users\fpcor\Desktop\K-Means-Clustering\clusters.lyr"
    self.params[5].symbology = "C:\Users\fpcor\Desktop\K-Means-Clustering\convexhulls.lyr"
    return
  
  def updateParameters(self):
    #If K Optimized is True, don't ask for K
    if self.params[2].value == True:
      self.params[1].enabled = False
    else:
      self.params[1].enabled = True
                                    
  def updateMessages(self):
    #Rasie warning about runtime of K Optimized
    if self.params[2].value == True:
      self.params[2].setWarningMessage("Optimization of K may significant extend tool runtime")
    return
