cmake_minimum_required(VERSION 2.8.9)

project(PETDICOMExtension)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/PETDICOM")
set(EXTENSION_CATEGORY "Converters")
set(EXTENSION_CONTRIBUTORS "Ethan Ulrich (University of Iowa), Andrey Fedorov (BWH, SPL)")
set(EXTENSION_DESCRIPTION "The PET DICOM Extension provides tools to import PET Standardized Uptake Value images from DICOM into Slicer.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/QIICR/Slicer-PETDICOMExtension/master/PETDICOMExtension.png")
set(EXTENSION_SCREENSHOTURLS "http://wiki.slicer.org/slicerWiki/images/thumb/2/2e/SUV_Factor_Calculator_GUI.png/418px-SUV_Factor_Calculator_GUI.png http://wiki.slicer.org/slicerWiki/images/thumb/2/29/DICOM_Browser_RWVM_Plugin.png/800px-DICOM_Browser_RWVM_Plugin.png http://wiki.slicer.org/slicerWiki/images/thumb/4/43/DICOM_Browser_PET_SUV_Plugin.png/800px-DICOM_Browser_PET_SUV_Plugin.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)

if(CMAKE_CONFIGURATION_TYPES)
  set(DEPENDENCIES_ADDITIONAL_MODULE_PATHS "")
  foreach(config ${CMAKE_CONFIGURATION_TYPES})
    list(APPEND DEPENDENCIES_ADDITIONAL_MODULE_PATHS "${CMAKE_BINARY_DIR}/${Slicer_CLIMODULES_LIB_DIR}/${config}")
    list(APPEND DEPENDENCIES_ADDITIONAL_MODULE_PATHS "${CMAKE_BINARY_DIR}/${Slicer_QTSCRIPTEDMODULES_LIB_DIR}/${config}")
  endforeach()
else()
  set(DEPENDENCIES_ADDITIONAL_MODULE_PATHS
    ${CMAKE_BINARY_DIR}/${Slicer_CLIMODULES_LIB_DIR}
    ${CMAKE_BINARY_DIR}/${Slicer_QTSCRIPTEDMODULES_LIB_DIR}
    )
endif()

# Additional C/CXX flags - Should be defined before including Slicer_USE_FILE
set(ADDITIONAL_C_FLAGS "" CACHE STRING "Additional ${EXTENSION_NAME} C Flags")
set(ADDITIONAL_CXX_FLAGS "" CACHE STRING "Additional ${EXTENSION_NAME} CXX Flags")

include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(SUVFactorCalculatorCLI)
add_subdirectory(DICOMRWVMPlugin)
add_subdirectory(DICOMPETSUVPlugin)
add_subdirectory(Testing)
## NEXT_MODULE

#-----------------------------------------------------------------------------

include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
