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

  #def __scanForRealWorldValueMappingObject(self,fileLists):

  def __scanForValidPETSeries(self,fileLists):
    
    #petStudies = set()
    
    petSeriesList = []
    
    for fileList in fileLists:
    
      studyUID = self.__getSeriesInformation(fileList, self.tags['studyInstanceUID'])
      modality = self.__getSeriesInformation(fileList, self.tags['seriesModality'])  
    
      if modality == self.petTerm:
        #petStudies.add(studyUID)
        petSeriesList.append(studyUID)
            
    #for stdUID in petStudies:
      #petSeries.append(stdUID)       
    print "  Found "+ str(len(petSeriesList)) +" PET series"
    return petSeriesList
       

  def examine(self,fileLists):
    """ Returns a list of DICOMLoadable instances
    corresponding to ways of interpreting the
    fileLists parameter.
    """
    print "DICOMPETSUVPlugin::examine()"
    
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
    loadables.extend(self.rwvPlugin.examineLoadables(petLoadables))
    
    return loadables
    
  def generateRWVM(self, loadables):
    """Return a new list of loadables after generating Real World Value Mapping
    objects for each loadable
    """
    newLoadables = []
    for loadable in loadables:
      # Call SUV Factor Calculator module
      sopInstanceUID = self.__getSeriesInformation(loadable.files, self.tags['sopInstanceUID'])
      seriesDirectory = self.__getDirectoryOfImageSeries(sopInstanceUID)
      
      parameters = {}
      parameters['PETDICOMPath'] = seriesDirectory
      parameters['RWVDICOMPath'] = seriesDirectory
      SUVFactorCalculator = None
      SUVFactorCalculator = slicer.cli.run(slicer.modules.suvfactorcalculator, SUVFactorCalculator, parameters, wait_for_completion=True)
      
      rwvFile = SUVFactorCalculator.GetParameterDefault(2,19)
      # Create new loadable for this rwvFile
      rwvLoadable = DICOMLib.DICOMLoadable()
      rwvLoadable.files = [rwvFile]
      newLoadables.append(rwvLoadable)
      
      #TODO add to DICOM Browser!  Else an RWMV will be genereated each time
      #self.addRWMVToDatabase(rwvFile)
    
    return newLoadables
    
  def addRWMVToDatabase(self, rwvFile):
    indexer = ctk.ctkDICOMIndexer()
    destinationDir = os.path.dirname(slicer.dicomDatabase.databaseFilename)
    indexer.addFile( slicer.dicomDatabase, rwvFile, destinationDir )
    slicer.util.showStatusMessage("Loaded: %s" % rwvFile, 1000)
    
    """newLoadables = []  
    for loadable in loadables:
      bwLoadable = DICOMLib.DICOMLoadable()
      bwLoadable.name = " PET SUV(bw) Image"
      bwLoadable.tooltip = "PET Standardized Uptake Value (body weight) Image"
      bwLoadable.confidence = 0.99
      bsaLoadable = DICOMLib.DICOMLoadable()
      bsaLoadable.name = " PET SUV(bsa) Image"
      bsaLoadable.tooltip = "PET Standardized Uptake Value (body surface area) Image"
      bwLoadable.confidence = 0.85
      ibwLoadable = DICOMLib.DICOMLoadable()
      ibwLoadable.name = " PET SUV(ibw) Image"
      ibwLoadable.tooltip = "PET Standardized Uptake Value (ideal body weight) Image"
      bwLoadable.confidence = 0.85
      lbmLoadable = DICOMLib.DICOMLoadable()
      lbmLoadable.name = " PET SUV(lbm) Image"
      lbmLoadable.tooltip = "PET Standardized Uptake Value (lean body mass) Image"
      bwLoadable.confidence = 0.85
      
      if self.hasPatientWeight(loadable.files):
        bwLoadable.files += loadable.files
        if self.hasPatientHeight(loadable.files):
          bsaLoadable.files += loadable.files
          if self.hasPatientSex(loadable.files):
            ibwLoadable.files += loadable.files
            lbmLoadable.files += loadable.files
            
    if bwLoadable.files:
      newLoadables += [bwLoadable]
    if bsaLoadable.files:
      newLoadables += [bsaLoadable]
    if ibwLoadable.files:
      newLoadables += [ibwLoadable]
    if lbmLoadable.files:
      newLoadables += [lbmLoadable]
      
    return newLoadables"""

  def hasPatientWeight(self, fileList):
    """Check for valid PatientWeight tag"""
    pw = self.__getSeriesInformation(fileList, self.tags['patientWeight'])
    return ((pw is not None) and (float(pw) > 0))
    
  def hasPatientHeight(self, fileList):
    """Check for valid PatientHeight tag"""
    ph = self.__getSeriesInformation(fileList, self.tags['patientHeight'])
    return ((ph is not None) and (float(ph) > 0))
    
  def hasPatientSex(self, fileList):
    """Check for valid PatientSex tag"""
    ps = self.__getSeriesInformation(fileList, self.tags['patientSex'])
    return ((ps is not None) and (ps=="M" or ps=="F"))
    
  def convertStudyDate(self, fileList):
    """Return a readable study date string """
    studyDate = self.__getSeriesInformation(fileList, self.tags['studyDate'])
    if studyDate:
      if len(studyDate)==8:
        studyDate = studyDate[:4] + '-' + studyDate[4:6] + '-' + studyDate[6:]
    return studyDate
           

  def load(self,loadable):
    """Determine the correct conversion factor
    and load the volume into Slicer
    """
    
    return self.rwvPlugin.load(loadable)
    
    """sopInstanceUID = self.__getSeriesInformation(loadable.files, self.tags['sopInstanceUID'])
    seriesDirectory = self.__getDirectoryOfImageSeries(sopInstanceUID)
    
    # Determine the conversion factor
    parameters = {}
    parameters['PETDICOMPath'] = seriesDirectory
    SUVFactorCalculator = None
    SUVFactorCalculator = slicer.cli.run(slicer.modules.suvfactorcalculator, SUVFactorCalculator, parameters, wait_for_completion=True)
    
    conversionFactor = 0
    factorType = ''
    if loadable.name == " PET SUV(bw) Image":
      conversionFactor = SUVFactorCalculator.GetParameterDefault(1,14)
      factorType = 'SUV(bw)'
    elif loadable.name == " PET SUV(lbm) Image":
      conversionFactor = SUVFactorCalculator.GetParameterDefault(1,15)
      factorType = 'SUV(lbm)'
    elif loadable.name == " PET SUV(bsa) Image":
      conversionFactor = SUVFactorCalculator.GetParameterDefault(1,16)
      factorType = 'SUV(bsa)'
    elif loadable.name == " PET SUV(ibw) Image":
      conversionFactor = SUVFactorCalculator.GetParameterDefault(1,17)
      factorType = 'SUV(ibw)'
    else:
      conversionFactor = 1
    
    #print "  conversionFactor " + str(conversionFactor)
    # Create volume node
    petNode = self.scalarVolumePlugin.load(loadable)
    multiplier = vtk.vtkImageMathematics()
    multiplier.SetOperationToMultiplyByK()
    multiplier.SetConstantK(float(conversionFactor))
    multiplier.SetInput1(petNode.GetImageData())
    multiplier.Update()
    petNode.GetImageData().DeepCopy(multiplier.GetOutput())
    
    volumeLogic = slicer.modules.volumes.logic()
    appLogic = slicer.app.applicationLogic()
    selNode = appLogic.GetSelectionNode()
    selNode.SetReferenceActiveVolumeID(petNode.GetID())
    appLogic.PropagateVolumeSelection()
    
    # Change display
    displayNode = petNode.GetVolumeDisplayNode()
    displayNode.SetInterpolate(0)
    displayNode.SetAndObserveColorNodeID('vtkMRMLColorTableNodeInvertedGrey')
    
    # Change name
    patientID = self.__getSeriesInformation(loadable.files, self.tags['patientID'])
    studyDate = self.convertStudyDate(loadable.files)
    name = patientID + '_' + studyDate + ' ' + factorType
    petNode.SetName(name)
    
    # Set Attributes
    patientName = self.__getSeriesInformation(loadable.files, self.tags['patientName'])
    patientBirthDate = self.__getSeriesInformation(loadable.files, self.tags['patientBirthDate'])
    patientSex = self.__getSeriesInformation(loadable.files, self.tags['patientSex'])
    patientHeight = self.__getSeriesInformation(loadable.files, self.tags['patientHeight'])
    patientWeight = self.__getSeriesInformation(loadable.files, self.tags['patientWeight'])
    
    petNode.SetAttribute('DICOM.PatientID', patientID)  
    petNode.SetAttribute('DICOM.PatientName', patientName)
    petNode.SetAttribute('DICOM.PatientBirthDate', patientBirthDate)
    petNode.SetAttribute('DICOM.PatientSex', patientSex)
    petNode.SetAttribute('DICOM.PatientHeight', patientHeight)
    petNode.SetAttribute('DICOM.PatientWeight', patientWeight)
    
    return petNode"""
      

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


