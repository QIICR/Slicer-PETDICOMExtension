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
    
    #print "DICOMRWVMPlugin __init__()"
    self.loadType = "Real World Value Mapping Plugin"
    self.tags['patientID'] = "0010,0020"
    self.tags['patientName'] = "0010,0010"
    self.tags['patientBirthDate'] = "0010,0030"
    self.tags['patientSex'] = "0010,0040"
    #self.tags['patientHeight'] = "0010,1020"
    #self.tags['patientWeight'] = "0010,1030"
    
    #self.tags['relatedSeriesSequence'] = "0008,1250"
    self.tags['referencedSeriesSequence'] = "0008,1115"
    
    #self.tags['radioPharmaconStartTime'] = "0018,1072"
    #self.tags['decayCorrection'] = "0054,1102"
    #self.tags['decayFactor'] = "0054,1321"
    #self.tags['frameRefTime'] = "0054,1300"
    #self.tags['radionuclideHalfLife'] = "0018,1075"
    self.tags['contentTime'] = "0008,0033"
    #self.tags['seriesTime'] = "0008,0031" 


    #self.tags['seriesDescription'] = "0008,103e"
    self.tags['seriesModality'] = "0008,0060"
    self.tags['seriesInstanceUID'] = "0020,000E"
    self.tags['sopInstanceUID'] = "0008,0018"
  
    self.tags['studyInstanceUID'] = "0020,000D"
    self.tags['studyDate'] = "0008,0020"
    self.tags['studyTime'] = "0008,0030"
    self.tags['studyID'] = "0020,0010"
    
    #self.tags['rows'] = "0028,0010"
    #self.tags['columns'] = "0028,0011"
    #self.tags['spacing'] = "0028,0030"
    #self.tags['position'] = "0020,0032"
    #self.tags['orientation'] = "0020,0037"
    #self.tags['pixelData'] = "7fe0,0010"
    
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
          #if self.__getSeriesInformation(fileList, self.tags['seriesModality']) != "RWV":
            #print dicomFile.SeriesInstanceUID
            #seriesUIDs.append(dicomFile.SeriesInstanceUID)
            seriesUIDs.append(dicomFile.SOPInstanceUID)
            #filesByUID.append(fileList)
            filesByUID[dicomFile.SOPInstanceUID] = fileList
            #print self.__getSeriesInformation(fileList, self.tags['seriesInstanceUID'])
            #seriesUIDs.append(self.__getSeriesInformation(fileList, self.tags['seriesInstanceUID']))
    
    for fileList in fileLists:
      #ds = dicom.read_file(fileList)
      #if ds.Modality == "RWV":
      #if self.__getSeriesInformation(fileList, self.tags['seriesModality']) == "RWV":
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
                #rwvLoadable.files = self.getReferencedSeriesFilesFromUID(seriesUIDs,uid)
                rwvLoadable.files = filesByUID[uid]
                #print "  SLOPE: " + str(rwvLoadable.slope)
                loadables += [rwvLoadable]
        
        """print fileList[0]
        cachedLoadables = self.getCachedLoadables(fileList)
        
        if not cachedLoadables:
          #print "  not cachedLoadables"
          cachedLoadables = self.scalarVolumePlugin.examineFiles(fileList)
          self.cacheLoadables(fileList, cachedLoadables)

        for ldbl in cachedLoadables:
          if ldbl.selected:
            dataset = dicom.read_file(ldbl.files[0])
            refRWVMSeq = dataset.ReferencedImageRealWorldValueMappingSequence            
            if refRWVMSeq:
              for item in refRWVMSeq:
                uids = self.getSeriesUIDsFromRWVM(item)
                files = self.getReferencedSeriesFilesFromUIDs(cachedLoadables,uids)
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
                rwvLoadable.name = unitMeanings[2]         
                rwvLoadable.tooltip = unitMeanings[2]
                rwvLoadable.confidence = 0.99
                rwvLoadable.slope = slope
                #print "  SLOPE: " + str(rwvLoadable.slope)
                loadables += [rwvLoadable]
              
              #rwvList.append(rwvLoadable)
              #loadables += [rwvLoadable]
            if self.hasPatientWeight(fileList):
              bwLoadable.files += ldbl.files
              if self.hasPatientHeight(fileList):
                bsaLoadable.files += ldbl.files
                if self.hasPatientSex(fileList):
                  ibwLoadable.files += ldbl.files
                  lbmLoadable.files += ldbl.files"""
        #self.cacheLoadables(ldbl.files, [ldbl])
        #break
  
    """if bwLoadable.files:
      loadables += [bwLoadable]
    if bsaLoadable.files:
      loadables += [bsaLoadable]
    if ibwLoadable.files:
      loadables += [ibwLoadable]
    if lbmLoadable.files:
      loadables += [lbmLoadable]"""
             
    return loadables

  def getSeriesUIDFromRWVM(self, refImageSeq):
    """Return the series UID related to this RWVM object """
    imageSeq = refImageSeq.ReferencedImageSequence
    instanceUID = (imageSeq[0])[0x0008,0x1155].value
    #for item in imageSeq:
      #uids.append(item[0x0008,0x1155].value)
    #return uids
    return instanceUID
    #uid = ('.').join(instanceUID.split('.')[:-1])
    #return uid
    
  def getReferencedSeriesFilesFromUID(self,seriesUIDs,uids):
    """Return the series files related to a UID"""
    files = []
    #if uid in seriesUIDs:
      
      
    for loadable in cachedLoadables:
      if loadable.selected:
        dataset = dicom.read_file(loadable.files[0])
        seriesInstanceUID = dataset.SeriesInstanceUID
        print seriesInstanceUID
        firstUID = ('.').join(uids[0].split('.')[:-1])
        print ('.').join(uids[0].split('.')[:-1])
        if firstUID == seriesInstanceUID:
          print "TRUE"
          files.append(loadable.files)
          break
        
    return files
   
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
    
    return petNode
    
    """imageSeriesAndFiles = self.__seperateFilesListIntoImageSeries(loadable.files) 
    studiesAndImageSeries = self.__seperateImageSeriesAndFilesIntoStudies(imageSeriesAndFiles)
    
    petImageSeriesInStudies = self.__extractSpecificModalitySeriesForStudies(studiesAndImageSeries, imageSeriesAndFiles, self.petTerm)
    ctImageSeriesInStudies = self.__extractSpecificModalitySeriesForStudies(studiesAndImageSeries, imageSeriesAndFiles, self.ctTerm)
   
    patientID = None  
    patientName = None
    patientBirthDate = None
    patientSex = None
    patientHeight = None 
    
    probeFiles = None
    if imageSeriesAndFiles.keys():
      probeImgSerUID = imageSeriesAndFiles.keys()[0]
      probeFiles =  imageSeriesAndFiles[probeImgSerUID]   
    
    if probeFiles:
      patientID = self.__getSeriesInformation(probeFiles, self.tags['patientID'])
      patientName = self.__getSeriesInformation(probeFiles, self.tags['patientName'])
      patientBirthDate = self.__getSeriesInformation(probeFiles, self.tags['patientBirthDate'])
      patientSex = self.__getSeriesInformation(probeFiles, self.tags['patientSex'])
      patientHeight = self.__getSeriesInformation(probeFiles, self.tags['patientHeight'])
       

    reportNode = None
    
    # import into existing Report node  
    matchingReports = []
    reportNodes = slicer.mrmlScene.GetNodesByClass('vtkMRMLLongitudinalPETCTReportNode')
    reportNodes.SetReferenceCount(reportNodes.GetReferenceCount()-1)
    
    for i in xrange(reportNodes.GetNumberOfItems()):
      rn = reportNodes.GetItemAsObject(i)  
      if (rn.GetAttribute("DICOM.PatientID") == patientID) | ((rn.GetAttribute("DICOM.PatientName") == patientName) & (rn.GetAttribute("DICOM.PatientBirthDate") == patientBirthDate) & (rn.GetAttribute("DICOM.PatientSex") == patientSex)):
        matchingReports.append(i)
   
    if matchingReports:
      selectables = []
      selectables.append("Create new PET/CT Report")
      for id in matchingReports:
        rn = reportNodes.GetItemAsObject(id)
        selectables.append("Import into "+ rn.GetName() + " --- Number of available studies: "+str(rn.GetNumberOfStudyNodeIDs()) )             
      dialogTitle = "Import PET/CT Studies into existing Report"
      dialogLabel = "One or more Reports for the selected Patient already exist!"
      selected = qt.QInputDialog.getItem(None,dialogTitle,dialogLabel,selectables,0,False)  
    
      if (selected in selectables) & (selected != selectables[0]):   
        reportNode = reportNodes.GetItemAsObject(selectables.index(selected)-1)
    
    # create new Report node    
    if not reportNode:        
      reportNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLLongitudinalPETCTReportNode')
      reportNode.SetReferenceCount(reportNode.GetReferenceCount()-1)
      slicer.mrmlScene.AddNode(reportNode)  

      reportNode.SetName("Report for "+patientName)
      reportNode.SetAttribute('DICOM.PatientID', patientID)  
      reportNode.SetAttribute('DICOM.PatientName', patientName)
      reportNode.SetAttribute('DICOM.PatientBirthDate', patientBirthDate)
      reportNode.SetAttribute('DICOM.PatientSex', patientSex)
      reportNode.SetAttribute('DICOM.PatientHeight', patientHeight)


    # setup Report's default color node and table for Finding types
    colorLogic = slicer.modules.colors.logic()
    defaultColorNodeID = colorLogic.GetDefaultEditorColorNodeID()
    colorTableNode = slicer.mrmlScene.GetNodeByID(defaultColorNodeID)
    reportNode.SetColorTableNodeID(colorTableNode.GetID())   
 
    
    for studyUID in studiesAndImageSeries.keys():
      
      if reportNode.IsStudyInReport(studyUID):
        continue      
        
      petDescriptions = [] #petImageSeriesInStudies[studyUID]
      ctDescriptions = []
      studyDescription = None 
      
      for petUID in petImageSeriesInStudies[studyUID]:
        petDescriptions.append(self.__getImageSeriesDescription(imageSeriesAndFiles[petUID]))  
        
        if not studyDescription:
          date = self.__getSeriesInformation(imageSeriesAndFiles[petUID], self.tags['studyDate'])
          date = date[:4]+"."+date[4:6]+"."+date[6:8]
          time = self.__getSeriesInformation(imageSeriesAndFiles[petUID], self.tags['studyTime'])  
          time = time[:2]+":"+time[2:4]+":"+time[4:6]
          studyDescription = "Multiple PET and/or CT image series have been found for the Study from "+date+" "+time+". Please change the selection if a different pair of image series should be loaded." 
            
      
      for ctUID in ctImageSeriesInStudies[studyUID]:
        ctDescriptions.append(self.__getImageSeriesDescription(imageSeriesAndFiles[ctUID]))     
            
      
      selectedIndexes = [0,0]           
     
      if (len(petDescriptions) > 1) | (len(ctDescriptions) > 1):
        dialog = PETCTSeriesSelectorDialog(None,studyDescription,petDescriptions, ctDescriptions, 0, 0)
        dialog.parent.exec_()
        selectedIndexes = dialog.getSelectedSeries()
      
      # UID of current PET series
      petImageSeriesUID = petImageSeriesInStudies[studyUID][selectedIndexes[0]]
      # UID of current CT series 
      ctImageSeriesUID = None
      if ctDescriptions: # for PET only support
        ctImageSeriesUID = ctImageSeriesInStudies[studyUID][selectedIndexes[1]]
      
                    
      # create PET SUV volume node
      petVolumeNode = self.scalarVolumePlugin.load(self.getCachedLoadables(imageSeriesAndFiles[petImageSeriesUID])[0])
      petDir = self.__getDirectoryOfImageSeries(self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['sopInstanceUID']))
      
      parameters = {}
      parameters["PETVolume"] = petVolumeNode.GetID()
      parameters["PETDICOMPath"] = petDir
      parameters["SUVVolume"] = petVolumeNode.GetID()

      
      quantificationCLI = qt.QSettings().value('LongitudinalPETCT/quantificationCLIModule')
      
      if quantificationCLI == None:
        quantificationCLI = "petsuvimagemaker"
       
       
      cliNode = None
      cliNode = slicer.cli.run(getattr(slicer.modules, quantificationCLI), cliNode, parameters) 
      
      # create PET label volume node
      volLogic = slicer.modules.volumes.logic()
      petLabelVolumeNode = volLogic.CreateAndAddLabelVolume(slicer.mrmlScene,petVolumeNode,petVolumeNode.GetName()+"_LabelVolume")
      
      ctVolumeNode = None
      # create CT volume node
      if ctImageSeriesUID:
        ctVolumeNode = self.scalarVolumePlugin.load(self.getCachedLoadables(imageSeriesAndFiles[ctImageSeriesUID])[0])
      
      # create Study node
      studyNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLLongitudinalPETCTStudyNode')
      studyNode.SetReferenceCount(studyNode.GetReferenceCount()-1)
      
      studyNode.SetName("Study_"+ self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['studyDate']))

      studyNode.SetAttribute('DICOM.StudyID',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['studyID']))
      studyNode.SetAttribute('DICOM.StudyInstanceUID',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['studyInstanceUID']))
      studyNode.SetAttribute('DICOM.StudyDate',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['studyDate']))
      studyNode.SetAttribute('DICOM.StudyTime',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['studyTime']))
      studyNode.SetAttribute('DICOM.RadioPharmaconStartTime',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['radioPharmaconStartTime']))
      studyNode.SetAttribute('DICOM.DecayFactor',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['decayCorrection']))
      studyNode.SetAttribute('DICOM.DecayCorrection',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['decayFactor']))
      studyNode.SetAttribute('DICOM.FrameReferenceTime',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['frameRefTime']))
      studyNode.SetAttribute('DICOM.RadionuclideHalfLife',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['radionuclideHalfLife']))
      studyNode.SetAttribute('DICOM.PETSeriesTime',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['seriesTime']))
      if ctImageSeriesUID: 
        studyNode.SetAttribute('DICOM.CTSeriesTime',self.__getSeriesInformation(imageSeriesAndFiles[ctImageSeriesUID], self.tags['seriesTime']))
      studyNode.SetAttribute('DICOM.PatientWeight',self.__getSeriesInformation(imageSeriesAndFiles[petImageSeriesUID], self.tags['patientWeight']))
      
      studyNode.SetAndObservePETVolumeNodeID(petVolumeNode.GetID())
      if ctVolumeNode:
        studyNode.SetAndObserveCTVolumeNodeID(ctVolumeNode.GetID())
      studyNode.SetAndObservePETLabelVolumeNodeID(petLabelVolumeNode.GetID())
          
      slicer.mrmlScene.AddNode(studyNode) 
      reportNode.AddStudyNodeID(studyNode.GetID())
                    
    return reportNode"""
      

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


