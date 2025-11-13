#include <ncurses.h>
#include "ui/screen.hpp"
#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/details/os.h>

int main() {
    spdlog::info("Starting Gentifyer...");

    spdlog::set_level(spdlog::level::trace);

    const char* logfile = "gentifyer.log";
    spdlog::info("Initializing logger redirected to {}", logfile);
    auto gentifyer_logger = spdlog::basic_logger_mt("gentifyer_logger", "gentifyer.log");

    spdlog::info("All output will be redirected to {}.", logfile);
    spdlog::set_default_logger(gentifyer_logger);

    auto t = spdlog::details::os::localtime();
    char buffer[64];
    std::strftime(buffer, sizeof(buffer), "%d-%m-%Y %H:%M:%S", &t);
    spdlog::info(" --- New log from launch at {} --- ", buffer);

    // Init ncurses
    spdlog::info("Initializing ncurses...");
    initscr();
    raw();
    noecho();
    keypad(stdscr, TRUE);
    curs_set(0);

    Screen screen = Screen{
        .components = {
            std::string("0"),
            std::string("1"),
            std::string("2"),
            std::string("3"),
            std::string("4"),
            std::string("5"),
            std::string("6"),
            std::string("7"),
            std::string("8"),
            std::string("9"),
            std::string("10"),
            std::string("11"),
            std::string("12"),
            std::string("13"),
            std::string("14"),
            std::string("15"),
            std::string("16"),
            std::string("17"),
            std::string("18"),
            std::string("19"),
            std::string("20"),
            std::string("21"),
            std::string("22"),
            std::string("23"),
            std::string("24"),
            std::string("25"),
            std::string("26"),
            std::string("27"),
            std::string("28"),
            std::string("29"),
            std::string("30"),
            std::string("31")
        }
    };

    handle_screen(screen);

    // Clean up
    endwin();

    return 0;
}
