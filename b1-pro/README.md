# Q1 key bindings on the Keychron B1 Pro

The port starts from the stock keymap for your B1 Pro revision. It keeps
the physical Mac/Windows and connection switches, Bluetooth pairing,
and the stock function rows and shortcuts.

| Key | Output in macOS and Windows modes |
| --- | --- |
| Caps Lock | Tap for Escape. Press another key while holding it for Left Ctrl, or hold it alone for 10 seconds. |
| Right Shift | Single tap or hold for Right Shift. Double-tap within 200 ms for Caps Lock. |
| Fn + Left | Single tap for Home. Double-tap within 200 ms for End. |

The **Mac/Win switch** selects the base layout. **Fn + Right** still sends
End. The Q1's RGB controls, knob controls, and software NKRO and GUI-lock
toggles are specific to the Q1 configuration. Keychron's stock Fn shortcuts
remain available on the B1 Pro.

## Identify the keyboard

Connect the keyboard directly over USB in Cable mode. In
[Keychron Launcher](https://launcher.keychron.com/), open **Settings → Device
Info** and read the PID. Use the PID to select the shield, since multiple
hardware revisions share the B1 Pro name. Keychron's
[B Pro firmware guide](https://www.keychron.com/blogs/archived/how-to-use-the-launcher-web-app-or-manually-flash-firmware-for-your-b-pro-series-keyboard)
lists the stock firmware for each PID.

| USB PID | Layout | Shield |
| --- | --- | --- |
| `0x0711` | ANSI | `keychron_b1_us` |
| `0x0712` | ISO | `keychron_b1_uk` |
| `0x0713` | JIS | `keychron_b1_jis` |
| `0x071a` | ANSI | `keychron_b1_usn` |
| `0x071b` | ISO | `keychron_b1_ukn` |
| `0x071c` | JIS | `keychron_b1_jisn` |

The generator supports the six PIDs in this table. Keychron also lists
`0x0714` and `0x0716`, which have no matching target in the source used here.

## Build

Use Python 3, West, and a Zephyr toolchain compatible with the fork's
Zephyr 3.2 base. For a fresh workspace, clone the Keychron fork and apply
its bundled 2.4 GHz patch as shown in
[Keychron's build instructions](https://github.com/Keychron/zmk/tree/c284513085c005edf5f9a52b28c8090cc6ed01d2#readme).

```sh
git clone --branch keychron_bpro https://github.com/Keychron/zmk.git keychron-zmk
cd keychron-zmk
git checkout --detach c284513085c005edf5f9a52b28c8090cc6ed01d2
west init -l app/
west update
git -C zephyr am "$PWD/0001-esb-nrf-fix.patch"
```

From the root of this repository, set `zmk` to the absolute path of your
Keychron checkout and apply the Launcher patch once. It assigns a stable
numeric code to each Q1 behavior so Launcher can save and restore it.

```sh
zmk=/absolute/path/to/keychron-zmk
git -C "$zmk" apply "$PWD/b1-pro/launcher-bindings.patch"
```

Set `pid` to the USB PID you read from the keyboard. The generator selects
the shield and produces its keymap. The build passes that exact file to West.
Run these commands together in the same shell.

```sh
pid=0x0711
config=$(mktemp -d)
keymap=$(python3 b1-pro/prepare-keymap.py --pid "$pid" --zmk "$zmk" --output "$config") &&
    (cd "$zmk" && west build -s app -d "$config/build" -b keychron -- \
        -DSHIELD="$(basename "$keymap" .keymap)" -DKEYMAP_FILE="$keymap" -DZMK_CONFIG="$config")
```

The expected image is `$config/build/zephyr/zmk.uf2`. Save the stock firmware
for the same PID and back up any existing Launcher remaps before flashing.
Launcher can reload earlier saved layer assignments after an update.
Check all three bindings in both OS modes after flashing and after a power
cycle. Also verify USB, Bluetooth, and 2.4 GHz connections.

## Test Launcher persistence

With Python packages `pyelftools` and `unicorn` installed, run the following
from the root of this repository. The test runs the built firmware’s Launcher
reset, save, and restore routines with emulated flash storage.

```sh
python3 b1-pro/tests/launcher-roundtrip.py "$config/build/zephyr/zmk.elf"
```
