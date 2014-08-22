cmake_minimum_required(VERSION 2.8.9)

project(PETDICOMExtension)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://www.example.com/Slicer/Extensions/PETDICOMExtension")
set(EXTENSION_CATEGORY "Converters")
set(EXTENSION_CONTRIBUTORS "Ethan Ulrich (University of Iowa), Andrey Fedorov (BWH, SPL)")
set(EXTENSION_DESCRIPTION "The PET DICOM Extension provides tools to import PET Standardized Uptake Value images from DICOM into Slicer.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/QIICR/Slicer-PETDICOMExtension/master/PETDICOMExtension.png")
#set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/PETDICOMExtension/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(SUVFactorCalculatorCLI)
add_subdirectory(DICOMRWVMPlugin)
add_subdirectory(DICOMPETSUVPlugin)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
