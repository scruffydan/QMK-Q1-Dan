/* Copyright 2021 @ Keychron (https://www.keychron.com)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include QMK_KEYBOARD_H
//#include "keychron_common.h"

//Custom Keycodes
enum custom_keycodes {
    RGB_RESET = SAFE_RANGE,
//  Other keycodes
    //example1,
};

//Tap Dance Declarations
enum {
    TD_RSFT_CAPS,
    TD_HOME_END,
};



bool process_record_user(uint16_t keycode, keyrecord_t* record) {
    switch (keycode) {
        case RGB_RESET:  // Sets the RGB Matrix mode back to the default.
                         // This should match values in the config.h file
            if (record->event.pressed) {
                rgb_matrix_mode(RGB_MATRIX_ALPHAS_MODS);
                rgb_matrix_sethsv(21, 255, 255);
                rgb_matrix_set_speed(235);
            }
          return false;
        // Other macros
      }
    return true;
}

//Tap Dance Definitions
tap_dance_action_t tap_dance_actions[] = {
    //Tap once for Right Shift, twice for Caps Lock
    [TD_RSFT_CAPS] = ACTION_TAP_DANCE_DOUBLE(KC_RSFT, KC_CAPS),
    //Tap once for Home, twice for End
    [TD_HOME_END] = ACTION_TAP_DANCE_DOUBLE(KC_HOME, KC_END),
};



// Setup Custom tapping terms
uint16_t get_tapping_term(uint16_t keycode, keyrecord_t *record) {
    switch (keycode) {
        case LCTL_T(KC_ESC):
            return  10000;
        default:
            return TAPPING_TERM;
    }
};


enum layers{
    MAC_BASE,
    MAC_FN,
    WIN_BASE,
    WIN_FN
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [MAC_BASE] = LAYOUT_ansi_82(
        KC_ESC,          KC_BRID,  KC_BRIU,  KC_MCTL,  KC_LPAD,  RGB_VAD,  RGB_VAI,  KC_MPRV,  KC_MPLY,  KC_MNXT,  KC_MUTE,  KC_VOLD,   KC_VOLU,   KC_DEL,             KC_MUTE,
        KC_GRV,          KC_1,     KC_2,     KC_3,     KC_4,     KC_5,     KC_6,     KC_7,     KC_8,     KC_9,     KC_0,     KC_MINS,   KC_EQL,    KC_BSPC,            KC_PGUP,
        KC_TAB,          KC_Q,     KC_W,     KC_E,     KC_R,     KC_T,     KC_Y,     KC_U,     KC_I,     KC_O,     KC_P,     KC_LBRC,   KC_RBRC,   KC_BSLS,            KC_PGDN,
        LCTL_T(KC_ESC),  KC_A,     KC_S,     KC_D,     KC_F,     KC_G,     KC_H,     KC_J,     KC_K,     KC_L,     KC_SCLN,  KC_QUOT,              KC_ENT,             TD(TD_HOME_END),
        KC_LSFT,         KC_Z,     KC_X,     KC_C,     KC_V,     KC_B,     KC_N,     KC_M,     KC_COMM,  KC_DOT,   KC_SLSH,             TD(TD_RSFT_CAPS),    KC_UP,
        KC_LCTL,         KC_LOPT,  KC_LCMD,                                KC_SPC,                                 KC_RCMD,  MO(MAC_FN),KC_ROPT,   KC_LEFT,  KC_DOWN,  KC_RGHT),

    [MAC_FN] = LAYOUT_ansi_82(
        _______,            KC_F1,    KC_F2,    KC_F3,    KC_F4,    KC_F5,    KC_F6,    KC_F7,    KC_F8,    KC_F9,    KC_F10,   KC_F11,   KC_F12,        _______,  RGB_TOG,
        _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,                 _______,
        RGB_TOG,  RGB_MOD,  RGB_VAI,  RGB_HUI,  RGB_SAI,  RGB_SPI,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,                 _______,
        RGB_RESET,RGB_RMOD, RGB_VAD,  RGB_HUD,  RGB_SAD,  RGB_SPD,  _______,  _______,  _______,  _______,  _______,  _______,            _______,                 _______,
        _______,            _______,  _______,  _______,  _______,  _______,  NK_TOGG,  _______,  _______,  _______,  _______,            TG(WIN_BASE),  _______,
        _______,  GU_TOGG,  _______,                                _______,                                _______,  _______,  _______,  _______,       _______,  _______),

    [WIN_BASE] = LAYOUT_ansi_82(
        KC_ESC,          KC_F1,    KC_F2,    KC_F3,    KC_F4,    KC_F5,    KC_F6,    KC_F7,    KC_F8,    KC_F9,    KC_F10,   KC_F11,    KC_F12,    KC_DEL,             KC_MUTE,
        KC_GRV,          KC_1,     KC_2,     KC_3,     KC_4,     KC_5,     KC_6,     KC_7,     KC_8,     KC_9,     KC_0,     KC_MINS,   KC_EQL,    KC_BSPC,            KC_PGUP,
        KC_TAB,          KC_Q,     KC_W,     KC_E,     KC_R,     KC_T,     KC_Y,     KC_U,     KC_I,     KC_O,     KC_P,     KC_LBRC,   KC_RBRC,   KC_BSLS,            KC_PGDN,
        LCTL_T(KC_ESC),  KC_A,     KC_S,     KC_D,     KC_F,     KC_G,     KC_H,     KC_J,     KC_K,     KC_L,     KC_SCLN,  KC_QUOT,              KC_ENT,             TD(TD_HOME_END),
        KC_LSFT,         KC_Z,     KC_X,     KC_C,     KC_V,     KC_B,     KC_N,     KC_M,     KC_COMM,  KC_DOT,   KC_SLSH,             TD(TD_RSFT_CAPS),    KC_UP,
        KC_LCTL,         KC_LWIN,  KC_LALT,                                KC_SPC,                                 KC_RALT,  MO(WIN_FN),KC_RCTL,   KC_LEFT,  KC_DOWN,  KC_RGHT),

    [WIN_FN] = LAYOUT_ansi_82(
        _______,            KC_BRID,  KC_BRIU,  _______,  _______,  RGB_VAD,  RGB_VAI,  KC_MPRV,  KC_MPLY,  KC_MNXT,  KC_MUTE,  KC_VOLD,  KC_VOLU,       _______,  RGB_TOG,
        _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,                 _______,
        RGB_TOG,  RGB_MOD,  RGB_VAI,  RGB_HUI,  RGB_SAI,  RGB_SPI,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,                 _______,
        RGB_RESET,RGB_RMOD, RGB_VAD,  RGB_HUD,  RGB_SAD,  RGB_SPD,  _______,  _______,  _______,  _______,  _______,  _______,            _______,                 _______,
        _______,            _______,  _______,  _______,  _______,  _______,  NK_TOGG,  _______,  _______,  _______,  _______,            TO(MAC_BASE),  _______,
        _______,  GU_TOGG,  _______,                                _______,                                _______,  _______,  _______,  _______,       _______,  _______)

};

#if defined(ENCODER_MAP_ENABLE)
const uint16_t PROGMEM encoder_map[][NUM_ENCODERS][NUM_DIRECTIONS] = {
    [MAC_BASE] = { ENCODER_CCW_CW(KC_VOLD, KC_VOLU) },
    [MAC_FN]   = { ENCODER_CCW_CW(RGB_VAD, RGB_VAI) },
    [WIN_BASE] = { ENCODER_CCW_CW(KC_VOLD, KC_VOLU) },
    [WIN_FN]   = { ENCODER_CCW_CW(RGB_VAD, RGB_VAI) },
};
#endif


// RGB Indicator Settings
bool rgb_matrix_indicators_advanced_user(uint8_t led_min, uint8_t led_max) {
    // Set Caps Lock indicator for non-modifier keys
    if (host_keyboard_led_state().caps_lock) {
        for (uint8_t i = led_min; i < led_max; i++) {
            if (g_led_config.flags[i] & LED_FLAG_KEYLIGHT) {
                rgb_matrix_set_color(i, RGB_RED);
            }
        }
    }


    for (uint8_t i = led_min; i < led_max; i++) {
        // Layer indicator
        switch(get_highest_layer(layer_state|default_layer_state)) {
            case WIN_BASE:
            case WIN_FN:
                rgb_matrix_set_color(72, RGB_WHITE);
                rgb_matrix_set_color(73, RGB_WHITE);
                rgb_matrix_set_color(74, RGB_WHITE);
                rgb_matrix_set_color(76, RGB_WHITE);
                rgb_matrix_set_color(77, RGB_WHITE);
                rgb_matrix_set_color(78, RGB_WHITE);
                break;
            default:
                break;
        }

    // Setup indicator for Fn Layers  with configured keycodes
    if (get_highest_layer(layer_state) > 0  &&
        // Exclude any non-default Layers Eg. WIN_BASE
        get_highest_layer(layer_state) != WIN_BASE) {
        uint8_t layer = get_highest_layer(layer_state);
        for (uint8_t row = 0; row < MATRIX_ROWS; ++row) {
            for (uint8_t col = 0; col < MATRIX_COLS; ++col) {
                uint8_t index = g_led_config.matrix_co[row][col];
                if (index >= led_min && index < led_max && index != NO_LED &&
                keymap_key_to_keycode(layer, (keypos_t){col,row}) > KC_TRNS) {
                    // This is where we set the color
                    rgb_matrix_set_color(index, RGB_BLUE);
                }
            }
        }
    }

    }
    return false;
};