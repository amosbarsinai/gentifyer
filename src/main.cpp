#include <ncurses.h>
#include "ui/screen.hpp"

int main() {
    // Init ncurses
    initscr();
    raw();
    noecho();
    keypad(stdscr, TRUE);


    // Clean up
    endwin();

    return 0;
}
