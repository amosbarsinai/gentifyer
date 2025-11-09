import device as device
from size import GiB
import screen
import os

def do_partitioning_screen():
    devs = device.block_devices()
    dev_options: list[screen.Menu.MenuOption] = list()

    for dev in devs:
        id = dev.path
        name = f"{id}: {int(dev.size / GiB)} GiB {dev.type}"
        selectable = True
        unselectable = None
        if not os.access(dev.path, os.W_OK):
            selectable = False
            unselectable = "insufficient permissions"
        if dev.size < 16 * GiB: # partitioner shouldn't let you do this anyway
            selectable = False
            unselectable = "not big enough: <16GiB"
        dev_options.append(
            screen.Menu.MenuOption(
                id, name, selectable, unselectable
            )
        )

    dev_options.append(
        screen.Menu.MenuOption(
            "r",
            "Refresh disks - if you just plugged one in",
            True,
            None,
            True
        )
    )

    choose_dev: screen.Screen = screen.Screen(
        "Choose a block device",
        [
            screen.TextBlock("It is highly recommended to install Gentoo on a single block device. That's usually your disk (/dev/sda in most cases), \
    but you can install Gentoo on anything with more than 16 GiB of storage."),
            screen.Menu(
                "bdev",
                "Choose a block device from the following:",
                dev_options
            )
        ]
    )

    return screen.screen_loop_wrapper(choose_dev)

while do_partitioning_screen() == "r":
    pass
