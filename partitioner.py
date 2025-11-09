from device import Device
from size import MiB, GiB
from math import ceil

def auto_part(device: Device, swap: bool, mem: int) -> tuple[int, int]:
    # Get the device's size
    size = device.size
    # GPT uses 1 MiB at each end of the disk
    size -= 2 * MiB
    # Boot
    # Assume EFI - Linux systems support both anyway
    # How much do we want to give EFI? That depends -
    # My /efi directory, for example, is tiny - it uses 300KiB out of the 1GiB I gave it - and I use a locally configured and compiled Gentoo kernel.
    # The Fedora Anaconda installer gives /boot/efi 600 MiB, and the Ubuntu 24 installer gives it 1 GiB.
    # I decided to go somewhere in between - 512MiB.
    efi_p = 512 * MiB

    # Swap
    # How much swap do we want?
    # According to a (slightly old) rule of thumb:
    # - Swap size of systems with under 4 GiB of memory should be two times the memory size
    # - Swap size of systems with 4 GiB < memory < 16 GiB should be memory size (1:1)
    # - Swap size of systems with memory > 16 GiB should be min(memory, disk size / 4)
    if swap or swap == None: # if swap is None, it's not forced - we can shrink it later to make more room for the disk if we need
        if mem < 4 * GiB:
            swap_p = 2 * mem
        elif 4 * GiB < mem <= 16 * GiB:
            swap_p = mem
        elif 16 * GiB < mem:
            swap_p = min(size / 4, mem)
    swap_p = ceil(swap_p * GiB) / GiB

    # It's a bad idea to install Gentoo with less than 16 GiB on the root partition, and an even worse one to automate doing that with an installer.
    # The device menu should automatically make entries with <16GiB unselectable, but if this script is run independently we should do this anyway
    if size - efi_p - swap_p < 16 * GiB:
        # Let's see if we can shrink swap
        if swap: # swap is forced
            return
        elif swap == None:
            if size - efi_p >= 16 * GiB: # we can shrink swap so the disk will be large enough to install
                swap_p -= 16 * GiB - (size - efi_p) # take the difference between what's left for root and 16 GiB and subtract it from swap
            else:
                return
    
    return (efi_p, swap_p)  # Since we measure this in bytes and not sectors, and GPT doesn't take up exactly one megabyte 
                            # at each side (34 sectors on 512-phys and 6 sectors on 4096-phys), we don't return the root partition
                            # size - we just give it straight to libparted and tell it to fill the rest of the disk. The error
                            # margin here is, in the worst case, 1MiB of sectors (optimal alignment, and it's not half that because at the
                            # start of the disk we can't just snap to the closest OA - again, 34 or 6 sectors at the start are GPT),
                            # which is negligible in any disk that's big enough for this function to format.
