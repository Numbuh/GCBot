cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)

project(shinybot)
pico_sdk_init()

add_executable(shinybot
    main.cpp
    controller.cpp
)

target_link_libraries(shinybot pico_stdlib)
pico_add_extra_outputs(shinybot)
