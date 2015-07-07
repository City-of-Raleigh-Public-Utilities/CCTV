import arcpy
import os, sys
import multiprocessing

arcpy.env.overwriteOutput = True

#Set connection file to SDE
cctv = os.path.join(os.path.dirname(sys.argv[0]), 'CCTV.gdb/SewerCollectionNetwork')
directory = 'C:/Data'
#Output file geodatabase
outfile = os.path.join('C:/Data', 'CCTV.gdb/SewerCollectionNetwork')

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
  ignore = ['WAKE.STREET', 'WAKE.JURISDICTION', 'RPUD.PU_Regions']
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
        if lyr.name not in ignore:
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

  #Sets the changes the current map document to new workspace
  changeWorkSpace("C:/Data/CCTV.gdb")

refresh()
