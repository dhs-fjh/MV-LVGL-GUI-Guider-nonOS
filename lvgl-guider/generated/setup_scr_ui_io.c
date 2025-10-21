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



void setup_scr_ui_io(lv_ui *ui)
{
    //Write codes ui_io
    ui->ui_io = lv_obj_create(NULL);
    lv_obj_set_size(ui->ui_io, 320, 240);
    lv_obj_set_scrollbar_mode(ui->ui_io, LV_SCROLLBAR_MODE_OFF);

    //Write style for ui_io, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_io, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_io_label_title
    ui->ui_io_label_title = lv_label_create(ui->ui_io);
    lv_label_set_text(ui->ui_io_label_title, "IO Control");
    lv_label_set_long_mode(ui->ui_io_label_title, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_io_label_title, 70, 15);
    lv_obj_set_size(ui->ui_io_label_title, 180, 30);

    //Write style for ui_io_label_title, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_io_label_title, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_io_label_title, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_io_label_title, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_io_label_title, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_io_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_io_btn_home
    ui->ui_io_btn_home = lv_btn_create(ui->ui_io);
    ui->ui_io_btn_home_label = lv_label_create(ui->ui_io_btn_home);
    lv_label_set_text(ui->ui_io_btn_home_label, "" LV_SYMBOL_HOME " ");
    lv_label_set_long_mode(ui->ui_io_btn_home_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_io_btn_home_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_io_btn_home, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_io_btn_home_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_io_btn_home, 5, 5);
    lv_obj_set_size(ui->ui_io_btn_home, 40, 30);

    //Write style for ui_io_btn_home, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_io_btn_home, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_io_btn_home, lv_color_hex(0xff0027), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_io_btn_home, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_io_btn_home, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_io_btn_home, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_io_btn_home, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_io_btn_home, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_io_btn_home, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_io_btn_home, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_io_btn_home, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //The custom code of ui_io.


    //Update current screen layout.
    lv_obj_update_layout(ui->ui_io);

    //Init events for screen.
    events_init_ui_io(ui);
}
