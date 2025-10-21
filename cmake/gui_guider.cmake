# GUI Guider Generated Code Configuration

set(GUI_GUIDER_DIR ${CMAKE_SOURCE_DIR}/lvgl-guider/generated)
set(GUI_GUIDER_CUSTOM_DIR ${CMAKE_SOURCE_DIR}/lvgl-guider/custom)

# Collect all GUI Guider generated source files
file(GLOB GUI_GUIDER_SOURCES
    ${GUI_GUIDER_DIR}/*.c
    ${GUI_GUIDER_DIR}/guider_fonts/*.c
    ${GUI_GUIDER_DIR}/guider_customer_fonts/*.c
    ${GUI_GUIDER_CUSTOM_DIR}/*.c
)

# Create GUI Guider library
add_library(gui_guider STATIC ${GUI_GUIDER_SOURCES})

# Define compile definitions for non-simulator build
target_compile_definitions(gui_guider PRIVATE
    
    STM32F407xx
    USE_HAL_DRIVER
)

# GUI Guider include directories
target_include_directories(gui_guider PUBLIC
    ${GUI_GUIDER_DIR}
    ${GUI_GUIDER_DIR}/guider_fonts
    ${GUI_GUIDER_DIR}/guider_customer_fonts
    ${GUI_GUIDER_DIR}/images
    ${GUI_GUIDER_CUSTOM_DIR}
    # Add driver include paths for events_init.c
    ${CMAKE_SOURCE_DIR}/src/drivers/device
    ${CMAKE_SOURCE_DIR}/src/drivers/comm
    ${CMAKE_SOURCE_DIR}/src/hal
    ${CMAKE_SOURCE_DIR}/Core/Inc
    ${CMAKE_SOURCE_DIR}/Core/config
    # Add STM32 HAL driver paths
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Inc
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Inc/Legacy
    ${CMAKE_SOURCE_DIR}/Drivers/CMSIS/Device/ST/STM32F4xx/Include
    ${CMAKE_SOURCE_DIR}/Drivers/CMSIS/Include
)

# Link LVGL library
target_link_libraries(gui_guider PUBLIC lvgl)
