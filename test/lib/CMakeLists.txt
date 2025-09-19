cmake_minimum_required(VERSION 3.25)
project(TestLibraries C )

#this is a simple test project to build a static library with arm-none-eabi-gcc toolchain
#it is used to verify that the created docker image works as expected

# Specify the include directory
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/inc)

# List all source files explicitly
set(SOURCES
   src/lib.c
    # Add more source files here as needed
)

# Create the static library
add_library(MyStaticLibrary STATIC ${SOURCES})

# Optionally, set the include directories for consumers
target_include_directories(MyStaticLibrary PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc)