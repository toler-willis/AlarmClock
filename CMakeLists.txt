cmake_minimum_required(VERSION 3.14)
project(alarm_clock C)

set(CMAKE_C_STANDARD 11)

include(FetchContent)
FetchContent_Declare(
  Unity
  GIT_REPOSITORY https://github.com/ThrowTheSwitch/Unity.git
  GIT_TAG        v2.6.0
)
FetchContent_MakeAvailable(Unity)

enable_testing()

add_executable(test_led_driver
  tests/test_led_driver.c
  led_driver.c
)
target_link_libraries(test_led_driver PRIVATE unity)
target_include_directories(test_led_driver PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

add_test(NAME test_led_driver COMMAND test_led_driver)
