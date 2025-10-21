#ifndef __COMM_CONFIG_H
#define __COMM_CONFIG_H

// 这里是驱动程序的配置选项
// communication
#define USE_LOG_LITE 1

#define DRIVER_CAN_ENABLED 0
#define DRIVER_LOG_ENABLED 1
#define DRIVER_CMD_ENABLED 1
#define DRIVER_SBUS_ENABLED 0

typedef enum {
  UART_LOG,
  UART_RC,
  UART_RS485,
  UART2,
} uartx_e;

typedef enum {
  CAN1_PORT,
  CAN2_PORT,
} canx_e;

#endif // __COMM_CONFIG_H