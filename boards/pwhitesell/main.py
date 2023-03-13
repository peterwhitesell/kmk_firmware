print("Starting split mode ⌨️~⌨️")

import board
# print(dir(board))

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.modules.pmw3360 import PMW3360
from kmk.modules.split import Split, SplitSide
from kmk.modules.layers import Layers
from kmk.modules.rgbkeys import RGBKeys
from storage import getmount
from kmk.modules.modtap import ModTap
from kmk.modules.tapdance import TapDance
from kmk.utils import Debug
side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

print("split side is:", side)
if side == SplitSide.RIGHT:
  print("~⌨️  RIGHT")
  rgb_pin = board.GP17
  rgb_pixels = 30
else:
  print("LEFT  ⌨~")
  rgb_pin = board.A3
  rgb_pixels = 32

keyboard = KMKKeyboard()
keyboard.debug_enabled = True

keyboard.modules.append(MouseKeys())
keyboard.modules.append(ModTap())
keyboard.modules.append(TapDance())
keyboard.modules.append(Layers())

v = 50
s = 255
rgb = RGB(
  animation_mode=AnimationModes.STATIC_STANDBY,
  pixel_pin=rgb_pin,
  num_pixels=rgb_pixels,
  hue_default=56,
  sat_default=s,
  val_default=v,
  val_limit=v,
)
keyboard.extensions.append(rgb)
keyboard.modules.append(RGBKeys(
  coord_mapping=[
      0 ,   1 ,   2 ,   3 ,   4 ,   5 ,                    37 ,  36 ,  35 ,  34 ,  33 ,  32 ,
     11 ,  10 ,   9 ,   8 ,   7 ,   6 ,                    38 ,  39 ,  40 ,  41 ,  42 ,  43 ,
     12 ,  13 ,  14 ,  15 ,  16 ,  17 ,                    49 ,  48 ,  47 ,  46 ,  45 ,  44 ,
     23 ,  22 ,  21 ,  20 ,  19 ,  18 ,                    50 ,  51 ,  52 ,  53 ,  54 ,  55 ,
                 24 ,  25 ,                                            57 ,  56 ,
                             26 ,  27 ,                          58 ,
                               29 ,  28 ,           59 ,        61 ,
                               30 ,  31 ,                 60 ,
  ],
  split_side=side,
  split_offset=32,
))

keyboard.diode_orientation = DiodeOrientation.ROW2COL
if side == SplitSide.RIGHT:
  keyboard.col_pins = (
    board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7
  )
  keyboard.row_pins = (
    board.GP8,
    board.GP9,
    board.A0,
    board.A1,
    board.A2,
    board.A3,
  )
else:
  keyboard.col_pins = (
    board.GP7, board.GP6, board.GP5, board.GP4, board.GP3, board.GP2
  )
  keyboard.row_pins = (
    board.GP21,
    board.GP23,
    board.GP20,
    board.GP22,
    board.A0,
    board.A1
  )

keyboard.coord_mapping = [
    0,    1,    2,    3,    4,    5,                     36,   37,   38,   39,   40,   41,
    6,    7,    8,    9,    10,   11,                    42,   43,   44,   45,   46,   47,
    12,   13,   14,   15,   16,   17,                    48,   49,   50,   51,   52,   53,
    18,   19,   20,   21,   22,   23,                    54,   55,   56,   57,   58,   59,
                26,    27,                                           62,   63,
                            28,   29,                          61,
                               34,   35,             60,        67,
                                  32,  33,               66,
]
left = (0, 30)
right = (36, 66)

if side == SplitSide.RIGHT:
  pmw3360 = PMW3360(cs=board.GP21, miso=board.GP20, mosi=board.GP23, sclk=board.GP22, invert_x=True, invert_y=True, flip_xy=True)
  keyboard.modules.append(pmw3360)

split = Split(
  split_side=side,
  split_target_left=False,
  uart_flip=True,
  split_flip=False,
  use_pio=True,
  data_pin=board.GP1,
  data_pin2=board.GP0,
)
keyboard.modules.append(split)

_L1_ = KC.RGB(KC.MO(1), hsa=(190, 255, 50))
_L2_ = KC.RGB(KC.MO(2), hsa=(190, 255, 50))
_🚫_ = KC.RGB(KC.NO, hsa=(0, 0, 0))
↓___ = KC.TRNS
__1_ = KC.RGB(KC.N1, hsa=(15, 255, 50))
__2_ = KC.RGB(KC.N2, hsa=(15, 255, 50))
__3_ = KC.RGB(KC.N3, hsa=(15, 255, 50))
__4_ = KC.RGB(KC.N4, hsa=(15, 255, 50))
__5_ = KC.RGB(KC.N5, hsa=(15, 255, 50))
__6_ = KC.RGB(KC.N6, hsa=(15, 255, 50))
__7_ = KC.RGB(KC.N7, hsa=(15, 255, 50))
__8_ = KC.RGB(KC.N8, hsa=(15, 255, 50))
__9_ = KC.RGB(KC.N9, hsa=(15, 255, 50))
__0_ = KC.RGB(KC.N0, hsa=(15, 255, 50))
_TAB = KC.RGB(KC.TAB, hsa=(70, 255, 50))
CTAB = KC.RGB(KC.LCMD(KC.TAB), hsa=(190, 255, 50))
TTAB = KC.RGB(KC.LCMD(KC.GRV), hsa=(195, 255, 50))
__A_ = KC.RGB(KC.A, hsa=(30, 255, 50))
__B_ = KC.RGB(KC.B, hsa=(30, 190, 50))
__C_ = KC.RGB(KC.C, hsa=(30, 190, 50))
__D_ = KC.RGB(KC.D, hsa=(30, 255, 50))
__E_ = KC.RGB(KC.E, hsa=(30, 190, 50))
__F_ = KC.RGB(KC.F, hsa=(30, 255, 50))
__G_ = KC.RGB(KC.G, hsa=(30, 190, 50))
__H_ = KC.RGB(KC.H, hsa=(30, 190, 50))
__I_ = KC.RGB(KC.I, hsa=(30, 190, 50))
__J_ = KC.RGB(KC.J, hsa=(30, 255, 50))
__K_ = KC.RGB(KC.K, hsa=(30, 255, 50))
__L_ = KC.RGB(KC.L, hsa=(30, 255, 50))
__M_ = KC.RGB(KC.M, hsa=(30, 190, 50))
__N_ = KC.RGB(KC.N, hsa=(30, 190, 50))
__O_ = KC.RGB(KC.O, hsa=(30, 190, 50))
__P_ = KC.RGB(KC.P, hsa=(30, 190, 50))
__Q_ = KC.RGB(KC.Q, hsa=(30, 190, 50))
__S_ = KC.RGB(KC.S, hsa=(30, 255, 50))
__R_ = KC.RGB(KC.R, hsa=(30, 190, 50))
__T_ = KC.RGB(KC.T, hsa=(30, 190, 50))
__U_ = KC.RGB(KC.U, hsa=(30, 190, 50))
__V_ = KC.RGB(KC.V, hsa=(30, 190, 50))
__W_ = KC.RGB(KC.W, hsa=(30, 190, 50))
__X_ = KC.RGB(KC.X, hsa=(30, 190, 50))
__Y_ = KC.RGB(KC.Y, hsa=(30, 190, 50))
__Z_ = KC.RGB(KC.Z, hsa=(30, 190, 50))
LALT = KC.RGB(KC.LALT, hsa=(120, 255, 50))
RALT = KC.RGB(KC.RALT, hsa=(120, 255, 50))
SPCE = KC.RGB(KC.SPACE, hsa=(70, 255, 50))
BKSP = KC.RGB(KC.BSPC, hsa=(0, 255, 50))
QUOT = KC.RGB(KC.QUOT, hsa=(40, 255, 50))
SCLN = KC.RGB(KC.SCLN, hsa=(70, 255, 50))
LSFT = KC.RGB(KC.LSFT, hsa=(120, 255, 50))
RSFT = KC.RGB(KC.RSFT, hsa=(120, 255, 50))
RCMD = KC.RGB(KC.RCMD, hsa=(120, 255, 50))
LCMD = KC.RGB(KC.LCMD, hsa=(120, 255, 50))
RCTL = KC.RGB(KC.RCTL, hsa=(120, 255, 50))
LCTL = KC.RGB(KC.LCTL, hsa=(120, 255, 50))
LCLK = KC.RGB(KC.MB_LMB, hsa=(130, 255, 50))
CCLK = KC.RGB(KC.LCMD(KC.MB_LMB), hsa=(135, 255, 50))
RCLK = KC.RGB(KC.MB_RMB, hsa=(130, 255, 50))
ENTR = KC.RGB(KC.ENT, hsa=(70, 255, 50))
CENT = KC.RGB(KC.LCMD(KC.ENT), hsa=(70, 255, 50))
PERD = KC.RGB(KC.DOT, hsa=(40, 255, 50))
COMA = KC.RGB(KC.COMM, hsa=(40, 255, 50))
SLSH = KC.RGB(KC.SLSH, hsa=(40, 255, 50))
__↑_ = KC.RGB(KC.UP, hsa=(150, 255, 50))
__↓_ = KC.RGB(KC.DOWN, hsa=(150, 255, 50))
__←_ = KC.RGB(KC.LEFT, hsa=(150, 255, 50))
__→_ = KC.RGB(KC.RIGHT, hsa=(150, 255, 50))
PGUP = KC.RGB(KC.PGUP, hsa=(150, 255, 50))
PGDN = KC.RGB(KC.PGDN, hsa=(150, 255, 50))
HOME = KC.RGB(KC.HOME, hsa=(150, 255, 50))
_END = KC.RGB(KC.END, hsa=(150, 255, 50))
BKWD = KC.RGB(KC.LALT(KC.LEFT), hsa=(150, 255, 50))
FWWD = KC.RGB(KC.LALT(KC.RIGHT), hsa=(150, 255, 50))
BKLN = KC.RGB(KC.TD(KC.LCMD(KC.LEFT), KC.HOME), hsa=(150, 125, 50))
FWLN = KC.RGB(KC.TD(KC.LCMD(KC.RIGHT), KC.END), hsa=(150, 125, 50))
DLWD = KC.RGB(KC.LALT(KC.BKSP), hsa=(0, 255, 50))
DLLN = KC.RGB(KC.LCMD(KC.BKSP), hsa=(0, 255, 50))
_EQL = KC.RGB(KC.EQL, hsa=(40, 255, 50))
MINS = KC.RGB(KC.MINUS, hsa=(40, 255, 50))
UNDS = KC.RGB(KC.UNDS, hsa=(40, 255, 50))
LCBR = KC.RGB(KC.LCBR, hsa=(40, 255, 50))
RCBR = KC.RGB(KC.RCBR, hsa=(40, 255, 50))
LPRN = KC.RGB(KC.LPRN, hsa=(40, 255, 50))
RPRN = KC.RGB(KC.RPRN, hsa=(40, 255, 50))
LBRC = KC.RGB(KC.LBRC, hsa=(40, 255, 50))
RBRC = KC.RGB(KC.RBRC, hsa=(40, 255, 50))
LABK = KC.RGB(KC.RGB(KC.LABK, (90, 90, 50)), hsa=(40, 255, 50))
RABK = KC.RGB(KC.RABK, hsa=(40, 255, 50))
BSLS = KC.RGB(KC.BSLS, hsa=(40, 255, 50))
COPY = KC.RGB(KC.LCMD(KC.C), hsa=(190, 255, 50))
_CUT = KC.RGB(KC.LCMD(KC.X), hsa=(190, 255, 50))
PAST = KC.RGB(KC.LCMD(KC.V), hsa=(190, 255, 50))
UNDO = KC.RGB(KC.LCMD(KC.Z), hsa=(190, 255, 50))
_ALL = KC.RGB(KC.LCMD(KC.A), hsa=(190, 255, 50))
SAVE = KC.RGB(KC.LCMD(KC.S), hsa=(190, 255, 50))
MTSL = KC.RGB(KC.LCMD(KC.D), hsa=(190, 255, 50))
FIND = KC.RGB(KC.LCMD(KC.F), hsa=(190, 255, 50))
SKSL = KC.RGB(KC.LCMD(KC.K), hsa=(190, 255, 50))
CLOS = KC.RGB(KC.LCMD(KC.W), hsa=(0, 255, 50))
RLOD = KC.RGB(KC.LCMD(KC.R), hsa=(190, 255, 50))
NTAB = KC.RGB(KC.LCMD(KC.T), hsa=(190, 255, 50))
TICK = KC.RGB(KC.GRV, hsa=(60, 255, 50))
ESCP = KC.RGB(KC.ESC, hsa=(0, 255, 50))
DELT = KC.RGB(KC.DEL, hsa=(0, 255, 50))
EMOJ = KC.RGB(KC.LCMD(KC.LCTL(KC.SPACE)), hsa=(190, 255, 50))
_URL = KC.RGB(KC.LCMD(KC.L), hsa=(190, 255, 50))
LNCH = KC.RGB(KC.LCMD(KC.SPACE), hsa=(190, 255, 50))
CLPB = KC.RGB(LCMD(LSFT(KC.V)), hsa=(190, 255, 50))

keyboard.keymap = [[
  ESCP, __1_, __2_, __3_, __4_, __5_,                   __6_, __7_, __8_, __9_, __0_, BKSP,
  _TAB, __Q_, __W_, __E_, __R_, __T_,                   __Y_, __U_, __I_, __O_, __P_, QUOT,
  LSFT, __A_, __S_, __D_, __F_, __G_,                   __H_, __J_, __K_, __L_, SCLN, ENTR,
  LCTL, __Z_, __X_, __C_, __V_, __B_,                   __N_, __M_, COMA, PERD, SLSH, RSFT,
              LALT, LCMD,                                           LCMD, LALT,
                          BKSP, SPCE,                         SPCE,
                             LCLK, _L1_,          LCLK,       _L1_,
                                RCLK, _L2_,              RCLK,
], [
  ↓___, _🚫_, _🚫_, _🚫_, _🚫_, LABK,                   RABK, _🚫_, _🚫_, _🚫_, MINS, DLWD,
  CTAB, ESCP, CLOS, _🚫_, RLOD, NTAB,                   RCBR, _URL, __↑_, _🚫_, _🚫_, TICK,
  ↓___, _ALL, SAVE, MTSL, FIND, LPRN,                   RPRN, __←_, SKSL, __→_, _🚫_, CENT,
  ↓___, UNDO, _CUT, COPY, PAST, LBRC,                   RBRC, MINS, _EQL, UNDS, BSLS, ↓___,
              ↓___, ↓___,                                           ↓___, ↓___,
                          DLWD, ↓___,                         __↓_,
                             LSFT, ↓___,          ↓___,       EMOJ,
                             ↓___, ↓___,                RCLK,
], [
  ↓___, _🚫_, _🚫_, _🚫_, _🚫_, _🚫_,                   _🚫_, _🚫_, _🚫_, _🚫_, _🚫_, DLLN,
  TTAB, __7_, __8_, __9_, __0_, _🚫_,                   _🚫_, _🚫_, PGUP, _🚫_, _🚫_, ↓___,
  ↓___, __4_, __5_, __6_, _🚫_, _🚫_,                   BKLN, BKWD, _🚫_, FWWD, FWLN, ↓___,
  ↓___, __1_, __2_, __3_, CLPB, _🚫_,                   _🚫_, _🚫_, _🚫_, _🚫_, _🚫_, ↓___,
              ↓___, ↓___,                                           ↓___, ↓___,
                          DELT, ↓___,                         PGDN,
                             ↓___, ↓___,          ↓___,       LNCH,
                             LSFT, ↓___,                ↓___,
# ], [
#   ↓___, ↓___, ↓___, ↓___, ↓___, ↓___,                   ↓___, ↓___, ↓___, ↓___, ↓___, ↓___,
#   ↓___, ↓___, ↓___, ↓___, ↓___, ↓___,                   ↓___, ↓___, ↓___, ↓___, ↓___, ↓___,
#   ↓___, ↓___, ↓___, ↓___, ↓___, ↓___,                   ↓___, ↓___, ↓___, ↓___, ↓___, ↓___,
#   ↓___, ↓___, ↓___, ↓___, ↓___, ↓___,                   ↓___, ↓___, ↓___, ↓___, ↓___, ↓___,
#               ↓___, ↓___,                                           ↓___, ↓___,
#                           ↓___, ↓___,                         ↓___,
#                              ↓___, ↓___,          ↓___,       ↓___,
#                              ↓___, ↓___,                ↓___,
]]

if __name__ == '__main__':
  print('starting kmk...')
  keyboard.go()
  print('returned from kmk...')
  