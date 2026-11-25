"""Generate a Q1-style keymap from the matching Keychron B1 Pro keymap."""

import argparse
from pathlib import Path
import re


TARGETS = {
    "0x0711": "b1/us/keychron_b1_us",
    "0x0712": "b1/uk/keychron_b1_uk",
    "0x0713": "b1/jis/keychron_b1_jis",
    "0x071a": "b1n/us/keychron_b1_usn",
    "0x071b": "b1n/uk/keychron_b1_ukn",
    "0x071c": "b1n/jis/keychron_b1_jisn",
}


def layer_bindings(keymap, layer):
    layer_pattern = rf"(\b{layer}\s*\{{\s*bindings\s*=\s*<)([^>]*)(>\s*;)"
    matches = list(re.finditer(layer_pattern, keymap))
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {layer} bindings block")
    return matches[0]


def binding_spans(bindings):
    """Return (start, end, binding) for each binding, ignoring comments."""
    code = re.sub(r"//[^\n]*|/\*.*?\*/", lambda comment: " " * len(comment[0]),
                  bindings, flags=re.DOTALL)
    return [(match.start(), match.end(), " ".join(match[0].split()))
            for match in re.finditer(r"&[^&]*[^&\s]", code)]


def replace_bindings(keymap, layer, replacements):
    block = layer_bindings(keymap, layer)
    bindings = block[2]
    for keycode, behavior in replacements.items():
        pattern = rf"&kp[ \t]+{keycode}(?=\s|$)"
        bindings, count = re.subn(pattern, behavior, bindings)
        if count != 1:
            raise ValueError(f"Expected exactly one {keycode} binding in {layer}")

    return keymap[:block.start(2)] + bindings + keymap[block.end(2):]


BOOTLOADER = "&long_press_bootloader 0 0"


def add_bootloader(keymap, base_layer, fn_layer):
    """Hold Fn + minus for three seconds to enter the bootloader (Launcher code 0x7E03).

    Some targets already assign it; the ANSI and ISO b1 targets leave it transparent.
    """
    base = binding_spans(layer_bindings(keymap, base_layer)[2])
    fn_block = layer_bindings(keymap, fn_layer)
    fn = binding_spans(fn_block[2])
    if len(base) != len(fn):
        raise ValueError(f"{base_layer} and {fn_layer} have different key counts")
    minus = [index for index, (_, _, binding) in enumerate(base) if binding == "&kp MINUS"]
    if len(minus) != 1:
        raise ValueError(f"Expected exactly one MINUS binding in {base_layer}")
    start, end, binding = fn[minus[0]]
    if binding == BOOTLOADER:
        return keymap
    if binding != "&trans":
        raise ValueError(f"Expected &trans on minus in {fn_layer}, found {binding}")
    offset = fn_block.start(2)
    return keymap[:offset + start] + BOOTLOADER + keymap[offset + end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pid", type=str.lower, choices=TARGETS, required=True)
    parser.add_argument("--zmk", type=Path, required=True, help="Keychron ZMK checkout")
    parser.add_argument("--output", type=Path, required=True, help="ZMK config directory")
    args = parser.parse_args()

    target = args.zmk / "app/boards/shields/keychron" / TARGETS[args.pid]
    config = target.with_suffix(".conf")
    keymap_path = target.with_suffix(".keymap")
    try:
        if f"config_usb_device_pid={args.pid}" not in config.read_text().lower().splitlines():
            raise ValueError(f"{config} does not identify itself as PID {args.pid}")
        keymap = keymap_path.read_text()
        for layer in ("default_layer", "layer_two"):
            keymap = replace_bindings(keymap, layer, {
                "CLCK": "&q1_ctrl_escape LCTRL ESC",
                "RSHFT": "&q1_shift_caps 0",
            })
        for layer in ("layer_one", "layer_three"):
            keymap = replace_bindings(keymap, layer, {"HOME": "&q1_home_end 0"})
        keymap = add_bootloader(keymap, "layer_two", "layer_three")

        behaviors = Path(__file__).with_name("q1-behaviors.dtsi").read_text()
        args.output.mkdir(parents=True, exist_ok=True)
        output = args.output / keymap_path.name
        with output.open("x") as generated:
            generated.write(f"{keymap.rstrip()}\n\n{behaviors}")
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(output)


if __name__ == "__main__":
    main()
