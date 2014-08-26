
#-----------------------------------------------------------------------------
set(MODULE_NAME SUVFactorCalculator)

#-----------------------------------------------------------------------------

#
# SlicerExecutionModel
#
find_package(SlicerExecutionModel REQUIRED GenerateCLP)
include(${SlicerExecutionModel_USE_FILE})

find_package(DCMTK REQUIRED)

find_package(ITK REQUIRED)
include(${ITK_USE_FILE})

find_package(VTK REQUIRED)

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
  ${VTK_INCLUDE_DIRS}
  ${vtkITK_INCLUDE_DIRS}
  ${DCMTK_INCLUDE_DIRS}
  )

set(MODULE_SRCS
  itkDCMTKFileReader.h
  dcmHelpersCommon.h
  dcmUnitsConversionHelper.h
  SUVFactorCalculator.xml
  itkDCMTKFileReader.cxx
  dcmHelpersCommon.cxx
  dcmUnitsConversionHelper.cxx
  SUVFactorCalculator.cxx  
  )

set(MODULE_TARGET_LIBRARIES
  ${ITK_LIBRARIES}
  ${VTK_LIBRARIES}
  ${DCMTK_LIBRARIES}
  vtkIOCore
  vtkITK
  ITKIODCMTK
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
