import arcpy
import os, sys
import multiprocessing

arcpy.env.overwriteOutput = True

#Set connection file to SDE
cctv = os.path.join(os.path.dirname(sys.argv[0]), 'CCTV.gdb/SewerCollectionNetwork')
wake = os.path.join(os.path.dirname(sys.argv[0]), 'WAKE_READ_ONLY.sde')
directory = 'C:/Data'
#Output file geodatabase
outfile = os.path.join('C:/Data', 'CCTV.gdb/SewerCollectionNetwork')
baseData = os.path.join('C:/Data', 'CCTV.gdb/BaseMap')
#Checkbox argument that determines if base map features are updated
baseMap = sys.argv[1] #true/false
baseLayers = ['WAKE.STREET', 'WAKE.JURISDICTION', 'WAKE.PROPERTY_A']

#Set workspace
arcpy.env.workspace = cctv

#Get features from dataset
def getArguments():
  fcList = arcpy.ListFeatureClasses()
  return fcList

#Copy function for pooling
def copy (fc):
  arcpy.AddMessage('Copying %s' % fc)
  outFeatureClass = os.path.join(outfile, fc)
  arcpy.CopyFeatures_management(fc, outFeatureClass)

#Changes the workspace in the "CURRENT" map
def changeWorkSpace (ws):
  desc = arcpy.Describe(ws)

  workspaceTypes = {
        'esriDataSourcesGDB.AccessWorkspaceFactory.1': 'ACCESS_WORKSPACE',
        'esriDataSourcesGDB.FileGDBWorkspaceFactory.1': 'FILEGDB_WORKSPACE',
        'esriDataSourcesGDB.SdeWorkspaceFactory.1': 'SDE_WORKSPACE',
        '': 'SHAPEFILE_WORKSPACE'
        }

  mxd = arcpy.mapping.MapDocument('CURRENT')
  wsTpye = workspaceTypes[desc.workspaceFactoryProgID]
  for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports('dataSource') and lyr.isFeatureLayer:
      try:
        if lyr.name not in baseLayers:
          lyr.replaceDataSource(ws, wsTpye)
          arcpy.AddMessage('%s Data Source Updated' % lyr.name)
      except:
        pass
  arcpy.RefreshTOC()

def refresh():
  #Checks for directory
  if not os.path.exists(directory):
    os.makedirs(directory)
  #Check if .gdb exists and creates one if it doesn't
  if not arcpy.Exists(outfile):
    arcpy.CreateFileGDB_management("C:/Data", "CCTV.gdb")
    arcpy.CreateFeatureDataset_management("C:/Data/CCTV.gdb", "SewerCollectionNetwork")
  #Secondary check to ensure .gdb was creatred
  if arcpy.Exists(outfile):
    for i in getArguments():
      copy(i)

  #Runs if update basemap option is set to true
  if baseMap:
    #Creates dataset if it doesn't exist
    if not arcpy.Exists(baseData):
      arcpy.CreateFeatureDataset_management("C:/Data/CCTV.gdb", "BaseMap")

    #Change workspace to wake read only
    arcpy.env.workspace = wake
    
    #Copies feature classes to dataset
    for b in baseLayers:
      arcpy.AddMessage('Copying %s' % b)
      outFeatureClass = os.path.join(baseData, b)
      arcpy.CopyFeatures_management(b, outFeatureClass)

    #Change workspace back to cctv
    arcpy.env.workspace = cctv


  #Sets the changes the current map document to new workspace
  changeWorkSpace("C:/Data/CCTV.gdb")

refresh()
