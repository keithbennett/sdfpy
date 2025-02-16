cmake_minimum_required(VERSION 3.21)
project(sdfr)

add_subdirectory(src/C C EXCLUDE_FROM_ALL)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Install the shared library
install(TARGETS sdfc_shared DESTINATION ${SKBUILD_PROJECT_NAME})
