# keyboard-firmware

Firmware keymaps for two Keychron keyboards.

- [Keychron Q1](q1/README.md) contains the QMK keymap, configuration, and build rules, with build instructions.
- [Keychron B1 Pro](b1-pro/README.md) contains the ZMK keymap generator, Launcher support, and build and recovery instructions for the Q1-style shortcuts.

## Typing shortcuts

These bindings work in both Mac and Windows layouts.

| Action | Q1 | B1 Pro |
| --- | --- | --- |
| Escape | Tap Caps Lock | Tap Caps Lock |
| Left Ctrl | Hold Caps Lock and press another key, or hold Caps Lock alone for 10 seconds | Hold Caps Lock and press another key, or hold Caps Lock alone for 10 seconds |
| Right Shift | Tap or hold Right Shift | Tap or hold Right Shift |
| Caps Lock | Double-tap Right Shift | Double-tap Right Shift |
| Home | Tap Home | Press Fn + Left |
| End | Double-tap Home | Hold Fn and double-tap Left, or press Fn + Right |

Double-taps use a 200 ms window.

## Keychron Q1

This keymap covers the Q1 v1 and v2 ANSI models with a knob. The physical
Mac/Win switch selects the layout. **Fn + Right Shift** switches layouts in
software until you move the switch or restart the keyboard.

### Function row

| Key | Mac | Win | Win + Fn |
| --- | --- | --- | --- |
| F1 / F2 | Display brightness down / up | F1 / F2 | Display brightness down / up |
| F3 / F4 | Mission Control / Launchpad | F3 / F4 | F3 / F4 |
| F5 / F6 | Keyboard backlight brightness down / up | F5 / F6 | Keyboard backlight brightness down / up |
| F7 / F8 / F9 | Previous track / Play or pause / Next track | F7 / F8 / F9 | Previous track / Play or pause / Next track |
| F10 / F11 / F12 | Mute / Volume down / Volume up | F10 / F11 / F12 | Mute / Volume down / Volume up |

In the Mac layout, hold Fn to send F1–F12. The bottom row before the arrow
keys reads **Ctrl, Option, Command, Space, Command, Fn, Option** in Mac
and **Ctrl, Win, Alt, Space, Alt, Fn, Ctrl** in Win.

### Knob and Fn controls

| Key | Action in both layouts |
| --- | --- |
| Turn knob | Adjust volume |
| Press knob | Mute or unmute audio |
| Fn + turn knob | Adjust keyboard backlight brightness |
| Fn + press knob or Fn + Tab | Toggle keyboard backlight |
| Fn + Q / A | Next / previous lighting effect |
| Fn + W / S | Increase / decrease backlight brightness |
| Fn + E / D | Increase / decrease backlight hue |
| Fn + R / F | Increase / decrease backlight saturation |
| Fn + T / G | Increase / decrease lighting effect speed |
| Fn + Caps Lock | Reset the lighting effect, color, and speed |
| Fn + N | Toggle N-key rollover |
| Fn + left Option (Mac) or left Win (Win) | Toggle the GUI key lock |

See the [Q1 firmware keymap](q1/keymap.c) for all four layers.

## Keychron B1 Pro

The B1 Pro generator applies the typing shortcuts above to the stock keymap
for the selected hardware revision. The physical Mac/Win switch selects the
layout, and the function row and wireless pairing shortcuts follow that
revision's stock keymap. See the [B1 Pro guide](b1-pro/README.md#identify-the-keyboard)
to match your keyboard's USB PID to its revision and layout.

- A single **Fn + Left** tap sends Home after 200 ms. If you release Fn and
  press Left again during that window, Left is sent before Home.
- For recovery, connect over USB, set the switches to **Cable** and **Win**,
  and hold **Fn + minus** for three seconds to enter the bootloader. This
  binding is built into the keymap for all six supported PIDs, and a Launcher
  keymap reset restores it. See [Install and recover](b1-pro/README.md#install-and-recover).
