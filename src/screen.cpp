#include <ncurses.h>
#include "ui/screen.hpp"

void draw_on_screen() {
    // Draw the border around the screen
    int rows, cols;
    getmaxyx(stdscr, rows, cols);
    if (rows <= 0 || cols <= 0) return;
    for (int c = 1; c < cols - 1; ++c) {
        mvaddch(0, c, ACS_HLINE);
        mvaddch(rows - 1, c, ACS_HLINE);
    }
    for (int r = 1; r < rows - 1; ++r) {
        mvaddch(r, 0, ACS_VLINE);
        mvaddch(r, cols - 1, ACS_VLINE);
    }
    mvaddch(0, 0, ACS_ULCORNER);
    mvaddch(0, cols - 1, ACS_URCORNER);
    mvaddch(rows - 1, 0, ACS_LLCORNER);
    mvaddch(rows - 1, cols - 1, ACS_LRCORNER);

    // Refresh the screen to show the changes
    refresh();
}
