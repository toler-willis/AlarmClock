---
itemId: LED-TC-002
itemType: Test Case
itemTitle: Green LED Armed-State Verification
itemTests:
  - KXITM36BZ7JX4H99BM8CA1DJSE7XT6E  # DI-002: Green LED Indicates Alarm is Armed
  - KXITM4BJ1RTM5GQ8JXSB9Z37D5S9BWN  # Spec-001: LED Driver state machine
---

# LED-TC-002: Green LED Armed-State Verification

Verifies that when the LED driver is placed in the `LED_STATE_ARMED` state, the
green LED is driven active and the red LED is driven inactive — satisfying the
"Green LED indicates alarm is armed" requirement (DI-002) as implemented by the
LED driver state machine (Spec-001).

## Steps
1. Call `set_led_state(LED_STATE_ARMED)`.
2. Read the last value written to `PIN_RED`.
3. Read the last value written to `PIN_GREEN`.

## Expected behavior
- `PIN_RED` is `LOW`.
- `PIN_GREEN` is `HIGH`.

Automated by: `tests/test_led_driver.c::test_armed_state_lights_green_only`
