import os
import sys as SYS
import dicom
from __main__ import vtk, qt, ctk, slicer
from DICOMLib import DICOMPlugin
from DICOMLib import DICOMLoadable


import DICOMLib

import math as math

#
# This is the plugin to handle Real World Value Mapping objects
# from DICOM files into MRML nodes.  It follows the DICOM module's
# plugin architecture.
#

class DICOMRWVMPluginClass(DICOMPlugin):
  """ PET specific interpretation code
  """

  def __init__(self):
    super(DICOMRWVMPluginClass,self).__init__()
    self.epsilon = 0.01
    self.loadType = "Real World Value Mapping Plugin"
    self.tags['patientID'] = "0010,0020"
    self.tags['patientName'] = "0010,0010"
    self.tags['patientBirthDate'] = "0010,0030"
    self.tags['patientSex'] = "0010,0040"
    self.tags['patientHeight'] = "0010,1020"
    self.tags['patientWeight'] = "0010,1030"
    
    self.tags['referencedSeriesSequence'] = "0008,1115"
    
    self.tags['contentTime'] = "0008,0033"
    self.tags['seriesTime'] = "0008,0031" 
    self.tags['triggerTime'] = "0018,1060"
    self.tags['diffusionGradientOrientation'] = "0018,9089"
    self.tags['imageOrientationPatient'] = "0020,0037"
    self.tags['numberOfFrames'] = "0028,0008"

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

    self.tags['referencedImageRWVMappingSeq'] = "0040,9094"
 
    
    #self.fileLists = []
    #self.patientName = ""
    #self.patientBirthDate = ""
    #self.patientSex = ""

    self.scalarVolumePlugin = slicer.modules.dicomPlugins['DICOMScalarVolumePlugin']()
    #self.filesByUID = {} # indexed dictionary by uid 
  
  
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
    scalarVolumeLoadables = []
    for fileList in fileLists:
      scalarVolumeLoadables.extend(self.scalarVolumePlugin.examineFiles(fileList))
      
    loadables = self.examineLoadables(scalarVolumeLoadables)
    return loadables

  
  def examineLoadables(self, loadables):
    """ Returns a new list of DICOMLoadable instances
    that are associated with RWVM objects.
    """
    newLoadables = []
    for loadable in loadables:
      dicomFile = dicom.read_file(loadable.files[0])
      if dicomFile.Modality == "RWV":
        refRWVMSeq = dicomFile.ReferencedImageRealWorldValueMappingSequence
        refSeriesSeq = dicomFile.ReferencedSeriesSequence
        if refRWVMSeq:
          # May have more than one RWVM value
          for item in refRWVMSeq:
            rwvLoadable = DICOMLib.DICOMLoadable()
            # Get the referenced files from the database
            refImageSeq = item.ReferencedImageSequence
            instanceFiles = []
            for instance in refImageSeq:
              uid = instance.ReferencedSOPInstanceUID
              if uid:
                instanceFiles += [slicer.dicomDatabase.fileForInstance(uid)]
            instanceFiles.sort()
            # Get the Real World Values
            rwvLoadable.files = instanceFiles
            rwvmSeq = item.RealWorldValueMappingSequence
            unitsSeq = rwvmSeq[0].MeasurementUnitsCodeSequence
            rwvLoadable.name = unitsSeq[0].CodeMeaning
            rwvLoadable.tooltip = unitsSeq[0].CodeMeaning
            rwvLoadable.units = unitsSeq[0].CodeValue
            rwvLoadable.confidence = 0.95
            rwvLoadable.slope = rwvmSeq[0].RealWorldValueSlope
            rwvLoadable.referencedSeriesInstanceUID = refSeriesSeq[0].SeriesInstanceUID
            newLoadables.append(rwvLoadable)
            
    return newLoadables
  
  
  def convertStudyDate(self, fileList):
    """Return a readable study date string """
    studyDate = self.__getSeriesInformation(fileList, self.tags['studyDate'])
    if studyDate:
      if len(studyDate)==8:
        studyDate = studyDate[:4] + '-' + studyDate[4:6] + '-' + studyDate[6:]
    return studyDate
           
  
  def load(self,loadable):
    """Use the conversion factor to load the volume into Slicer"""
    sopInstanceUID = self.__getSeriesInformation(loadable.files, self.tags['sopInstanceUID'])
    seriesDirectory = self.__getDirectoryOfImageSeries(sopInstanceUID)

    conversionFactor = loadable.slope
    factorType = (loadable.name).replace(' ','_')

    # Create volume node
    imageNode = self.scalarVolumePlugin.load(loadable)
    multiplier = vtk.vtkImageMathematics()
    multiplier.SetOperationToMultiplyByK()
    multiplier.SetConstantK(float(conversionFactor))
    multiplier.SetInput1Data(imageNode.GetImageData())
    multiplier.Update()
    imageNode.GetImageData().DeepCopy(multiplier.GetOutput())
    
    volumeLogic = slicer.modules.volumes.logic()
    appLogic = slicer.app.applicationLogic()
    selNode = appLogic.GetSelectionNode()
    selNode.SetReferenceActiveVolumeID(imageNode.GetID())
    appLogic.PropagateVolumeSelection()
    
    # Change display
    displayNode = imageNode.GetVolumeDisplayNode()
    displayNode.SetInterpolate(0)
    
    # Change name
    patientID = self.__getSeriesInformation(loadable.files, self.tags['patientID'])
    studyDate = self.convertStudyDate(loadable.files)
    name = patientID.replace(' ','_') + '_' + studyDate + '_' + factorType
    imageNode.SetName(name)
    
    # Set Attributes
    patientName = self.__getSeriesInformation(loadable.files, self.tags['patientName'])
    patientBirthDate = self.__getSeriesInformation(loadable.files, self.tags['patientBirthDate'])
    patientSex = self.__getSeriesInformation(loadable.files, self.tags['patientSex'])
    patientHeight = self.__getSeriesInformation(loadable.files, self.tags['patientHeight'])
    patientWeight = self.__getSeriesInformation(loadable.files, self.tags['patientWeight'])
    
    imageNode.SetAttribute('DICOM.PatientID', patientID)  
    imageNode.SetAttribute('DICOM.PatientName', patientName)
    imageNode.SetAttribute('DICOM.PatientBirthDate', patientBirthDate)
    imageNode.SetAttribute('DICOM.PatientSex', patientSex)
    imageNode.SetAttribute('DICOM.PatientHeight', patientHeight)
    imageNode.SetAttribute('DICOM.PatientWeight', patientWeight)
    imageNode.SetAttribute('VolumeType',loadable.name)
    imageNode.SetAttribute('PixelUnits',loadable.units)
    
    return imageNode
          
  
#
# DICOMRWVMPlugin
#

class DICOMRWVMPlugin:
  """
  This class is the 'hook' for slicer to detect and recognize the plugin
  as a loadable scripted module
  """
  def __init__(self, parent):
    parent.title = "DICOM Real World Value Mapping Plugin"
    parent.categories = ["Developer Tools.DICOM Plugins"]
    parent.contributors = ["Ethan Ulrich (Univ. of Iowa), Paul Mercea (Univ. of Heidelberg), Andrey Fedorov (BWH)"]
    parent.helpText = """
    Plugin to the DICOM Module to parse and load DICOM series associated with 
    Real World Value Mapping objects. Provides options for standardized uptake values.
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
    slicer.modules.dicomPlugins['DICOMRWVMPlugin'] = DICOMRWVMPluginClass

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


