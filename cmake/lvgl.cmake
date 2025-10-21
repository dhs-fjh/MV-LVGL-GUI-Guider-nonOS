# LVGL Library Configuration

set(LVGL_DIR ${CMAKE_SOURCE_DIR}/lvgl-guider/lvgl)

# Collect all LVGL source files
file(GLOB_RECURSE LVGL_SOURCES
    ${LVGL_DIR}/src/*.c
)

# Remove files that require FreeRTOS or are not needed
list(FILTER LVGL_SOURCES EXCLUDE REGEX ".*lv_video\\.c$")
list(FILTER LVGL_SOURCES EXCLUDE REGEX ".*lv_zh_keyboard\\.c$")

# Create LVGL library
add_library(lvgl STATIC ${LVGL_SOURCES})

# LVGL include directories - USE Core/lvgl for lv_conf.h
target_include_directories(lvgl PUBLIC
    ${LVGL_DIR}
    ${LVGL_DIR}/src
    ${CMAKE_SOURCE_DIR}/Core/lvgl  # For lv_conf.h - user's ported config
)

# Compile definitions for LVGL
target_compile_definitions(lvgl PUBLIC
    LV_CONF_INCLUDE_SIMPLE
)

# Compile options
target_compile_options(lvgl PRIVATE
    -Wno-unused-parameter
    -Wno-missing-field-initializers
)
