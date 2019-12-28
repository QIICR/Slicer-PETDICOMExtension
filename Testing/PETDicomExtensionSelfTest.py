import os
import unittest
import vtk, qt, ctk, slicer, logging
from DICOMLib import DICOMUtils
from slicer.ScriptedLoadableModule import *

if slicer.app.majorVersion >= 5 or (slicer.app.majorVersion == 4 and slicer.app.minorVersion >= 11):
  import pydicom
else:
  import dicom

#
# PETDicomExtensionSelfTest
#

class PETDicomExtensionSelfTest(ScriptedLoadableModule):
  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "PETDicomExtensionSelfTest"
    self.parent.categories = ["Testing.TestCases"]
    self.parent.dependencies = []
    self.parent.contributors = ["Christian Bauer (University of Iowa)"]
    self.parent.helpText = """This is a self test for PET DICOM plugins."""
    parent.acknowledgementText = """This work was partially funded by NIH grants U01-CA140206 and U24-CA180918."""

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['PETDicomExtensionSelfTest'] = self.runTest

  def runTest(self):
    tester = PETDicomExtensionSelfTestTest()
    tester.runTest()

#
# PETDicomExtensionSelfTestWidget
#

class PETDicomExtensionSelfTestWidget(ScriptedLoadableModuleWidget):
  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

#
# PETDicomExtensionSelfTestLogic
#

class PETDicomExtensionSelfTestLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass


class PETDicomExtensionSelfTestTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  """
    
  # ------------------------------------------------------------------------------
  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    self.UID = '1.3.6.1.4.1.14519.5.2.1.2744.7002.886851941687931416391879144903'
    self.PatientName = 'QIN-HEADNECK-01-0139'
    self.tempDicomDatabase = os.path.join(slicer.app.temporaryPath,'PETTest')
    slicer.mrmlScene.Clear(0)
    self.originalDicomDatabase = DICOMUtils.openTemporaryDatabase(self.tempDicomDatabase)
    
  # ------------------------------------------------------------------------------
  def doCleanups(self):
    """ cleanup temporary data in case an exception occurs
    """ 
    self.tearDown()   
  
  # ------------------------------------------------------------------------------
  def tearDown(self):
    """ Close temporary DICOM database and remove temporary data
    """ 
    import shutil
    if self.originalDicomDatabase:
      DICOMUtils.closeTemporaryDatabase(self.originalDicomDatabase, True)
      shutil.rmtree(self.tempDicomDatabase) # closeTemporaryDatabase cleanup doesn't work. We need to do it manually
      self.originalDicomDatabase = None      
    
  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_PETDicomExtensionSelfTest_Main()
    self.tearDown()

  # ------------------------------------------------------------------------------
  def test_PETDicomExtensionSelfTest_Main(self):
    """ test PET SUV Plugin and DICOM RWVM creation 
    """ 
    self.delayDisplay('Checking for PET DICOM plugins')
    dicomWidget = slicer.modules.dicom.widgetRepresentation().self()
    dicomPluginCheckbox =  dicomWidget.detailsPopup.pluginSelector.checkBoxByPlugin
    self.assertIn('DICOMPETSUVPlugin', dicomPluginCheckbox)
    self.assertIn('DICOMRWVMPlugin', dicomPluginCheckbox)    
    
    self.delayDisplay('Adding PET DICOM dataset to DICOM database (including download if necessary)')
    self._downloadTestData()
    
    self.delayDisplay('Loading data with DICOMPETSUVPlugin')
    self._loadWithPlugin(self.UID, 'DICOMPETSUVPlugin')
    imageNode = slicer.mrmlScene.GetFirstNodeByClass('vtkMRMLScalarVolumeNode')
    self.assertIsNotNone(imageNode)
    
    self.delayDisplay('Testing properties of loaded SUV normalized data')
    self._testDataProperties(imageNode)
    
    self.delayDisplay('Testing DICOM database for created RWVM file')
    patientUID = DICOMUtils.getDatabasePatientUIDByPatientName(self.PatientName)
    studies = slicer.dicomDatabase.studiesForPatient(patientUID)
    series = slicer.dicomDatabase.seriesForStudy(studies[0])
    RWVMSeries = None
    for serie in series:
      description = slicer.dicomDatabase.descriptionForSeries(serie)
      if description=='PET SUV Factors':
        RWVMSeries = serie
    self.assertIsNotNone(RWVMSeries)
    files = slicer.dicomDatabase.filesForSeries(RWVMSeries)
    self.assertTrue(len(files)>0)
    RWVMFile = files[0]
    print(RWVMFile)
    
    self.delayDisplay('Testing RealWorldValueSlope stored in RWVM file')
    if slicer.app.majorVersion >= 5 or (slicer.app.majorVersion == 4 and slicer.app.minorVersion >= 11):
      rwvm = pydicom.dcmread(RWVMFile)
    else:
      rwvm = dicom.read_file(RWVMFile)
    self.assertIn('ReferencedImageRealWorldValueMappingSequence',  rwvm)
    rirwvms = rwvm.ReferencedImageRealWorldValueMappingSequence[0]
    self.assertIn('RealWorldValueMappingSequence', rirwvms)
    rwvms = rirwvms.RealWorldValueMappingSequence[0]
    self.assertIn('RealWorldValueSlope', rwvms)
    slope = rwvms.RealWorldValueSlope
    self.assertTrue(abs(slope-0.000401664)<0.00001)
    
    self.delayDisplay('Loading data with DICOMRWVMPlugin')
    slicer.mrmlScene.Clear(0)
    self._loadWithPlugin(RWVMSeries, 'DICOMRWVMPlugin')
    imageNode = slicer.mrmlScene.GetFirstNodeByClass('vtkMRMLScalarVolumeNode')
    self.assertIsNotNone(imageNode)
    
    self.delayDisplay('Testing properties of loaded SUV normalized data')
    self._testDataProperties(imageNode)
        
    self.delayDisplay('Test passed!')
      
  # ------------------------------------------------------------------------------
  def _downloadTestData(self):
    """ download DICOM PET scan and add to DICOM database
    """ 
    from six.moves.urllib.parse import urlparse, urlencode
    from six.moves.urllib.request import urlopen, urlretrieve
    from six.moves.urllib.error import HTTPError
    quantity = slicer.vtkCodedEntry()
    quantity.SetFromString('CodeValue:126400|CodingSchemeDesignator:DCM|CodeMeaning:Standardized Uptake Value')
    units = slicer.vtkCodedEntry()
    units.SetFromString('CodeValue:{SUVbw}g/ml|CodingSchemeDesignator:UCUM|CodeMeaning:Standardized Uptake Value body weight')      
    url = 'http://slicer.kitware.com/midas3/download/item/257234/QIN-HEADNECK-01-0139-PET.zip'
    zipFile = 'QIN-HEADNECK-01-0139-PET.zip'
    suvNormalizationFactor = 0.00040166400000000007
    destinationDirectory = self.tempDicomDatabase
    filePath = os.path.join(destinationDirectory, zipFile)
    # download dataset if necessary
    if not len(slicer.dicomDatabase.filesForSeries(self.UID)):
      filePath = os.path.join(destinationDirectory, zipFile)
      if not os.path.exists(os.path.dirname(filePath)):
        os.makedirs(os.path.dirname(filePath))
      logging.debug('Saving download %s to %s ' % (url, filePath))
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        slicer.util.delayDisplay('Requesting download of %s...\n' % url, 1000)
        urlretrieve(url, filePath)
      if os.path.exists(filePath) and os.path.splitext(filePath)[1]=='.zip':
        success = slicer.app.applicationLogic().Unzip(filePath, destinationDirectory)
        if not success:
          logging.error("Archive %s was NOT unzipped successfully." %  filePath)
      indexer = ctk.ctkDICOMIndexer()
      indexer.addDirectory(slicer.dicomDatabase, destinationDirectory, None)
      indexer.waitForImportFinished()
    
  # ------------------------------------------------------------------------------
  def _loadWithPlugin(self, UID, pluginName):
    dicomWidget = slicer.modules.dicom.widgetRepresentation().self()
    dicomPluginCheckbox =  dicomWidget.detailsPopup.pluginSelector.checkBoxByPlugin
    dicomPluginStates = {(key,value.checked) for key,value in dicomPluginCheckbox.items()}
    for cb in list(dicomPluginCheckbox.values()):
      cb.checked=False
    dicomPluginCheckbox[pluginName].checked = True
    success=DICOMUtils.loadSeriesByUID([UID])    
    for key,value in dicomPluginStates:
      dicomPluginCheckbox[key].checked=value
  
  # ------------------------------------------------------------------------------
  def _testDataProperties(self, imageNode):
    units = imageNode.GetVoxelValueUnits()
    self.assertTrue(units.GetCodeMeaning()=='Standardized Uptake Value body weight')
    self.assertTrue(units.GetCodeValue()=='{SUVbw}g/ml')
    self.assertTrue(units.GetCodingSchemeDesignator()=='UCUM')
    quantity = imageNode.GetVoxelValueQuantity()
    self.assertTrue(quantity.GetCodeMeaning()=='Standardized Uptake Value')
    self.assertTrue(quantity.GetCodeValue()=='126400')
    self.assertTrue(quantity.GetCodingSchemeDesignator()=='DCM')
    scalarRange = imageNode.GetImageData().GetScalarRange()
    self.assertTrue(abs(scalarRange[0]-0)<0.01)
    self.assertTrue(abs(scalarRange[1]-89.85876418551707)<0.01)
    
    
    
