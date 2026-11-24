"""Exercise Keychron's Launcher codec in a compiled B1 Pro ELF (pyelftools, unicorn)."""

import argparse
import struct

from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_HOOK_CODE, UC_MODE_MCLASS, UC_MODE_THUMB
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)


class Firmware:
    def __init__(self, elf, storage):
        self.cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB | UC_MODE_MCLASS)
        self.cpu.mem_map(0, 1024 * 1024)
        self.cpu.mem_map(0x20000000, 256 * 1024)
        for segment in elf.iter_segments():
            if segment["p_type"] == "PT_LOAD" and segment["p_filesz"]:
                self.cpu.mem_write(segment["p_vaddr"], segment.data())
        self.symbols = elf.get_section_by_name(".symtab")
        self.storage = storage
        # Only replace the flash storage boundary. Run the firmware's codec,
        # matrix transform, reset, layer save, and restore functions as built.
        for function in ("settings_save_one", "load_immediate_value"):
            address = self.symbol(function)["st_value"] & ~1
            self.cpu.hook_add(UC_HOOK_CODE, self.settings_io, function,
                              begin=address, end=address)

    def symbol(self, name):
        return self.symbols.get_symbol_by_name(name)[0]

    def string(self, address):
        return bytes(self.cpu.mem_read(address, 64)).split(b"\0", 1)[0].decode()

    def settings_io(self, cpu, address, size, function):
        key = self.string(cpu.reg_read(UC_ARM_REG_R0))
        data = cpu.reg_read(UC_ARM_REG_R1)
        length = cpu.reg_read(UC_ARM_REG_R2)
        if function == "settings_save_one":
            self.storage[key] = bytes(cpu.mem_read(data, length))
        else:
            assert len(self.storage[key]) == length
            cpu.mem_write(data, self.storage[key])
        cpu.reg_write(UC_ARM_REG_R0, 0)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    def call(self, function, argument=0):
        stop = 0xFFFF0
        self.cpu.reg_write(UC_ARM_REG_R0, argument)
        self.cpu.reg_write(UC_ARM_REG_SP, 0x2003FF00)
        self.cpu.reg_write(UC_ARM_REG_LR, stop | 1)
        self.cpu.emu_start(self.symbol(function)["st_value"] | 1, stop, count=2000000)
        assert self.cpu.reg_read(UC_ARM_REG_PC) == stop, function
        return self.cpu.reg_read(UC_ARM_REG_R0)

    def bindings(self):
        keymap = self.symbol("zmk_keymap")
        data = self.cpu.mem_read(keymap["st_value"], keymap["st_size"])
        return [(self.string(label), hold, tap)
                for label, hold, tap in struct.iter_unpack("<III", data)]


def check(elf):
    storage = {}
    board = Firmware(elf, storage)
    defaults = board.bindings()
    codes = {
        ("Q1_CTRL_ESCAPE", 0x700E0, 0x70029): 0x7E40,
        ("Q1_SHIFT_CAPS", 0, 0): 0x7E41,
        ("Q1_HOME_END", 0, 0): 0x7E42,
    }
    for binding in codes:
        assert defaults.count(binding) == 2, binding

    board.call("generate_via_keymaps")
    board.call("dynamic_keymap_reset", 0)
    reset = board.bindings()
    for position, binding in enumerate(defaults):
        if binding in codes:
            assert reset[position] == binding, ("reset", position, binding)
    for layer in range(4):
        board.call("via_ee_update_keymap", layer)

    layer_size = len(defaults) // 4
    for index, binding in enumerate(defaults):
        if binding in codes:
            layer, position = divmod(index, layer_size)
            cell = board.call("zmk_matrix_transform_position_to_row_column", position)
            saved = storage[f"via_ee/keymaps/{layer}"]
            assert struct.unpack_from(">H", saved, 2 * cell)[0] == codes[binding]

    # Cycle the three encoded assignments in the saved layers. Changed positions
    # force the next boot to decode each ID instead of retaining compiled defaults.
    bindings = list(codes)
    rotated = dict(zip(bindings, bindings[1:] + bindings[:1]))
    next_code = {codes[old]: codes[new] for old, new in rotated.items()}
    for key, data in storage.items():
        words = [value for value, in struct.iter_unpack(">H", data)]
        storage[key] = b"".join(struct.pack(">H", next_code.get(w, w)) for w in words)

    restarted = Firmware(elf, storage)
    restarted.call("generate_via_keymaps")
    restarted.call("via_ee_read_keymaps")
    restored = restarted.bindings()
    for position, binding in enumerate(defaults):
        assert restored[position] == rotated.get(binding, binding), ("restore", position, binding)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf", nargs="+", help="compiled B1 Pro zmk.elf")
    for path in parser.parse_args().elf:
        with open(path, "rb") as image:
            check(ELFFile(image))
        print(f"Launcher reset and restore passed for {path}")
