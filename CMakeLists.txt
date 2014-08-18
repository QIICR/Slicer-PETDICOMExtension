cmake_minimum_required(VERSION 2.8.7)

#-----------------------------------------------------------------------------
set(MODULE_NAME SUVFactorCalculator)

find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

find_package(SlicerExecutionModel REQUIRED GenerateCLP)
include(${SlicerExecutionModel_USE_FILE})

find_package(DCMTK REQUIRED)

find_package(ITK REQUIRED)
include(${ITK_USE_FILE})

include(${CMAKE_CURRENT_SOURCE_DIR}/CMake/${MODULE_NAME}MacroExtractRepositoryInfo.cmake)

#-----------------------------------------------------------------------------
SlicerMacroExtractRepositoryInfo(VAR_PREFIX ${MODULE_NAME})
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/CMake/vtk${MODULE_NAME}VersionConfigure.h.in
    ${CMAKE_CURRENT_BINARY_DIR}/vtk${MODULE_NAME}VersionConfigure.h
    )

#-----------------------------------------------------------------------------
set(MODULE_INCLUDE_DIRECTORIES
  ${Slicer_Libs_INCLUDE_DIRS}
  ${ITK_INCLUDE_DIRS}
  ${vtkITK_INCLUDE_DIRS}
  ${DCMTK_INCLUDE_DIRS}
  )

set(MODULE_SRCS
  itkDCMTKFileReader.cxx
  dcmHelpersCommon.cxx
  SUVFactorCalculator.cxx  
  )

set(MODULE_TARGET_LIBRARIES
  ${ITK_LIBRARIES}
  ${VTK_LIBRARIES}
  ${DCMTK_LIBRARIES}
  vtkITK
  ITKIODCMTK
  )
  
#-----------------------------------------------------------------------------
SEMMacroBuildCLI(
  NAME ${MODULE_NAME}
  INCLUDE_DIRECTORIES ${MODULE_INCLUDE_DIRECTORIES}
  TARGET_LIBRARIES ${MODULE_TARGET_LIBRARIES}
  ADDITIONAL_SRCS ${MODULE_SRCS}
  EXECUTABLE_ONLY
  )

#-----------------------------------------------------------------------------
if(BUILD_TESTING)
  add_subdirectory(Testing)
endif()
