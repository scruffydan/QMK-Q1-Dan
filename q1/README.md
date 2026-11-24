# Keychron Q1 keymap

This QMK keymap is for the Keychron Q1 ANSI model with a knob, version 1 or
version 2. It needs QMK 0.27.0 or later, which added the `RM_*` RGB Matrix
keycodes. Keychron's own QMK fork does not have them.

| Key | Output |
| --- | --- |
| Caps Lock | Tap for Escape. Press another key while holding it for Left Ctrl, or hold it alone for 10 seconds. |
| Right Shift | Single tap or hold for Right Shift. Double-tap within 200 ms for Caps Lock. |
| Home | Single tap for Home. Double-tap within 200 ms for End. |
| Fn + Right Shift | Switch between the Mac and Win layouts until the keyboard restarts. |

Caps Lock gives Ctrl only once you press another key, so Ctrl + mouse click
does not work with it. Use Left Ctrl instead.

The **Mac/Win** switch sets the layout when the keyboard starts and whenever
you move it. In the Win layout the bottom-row modifiers light white. Holding
Fn lights the keys that have an Fn assignment blue.

## Build

Copy `keymap.c`, `config.h`, and `rules.mk` into a new keymap directory in
your QMK checkout, then build for your board. For a version 2 board:

```sh
keymap=$HOME/qmk_firmware/keyboards/keychron/q1v2/ansi_encoder/keymaps/dan
mkdir -p "$keymap" && cp q1/keymap.c q1/config.h q1/rules.mk "$keymap"
qmk compile -kb keychron/q1v2/ansi_encoder -km dan
```

For a version 1 board, use `keychron/q1v1/ansi_encoder` in both places.
