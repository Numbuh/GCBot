#ifndef CONTROLLER_H
#define CONTROLLER_H

#include "pico/stdlib.h"

void init_controller();
void send_button(uint16_t buttons);

#endif
