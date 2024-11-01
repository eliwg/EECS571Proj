#include <rtems.h>
#include <bsp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define UART_DEVICE "/dev/ttyUSB0"
#define BUF_SZ 256

rtems_id task_id;

void uart_read_task(rtems_task_argument argument) {
    char buf[BUF_SZ];
    int bytes_read;
    int fd;

    // fd = open(UART_DEVICE, O_RDONLY);
    printf("Hello\n");
    fflush(stdout);

    while (1) {
        // bytes_read = read(UART_DEVICE, buf, sizeof(buf) - 1);
        bytes_read = scanf("%s", buf);
        printf("Bytes read = %d\n", bytes_read);
        fflush(stdout);
        if (bytes_read > 0) {
            buf[bytes_read] = '\0';  // Null-terminate the string
            printf("Read from UART: %s\n", buf);
			fflush(stdout);
        } else {
            // Handle error or timeout
            rtems_task_wake_after(10);  // Sleep for 10 ms to avoid busy waiting
        }
    }
}

rtems_task Init(rtems_task_argument ignored) {
    rtems_status_code status;

	printf("Hello world!\n The tasks have not yet been created!\n");

    // Create the UART read task
    status = rtems_task_create(
        rtems_build_name('U', 'A', 'R', 'T'),
        1,
        RTEMS_MINIMUM_STACK_SIZE,
        RTEMS_DEFAULT_MODES,
        RTEMS_DEFAULT_ATTRIBUTES,
        &task_id
    );

    if (status != RTEMS_SUCCESSFUL) {
        printf("Task create failed: %d\n", status);
        exit(1);
    }

    status = rtems_task_start(task_id, uart_read_task, 0);
    if (status != RTEMS_SUCCESSFUL) {
        printf("Task start failed: %d\n", status);
        exit(1);
    }

    // Delete Init task
    rtems_task_delete(RTEMS_SELF);
}

rtems_task Init(rtems_task_argument ignored);
