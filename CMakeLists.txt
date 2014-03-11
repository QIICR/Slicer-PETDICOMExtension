cmake_minimum_required(VERSION 2.8.7)

#-----------------------------------------------------------------------------
set(MODULE_NAME SUVFactorCalculator)

#find_package(GenerateCLP REQUIRED)
#include(${GenerateCLP_USE_FILE})

find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

set(SUVFACTORCALCULATOR_SOURCE SUVFactorCalculator.cxx)
#GENERATECLP(SUVFACTORCALCULATOR_SOURCE SUVFactorCalculator.xml)

#-----------------------------------------------------------------------------
set(MODULE_INCLUDE_DIRECTORIES
  ${Slicer_Libs_INCLUDE_DIRS}
  ${vtkITK_INCLUDE_DIRS}
  )

set(MODULE_SRCS
  itkDCMTKFileReader.cxx
  itkDCMTKFileReader.h
  )

set(MODULE_TARGET_LIBRARIES
  ${ITK_LIBRARIES}
  ${VTK_LIBRARIES}
  ${DCMTK_LIBRARIES}
  vtkITK
  )
  
#-----------------------------------------------------------------------------
SEMMacroBuildCLI(
  NAME ${MODULE_NAME}
  TARGET_LIBRARIES ${MODULE_TARGET_LIBRARIES}
  INCLUDE_DIRECTORIES ${MODULE_INCLUDE_DIRECTORIES}
  ADDITIONAL_SRCS ${MODULE_SRCS}
  EXECUTABLE_ONLY
  )

#-----------------------------------------------------------------------------
if(BUILD_TESTING)
  add_subdirectory(Testing)
endif()
