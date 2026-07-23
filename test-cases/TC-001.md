---
itemId: LED-TC-001
itemType: Test Case
itemTitle: Red LED Off-State Verification
itemTests:
  - KXITM55BPSD4PVF8N1VHFN1EM55KKCZ  # DI-001: Red LED Indicates Alarm Off
  - KXITM4BJ1RTM5GQ8JXSB9Z37D5S9BWN  # Spec-001: LED Driver state machine
---

# LED-TC-001: Red LED Off-State Verification

Verifies that when the LED driver is placed in the `LED_STATE_OFF` state, the red
LED is driven active and the green LED is driven inactive — satisfying the
"Red LED indicates alarm off" requirement (DI-001) as implemented by the LED
driver state machine (Spec-001).

## Steps
1. Call `set_led_state(LED_STATE_OFF)`.
2. Read the last value written to `PIN_RED`.
3. Read the last value written to `PIN_GREEN`.

## Expected behavior
- `PIN_RED` is `HIGH`.
- `PIN_GREEN` is `LOW`.

Automated by: `tests/test_led_driver.c::test_off_state_lights_red_only`
This is a change to force a commit refresh
