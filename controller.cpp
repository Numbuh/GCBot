#include "controller.h"

#define DATA_PIN 2

void init_controller() {
    gpio_init(DATA_PIN);
    gpio_set_dir(DATA_PIN, GPIO_OUT);
    gpio_put(DATA_PIN, 1);
}

void send_button(uint16_t buttons) {
    // TODO: Implement real GameCube protocol.
    // For now, just fake a pulse for testing
    gpio_put(DATA_PIN, 0);
    sleep_us(20);
    gpio_put(DATA_PIN, 1);
}
