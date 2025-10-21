#ifndef __HAL_CONFIG_H
#define __HAL_CONFIG_H

/* SYS Config */
// #define USE_FREE_RTOS 0
// #define USE_CMSIS_OS 0
#define USE_CMSIS_OS2 0

#define HAL_DELAY_ENABLED 1
#define USE_DELAY_UNTIL 0

/* GPIO Config*/
#define HAL_GPIO_ENABLED 1

/* TIM Config */
#define HAL_TIM_ENABLE 0

/* TIM Hardware Channels */
#define HW_TIM_1_EN 0   // TIM1
#define HW_TIM_2_EN 0   // TIM2
#define HW_TIM_3_EN 0   // TIM3
#define HW_TIM_4_EN 0   // TIM4
#define HW_TIM_5_EN 0   // TIM5
#define HW_TIM_6_EN 0   // TIM6
#define HW_TIM_7_EN 0   // TIM7
#define HW_TIM_8_EN 0   // TIM8
#define HW_TIM_9_EN 0   // TIM9
#define HW_TIM_10_EN 0  // TIM10
#define HW_TIM_11_END 0 // TIM11
#define HW_TIM_12_END 0 // TIM12
#define HW_TIM_13_END 0 // TIM13
#define HW_TIM_14_END 0 // TIM14

// 根据硬件配置定义可用TIM通道数
#define HW_TIM_EN_CNT                                                          \
  (HW_TIM_1_EN + HW_TIM_2_EN + HW_TIM_3_EN + HW_TIM_4_EN + HW_TIM_5_EN +       \
   HW_TIM_6_EN + HW_TIM_7_EN + HW_TIM_8_EN + HW_TIM_9_EN + HW_TIM_10_EN +      \
   HW_TIM_11_END + HW_TIM_12_END + HW_TIM_13_END + HW_TIM_14_END)

/* UART Config*/
#define HAL_UART_ENABLED 1

/* UART Hardware Channels */
#define HW_UART_1_EN 1 // UART1 通道未启用
#define HW_UART_2_EN 0 // UART2 通道未启用
#define HW_UART_3_EN 1 // UART3 通道未启用
#define HW_UART_4_EN 0 // UART4 通道启用
#define HW_UART_5_EN 0 // UART5
#define HW_UART_6_EN 0 // UART6 通道启用

// 根据硬件配置定义可用UART通道数
#define HW_UART_EN_CNT                                                         \
  (HW_UART_1_EN + HW_UART_2_EN + HW_UART_3_EN + HW_UART_4_EN + HW_UART_5_EN +  \
   HW_UART_6_EN)

#define HW_LOG_HUART UART_3
#define HW_CMD_HUART UART_3

#define HW_SBUS_HUART UART_4
#define HW_JODELL_HUART UART_6

/* CAN Config*/
#define HAL_CAN_ENABLED 0
#define HW_CAN_1_EN 0 // CAN1 通道启用
#define HW_CAN_2_EN 0 // CAN2 通道启用（如果硬件不支持可设为0）

// 根据硬件配置定义可用CAN通道数
#define HW_CAN_EN_CNT (HW_CAN_1_EN + HW_CAN_2_EN)

/* ADC Config */
#define HAL_ADC_ENABLED 0

/* ADC Hardware Channels */
#define HW_ADC_1_EN 0 // ADC1 通道启用
#define HW_ADC_2_EN 0 // ADC2 通道未启用
#define HW_ADC_3_EN 0 // ADC3 通道未启用

// 根据硬件配置定义可用ADC通道数
#define HW_ADC_EN_CNT (HW_ADC_1_EN + HW_ADC_2_EN + HW_ADC_3_EN)

#define HAL_SPI_SW_ENABLED 1

#endif // __HAL_CONFIG_H