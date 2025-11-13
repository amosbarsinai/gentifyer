#pragma once
#include <string>
#include <vector>

struct MenuOption {
    std::string title;
    std::string id;
    bool selectable = true;
    std::string unselectable;
};

struct Menu {
    std::vector<MenuOption> options;
    std::string title;
    std::string id;
};
