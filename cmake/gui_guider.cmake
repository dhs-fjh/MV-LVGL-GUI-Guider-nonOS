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

# GUI Guider include directories
target_include_directories(gui_guider PUBLIC
    ${GUI_GUIDER_DIR}
    ${GUI_GUIDER_DIR}/guider_fonts
    ${GUI_GUIDER_DIR}/guider_customer_fonts
    ${GUI_GUIDER_DIR}/images
    ${GUI_GUIDER_CUSTOM_DIR}
)

# Link LVGL library
target_link_libraries(gui_guider PUBLIC lvgl)
