/**
 * @file ui_app.h
 * @brief LVGL GUI Guider Application Integration Header
 */

#ifndef UI_APP_H
#define UI_APP_H

#ifdef __cplusplus
extern "C" {
#endif

#include "lvgl.h"
#include "gui_guider.h"

// Global UI instance (accessible from anywhere)
extern lv_ui guider_ui;

/**
 * @brief Initialize LVGL and GUI Guider UI
 *
 * Call this after hardware initialization
 */
void ui_app_init(void);

/**
 * @brief Run LVGL task handler
 *
 * Call this every 5-10ms in main loop or FreeRTOS task
 */
void ui_app_task(void);

/**
 * @brief Screen navigation functions
 */
void ui_app_load_main_screen(void);
void ui_app_load_comm_uart_screen(void);
void ui_app_load_comm_can_screen(void);
void ui_app_load_led_screen(void);
void ui_app_load_storage_screen(void);

/**
 * @brief Get current active screen
 */
lv_obj_t* ui_app_get_active_screen(void);

/**
 * @brief Example function to update UI elements
 */
void ui_app_update_led_period(uint32_t period_ms);

#ifdef __cplusplus
}
#endif

#endif // UI_APP_H
