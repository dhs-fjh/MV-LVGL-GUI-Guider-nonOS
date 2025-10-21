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



void setup_scr_ui_comm(lv_ui *ui)
{
    //Write codes ui_comm
    ui->ui_comm = lv_obj_create(NULL);
    lv_obj_set_size(ui->ui_comm, 320, 240);
    lv_obj_set_scrollbar_mode(ui->ui_comm, LV_SCROLLBAR_MODE_OFF);

    //Write style for ui_comm, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_list_comm
    ui->ui_comm_list_comm = lv_list_create(ui->ui_comm);
    ui->ui_comm_list_comm_item0 = lv_list_add_btn(ui->ui_comm_list_comm, LV_SYMBOL_USB, "CAN");
    ui->ui_comm_list_comm_item1 = lv_list_add_btn(ui->ui_comm_list_comm, LV_SYMBOL_USB, "UART");
    ui->ui_comm_list_comm_item2 = lv_list_add_btn(ui->ui_comm_list_comm, LV_SYMBOL_USB, "RC");
    lv_obj_set_pos(ui->ui_comm_list_comm, 5, 40);
    lv_obj_set_size(ui->ui_comm_list_comm, 310, 195);
    lv_obj_set_scrollbar_mode(ui->ui_comm_list_comm, LV_SCROLLBAR_MODE_OFF);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_list_comm_main_main_default
    static lv_style_t style_ui_comm_list_comm_main_main_default;
    ui_init_style(&style_ui_comm_list_comm_main_main_default);

    lv_style_set_pad_top(&style_ui_comm_list_comm_main_main_default, 5);
    lv_style_set_pad_left(&style_ui_comm_list_comm_main_main_default, 5);
    lv_style_set_pad_right(&style_ui_comm_list_comm_main_main_default, 5);
    lv_style_set_pad_bottom(&style_ui_comm_list_comm_main_main_default, 5);
    lv_style_set_bg_opa(&style_ui_comm_list_comm_main_main_default, 255);
    lv_style_set_bg_color(&style_ui_comm_list_comm_main_main_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_list_comm_main_main_default, LV_GRAD_DIR_NONE);
    lv_style_set_border_width(&style_ui_comm_list_comm_main_main_default, 1);
    lv_style_set_border_opa(&style_ui_comm_list_comm_main_main_default, 255);
    lv_style_set_border_color(&style_ui_comm_list_comm_main_main_default, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_list_comm_main_main_default, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_list_comm_main_main_default, 3);
    lv_style_set_shadow_width(&style_ui_comm_list_comm_main_main_default, 0);
    lv_obj_add_style(ui->ui_comm_list_comm, &style_ui_comm_list_comm_main_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_FOCUSED for &style_ui_comm_list_comm_main_main_focused
    static lv_style_t style_ui_comm_list_comm_main_main_focused;
    ui_init_style(&style_ui_comm_list_comm_main_main_focused);

    lv_style_set_pad_top(&style_ui_comm_list_comm_main_main_focused, 5);
    lv_style_set_pad_left(&style_ui_comm_list_comm_main_main_focused, 5);
    lv_style_set_pad_right(&style_ui_comm_list_comm_main_main_focused, 5);
    lv_style_set_pad_bottom(&style_ui_comm_list_comm_main_main_focused, 5);
    lv_style_set_bg_opa(&style_ui_comm_list_comm_main_main_focused, 255);
    lv_style_set_bg_color(&style_ui_comm_list_comm_main_main_focused, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_list_comm_main_main_focused, LV_GRAD_DIR_NONE);
    lv_style_set_border_width(&style_ui_comm_list_comm_main_main_focused, 1);
    lv_style_set_border_opa(&style_ui_comm_list_comm_main_main_focused, 255);
    lv_style_set_border_color(&style_ui_comm_list_comm_main_main_focused, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_list_comm_main_main_focused, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_list_comm_main_main_focused, 3);
    lv_style_set_shadow_width(&style_ui_comm_list_comm_main_main_focused, 0);
    lv_obj_add_style(ui->ui_comm_list_comm, &style_ui_comm_list_comm_main_main_focused, LV_PART_MAIN|LV_STATE_FOCUSED);

    //Write style state: LV_STATE_DISABLED for &style_ui_comm_list_comm_main_main_disabled
    static lv_style_t style_ui_comm_list_comm_main_main_disabled;
    ui_init_style(&style_ui_comm_list_comm_main_main_disabled);

    lv_style_set_pad_top(&style_ui_comm_list_comm_main_main_disabled, 5);
    lv_style_set_pad_left(&style_ui_comm_list_comm_main_main_disabled, 5);
    lv_style_set_pad_right(&style_ui_comm_list_comm_main_main_disabled, 5);
    lv_style_set_pad_bottom(&style_ui_comm_list_comm_main_main_disabled, 5);
    lv_style_set_bg_opa(&style_ui_comm_list_comm_main_main_disabled, 255);
    lv_style_set_bg_color(&style_ui_comm_list_comm_main_main_disabled, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_list_comm_main_main_disabled, LV_GRAD_DIR_NONE);
    lv_style_set_border_width(&style_ui_comm_list_comm_main_main_disabled, 1);
    lv_style_set_border_opa(&style_ui_comm_list_comm_main_main_disabled, 255);
    lv_style_set_border_color(&style_ui_comm_list_comm_main_main_disabled, lv_color_hex(0xe1e6ee));
    lv_style_set_border_side(&style_ui_comm_list_comm_main_main_disabled, LV_BORDER_SIDE_FULL);
    lv_style_set_radius(&style_ui_comm_list_comm_main_main_disabled, 3);
    lv_style_set_shadow_width(&style_ui_comm_list_comm_main_main_disabled, 0);
    lv_obj_add_style(ui->ui_comm_list_comm, &style_ui_comm_list_comm_main_main_disabled, LV_PART_MAIN|LV_STATE_DISABLED);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_list_comm_main_scrollbar_default
    static lv_style_t style_ui_comm_list_comm_main_scrollbar_default;
    ui_init_style(&style_ui_comm_list_comm_main_scrollbar_default);

    lv_style_set_radius(&style_ui_comm_list_comm_main_scrollbar_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_list_comm_main_scrollbar_default, 255);
    lv_style_set_bg_color(&style_ui_comm_list_comm_main_scrollbar_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_list_comm_main_scrollbar_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(ui->ui_comm_list_comm, &style_ui_comm_list_comm_main_scrollbar_default, LV_PART_SCROLLBAR|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_list_comm_extra_btns_main_default
    static lv_style_t style_ui_comm_list_comm_extra_btns_main_default;
    ui_init_style(&style_ui_comm_list_comm_extra_btns_main_default);

    lv_style_set_pad_top(&style_ui_comm_list_comm_extra_btns_main_default, 5);
    lv_style_set_pad_left(&style_ui_comm_list_comm_extra_btns_main_default, 5);
    lv_style_set_pad_right(&style_ui_comm_list_comm_extra_btns_main_default, 5);
    lv_style_set_pad_bottom(&style_ui_comm_list_comm_extra_btns_main_default, 5);
    lv_style_set_border_width(&style_ui_comm_list_comm_extra_btns_main_default, 0);
    lv_style_set_text_color(&style_ui_comm_list_comm_extra_btns_main_default, lv_color_hex(0x0D3055));
    lv_style_set_text_font(&style_ui_comm_list_comm_extra_btns_main_default, &lv_font_montserratMedium_16);
    lv_style_set_text_opa(&style_ui_comm_list_comm_extra_btns_main_default, 255);
    lv_style_set_radius(&style_ui_comm_list_comm_extra_btns_main_default, 3);
    lv_style_set_bg_opa(&style_ui_comm_list_comm_extra_btns_main_default, 255);
    lv_style_set_bg_color(&style_ui_comm_list_comm_extra_btns_main_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_list_comm_extra_btns_main_default, LV_GRAD_DIR_NONE);
    lv_obj_add_style(ui->ui_comm_list_comm_item2, &style_ui_comm_list_comm_extra_btns_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_add_style(ui->ui_comm_list_comm_item1, &style_ui_comm_list_comm_extra_btns_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_add_style(ui->ui_comm_list_comm_item0, &style_ui_comm_list_comm_extra_btns_main_default, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write style state: LV_STATE_DEFAULT for &style_ui_comm_list_comm_extra_texts_main_default
    static lv_style_t style_ui_comm_list_comm_extra_texts_main_default;
    ui_init_style(&style_ui_comm_list_comm_extra_texts_main_default);

    lv_style_set_pad_top(&style_ui_comm_list_comm_extra_texts_main_default, 5);
    lv_style_set_pad_left(&style_ui_comm_list_comm_extra_texts_main_default, 5);
    lv_style_set_pad_right(&style_ui_comm_list_comm_extra_texts_main_default, 5);
    lv_style_set_pad_bottom(&style_ui_comm_list_comm_extra_texts_main_default, 5);
    lv_style_set_border_width(&style_ui_comm_list_comm_extra_texts_main_default, 0);
    lv_style_set_text_color(&style_ui_comm_list_comm_extra_texts_main_default, lv_color_hex(0x0D3055));
    lv_style_set_text_font(&style_ui_comm_list_comm_extra_texts_main_default, &lv_font_montserratMedium_16);
    lv_style_set_text_opa(&style_ui_comm_list_comm_extra_texts_main_default, 255);
    lv_style_set_radius(&style_ui_comm_list_comm_extra_texts_main_default, 3);
    lv_style_set_transform_width(&style_ui_comm_list_comm_extra_texts_main_default, 0);
    lv_style_set_bg_opa(&style_ui_comm_list_comm_extra_texts_main_default, 255);
    lv_style_set_bg_color(&style_ui_comm_list_comm_extra_texts_main_default, lv_color_hex(0xffffff));
    lv_style_set_bg_grad_dir(&style_ui_comm_list_comm_extra_texts_main_default, LV_GRAD_DIR_NONE);

    //Write codes ui_comm_label_title
    ui->ui_comm_label_title = lv_label_create(ui->ui_comm);
    lv_label_set_text(ui->ui_comm_label_title, "Communication");
    lv_label_set_long_mode(ui->ui_comm_label_title, LV_LABEL_LONG_WRAP);
    lv_obj_set_pos(ui->ui_comm_label_title, 70, 15);
    lv_obj_set_size(ui->ui_comm_label_title, 180, 30);

    //Write style for ui_comm_label_title, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_border_width(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_label_title, lv_color_hex(0x000000), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_label_title, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_label_title, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_letter_space(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_line_space(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_label_title, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_opa(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_top(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_right(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_bottom(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_pad_left(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_label_title, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes ui_comm_btn_home
    ui->ui_comm_btn_home = lv_btn_create(ui->ui_comm);
    ui->ui_comm_btn_home_label = lv_label_create(ui->ui_comm_btn_home);
    lv_label_set_text(ui->ui_comm_btn_home_label, "" LV_SYMBOL_HOME " ");
    lv_label_set_long_mode(ui->ui_comm_btn_home_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->ui_comm_btn_home_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->ui_comm_btn_home, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->ui_comm_btn_home_label, LV_PCT(100));
    lv_obj_set_pos(ui->ui_comm_btn_home, 5, 5);
    lv_obj_set_size(ui->ui_comm_btn_home, 40, 30);

    //Write style for ui_comm_btn_home, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->ui_comm_btn_home, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->ui_comm_btn_home, lv_color_hex(0xff0027), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->ui_comm_btn_home, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->ui_comm_btn_home, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->ui_comm_btn_home, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->ui_comm_btn_home, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->ui_comm_btn_home, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->ui_comm_btn_home, &lv_font_montserratMedium_16, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->ui_comm_btn_home, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->ui_comm_btn_home, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //The custom code of ui_comm.


    //Update current screen layout.
    lv_obj_update_layout(ui->ui_comm);

    //Init events for screen.
    events_init_ui_comm(ui);
}
