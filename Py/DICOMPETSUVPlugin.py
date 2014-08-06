import os
import sys as SYS
from __main__ import vtk, qt, ctk, slicer
from DICOMLib import DICOMPlugin
from DICOMLib import DICOMLoadable


import DICOMLib

import math as math

#
# This is the plugin to handle PET SUV volumes
# from DICOM files into MRML nodes.  It follows the DICOM module's
# plugin architecture.
#

class DICOMPETSUVPluginClass(DICOMPlugin):
  """ PET specific interpretation code
  """

  def __init__(self):
    super(DICOMPETSUVPluginClass,self).__init__()
    
    #print "DICOMPETSUVPlugin __init__()"
    self.loadType = "PET SUV Plugin"
    self.tags['patientID'] = "0010,0020"
    self.tags['patientName'] = "0010,0010"
    self.tags['patientBirthDate'] = "0010,0030"
    self.tags['patientSex'] = "0010,0040"
    self.tags['patientHeight'] = "0010,1020"
    self.tags['patientWeight'] = "0010,1030"
    
    self.tags['relatedSeriesSequence'] = "0008,1250"
    
    self.tags['radioPharmaconStartTime'] = "0018,1072"
    self.tags['decayCorrection'] = "0054,1102"
    self.tags['decayFactor'] = "0054,1321"
    self.tags['frameRefTime'] = "0054,1300"
    self.tags['radionuclideHalfLife'] = "0018,1075"
    self.tags['contentTime'] = "0008,0033"
    self.tags['seriesTime'] = "0008,0031" 


    self.tags['seriesDescription'] = "0008,103e"
    self.tags['seriesModality'] = "0008,0060"
    self.tags['seriesInstanceUID'] = "0020,000E"
    self.tags['sopInstanceUID'] = "0008,0018"
  
    self.tags['studyInstanceUID'] = "0020,000D"
    self.tags['studyDate'] = "0008,0020"
    self.tags['studyTime'] = "0008,0030"
    self.tags['studyID'] = "0020,0010"
    
    self.tags['rows'] = "0028,0010"
    self.tags['columns'] = "0028,0011"
    self.tags['spacing'] = "0028,0030"
    self.tags['position'] = "0020,0032"
    self.tags['orientation'] = "0020,0037"
    self.tags['pixelData'] = "7fe0,0010"
    
    self.tags['referencedImageRWVMappingSeq'] = "0008,1140"
 
    
    self.fileLists = []
    self.patientName = ""
    self.patientBirthDate = ""
    self.patientSex = ""
    
    self.ctTerm = "CT"
    self.petTerm = "PT"

    self.scalarVolumePlugin = slicer.modules.dicomPlugins['DICOMScalarVolumePlugin']()
    self.rwvPlugin = slicer.modules.dicomPlugins['DICOMRWVMPlugin']()
    
    self.rwvmList = []
    self.rwvmListCreated = False
    self.rwvmListModified = False
    #self.rwvmReferencedUIDList = []
  
  
  def __getDirectoryOfImageSeries(self, sopInstanceUID):
    f = slicer.dicomDatabase.fileForInstance(sopInstanceUID)
    return os.path.dirname(f)  
    

  def __getSeriesInformation(self,seriesFiles,dicomTag):
    if seriesFiles:
      return  slicer.dicomDatabase.fileValue(seriesFiles[0],dicomTag)          


  def examine(self,fileLists):
    """ Returns a list of DICOMLoadable instances
    corresponding to ways of interpreting the
    fileLists parameter.
    """
    loadables = []
    # generate the Real World Value Mapping object list
    if not self.rwvmListCreated:
      for dicomFile in slicer.dicomDatabase.allFiles():
        if slicer.dicomDatabase.fileValue(dicomFile,self.tags['seriesModality']) == "RWV":
          self.rwvmList.append(dicomFile)
      self.rwvmListCreated = True
    
    # get from cache or create new loadables using ScalarVolumePlugin
    for fileList in fileLists:
      cachedLoadables = self.getCachedLoadables(fileList)
      if cachedLoadables:
        loadables += cachedLoadables
      else:
        modality = slicer.dicomDatabase.fileValue(fileList[0],self.tags['seriesModality'])
        if modality == "PT":
          # check if PET series already has Real World Value Mapping
          hasRWVM = False
          dicomFile = dicom.read_file(fileList[0])
          for rwvm in self.rwvmList:
            if dicomFile.SeriesInstanceUID == self.getReferencedSeriesInstanceUID(rwvm):
              hasRWVM = True
              loadablesForFiles = self.rwvPlugin.getLoadablesFromRWVMFile([rwvm])
              for loadable in loadablesForFiles:
                loadable.confidence = 1.0
                if "Standardized Uptake Value body weight" in loadable.name:
                  loadable.selected = True
              loadables += loadablesForFiles
              self.cacheLoadables(fileList,loadablesForFiles)
              break
          if not hasRWVM:
            # Call SUV Factor Calculator to create RWVM loadables for this PET series
            rwvmFile = self.generateRWVMforFileList(fileList)
            loadablesForFiles = self.rwvPlugin.getLoadablesFromRWVMFile([rwvmFile])
            for loadable in loadablesForFiles:
              loadable.confidence = 1.0
              if "Standardized Uptake Value body weight" in loadable.name:
                loadable.selected = True
            loadables += loadablesForFiles
            self.cacheLoadables(fileList,loadablesForFiles)
        elif modality == "RWV":
          # ignore...DICOMRWVMPlugin should catch these
          """# Create loadables but with a lower confidence
          loadablesForFiles = self.rwvPlugin.getLoadablesFromRWVMFile(fileList)
          for loadable in loadablesForFiles:
            loadable.confidence = 0.95
          loadables += loadablesForFiles
          self.cacheLoadables(fileList,loadablesForFiles)"""

    return loadables
    
  
  def generateRWVMforFileList(self, fileList):
    """Return a list of loadables after generating Real World Value Mapping
    objects for a PET series
    """
    loadables = []
    # Call SUV Factor Calculator module
    sopInstanceUID = self.__getSeriesInformation(fileList, self.tags['sopInstanceUID'])
    seriesDirectory = self.__getDirectoryOfImageSeries(sopInstanceUID)
    
    parameters = {}
    parameters['PETDICOMPath'] = seriesDirectory
    parameters['RWVDICOMPath'] = seriesDirectory
    SUVFactorCalculator = None
    SUVFactorCalculator = slicer.cli.run(slicer.modules.suvfactorcalculator, SUVFactorCalculator, parameters, wait_for_completion=True)
    
    rwvFile = SUVFactorCalculator.GetParameterDefault(1,19)
    self.rwvmList.append(rwvFile)

    return rwvFile

    
  def getReferencedSeriesInstanceUID(self, rwvmFile):
    """Helper method to read the Referenced Series Instance UID from an RWVM file"""
    dicomFile = dicom.read_file(rwvmFile)
    refSeriesSeq = dicomFile.ReferencedSeriesSequence
    return refSeriesSeq[0].SeriesInstanceUID
  
       
  def convertStudyDate(self, fileList):
    """Return a readable study date string """
    studyDate = self.__getSeriesInformation(fileList, self.tags['studyDate'])
    if studyDate:
      if len(studyDate)==8:
        studyDate = studyDate[:4] + '-' + studyDate[4:6] + '-' + studyDate[6:]
    return studyDate
           

  def load(self,loadable):
    """Call the DICOMRWVMPlugin to load
    the series into Slicer
    """    
    print loadable.derivedItems
    return self.rwvPlugin.load(loadable)

  
#
# DICOMPETSUVPlugin
#

class DICOMPETSUVPlugin:
  """
  This class is the 'hook' for slicer to detect and recognize the plugin
  as a loadable scripted module
  """
  def __init__(self, parent):
    parent.title = "DICOM PET SUV Volume Plugin"
    parent.categories = ["Developer Tools.DICOM Plugins"]
    parent.contributors = ["Ethan Ulrich (Univ. of Iowa)"]
    parent.helpText = """
    Plugin to the DICOM Module to parse and load PET volumes
    from DICOM files. Provides options for standardized uptake values.
    No module interface here, only in the DICOM module
    """
    parent.acknowledgementText = """
    This DICOM Plugin was developed by
    Ethan Ulrich, Univ. of Iowa
    and was partially funded by NIH grant U24 CA180918.
    """

    # don't show this module - it only appears in the DICOM module
    parent.hidden = True

    # Add this extension to the DICOM module's list for discovery when the module
    # is created.  Since this module may be discovered before DICOM itself,
    # create the list if it doesn't already exist.
    try:
      slicer.modules.dicomPlugins
    except AttributeError:
      slicer.modules.dicomPlugins = {}
    slicer.modules.dicomPlugins['DICOMPETSUVPlugin'] = DICOMPETSUVPluginClass

#
# DICOMPETSUVWidget
#

class DICOMPETSUVWidget:
  def __init__(self, parent = None):
    self.parent = parent

  def setup(self):
    # don't display anything for this widget - it will be hidden anyway
    pass

  def enter(self):
    pass

  def exit(self):
    pass


