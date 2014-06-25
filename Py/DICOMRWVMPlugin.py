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
    #print "DICOMRWVMPlugin __init__()"
    self.loadType = "Real World Value Mapping Plugin"
    self.tags['patientID'] = "0010,0020"
    self.tags['patientName'] = "0010,0010"
    self.tags['patientBirthDate'] = "0010,0030"
    self.tags['patientSex'] = "0010,0040"
    self.tags['patientHeight'] = "0010,1020"
    self.tags['patientWeight'] = "0010,1030"
    
    #self.tags['relatedSeriesSequence'] = "0008,1250"
    self.tags['referencedSeriesSequence'] = "0008,1115"
    
    #self.tags['radioPharmaconStartTime'] = "0018,1072"
    #self.tags['decayCorrection'] = "0054,1102"
    #self.tags['decayFactor'] = "0054,1321"
    #self.tags['frameRefTime'] = "0054,1300"
    #self.tags['radionuclideHalfLife'] = "0018,1075"
    self.tags['contentTime'] = "0008,0033"
    #self.tags['seriesTime'] = "0008,0031" 
    self.tags['contentTime'] = "0008,0033"
    self.tags['triggerTime'] = "0018,1060"
    self.tags['diffusionGradientOrientation'] = "0018,9089"
    self.tags['imageOrientationPatient'] = "0020,0037"
    self.tags['numberOfFrames'] = "0028,0008"


    #self.tags['seriesDescription'] = "0008,103e"
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
    
    #self.tags['referencedImageRWVMappingSeq'] = "0008,1140"
    self.tags['referencedImageRWVMappingSeq'] = "0040,9094"
 
    
    #self.fileLists = []
    self.patientName = ""
    self.patientBirthDate = ""
    self.patientSex = ""
    
    #self.ctTerm = "CT"
    #self.petTerm = "PT"
    
    #slicer.dicomDatabase.setTagsToPrecache(self.tags)

    self.scalarVolumePlugin = slicer.modules.dicomPlugins['DICOMScalarVolumePlugin']()
  
  
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
    print "DICOMRWVMPlugin::examine()"
    
    loadables = []
    rwvList = []
    seriesUIDs = []
    filesByUID = {} # indexed dictionary by uid 
    for fileList in fileLists:
      for dcmFile in fileList:
        if os.path.isfile(dcmFile):
          dicomFile = dicom.read_file(dcmFile)
          if dicomFile.Modality != "RWV":
            seriesUIDs.append(dicomFile.SOPInstanceUID)
            filesByUID[dicomFile.SOPInstanceUID] = fileList
    
    for fileList in fileLists:
      if os.path.isfile(fileList[0]):
        dicomFile = dicom.read_file(fileList[0])
        if dicomFile.Modality == "RWV":
          print "  Modality is RWV"
          # Create loadables from the first file
          dicomFile = dicom.read_file(fileList[0])
          refRWVMSeq = dicomFile.ReferencedImageRealWorldValueMappingSequence
          if refRWVMSeq:
            # Get the Series UID
            for item in refRWVMSeq:
              uid = self.getSeriesUIDFromRWVM(item)
              print "UID: " + uid
              if uid in seriesUIDs:
                print "UID " + uid + " is a loadable series"
                rwvLoadable = DICOMLib.DICOMLoadable()
                rwvmSeq = item.RealWorldValueMappingSequence
                maps = []
                for mapper in rwvmSeq[0]:
                  maps.append(mapper)
                
                units = maps[2].value
                lastValueMapped = maps[3].value
                firstValueMapped = maps[4].value
                intercept = maps[5].value
                slope = maps[6].value
                unitMeanings = []
                for unitMeaning in maps[1][0]:
                  unitMeanings.append(unitMeaning)
                rwvLoadable.name = unitMeanings[2].value       
                rwvLoadable.tooltip = unitMeanings[2].value
                rwvLoadable.confidence = 0.99
                rwvLoadable.slope = slope
                rwvLoadable.files = filesByUID[uid]
                loadables += [rwvLoadable]
    
    loadables = self.prepareLoadableFiles(loadables)         
    return loadables

  def getSeriesUIDFromRWVM(self, refImageSeq):
    """Return the series UID related to this RWVM object """
    imageSeq = refImageSeq.ReferencedImageSequence
    instanceUID = (imageSeq[0])[0x0008,0x1155].value
    return instanceUID
    
  def prepareLoadableFiles(self, loadables):
    subseriesTags = [
        "seriesInstanceUID",
        "contentTime",
        "triggerTime",
        "diffusionGradientOrientation",
        "imageOrientationPatient",
    ]
    #
    # first, look for subseries within this series
    # - build a list of files for each unique value
    #   of each tag
    #
    newLoadables = []
    for loadable in loadables:
      # while looping through files, keep track of their
      # position and orientation for later use
      positions = {}
      orientations = {}
      subseriesFiles = {}
      subseriesValues = {}
      for file in loadable.files:

        # save position and orientation
        positions[file] = slicer.dicomDatabase.fileValue(file,self.tags['position'])
        if positions[file] == "":
          positions[file] = None
        orientations[file] = slicer.dicomDatabase.fileValue(file,self.tags['orientation'])
        if orientations[file] == "":
          orientations[file] = None

        # check for subseries values
        for tag in subseriesTags:
          value = slicer.dicomDatabase.fileValue(file,self.tags[tag])
          if not subseriesValues.has_key(tag):
            subseriesValues[tag] = []
          if not subseriesValues[tag].__contains__(value):
            subseriesValues[tag].append(value)
          if not subseriesFiles.has_key((tag,value)):
            subseriesFiles[tag,value] = []
          subseriesFiles[tag,value].append(file)

      # Pixel data is available, so add the default loadable to the output
      newLoadables.append(loadable)
      
    for loadable in newLoadables:
      #
      # use the first file to get the ImageOrientationPatient for the
      # series and calculate the scan direction (assumed to be perpendicular
      # to the acquisition plane)
      #
      value = slicer.dicomDatabase.fileValue(loadable.files[0], self.tags['numberOfFrames'])
      if value != "":
        loadable.warning = "Multi-frame image. If slice orientation or spacing is non-uniform then the image may be displayed incorrectly. Use with caution."

      validGeometry = True
      ref = {}
      for tag in [self.tags['position'], self.tags['orientation']]:
        value = slicer.dicomDatabase.fileValue(loadable.files[0], tag)
        if not value or value == "":
          loadable.warning = "Reference image in series does not contain geometry information.  Please use caution."
          validGeometry = False
          loadable.confidence = 0.2
          break
        ref[tag] = value

      if not validGeometry:
        continue

      # get the geometry of the scan
      # with respect to an arbitrary slice
      sliceAxes = [float(zz) for zz in ref[self.tags['orientation']].split('\\')]
      x = sliceAxes[:3]
      y = sliceAxes[3:]
      scanAxis = self.cross(x,y)
      scanOrigin = [float(zz) for zz in ref[self.tags['position']].split('\\')]

      #
      # for each file in series, calculate the distance along
      # the scan axis, sort files by this
      #
      sortList = []
      missingGeometry = False
      for file in loadable.files:
        if not positions[file]:
          missingGeometry = True
          break
        position = [float(zz) for zz in positions[file].split('\\')]
        vec = self.difference(position, scanOrigin)
        dist = self.dot(vec, scanAxis)
        sortList.append((file, dist))

      if missingGeometry:
        loadable.warning = "One or more images is missing geometry information"
      else:
        sortedFiles = sorted(sortList, key=lambda x: x[1])
        distances = {}
        loadable.files = []
        for file,dist in sortedFiles:
          loadable.files.append(file)
          distances[file] = dist

        #
        # confirm equal spacing between slices
        # - use variable 'epsilon' to determine the tolerance
        #
        spaceWarnings = 0
        if len(loadable.files) > 1:
          file0 = loadable.files[0]
          file1 = loadable.files[1]
          dist0 = distances[file0]
          dist1 = distances[file1]
          spacing0 = dist1 - dist0
          n = 1
          for fileN in loadable.files[1:]:
            fileNminus1 = loadable.files[n-1]
            distN = distances[fileN]
            distNminus1 = distances[fileNminus1]
            spacingN = distN - distNminus1
            spaceError = spacingN - spacing0
            if abs(spaceError) > self.epsilon:
              spaceWarnings += 1
              loadable.warning = "Images are not equally spaced (a difference of %g in spacings was detected).  Slicer will load this series as if it had a spacing of %g.  Please use caution." % (spaceError, spacing0)
              break
            n += 1

        if spaceWarnings != 0:
          print("Geometric issues were found with %d of the series.  Please use caution." % spaceWarnings)

    return newLoadables

  #
  # math utilities for processing dicom volumes
  # TODO: there must be good replacements for these
  #
  def cross(self, x, y):
    return [x[1] * y[2] - x[2] * y[1],
            x[2] * y[0] - x[0] * y[2],
            x[0] * y[1] - x[1] * y[0]]

  def difference(self, x, y):
    return [x[0] - y[0], x[1] - y[1], x[2] - y[2]]

  def dot(self, x, y):
    return x[0] * y[0] + x[1] * y[1] + x[2] * y[2]
  
  def convertStudyDate(self, fileList):
    """Return a readable study date string """
    studyDate = self.__getSeriesInformation(fileList, self.tags['studyDate'])
    if studyDate:
      if len(studyDate)==8:
        studyDate = studyDate[:4] + '-' + studyDate[4:6] + '-' + studyDate[6:]
    return studyDate
           

  def __seperateFilesListIntoImageSeries(self, files):
    
    imageSeries = {}
    
    for file in files:
      seriesUID = self.__getSeriesInformation([file], self.tags['seriesInstanceUID'])
      
      if (seriesUID in imageSeries) == False:
        imageSeries[seriesUID] = [] 
            
      imageSeries[seriesUID].append(file)  
      
    return imageSeries


  def __seperateImageSeriesAndFilesIntoStudies(self, imageSeriesAndFiles):
    
    studies = {}
    
    for seriesUID in imageSeriesAndFiles.keys():
      
      if len(imageSeriesAndFiles[seriesUID]) == 0:
        continue    
      
      studyUID = self.__getSeriesInformation(imageSeriesAndFiles[seriesUID], self.tags['studyInstanceUID'])   
      
      if (studyUID in studies) == False:
        studies[studyUID] = []
      
      studies[studyUID].append(seriesUID)
    
      
    return studies
    
    
  def __extractSpecificModalitySeriesForStudies(self, studiesAndImageSeries, imageSeriesAndFiles, modality):
    
    seriesForStudies = {}
    
    for studyUID in studiesAndImageSeries.keys():
      
      seriesForStudies[studyUID] = []
        
      seriesList = studiesAndImageSeries[studyUID] 
      
      for seriesUID in seriesList:
        
        if seriesUID in imageSeriesAndFiles.keys():
        
          if len(imageSeriesAndFiles[seriesUID]) == 0:
            continue
        
          if self.__getSeriesInformation(imageSeriesAndFiles[seriesUID], self.tags['seriesModality']) == modality:   
            seriesForStudies[studyUID].append(seriesUID)      

    return seriesForStudies         
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
  
  def __getImageSeriesDescription(self,files):
    
    rows = self.__getSeriesInformation(files, self.tags['rows'])
    columns = self.__getSeriesInformation(files, self.tags['columns'])
    slices = len(files)
    
    spacingRows = self.__getSeriesInformation(files, self.tags['spacing']).split('\\')[0]
    spacingCols = self.__getSeriesInformation(files, self.tags['spacing']).split('\\')[1]
    
    width = int(columns) * float(spacingCols)
    height = int(rows) * float(spacingRows)
    
    seriesTime = self.__getSeriesInformation(files, self.tags['seriesTime'])          
    seriesTime = seriesTime[:2]+":"+seriesTime[2:4]+":"+seriesTime[4:6]
    return "Series Time: "+seriesTime+ " | Width: "+str(width)+"mm | Height: "+str(height)+"mm | Slices: "+str(slices)

  
  def load(self,loadable):
    """Determine the correct conversion factor
    and load the volume into Slicer
    """
    sopInstanceUID = self.__getSeriesInformation(loadable.files, self.tags['sopInstanceUID'])
    seriesDirectory = self.__getDirectoryOfImageSeries(sopInstanceUID)
    
    # Determine the conversion factor
    conversionFactor = loadable.slope
    factorType = (loadable.name).replace(' ','_')
    """parameters = {}
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
      conversionFactor = 1"""
    
    print "  conversionFactor " + str(conversionFactor)
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
    #displayNode.SetAndObserveColorNodeID('vtkMRMLColorTableNodeInvertedGrey')
    
    # Change name
    patientID = self.__getSeriesInformation(loadable.files, self.tags['patientID'])
    studyDate = self.convertStudyDate(loadable.files)
    name = patientID + '_' + studyDate + '_' + factorType
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
    
    return imageNode

  
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
# DICOMRWVMPlugin
#

class DICOMRWVMPlugin:
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


