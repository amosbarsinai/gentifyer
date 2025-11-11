#include <ncurses.h>
#include "ui/screen.hpp"

int main() {
    // Init ncurses
    initscr();
    raw();
    noecho();
    keypad(stdscr, TRUE);
    curs_set(0);

    draw_on_screen();
    getch();

    // Clean up
    endwin();

    return 0;
}
