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
    self.loadType = "PET SUV Volume"
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
    #print "DICOMPETSUVPlugin::examine()"
    
    loadables = []
    scalarVolumeLoadables = []
    for fileList in fileLists:
      scalarVolumeLoadables.extend(self.scalarVolumePlugin.examineFiles(fileList))
    
    # First search for Real World Value Mapping objects 
    rwvLoadables = [] 
    for loadable in scalarVolumeLoadables:
      dicomFile = dicom.read_file(loadable.files[0])
      if dicomFile.Modality == "RWV":
        rwvLoadables = self.rwvPlugin.examineLoadables(scalarVolumeLoadables)
        break # only needed once
    for loadable in rwvLoadables:
      loadable.confidence = 1.0
      if loadable.name == "Standardized Uptake Value body weight":
        loadable.selected = True
    if rwvLoadables:
      loadables.extend(rwvLoadables)
    
    # Remove any loadables that are not PET or have a RWVM loadable
    for loadable in scalarVolumeLoadables:
      dicomFile = dicom.read_file(loadable.files[0])
      if dicomFile.Modality == "PT":
        for rwvLoadable in rwvLoadables:
          if dicomFile.SeriesInstanceUID == rwvLoadable.referencedSeriesInstanceUID:
            if loadable in scalarVolumeLoadables: 
              scalarVolumeLoadables.remove(loadable)
      else:
        if loadable in scalarVolumeLoadables:
          scalarVolumeLoadables.remove(loadable)
      
    # Call SUV Factor Calculator module on remaining PET loadables
    petLoadables = self.generateRWVM(scalarVolumeLoadables)
    print ''
    print '                               petLoadables: ' + str(len(scalarVolumeLoadables))
    newRWVLoadables = self.rwvPlugin.examineLoadables(petLoadables)
    print '                            newRWVLoadables: ' + str(len(scalarVolumeLoadables))
    print ''
    for loadable in newRWVLoadables:
      loadable.confidence = 1.0
      if loadable.name == "Standardized Uptake Value body weight":
        loadable.selected = True
    if newRWVLoadables:
      loadables.extend(newRWVLoadables)
    
    #loadables.extend(self.rwvPlugin.examineLoadables(petLoadables))
    print '                           total returned loadables: ' + str(len(loadables))
    return loadables
    
  def generateRWVM(self, loadables):
    """Return a new list of loadables after generating Real World Value Mapping
    objects for each loadable
    """
    newLoadables = []
    for loadable in loadables:
      dicomFile = dicom.read_file(loadable.files[0])
      if dicomFile.Modality == "PT":
        # Call SUV Factor Calculator module
        sopInstanceUID = self.__getSeriesInformation(loadable.files, self.tags['sopInstanceUID'])
        seriesDirectory = self.__getDirectoryOfImageSeries(sopInstanceUID)
        
        parameters = {}
        parameters['PETDICOMPath'] = seriesDirectory
        parameters['RWVDICOMPath'] = seriesDirectory
        SUVFactorCalculator = None
        SUVFactorCalculator = slicer.cli.run(slicer.modules.suvfactorcalculator, SUVFactorCalculator, parameters, wait_for_completion=True)
        
        rwvFile = SUVFactorCalculator.GetParameterDefault(1,19)
        # Create new loadable for this rwvFile
        rwvLoadable = DICOMLib.DICOMLoadable()
        rwvLoadable.files = [rwvFile]
        newLoadables.append(rwvLoadable)

        slicer.dicomDatabase.insert(rwvFile,False,False,False,os.path.dirname(rwvFile))
    
    return newLoadables
    
       
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
    return self.rwvPlugin.load(loadable)
      

class PETCTSeriesSelectorDialog(object):
  
  def __init__(self, parent=None, studyDescription="",petDescriptions=[],ctDescriptions=[],petSelection=0,ctSelection=0):
    
    self.studyDescription = studyDescription
    self.petDescriptions = petDescriptions
    self.ctDescriptions = ctDescriptions  
    self.petSelection = petSelection
    self.ctSelection = ctSelection
    
    if not parent:
      self.parent = qt.QDialog()
      self.parent.setModal(True)
      self.parent.setLayout(qt.QGridLayout())
      self.layout = self.parent.layout()
      self.setup()
      self.parent.show()
      
    else:
      self.parent = parent
      self.layout = parent.layout() 
      
  
  def setup(self):
      
    self.studyLabel = qt.QLabel(self.studyDescription)
    self.studyLabel.setAlignment(qt.Qt.AlignCenter)
    self.petLabel = qt.QLabel("PET Image Series")
    self.petLabel.setAlignment(qt.Qt.AlignCenter)
    self.ctLabel = qt.QLabel("CT Image Series")
    self.ctLabel.setAlignment(qt.Qt.AlignCenter)
    self.petList = qt.QListWidget()
    self.petList.addItems(self.petDescriptions)
    self.petList.setCurrentRow(self.petSelection)
    self.ctList = qt.QListWidget()
    self.ctList.addItems(self.ctDescriptions)
    self.ctList.setCurrentRow(self.ctSelection)
    self.button = qt.QPushButton("Ok")
    
    self.layout.addWidget(self.studyLabel,0,0,1,2)
    self.layout.addWidget(self.petLabel,1,0,1,1)
    self.layout.addWidget(self.ctLabel,1,1,1,1)
    self.layout.addWidget(self.petList,2,0,1,1)
    self.layout.addWidget(self.ctList,2,1,1,1)
    self.layout.addWidget(self.button,3,0,1,2)
    
    self.button.connect('clicked()',self.parent.close)    
      

  def getSelectedSeries(self):
    return [self.petList.currentRow, self.ctList.currentRow]              
          
          
  
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


