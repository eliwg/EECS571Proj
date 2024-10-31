/*
 * Hello world example
 */
#include <rtems.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

rtems_task Init(
  rtems_task_argument ignored
)
{
  printf("Hello World!");
  exit( 0 );
}