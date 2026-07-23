#include "unity.h"
#include "led_driver.h"
#include "gpio.h"

#define PIN_RED   4
#define PIN_GREEN 5

static int pin_state[8];

/* Test stub — the production build links against the real gpio module. */
void gpio_set(int pin, int value) {
    pin_state[pin] = value;
}

void setUp(void) {
    for (int i = 0; i < 8; i++) pin_state[i] = -1;
}

void tearDown(void) {}

/* @tests:TC-001 */
void test_off_state_lights_red_only(void) {
    set_led_state(LED_STATE_OFF);
    TEST_ASSERT_EQUAL_INT(HIGH, pin_state[PIN_RED]);
    TEST_ASSERT_EQUAL_INT(LOW,  pin_state[PIN_GREEN]);
}

/* @tests:LED-TC-002 */
void test_armed_state_lights_green_only(void) {
    set_led_state(LED_STATE_ARMED);
    TEST_ASSERT_EQUAL_INT(LOW,  pin_state[PIN_RED]);
    TEST_ASSERT_EQUAL_INT(HIGH, pin_state[PIN_GREEN]);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_off_state_lights_red_only);
    RUN_TEST(test_armed_state_lights_green_only);
    return UNITY_END();
}
