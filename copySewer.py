import arcpy
import os, sys

arcpy.env.overwriteOutput = True

#Set connection file to SDE
sde = os.path.join(os.path.dirname(sys.argv[0]), 'CCTV.sde')
cctv = os.path.join(sde, 'RPUD.SewerCollectionNetwork')
PU_Regions = os.path.join(sde, 'RPUD.PU_Regions')

#Output file geodatabase
outfile = u'\\\\corfile\Common\Public Utilities\CCTV\CCTV.gdb\SewerCollectionNetwork'

#Set workspace
arcpy.env.workspace = cctv

#Get features from dataset
def getArguments():
  fcList = arcpy.ListFeatureClasses()
  print fcList
  return fcList

#Copy function for pooling
def copy (fc):
  print 'Copying %s' % fc

  outFeatureClass = os.path.join(outfile, fc.split('.')[1])
  arcpy.CopyFeatures_management(fc, outFeatureClass)
  print '%s copyied' % fc

for i in getArguments():
  copy(i)
