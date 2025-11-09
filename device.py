from enum import Enum
from pathlib import Path
from size import *
from math import ceil
from pyudev import Context

class DeviceType(Enum):
    SATA_SSD       = 0
    NVMe_SSD       = 1
    HDD            = 2
    REMOVABLE_HDD  = 3
    USB_STORAGE    = 4
    USB_FLASH      = 5
    SD_CARD        = 6
    eMMC_STORAGE   = 7
    OTHER          = 8
    def __str__(self):
        match self:
            case            DeviceType.SATA_SSD:
                return                            "SATA SSD"
            case            DeviceType.NVMe_SSD:
                return                            "NVMe SSD"
            case                 DeviceType.HDD:
                return                            "Hard Disk (HDD)"
            case       DeviceType.REMOVABLE_HDD:
                return                            "Removable HDD"
            case         DeviceType.USB_STORAGE:
                return                            "Removable Storage Device"
            case           DeviceType.USB_FLASH:
                return                            "Removable Flash Device"
            case             DeviceType.SD_CARD:
                return                            "SD Card"
            case        DeviceType.eMMC_STORAGE:
                return                            "eMMC Storage Device"
            case               DeviceType.OTHER:
                return                            "Unknown"

class Device:
    def __init__(self, path: Path, size: int, type: DeviceType):
        self.path: Path       = path
        self.size: int        = size
        self.type: DeviceType = type
    def __str__(self):
        return f"""Device object
        at {self.path}
        size: {self.size} ({self.size / (1024 ** 3)} GiB)
        detected type: {self.type}"""

def block_devices() -> list[Device]:
    context = Context()
    devices = list()
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        device_type = DeviceType.OTHER

        size = int(device.attributes.get('size')) * 512 # 'size' is always in 512-byte sectors, even in 4096-byte disks

        parent = device.find_parent('usb')

        removable = device.attributes.get('removable', None)
        is_removable = removable and int(removable) == 1

        rotational = device.attributes.get('queue/rotational', None)

        if parent:
            if is_removable:
                device_type = DeviceType.USB_FLASH
            else:
                device_type = DeviceType.USB_STORAGE
        elif 'nvme' in device.device_node:
            device_type = DeviceType.NVMe_SSD
        elif rotational is not None:
            if int(rotational) == 1:
                if is_removable:
                    device_type = DeviceType.REMOVABLE_HDD
                else:
                    device_type = DeviceType.HDD
            else:
                device_type = DeviceType.SATA_SSD

        if device.device_node.startswith('/dev/mmcblk'):
            if device.get('ID_DRIVE_FLASH_SD', 0) == "1":
                device_type = DeviceType.SD_CARD
            else:
                device_type = DeviceType.eMMC_STORAGE
            
        devices.append(Device(Path(device.device_node), size, device_type))
    return devices
