#ifndef __DISPLAY_CONFIG_H
#define __DISPLAY_CONFIG_H

#include "main.h"

#define DISPLAY_HW_TYPE LCD
#define USE_FMC 1
#if DISPLAY_HW_TYPE == LCD
#define LCD_BL_GPIO LCD_BL_GPIO_Port
#define LCD_BL_PIN LCD_BL_Pin
#endif

// 使用NOR/SRAM的 Bank1.sector1,地址位HADDR[27,26]=11 A6作为数据命令区分线
// 注意设置时STM32内部会右移一位对其! 111 1110=0X7E

#if USE_FMC
#define LCD_ADDR 0x6001FFFE
#endif

#define SCREEN_WIDTH     240                     // 屏的宽度像素点
#define SCREEN_HEIGHT    320                     // 屏的高度像素点

#define DRIVER_LCD_ILI9341_ENABLED 1

#endif // __DISPLAY_CONFIG_H