#include "led_driver.h"
#include "gpio.h"

#define PIN_RED   4
#define PIN_GREEN 5

void set_led_state(led_state_t state) {
    switch (state) {
        case LED_STATE_OFF:
            gpio_set(PIN_RED, HIGH);
            gpio_set(PIN_GREEN, LOW);
            break;
        case LED_STATE_ARMED:
            gpio_set(PIN_RED, LOW);
            gpio_set(PIN_GREEN, HIGH);
            break;
    }
}
