/*
* Copyright 2025 NXP
* NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
* accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
* activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
* comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
* terms, then you may not retain, install, activate or otherwise use the software.
*/

#include "events_init.h"
#include <stdio.h>
#include "lvgl.h"

#if LV_USE_GUIDER_SIMULATOR && LV_USE_FREEMASTER
#include "freemaster_client.h"
#endif

/****************** ui main↓ ******************/
#include "custom.h"
#if GUI_SIMULATOR != 1
#include "driver_log.h"
#include "hal_delay.h"

#include <string.h>
#include <stdio.h>
static const hal_delay_interface_t *hal_delay = NULL;
#endif
/****************** ui main↑ ******************/
/****************** ui main uart↓ ******************/
#if GUI_SIMULATOR != 1
#include "driver_cmd.h"

// 静态变量：定时器
static uart_arg_t uart_arg;
static const driver_cmd_interface_t *cmd = NULL;
static lv_timer_t *uart_scan_timer = NULL;
static uint8_t current_uart_ch = 0;      // 当前选择的串口通道

// 定时器回调：扫描串口接收缓冲区
static void uart_scan_timer_cb(lv_timer_t *timer) {
    lv_ui *ui = (lv_ui *)timer->user_data;

    // 获取 CMD 接口（使用 LOG 串口）
    const driver_cmd_interface_t *cmd = driver_cmd_get_interface();
    if (!cmd || !cmd->msg)
        return;

    // 检查是否启用时间戳
    bool time_stamp_enabled =
        lv_obj_has_state(ui->ui_comm_uart_cb_time_stamp, LV_STATE_CHECKED);

    // 扫描所有缓冲区，查找新数据
    for (uint8_t i = 0; i < CMD_RX_BUFFER_COUNT; i++) {
      uart_msg_t *msg = &(cmd->msg[i]);

      // 检查是否有新数据（rx_flag 置位）
      if (msg->rx_flag && msg->length > 0) {
        // 确保数据有结束符
        if (msg->data[msg->length] != '\0') {
          msg->data[msg->length] = '\0';
        }

        // 准备要显示的数据（可能带时间戳）
        char display_data[CMD_RX_BUFFER_SIZE + 32];
        if (time_stamp_enabled) {
          snprintf(display_data, sizeof(display_data), "[%lu] %s",
                   msg->time_stamp, (char *)msg->data);
        } else {
          snprintf(display_data, sizeof(display_data), "%s", (char *)msg->data);
        }

        // 获取当前文本区内容
        const char *current_text =
            lv_textarea_get_text(ui->ui_comm_uart_ta_rx_buf);
        size_t current_len = strlen(current_text);
        size_t new_data_len = strlen(display_data);

        // 计算总长度（限制在 512 字节内）
        size_t total_len = current_len + new_data_len + 2; // +2 for "\r\n"

        if (total_len > 512) {
          // 删除缓冲区前 256 字节，保留后面内容，然后追加新数据
          size_t keep_start = (current_len > 256) ? (current_len - 256) : 0;
          size_t keep_len = current_len - keep_start;

          // 1. 构造新内容：保留的后面部分 + 换行 + 新数据
          char temp_buf[512];
          memcpy(temp_buf, current_text + keep_start, keep_len);
          temp_buf[keep_len] = '\r';
          temp_buf[keep_len + 1] = '\n';
          memcpy(temp_buf + keep_len + 2, display_data, new_data_len);
          temp_buf[keep_len + 2 + new_data_len] = '\0';

          // 2. 一次性设置新内容（自动清空旧数据）
          lv_textarea_set_text(ui->ui_comm_uart_ta_rx_buf, temp_buf);
        } else {
          // 追加新数据
          lv_textarea_add_text(ui->ui_comm_uart_ta_rx_buf, display_data);
          lv_textarea_add_text(ui->ui_comm_uart_ta_rx_buf, "\r\n");
        }

        // 清除 rx_flag，标记已处理
        msg->rx_flag = 0;
      }
    }
}
#endif
/****************** ui main uart↑ ******************/
#include <stdlib.h>
#include <time.h>

static uint16_t ui_comm_rc_data[16];
static lv_timer_t *rc_update_timer = NULL;

// 获取 Bar 对象的辅助函数
static lv_obj_t* get_rc_bar(lv_ui *ui, int index)
{
    lv_obj_t *bars[] = {
        ui->ui_comm_rc_bar_1, ui->ui_comm_rc_bar_2, ui->ui_comm_rc_bar_3, ui->ui_comm_rc_bar_4,
        ui->ui_comm_rc_bar_5, ui->ui_comm_rc_bar_6, ui->ui_comm_rc_bar_7, ui->ui_comm_rc_bar_8,
        ui->ui_comm_rc_bar_9, ui->ui_comm_rc_bar_10, ui->ui_comm_rc_bar_11, ui->ui_comm_rc_bar_12,
        ui->ui_comm_rc_bar_13, ui->ui_comm_rc_bar_14, ui->ui_comm_rc_bar_15, ui->ui_comm_rc_bar_16
    };
    return (index >= 0 && index < 16) ? bars[index] : NULL;
}

// 定时器回调
static void rc_timer_callback(lv_timer_t *timer)
{
    lv_ui *ui = (lv_ui *)timer->user_data;

    for(int i = 0; i < 16; i++) {
        ui_comm_rc_data[i] = 200 + (rand() % 1601);  // [0-1800]
        lv_bar_set_value(get_rc_bar(ui, i), ui_comm_rc_data[i], LV_ANIM_ON);
    }
}
/****************** ui led↓ ******************/
static unsigned int ui_led_slider_period_val = 0;
static bool ui_led_cb_blink_checked = 0;
static bool ui_led_cb_sta_checked = 0;
#if GUI_SIMULATOR != 1
#include "driver_led.h"
static const driver_led_interface_t *led = NULL;
#endif
/****************** ui led↑ ******************/


static void ui_main_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_SCREEN_LOAD_START:
    {

        break;
    }
    default:
        break;
    }
}

static void ui_main_btn_pwr_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        break;
    }
    default:
        break;
    }
}

static void ui_main_btn_io_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_io, guider_ui.ui_io_del, &guider_ui.ui_main_del, setup_scr_ui_io, LV_SCR_LOAD_ANIM_MOVE_LEFT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

static void ui_main_btn_comm_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_comm, guider_ui.ui_comm_del, &guider_ui.ui_main_del, setup_scr_ui_comm, LV_SCR_LOAD_ANIM_MOVE_LEFT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

static void ui_main_btn_led_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_led, guider_ui.ui_led_del, &guider_ui.ui_main_del, setup_scr_ui_led, LV_SCR_LOAD_ANIM_MOVE_LEFT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

static void ui_main_btn_storage_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_storage, guider_ui.ui_storage_del, &guider_ui.ui_main_del, setup_scr_ui_storage, LV_SCR_LOAD_ANIM_MOVE_LEFT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

static void ui_main_btn_settings_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_settings, guider_ui.ui_settings_del, &guider_ui.ui_main_del, setup_scr_ui_settings, LV_SCR_LOAD_ANIM_MOVE_LEFT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_ui_main (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->ui_main, ui_main_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_main_btn_pwr, ui_main_btn_pwr_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_main_btn_io, ui_main_btn_io_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_main_btn_comm, ui_main_btn_comm_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_main_btn_led, ui_main_btn_led_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_main_btn_storage, ui_main_btn_storage_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_main_btn_settings, ui_main_btn_settings_event_handler, LV_EVENT_ALL, ui);
}

static void ui_settings_btn_home_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_main, guider_ui.ui_main_del, &guider_ui.ui_settings_del, setup_scr_ui_main, LV_SCR_LOAD_ANIM_MOVE_RIGHT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_ui_settings (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->ui_settings_btn_home, ui_settings_btn_home_event_handler, LV_EVENT_ALL, ui);
}

static void ui_storage_btn_next_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        break;
    }
    default:
        break;
    }
}

static void ui_storage_btn_prev_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        break;
    }
    default:
        break;
    }
}

static void ui_storage_btn_home_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_main, guider_ui.ui_main_del, &guider_ui.ui_storage_del, setup_scr_ui_main, LV_SCR_LOAD_ANIM_MOVE_RIGHT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_ui_storage (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->ui_storage_btn_next, ui_storage_btn_next_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_storage_btn_prev, ui_storage_btn_prev_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_storage_btn_home, ui_storage_btn_home_event_handler, LV_EVENT_ALL, ui);
}

static void ui_comm_list_comm_item0_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_comm_can, guider_ui.ui_comm_can_del, &guider_ui.ui_comm_del, setup_scr_ui_comm_can, LV_SCR_LOAD_ANIM_MOVE_BOTTOM, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

static void ui_comm_list_comm_item1_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_comm_uart, guider_ui.ui_comm_uart_del, &guider_ui.ui_comm_del, setup_scr_ui_comm_uart, LV_SCR_LOAD_ANIM_MOVE_BOTTOM, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

static void ui_comm_list_comm_item2_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_comm_rc, guider_ui.ui_comm_rc_del, &guider_ui.ui_comm_del, setup_scr_ui_comm_rc, LV_SCR_LOAD_ANIM_MOVE_BOTTOM, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

static void ui_comm_btn_home_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_main, guider_ui.ui_main_del, &guider_ui.ui_comm_del, setup_scr_ui_main, LV_SCR_LOAD_ANIM_MOVE_RIGHT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_ui_comm (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->ui_comm_list_comm_item0, ui_comm_list_comm_item0_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_list_comm_item1, ui_comm_list_comm_item1_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_list_comm_item2, ui_comm_list_comm_item2_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_btn_home, ui_comm_btn_home_event_handler, LV_EVENT_ALL, ui);
}

static void ui_comm_can_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_SCREEN_LOAD_START:
    {
        // 申请rx_msg_buf内存
        break;
    }
    case LV_EVENT_SCREEN_UNLOADED:
    {
        // 释放rx_msg_buf内存
        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_ddlist_ch_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_VALUE_CHANGED:
    {
        uint16_t id = lv_dropdown_get_selected(guider_ui.ui_comm_can_ddlist_ch);
        // 发送通道
        LV_UNUSED(id);
        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_ddlist_rate_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_VALUE_CHANGED:
    {
        uint16_t id = lv_dropdown_get_selected(guider_ui.ui_comm_can_ddlist_rate);
        // 发送波特率修改
        LV_UNUSED(id);
        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_ddlist_rtr_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_VALUE_CHANGED:
    {
        uint16_t id = lv_dropdown_get_selected(guider_ui.ui_comm_can_ddlist_rtr);
        // 数据/遥控帧
        LV_UNUSED(id);
        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_ddlist_ide_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_VALUE_CHANGED:
    {
        uint16_t id = lv_dropdown_get_selected(guider_ui.ui_comm_can_ddlist_ide);
        // ID模式
        LV_UNUSED(id);
        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_ta_can_id_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_VALUE_CHANGED:
    {
        // 文本转ID
        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_ta_tx_buf_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_btn_tx_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {

        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_btn_tx_clean_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        lv_textarea_set_text(guider_ui.ui_comm_can_ta_tx_buf, "");
        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_btn_rx_clean_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        lv_textarea_set_text(guider_ui.ui_comm_can_ta_rx_msg, "");
        // buf索引归零
        break;
    }
    default:
        break;
    }
}

static void ui_comm_can_btn_back_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_comm, guider_ui.ui_comm_del, &guider_ui.ui_comm_can_del, setup_scr_ui_comm, LV_SCR_LOAD_ANIM_MOVE_TOP, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_ui_comm_can (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->ui_comm_can, ui_comm_can_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_ddlist_ch, ui_comm_can_ddlist_ch_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_ddlist_rate, ui_comm_can_ddlist_rate_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_ddlist_rtr, ui_comm_can_ddlist_rtr_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_ddlist_ide, ui_comm_can_ddlist_ide_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_ta_can_id, ui_comm_can_ta_can_id_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_ta_tx_buf, ui_comm_can_ta_tx_buf_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_btn_tx, ui_comm_can_btn_tx_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_btn_tx_clean, ui_comm_can_btn_tx_clean_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_btn_rx_clean, ui_comm_can_btn_rx_clean_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_can_btn_back, ui_comm_can_btn_back_event_handler, LV_EVENT_ALL, ui);
}

static void ui_comm_uart_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_SCREEN_LOAD_START:
    {
#if GUI_SIMULATOR != 1
      if (!cmd)
        cmd = driver_cmd_get_interface();
#endif
        break;
    }
    case LV_EVENT_SCREEN_UNLOADED:
    {
#if GUI_SIMULATOR != 1
        // 删除定时器
        if (uart_scan_timer) {
            lv_timer_del(uart_scan_timer);
            uart_scan_timer = NULL;
        }
#endif

        break;
    }
    default:
        break;
    }
}

static void ui_comm_uart_sw_uart_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_VALUE_CHANGED:
    {
        lv_obj_t * status_obj = lv_event_get_target(e);
        int status = lv_obj_has_state(status_obj, LV_STATE_CHECKED) ? true : false;
#if GUI_SIMULATOR != 1
        if (status) {
            // === 打开串口监听 ===
            // 1. 获取当前选择的串口通道（从下拉列表）
            current_uart_ch =
                lv_dropdown_get_selected(guider_ui.ui_comm_uart_ddlist_ch);

            // 2. 清空
            lv_textarea_set_text(guider_ui.ui_comm_uart_ta_rx_buf, "");

            // 3. 创建定时器（每 5ms 扫描一次）
            if (!uart_scan_timer) {
                uart_scan_timer =
                    lv_timer_create(uart_scan_timer_cb, 5, &guider_ui);
            }

            LV_LOG_USER("UART monitor started on channel %d", current_uart_ch);

        } else {
            // === 关闭串口监听 ===

            // 1. 删除定时器
            if (uart_scan_timer) {
                lv_timer_del(uart_scan_timer);
                uart_scan_timer = NULL;
            }
            LV_LOG_USER("UART monitor stopped");
        }
#else
        // 仿真器模式：仅显示状态
        if (status) {
            lv_textarea_set_text(guider_ui.ui_comm_uart_ta_rx_buf,
                                 "Simulator Mode\r\nNo real UART data");
        }
#endif
        break;
    }
    default:
        break;
    }
}

static void ui_comm_uart_btn_tx_clean_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        lv_textarea_set_text(guider_ui.ui_comm_uart_ta_tx_buf, "");
        break;
    }
    default:
        break;
    }
}

static void ui_comm_uart_btn_rx_clean_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        lv_textarea_set_text(guider_ui.ui_comm_uart_ta_rx_buf, "");
        break;
    }
    default:
        break;
    }
}

static void ui_comm_uart_btn_back_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_comm, guider_ui.ui_comm_del, &guider_ui.ui_comm_uart_del, setup_scr_ui_comm, LV_SCR_LOAD_ANIM_MOVE_TOP, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_ui_comm_uart (lv_ui *ui)
{
  lv_obj_add_event_cb(ui->ui_comm_uart, ui_comm_uart_event_handler,
                      LV_EVENT_ALL, ui);
  lv_obj_add_event_cb(ui->ui_comm_uart_sw_uart,
                      ui_comm_uart_sw_uart_event_handler, LV_EVENT_ALL, ui);
  lv_obj_add_event_cb(ui->ui_comm_uart_btn_tx_clean,
                      ui_comm_uart_btn_tx_clean_event_handler, LV_EVENT_ALL,
                      ui);
  lv_obj_add_event_cb(ui->ui_comm_uart_btn_rx_clean,
                      ui_comm_uart_btn_rx_clean_event_handler, LV_EVENT_ALL,
                      ui);
  lv_obj_add_event_cb(ui->ui_comm_uart_btn_back,
                      ui_comm_uart_btn_back_event_handler, LV_EVENT_ALL, ui);
}

static void ui_comm_rc_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_SCREEN_LOAD_START:
    {
        srand(lv_tick_get());

        // 加载旧值
        for(int i = 0; i < 16; i++) {
            lv_bar_set_value(get_rc_bar(&guider_ui, i), ui_comm_rc_data[i], LV_ANIM_OFF);
        }

        // 创建定时器
        if(rc_update_timer == NULL) {
            rc_update_timer = lv_timer_create(rc_timer_callback, 3000, &guider_ui);
        }
        break;
    }
    case LV_EVENT_SCREEN_UNLOADED:
    {
        // 删除定时器
        if(rc_update_timer != NULL) {
            lv_timer_del(rc_update_timer);
            rc_update_timer = NULL;
        }
        break;
    }
    default:
        break;
    }
}

static void ui_comm_rc_btn_back_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_RELEASED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_comm, guider_ui.ui_comm_del, &guider_ui.ui_comm_rc_del, setup_scr_ui_comm, LV_SCR_LOAD_ANIM_MOVE_TOP, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_ui_comm_rc (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->ui_comm_rc, ui_comm_rc_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_comm_rc_btn_back, ui_comm_rc_btn_back_event_handler, LV_EVENT_ALL, ui);
}

static void ui_io_btn_home_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_main, guider_ui.ui_main_del, &guider_ui.ui_io_del, setup_scr_ui_main, LV_SCR_LOAD_ANIM_MOVE_RIGHT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_ui_io (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->ui_io_btn_home, ui_io_btn_home_event_handler, LV_EVENT_ALL, ui);
}

static void ui_led_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_SCREEN_LOAD_START:
    {
#if GUI_SIMULATOR != 1
        led = driver_led_get_interface();
        if(led->auto_blink_enabled)
            ui_led_cb_blink_checked = 1;
        ui_led_slider_period_val = led->blink_period_ms;
#endif

        // 加载LED闪烁使能值
        if(ui_led_cb_blink_checked)
            lv_obj_add_state(guider_ui.ui_led_cb_blink, LV_STATE_CHECKED);

        // 加载LED当前状态
        // ui_led_cb_sta_checked = ; // 读取LED状态
        if(ui_led_cb_sta_checked)
            lv_obj_add_state(guider_ui.ui_led_cb_sta, LV_STATE_CHECKED);

        // 加载LED闪烁间隔值
        lv_slider_set_value(guider_ui.ui_led_slider_period, ui_led_slider_period_val, LV_ANIM_OFF);
        char buf[5];
        lv_snprintf(buf, sizeof(buf), "%4d", ui_led_slider_period_val);  // 格式化为4位数
        lv_label_set_text(guider_ui.ui_led_label_period, buf);


        break;
    }
    default:
        break;
    }
}

static void ui_led_slider_period_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_VALUE_CHANGED:
    {
        lv_obj_t *slider = lv_event_get_target(e);
        ui_led_slider_period_val = lv_slider_get_value(slider);
        char buf[5];
        lv_snprintf(buf, sizeof(buf), "%4d", ui_led_slider_period_val);  // 格式化为4位数
        lv_label_set_text(guider_ui.ui_led_label_period, buf);
        LV_LOG_USER("LED blink period: %d", ui_led_slider_period_val);
#if GUI_SIMULATOR != 1
        led->set_blink_period(ui_led_slider_period_val);
        log_debug("LED blink period: %d", ui_led_slider_period_val);
#endif
        break;
    }
    default:
        break;
    }
}

static void ui_led_cb_sta_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        lv_obj_t * status_obj = lv_event_get_target(e);
        int status = lv_obj_get_state(status_obj) & LV_STATE_CHECKED ? true : false;
        if(status) {
            ui_led_cb_sta_checked = 1;
        } else {
            ui_led_cb_sta_checked = 0;
        }
#if GUI_SIMULATOR != 1
        if(status)
            led->on();
        else
            led->off();
        log_debug("LED status: %d", status);
#endif
        LV_LOG_USER("LED status: %d", ui_led_cb_sta_checked);
        break;
    }
    default:
        break;
    }
}

static void ui_led_cb_blink_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        lv_obj_t * status_obj = lv_event_get_target(e);
        int status = lv_obj_get_state(status_obj) & LV_STATE_CHECKED ? true : false;
        if(status) {
            ui_led_cb_blink_checked = 1;
        } else {
            ui_led_cb_blink_checked = 0;
        }
#if GUI_SIMULATOR != 1
        led->enable_auto_blink(status);
        log_debug("LED auto blink: %d", status);
#endif
        LV_LOG_USER("LED auto blink: %d", ui_led_cb_blink_checked);
        break;
    }
    default:
        break;
    }
}

static void ui_led_btn_home_event_handler (lv_event_t *e)
{
    lv_event_code_t code = lv_event_get_code(e);
    switch (code) {
    case LV_EVENT_CLICKED:
    {
        ui_load_scr_animation(&guider_ui, &guider_ui.ui_main, guider_ui.ui_main_del, &guider_ui.ui_led_del, setup_scr_ui_main, LV_SCR_LOAD_ANIM_MOVE_RIGHT, 200, 0, false, true);
        break;
    }
    default:
        break;
    }
}

void events_init_ui_led (lv_ui *ui)
{
    lv_obj_add_event_cb(ui->ui_led, ui_led_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_led_slider_period, ui_led_slider_period_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_led_cb_sta, ui_led_cb_sta_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_led_cb_blink, ui_led_cb_blink_event_handler, LV_EVENT_ALL, ui);
    lv_obj_add_event_cb(ui->ui_led_btn_home, ui_led_btn_home_event_handler, LV_EVENT_ALL, ui);
}


void events_init(lv_ui *ui)
{

}
