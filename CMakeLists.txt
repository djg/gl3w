project(gl3w C)

cmake_minimum_required(VERSION 2.8)

add_custom_command(
  OUTPUT include/GLES3/gles3w.h
  COMMAND python ${CMAKE_CURRENT_SOURCE_DIR}/gles3w_gen.py
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/gles3w_gen.py)

add_custom_target(
  gl3w ALL echo
  DEPENDS include/GLES3/gles3w.h)
