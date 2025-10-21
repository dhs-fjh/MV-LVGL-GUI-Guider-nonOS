# Copyright 2025 NXP
# NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
# accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
# activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
# terms, then you may not retain, install, activate or otherwise use the software.

import SDL
import utime as time
import usys as sys
import lvgl as lv
import lodepng as png
import ustruct
import fs_driver

lv.init()
SDL.init(w=320,h=240)

# Register SDL display driver.
disp_buf1 = lv.disp_draw_buf_t()
buf1_1 = bytearray(320*240*4)
disp_buf1.init(buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = disp_buf1
disp_drv.flush_cb = SDL.monitor_flush
disp_drv.hor_res = 320
disp_drv.ver_res = 240
disp_drv.register()

# Regsiter SDL mouse driver
indev_drv = lv.indev_drv_t()
indev_drv.init()
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = SDL.mouse_read
indev_drv.register()

fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'Z')

# Below: Taken from https://github.com/lvgl/lv_binding_micropython/blob/master/driver/js/imagetools.py#L22-L94

COLOR_SIZE = lv.color_t.__SIZE__
COLOR_IS_SWAPPED = hasattr(lv.color_t().ch,'green_h')

class lodepng_error(RuntimeError):
    def __init__(self, err):
        if type(err) is int:
            super().__init__(png.error_text(err))
        else:
            super().__init__(err)

# Parse PNG file header
# Taken from https://github.com/shibukawa/imagesize_py/blob/ffef30c1a4715c5acf90e8945ceb77f4a2ed2d45/imagesize.py#L63-L85

def get_png_info(decoder, src, header):
    # Only handle variable image types

    if lv.img.src_get_type(src) != lv.img.SRC.VARIABLE:
        return lv.RES.INV

    data = lv.img_dsc_t.__cast__(src).data
    if data == None:
        return lv.RES.INV

    png_header = bytes(data.__dereference__(24))

    if png_header.startswith(b'\211PNG\r\n\032\n'):
        if png_header[12:16] == b'IHDR':
            start = 16
        # Maybe this is for an older PNG version.
        else:
            start = 8
        try:
            width, height = ustruct.unpack(">LL", png_header[start:start+8])
        except ustruct.error:
            return lv.RES.INV
    else:
        return lv.RES.INV

    header.always_zero = 0
    header.w = width
    header.h = height
    header.cf = lv.img.CF.TRUE_COLOR_ALPHA

    return lv.RES.OK

def convert_rgba8888_to_bgra8888(img_view):
    for i in range(0, len(img_view), lv.color_t.__SIZE__):
        ch = lv.color_t.__cast__(img_view[i:i]).ch
        ch.red, ch.blue = ch.blue, ch.red

# Read and parse PNG file

def open_png(decoder, dsc):
    img_dsc = lv.img_dsc_t.__cast__(dsc.src)
    png_data = img_dsc.data
    png_size = img_dsc.data_size
    png_decoded = png.C_Pointer()
    png_width = png.C_Pointer()
    png_height = png.C_Pointer()
    error = png.decode32(png_decoded, png_width, png_height, png_data, png_size)
    if error:
        raise lodepng_error(error)
    img_size = png_width.int_val * png_height.int_val * 4
    img_data = png_decoded.ptr_val
    img_view = img_data.__dereference__(img_size)

    if COLOR_SIZE == 4:
        convert_rgba8888_to_bgra8888(img_view)
    else:
        raise lodepng_error("Error: Color mode not supported yet!")

    dsc.img_data = img_data
    return lv.RES.OK

# Above: Taken from https://github.com/lvgl/lv_binding_micropython/blob/master/driver/js/imagetools.py#L22-L94

decoder = lv.img.decoder_create()
decoder.info_cb = get_png_info
decoder.open_cb = open_png

def anim_x_cb(obj, v):
    obj.set_x(v)

def anim_y_cb(obj, v):
    obj.set_y(v)

def anim_width_cb(obj, v):
    obj.set_width(v)

def anim_height_cb(obj, v):
    obj.set_height(v)

def anim_img_zoom_cb(obj, v):
    obj.set_zoom(v)

def anim_img_rotate_cb(obj, v):
    obj.set_angle(v)

global_font_cache = {}
def test_font(font_family, font_size):
    global global_font_cache
    if font_family + str(font_size) in global_font_cache:
        return global_font_cache[font_family + str(font_size)]
    if font_size % 2:
        candidates = [
            (font_family, font_size),
            (font_family, font_size-font_size%2),
            (font_family, font_size+font_size%2),
            ("montserrat", font_size-font_size%2),
            ("montserrat", font_size+font_size%2),
            ("montserrat", 16)
        ]
    else:
        candidates = [
            (font_family, font_size),
            ("montserrat", font_size),
            ("montserrat", 16)
        ]
    for (family, size) in candidates:
        try:
            if eval(f'lv.font_{family}_{size}'):
                global_font_cache[font_family + str(font_size)] = eval(f'lv.font_{family}_{size}')
                if family != font_family or size != font_size:
                    print(f'WARNING: lv.font_{family}_{size} is used!')
                return eval(f'lv.font_{family}_{size}')
        except AttributeError:
            try:
                load_font = lv.font_load(f"Z:MicroPython/lv_font_{family}_{size}.fnt")
                global_font_cache[font_family + str(font_size)] = load_font
                return load_font
            except:
                if family == font_family and size == font_size:
                    print(f'WARNING: lv.font_{family}_{size} is NOT supported!')

global_image_cache = {}
def load_image(file):
    global global_image_cache
    if file in global_image_cache:
        return global_image_cache[file]
    try:
        with open(file,'rb') as f:
            data = f.read()
    except:
        print(f'Could not open {file}')
        sys.exit()

    img = lv.img_dsc_t({
        'data_size': len(data),
        'data': data
    })
    global_image_cache[file] = img
    return img

def calendar_event_handler(e,obj):
    code = e.get_code()

    if code == lv.EVENT.VALUE_CHANGED:
        source = e.get_current_target()
        date = lv.calendar_date_t()
        if source.get_pressed_date(date) == lv.RES.OK:
            source.set_highlighted_dates([date], 1)

def spinbox_increment_event_cb(e, obj):
    code = e.get_code()
    if code == lv.EVENT.SHORT_CLICKED or code == lv.EVENT.LONG_PRESSED_REPEAT:
        obj.increment()
def spinbox_decrement_event_cb(e, obj):
    code = e.get_code()
    if code == lv.EVENT.SHORT_CLICKED or code == lv.EVENT.LONG_PRESSED_REPEAT:
        obj.decrement()

def digital_clock_cb(timer, obj, current_time, show_second, use_ampm):
    hour = int(current_time[0])
    minute = int(current_time[1])
    second = int(current_time[2])
    ampm = current_time[3]
    second = second + 1
    if second == 60:
        second = 0
        minute = minute + 1
        if minute == 60:
            minute = 0
            hour = hour + 1
            if use_ampm:
                if hour == 12:
                    if ampm == 'AM':
                        ampm = 'PM'
                    elif ampm == 'PM':
                        ampm = 'AM'
                if hour > 12:
                    hour = hour % 12
    hour = hour % 24
    if use_ampm:
        if show_second:
            obj.set_text("%d:%02d:%02d %s" %(hour, minute, second, ampm))
        else:
            obj.set_text("%d:%02d %s" %(hour, minute, ampm))
    else:
        if show_second:
            obj.set_text("%d:%02d:%02d" %(hour, minute, second))
        else:
            obj.set_text("%d:%02d" %(hour, minute))
    current_time[0] = hour
    current_time[1] = minute
    current_time[2] = second
    current_time[3] = ampm

def analog_clock_cb(timer, obj):
    datetime = time.localtime()
    hour = datetime[3]
    if hour >= 12: hour = hour - 12
    obj.set_time(hour, datetime[4], datetime[5])

def datetext_event_handler(e, obj):
    code = e.get_code()
    target = e.get_target()
    if code == lv.EVENT.FOCUSED:
        if obj is None:
            bg = lv.layer_top()
            bg.add_flag(lv.obj.FLAG.CLICKABLE)
            obj = lv.calendar(bg)
            scr = target.get_screen()
            scr_height = scr.get_height()
            scr_width = scr.get_width()
            obj.set_size(int(scr_width * 0.8), int(scr_height * 0.8))
            datestring = target.get_text()
            year = int(datestring.split('/')[0])
            month = int(datestring.split('/')[1])
            day = int(datestring.split('/')[2])
            obj.set_showed_date(year, month)
            highlighted_days=[lv.calendar_date_t({'year':year, 'month':month, 'day':day})]
            obj.set_highlighted_dates(highlighted_days, 1)
            obj.align(lv.ALIGN.CENTER, 0, 0)
            lv.calendar_header_arrow(obj)
            obj.add_event_cb(lambda e: datetext_calendar_event_handler(e, target), lv.EVENT.ALL, None)
            scr.update_layout()

def datetext_calendar_event_handler(e, obj):
    code = e.get_code()
    target = e.get_current_target()
    if code == lv.EVENT.VALUE_CHANGED:
        date = lv.calendar_date_t()
        if target.get_pressed_date(date) == lv.RES.OK:
            obj.set_text(f"{date.year}/{date.month}/{date.day}")
            bg = lv.layer_top()
            bg.clear_flag(lv.obj.FLAG.CLICKABLE)
            bg.set_style_bg_opa(lv.OPA.TRANSP, 0)
            target.delete()

def ta_event_cb(e,kb):
    code = e.get_code()
    ta = e.get_target()
    if code == lv.EVENT.FOCUSED:
        kb.set_textarea(ta)
        kb.move_foreground()
        kb.clear_flag(lv.obj.FLAG.HIDDEN)

    if code == lv.EVENT.DEFOCUSED:
        kb.set_textarea(None)
        kb.move_background()
        kb.add_flag(lv.obj.FLAG.HIDDEN)

# Create ui_main
ui_main = lv.obj()
g_kb_ui_main = lv.keyboard(ui_main)
g_kb_ui_main.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_main), lv.EVENT.ALL, None)
g_kb_ui_main.add_flag(lv.obj.FLAG.HIDDEN)
g_kb_ui_main.set_style_text_font(test_font("SourceHanSerifSC_Regular", 18), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main.set_size(320, 240)
ui_main.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_main, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_main.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_main_btn_pwr
ui_main_btn_pwr = lv.btn(ui_main)
ui_main_btn_pwr_label = lv.label(ui_main_btn_pwr)
ui_main_btn_pwr_label.set_text(""+lv.SYMBOL.POWER+" ")
ui_main_btn_pwr_label.set_long_mode(lv.label.LONG.WRAP)
ui_main_btn_pwr_label.set_width(lv.pct(100))
ui_main_btn_pwr_label.align(lv.ALIGN.CENTER, 0, 0)
ui_main_btn_pwr.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_main_btn_pwr.set_pos(260, 180)
ui_main_btn_pwr.set_size(40, 40)
# Set style for ui_main_btn_pwr, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_main_btn_pwr.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_pwr.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_pwr.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_pwr.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_pwr.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_pwr.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_pwr.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_pwr.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_pwr.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_pwr.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_main_btn_io
ui_main_btn_io = lv.btn(ui_main)
ui_main_btn_io_label = lv.label(ui_main_btn_io)
ui_main_btn_io_label.set_text(""+lv.SYMBOL.GPS+" ")
ui_main_btn_io_label.set_long_mode(lv.label.LONG.WRAP)
ui_main_btn_io_label.set_width(lv.pct(100))
ui_main_btn_io_label.align(lv.ALIGN.CENTER, 0, 0)
ui_main_btn_io.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_main_btn_io.set_pos(260, 20)
ui_main_btn_io.set_size(40, 40)
# Set style for ui_main_btn_io, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_main_btn_io.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_io.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_io.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_io.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_io.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_io.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_io.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_io.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_io.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_io.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_main_btn_comm
ui_main_btn_comm = lv.btn(ui_main)
ui_main_btn_comm_label = lv.label(ui_main_btn_comm)
ui_main_btn_comm_label.set_text(""+lv.SYMBOL.USB+" ")
ui_main_btn_comm_label.set_long_mode(lv.label.LONG.WRAP)
ui_main_btn_comm_label.set_width(lv.pct(100))
ui_main_btn_comm_label.align(lv.ALIGN.CENTER, 0, 0)
ui_main_btn_comm.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_main_btn_comm.set_pos(200, 20)
ui_main_btn_comm.set_size(40, 40)
# Set style for ui_main_btn_comm, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_main_btn_comm.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_comm.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_comm.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_comm.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_comm.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_comm.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_comm.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_comm.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_comm.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_comm.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_main_btn_led
ui_main_btn_led = lv.btn(ui_main)
ui_main_btn_led_label = lv.label(ui_main_btn_led)
ui_main_btn_led_label.set_text(""+lv.SYMBOL.CHARGE+" ")
ui_main_btn_led_label.set_long_mode(lv.label.LONG.WRAP)
ui_main_btn_led_label.set_width(lv.pct(100))
ui_main_btn_led_label.align(lv.ALIGN.CENTER, 0, 0)
ui_main_btn_led.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_main_btn_led.set_pos(140, 20)
ui_main_btn_led.set_size(40, 40)
# Set style for ui_main_btn_led, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_main_btn_led.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_led.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_led.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_led.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_led.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_led.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_led.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_led.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_led.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_led.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_main_btn_storage
ui_main_btn_storage = lv.btn(ui_main)
ui_main_btn_storage_label = lv.label(ui_main_btn_storage)
ui_main_btn_storage_label.set_text(""+lv.SYMBOL.DIRECTORY+" ")
ui_main_btn_storage_label.set_long_mode(lv.label.LONG.WRAP)
ui_main_btn_storage_label.set_width(lv.pct(100))
ui_main_btn_storage_label.align(lv.ALIGN.CENTER, 0, 0)
ui_main_btn_storage.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_main_btn_storage.set_pos(80, 20)
ui_main_btn_storage.set_size(40, 40)
# Set style for ui_main_btn_storage, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_main_btn_storage.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_storage.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_storage.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_storage.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_storage.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_storage.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_storage.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_storage.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_storage.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_storage.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_main_btn_settings
ui_main_btn_settings = lv.btn(ui_main)
ui_main_btn_settings_label = lv.label(ui_main_btn_settings)
ui_main_btn_settings_label.set_text(""+lv.SYMBOL.SETTINGS+" ")
ui_main_btn_settings_label.set_long_mode(lv.label.LONG.WRAP)
ui_main_btn_settings_label.set_width(lv.pct(100))
ui_main_btn_settings_label.align(lv.ALIGN.CENTER, 0, 0)
ui_main_btn_settings.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_main_btn_settings.set_pos(20, 20)
ui_main_btn_settings.set_size(40, 40)
# Set style for ui_main_btn_settings, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_main_btn_settings.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_settings.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_settings.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_settings.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_settings.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_settings.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_settings.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_settings.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_settings.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_main_btn_settings.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

ui_main.update_layout()
# Create ui_settings
ui_settings = lv.obj()
g_kb_ui_settings = lv.keyboard(ui_settings)
g_kb_ui_settings.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_settings), lv.EVENT.ALL, None)
g_kb_ui_settings.add_flag(lv.obj.FLAG.HIDDEN)
g_kb_ui_settings.set_style_text_font(test_font("SourceHanSerifSC_Regular", 18), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings.set_size(320, 240)
ui_settings.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_settings, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_settings.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_settings_label_title
ui_settings_label_title = lv.label(ui_settings)
ui_settings_label_title.set_text("Settings")
ui_settings_label_title.set_long_mode(lv.label.LONG.WRAP)
ui_settings_label_title.set_width(lv.pct(100))
ui_settings_label_title.set_pos(69, 14)
ui_settings_label_title.set_size(180, 30)
# Set style for ui_settings_label_title, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_settings_label_title.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_label_title.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_settings_btn_home
ui_settings_btn_home = lv.btn(ui_settings)
ui_settings_btn_home_label = lv.label(ui_settings_btn_home)
ui_settings_btn_home_label.set_text(""+lv.SYMBOL.HOME+" ")
ui_settings_btn_home_label.set_long_mode(lv.label.LONG.WRAP)
ui_settings_btn_home_label.set_width(lv.pct(100))
ui_settings_btn_home_label.align(lv.ALIGN.CENTER, 0, 0)
ui_settings_btn_home.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_settings_btn_home.set_pos(5, 5)
ui_settings_btn_home.set_size(40, 30)
# Set style for ui_settings_btn_home, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_settings_btn_home.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_btn_home.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_btn_home.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_btn_home.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_btn_home.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_btn_home.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_btn_home.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_btn_home.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_btn_home.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_settings_btn_home.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

ui_settings.update_layout()
# Create ui_storage
ui_storage = lv.obj()
g_kb_ui_storage = lv.keyboard(ui_storage)
g_kb_ui_storage.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_storage), lv.EVENT.ALL, None)
g_kb_ui_storage.add_flag(lv.obj.FLAG.HIDDEN)
g_kb_ui_storage.set_style_text_font(test_font("SourceHanSerifSC_Regular", 18), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage.set_size(320, 240)
ui_storage.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_storage, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_storage.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_storage_list_files
ui_storage_list_files = lv.list(ui_storage)
ui_storage_list_files_item0 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_0")
ui_storage_list_files_item1 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_1")
ui_storage_list_files_item2 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_2")
ui_storage_list_files_item3 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_3")
ui_storage_list_files_item4 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_4")
ui_storage_list_files_item5 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_5")
ui_storage_list_files_item6 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_6")
ui_storage_list_files_item7 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_7")
ui_storage_list_files_item8 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_8")
ui_storage_list_files_item9 = ui_storage_list_files.add_btn(lv.SYMBOL.FILE, "file_9")
ui_storage_list_files.set_pos(5, 40)
ui_storage_list_files.set_size(310, 195)
ui_storage_list_files.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_storage_list_files, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_storage_list_files.set_style_pad_top(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_pad_left(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_pad_right(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_pad_bottom(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_storage_list_files, Part: lv.PART.MAIN, State: lv.STATE.FOCUSED.
ui_storage_list_files.set_style_pad_top(5, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_pad_left(5, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_pad_right(5, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_pad_bottom(5, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_border_width(1, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_radius(3, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_storage_list_files.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.FOCUSED)
# Set style for ui_storage_list_files, Part: lv.PART.MAIN, State: lv.STATE.DISABLED.
ui_storage_list_files.set_style_pad_top(5, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_pad_left(5, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_pad_right(5, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_pad_bottom(5, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_radius(3, lv.PART.MAIN|lv.STATE.DISABLED)
ui_storage_list_files.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DISABLED)
# Set style for ui_storage_list_files, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
ui_storage_list_files.set_style_radius(3, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_bg_opa(255, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_storage_list_files.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
# Set style for ui_storage_list_files, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_storage_list_files_extra_btns_main_default = lv.style_t()
style_ui_storage_list_files_extra_btns_main_default.init()
style_ui_storage_list_files_extra_btns_main_default.set_pad_top(5)
style_ui_storage_list_files_extra_btns_main_default.set_pad_left(5)
style_ui_storage_list_files_extra_btns_main_default.set_pad_right(5)
style_ui_storage_list_files_extra_btns_main_default.set_pad_bottom(5)
style_ui_storage_list_files_extra_btns_main_default.set_border_width(0)
style_ui_storage_list_files_extra_btns_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_storage_list_files_extra_btns_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_storage_list_files_extra_btns_main_default.set_text_opa(255)
style_ui_storage_list_files_extra_btns_main_default.set_radius(3)
style_ui_storage_list_files_extra_btns_main_default.set_bg_opa(255)
style_ui_storage_list_files_extra_btns_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_storage_list_files_extra_btns_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_storage_list_files_item9.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files_item8.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files_item7.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files_item6.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files_item5.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files_item4.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files_item3.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files_item2.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files_item1.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_list_files_item0.add_style(style_ui_storage_list_files_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_storage_list_files, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_storage_list_files_extra_texts_main_default = lv.style_t()
style_ui_storage_list_files_extra_texts_main_default.init()
style_ui_storage_list_files_extra_texts_main_default.set_pad_top(5)
style_ui_storage_list_files_extra_texts_main_default.set_pad_left(5)
style_ui_storage_list_files_extra_texts_main_default.set_pad_right(5)
style_ui_storage_list_files_extra_texts_main_default.set_pad_bottom(5)
style_ui_storage_list_files_extra_texts_main_default.set_border_width(0)
style_ui_storage_list_files_extra_texts_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_storage_list_files_extra_texts_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_storage_list_files_extra_texts_main_default.set_text_opa(255)
style_ui_storage_list_files_extra_texts_main_default.set_radius(3)
style_ui_storage_list_files_extra_texts_main_default.set_transform_width(0)
style_ui_storage_list_files_extra_texts_main_default.set_bg_opa(255)
style_ui_storage_list_files_extra_texts_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_storage_list_files_extra_texts_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)

# Create ui_storage_btn_next
ui_storage_btn_next = lv.btn(ui_storage)
ui_storage_btn_next_label = lv.label(ui_storage_btn_next)
ui_storage_btn_next_label.set_text(""+lv.SYMBOL.RIGHT+" ")
ui_storage_btn_next_label.set_long_mode(lv.label.LONG.WRAP)
ui_storage_btn_next_label.set_width(lv.pct(100))
ui_storage_btn_next_label.align(lv.ALIGN.CENTER, 0, 0)
ui_storage_btn_next.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_storage_btn_next.set_pos(275, 5)
ui_storage_btn_next.set_size(40, 30)
# Set style for ui_storage_btn_next, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_storage_btn_next.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_next.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_next.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_next.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_next.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_next.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_next.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_next.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_next.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_next.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_storage_btn_prev
ui_storage_btn_prev = lv.btn(ui_storage)
ui_storage_btn_prev_label = lv.label(ui_storage_btn_prev)
ui_storage_btn_prev_label.set_text(""+lv.SYMBOL.LEFT+" ")
ui_storage_btn_prev_label.set_long_mode(lv.label.LONG.WRAP)
ui_storage_btn_prev_label.set_width(lv.pct(100))
ui_storage_btn_prev_label.align(lv.ALIGN.CENTER, 0, 0)
ui_storage_btn_prev.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_storage_btn_prev.set_pos(230, 5)
ui_storage_btn_prev.set_size(40, 30)
# Set style for ui_storage_btn_prev, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_storage_btn_prev.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_prev.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_prev.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_prev.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_prev.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_prev.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_prev.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_prev.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_prev.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_prev.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_storage_label_title
ui_storage_label_title = lv.label(ui_storage)
ui_storage_label_title.set_text("Storage")
ui_storage_label_title.set_long_mode(lv.label.LONG.WRAP)
ui_storage_label_title.set_width(lv.pct(100))
ui_storage_label_title.set_pos(70, 15)
ui_storage_label_title.set_size(180, 30)
# Set style for ui_storage_label_title, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_storage_label_title.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_title.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_storage_label_page
ui_storage_label_page = lv.label(ui_storage)
ui_storage_label_page.set_text("1/1")
ui_storage_label_page.set_long_mode(lv.label.LONG.WRAP)
ui_storage_label_page.set_width(lv.pct(100))
ui_storage_label_page.set_pos(60, 15)
ui_storage_label_page.set_size(60, 30)
# Set style for ui_storage_label_page, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_storage_label_page.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_label_page.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_storage_btn_home
ui_storage_btn_home = lv.btn(ui_storage)
ui_storage_btn_home_label = lv.label(ui_storage_btn_home)
ui_storage_btn_home_label.set_text(""+lv.SYMBOL.HOME+" ")
ui_storage_btn_home_label.set_long_mode(lv.label.LONG.WRAP)
ui_storage_btn_home_label.set_width(lv.pct(100))
ui_storage_btn_home_label.align(lv.ALIGN.CENTER, 0, 0)
ui_storage_btn_home.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_storage_btn_home.set_pos(5, 5)
ui_storage_btn_home.set_size(40, 30)
# Set style for ui_storage_btn_home, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_storage_btn_home.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_home.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_home.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_home.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_home.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_home.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_home.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_home.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_home.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_storage_btn_home.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

ui_storage.update_layout()
# Create ui_comm
ui_comm = lv.obj()
g_kb_ui_comm = lv.keyboard(ui_comm)
g_kb_ui_comm.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm), lv.EVENT.ALL, None)
g_kb_ui_comm.add_flag(lv.obj.FLAG.HIDDEN)
g_kb_ui_comm.set_style_text_font(test_font("SourceHanSerifSC_Regular", 18), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm.set_size(320, 240)
ui_comm.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_comm, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_list_comm
ui_comm_list_comm = lv.list(ui_comm)
ui_comm_list_comm_item0 = ui_comm_list_comm.add_btn(lv.SYMBOL.USB, "CAN")
ui_comm_list_comm_item1 = ui_comm_list_comm.add_btn(lv.SYMBOL.USB, "UART")
ui_comm_list_comm_item2 = ui_comm_list_comm.add_btn(lv.SYMBOL.USB, "RC")
ui_comm_list_comm.set_pos(5, 40)
ui_comm_list_comm.set_size(310, 195)
ui_comm_list_comm.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_comm_list_comm, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_list_comm.set_style_pad_top(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_pad_left(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_pad_right(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_pad_bottom(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_list_comm, Part: lv.PART.MAIN, State: lv.STATE.FOCUSED.
ui_comm_list_comm.set_style_pad_top(5, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_pad_left(5, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_pad_right(5, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_pad_bottom(5, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_border_width(1, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_radius(3, lv.PART.MAIN|lv.STATE.FOCUSED)
ui_comm_list_comm.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.FOCUSED)
# Set style for ui_comm_list_comm, Part: lv.PART.MAIN, State: lv.STATE.DISABLED.
ui_comm_list_comm.set_style_pad_top(5, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_pad_left(5, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_pad_right(5, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_pad_bottom(5, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_radius(3, lv.PART.MAIN|lv.STATE.DISABLED)
ui_comm_list_comm.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DISABLED)
# Set style for ui_comm_list_comm, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
ui_comm_list_comm.set_style_radius(3, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_bg_opa(255, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_list_comm.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
# Set style for ui_comm_list_comm, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_list_comm_extra_btns_main_default = lv.style_t()
style_ui_comm_list_comm_extra_btns_main_default.init()
style_ui_comm_list_comm_extra_btns_main_default.set_pad_top(5)
style_ui_comm_list_comm_extra_btns_main_default.set_pad_left(5)
style_ui_comm_list_comm_extra_btns_main_default.set_pad_right(5)
style_ui_comm_list_comm_extra_btns_main_default.set_pad_bottom(5)
style_ui_comm_list_comm_extra_btns_main_default.set_border_width(0)
style_ui_comm_list_comm_extra_btns_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_list_comm_extra_btns_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_list_comm_extra_btns_main_default.set_text_opa(255)
style_ui_comm_list_comm_extra_btns_main_default.set_radius(3)
style_ui_comm_list_comm_extra_btns_main_default.set_bg_opa(255)
style_ui_comm_list_comm_extra_btns_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_list_comm_extra_btns_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_list_comm_item2.add_style(style_ui_comm_list_comm_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm_item1.add_style(style_ui_comm_list_comm_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_list_comm_item0.add_style(style_ui_comm_list_comm_extra_btns_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_list_comm, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_list_comm_extra_texts_main_default = lv.style_t()
style_ui_comm_list_comm_extra_texts_main_default.init()
style_ui_comm_list_comm_extra_texts_main_default.set_pad_top(5)
style_ui_comm_list_comm_extra_texts_main_default.set_pad_left(5)
style_ui_comm_list_comm_extra_texts_main_default.set_pad_right(5)
style_ui_comm_list_comm_extra_texts_main_default.set_pad_bottom(5)
style_ui_comm_list_comm_extra_texts_main_default.set_border_width(0)
style_ui_comm_list_comm_extra_texts_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_list_comm_extra_texts_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_list_comm_extra_texts_main_default.set_text_opa(255)
style_ui_comm_list_comm_extra_texts_main_default.set_radius(3)
style_ui_comm_list_comm_extra_texts_main_default.set_transform_width(0)
style_ui_comm_list_comm_extra_texts_main_default.set_bg_opa(255)
style_ui_comm_list_comm_extra_texts_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_list_comm_extra_texts_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)

# Create ui_comm_label_title
ui_comm_label_title = lv.label(ui_comm)
ui_comm_label_title.set_text("Communication")
ui_comm_label_title.set_long_mode(lv.label.LONG.WRAP)
ui_comm_label_title.set_width(lv.pct(100))
ui_comm_label_title.set_pos(70, 15)
ui_comm_label_title.set_size(180, 30)
# Set style for ui_comm_label_title, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_label_title.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_label_title.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_btn_home
ui_comm_btn_home = lv.btn(ui_comm)
ui_comm_btn_home_label = lv.label(ui_comm_btn_home)
ui_comm_btn_home_label.set_text(""+lv.SYMBOL.HOME+" ")
ui_comm_btn_home_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_btn_home_label.set_width(lv.pct(100))
ui_comm_btn_home_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_btn_home.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_btn_home.set_pos(5, 5)
ui_comm_btn_home.set_size(40, 30)
# Set style for ui_comm_btn_home, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_btn_home.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_btn_home.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_btn_home.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_btn_home.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_btn_home.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_btn_home.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_btn_home.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_btn_home.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_btn_home.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_btn_home.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

ui_comm.update_layout()
# Create ui_comm_can
ui_comm_can = lv.obj()
g_kb_ui_comm_can = lv.keyboard(ui_comm_can)
g_kb_ui_comm_can.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm_can), lv.EVENT.ALL, None)
g_kb_ui_comm_can.add_flag(lv.obj.FLAG.HIDDEN)
g_kb_ui_comm_can.set_style_text_font(test_font("SourceHanSerifSC_Regular", 18), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can.set_size(320, 240)
ui_comm_can.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_comm_can, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_can_ta_rx_msg
ui_comm_can_ta_rx_msg = lv.textarea(ui_comm_can)
ui_comm_can_ta_rx_msg.set_text("Hello World")
ui_comm_can_ta_rx_msg.set_placeholder_text("")
ui_comm_can_ta_rx_msg.set_password_bullet("*")
ui_comm_can_ta_rx_msg.set_password_mode(False)
ui_comm_can_ta_rx_msg.set_one_line(False)
ui_comm_can_ta_rx_msg.set_accepted_chars("")
ui_comm_can_ta_rx_msg.set_max_length(512)
ui_comm_can_ta_rx_msg.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm_can), lv.EVENT.ALL, None)
ui_comm_can_ta_rx_msg.set_pos(5, 110)
ui_comm_can_ta_rx_msg.set_size(310, 125)
# Set style for ui_comm_can_ta_rx_msg, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_ta_rx_msg.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_text_font(test_font("montserratMedium", 12), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_text_letter_space(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_border_width(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_border_color(lv.color_hex(0xe6e6e6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_pad_top(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_pad_right(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_pad_left(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_radius(4, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_can_ta_rx_msg, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
ui_comm_can_ta_rx_msg.set_style_bg_opa(255, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_can_ta_rx_msg.set_style_radius(0, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_can_ddlist_ch
ui_comm_can_ddlist_ch = lv.dropdown(ui_comm_can)
ui_comm_can_ddlist_ch.set_options("1\n2")
ui_comm_can_ddlist_ch.set_pos(275, 75)
ui_comm_can_ddlist_ch.set_size(40, 30)
# Set style for ui_comm_can_ddlist_ch, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_ddlist_ch.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ch.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_can_ddlist_ch, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_can_ddlist_ch_extra_list_selected_checked = lv.style_t()
style_ui_comm_can_ddlist_ch_extra_list_selected_checked.init()
style_ui_comm_can_ddlist_ch_extra_list_selected_checked.set_border_width(1)
style_ui_comm_can_ddlist_ch_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_can_ddlist_ch_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_can_ddlist_ch_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_can_ddlist_ch_extra_list_selected_checked.set_radius(3)
style_ui_comm_can_ddlist_ch_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_can_ddlist_ch_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_can_ddlist_ch_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_ch.get_list().add_style(style_ui_comm_can_ddlist_ch_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_can_ddlist_ch, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_can_ddlist_ch_extra_list_main_default = lv.style_t()
style_ui_comm_can_ddlist_ch_extra_list_main_default.init()
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_max_height(90)
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_text_opa(255)
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_border_width(1)
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_border_opa(255)
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_radius(3)
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_bg_opa(255)
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_can_ddlist_ch_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_ch.get_list().add_style(style_ui_comm_can_ddlist_ch_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_can_ddlist_ch, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_can_ddlist_ch_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_can_ddlist_ch_extra_list_scrollbar_default.init()
style_ui_comm_can_ddlist_ch_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_can_ddlist_ch_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_can_ddlist_ch_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_can_ddlist_ch_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_ch.get_list().add_style(style_ui_comm_can_ddlist_ch_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_can_ddlist_rate
ui_comm_can_ddlist_rate = lv.dropdown(ui_comm_can)
ui_comm_can_ddlist_rate.set_options("1M\n800K\n500K\n400K\n250K\n200K\n125K\n100K\n50K\n20K\n10K\n5K")
ui_comm_can_ddlist_rate.set_pos(200, 75)
ui_comm_can_ddlist_rate.set_size(70, 30)
# Set style for ui_comm_can_ddlist_rate, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_ddlist_rate.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rate.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_can_ddlist_rate, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_can_ddlist_rate_extra_list_selected_checked = lv.style_t()
style_ui_comm_can_ddlist_rate_extra_list_selected_checked.init()
style_ui_comm_can_ddlist_rate_extra_list_selected_checked.set_border_width(1)
style_ui_comm_can_ddlist_rate_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_can_ddlist_rate_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_can_ddlist_rate_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_can_ddlist_rate_extra_list_selected_checked.set_radius(3)
style_ui_comm_can_ddlist_rate_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_can_ddlist_rate_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_can_ddlist_rate_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_rate.get_list().add_style(style_ui_comm_can_ddlist_rate_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_can_ddlist_rate, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_can_ddlist_rate_extra_list_main_default = lv.style_t()
style_ui_comm_can_ddlist_rate_extra_list_main_default.init()
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_max_height(90)
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_text_opa(255)
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_border_width(1)
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_border_opa(255)
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_radius(3)
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_bg_opa(255)
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_can_ddlist_rate_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_rate.get_list().add_style(style_ui_comm_can_ddlist_rate_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_can_ddlist_rate, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_can_ddlist_rate_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_can_ddlist_rate_extra_list_scrollbar_default.init()
style_ui_comm_can_ddlist_rate_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_can_ddlist_rate_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_can_ddlist_rate_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_can_ddlist_rate_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_rate.get_list().add_style(style_ui_comm_can_ddlist_rate_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_can_ddlist_rtr
ui_comm_can_ddlist_rtr = lv.dropdown(ui_comm_can)
ui_comm_can_ddlist_rtr.set_options("D\nR")
ui_comm_can_ddlist_rtr.set_pos(153, 75)
ui_comm_can_ddlist_rtr.set_size(42, 30)
# Set style for ui_comm_can_ddlist_rtr, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_ddlist_rtr.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_rtr.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_can_ddlist_rtr, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked = lv.style_t()
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked.init()
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked.set_border_width(1)
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked.set_radius(3)
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_can_ddlist_rtr_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_rtr.get_list().add_style(style_ui_comm_can_ddlist_rtr_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_can_ddlist_rtr, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_can_ddlist_rtr_extra_list_main_default = lv.style_t()
style_ui_comm_can_ddlist_rtr_extra_list_main_default.init()
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_max_height(90)
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_text_opa(255)
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_border_width(1)
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_border_opa(255)
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_radius(3)
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_bg_opa(255)
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_can_ddlist_rtr_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_rtr.get_list().add_style(style_ui_comm_can_ddlist_rtr_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_can_ddlist_rtr, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_can_ddlist_rtr_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_can_ddlist_rtr_extra_list_scrollbar_default.init()
style_ui_comm_can_ddlist_rtr_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_can_ddlist_rtr_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_can_ddlist_rtr_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_can_ddlist_rtr_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_rtr.get_list().add_style(style_ui_comm_can_ddlist_rtr_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_can_ddlist_ide
ui_comm_can_ddlist_ide = lv.dropdown(ui_comm_can)
ui_comm_can_ddlist_ide.set_options("S\nE")
ui_comm_can_ddlist_ide.set_pos(106, 75)
ui_comm_can_ddlist_ide.set_size(42, 30)
# Set style for ui_comm_can_ddlist_ide, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_ddlist_ide.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ddlist_ide.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_can_ddlist_ide, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_can_ddlist_ide_extra_list_selected_checked = lv.style_t()
style_ui_comm_can_ddlist_ide_extra_list_selected_checked.init()
style_ui_comm_can_ddlist_ide_extra_list_selected_checked.set_border_width(1)
style_ui_comm_can_ddlist_ide_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_can_ddlist_ide_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_can_ddlist_ide_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_can_ddlist_ide_extra_list_selected_checked.set_radius(3)
style_ui_comm_can_ddlist_ide_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_can_ddlist_ide_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_can_ddlist_ide_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_ide.get_list().add_style(style_ui_comm_can_ddlist_ide_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_can_ddlist_ide, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_can_ddlist_ide_extra_list_main_default = lv.style_t()
style_ui_comm_can_ddlist_ide_extra_list_main_default.init()
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_max_height(90)
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_text_opa(255)
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_border_width(1)
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_border_opa(255)
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_radius(3)
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_bg_opa(255)
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_can_ddlist_ide_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_ide.get_list().add_style(style_ui_comm_can_ddlist_ide_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_can_ddlist_ide, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_can_ddlist_ide_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_can_ddlist_ide_extra_list_scrollbar_default.init()
style_ui_comm_can_ddlist_ide_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_can_ddlist_ide_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_can_ddlist_ide_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_can_ddlist_ide_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_can_ddlist_ide.get_list().add_style(style_ui_comm_can_ddlist_ide_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_can_ta_can_id
ui_comm_can_ta_can_id = lv.textarea(ui_comm_can)
ui_comm_can_ta_can_id.set_text("AAA")
ui_comm_can_ta_can_id.set_placeholder_text("")
ui_comm_can_ta_can_id.set_password_bullet("*")
ui_comm_can_ta_can_id.set_password_mode(False)
ui_comm_can_ta_can_id.set_one_line(False)
ui_comm_can_ta_can_id.set_accepted_chars("")
ui_comm_can_ta_can_id.set_max_length(32)
ui_comm_can_ta_can_id.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm_can), lv.EVENT.ALL, None)
ui_comm_can_ta_can_id.set_pos(35, 75)
ui_comm_can_ta_can_id.set_size(66, 30)
# Set style for ui_comm_can_ta_can_id, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_ta_can_id.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_text_letter_space(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_border_width(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_border_color(lv.color_hex(0xe6e6e6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_pad_top(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_pad_right(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_pad_left(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_radius(4, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_can_ta_can_id, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
ui_comm_can_ta_can_id.set_style_bg_opa(255, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_can_ta_can_id.set_style_radius(0, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_can_label_can_id
ui_comm_can_label_can_id = lv.label(ui_comm_can)
ui_comm_can_label_can_id.set_text("ID:")
ui_comm_can_label_can_id.set_long_mode(lv.label.LONG.WRAP)
ui_comm_can_label_can_id.set_width(lv.pct(100))
ui_comm_can_label_can_id.set_pos(3, 82)
ui_comm_can_label_can_id.set_size(30, 16)
# Set style for ui_comm_can_label_can_id, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_label_can_id.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_can_id.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_can_ta_tx_buf
ui_comm_can_ta_tx_buf = lv.textarea(ui_comm_can)
ui_comm_can_ta_tx_buf.set_text("AA BB CC DD EE FF AA BB CC")
ui_comm_can_ta_tx_buf.set_placeholder_text("")
ui_comm_can_ta_tx_buf.set_password_bullet("*")
ui_comm_can_ta_tx_buf.set_password_mode(False)
ui_comm_can_ta_tx_buf.set_one_line(True)
ui_comm_can_ta_tx_buf.set_accepted_chars("")
ui_comm_can_ta_tx_buf.set_max_length(32)
ui_comm_can_ta_tx_buf.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm_can), lv.EVENT.ALL, None)
ui_comm_can_ta_tx_buf.set_pos(5, 40)
ui_comm_can_ta_tx_buf.set_size(310, 30)
# Set style for ui_comm_can_ta_tx_buf, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_ta_tx_buf.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_text_letter_space(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_border_width(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_border_color(lv.color_hex(0xe6e6e6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_pad_top(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_pad_right(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_pad_left(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_radius(4, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_can_ta_tx_buf, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
ui_comm_can_ta_tx_buf.set_style_bg_opa(255, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_can_ta_tx_buf.set_style_radius(0, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_can_btn_tx
ui_comm_can_btn_tx = lv.btn(ui_comm_can)
ui_comm_can_btn_tx_label = lv.label(ui_comm_can_btn_tx)
ui_comm_can_btn_tx_label.set_text(""+lv.SYMBOL.UPLOAD+"")
ui_comm_can_btn_tx_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_can_btn_tx_label.set_width(lv.pct(100))
ui_comm_can_btn_tx_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_can_btn_tx.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_pos(275, 5)
ui_comm_can_btn_tx.set_size(40, 30)
# Set style for ui_comm_can_btn_tx, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_btn_tx.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_can_btn_tx_clean
ui_comm_can_btn_tx_clean = lv.btn(ui_comm_can)
ui_comm_can_btn_tx_clean_label = lv.label(ui_comm_can_btn_tx_clean)
ui_comm_can_btn_tx_clean_label.set_text(""+lv.SYMBOL.TRASH+"")
ui_comm_can_btn_tx_clean_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_can_btn_tx_clean_label.set_width(lv.pct(100))
ui_comm_can_btn_tx_clean_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_can_btn_tx_clean.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_pos(230, 5)
ui_comm_can_btn_tx_clean.set_size(40, 30)
# Set style for ui_comm_can_btn_tx_clean, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_btn_tx_clean.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_tx_clean.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_can_label_tittle
ui_comm_can_label_tittle = lv.label(ui_comm_can)
ui_comm_can_label_tittle.set_text("CAN Data View")
ui_comm_can_label_tittle.set_long_mode(lv.label.LONG.WRAP)
ui_comm_can_label_tittle.set_width(lv.pct(100))
ui_comm_can_label_tittle.set_pos(70, 15)
ui_comm_can_label_tittle.set_size(180, 30)
# Set style for ui_comm_can_label_tittle, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_label_tittle.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_label_tittle.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_can_btn_rx_clean
ui_comm_can_btn_rx_clean = lv.btn(ui_comm_can)
ui_comm_can_btn_rx_clean_label = lv.label(ui_comm_can_btn_rx_clean)
ui_comm_can_btn_rx_clean_label.set_text(""+lv.SYMBOL.TRASH+"")
ui_comm_can_btn_rx_clean_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_can_btn_rx_clean_label.set_width(lv.pct(100))
ui_comm_can_btn_rx_clean_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_can_btn_rx_clean.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_pos(50, 5)
ui_comm_can_btn_rx_clean.set_size(40, 30)
# Set style for ui_comm_can_btn_rx_clean, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_btn_rx_clean.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_rx_clean.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_can_btn_back
ui_comm_can_btn_back = lv.btn(ui_comm_can)
ui_comm_can_btn_back_label = lv.label(ui_comm_can_btn_back)
ui_comm_can_btn_back_label.set_text(""+lv.SYMBOL.LEFT+" ")
ui_comm_can_btn_back_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_can_btn_back_label.set_width(lv.pct(100))
ui_comm_can_btn_back_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_can_btn_back.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_pos(5, 5)
ui_comm_can_btn_back.set_size(40, 30)
# Set style for ui_comm_can_btn_back, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_can_btn_back.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_can_btn_back.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

ui_comm_can.update_layout()
# Create ui_comm_uart
ui_comm_uart = lv.obj()
g_kb_ui_comm_uart = lv.keyboard(ui_comm_uart)
g_kb_ui_comm_uart.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm_uart), lv.EVENT.ALL, None)
g_kb_ui_comm_uart.add_flag(lv.obj.FLAG.HIDDEN)
g_kb_ui_comm_uart.set_style_text_font(test_font("SourceHanSerifSC_Regular", 18), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart.set_size(320, 240)
ui_comm_uart.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_comm_uart, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_uart_ta_rx_msg
ui_comm_uart_ta_rx_msg = lv.textarea(ui_comm_uart)
ui_comm_uart_ta_rx_msg.set_text("RX BUF")
ui_comm_uart_ta_rx_msg.set_placeholder_text("")
ui_comm_uart_ta_rx_msg.set_password_bullet("*")
ui_comm_uart_ta_rx_msg.set_password_mode(False)
ui_comm_uart_ta_rx_msg.set_one_line(False)
ui_comm_uart_ta_rx_msg.set_accepted_chars("")
ui_comm_uart_ta_rx_msg.set_max_length(32)
ui_comm_uart_ta_rx_msg.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm_uart), lv.EVENT.ALL, None)
ui_comm_uart_ta_rx_msg.set_pos(5, 145)
ui_comm_uart_ta_rx_msg.set_size(310, 90)
# Set style for ui_comm_uart_ta_rx_msg, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_ta_rx_msg.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_text_font(test_font("montserratMedium", 12), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_text_letter_space(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_border_width(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_border_color(lv.color_hex(0xe6e6e6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_pad_top(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_pad_right(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_pad_left(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_radius(4, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_ta_rx_msg, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
ui_comm_uart_ta_rx_msg.set_style_bg_opa(255, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_uart_ta_rx_msg.set_style_radius(0, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_uart_ddlist_rx_fmt
ui_comm_uart_ddlist_rx_fmt = lv.dropdown(ui_comm_uart)
ui_comm_uart_ddlist_rx_fmt.set_options("H\nD")
ui_comm_uart_ddlist_rx_fmt.set_pos(265, 110)
ui_comm_uart_ddlist_rx_fmt.set_size(50, 30)
# Set style for ui_comm_uart_ddlist_rx_fmt, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_ddlist_rx_fmt.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_rx_fmt.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_ddlist_rx_fmt, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked = lv.style_t()
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked.init()
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked.set_border_width(1)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked.set_radius(3)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_rx_fmt.get_list().add_style(style_ui_comm_uart_ddlist_rx_fmt_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_uart_ddlist_rx_fmt, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default = lv.style_t()
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.init()
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_max_height(90)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_text_opa(255)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_border_width(1)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_border_opa(255)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_radius(3)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_rx_fmt.get_list().add_style(style_ui_comm_uart_ddlist_rx_fmt_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_uart_ddlist_rx_fmt, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default.init()
style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_rx_fmt.get_list().add_style(style_ui_comm_uart_ddlist_rx_fmt_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_uart_ddlist_check
ui_comm_uart_ddlist_check = lv.dropdown(ui_comm_uart)
ui_comm_uart_ddlist_check.set_options("NONE\nODD\nEVEN")
ui_comm_uart_ddlist_check.set_pos(170, 110)
ui_comm_uart_ddlist_check.set_size(90, 30)
# Set style for ui_comm_uart_ddlist_check, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_ddlist_check.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_check.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_ddlist_check, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_uart_ddlist_check_extra_list_selected_checked = lv.style_t()
style_ui_comm_uart_ddlist_check_extra_list_selected_checked.init()
style_ui_comm_uart_ddlist_check_extra_list_selected_checked.set_border_width(1)
style_ui_comm_uart_ddlist_check_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_uart_ddlist_check_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_check_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_check_extra_list_selected_checked.set_radius(3)
style_ui_comm_uart_ddlist_check_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_uart_ddlist_check_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_uart_ddlist_check_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_check.get_list().add_style(style_ui_comm_uart_ddlist_check_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_uart_ddlist_check, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_check_extra_list_main_default = lv.style_t()
style_ui_comm_uart_ddlist_check_extra_list_main_default.init()
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_max_height(90)
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_text_opa(255)
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_border_width(1)
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_border_opa(255)
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_radius(3)
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_uart_ddlist_check_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_check.get_list().add_style(style_ui_comm_uart_ddlist_check_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_uart_ddlist_check, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default.init()
style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_check.get_list().add_style(style_ui_comm_uart_ddlist_check_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_uart_ddlist_data_bit
ui_comm_uart_ddlist_data_bit = lv.dropdown(ui_comm_uart)
ui_comm_uart_ddlist_data_bit.set_options("8\n9\n7\n6\n5")
ui_comm_uart_ddlist_data_bit.set_pos(115, 110)
ui_comm_uart_ddlist_data_bit.set_size(50, 30)
# Set style for ui_comm_uart_ddlist_data_bit, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_ddlist_data_bit.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_data_bit.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_ddlist_data_bit, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked = lv.style_t()
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked.init()
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked.set_border_width(1)
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked.set_radius(3)
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_data_bit.get_list().add_style(style_ui_comm_uart_ddlist_data_bit_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_uart_ddlist_data_bit, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default = lv.style_t()
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.init()
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_max_height(90)
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_text_opa(255)
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_border_width(1)
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_border_opa(255)
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_radius(3)
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_uart_ddlist_data_bit_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_data_bit.get_list().add_style(style_ui_comm_uart_ddlist_data_bit_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_uart_ddlist_data_bit, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default.init()
style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_data_bit.get_list().add_style(style_ui_comm_uart_ddlist_data_bit_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_uart_ddlist_stop
ui_comm_uart_ddlist_stop = lv.dropdown(ui_comm_uart)
ui_comm_uart_ddlist_stop.set_options("1\n1.5\n2")
ui_comm_uart_ddlist_stop.set_pos(60, 110)
ui_comm_uart_ddlist_stop.set_size(50, 30)
# Set style for ui_comm_uart_ddlist_stop, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_ddlist_stop.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_stop.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_ddlist_stop, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked = lv.style_t()
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked.init()
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked.set_border_width(1)
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked.set_radius(3)
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_uart_ddlist_stop_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_stop.get_list().add_style(style_ui_comm_uart_ddlist_stop_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_uart_ddlist_stop, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_stop_extra_list_main_default = lv.style_t()
style_ui_comm_uart_ddlist_stop_extra_list_main_default.init()
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_max_height(90)
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_text_opa(255)
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_border_width(1)
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_border_opa(255)
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_radius(3)
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_uart_ddlist_stop_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_stop.get_list().add_style(style_ui_comm_uart_ddlist_stop_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_uart_ddlist_stop, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default.init()
style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_stop.get_list().add_style(style_ui_comm_uart_ddlist_stop_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_uart_cb_time_stamp
ui_comm_uart_cb_time_stamp = lv.checkbox(ui_comm_uart)
ui_comm_uart_cb_time_stamp.set_text("T")
ui_comm_uart_cb_time_stamp.set_pos(5, 114)
# Set style for ui_comm_uart_cb_time_stamp, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_cb_time_stamp.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_text_letter_space(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_radius(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_cb_time_stamp, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_uart_cb_time_stamp.set_style_pad_all(3, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_border_width(2, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_border_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_border_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_radius(6, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_uart_cb_time_stamp.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_uart_ddlist_tx_fmt
ui_comm_uart_ddlist_tx_fmt = lv.dropdown(ui_comm_uart)
ui_comm_uart_ddlist_tx_fmt.set_options("H\nD")
ui_comm_uart_ddlist_tx_fmt.set_pos(265, 75)
ui_comm_uart_ddlist_tx_fmt.set_size(50, 30)
# Set style for ui_comm_uart_ddlist_tx_fmt, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_ddlist_tx_fmt.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_tx_fmt.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_ddlist_tx_fmt, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked = lv.style_t()
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked.init()
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked.set_border_width(1)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked.set_radius(3)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_tx_fmt.get_list().add_style(style_ui_comm_uart_ddlist_tx_fmt_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_uart_ddlist_tx_fmt, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default = lv.style_t()
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.init()
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_max_height(90)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_text_opa(255)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_border_width(1)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_border_opa(255)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_radius(3)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_tx_fmt.get_list().add_style(style_ui_comm_uart_ddlist_tx_fmt_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_uart_ddlist_tx_fmt, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default.init()
style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_tx_fmt.get_list().add_style(style_ui_comm_uart_ddlist_tx_fmt_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_uart_ddlist_ch
ui_comm_uart_ddlist_ch = lv.dropdown(ui_comm_uart)
ui_comm_uart_ddlist_ch.set_options("LOG\nRC\nRS485\nUART2")
ui_comm_uart_ddlist_ch.set_pos(170, 75)
ui_comm_uart_ddlist_ch.set_size(90, 30)
# Set style for ui_comm_uart_ddlist_ch, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_ddlist_ch.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_border_width(1, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_border_color(lv.color_hex(0xe1e6ee), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_pad_top(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_pad_left(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_pad_right(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_radius(3, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ddlist_ch.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_ddlist_ch, Part: lv.PART.SELECTED, State: lv.STATE.CHECKED.
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked = lv.style_t()
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked.init()
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked.set_border_width(1)
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked.set_border_opa(255)
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked.set_radius(3)
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked.set_bg_opa(255)
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked.set_bg_color(lv.color_hex(0x00a1b5))
style_ui_comm_uart_ddlist_ch_extra_list_selected_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_ch.get_list().add_style(style_ui_comm_uart_ddlist_ch_extra_list_selected_checked, lv.PART.SELECTED|lv.STATE.CHECKED)
# Set style for ui_comm_uart_ddlist_ch, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_ch_extra_list_main_default = lv.style_t()
style_ui_comm_uart_ddlist_ch_extra_list_main_default.init()
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_max_height(90)
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_text_color(lv.color_hex(0x0D3055))
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_text_font(test_font("montserratMedium", 16))
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_text_opa(255)
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_border_width(1)
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_border_opa(255)
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_border_color(lv.color_hex(0xe1e6ee))
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_border_side(lv.BORDER_SIDE.FULL)
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_radius(3)
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_bg_color(lv.color_hex(0xffffff))
style_ui_comm_uart_ddlist_ch_extra_list_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_ch.get_list().add_style(style_ui_comm_uart_ddlist_ch_extra_list_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_uart_ddlist_ch, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default = lv.style_t()
style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default.init()
style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default.set_radius(3)
style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default.set_bg_opa(255)
style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default.set_bg_color(lv.color_hex(0x00ff00))
style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
ui_comm_uart_ddlist_ch.get_list().add_style(style_ui_comm_uart_ddlist_ch_extra_list_scrollbar_default, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_uart_ta_rate
ui_comm_uart_ta_rate = lv.textarea(ui_comm_uart)
ui_comm_uart_ta_rate.set_text("921600")
ui_comm_uart_ta_rate.set_placeholder_text("")
ui_comm_uart_ta_rate.set_password_bullet("*")
ui_comm_uart_ta_rate.set_password_mode(False)
ui_comm_uart_ta_rate.set_one_line(False)
ui_comm_uart_ta_rate.set_accepted_chars("")
ui_comm_uart_ta_rate.set_max_length(32)
ui_comm_uart_ta_rate.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm_uart), lv.EVENT.ALL, None)
ui_comm_uart_ta_rate.set_pos(60, 75)
ui_comm_uart_ta_rate.set_size(105, 30)
# Set style for ui_comm_uart_ta_rate, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_ta_rate.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_text_letter_space(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_border_width(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_border_color(lv.color_hex(0xe6e6e6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_pad_top(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_pad_right(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_pad_left(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_radius(4, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_ta_rate, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
ui_comm_uart_ta_rate.set_style_bg_opa(255, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_uart_ta_rate.set_style_radius(0, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_uart_sw_uart
ui_comm_uart_sw_uart = lv.switch(ui_comm_uart)
ui_comm_uart_sw_uart.set_pos(5, 75)
ui_comm_uart_sw_uart.set_size(50, 30)
# Set style for ui_comm_uart_sw_uart, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_sw_uart.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_sw_uart.set_style_bg_color(lv.color_hex(0xe6e2e6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_sw_uart.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_sw_uart.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_sw_uart.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_sw_uart.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_sw_uart, Part: lv.PART.INDICATOR, State: lv.STATE.CHECKED.
ui_comm_uart_sw_uart.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_comm_uart_sw_uart.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_comm_uart_sw_uart.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_comm_uart_sw_uart.set_style_border_width(0, lv.PART.INDICATOR|lv.STATE.CHECKED)

# Set style for ui_comm_uart_sw_uart, Part: lv.PART.KNOB, State: lv.STATE.DEFAULT.
ui_comm_uart_sw_uart.set_style_bg_opa(255, lv.PART.KNOB|lv.STATE.DEFAULT)
ui_comm_uart_sw_uart.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.KNOB|lv.STATE.DEFAULT)
ui_comm_uart_sw_uart.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.KNOB|lv.STATE.DEFAULT)
ui_comm_uart_sw_uart.set_style_border_width(0, lv.PART.KNOB|lv.STATE.DEFAULT)
ui_comm_uart_sw_uart.set_style_radius(10, lv.PART.KNOB|lv.STATE.DEFAULT)

# Create ui_comm_uart_ta_tx_buf
ui_comm_uart_ta_tx_buf = lv.textarea(ui_comm_uart)
ui_comm_uart_ta_tx_buf.set_text("")
ui_comm_uart_ta_tx_buf.set_placeholder_text("")
ui_comm_uart_ta_tx_buf.set_password_bullet("*")
ui_comm_uart_ta_tx_buf.set_password_mode(False)
ui_comm_uart_ta_tx_buf.set_one_line(True)
ui_comm_uart_ta_tx_buf.set_accepted_chars("")
ui_comm_uart_ta_tx_buf.set_max_length(32)
ui_comm_uart_ta_tx_buf.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm_uart), lv.EVENT.ALL, None)
ui_comm_uart_ta_tx_buf.set_pos(5, 40)
ui_comm_uart_ta_tx_buf.set_size(310, 30)
# Set style for ui_comm_uart_ta_tx_buf, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_ta_tx_buf.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_text_font(test_font("montserratMedium", 14), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_text_letter_space(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_border_width(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_border_color(lv.color_hex(0xe6e6e6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_pad_top(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_pad_right(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_pad_left(4, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_radius(4, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_comm_uart_ta_tx_buf, Part: lv.PART.SCROLLBAR, State: lv.STATE.DEFAULT.
ui_comm_uart_ta_tx_buf.set_style_bg_opa(255, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)
ui_comm_uart_ta_tx_buf.set_style_radius(0, lv.PART.SCROLLBAR|lv.STATE.DEFAULT)

# Create ui_comm_uart_btn_tx
ui_comm_uart_btn_tx = lv.btn(ui_comm_uart)
ui_comm_uart_btn_tx_label = lv.label(ui_comm_uart_btn_tx)
ui_comm_uart_btn_tx_label.set_text(""+lv.SYMBOL.UPLOAD+"")
ui_comm_uart_btn_tx_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_uart_btn_tx_label.set_width(lv.pct(100))
ui_comm_uart_btn_tx_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_uart_btn_tx.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_pos(275, 5)
ui_comm_uart_btn_tx.set_size(40, 30)
# Set style for ui_comm_uart_btn_tx, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_btn_tx.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_uart_btn_tx_clean
ui_comm_uart_btn_tx_clean = lv.btn(ui_comm_uart)
ui_comm_uart_btn_tx_clean_label = lv.label(ui_comm_uart_btn_tx_clean)
ui_comm_uart_btn_tx_clean_label.set_text(""+lv.SYMBOL.TRASH+"")
ui_comm_uart_btn_tx_clean_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_uart_btn_tx_clean_label.set_width(lv.pct(100))
ui_comm_uart_btn_tx_clean_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_uart_btn_tx_clean.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_pos(230, 5)
ui_comm_uart_btn_tx_clean.set_size(40, 30)
# Set style for ui_comm_uart_btn_tx_clean, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_btn_tx_clean.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_tx_clean.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_uart_label_tittle
ui_comm_uart_label_tittle = lv.label(ui_comm_uart)
ui_comm_uart_label_tittle.set_text("UART Data View")
ui_comm_uart_label_tittle.set_long_mode(lv.label.LONG.WRAP)
ui_comm_uart_label_tittle.set_width(lv.pct(100))
ui_comm_uart_label_tittle.set_pos(70, 15)
ui_comm_uart_label_tittle.set_size(180, 30)
# Set style for ui_comm_uart_label_tittle, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_label_tittle.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_label_tittle.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_uart_btn_rx_clean
ui_comm_uart_btn_rx_clean = lv.btn(ui_comm_uart)
ui_comm_uart_btn_rx_clean_label = lv.label(ui_comm_uart_btn_rx_clean)
ui_comm_uart_btn_rx_clean_label.set_text(""+lv.SYMBOL.TRASH+"")
ui_comm_uart_btn_rx_clean_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_uart_btn_rx_clean_label.set_width(lv.pct(100))
ui_comm_uart_btn_rx_clean_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_uart_btn_rx_clean.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_pos(50, 5)
ui_comm_uart_btn_rx_clean.set_size(40, 30)
# Set style for ui_comm_uart_btn_rx_clean, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_btn_rx_clean.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_rx_clean.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_uart_btn_back
ui_comm_uart_btn_back = lv.btn(ui_comm_uart)
ui_comm_uart_btn_back_label = lv.label(ui_comm_uart_btn_back)
ui_comm_uart_btn_back_label.set_text(""+lv.SYMBOL.LEFT+" ")
ui_comm_uart_btn_back_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_uart_btn_back_label.set_width(lv.pct(100))
ui_comm_uart_btn_back_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_uart_btn_back.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_pos(5, 5)
ui_comm_uart_btn_back.set_size(40, 30)
# Set style for ui_comm_uart_btn_back, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_uart_btn_back.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_uart_btn_back.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

ui_comm_uart.update_layout()
# Create ui_comm_rc
ui_comm_rc = lv.obj()
g_kb_ui_comm_rc = lv.keyboard(ui_comm_rc)
g_kb_ui_comm_rc.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_comm_rc), lv.EVENT.ALL, None)
g_kb_ui_comm_rc.add_flag(lv.obj.FLAG.HIDDEN)
g_kb_ui_comm_rc.set_style_text_font(test_font("SourceHanSerifSC_Regular", 18), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc.set_size(320, 240)
ui_comm_rc.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_comm_rc, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_tittle
ui_comm_rc_label_tittle = lv.label(ui_comm_rc)
ui_comm_rc_label_tittle.set_text("RC Data View")
ui_comm_rc_label_tittle.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_tittle.set_width(lv.pct(100))
ui_comm_rc_label_tittle.set_pos(70, 15)
ui_comm_rc_label_tittle.set_size(180, 30)
# Set style for ui_comm_rc_label_tittle, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_tittle.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_tittle.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_btn_back
ui_comm_rc_btn_back = lv.btn(ui_comm_rc)
ui_comm_rc_btn_back_label = lv.label(ui_comm_rc_btn_back)
ui_comm_rc_btn_back_label.set_text(""+lv.SYMBOL.LEFT+" ")
ui_comm_rc_btn_back_label.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_btn_back_label.set_width(lv.pct(100))
ui_comm_rc_btn_back_label.align(lv.ALIGN.CENTER, 0, 0)
ui_comm_rc_btn_back.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_pos(5, 5)
ui_comm_rc_btn_back.set_size(40, 30)
# Set style for ui_comm_rc_btn_back, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_btn_back.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_btn_back.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_cont_1
ui_comm_rc_cont_1 = lv.obj(ui_comm_rc)
ui_comm_rc_cont_1.set_pos(5, 40)
ui_comm_rc_cont_1.set_size(310, 195)
ui_comm_rc_cont_1.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_comm_rc_cont_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_cont_1.set_style_border_width(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_border_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_cont_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Create ui_comm_rc_label_1
ui_comm_rc_label_1 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_1.set_text("CH1")
ui_comm_rc_label_1.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_1.set_width(lv.pct(100))
ui_comm_rc_label_1.set_pos(10, 10)
ui_comm_rc_label_1.set_size(50, 16)
# Set style for ui_comm_rc_label_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_2
ui_comm_rc_label_2 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_2.set_text("CH2")
ui_comm_rc_label_2.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_2.set_width(lv.pct(100))
ui_comm_rc_label_2.set_pos(10, 40)
ui_comm_rc_label_2.set_size(50, 16)
# Set style for ui_comm_rc_label_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_3
ui_comm_rc_label_3 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_3.set_text("CH3")
ui_comm_rc_label_3.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_3.set_width(lv.pct(100))
ui_comm_rc_label_3.set_pos(10, 70)
ui_comm_rc_label_3.set_size(50, 16)
# Set style for ui_comm_rc_label_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_4
ui_comm_rc_label_4 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_4.set_text("CH4")
ui_comm_rc_label_4.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_4.set_width(lv.pct(100))
ui_comm_rc_label_4.set_pos(10, 100)
ui_comm_rc_label_4.set_size(50, 16)
# Set style for ui_comm_rc_label_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_5
ui_comm_rc_label_5 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_5.set_text("CH5")
ui_comm_rc_label_5.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_5.set_width(lv.pct(100))
ui_comm_rc_label_5.set_pos(10, 130)
ui_comm_rc_label_5.set_size(50, 16)
# Set style for ui_comm_rc_label_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_5.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_6
ui_comm_rc_label_6 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_6.set_text("CH6")
ui_comm_rc_label_6.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_6.set_width(lv.pct(100))
ui_comm_rc_label_6.set_pos(10, 160)
ui_comm_rc_label_6.set_size(50, 16)
# Set style for ui_comm_rc_label_6, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_6.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_6.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_7
ui_comm_rc_label_7 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_7.set_text("CH7")
ui_comm_rc_label_7.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_7.set_width(lv.pct(100))
ui_comm_rc_label_7.set_pos(10, 190)
ui_comm_rc_label_7.set_size(50, 16)
# Set style for ui_comm_rc_label_7, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_7.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_7.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_8
ui_comm_rc_label_8 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_8.set_text("CH8")
ui_comm_rc_label_8.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_8.set_width(lv.pct(100))
ui_comm_rc_label_8.set_pos(10, 220)
ui_comm_rc_label_8.set_size(50, 16)
# Set style for ui_comm_rc_label_8, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_8.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_8.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_9
ui_comm_rc_label_9 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_9.set_text("CH9")
ui_comm_rc_label_9.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_9.set_width(lv.pct(100))
ui_comm_rc_label_9.set_pos(10, 250)
ui_comm_rc_label_9.set_size(50, 16)
# Set style for ui_comm_rc_label_9, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_9.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_9.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_10
ui_comm_rc_label_10 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_10.set_text("CH10")
ui_comm_rc_label_10.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_10.set_width(lv.pct(100))
ui_comm_rc_label_10.set_pos(10, 280)
ui_comm_rc_label_10.set_size(50, 16)
# Set style for ui_comm_rc_label_10, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_10.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_10.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_11
ui_comm_rc_label_11 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_11.set_text("CH11")
ui_comm_rc_label_11.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_11.set_width(lv.pct(100))
ui_comm_rc_label_11.set_pos(10, 310)
ui_comm_rc_label_11.set_size(50, 16)
# Set style for ui_comm_rc_label_11, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_11.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_11.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_12
ui_comm_rc_label_12 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_12.set_text("CH12")
ui_comm_rc_label_12.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_12.set_width(lv.pct(100))
ui_comm_rc_label_12.set_pos(10, 340)
ui_comm_rc_label_12.set_size(50, 16)
# Set style for ui_comm_rc_label_12, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_12.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_12.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_13
ui_comm_rc_label_13 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_13.set_text("CH13")
ui_comm_rc_label_13.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_13.set_width(lv.pct(100))
ui_comm_rc_label_13.set_pos(10, 370)
ui_comm_rc_label_13.set_size(50, 16)
# Set style for ui_comm_rc_label_13, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_13.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_13.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_14
ui_comm_rc_label_14 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_14.set_text("CH14")
ui_comm_rc_label_14.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_14.set_width(lv.pct(100))
ui_comm_rc_label_14.set_pos(10, 400)
ui_comm_rc_label_14.set_size(50, 16)
# Set style for ui_comm_rc_label_14, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_14.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_14.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_15
ui_comm_rc_label_15 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_15.set_text("CH15")
ui_comm_rc_label_15.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_15.set_width(lv.pct(100))
ui_comm_rc_label_15.set_pos(10, 430)
ui_comm_rc_label_15.set_size(50, 16)
# Set style for ui_comm_rc_label_15, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_15.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_15.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_label_16
ui_comm_rc_label_16 = lv.label(ui_comm_rc_cont_1)
ui_comm_rc_label_16.set_text("CH16")
ui_comm_rc_label_16.set_long_mode(lv.label.LONG.WRAP)
ui_comm_rc_label_16.set_width(lv.pct(100))
ui_comm_rc_label_16.set_pos(10, 460)
ui_comm_rc_label_16.set_size(50, 16)
# Set style for ui_comm_rc_label_16, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_label_16.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_label_16.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_1
ui_comm_rc_bar_1 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_1.set_style_anim_time(1000, 0)
ui_comm_rc_bar_1.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_1.set_range(200, 1800)
ui_comm_rc_bar_1.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_1.set_pos(80, 10)
ui_comm_rc_bar_1.set_size(200, 16)
# Set style for ui_comm_rc_bar_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_1.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_1.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_1.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_1.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_1, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_1.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_1.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_1.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_1.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_2
ui_comm_rc_bar_2 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_2.set_style_anim_time(1000, 0)
ui_comm_rc_bar_2.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_2.set_range(200, 1800)
ui_comm_rc_bar_2.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_2.set_pos(80, 40)
ui_comm_rc_bar_2.set_size(200, 16)
# Set style for ui_comm_rc_bar_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_2.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_2.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_2.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_2.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_2, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_2.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_2.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_2.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_2.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_3
ui_comm_rc_bar_3 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_3.set_style_anim_time(1000, 0)
ui_comm_rc_bar_3.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_3.set_range(200, 1800)
ui_comm_rc_bar_3.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_3.set_pos(80, 70)
ui_comm_rc_bar_3.set_size(200, 16)
# Set style for ui_comm_rc_bar_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_3.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_3.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_3.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_3.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_3, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_3.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_3.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_3.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_3.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_4
ui_comm_rc_bar_4 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_4.set_style_anim_time(1000, 0)
ui_comm_rc_bar_4.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_4.set_range(200, 1800)
ui_comm_rc_bar_4.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_4.set_pos(80, 100)
ui_comm_rc_bar_4.set_size(200, 16)
# Set style for ui_comm_rc_bar_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_4.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_4.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_4.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_4.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_4, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_4.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_4.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_4.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_4.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_5
ui_comm_rc_bar_5 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_5.set_style_anim_time(1000, 0)
ui_comm_rc_bar_5.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_5.set_range(200, 1800)
ui_comm_rc_bar_5.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_5.set_pos(80, 130)
ui_comm_rc_bar_5.set_size(200, 16)
# Set style for ui_comm_rc_bar_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_5.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_5.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_5.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_5.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_5, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_5.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_5.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_5.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_5.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_6
ui_comm_rc_bar_6 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_6.set_style_anim_time(1000, 0)
ui_comm_rc_bar_6.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_6.set_range(200, 1800)
ui_comm_rc_bar_6.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_6.set_pos(80, 160)
ui_comm_rc_bar_6.set_size(200, 16)
# Set style for ui_comm_rc_bar_6, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_6.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_6.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_6.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_6.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_6.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_6, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_6.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_6.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_6.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_6.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_7
ui_comm_rc_bar_7 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_7.set_style_anim_time(1000, 0)
ui_comm_rc_bar_7.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_7.set_range(200, 1800)
ui_comm_rc_bar_7.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_7.set_pos(80, 190)
ui_comm_rc_bar_7.set_size(200, 16)
# Set style for ui_comm_rc_bar_7, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_7.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_7.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_7.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_7.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_7.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_7, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_7.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_7.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_7.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_7.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_8
ui_comm_rc_bar_8 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_8.set_style_anim_time(1000, 0)
ui_comm_rc_bar_8.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_8.set_range(200, 1800)
ui_comm_rc_bar_8.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_8.set_pos(80, 220)
ui_comm_rc_bar_8.set_size(200, 16)
# Set style for ui_comm_rc_bar_8, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_8.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_8.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_8.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_8.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_8.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_8, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_8.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_8.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_8.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_8.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_9
ui_comm_rc_bar_9 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_9.set_style_anim_time(1000, 0)
ui_comm_rc_bar_9.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_9.set_range(200, 1800)
ui_comm_rc_bar_9.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_9.set_pos(80, 250)
ui_comm_rc_bar_9.set_size(200, 16)
# Set style for ui_comm_rc_bar_9, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_9.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_9.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_9.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_9.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_9.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_9, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_9.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_9.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_9.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_9.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_10
ui_comm_rc_bar_10 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_10.set_style_anim_time(1000, 0)
ui_comm_rc_bar_10.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_10.set_range(200, 1800)
ui_comm_rc_bar_10.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_10.set_pos(80, 280)
ui_comm_rc_bar_10.set_size(200, 16)
# Set style for ui_comm_rc_bar_10, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_10.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_10.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_10.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_10.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_10.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_10, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_10.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_10.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_10.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_10.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_11
ui_comm_rc_bar_11 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_11.set_style_anim_time(1000, 0)
ui_comm_rc_bar_11.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_11.set_range(200, 1800)
ui_comm_rc_bar_11.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_11.set_pos(80, 310)
ui_comm_rc_bar_11.set_size(200, 16)
# Set style for ui_comm_rc_bar_11, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_11.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_11.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_11.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_11.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_11.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_11, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_11.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_11.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_11.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_11.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_12
ui_comm_rc_bar_12 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_12.set_style_anim_time(1000, 0)
ui_comm_rc_bar_12.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_12.set_range(200, 1800)
ui_comm_rc_bar_12.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_12.set_pos(80, 340)
ui_comm_rc_bar_12.set_size(200, 16)
# Set style for ui_comm_rc_bar_12, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_12.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_12.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_12.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_12.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_12.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_12, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_12.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_12.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_12.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_12.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_13
ui_comm_rc_bar_13 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_13.set_style_anim_time(1000, 0)
ui_comm_rc_bar_13.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_13.set_range(200, 1800)
ui_comm_rc_bar_13.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_13.set_pos(80, 370)
ui_comm_rc_bar_13.set_size(200, 16)
# Set style for ui_comm_rc_bar_13, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_13.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_13.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_13.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_13.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_13.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_13, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_13.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_13.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_13.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_13.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_14
ui_comm_rc_bar_14 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_14.set_style_anim_time(1000, 0)
ui_comm_rc_bar_14.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_14.set_range(200, 1800)
ui_comm_rc_bar_14.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_14.set_pos(80, 400)
ui_comm_rc_bar_14.set_size(200, 16)
# Set style for ui_comm_rc_bar_14, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_14.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_14.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_14.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_14.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_14.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_14, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_14.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_14.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_14.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_14.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_15
ui_comm_rc_bar_15 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_15.set_style_anim_time(1000, 0)
ui_comm_rc_bar_15.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_15.set_range(200, 1800)
ui_comm_rc_bar_15.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_15.set_pos(80, 430)
ui_comm_rc_bar_15.set_size(200, 16)
# Set style for ui_comm_rc_bar_15, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_15.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_15.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_15.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_15.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_15.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_15, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_15.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_15.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_15.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_15.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_comm_rc_bar_16
ui_comm_rc_bar_16 = lv.bar(ui_comm_rc_cont_1)
ui_comm_rc_bar_16.set_style_anim_time(1000, 0)
ui_comm_rc_bar_16.set_mode(lv.bar.MODE.NORMAL)
ui_comm_rc_bar_16.set_range(200, 1800)
ui_comm_rc_bar_16.set_value(200, lv.ANIM.OFF)
ui_comm_rc_bar_16.set_pos(80, 460)
ui_comm_rc_bar_16.set_size(200, 16)
# Set style for ui_comm_rc_bar_16, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_16.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_16.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_16.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_16.set_style_radius(10, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_comm_rc_bar_16.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for ui_comm_rc_bar_16, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_comm_rc_bar_16.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_16.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_16.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_comm_rc_bar_16.set_style_radius(10, lv.PART.INDICATOR|lv.STATE.DEFAULT)

ui_comm_rc.update_layout()
# Create ui_io
ui_io = lv.obj()
g_kb_ui_io = lv.keyboard(ui_io)
g_kb_ui_io.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_io), lv.EVENT.ALL, None)
g_kb_ui_io.add_flag(lv.obj.FLAG.HIDDEN)
g_kb_ui_io.set_style_text_font(test_font("SourceHanSerifSC_Regular", 18), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io.set_size(320, 240)
ui_io.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_io, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_io.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_io_label_title
ui_io_label_title = lv.label(ui_io)
ui_io_label_title.set_text("IO Control")
ui_io_label_title.set_long_mode(lv.label.LONG.WRAP)
ui_io_label_title.set_width(lv.pct(100))
ui_io_label_title.set_pos(70, 15)
ui_io_label_title.set_size(180, 30)
# Set style for ui_io_label_title, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_io_label_title.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_label_title.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_io_btn_home
ui_io_btn_home = lv.btn(ui_io)
ui_io_btn_home_label = lv.label(ui_io_btn_home)
ui_io_btn_home_label.set_text(""+lv.SYMBOL.HOME+" ")
ui_io_btn_home_label.set_long_mode(lv.label.LONG.WRAP)
ui_io_btn_home_label.set_width(lv.pct(100))
ui_io_btn_home_label.align(lv.ALIGN.CENTER, 0, 0)
ui_io_btn_home.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_io_btn_home.set_pos(5, 5)
ui_io_btn_home.set_size(40, 30)
# Set style for ui_io_btn_home, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_io_btn_home.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_btn_home.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_btn_home.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_btn_home.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_btn_home.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_btn_home.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_btn_home.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_btn_home.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_btn_home.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_io_btn_home.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

ui_io.update_layout()
# Create ui_led
ui_led = lv.obj()
g_kb_ui_led = lv.keyboard(ui_led)
g_kb_ui_led.add_event_cb(lambda e: ta_event_cb(e, g_kb_ui_led), lv.EVENT.ALL, None)
g_kb_ui_led.add_flag(lv.obj.FLAG.HIDDEN)
g_kb_ui_led.set_style_text_font(test_font("SourceHanSerifSC_Regular", 18), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led.set_size(320, 240)
ui_led.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for ui_led, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_led.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_led_slider_period
ui_led_slider_period = lv.slider(ui_led)
ui_led_slider_period.set_range(50, 1000)
ui_led_slider_period.set_mode(lv.slider.MODE.NORMAL)
ui_led_slider_period.set_value(500, lv.ANIM.OFF)
ui_led_slider_period.set_pos(20, 180)
ui_led_slider_period.set_size(280, 10)
# Set style for ui_led_slider_period, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_led_slider_period.set_style_bg_opa(60, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_radius(8, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_outline_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_led_slider_period, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_led_slider_period.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_radius(8, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Set style for ui_led_slider_period, Part: lv.PART.KNOB, State: lv.STATE.DEFAULT.
ui_led_slider_period.set_style_bg_opa(255, lv.PART.KNOB|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.KNOB|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.KNOB|lv.STATE.DEFAULT)
ui_led_slider_period.set_style_radius(8, lv.PART.KNOB|lv.STATE.DEFAULT)

# Create ui_led_label_period
ui_led_label_period = lv.label(ui_led)
ui_led_label_period.set_text("")
ui_led_label_period.set_long_mode(lv.label.LONG.WRAP)
ui_led_label_period.set_width(lv.pct(100))
ui_led_label_period.set_pos(120, 150)
ui_led_label_period.set_size(110, 30)
# Set style for ui_led_label_period, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_led_label_period.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_period.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_led_label_blink
ui_led_label_blink = lv.label(ui_led)
ui_led_label_blink.set_text("Blink Period: ")
ui_led_label_blink.set_long_mode(lv.label.LONG.WRAP)
ui_led_label_blink.set_width(lv.pct(100))
ui_led_label_blink.set_pos(10, 150)
ui_led_label_blink.set_size(110, 30)
# Set style for ui_led_label_blink, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_led_label_blink.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_blink.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_led_cb_sta
ui_led_cb_sta = lv.checkbox(ui_led)
ui_led_cb_sta.set_text("LED ON")
ui_led_cb_sta.set_pos(10, 80)
# Set style for ui_led_cb_sta, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_led_cb_sta.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_text_letter_space(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_radius(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_led_cb_sta, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_led_cb_sta.set_style_pad_all(3, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_border_width(2, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_border_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_border_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_radius(6, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_sta.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Create ui_led_cb_blink
ui_led_cb_blink = lv.checkbox(ui_led)
ui_led_cb_blink.set_text("Auto blink")
ui_led_cb_blink.set_pos(10, 50)
# Set style for ui_led_cb_blink, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_led_cb_blink.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_text_color(lv.color_hex(0x0D3055), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_text_letter_space(2, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_radius(6, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Set style for ui_led_cb_blink, Part: lv.PART.INDICATOR, State: lv.STATE.DEFAULT.
ui_led_cb_blink.set_style_pad_all(3, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_border_width(2, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_border_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_border_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_radius(6, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_bg_color(lv.color_hex(0xffffff), lv.PART.INDICATOR|lv.STATE.DEFAULT)
ui_led_cb_blink.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# Set style for ui_led_cb_blink, Part: lv.PART.INDICATOR, State: lv.STATE.CHECKED.
ui_led_cb_blink.set_style_pad_all(3, lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_led_cb_blink.set_style_border_width(2, lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_led_cb_blink.set_style_border_opa(255, lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_led_cb_blink.set_style_border_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_led_cb_blink.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_led_cb_blink.set_style_radius(6, lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_led_cb_blink.set_style_bg_opa(255, lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_led_cb_blink.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.INDICATOR|lv.STATE.CHECKED)
ui_led_cb_blink.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.INDICATOR|lv.STATE.CHECKED)

# Create ui_led_label_title
ui_led_label_title = lv.label(ui_led)
ui_led_label_title.set_text("LED Status")
ui_led_label_title.set_long_mode(lv.label.LONG.WRAP)
ui_led_label_title.set_width(lv.pct(100))
ui_led_label_title.set_pos(70, 15)
ui_led_label_title.set_size(180, 30)
# Set style for ui_led_label_title, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_led_label_title.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_label_title.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create ui_led_btn_home
ui_led_btn_home = lv.btn(ui_led)
ui_led_btn_home_label = lv.label(ui_led_btn_home)
ui_led_btn_home_label.set_text(""+lv.SYMBOL.HOME+" ")
ui_led_btn_home_label.set_long_mode(lv.label.LONG.WRAP)
ui_led_btn_home_label.set_width(lv.pct(100))
ui_led_btn_home_label.align(lv.ALIGN.CENTER, 0, 0)
ui_led_btn_home.set_style_pad_all(0, lv.STATE.DEFAULT)
ui_led_btn_home.set_pos(5, 5)
ui_led_btn_home.set_size(40, 30)
# Set style for ui_led_btn_home, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
ui_led_btn_home.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_btn_home.set_style_bg_color(lv.color_hex(0xff0027), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_btn_home.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_btn_home.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_btn_home.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_btn_home.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_btn_home.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_btn_home.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_btn_home.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
ui_led_btn_home.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

ui_led.update_layout()

def ui_main_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.SCREEN_LOAD_START):
        pass
        

ui_main.add_event_cb(lambda e: ui_main_event_handler(e), lv.EVENT.ALL, None)

def ui_main_btn_pwr_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
ui_main_btn_pwr.add_event_cb(lambda e: ui_main_btn_pwr_event_handler(e), lv.EVENT.ALL, None)

def ui_main_btn_io_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_io, lv.SCR_LOAD_ANIM.MOVE_LEFT, 200, 0, False)
ui_main_btn_io.add_event_cb(lambda e: ui_main_btn_io_event_handler(e), lv.EVENT.ALL, None)

def ui_main_btn_comm_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_comm, lv.SCR_LOAD_ANIM.MOVE_LEFT, 200, 0, False)
ui_main_btn_comm.add_event_cb(lambda e: ui_main_btn_comm_event_handler(e), lv.EVENT.ALL, None)

def ui_main_btn_led_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_led, lv.SCR_LOAD_ANIM.MOVE_LEFT, 200, 0, False)
ui_main_btn_led.add_event_cb(lambda e: ui_main_btn_led_event_handler(e), lv.EVENT.ALL, None)

def ui_main_btn_storage_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_storage, lv.SCR_LOAD_ANIM.MOVE_LEFT, 200, 0, False)
ui_main_btn_storage.add_event_cb(lambda e: ui_main_btn_storage_event_handler(e), lv.EVENT.ALL, None)

def ui_main_btn_settings_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_settings, lv.SCR_LOAD_ANIM.MOVE_LEFT, 200, 0, False)
ui_main_btn_settings.add_event_cb(lambda e: ui_main_btn_settings_event_handler(e), lv.EVENT.ALL, None)

def ui_settings_btn_home_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_main, lv.SCR_LOAD_ANIM.MOVE_RIGHT, 200, 0, False)
ui_settings_btn_home.add_event_cb(lambda e: ui_settings_btn_home_event_handler(e), lv.EVENT.ALL, None)

def ui_storage_btn_next_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
ui_storage_btn_next.add_event_cb(lambda e: ui_storage_btn_next_event_handler(e), lv.EVENT.ALL, None)

def ui_storage_btn_prev_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
ui_storage_btn_prev.add_event_cb(lambda e: ui_storage_btn_prev_event_handler(e), lv.EVENT.ALL, None)

def ui_storage_btn_home_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_main, lv.SCR_LOAD_ANIM.MOVE_RIGHT, 200, 0, False)
ui_storage_btn_home.add_event_cb(lambda e: ui_storage_btn_home_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_list_comm_item1_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_comm_can, lv.SCR_LOAD_ANIM.MOVE_BOTTOM, 200, 0, False)
ui_comm_list_comm_item1.add_event_cb(lambda e: ui_comm_list_comm_item1_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_list_comm_item2_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_comm_uart, lv.SCR_LOAD_ANIM.MOVE_BOTTOM, 200, 0, False)
ui_comm_list_comm_item2.add_event_cb(lambda e: ui_comm_list_comm_item2_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_list_comm_item3_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_comm_rc, lv.SCR_LOAD_ANIM.MOVE_BOTTOM, 200, 0, False)
ui_comm_list_comm_item3.add_event_cb(lambda e: ui_comm_list_comm_item3_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_btn_home_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_main, lv.SCR_LOAD_ANIM.MOVE_RIGHT, 200, 0, False)
ui_comm_btn_home.add_event_cb(lambda e: ui_comm_btn_home_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.SCREEN_LOAD_START):
        pass
        

    if (code == lv.EVENT.SCREEN_UNLOADED):
        pass
        

ui_comm_can.add_event_cb(lambda e: ui_comm_can_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_ddlist_ch_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.VALUE_CHANGED):
        pass
        

ui_comm_can_ddlist_ch.add_event_cb(lambda e: ui_comm_can_ddlist_ch_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_ddlist_rate_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.VALUE_CHANGED):
        pass
        

ui_comm_can_ddlist_rate.add_event_cb(lambda e: ui_comm_can_ddlist_rate_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_ddlist_rtr_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.VALUE_CHANGED):
        pass
        

ui_comm_can_ddlist_rtr.add_event_cb(lambda e: ui_comm_can_ddlist_rtr_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_ddlist_ide_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.VALUE_CHANGED):
        pass
        

ui_comm_can_ddlist_ide.add_event_cb(lambda e: ui_comm_can_ddlist_ide_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_ta_can_id_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.VALUE_CHANGED):
        pass
        

ui_comm_can_ta_can_id.add_event_cb(lambda e: ui_comm_can_ta_can_id_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_ta_tx_buf_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
ui_comm_can_ta_tx_buf.add_event_cb(lambda e: ui_comm_can_ta_tx_buf_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_btn_tx_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        

ui_comm_can_btn_tx.add_event_cb(lambda e: ui_comm_can_btn_tx_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_btn_tx_clean_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        ui_comm_can_ta_tx_buf.set_text("")
ui_comm_can_btn_tx_clean.add_event_cb(lambda e: ui_comm_can_btn_tx_clean_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_btn_rx_clean_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        ui_comm_can_ta_rx_msg.set_text("")
        

ui_comm_can_btn_rx_clean.add_event_cb(lambda e: ui_comm_can_btn_rx_clean_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_can_btn_back_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_comm, lv.SCR_LOAD_ANIM.MOVE_TOP, 200, 0, False)
ui_comm_can_btn_back.add_event_cb(lambda e: ui_comm_can_btn_back_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_uart_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.SCREEN_LOAD_START):
        pass
        

ui_comm_uart.add_event_cb(lambda e: ui_comm_uart_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_uart_ddlist_ch_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.VALUE_CHANGED):
        pass
        

ui_comm_uart_ddlist_ch.add_event_cb(lambda e: ui_comm_uart_ddlist_ch_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_uart_sw_uart_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.VALUE_CHANGED):
        pass
ui_comm_uart_sw_uart.add_event_cb(lambda e: ui_comm_uart_sw_uart_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_uart_btn_tx_clean_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        ui_comm_uart_ta_tx_buf.set_text("")
ui_comm_uart_btn_tx_clean.add_event_cb(lambda e: ui_comm_uart_btn_tx_clean_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_uart_btn_rx_clean_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        ui_comm_uart_ta_rx_msg.set_text("")
ui_comm_uart_btn_rx_clean.add_event_cb(lambda e: ui_comm_uart_btn_rx_clean_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_uart_btn_back_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_comm, lv.SCR_LOAD_ANIM.MOVE_TOP, 200, 0, False)
ui_comm_uart_btn_back.add_event_cb(lambda e: ui_comm_uart_btn_back_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_rc_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.SCREEN_LOAD_START):
        pass
        

    if (code == lv.EVENT.SCREEN_UNLOADED):
        pass
        // 删除定时器
        
        if(rc_update_timer != NULL) {
        
            lv_timer_del(rc_update_timer)
        
            rc_update_timer = NULL
        
        }

ui_comm_rc.add_event_cb(lambda e: ui_comm_rc_event_handler(e), lv.EVENT.ALL, None)

def ui_comm_rc_btn_back_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.RELEASED):
        pass
        lv.scr_load_anim(ui_comm, lv.SCR_LOAD_ANIM.MOVE_TOP, 200, 0, False)
ui_comm_rc_btn_back.add_event_cb(lambda e: ui_comm_rc_btn_back_event_handler(e), lv.EVENT.ALL, None)

def ui_io_btn_home_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.scr_load_anim(ui_main, lv.SCR_LOAD_ANIM.MOVE_RIGHT, 200, 0, False)
ui_io_btn_home.add_event_cb(lambda e: ui_io_btn_home_event_handler(e), lv.EVENT.ALL, None)

def ui_led_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.SCREEN_LOAD_START):
        pass
        

ui_led.add_event_cb(lambda e: ui_led_event_handler(e), lv.EVENT.ALL, None)

def ui_led_slider_period_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.VALUE_CHANGED):
        pass
        

ui_led_slider_period.add_event_cb(lambda e: ui_led_slider_period_event_handler(e), lv.EVENT.ALL, None)

def ui_led_cb_sta_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        

ui_led_cb_sta.add_event_cb(lambda e: ui_led_cb_sta_event_handler(e), lv.EVENT.ALL, None)

def ui_led_cb_blink_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        

ui_led_cb_blink.add_event_cb(lambda e: ui_led_cb_blink_event_handler(e), lv.EVENT.ALL, None)

def ui_led_btn_home_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.scr_load_anim(ui_main, lv.SCR_LOAD_ANIM.MOVE_RIGHT, 200, 0, False)
ui_led_btn_home.add_event_cb(lambda e: ui_led_btn_home_event_handler(e), lv.EVENT.ALL, None)

# content from custom.py

# Load the default screen
lv.scr_load(ui_main)

while SDL.check():
    time.sleep_ms(5)

