#pragma once
#include "component.hpp"
#include <variant>

struct Screen {
    std::vector<std::variant<std::string, Menu>> components;
};

void handle_screen(Screen& screen);
