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


def replace_bindings(keymap, layer, replacements):
    layer_pattern = rf"(\b{layer}\s*\{{\s*bindings\s*=\s*<)([^>]*)(>\s*;)"
    matches = list(re.finditer(layer_pattern, keymap))
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {layer} bindings block")

    block = matches[0]
    bindings = block[2]
    for keycode, behavior in replacements.items():
        pattern = rf"&kp[ \t]+{keycode}(?=\s|$)"
        bindings, count = re.subn(pattern, behavior, bindings)
        if count != 1:
            raise ValueError(f"Expected exactly one {keycode} binding in {layer}")

    return keymap[:block.start(2)] + bindings + keymap[block.end(2):]


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
