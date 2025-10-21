/*
* Copyright 2025 NXP
* NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
* accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
* activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
* comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
* terms, then you may not retain, install, activate or otherwise use the software.
*/

#ifndef GUI_GUIDER_H
#define GUI_GUIDER_H
#ifdef __cplusplus
extern "C" {
#endif

#include "lvgl.h"

typedef struct
{
  
	lv_obj_t *ui_main;
	bool ui_main_del;
	lv_obj_t *ui_main_btn_pwr;
	lv_obj_t *ui_main_btn_pwr_label;
	lv_obj_t *ui_main_btn_io;
	lv_obj_t *ui_main_btn_io_label;
	lv_obj_t *ui_main_btn_comm;
	lv_obj_t *ui_main_btn_comm_label;
	lv_obj_t *ui_main_btn_led;
	lv_obj_t *ui_main_btn_led_label;
	lv_obj_t *ui_main_btn_storage;
	lv_obj_t *ui_main_btn_storage_label;
	lv_obj_t *ui_main_btn_settings;
	lv_obj_t *ui_main_btn_settings_label;
	lv_obj_t *ui_settings;
	bool ui_settings_del;
	lv_obj_t *ui_settings_label_title;
	lv_obj_t *ui_settings_btn_home;
	lv_obj_t *ui_settings_btn_home_label;
	lv_obj_t *ui_storage;
	bool ui_storage_del;
	lv_obj_t *ui_storage_list_files;
	lv_obj_t *ui_storage_list_files_item0;
	lv_obj_t *ui_storage_list_files_item1;
	lv_obj_t *ui_storage_list_files_item2;
	lv_obj_t *ui_storage_list_files_item3;
	lv_obj_t *ui_storage_list_files_item4;
	lv_obj_t *ui_storage_list_files_item5;
	lv_obj_t *ui_storage_list_files_item6;
	lv_obj_t *ui_storage_list_files_item7;
	lv_obj_t *ui_storage_list_files_item8;
	lv_obj_t *ui_storage_list_files_item9;
	lv_obj_t *ui_storage_btn_next;
	lv_obj_t *ui_storage_btn_next_label;
	lv_obj_t *ui_storage_btn_prev;
	lv_obj_t *ui_storage_btn_prev_label;
	lv_obj_t *ui_storage_label_title;
	lv_obj_t *ui_storage_label_page;
	lv_obj_t *ui_storage_btn_home;
	lv_obj_t *ui_storage_btn_home_label;
	lv_obj_t *ui_comm;
	bool ui_comm_del;
	lv_obj_t *ui_comm_list_comm;
	lv_obj_t *ui_comm_list_comm_item0;
	lv_obj_t *ui_comm_list_comm_item1;
	lv_obj_t *ui_comm_list_comm_item2;
	lv_obj_t *ui_comm_label_title;
	lv_obj_t *ui_comm_btn_home;
	lv_obj_t *ui_comm_btn_home_label;
	lv_obj_t *ui_comm_can;
	bool ui_comm_can_del;
	lv_obj_t *ui_comm_can_ta_rx_msg;
	lv_obj_t *ui_comm_can_ddlist_ch;
	lv_obj_t *ui_comm_can_ddlist_rate;
	lv_obj_t *ui_comm_can_ddlist_rtr;
	lv_obj_t *ui_comm_can_ddlist_ide;
	lv_obj_t *ui_comm_can_ta_can_id;
	lv_obj_t *ui_comm_can_label_can_id;
	lv_obj_t *ui_comm_can_ta_tx_buf;
	lv_obj_t *ui_comm_can_btn_tx;
	lv_obj_t *ui_comm_can_btn_tx_label;
	lv_obj_t *ui_comm_can_btn_tx_clean;
	lv_obj_t *ui_comm_can_btn_tx_clean_label;
	lv_obj_t *ui_comm_can_label_tittle;
	lv_obj_t *ui_comm_can_btn_rx_clean;
	lv_obj_t *ui_comm_can_btn_rx_clean_label;
	lv_obj_t *ui_comm_can_btn_back;
	lv_obj_t *ui_comm_can_btn_back_label;
	lv_obj_t *ui_comm_uart;
	bool ui_comm_uart_del;
	lv_obj_t *ui_comm_uart_ta_rx_msg;
	lv_obj_t *ui_comm_uart_ddlist_rx_fmt;
	lv_obj_t *ui_comm_uart_ddlist_check;
	lv_obj_t *ui_comm_uart_ddlist_data_bit;
	lv_obj_t *ui_comm_uart_ddlist_stop;
	lv_obj_t *ui_comm_uart_cb_time_stamp;
	lv_obj_t *ui_comm_uart_ddlist_tx_fmt;
	lv_obj_t *ui_comm_uart_ddlist_ch;
	lv_obj_t *ui_comm_uart_ta_rate;
	lv_obj_t *ui_comm_uart_sw_uart;
	lv_obj_t *ui_comm_uart_ta_tx_buf;
	lv_obj_t *ui_comm_uart_btn_tx;
	lv_obj_t *ui_comm_uart_btn_tx_label;
	lv_obj_t *ui_comm_uart_btn_tx_clean;
	lv_obj_t *ui_comm_uart_btn_tx_clean_label;
	lv_obj_t *ui_comm_uart_label_tittle;
	lv_obj_t *ui_comm_uart_btn_rx_clean;
	lv_obj_t *ui_comm_uart_btn_rx_clean_label;
	lv_obj_t *ui_comm_uart_btn_back;
	lv_obj_t *ui_comm_uart_btn_back_label;
	lv_obj_t *ui_comm_rc;
	bool ui_comm_rc_del;
	lv_obj_t *ui_comm_rc_label_tittle;
	lv_obj_t *ui_comm_rc_btn_back;
	lv_obj_t *ui_comm_rc_btn_back_label;
	lv_obj_t *ui_comm_rc_cont_1;
	lv_obj_t *ui_comm_rc_label_1;
	lv_obj_t *ui_comm_rc_label_2;
	lv_obj_t *ui_comm_rc_label_3;
	lv_obj_t *ui_comm_rc_label_4;
	lv_obj_t *ui_comm_rc_label_5;
	lv_obj_t *ui_comm_rc_label_6;
	lv_obj_t *ui_comm_rc_label_7;
	lv_obj_t *ui_comm_rc_label_8;
	lv_obj_t *ui_comm_rc_label_9;
	lv_obj_t *ui_comm_rc_label_10;
	lv_obj_t *ui_comm_rc_label_11;
	lv_obj_t *ui_comm_rc_label_12;
	lv_obj_t *ui_comm_rc_label_13;
	lv_obj_t *ui_comm_rc_label_14;
	lv_obj_t *ui_comm_rc_label_15;
	lv_obj_t *ui_comm_rc_label_16;
	lv_obj_t *ui_comm_rc_bar_1;
	lv_obj_t *ui_comm_rc_bar_2;
	lv_obj_t *ui_comm_rc_bar_3;
	lv_obj_t *ui_comm_rc_bar_4;
	lv_obj_t *ui_comm_rc_bar_5;
	lv_obj_t *ui_comm_rc_bar_6;
	lv_obj_t *ui_comm_rc_bar_7;
	lv_obj_t *ui_comm_rc_bar_8;
	lv_obj_t *ui_comm_rc_bar_9;
	lv_obj_t *ui_comm_rc_bar_10;
	lv_obj_t *ui_comm_rc_bar_11;
	lv_obj_t *ui_comm_rc_bar_12;
	lv_obj_t *ui_comm_rc_bar_13;
	lv_obj_t *ui_comm_rc_bar_14;
	lv_obj_t *ui_comm_rc_bar_15;
	lv_obj_t *ui_comm_rc_bar_16;
	lv_obj_t *ui_io;
	bool ui_io_del;
	lv_obj_t *ui_io_label_title;
	lv_obj_t *ui_io_btn_home;
	lv_obj_t *ui_io_btn_home_label;
	lv_obj_t *ui_led;
	bool ui_led_del;
	lv_obj_t *ui_led_slider_period;
	lv_obj_t *ui_led_label_period;
	lv_obj_t *ui_led_label_blink;
	lv_obj_t *ui_led_cb_sta;
	lv_obj_t *ui_led_cb_blink;
	lv_obj_t *ui_led_label_title;
	lv_obj_t *ui_led_btn_home;
	lv_obj_t *ui_led_btn_home_label;
	lv_obj_t *g_kb_top_layer;
}lv_ui;

typedef void (*ui_setup_scr_t)(lv_ui * ui);

void ui_init_style(lv_style_t * style);

void ui_load_scr_animation(lv_ui *ui, lv_obj_t ** new_scr, bool new_scr_del, bool * old_scr_del, ui_setup_scr_t setup_scr,
                           lv_scr_load_anim_t anim_type, uint32_t time, uint32_t delay, bool is_clean, bool auto_del);

void ui_animation(void * var, int32_t duration, int32_t delay, int32_t start_value, int32_t end_value, lv_anim_path_cb_t path_cb,
                       uint16_t repeat_cnt, uint32_t repeat_delay, uint32_t playback_time, uint32_t playback_delay,
                       lv_anim_exec_xcb_t exec_cb, lv_anim_start_cb_t start_cb, lv_anim_ready_cb_t ready_cb, lv_anim_deleted_cb_t deleted_cb);


void init_scr_del_flag(lv_ui *ui);

void setup_ui(lv_ui *ui);

void init_keyboard(lv_ui *ui);

extern lv_ui guider_ui;


void setup_scr_ui_main(lv_ui *ui);
void setup_scr_ui_settings(lv_ui *ui);
void setup_scr_ui_storage(lv_ui *ui);
void setup_scr_ui_comm(lv_ui *ui);
void setup_scr_ui_comm_can(lv_ui *ui);
void setup_scr_ui_comm_uart(lv_ui *ui);
void setup_scr_ui_comm_rc(lv_ui *ui);
void setup_scr_ui_io(lv_ui *ui);
void setup_scr_ui_led(lv_ui *ui);

LV_FONT_DECLARE(lv_font_montserratMedium_16)
LV_FONT_DECLARE(lv_font_montserratMedium_12)
LV_FONT_DECLARE(lv_font_montserratMedium_14)
LV_FONT_DECLARE(lv_font_SourceHanSerifSC_Regular_18)


#ifdef __cplusplus
}
#endif
#endif
