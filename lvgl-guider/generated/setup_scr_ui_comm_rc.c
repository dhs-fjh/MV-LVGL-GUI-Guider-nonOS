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



void setup_scr_ui_comm_rc(lv_ui *ui)
{
    //Write codes ui_comm_rc
    ui->ui_comm_rc = lv_obj_create(NULL);
    lv_obj_set_size(ui->ui_comm_rc, 320, 240);
    lv_obj_set_scrollbar_mode(ui->ui_comm_rc, LV_SCROLLBAR_MODE_OFF);

    //Write style for ui_comm_rc, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_tittle
    ui->ui_comm_rc_label_tittle = lv_label_create(ui->ui_comm_rc);
    lv_label_set_text(ui->ui_comm_rc_label_tittle, "RC Data View");
    lv_label_set_long_mode(ui->ui_comm_rc_label_tittle, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_tittle, 70, 15);
    lv_obj_set_size(ui->ui_comm_rc_label_tittle, 180, 30);

    //Write style for ui_comm_rc_label_tittle, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_tittle, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_tittle, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_tittle, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_tittle, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_tittle, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_btn_back
    ui->ui_comm_rc_btn_back = lv_btn_create(ui->ui_comm_rc);
    ui->ui_comm_rc_btn_back_label = lv_label_create(ui->ui_comm_rc_btn_back);
    lv_label_set_text(ui->ui_comm_rc_btn_back_label, "" LV_SYMBOL_LEFT " ");
    lv_label_set_long_mode(ui->ui_comm_rc_btn_back_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_comm_rc_btn_back_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_comm_rc_btn_back, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_comm_rc_btn_back_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_comm_rc_btn_back, 5, 5);
    lv_obj_set_size(ui->ui_comm_rc_btn_back, 40, 30);

    //Write style for ui_comm_rc_btn_back, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_btn_back, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_btn_back, lv_color_hex(0xff0027), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_btn_back, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_rc_btn_back, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_btn_back, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_btn_back, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_btn_back, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_btn_back, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_btn_back, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_btn_back, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_cont_rc
    ui->ui_comm_rc_cont_rc = lv_obj_create(ui->ui_comm_rc);
    lv_obj_set_pos(ui->ui_comm_rc_cont_rc, 5, 40);
    lv_obj_set_size(ui->ui_comm_rc_cont_rc, 310, 195);
    lv_obj_set_scrollbar_mode(ui->ui_comm_rc_cont_rc, LV_SCROLLBAR_MODE_OFF);

    //Write style for ui_comm_rc_cont_rc, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_cont_rc, 2, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_opa(ui->ui_comm_rc_cont_rc, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_color(ui->ui_comm_rc_cont_rc, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_side(ui->ui_comm_rc_cont_rc, LV_BORDER_SIDE_FULL, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_cont_rc, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_cont_rc, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_cont_rc, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_cont_rc, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_cont_rc, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_cont_rc, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_cont_rc, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_cont_rc, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_cont_rc, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_1
    ui->ui_comm_rc_label_1 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_1, "CH1");
    lv_label_set_long_mode(ui->ui_comm_rc_label_1, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_1, 10, 10);
    lv_obj_set_size(ui->ui_comm_rc_label_1, 50, 16);

    //Write style for ui_comm_rc_label_1, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_1, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_1, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_1, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_1, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_2
    ui->ui_comm_rc_label_2 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_2, "CH2");
    lv_label_set_long_mode(ui->ui_comm_rc_label_2, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_2, 10, 40);
    lv_obj_set_size(ui->ui_comm_rc_label_2, 50, 16);

    //Write style for ui_comm_rc_label_2, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_2, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_2, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_2, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_2, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_3
    ui->ui_comm_rc_label_3 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_3, "CH3");
    lv_label_set_long_mode(ui->ui_comm_rc_label_3, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_3, 10, 70);
    lv_obj_set_size(ui->ui_comm_rc_label_3, 50, 16);

    //Write style for ui_comm_rc_label_3, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_3, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_3, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_3, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_3, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_4
    ui->ui_comm_rc_label_4 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_4, "CH4");
    lv_label_set_long_mode(ui->ui_comm_rc_label_4, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_4, 10, 100);
    lv_obj_set_size(ui->ui_comm_rc_label_4, 50, 16);

    //Write style for ui_comm_rc_label_4, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_4, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_4, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_4, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_4, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_5
    ui->ui_comm_rc_label_5 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_5, "CH5");
    lv_label_set_long_mode(ui->ui_comm_rc_label_5, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_5, 10, 130);
    lv_obj_set_size(ui->ui_comm_rc_label_5, 50, 16);

    //Write style for ui_comm_rc_label_5, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_5, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_5, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_5, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_5, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_6
    ui->ui_comm_rc_label_6 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_6, "CH6");
    lv_label_set_long_mode(ui->ui_comm_rc_label_6, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_6, 10, 160);
    lv_obj_set_size(ui->ui_comm_rc_label_6, 50, 16);

    //Write style for ui_comm_rc_label_6, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_6, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_6, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_6, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_6, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_7
    ui->ui_comm_rc_label_7 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_7, "CH7");
    lv_label_set_long_mode(ui->ui_comm_rc_label_7, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_7, 10, 190);
    lv_obj_set_size(ui->ui_comm_rc_label_7, 50, 16);

    //Write style for ui_comm_rc_label_7, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_7, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_7, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_7, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_7, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_8
    ui->ui_comm_rc_label_8 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_8, "CH8");
    lv_label_set_long_mode(ui->ui_comm_rc_label_8, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_8, 10, 220);
    lv_obj_set_size(ui->ui_comm_rc_label_8, 50, 16);

    //Write style for ui_comm_rc_label_8, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_8, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_8, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_8, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_8, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_9
    ui->ui_comm_rc_label_9 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_9, "CH9");
    lv_label_set_long_mode(ui->ui_comm_rc_label_9, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_9, 10, 250);
    lv_obj_set_size(ui->ui_comm_rc_label_9, 50, 16);

    //Write style for ui_comm_rc_label_9, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_9, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_9, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_9, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_9, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_10
    ui->ui_comm_rc_label_10 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_10, "CH10");
    lv_label_set_long_mode(ui->ui_comm_rc_label_10, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_10, 10, 280);
    lv_obj_set_size(ui->ui_comm_rc_label_10, 50, 16);

    //Write style for ui_comm_rc_label_10, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_10, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_10, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_10, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_10, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_11
    ui->ui_comm_rc_label_11 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_11, "CH11");
    lv_label_set_long_mode(ui->ui_comm_rc_label_11, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_11, 10, 310);
    lv_obj_set_size(ui->ui_comm_rc_label_11, 50, 16);

    //Write style for ui_comm_rc_label_11, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_11, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_11, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_11, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_11, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_12
    ui->ui_comm_rc_label_12 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_12, "CH12");
    lv_label_set_long_mode(ui->ui_comm_rc_label_12, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_12, 10, 340);
    lv_obj_set_size(ui->ui_comm_rc_label_12, 50, 16);

    //Write style for ui_comm_rc_label_12, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_12, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_12, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_12, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_12, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_13
    ui->ui_comm_rc_label_13 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_13, "CH13");
    lv_label_set_long_mode(ui->ui_comm_rc_label_13, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_13, 10, 370);
    lv_obj_set_size(ui->ui_comm_rc_label_13, 50, 16);

    //Write style for ui_comm_rc_label_13, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_13, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_13, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_13, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_13, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_14
    ui->ui_comm_rc_label_14 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_14, "CH14");
    lv_label_set_long_mode(ui->ui_comm_rc_label_14, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_14, 10, 400);
    lv_obj_set_size(ui->ui_comm_rc_label_14, 50, 16);

    //Write style for ui_comm_rc_label_14, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_14, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_14, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_14, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_14, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_15
    ui->ui_comm_rc_label_15 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_15, "CH15");
    lv_label_set_long_mode(ui->ui_comm_rc_label_15, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_15, 10, 430);
    lv_obj_set_size(ui->ui_comm_rc_label_15, 50, 16);

    //Write style for ui_comm_rc_label_15, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_15, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_15, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_15, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_15, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_label_16
    ui->ui_comm_rc_label_16 = lv_label_create(ui->ui_comm_rc_cont_rc);
    lv_label_set_text(ui->ui_comm_rc_label_16, "CH16");
    lv_label_set_long_mode(ui->ui_comm_rc_label_16, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_rc_label_16, 10, 460);
    lv_obj_set_size(ui->ui_comm_rc_label_16, 50, 16);

    //Write style for ui_comm_rc_label_16, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_rc_label_16, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_rc_label_16, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_rc_label_16, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_rc_label_16, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_label_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_1
    ui->ui_comm_rc_bar_1 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_1, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_1, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_1, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_1, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_1, 80, 10);
    lv_obj_set_size(ui->ui_comm_rc_bar_1, 200, 16);

    //Write style for ui_comm_rc_bar_1, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_1, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_1, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_1, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_1, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_1, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_1, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_1, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_1, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_1, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_2
    ui->ui_comm_rc_bar_2 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_2, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_2, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_2, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_2, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_2, 80, 40);
    lv_obj_set_size(ui->ui_comm_rc_bar_2, 200, 16);

    //Write style for ui_comm_rc_bar_2, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_2, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_2, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_2, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_2, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_2, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_2, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_2, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_2, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_2, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_3
    ui->ui_comm_rc_bar_3 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_3, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_3, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_3, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_3, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_3, 80, 70);
    lv_obj_set_size(ui->ui_comm_rc_bar_3, 200, 16);

    //Write style for ui_comm_rc_bar_3, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_3, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_3, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_3, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_3, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_3, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_3, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_3, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_3, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_3, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_4
    ui->ui_comm_rc_bar_4 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_4, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_4, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_4, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_4, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_4, 80, 100);
    lv_obj_set_size(ui->ui_comm_rc_bar_4, 200, 16);

    //Write style for ui_comm_rc_bar_4, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_4, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_4, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_4, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_4, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_4, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_4, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_4, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_4, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_4, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_4, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_5
    ui->ui_comm_rc_bar_5 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_5, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_5, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_5, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_5, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_5, 80, 130);
    lv_obj_set_size(ui->ui_comm_rc_bar_5, 200, 16);

    //Write style for ui_comm_rc_bar_5, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_5, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_5, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_5, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_5, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_5, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_5, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_5, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_5, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_5, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_5, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_6
    ui->ui_comm_rc_bar_6 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_6, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_6, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_6, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_6, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_6, 80, 160);
    lv_obj_set_size(ui->ui_comm_rc_bar_6, 200, 16);

    //Write style for ui_comm_rc_bar_6, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_6, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_6, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_6, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_6, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_6, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_6, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_6, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_6, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_6, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_6, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_7
    ui->ui_comm_rc_bar_7 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_7, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_7, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_7, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_7, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_7, 80, 190);
    lv_obj_set_size(ui->ui_comm_rc_bar_7, 200, 16);

    //Write style for ui_comm_rc_bar_7, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_7, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_7, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_7, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_7, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_7, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_7, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_7, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_7, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_7, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_7, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_8
    ui->ui_comm_rc_bar_8 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_8, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_8, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_8, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_8, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_8, 80, 220);
    lv_obj_set_size(ui->ui_comm_rc_bar_8, 200, 16);

    //Write style for ui_comm_rc_bar_8, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_8, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_8, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_8, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_8, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_8, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_8, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_8, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_8, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_8, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_8, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_9
    ui->ui_comm_rc_bar_9 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_9, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_9, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_9, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_9, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_9, 80, 250);
    lv_obj_set_size(ui->ui_comm_rc_bar_9, 200, 16);

    //Write style for ui_comm_rc_bar_9, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_9, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_9, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_9, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_9, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_9, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_9, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_9, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_9, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_9, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_9, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_10
    ui->ui_comm_rc_bar_10 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_10, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_10, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_10, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_10, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_10, 80, 280);
    lv_obj_set_size(ui->ui_comm_rc_bar_10, 200, 16);

    //Write style for ui_comm_rc_bar_10, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_10, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_10, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_10, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_10, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_10, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_10, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_10, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_10, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_10, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_10, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_11
    ui->ui_comm_rc_bar_11 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_11, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_11, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_11, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_11, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_11, 80, 310);
    lv_obj_set_size(ui->ui_comm_rc_bar_11, 200, 16);

    //Write style for ui_comm_rc_bar_11, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_11, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_11, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_11, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_11, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_11, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_11, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_11, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_11, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_11, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_11, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_12
    ui->ui_comm_rc_bar_12 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_12, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_12, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_12, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_12, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_12, 80, 340);
    lv_obj_set_size(ui->ui_comm_rc_bar_12, 200, 16);

    //Write style for ui_comm_rc_bar_12, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_12, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_12, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_12, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_12, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_12, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_12, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_12, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_12, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_12, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_12, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_13
    ui->ui_comm_rc_bar_13 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_13, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_13, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_13, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_13, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_13, 80, 370);
    lv_obj_set_size(ui->ui_comm_rc_bar_13, 200, 16);

    //Write style for ui_comm_rc_bar_13, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_13, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_13, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_13, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_13, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_13, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_13, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_13, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_13, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_13, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_13, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_14
    ui->ui_comm_rc_bar_14 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_14, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_14, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_14, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_14, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_14, 80, 400);
    lv_obj_set_size(ui->ui_comm_rc_bar_14, 200, 16);

    //Write style for ui_comm_rc_bar_14, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_14, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_14, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_14, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_14, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_14, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_14, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_14, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_14, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_14, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_14, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_15
    ui->ui_comm_rc_bar_15 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_15, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_15, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_15, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_15, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_15, 80, 430);
    lv_obj_set_size(ui->ui_comm_rc_bar_15, 200, 16);

    //Write style for ui_comm_rc_bar_15, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_15, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_15, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_15, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_15, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_15, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_15, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_15, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_15, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_15, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_15, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //Write codes ui_comm_rc_bar_16
    ui->ui_comm_rc_bar_16 = lv_bar_create(ui->ui_comm_rc_cont_rc);
    lv_obj_set_style_anim_time(ui->ui_comm_rc_bar_16, 1000, 0);
    lv_bar_set_mode(ui->ui_comm_rc_bar_16, LV_BAR_MODE_NORMAL);
    lv_bar_set_range(ui->ui_comm_rc_bar_16, 200, 1800);
    lv_bar_set_value(ui->ui_comm_rc_bar_16, 200, LV_ANIM_OFF);
    lv_obj_set_pos(ui->ui_comm_rc_bar_16, 80, 460);
    lv_obj_set_size(ui->ui_comm_rc_bar_16, 200, 16);

    //Write style for ui_comm_rc_bar_16, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_16, 60, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_16, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_16, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_16, 10, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_rc_bar_16, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style for ui_comm_rc_bar_16, Part: LV_PART_INDICATOR, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_rc_bar_16, 255, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_rc_bar_16, lv_color_hex(0x2195f6), LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_rc_bar_16, LV_GRAD_DIR_NONE, LV_PART_INDICATOR|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_rc_bar_16, 10, LV_PART_INDICATOR|LV_STATE_DEFAULT);

    //The custom code of ui_comm_rc.


    //Update current screen layout.
    lv_obj_update_layout(ui->ui_comm_rc);

    //Init events for screen.
    events_init_ui_comm_rc(ui);
}
