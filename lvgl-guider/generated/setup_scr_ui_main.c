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



void setup_scr_ui_main(lv_ui *ui)
{
    //Write codes ui_main
    ui->ui_main = lv_obj_create(NULL);
    lv_obj_set_size(ui->ui_main, 320, 240);
    lv_obj_set_scrollbar_mode(ui->ui_main, LV_SCROLLBAR_MODE_OFF);

    //Write style for ui_main, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_main, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_main_btn_pwr
    ui->ui_main_btn_pwr = lv_btn_create(ui->ui_main);
    ui->ui_main_btn_pwr_label = lv_label_create(ui->ui_main_btn_pwr);
    lv_label_set_text(ui->ui_main_btn_pwr_label, "" LV_SYMBOL_POWER " ");
    lv_label_set_long_mode(ui->ui_main_btn_pwr_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_main_btn_pwr_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_main_btn_pwr, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_main_btn_pwr_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_main_btn_pwr, 260, 180);
    lv_obj_set_size(ui->ui_main_btn_pwr, 40, 40);

    //Write style for ui_main_btn_pwr, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_main_btn_pwr, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_main_btn_pwr, lv_color_hex(0xff0027), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_main_btn_pwr, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_main_btn_pwr, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_main_btn_pwr, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_main_btn_pwr, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_main_btn_pwr, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_main_btn_pwr, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_main_btn_pwr, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_main_btn_pwr, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_main_btn_io
    ui->ui_main_btn_io = lv_btn_create(ui->ui_main);
    ui->ui_main_btn_io_label = lv_label_create(ui->ui_main_btn_io);
    lv_label_set_text(ui->ui_main_btn_io_label, "" LV_SYMBOL_GPS " ");
    lv_label_set_long_mode(ui->ui_main_btn_io_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_main_btn_io_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_main_btn_io, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_main_btn_io_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_main_btn_io, 260, 20);
    lv_obj_set_size(ui->ui_main_btn_io, 40, 40);

    //Write style for ui_main_btn_io, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_main_btn_io, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_main_btn_io, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_main_btn_io, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_main_btn_io, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_main_btn_io, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_main_btn_io, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_main_btn_io, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_main_btn_io, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_main_btn_io, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_main_btn_io, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_main_btn_comm
    ui->ui_main_btn_comm = lv_btn_create(ui->ui_main);
    ui->ui_main_btn_comm_label = lv_label_create(ui->ui_main_btn_comm);
    lv_label_set_text(ui->ui_main_btn_comm_label, "" LV_SYMBOL_USB " ");
    lv_label_set_long_mode(ui->ui_main_btn_comm_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_main_btn_comm_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_main_btn_comm, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_main_btn_comm_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_main_btn_comm, 200, 20);
    lv_obj_set_size(ui->ui_main_btn_comm, 40, 40);

    //Write style for ui_main_btn_comm, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_main_btn_comm, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_main_btn_comm, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_main_btn_comm, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_main_btn_comm, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_main_btn_comm, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_main_btn_comm, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_main_btn_comm, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_main_btn_comm, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_main_btn_comm, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_main_btn_comm, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_main_btn_led
    ui->ui_main_btn_led = lv_btn_create(ui->ui_main);
    ui->ui_main_btn_led_label = lv_label_create(ui->ui_main_btn_led);
    lv_label_set_text(ui->ui_main_btn_led_label, "" LV_SYMBOL_CHARGE " ");
    lv_label_set_long_mode(ui->ui_main_btn_led_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_main_btn_led_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_main_btn_led, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_main_btn_led_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_main_btn_led, 140, 20);
    lv_obj_set_size(ui->ui_main_btn_led, 40, 40);

    //Write style for ui_main_btn_led, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_main_btn_led, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_main_btn_led, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_main_btn_led, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_main_btn_led, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_main_btn_led, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_main_btn_led, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_main_btn_led, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_main_btn_led, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_main_btn_led, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_main_btn_led, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_main_btn_storage
    ui->ui_main_btn_storage = lv_btn_create(ui->ui_main);
    ui->ui_main_btn_storage_label = lv_label_create(ui->ui_main_btn_storage);
    lv_label_set_text(ui->ui_main_btn_storage_label, "" LV_SYMBOL_DIRECTORY " ");
    lv_label_set_long_mode(ui->ui_main_btn_storage_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_main_btn_storage_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_main_btn_storage, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_main_btn_storage_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_main_btn_storage, 80, 20);
    lv_obj_set_size(ui->ui_main_btn_storage, 40, 40);

    //Write style for ui_main_btn_storage, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_main_btn_storage, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_main_btn_storage, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_main_btn_storage, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_main_btn_storage, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_main_btn_storage, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_main_btn_storage, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_main_btn_storage, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_main_btn_storage, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_main_btn_storage, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_main_btn_storage, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_main_btn_settings
    ui->ui_main_btn_settings = lv_btn_create(ui->ui_main);
    ui->ui_main_btn_settings_label = lv_label_create(ui->ui_main_btn_settings);
    lv_label_set_text(ui->ui_main_btn_settings_label, "" LV_SYMBOL_SETTINGS " ");
    lv_label_set_long_mode(ui->ui_main_btn_settings_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_main_btn_settings_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_main_btn_settings, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_main_btn_settings_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_main_btn_settings, 20, 20);
    lv_obj_set_size(ui->ui_main_btn_settings, 40, 40);

    //Write style for ui_main_btn_settings, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_main_btn_settings, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_main_btn_settings, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_main_btn_settings, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_main_btn_settings, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_main_btn_settings, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_main_btn_settings, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_main_btn_settings, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_main_btn_settings, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_main_btn_settings, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_main_btn_settings, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //The custom code of ui_main.


    //Update current screen layout.
    lv_obj_update_layout(ui->ui_main);

    //Init events for screen.
    events_init_ui_main(ui);
}
