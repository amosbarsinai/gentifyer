#include <ncurses.h>
#include "ui/screen.hpp"
#include "ui/component.hpp"
#include <variant>
#include <spdlog/spdlog.h>

void draw_border(int width, int height) {
    // Draw corners
    mvaddch(0, 0, ACS_ULCORNER);
    mvaddch(0, width - 1, ACS_URCORNER);
    mvaddch(height - 1, 0, ACS_LLCORNER);
    mvaddch(height - 1, width - 1, ACS_LRCORNER);

    // Draw top and bottom borders
    for (int x = 1; x < width - 1; ++x) {
        mvaddch(0, x, ACS_HLINE);
        mvaddch(height - 1, x, ACS_HLINE);
    }

    // Draw left and right borders
    for (int y = 1; y < height - 1; ++y) {
        mvaddch(y, 0, ACS_VLINE);
        mvaddch(y, width - 1, ACS_VLINE);
    }
}

std::vector<std::string> lines_of(Screen& screen, int width) {
    clear();
    std::vector<std::string> lines;
    size_t text_width = width - 8;
    for (const auto& component : screen.components) {
        if (std::holds_alternative<std::string>(component)) {
            std::string str = std::get<std::string>(component);
            std::vector<std::string> words;
            size_t pos = 0;
            for (size_t i = 0; i <= str.size(); ++i) {
                if (i == str.size() || str[i] == ' ') {
                    words.push_back(str.substr(pos, i - pos));
                    pos = i + 1;
                }
            }
            std::string line;
            for (std::string word : words) {
                if (line.size() + word.size() + 1 > text_width) {
                    lines.push_back(line);
                    line.clear();
                }
                if (!line.empty()) {
                    line += " ";
                }
                line += word;
            }
            if (line.size() > 0) {
                lines.push_back(line);
            }
        }
    }
    return lines;
}

void render_screen(std::vector<std::string> lines, int width, int height, int y_offset) {
    clear();
    for (auto& line : lines) {
        mvprintw(y_offset, 4, "%s", line.c_str());
        y_offset++;
    }

    draw_border(width, height);
    if (lines.size() > static_cast<std::size_t>(height - 2)) {
        std::string scrollmsg = "Use arrow keys to scroll";
        mvaddch(height - 1, (width - scrollmsg.size()) / 2 - 2, ACS_RTEE);
        mvaddch(height - 1, (width - scrollmsg.size()) / 2 - 1, ' ');
        mvaddch(height - 1, (width + scrollmsg.size()) / 2, ' ');
        mvaddch(height - 1, (width + scrollmsg.size()) / 2 + 1, ACS_LTEE);
        mvprintw(height - 1, (width - scrollmsg.size()) / 2, scrollmsg.c_str());
    }
    refresh();
}

void handle_screen(Screen& screen) {
    int width, height;
    getmaxyx(stdscr, height, width);
    int y_offset = 1;
    auto lines = lines_of(screen, width);
    bool running = true;
    while (running) {
        render_screen(lines, width, height, y_offset);
        auto ch = getch();
        if (ch == KEY_DOWN && y_offset > height - 1 - static_cast<int>(lines.size())) {
            y_offset--;
        }
        if (ch == KEY_UP && y_offset < 1) {
            y_offset++;
        }
        // DEBUG - until I add a quit menu
        if (ch == 'b') {
            running = false;
        }
    }
}
