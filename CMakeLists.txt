cmake_minimum_required(VERSION 3.22)

#
# This file is generated only once,
# and is not re-generated if converter is called multiple times.
#
# User is free to modify the file as much as necessary
#

# Setup compiler settings
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)


# Define the build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Debug")
endif()

# Set the project name
set(CMAKE_PROJECT_NAME LVGL)

# Enable compile command to ease indexing with e.g. clangd
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

# Core project settings
project(${CMAKE_PROJECT_NAME})
message("Build type: " ${CMAKE_BUILD_TYPE})

# Enable CMake support for ASM and C languages
enable_language(C ASM)

# Create an executable object type
add_executable(${CMAKE_PROJECT_NAME})

# Add STM32CubeMX generated sources
add_subdirectory(cmake/stm32cubemx)

# Add LVGL library
include(cmake/lvgl.cmake)

# Add GUI Guider generated code
include(cmake/gui_guider.cmake)

# Link directories setup
target_link_directories(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined library search paths
)

# Add sources to executable
target_sources(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user sources here
    # drivers
    src/drivers/comm/driver_log.c

    src/drivers/device/driver_led.c

    src/drivers/fs/driver_sd_fs.c

    src/drivers/display/lcd_ili9341.c

    src/drivers/touch/touch_xpt2046.c

    src/lite_lib/cJSON/cJSON.c

    # hal
    src/hal/hal_delay.c
    src/hal/hal_uart.c
    src/hal/hal_gpio.c

    src/hal/hal_spi_sw.c

    # LVGL porting layer
    Core/lvgl/porting/lv_port_disp.c
    Core/lvgl/porting/lv_port_indev.c
    Core/lvgl/porting/lv_port_fs.c

    # UI application layer
    Core/ui/ui_app.c
)

# Add include paths
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined include paths
    Core/config
    Core/ui

    src/drivers/comm
    src/drivers/device
    src/drivers/display
    src/drivers/touch
    src/drivers/fs

    src/lite_lib/cJSON

    src/hal

    # LVGL porting layer
    Core/lvgl/porting
)

# Add project symbols (macros)
target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined symbols
)

# Remove wrong libob.a library dependency when using cpp files
list(REMOVE_ITEM CMAKE_C_IMPLICIT_LINK_LIBRARIES ob)

# Add linked libraries
target_link_libraries(${CMAKE_PROJECT_NAME}
    stm32cubemx
    lvgl
    gui_guider

    # Add user defined libraries
)
