cmake_minimum_required(VERSION 2.8.7)

set(MODULE_NAME DICOMPETSUVPlugin)

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  find_package(Slicer REQUIRED)
  include(${Slicer_USE_FILE})
endif()

#-----------------------------------------------------------------------------
add_subdirectory(Py)
