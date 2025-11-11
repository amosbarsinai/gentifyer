from pathlib import Path
from os.path import realpath
from os import getenv
import sys
from platform import architecture
from subprocess import run

# check if arch is 32-bit
if architecture()[0] == '32bit':
    print("Gentifyer currently only supports 64-bit systems.")
    print("Aborting setup.")
    sys.exit(1)

MAGENTA = "\033[35m"
GREEN = "\033[32m"
RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"

def check_dep(name: str, location: Path):
    print(f"{BOLD+MAGENTA}Making sure {name} is installed: ", end='')
    if location.exists():
        print(f"{GREEN}OK{RESET}")
        print(f"{name} located at {realpath(location)}.{RESET}")
    else:
        print(f"{RED}ERROR{RESET}")
        print(f"{name} isn't installed (correctly). Gentifyer won't be able to compile.")
        print(f"{BOLD}Aborting setup.{RESET}")
        sys.exit(1)

print(f"{MAGENTA+BOLD}Setting up Gentifyer...{RESET}")

# check all deps
print(f"{MAGENTA+BOLD}Checking dependencies...{RESET}")
check_dep("C++ Compiler", Path("/usr/bin/g++"))
check_dep("Meson Build System", Path("/usr/bin/meson"))
check_dep("Ninja Build System", Path("/usr/bin/ninja"))
check_dep("Ncurses library", Path("/lib64/libncurses.so"))
print(f"{GREEN+BOLD}All dependencies are satisfied!{RESET}")

# compile and install Gentifyer
print(f"{MAGENTA+BOLD}Compiling and installing Gentifyer...{RESET}")
if not Path("./builddir").exists():
    try:
        run(["meson", "setup", "builddir"], check=True)
    except Exception as e:
        with open("setup_error.log", "w") as f:
            f.write(str(e))
        print(f"{RED+BOLD}Failed to set up Meson build directory. See setup_error.log for details.{RESET}")
        print(f"{BOLD}Aborting setup.{RESET}")
        sys.exit(1)
try:
    run(["meson", "compile", "-C", "builddir"], check=True)
except Exception as e:
    with open("setup_error.log", "w") as f:
        f.write(str(e))
    print(f"{RED+BOLD}Failed to compile Gentifyer. See setup_error.log for details.{RESET}")
    print(f"{BOLD}Aborting setup.{RESET}")
    sys.exit(1)
try:
    run(["sudo", "meson", "install", "-C", "builddir"], check=True)
except Exception as e:
    with open("setup_error.log", "w") as f:
        f.write(str(e))
    print(f"{RED+BOLD}Failed to install Gentifyer. See setup_error.log for details.{RESET}")
    print(f"{MAGENTA+BOLD}You might need to run this script with elevated privileges (e.g., using sudo).")
    print(f"However, Gentifyer has already been compiled and can be found in ./builddir/gentifyer. You can run it directly from there without installation.{RESET}")
    print(f"{BOLD}Aborting setup.{RESET}")
    sys.exit(1)

if "/usr/local/bin" not in getenv("PATH", ""):
    print(f"{MAGENTA+BOLD}Note: /usr/local/bin is not in your PATH environment variable.")
    print(f"You may need to add it to run Gentifyer from anywhere.{RESET}")
print(f"{GREEN+BOLD}Gentifyer has been successfully installed! You can run it using the command 'gentifyer'.{RESET}")
