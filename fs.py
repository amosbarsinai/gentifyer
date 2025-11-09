from zfsinfo import zfs_info
from enum import Enum

class Filesystem(Enum):
    EXT4 = 0
    BTRFS = 1
    XFS = 2
    VFAT = 3

    def min_root_size(self) -> int:
        match self:
            case Filesystem.EXT4:
                return 2 ** 16            # 64 KiB
            case Filesystem.BTRFS:
                return 114294784         # 872 MiB
            case Filesystem.XFS:
                return 1024 ** 2 * 300   # 300 MiB

    def __str__(self):
        match self:
            case Filesystem.EXT4:
                return "Ext4"
            case Filesystem.BTRFS:
                return "Btrfs"
            case Filesystem.ZFS:
                return "Z Filesystem"
            case Filesystem.XFS:
                return "X Filesystem"
            case Filesystem.VFAT:
                return "Virtual FAT"
