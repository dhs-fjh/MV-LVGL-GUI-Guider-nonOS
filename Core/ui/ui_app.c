/**
 * @file ui_app.c
 * @brief LVGL GUI Guider Application Integration
 *
 * This file demonstrates how to integrate GUI Guider generated UI
 * with your STM32 application using the hardware abstraction layer.
 */

#include "custom.h"
#include "events_init.h"
#include "gui_guider.h"
#include "lv_port_disp.h"
#include "lv_port_fs.h"
#include "lv_port_indev.h"
#include "lvgl.h"

// Global UI instance
lv_ui guider_ui;

/**
 * @brief Initialize LVGL and GUI Guider UI
 *
 * Call this function after hardware initialization is complete
 */
void ui_app_init(void) {
  // 1. Initialize LVGL library
  lv_init();

  // 2. Initialize display driver (connects to your LCD hardware)
  lv_port_disp_init();

  // 3. Initialize input device driver (connects to your touch hardware)
  lv_port_indev_init();
  lv_port_fs_init(); // 初始化FATFS文件系统接口

  // 4. Setup GUI Guider generated UI
  setup_ui(&guider_ui);

  // 5. Initialize custom code (if any)
  custom_init(&guider_ui);

  // 6. Initialize event handlers
  events_init(&guider_ui);

  // UI is now ready to use!
}

/**
 * @brief Run LVGL task handler
 *
 * Call this function periodically (every 5-10ms) in your main loop
 * or from a FreeRTOS task
 */
void ui_app_task(void) {
  // Handle LVGL tasks (rendering, input processing, animations, etc.)
  lv_timer_handler();
}

/**
 * @brief Example: Load a specific screen
 *
 * You can call these functions to navigate between screens
 */
void ui_app_load_main_screen(void) { lv_scr_load(guider_ui.ui_main); }

void ui_app_load_comm_uart_screen(void) { lv_scr_load(guider_ui.ui_comm_uart); }

void ui_app_load_comm_can_screen(void) { lv_scr_load(guider_ui.ui_comm_can); }

void ui_app_load_led_screen(void) { lv_scr_load(guider_ui.ui_led); }

void ui_app_load_storage_screen(void) { lv_scr_load(guider_ui.ui_storage); }

/**
 * @brief Example: Get current active screen
 *
 * @return Pointer to current screen object
 */
lv_obj_t *ui_app_get_active_screen(void) { return lv_scr_act(); }

/**
 * @brief Example: Access UI elements
 *
 * You can access any UI element through guider_ui structure:
 * - guider_ui.ui_main_btn_pwr
 * - guider_ui.ui_comm_uart_ta_tx_buf
 * - guider_ui.ui_led_slider_period
 * etc.
 */
void ui_app_update_led_period(uint32_t period_ms) {
  lv_slider_set_value(guider_ui.ui_led_slider_period, period_ms, LV_ANIM_ON);
}