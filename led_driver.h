/*
---
itemId: LED-001
itemType: Software Item Spec
itemTitle: LED Driver Interface Specification
---
*/

typedef enum {
    LED_STATE_OFF,
    LED_STATE_ARMED
} led_state_t;

void set_led_state(led_state_t state);
