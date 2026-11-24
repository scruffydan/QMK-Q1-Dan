# Q1 key bindings on the Keychron B1 Pro

The B1 Pro uses the Q1's typing shortcuts on both the Mac and Win layouts.
Use the physical **Mac/Win** switch to select the layout and the connection
switch to select Cable, Bluetooth, or 2.4 GHz.

| Key | Output in both layouts |
| --- | --- |
| Caps Lock | Tap for Escape. Press another key while holding it for Left Ctrl, or hold it alone for 10 seconds. |
| Right Shift | Single tap or hold for Right Shift. Double-tap within 200 ms for Caps Lock. |
| Fn + Left | Single tap for Home. Double-tap within 200 ms for End. |

**Fn + Right** sends End. The keymap uses the function rows and wireless
pairing shortcuts for the selected B1 Pro revision.

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

Use Python 3, West, CMake, Ninja, and a toolchain compatible with Zephyr 3.2.
Zephyr SDK 0.15.2 works on Apple Silicon macOS. You can install West and the
Python dependencies in a virtual environment. For a fresh build, clone the
Keychron fork and apply its bundled 2.4 GHz patch as shown in
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

The build produces `$config/build/zephyr/zmk.uf2`.

## Install and recover

1. Save the stock UF2 for your PID and use **Keymap → Export** in Launcher to
   save your current layers. Export macros separately if you use them.
2. With USB connected and the switches set to **Cable** and **Win**, hold
   **Fn + minus** for three seconds to enter the bootloader. This shortcut
   requires the bootloader assignment in the Win Fn layer. The firmware also
   supports Launcher's bootloader command over USB.
3. Copy the matching UF2 to the `NRF52BOOT` volume. The volume ejects as the
   keyboard reboots. Use the matching stock UF2 in the same way for recovery.
   After restoring stock firmware, import the keymap backup for stock firmware.
   [Keychron's flashing guide](https://www.keychron.com/blogs/archived/how-to-use-the-launcher-web-app-or-manually-flash-firmware-for-your-b-pro-series-keyboard)
4. Reconnect in Launcher and check both layouts. When restoring saved remaps,
   keep the new bindings in the import file. A full import replaces the saved
   layer assignments. Restart the keyboard and check that the assignments stick.

Launcher may display the three bindings as `CUSTOM(64)`, `CUSTOM(65)`,
and `CUSTOM(66)`. Their export codes are `0x7E40` for Caps Lock,
`0x7E41` for Right Shift, and `0x7E42` for Fn + Left. Use each code in
both OS layouts. On the `0x0711` target, preserve code `0x7E03` on **minus**
in the Win Fn layer to keep **Fn + minus** available for recovery. The compiled
default for that slot is transparent.

## Verified hardware

On the ANSI `0x0711` model, all three shortcuts work over USB in both layouts
and over Bluetooth in the Mac layout. The four Launcher layers, including
the saved recovery shortcut, persist across a power cycle. Physical 2.4 GHz
operation and the other hardware revisions remain unverified.

## Test Launcher persistence

With Python packages `pyelftools` and `unicorn` installed, run the following
from the root of this repository. The test runs the built firmware’s Launcher
reset, save, and restore routines with emulated flash storage.

```sh
python3 b1-pro/tests/launcher-roundtrip.py "$config/build/zephyr/zmk.elf"
```
