cmake_minimum_required(VERSION 2.8.7)

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  set(EXTENSION_NAME DICOMRWVMPlugin)
#  set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/LongitudinalPETCT")
#  set(EXTENSION_CATEGORY "Informatics")
#  set(EXTENSION_CONTRIBUTORS "Paul Mercea (University of Heidelberg), Andrey Fedorov(Surgical Planning Lab)")
#  set(EXTENSION_DESCRIPTION "The purpose of the Longitudinal PET/CT Analysis module is to provide a user friendly Slicer interface for quantification of DICOM PET/CT image data by computing the standardized uptake value (SUV) based on bodyweight for different regions of interest and for different timepoints.")
#  set(EXTENSION_ICONURL "http://www.slicer.org/slicerWiki/images/0/08/LongitudinalPETCTLogo.png")
#  set(EXTENSION_SCREENSHOTURLS "http://www.slicer.org/slicerWiki/images/3/31/LongitudinalPETCT_Screenshot.jpg")
endif()

#-----------------------------------------------------------------------------
#set(MODULE_NAME LongitudinalPETCT)
#set(MODULE_TITLE ${MODULE_NAME})

#string(TOUPPER ${MODULE_NAME} MODULE_NAME_UPPER)

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  find_package(Slicer REQUIRED)
  include(${Slicer_USE_FILE})
endif()

#-----------------------------------------------------------------------------
#add_subdirectory(MRML)
#add_subdirectory(Widgets)
#add_subdirectory(Logic)
add_subdirectory(Py)
#add_subdirectory(Quantification)

#-----------------------------------------------------------------------------
#set(MODULE_EXPORT_DIRECTIVE "Q_SLICER_QTMODULES_${MODULE_NAME_UPPER}_EXPORT")

#set(MODULE_INCLUDE_DIRECTORIES
#  ${CMAKE_CURRENT_SOURCE_DIR}/MRML
#  ${CMAKE_CURRENT_BINARY_DIR}/MRML
#  ${CMAKE_CURRENT_SOURCE_DIR}/Logic
#  ${CMAKE_CURRENT_BINARY_DIR}/Logic
#  ${CMAKE_CURRENT_SOURCE_DIR}/Widgets
#  ${CMAKE_CURRENT_BINARY_DIR}/Widgets
  #${vtkSlicerVolumesModuleLogic_SOURCE_DIR}
  #${vtkSlicerVolumesModuleLogic_BINARY_DIR}
#  )

#set(MODULE_SRCS
#  qSlicerLongitudinalPETCTModule.cxx
#  qSlicerLongitudinalPETCTModule.h
#  qSlicerLongitudinalPETCTModuleWidget.cxx
#  qSlicerLongitudinalPETCTModuleWidget.h
#  )

#set(MODULE_MOC_SRCS
#  qSlicerLongitudinalPETCTModule.h
#  qSlicerLongitudinalPETCTModuleWidget.h
#  )  
  
#-----------------------------------------------------------------------------  
#  set(MODULE_TARGET_LIBRARIES
#  vtkSlicer${MODULE_NAME}ModuleLogic
#  qSlicer${MODULE_NAME}ModuleWidgets
  #vtkSlicerVolumesModuleLogic
#  )
  


#-----------------------------------------------------------------------------
#slicerMacroBuildQtModule(
#  NAME ${MODULE_NAME}
#  TITLE ${MODULE_TITLE}
#  EXPORT_DIRECTIVE ${MODULE_EXPORT_DIRECTIVE}
#  INCLUDE_DIRECTORIES ${MODULE_INCLUDE_DIRECTORIES}
#  SRCS ${MODULE_SRCS}
#  MOC_SRCS ${MODULE_MOC_SRCS}
#  UI_SRCS ${MODULE_UI_SRCS}
#  TARGET_LIBRARIES ${MODULE_TARGET_LIBRARIES}
#  RESOURCES ${MODULE_RESOURCES}
#  )

#-----------------------------------------------------------------------------
#if(BUILD_TESTING)
#  add_subdirectory(Testing)
#endif()

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  include(${Slicer_EXTENSION_CPACK})
endif()
