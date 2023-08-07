print("Hello World!")
print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.consts import UnicodeMode
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.handlers.sequences import simple_key_sequence
from kmk.extensions.RGB import RGB
from kmk.extensions.media_keys import MediaKeys

keyboard = KMKKeyboard()
layers = Layers()
encoder_handler = EncoderHandler()
keyboard.modules = [layers, encoder_handler]

rgb_ext = RGB(pixel_pin = board.GP16,
              num_pixels=10,
              val_limit=100,
              hue_default=100,
              sat_default=255,
              val_default=79)
keyboard.extensions.append(rgb_ext)
keyboard.extensions.append(MediaKeys())


keyboard.col_pins = (board.GP0,board.GP1, board.GP2, board.GP3)    # try D5 on Feather, keeboar
keyboard.row_pins = (board.GP4, board.GP5, board.GP6, board.GP7, board.GP8)    # try D6 on Feather, keeboar
keyboard.diode_orientation = DiodeOrientation.ROW2COL

encoder_handler.pins = ((board.GP11, board.GP10, board.GP9, False),)


keyboard.tap_time = 250
keyboard.debug_enabled = False



MOMENTARY = KC.MO(1)
MOD_LAYER = KC.LM(1, KC.LSFT)
LAYER_TAP = KC.LT(1, KC.END, prefer_hold=True, tap_interrupted=False, tap_time=250) # any tap longer than 250ms will be interpreted as a hold


LYR_STD, LYR_GAME, LYR_GAMIN = 0, 1, 2 # We got 3 layers which can be switched by pressing the rotary encoder
TO_STD = KC.DF(LYR_STD)
TO_GAME = KC.DF(LYR_GAME)
TO_GAMIN = KC.DF(LYR_GAMIN)

BLANK = KC.KP_DOT
# See https://github.com/KMKfw/kmk_firmware/blob/master/kmk/keys.py for kmk key codes
keyboard.keymap = [
    [BLANK, KC.EQUAL,       KC.KP_ASTERISK, KC.KP_SLASH,
     KC.N7,     KC.N8,          KC.N9,          KC.KP_MINUS,
     KC.N4,     KC.N5,          KC.N6,          KC.KP_PLUS,
     KC.N1,     KC.N2,          KC.N3,          LAYER_TAP ,
     KC.N0,	    KC.KP_DOT,      KC.LABK,        KC.KP_ENTER,
    ],
    [BLANK, KC.LCBR,            KC.RCBR,                    KC.RGB_SAI, # Increases RGB Saturation!
     KC.LBRACKET,   KC.RBRACKET,        KC.MHEN,            KC.RGB_SAD, # Decreases RGB Saturation!
     KC.LPRN,       KC.RPRN,            KC.NO,              KC.NO,
     KC.NO,         KC.LCTL(KC.C),      KC.LCTL(KC.V),      KC.NO,
     KC.NO,         KC.DEL,             KC.RABK,            KC.RGUI,
    ],
    [BLANK, KC.RGB_MODE_SWIRL,            KC.RGB_MODE_KNIGHT,              KC.RGB_MODE_BREATHE_RAINBOW,
     KC.RGB_MODE_RAINBOW,   KC.RGB_MODE_BREATHE,        KC.RGB_MODE_PLAIN,            KC.RGB_MODE_PLAIN,
     KC.RGB_MODE_PLAIN,       KC.RGB_MODE_PLAIN,            KC.RGB_MODE_PLAIN,              KC.RGB_MODE_PLAIN,
     KC.RGB_MODE_PLAIN,       KC.RGB_MODE_PLAIN,            KC.RGB_MODE_PLAIN,              KC.RGB_MODE_PLAIN,
     KC.RGB_MODE_PLAIN,       KC.RGB_MODE_PLAIN,            KC.RGB_MODE_PLAIN,              KC.RGB_MODE_PLAIN,
    ], # KC.RGB_MODE_PLAIN resets animation mode to normal mode
]



encoder_handler.map = [ ((KC.VOLD, KC.VOLU, TO_GAME),), # 1st layer (STD)
                        ((KC.RGB_HUD,    KC.RGB_HUI, TO_GAMIN),), # 2nd layer (GAME)
                        ((KC.RGB_VAD,    KC.RGB_VAI, TO_STD),)] # 3rd layer (GAMIN)

if __name__ == '__main__':
    keyboard.go()
