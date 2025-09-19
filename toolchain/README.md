# Toolchain file

## Overview
This directory is copied to /home/<user>/toolchain directory in docker image.
This file declares the installed tools for cmake with arm-none-eabi-gcc.

To use on your project, add:
``` cmake ...... -DCMAKE_TOOLCHAIN_FILE=/home/<user>/toolchain/arm-none-eabi-gcc.cmake ```
Note: a relative path causes some unwanted behavior in cmake, its better to use an absolute here right now.



