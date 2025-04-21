#include "pico/stdlib.h"
#include "controller.h"

#define BUTTON_A      (1 << 0)
#define BUTTON_B      (1 << 1)
#define BUTTON_START  (1 << 4)
#define BUTTON_SELECT (1 << 5)

void mashA(int count, int delay) {
    for (int i = 0; i < count; i++) {
        send_button(BUTTON_A);
        sleep_ms(50);
        send_button(0);
        sleep_ms(delay);
    }
}

void softReset() {
    send_button(BUTTON_START | BUTTON_SELECT | BUTTON_A | BUTTON_B);
    sleep_ms(1000);
    send_button(0);
    sleep_ms(3000);
}

int main() {
    stdio_init_all();
    init_controller();

    while (true) {
        sleep_ms(5000);
        mashA(200, 100);
        sleep_ms(10000);
        mashA(20, 150);
        sleep_ms(5000);
        softReset();
    }
}
