# Gentifyer - ASCII Gentoo Linux Installer

A terminal-based installer for Gentoo Linux with an ASCII interface that simplifies the installation process while maintaining the flexibility and control that Gentoo users expect.

## Features

- 🖥️ ASCII-based user interface for a classic terminal experience
- 💾 Automated disk partitioning with customizable options
- 🔧 Dynamic system configuration
- 📦 Profile and USE flag selection
- 🚀 Streamlined installation process
- 🔒 UEFI-only support (sorry)
- 🛠️ Advanced partitioning options

## Prerequisites

- A working Linux environment (Live USB/CD)
- Internet connection
- Minimum 8GB RAM recommended
- At least 30GB free disk space
- Basic understanding of Gentoo Linux concepts

## Installation

1. Boot into a Linux live environment
2. Download the installer:
   ```bash
   git clone https://github.com/amosbarsinai/gentifyer.git
   cd gentifyer
   ```
3. Run the Gentifyer setup:
   ```bash
   python setup.py
   ```
4. To run the installer, you can just run:
   ```bash
   gentifyer
   ```

## Usage

The installer will guide you through the following steps:

1. Disk selection and partitioning
2. File system configuration
3. Base system installation
4. Kernel setup (compilation or download)
5. System configuration
   - Timezone setting
   - Locale configuration
   - Network setup
6. Bootloader installation

Use arrow keys to navigate through menus and follow the on-screen instructions.

## Configuration Options

- Custom partition layouts
- Multiple file system options
- Profile selection
- USE flag customization
- Network configuration
- System locale and timezone
- Bootloader options

## Contributing

Contributions are welcome! Please feel free to submit a PR.

## License

This project is licensed under the Unlicense - see the LICENSE file for details.
