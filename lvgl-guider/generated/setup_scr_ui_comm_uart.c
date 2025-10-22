/*
* Copyright 2025 NXP
* NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
* accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
* activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
* comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
* terms, then you may not retain, install, activate or otherwise use the software.
*/

#include "lvgl.h"
#include <stdio.h>
#include "gui_guider.h"
#include "events_init.h"
#include "widgets_init.h"
#include "custom.h"



void setup_scr_ui_comm_uart(lv_ui *ui)
{
    //Write codes ui_comm_uart
    ui->ui_comm_uart = lv_obj_create(NULL);
    lv_obj_set_size(ui->ui_comm_uart, 320, 240);
    lv_obj_set_scrollbar_mode(ui->ui_comm_uart, LV_SCROLLBAR_MODE_OFF);

    //Write style for ui_comm_uart, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_ta_rx_buf
    ui->ui_comm_uart_ta_rx_buf = lv_textarea_create(ui->ui_comm_uart);
    lv_textarea_set_text(ui->ui_comm_uart_ta_rx_buf, "");
    lv_textarea_set_placeholder_text(ui->ui_comm_uart_ta_rx_buf, "rx buf");
    lv_textarea_set_password_bullet(ui->ui_comm_uart_ta_rx_buf, "*");
    lv_textarea_set_password_mode(ui->ui_comm_uart_ta_rx_buf, false);
    lv_textarea_set_one_line(ui->ui_comm_uart_ta_rx_buf, false);
    lv_textarea_set_accepted_chars(ui->ui_comm_uart_ta_rx_buf, "");
    lv_textarea_set_max_length(ui->ui_comm_uart_ta_rx_buf, 512);
#if LV_USE_KEYBOARD != 0 || LV_USE_ZH_KEYBOARD != 0
    lv_obj_add_event_cb(ui->ui_comm_uart_ta_rx_buf, ta_event_cb, LV_EVENT_ALL, ui->g_kb_top_layer);
#endif
    lv_obj_set_pos(ui->ui_comm_uart_ta_rx_buf, 5, 145);
    lv_obj_set_size(ui->ui_comm_uart_ta_rx_buf, 310, 90);

    //Write style for ui_comm_uart_ta_rx_buf, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_text_color(ui->ui_comm_uart_ta_rx_buf, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_ta_rx_buf, &lv_font_montserratMedium_12, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_ta_rx_buf, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_uart_ta_rx_buf, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_uart_ta_rx_buf, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ta_rx_buf, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ta_rx_buf, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ta_rx_buf, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_ta_rx_buf, 2, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_ta_rx_buf, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_ta_rx_buf, lv_color_hex(0xe6e6e6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_ta_rx_buf, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_ta_rx_buf, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_ta_rx_buf, 4, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_ta_rx_buf, 4, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_ta_rx_buf, 4, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ta_rx_buf, 4, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_uart_ta_rx_buf, Part: LV_PART_SCROLLBAR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ta_rx_buf, 255, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ta_rx_buf, lv_color_hex(0x2195f6), LV_PART_SCROLLBAR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ta_rx_buf, LV_GRAD_DIR_NONE, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ta_rx_buf, 0, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_ddlist_rx_fmt
    ui->ui_comm_uart_ddlist_rx_fmt = lv_dropdown_create(ui->ui_comm_uart);
    lv_dropdown_set_options(ui->ui_comm_uart_ddlist_rx_fmt, "H\nD");
    lv_obj_set_pos(ui->ui_comm_uart_ddlist_rx_fmt, 265, 110);
    lv_obj_set_size(ui->ui_comm_uart_ddlist_rx_fmt, 50, 30);

    //Write style for ui_comm_uart_ddlist_rx_fmt, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_text_color(ui->ui_comm_uart_ddlist_rx_fmt, lv_color_hex(0x0D3055), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_ddlist_rx_fmt, &lv_font_montserratMedium_14, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_ddlist_rx_fmt, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_ddlist_rx_fmt, 1, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_ddlist_rx_fmt, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_ddlist_rx_fmt, lv_color_hex(0xe1e6ee), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_ddlist_rx_fmt, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_ddlist_rx_fmt, 8, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_ddlist_rx_fmt, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_ddlist_rx_fmt, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ddlist_rx_fmt, 3, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ddlist_rx_fmt, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ddlist_rx_fmt, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ddlist_rx_fmt, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_ddlist_rx_fmt, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_CHECKED for &style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked
    static lv_style_t style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked;
    ui_init_style(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked);

    lv_style_set_border_width(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, lv_color_hex(0x00a1b5));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_rx_fmt), &style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, LV_PART_SELECTED|LV_STATE_CHECKED);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default
    static lv_style_t style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default;
    ui_init_style(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default);

    lv_style_set_max_height(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, 90);
    lv_style_set_text_color(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, lv_color_hex(0x0D3055));
    lv_style_set_text_font(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, &lv_font_montserratMedium_16);
    lv_style_set_text_opa(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, 255);
    lv_style_set_border_width(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_rx_fmt), &style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default
    static lv_style_t style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default;
    ui_init_style(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default);

    lv_style_set_radius(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default, lv_color_hex(0x00ff00));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_rx_fmt), &style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_ddlist_check
    ui->ui_comm_uart_ddlist_check = lv_dropdown_create(ui->ui_comm_uart);
    lv_dropdown_set_options(ui->ui_comm_uart_ddlist_check, "NONE\nODD\nEVEN");
    lv_obj_set_pos(ui->ui_comm_uart_ddlist_check, 170, 110);
    lv_obj_set_size(ui->ui_comm_uart_ddlist_check, 90, 30);

    //Write style for ui_comm_uart_ddlist_check, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_text_color(ui->ui_comm_uart_ddlist_check, lv_color_hex(0x0D3055), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_ddlist_check, &lv_font_montserratMedium_14, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_ddlist_check, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_ddlist_check, 1, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_ddlist_check, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_ddlist_check, lv_color_hex(0xe1e6ee), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_ddlist_check, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_ddlist_check, 8, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_ddlist_check, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_ddlist_check, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ddlist_check, 3, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ddlist_check, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ddlist_check, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ddlist_check, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_ddlist_check, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_CHECKED for &style_ui_comm_uart_ddlist_check_extra_list_selected_checked
    static lv_style_t style_ui_comm_uart_ddlist_check_extra_list_selected_checked;
    ui_init_style(&style_ui_comm_uart_ddlist_check_extra_list_selected_checked);

    lv_style_set_border_width(&style_ui_comm_uart_ddlist_check_extra_list_selected_checked, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_check_extra_list_selected_checked, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_check_extra_list_selected_checked, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_check_extra_list_selected_checked, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_check_extra_list_selected_checked, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_check_extra_list_selected_checked, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_check_extra_list_selected_checked, lv_color_hex(0x00a1b5));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_check_extra_list_selected_checked, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_check), &style_ui_comm_uart_ddlist_check_extra_list_selected_checked, LV_PART_SELECTED|LV_STATE_CHECKED);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_check_extra_list_main_default
    static lv_style_t style_ui_comm_uart_ddlist_check_extra_list_main_default;
    ui_init_style(&style_ui_comm_uart_ddlist_check_extra_list_main_default);

    lv_style_set_max_height(&style_ui_comm_uart_ddlist_check_extra_list_main_default, 90);
    lv_style_set_text_color(&style_ui_comm_uart_ddlist_check_extra_list_main_default, lv_color_hex(0x0D3055));
    lv_style_set_text_font(&style_ui_comm_uart_ddlist_check_extra_list_main_default, &lv_font_montserratMedium_16);
    lv_style_set_text_opa(&style_ui_comm_uart_ddlist_check_extra_list_main_default, 255);
    lv_style_set_border_width(&style_ui_comm_uart_ddlist_check_extra_list_main_default, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_check_extra_list_main_default, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_check_extra_list_main_default, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_check_extra_list_main_default, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_check_extra_list_main_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_check_extra_list_main_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_check_extra_list_main_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_check_extra_list_main_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_check), &style_ui_comm_uart_ddlist_check_extra_list_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default
    static lv_style_t style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default;
    ui_init_style(&style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default);

    lv_style_set_radius(&style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default, lv_color_hex(0x00ff00));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_check), &style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_ddlist_data_bit
    ui->ui_comm_uart_ddlist_data_bit = lv_dropdown_create(ui->ui_comm_uart);
    lv_dropdown_set_options(ui->ui_comm_uart_ddlist_data_bit, "8\n9\n7\n6\n5");
    lv_obj_set_pos(ui->ui_comm_uart_ddlist_data_bit, 115, 110);
    lv_obj_set_size(ui->ui_comm_uart_ddlist_data_bit, 50, 30);

    //Write style for ui_comm_uart_ddlist_data_bit, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_text_color(ui->ui_comm_uart_ddlist_data_bit, lv_color_hex(0x0D3055), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_ddlist_data_bit, &lv_font_montserratMedium_14, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_ddlist_data_bit, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_ddlist_data_bit, 1, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_ddlist_data_bit, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_ddlist_data_bit, lv_color_hex(0xe1e6ee), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_ddlist_data_bit, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_ddlist_data_bit, 8, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_ddlist_data_bit, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_ddlist_data_bit, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ddlist_data_bit, 3, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ddlist_data_bit, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ddlist_data_bit, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ddlist_data_bit, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_ddlist_data_bit, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_CHECKED for &style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked
    static lv_style_t style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked;
    ui_init_style(&style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked);

    lv_style_set_border_width(&style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, lv_color_hex(0x00a1b5));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_data_bit), &style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, LV_PART_SELECTED|LV_STATE_CHECKED);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_data_bit_extra_list_main_default
    static lv_style_t style_ui_comm_uart_ddlist_data_bit_extra_list_main_default;
    ui_init_style(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default);

    lv_style_set_max_height(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, 90);
    lv_style_set_text_color(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, lv_color_hex(0x0D3055));
    lv_style_set_text_font(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, &lv_font_montserratMedium_16);
    lv_style_set_text_opa(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, 255);
    lv_style_set_border_width(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_data_bit), &style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default
    static lv_style_t style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default;
    ui_init_style(&style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default);

    lv_style_set_radius(&style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default, lv_color_hex(0x00ff00));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_data_bit), &style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_ddlist_stop
    ui->ui_comm_uart_ddlist_stop = lv_dropdown_create(ui->ui_comm_uart);
    lv_dropdown_set_options(ui->ui_comm_uart_ddlist_stop, "1\n1.5\n2");
    lv_obj_set_pos(ui->ui_comm_uart_ddlist_stop, 60, 110);
    lv_obj_set_size(ui->ui_comm_uart_ddlist_stop, 50, 30);

    //Write style for ui_comm_uart_ddlist_stop, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_text_color(ui->ui_comm_uart_ddlist_stop, lv_color_hex(0x0D3055), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_ddlist_stop, &lv_font_montserratMedium_14, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_ddlist_stop, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_ddlist_stop, 1, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_ddlist_stop, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_ddlist_stop, lv_color_hex(0xe1e6ee), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_ddlist_stop, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_ddlist_stop, 8, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_ddlist_stop, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_ddlist_stop, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ddlist_stop, 3, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ddlist_stop, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ddlist_stop, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ddlist_stop, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_ddlist_stop, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_CHECKED for &style_ui_comm_uart_ddlist_stop_extra_list_selected_checked
    static lv_style_t style_ui_comm_uart_ddlist_stop_extra_list_selected_checked;
    ui_init_style(&style_ui_comm_uart_ddlist_stop_extra_list_selected_checked);

    lv_style_set_border_width(&style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, lv_color_hex(0x00a1b5));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_stop), &style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, LV_PART_SELECTED|LV_STATE_CHECKED);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_stop_extra_list_main_default
    static lv_style_t style_ui_comm_uart_ddlist_stop_extra_list_main_default;
    ui_init_style(&style_ui_comm_uart_ddlist_stop_extra_list_main_default);

    lv_style_set_max_height(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, 90);
    lv_style_set_text_color(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, lv_color_hex(0x0D3055));
    lv_style_set_text_font(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, &lv_font_montserratMedium_16);
    lv_style_set_text_opa(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, 255);
    lv_style_set_border_width(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_stop_extra_list_main_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_stop), &style_ui_comm_uart_ddlist_stop_extra_list_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default
    static lv_style_t style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default;
    ui_init_style(&style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default);

    lv_style_set_radius(&style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default, lv_color_hex(0x00ff00));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_stop), &style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_cb_time_stamp
    ui->ui_comm_uart_cb_time_stamp = lv_checkbox_create(ui->ui_comm_uart);
    lv_checkbox_set_text(ui->ui_comm_uart_cb_time_stamp, "T");
    lv_obj_set_pos(ui->ui_comm_uart_cb_time_stamp, 5, 114);

    //Write style for ui_comm_uart_cb_time_stamp, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_pad_top(ui->ui_comm_uart_cb_time_stamp, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_cb_time_stamp, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_cb_time_stamp, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_uart_cb_time_stamp, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_uart_cb_time_stamp, lv_color_hex(0x0D3055), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_cb_time_stamp, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_cb_time_stamp, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_uart_cb_time_stamp, 2, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_cb_time_stamp, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_cb_time_stamp, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_cb_time_stamp, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_cb_time_stamp, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_cb_time_stamp, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_cb_time_stamp, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_uart_cb_time_stamp, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_pad_all(ui->ui_comm_uart_cb_time_stamp, 3, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_cb_time_stamp, 2, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_cb_time_stamp, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_cb_time_stamp, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_cb_time_stamp, LV_BORDER_SIDE_FULL, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_cb_time_stamp, 6, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_cb_time_stamp, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_cb_time_stamp, lv_color_hex(0xffffff), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_cb_time_stamp, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_ddlist_tx_fmt
    ui->ui_comm_uart_ddlist_tx_fmt = lv_dropdown_create(ui->ui_comm_uart);
    lv_dropdown_set_options(ui->ui_comm_uart_ddlist_tx_fmt, "H\nD");
    lv_obj_set_pos(ui->ui_comm_uart_ddlist_tx_fmt, 265, 75);
    lv_obj_set_size(ui->ui_comm_uart_ddlist_tx_fmt, 50, 30);

    //Write style for ui_comm_uart_ddlist_tx_fmt, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_text_color(ui->ui_comm_uart_ddlist_tx_fmt, lv_color_hex(0x0D3055), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_ddlist_tx_fmt, &lv_font_montserratMedium_14, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_ddlist_tx_fmt, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_ddlist_tx_fmt, 1, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_ddlist_tx_fmt, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_ddlist_tx_fmt, lv_color_hex(0xe1e6ee), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_ddlist_tx_fmt, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_ddlist_tx_fmt, 8, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_ddlist_tx_fmt, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_ddlist_tx_fmt, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ddlist_tx_fmt, 3, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ddlist_tx_fmt, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ddlist_tx_fmt, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ddlist_tx_fmt, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_ddlist_tx_fmt, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_CHECKED for &style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked
    static lv_style_t style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked;
    ui_init_style(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked);

    lv_style_set_border_width(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, lv_color_hex(0x00a1b5));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_tx_fmt), &style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, LV_PART_SELECTED|LV_STATE_CHECKED);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default
    static lv_style_t style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default;
    ui_init_style(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default);

    lv_style_set_max_height(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, 90);
    lv_style_set_text_color(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, lv_color_hex(0x0D3055));
    lv_style_set_text_font(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, &lv_font_montserratMedium_16);
    lv_style_set_text_opa(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, 255);
    lv_style_set_border_width(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_tx_fmt), &style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default
    static lv_style_t style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default;
    ui_init_style(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default);

    lv_style_set_radius(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default, lv_color_hex(0x00ff00));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_tx_fmt), &style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_ddlist_ch
    ui->ui_comm_uart_ddlist_ch = lv_dropdown_create(ui->ui_comm_uart);
    lv_dropdown_set_options(ui->ui_comm_uart_ddlist_ch, "LOG\nRC\nRS485\nUART2");
    lv_obj_set_pos(ui->ui_comm_uart_ddlist_ch, 170, 75);
    lv_obj_set_size(ui->ui_comm_uart_ddlist_ch, 90, 30);

    //Write style for ui_comm_uart_ddlist_ch, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_text_color(ui->ui_comm_uart_ddlist_ch, lv_color_hex(0x0D3055), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_ddlist_ch, &lv_font_montserratMedium_14, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_ddlist_ch, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_ddlist_ch, 1, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_ddlist_ch, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_ddlist_ch, lv_color_hex(0xe1e6ee), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_ddlist_ch, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_ddlist_ch, 8, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_ddlist_ch, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_ddlist_ch, 6, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ddlist_ch, 3, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ddlist_ch, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ddlist_ch, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ddlist_ch, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_ddlist_ch, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_CHECKED for &style_ui_comm_uart_ddlist_ch_extra_list_selected_checked
    static lv_style_t style_ui_comm_uart_ddlist_ch_extra_list_selected_checked;
    ui_init_style(&style_ui_comm_uart_ddlist_ch_extra_list_selected_checked);

    lv_style_set_border_width(&style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, lv_color_hex(0x00a1b5));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_ch), &style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, LV_PART_SELECTED|LV_STATE_CHECKED);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_ch_extra_list_main_default
    static lv_style_t style_ui_comm_uart_ddlist_ch_extra_list_main_default;
    ui_init_style(&style_ui_comm_uart_ddlist_ch_extra_list_main_default);

    lv_style_set_max_height(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, 90);
    lv_style_set_text_color(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, lv_color_hex(0x0D3055));
    lv_style_set_text_font(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, &lv_font_montserratMedium_16);
    lv_style_set_text_opa(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, 255);
    lv_style_set_border_width(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, 1);
    lv_style_set_border_opa(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, 255);
    lv_style_set_border_color(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_ch_extra_list_main_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_ch), &style_ui_comm_uart_ddlist_ch_extra_list_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default
    static lv_style_t style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default;
    ui_init_style(&style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default);

    lv_style_set_radius(&style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default, 255);
    lv_style_set_bg_color(&style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default, lv_color_hex(0x00ff00));
    lv_style_set_bg_grad_dir(&style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(lv_dropdown_get_list(ui->ui_comm_uart_ddlist_ch), &style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_ta_rate
    ui->ui_comm_uart_ta_rate = lv_textarea_create(ui->ui_comm_uart);
    lv_textarea_set_text(ui->ui_comm_uart_ta_rate, "921600");
    lv_textarea_set_placeholder_text(ui->ui_comm_uart_ta_rate, "");
    lv_textarea_set_password_bullet(ui->ui_comm_uart_ta_rate, "*");
    lv_textarea_set_password_mode(ui->ui_comm_uart_ta_rate, false);
    lv_textarea_set_one_line(ui->ui_comm_uart_ta_rate, false);
    lv_textarea_set_accepted_chars(ui->ui_comm_uart_ta_rate, "");
    lv_textarea_set_max_length(ui->ui_comm_uart_ta_rate, 32);
#if LV_USE_KEYBOARD != 0 || LV_USE_ZH_KEYBOARD != 0
    lv_obj_add_event_cb(ui->ui_comm_uart_ta_rate, ta_event_cb, LV_EVENT_ALL, ui->g_kb_top_layer);
#endif
    lv_obj_set_pos(ui->ui_comm_uart_ta_rate, 60, 75);
    lv_obj_set_size(ui->ui_comm_uart_ta_rate, 105, 30);

    //Write style for ui_comm_uart_ta_rate, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_text_color(ui->ui_comm_uart_ta_rate, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_ta_rate, &lv_font_montserratMedium_14, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_ta_rate, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_uart_ta_rate, 2, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_uart_ta_rate, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ta_rate, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ta_rate, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ta_rate, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_ta_rate, 2, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_ta_rate, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_ta_rate, lv_color_hex(0xe6e6e6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_ta_rate, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_ta_rate, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_ta_rate, 4, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_ta_rate, 4, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_ta_rate, 4, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ta_rate, 4, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_uart_ta_rate, Part: LV_PART_SCROLLBAR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ta_rate, 255, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ta_rate, lv_color_hex(0x2195f6), LV_PART_SCROLLBAR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ta_rate, LV_GRAD_DIR_NONE, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ta_rate, 0, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_sw_uart
    ui->ui_comm_uart_sw_uart = lv_switch_create(ui->ui_comm_uart);
    lv_obj_set_pos(ui->ui_comm_uart_sw_uart, 5, 75);
    lv_obj_set_size(ui->ui_comm_uart_sw_uart, 50, 30);

    //Write style for ui_comm_uart_sw_uart, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_sw_uart, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_sw_uart, lv_color_hex(0xe6e2e6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_sw_uart, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_sw_uart, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_sw_uart, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_sw_uart, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_uart_sw_uart, Part: LV_PART_INDICATOR, State: LV_STATE_CHECKED.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_sw_uart, 255, LV_PART_INDICATOR|LV_STATE_CHECKED);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_sw_uart, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_CHECKED);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_sw_uart, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_CHECKED);
    lv_obj_set_style_border_width(ui->ui_comm_uart_sw_uart, 0, LV_PART_INDICATOR|LV_STATE_CHECKED);

    //Write style for ui_comm_uart_sw_uart, Part: LV_PART_KNOB, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_sw_uart, 255, LV_PART_KNOB|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_sw_uart, lv_color_hex(0xffffff), LV_PART_KNOB|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_sw_uart, LV_GRAD_DIR_NONE, LV_PART_KNOB|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_sw_uart, 0, LV_PART_KNOB|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_sw_uart, 10, LV_PART_KNOB|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_ta_tx_buf
    ui->ui_comm_uart_ta_tx_buf = lv_textarea_create(ui->ui_comm_uart);
    lv_textarea_set_text(ui->ui_comm_uart_ta_tx_buf, "");
    lv_textarea_set_placeholder_text(ui->ui_comm_uart_ta_tx_buf, "tx buf");
    lv_textarea_set_password_bullet(ui->ui_comm_uart_ta_tx_buf, "*");
    lv_textarea_set_password_mode(ui->ui_comm_uart_ta_tx_buf, false);
    lv_textarea_set_one_line(ui->ui_comm_uart_ta_tx_buf, true);
    lv_textarea_set_accepted_chars(ui->ui_comm_uart_ta_tx_buf, "");
    lv_textarea_set_max_length(ui->ui_comm_uart_ta_tx_buf, 32);
#if LV_USE_KEYBOARD != 0 || LV_USE_ZH_KEYBOARD != 0
    lv_obj_add_event_cb(ui->ui_comm_uart_ta_tx_buf, ta_event_cb, LV_EVENT_ALL, ui->g_kb_top_layer);
#endif
    lv_obj_set_pos(ui->ui_comm_uart_ta_tx_buf, 5, 40);
    lv_obj_set_size(ui->ui_comm_uart_ta_tx_buf, 310, 30);

    //Write style for ui_comm_uart_ta_tx_buf, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_text_color(ui->ui_comm_uart_ta_tx_buf, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_ta_tx_buf, &lv_font_montserratMedium_14, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_ta_tx_buf, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_uart_ta_tx_buf, 2, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_uart_ta_tx_buf, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ta_tx_buf, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ta_tx_buf, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ta_tx_buf, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_ta_tx_buf, 2, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_uart_ta_tx_buf, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_uart_ta_tx_buf, lv_color_hex(0xe6e6e6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_uart_ta_tx_buf, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_ta_tx_buf, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_ta_tx_buf, 4, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_ta_tx_buf, 4, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_ta_tx_buf, 4, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ta_tx_buf, 4, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_uart_ta_tx_buf, Part: LV_PART_SCROLLBAR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_ta_tx_buf, 255, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_ta_tx_buf, lv_color_hex(0x2195f6), LV_PART_SCROLLBAR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_ta_tx_buf, LV_GRAD_DIR_NONE, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_ta_tx_buf, 0, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_btn_tx
    ui->ui_comm_uart_btn_tx = lv_btn_create(ui->ui_comm_uart);
    ui->ui_comm_uart_btn_tx_label = lv_label_create(ui->ui_comm_uart_btn_tx);
    lv_label_set_text(ui->ui_comm_uart_btn_tx_label, "" LV_SYMBOL_UPLOAD "");
    lv_label_set_long_mode(ui->ui_comm_uart_btn_tx_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_comm_uart_btn_tx_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_comm_uart_btn_tx, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_comm_uart_btn_tx_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_comm_uart_btn_tx, 275, 5);
    lv_obj_set_size(ui->ui_comm_uart_btn_tx, 40, 30);

    //Write style for ui_comm_uart_btn_tx, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_btn_tx, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_btn_tx, lv_color_hex(0xff0027), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_btn_tx, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_btn_tx, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_btn_tx, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_btn_tx, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_uart_btn_tx, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_btn_tx, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_btn_tx, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_uart_btn_tx, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_btn_tx_clean
    ui->ui_comm_uart_btn_tx_clean = lv_btn_create(ui->ui_comm_uart);
    ui->ui_comm_uart_btn_tx_clean_label = lv_label_create(ui->ui_comm_uart_btn_tx_clean);
    lv_label_set_text(ui->ui_comm_uart_btn_tx_clean_label, "" LV_SYMBOL_TRASH "");
    lv_label_set_long_mode(ui->ui_comm_uart_btn_tx_clean_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_comm_uart_btn_tx_clean_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_comm_uart_btn_tx_clean, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_comm_uart_btn_tx_clean_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_comm_uart_btn_tx_clean, 230, 5);
    lv_obj_set_size(ui->ui_comm_uart_btn_tx_clean, 40, 30);

    //Write style for ui_comm_uart_btn_tx_clean, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_btn_tx_clean, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_btn_tx_clean, lv_color_hex(0xff0027), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_btn_tx_clean, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_btn_tx_clean, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_btn_tx_clean, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_btn_tx_clean, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_uart_btn_tx_clean, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_btn_tx_clean, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_btn_tx_clean, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_uart_btn_tx_clean, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_label_tittle
    ui->ui_comm_uart_label_tittle = lv_label_create(ui->ui_comm_uart);
    lv_label_set_text(ui->ui_comm_uart_label_tittle, "UART Data View");
    lv_label_set_long_mode(ui->ui_comm_uart_label_tittle, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_uart_label_tittle, 70, 15);
    lv_obj_set_size(ui->ui_comm_uart_label_tittle, 180, 30);

    //Write style for ui_comm_uart_label_tittle, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_uart_label_tittle, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_label_tittle, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_label_tittle, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_uart_label_tittle, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_btn_rx_clean
    ui->ui_comm_uart_btn_rx_clean = lv_btn_create(ui->ui_comm_uart);
    ui->ui_comm_uart_btn_rx_clean_label = lv_label_create(ui->ui_comm_uart_btn_rx_clean);
    lv_label_set_text(ui->ui_comm_uart_btn_rx_clean_label, "" LV_SYMBOL_TRASH "");
    lv_label_set_long_mode(ui->ui_comm_uart_btn_rx_clean_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_comm_uart_btn_rx_clean_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_comm_uart_btn_rx_clean, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_comm_uart_btn_rx_clean_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_comm_uart_btn_rx_clean, 50, 5);
    lv_obj_set_size(ui->ui_comm_uart_btn_rx_clean, 40, 30);

    //Write style for ui_comm_uart_btn_rx_clean, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_btn_rx_clean, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_btn_rx_clean, lv_color_hex(0xff0027), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_btn_rx_clean, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_btn_rx_clean, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_btn_rx_clean, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_btn_rx_clean, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_uart_btn_rx_clean, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_btn_rx_clean, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_btn_rx_clean, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_uart_btn_rx_clean, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_uart_btn_back
    ui->ui_comm_uart_btn_back = lv_btn_create(ui->ui_comm_uart);
    ui->ui_comm_uart_btn_back_label = lv_label_create(ui->ui_comm_uart_btn_back);
    lv_label_set_text(ui->ui_comm_uart_btn_back_label, "" LV_SYMBOL_LEFT " ");
    lv_label_set_long_mode(ui->ui_comm_uart_btn_back_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_comm_uart_btn_back_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_comm_uart_btn_back, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_comm_uart_btn_back_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_comm_uart_btn_back, 5, 5);
    lv_obj_set_size(ui->ui_comm_uart_btn_back, 40, 30);

    //Write style for ui_comm_uart_btn_back, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_uart_btn_back, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_uart_btn_back, lv_color_hex(0xff0027), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_uart_btn_back, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_uart_btn_back, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_uart_btn_back, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_uart_btn_back, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_uart_btn_back, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_uart_btn_back, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_uart_btn_back, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_uart_btn_back, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //The custom code of ui_comm_uart.
    // lv_obj_clear_state(guider_ui.ui_comm_uart_ta_rx_buf, LV_STATE_EDITED); // 关键：禁用编辑状态
    // lv_obj_clear_flag(guider_ui.ui_comm_uart_ta_rx_buf, LV_OBJ_FLAG_CLICKABLE);
    // lv_obj_clear_flag(guider_ui.ui_comm_uart_ta_rx_buf, LV_OBJ_FLAG_CLICK_FOCUSABLE);
    lv_obj_remove_event_cb(ui->ui_comm_uart_ta_tx_buf, ta_event_cb);

    //Update current screen layout.
    lv_obj_update_layout(ui->ui_comm_uart);

    //Init events for screen.
    events_init_ui_comm_uart(ui);
}
