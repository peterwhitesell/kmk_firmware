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
from kmk.modules.capsword import CapsWord
from kmk.modules.oneshot import OneShot
from kmk.modules.rgbkeys import RGBKeys, Color
from storage import getmount
from kmk.modules.holdtap import HoldTap
from kmk.modules.tapdance import TapDance
from kmk.utils import Debug
side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

print("split side is:", side)
if side == SplitSide.RIGHT:
  print("~⌨️  RIGHT")
  # rgb_pin = board.GP17
  rgb_pin = board.GP8
  rgb_pixels = 24
else:
  print("LEFT  ⌨~")
  rgb_pin = board.A3
  rgb_pixels = 26

keyboard = KMKKeyboard()
keyboard.debug_enabled = True

keyboard.modules.append(MouseKeys())
keyboard.modules.append(HoldTap())

td = TapDance()
# td.tap_time = 750
keyboard.modules.append(td)
keyboard.modules.append(OneShot())
layers = Layers()
keyboard.modules.append(layers)

capsWord = CapsWord(timeout=5000)
keyboard.modules.append(capsWord)
keyboard.diode_orientation = DiodeOrientation.ROW2COL
if side == SplitSide.RIGHT:
  keyboard.col_pins = (
    board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7
  )
  keyboard.row_pins = (
    # board.GP8,
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
    # board.GP21,
    board.GP23,
    board.GP20,
    board.GP22,
    board.A0,
    board.A1
  )

keyboard.coord_mapping = [
     0,    1,    2,    3,    4,    5,                    30,   31,   32,   33,   34,   35,
     6,    7,    8,    9,   10,   11,                    36,   37,   38,   39,   40,   41,
    12,   13,   14,   15,   16,   17,                    42,   43,   44,   45,   46,   47,
                20,    21,                                           50,   51,
                            22,   23,                          49,
                               28,   29,             48,        55,
                                  26,  27,               54,
]

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

_L1_ = KC.MO(1)
SP_1 = KC.HT(KC.SPACE, KC.MO(1), tap_time=200)
SPC1 = KC.HT(KC.SPACE, KC.MO(1), tap_time=200)
_L2_ = KC.MO(2)
L1L2 = KC.TD(_L1_, _L2_)
_L3_ = KC.MO(3)
_L4_ = KC.MO(4)
_🚫_ = KC.NO
↓___ = KC.TRNS
__1_ = KC.N1
__2_ = KC.N2
__3_ = KC.N3
__4_ = KC.N4
__5_ = KC.N5
__6_ = KC.N6
__7_ = KC.N7
__8_ = KC.N8
__9_ = KC.N9
__0_ = KC.N0
_1__ = KC.N1
_2__ = KC.N2
_3__ = KC.N3
_4__ = KC.N4
_5__ = KC.N5
_6__ = KC.N6
_7__ = KC.N7
_8__ = KC.N8
_9__ = KC.N9
_0__ = KC.N0
_TAB = KC.TAB
CTAB = KC.LCMD(KC.TAB)
TTAB = KC.LCMD(KC.GRV)
__A_ = KC.A
__B_ = KC.B
__C_ = KC.C
__D_ = KC.D
__E_ = KC.E
__F_ = KC.F
__G_ = KC.G
__H_ = KC.H
__I_ = KC.I
__J_ = KC.J
__K_ = KC.K
__L_ = KC.L
__M_ = KC.M
__N_ = KC.N
__O_ = KC.O
__P_ = KC.P
__Q_ = KC.Q
__S_ = KC.S
__R_ = KC.R
__T_ = KC.T
__U_ = KC.U
__V_ = KC.V
__W_ = KC.W
__X_ = KC.X
__Y_ = KC.Y
__Z_ = KC.Z
LALT = KC.LALT
RALT = KC.RALT
SPCE = KC.SPACE
BKSP = KC.BSPC
QUOT = KC.QUOT
SCLN = KC.SCLN
EXLM = KC.EXLM
LSFT = KC.TD(KC.HT(KC.OS(KC.LSFT, tap_time=None), KC.LSFT), KC.CW)
RSFT = KC.TD(KC.HT(KC.OS(KC.RSFT, tap_time=None), KC.RSFT), KC.CW)
RCMD = KC.RCMD
LCMD = KC.LCMD
RCTL = KC.RCTL
LCTL = KC.LCTL
LCLK = KC.MB_LMB
CCLK = KC.LCMD(KC.MB_LMB)
RCLK = KC.MB_RMB
ENTR = KC.ENT
CENT = KC.LCMD(KC.ENT)
PERD = KC.DOT
COMA = KC.COMM
SLSH = KC.SLSH
__↑_ = KC.UP
__↓_ = KC.DOWN
__←_ = KC.LEFT
__→_ = KC.RIGHT
PGUP = KC.PGUP
PGDN = KC.PGDN
HOME = KC.HOME
_END = KC.END
BKWD = KC.LALT(KC.LEFT)
FWWD = KC.LALT(KC.RIGHT)
BKLN = KC.LCMD(KC.LEFT)
FWLN = KC.LCMD(KC.RIGHT)
DLWD = KC.LALT(KC.BKSP)
DLLN = KC.LCMD(KC.BKSP)
_EQL = KC.EQL
MINS = KC.MINUS
UNDS = KC.UNDS
LCBR = KC.LCBR
RCBR = KC.RCBR
LPRN = KC.LPRN
RPRN = KC.RPRN
LBRC = KC.LBRC
RBRC = KC.RBRC
LABK = KC.LABK
RABK = KC.RABK
BSLS = KC.BSLS
COPY = KC.LCMD(KC.C)
_CUT = KC.LCMD(KC.X)
PAST = KC.LCMD(KC.V)
UNDO = KC.LCMD(KC.Z)
_ALL = KC.LCMD(KC.A)
SAVE = KC.LCMD(KC.S)
MTSL = KC.LCMD(KC.D)
FIND = KC.LCMD(KC.F)
SKSL = KC.LCMD(KC.K)
CLOS = KC.LCMD(KC.W)
RLOD = KC.LCMD(KC.R)
NTAB = KC.LCMD(KC.T)
TICK = KC.GRV
ESCP = KC.ESC
DELT = KC.DEL
EMOJ = KC.LCMD(KC.LCTL(KC.SPACE))
_URL = KC.LCMD(KC.L)
LNCH = KC.LCMD(KC.SPACE)
CLPB = KC.LCMD(KC.LSFT(KC.V))
CMNT = KC.LCMD(KC.SLSH)
PRNT = KC.LCMD(KC.P)
PTSC = KC.LCMD(KC.LSFT(KC.N4))
VDSC = KC.LCMD(KC.LSFT(KC.N5))
OPEN = KC.LCMD(KC.O)
NEW_ = KC.LCMD(KC.N)
CMCT = KC.LCMD(KC.LCTL)
MSSN = KC.LCTL(KC.UP)
APPN = KC.LCTL(KC.DOWN)

class WordsTimeout():
  words_timeout = None
  keyboard = None
  def __init__(self, keyboard):
    self.keyboard = keyboard
  def words(self, key, keyboard, *args):
    if self.words_timeout is not None:
      keyboard.cancel_timeout(self.words_timeout)
      layers._mo_released(_L4_, keyboard)
    layers._mo_pressed(_L4_, keyboard) # TODO dont use internal methods
    self.words_timeout = keyboard.set_timeout(
      300,
      lambda: layers._mo_released(_L4_, keyboard) # TODO dont use internal methods
    )
    return key
wt = WordsTimeout(keyboard)
for k in [ KC.A, KC.B, KC.C, KC.D, KC.E, KC.F, KC.G, KC.H, KC.I, KC.J, KC.K, KC.L, KC.M, KC.N, KC.O, KC.P, KC.Q, KC.S, KC.R, KC.T, KC.U, KC.V, KC.W, KC.X, KC.Y, KC.Z]:
  k.after_press_handler(wt.words)

def ball_scroll_enable(key, keyboard, *args):
    pmw3360.start_v_scroll()
    return True

def ball_scroll_disable(key, keyboard, *args):
    pmw3360.start_v_scroll(False)
    return True

if side == SplitSide.RIGHT:
  SP_1.before_press_handler(ball_scroll_enable)
  SP_1.before_release_handler(ball_scroll_disable)

rgb = RGB(
  animation_mode=AnimationModes.STATIC_STANDBY,
  pixel_pin=rgb_pin,
  num_pixels=rgb_pixels,
  hue_default=56,
  sat_default=255,
  val_default=0,
  val_limit=255,
)
keyboard.extensions.append(rgb)
rgbkeys = RGBKeys(
  coord_mapping=[
      5,    4,    3,    2,    1,    0,                     26,   27,   28,   29,   30,   31,
      6,    7,    8,    9,   10,   11,                     37,   36,   35,   34,   33,   32,
     17,   16,   15,   14,   13,   12,                     38,   39,   40,   41,   42,   43,
                  18,   19,                                             45,   44,
                              20,   21,                           46,
                                23,   22,            47,         49,
                                24,   25,                  48,
  ],
  key_colors = {
    _🚫_: Color(v=0),
    _L1_: Color(h=190),
    L1L2: Color(h=190),
    _L2_: Color(h=190),
    _L3_: Color(h=190),
    __1_: Color(h=15),
    __2_: Color(h=15),
    __3_: Color(h=15),
    __4_: Color(h=15),
    __5_: Color(h=15),
    __6_: Color(h=15),
    __7_: Color(h=15),
    __8_: Color(h=15),
    __9_: Color(h=15),
    __0_: Color(h=15),
    _TAB: Color(h=70),
    CTAB: Color(h=190),
    TTAB: Color(h=195),
    __A_: Color(h=30),
    __B_: Color(h=30, s=200, v=150),
    __C_: Color(h=30, s=200, v=150),
    __D_: Color(h=30),
    __E_: Color(h=30, s=200, v=150),
    __F_: Color(h=30),
    __G_: Color(h=30, s=200, v=150),
    __H_: Color(h=30, s=200, v=150),
    __I_: Color(h=30, s=200, v=150),
    __J_: Color(h=30),
    __K_: Color(h=30),
    __L_: Color(h=30),
    __M_: Color(h=30, s=200, v=150),
    __N_: Color(h=30, s=200, v=150),
    __O_: Color(h=30, s=200, v=150),
    __P_: Color(h=30, s=200, v=150),
    __Q_: Color(h=30, s=200, v=150),
    __S_: Color(h=30),
    __R_: Color(h=30, s=200, v=150),
    __T_: Color(h=30, s=200, v=150),
    __U_: Color(h=30, s=200, v=150),
    __V_: Color(h=30, s=200, v=150),
    __W_: Color(h=30, s=200, v=150),
    __X_: Color(h=30, s=200, v=150),
    __Y_: Color(h=30, s=200, v=150),
    __Z_: Color(h=30, s=200, v=150),
    LALT: Color(h=120),
    RALT: Color(h=120),
    SPCE: Color(h=70),
    SPC1: Color(h=70),
    SP_1: Color(h=70),
    BKSP: Color(h=0),
    QUOT: Color(h=40),
    SCLN: Color(h=70),
    EXLM: Color(h=70),
    LSFT: Color(h=120),
    RSFT: Color(h=120),
    RCMD: Color(h=120),
    LCMD: Color(h=120),
    RCTL: Color(h=120),
    LCTL: Color(h=120),
    LCLK: Color(h=130),
    CCLK: Color(h=135),
    RCLK: Color(h=130),
    ENTR: Color(h=70),
    CENT: Color(h=70),
    PERD: Color(h=40),
    COMA: Color(h=40),
    SLSH: Color(h=40),
    __↑_: Color(h=150),
    __↓_: Color(h=150),
    __←_: Color(h=150),
    __→_: Color(h=150),
    PGUP: Color(h=150),
    PGDN: Color(h=150),
    HOME: Color(h=150),
    _END: Color(h=150),
    BKWD: Color(h=150),
    FWWD: Color(h=150),
    BKLN: Color(h=150),
    FWLN: Color(h=150),
    DLWD: Color(h=0),
    DLLN: Color(h=0),
    _EQL: Color(h=40),
    MINS: Color(h=40),
    UNDS: Color(h=40),
    LCBR: Color(h=40),
    RCBR: Color(h=40),
    LPRN: Color(h=40),
    RPRN: Color(h=40),
    LBRC: Color(h=40),
    RBRC: Color(h=40),
    LABK: Color(h=40),
    RABK: Color(h=40),
    BSLS: Color(h=40),
    COPY: Color(h=190),
    _CUT: Color(h=190),
    PAST: Color(h=190),
    UNDO: Color(h=190),
    _ALL: Color(h=190),
    SAVE: Color(h=190),
    MTSL: Color(h=190),
    FIND: Color(h=190),
    SKSL: Color(h=190),
    CLOS: Color(h=0),
    RLOD: Color(h=190),
    NTAB: Color(h=190),
    TICK: Color(h=60),
    ESCP: Color(h=0),
    DELT: Color(h=0),
    EMOJ: Color(h=190),
    _URL: Color(h=190),
    LNCH: Color(h=190),
    CLPB: Color(h=190),
    CMNT: Color(h=190),
    PRNT: Color(h=190),
    PTSC: Color(h=190),
    VDSC: Color(h=190),
    OPEN: Color(h=190),
    CMCT: Color(h=120),
    NEW_: Color(h=120),
    MSSN: Color(h=130),
    APPN: Color(h=130),
  },
  default_color=Color(h=0, s=255, v=255),
  split_side=side,
  split_offset=26,
)
keyboard.modules.append(rgbkeys)

keyboard.keymap = [[
  _TAB, __Q_, __W_, __E_, __R_, __T_,                   __Y_, __U_, __I_, __O_, __P_, QUOT,
  LSFT, __A_, __S_, __D_, __F_, __G_,                   __H_, __J_, __K_, __L_, SCLN, ENTR,
  LCTL, __Z_, __X_, __C_, __V_, __B_,                   __N_, __M_, COMA, PERD, SLSH, RSFT,
              LALT, LCMD,                                           LCMD, LALT,
                          BKSP, SP_1,                         SPC1,
                             LCLK, _L2_,          RCLK,       _L2_,
                                RCLK, _L3_,              LCLK
], [
  ↓___, ESCP, __7_, __8_, __9_, LCBR,                   RCBR, VDSC, __↑_, _🚫_, PTSC, TICK,
  ↓___, __0_, __4_, __5_, __6_, LPRN,                   RPRN, __←_, EXLM, __→_, _🚫_, CENT,
  ↓___, _🚫_, __1_, __2_, __3_, LBRC,                   RBRC, MINS, _EQL, UNDS, BSLS, ↓___,
              ↓___, ↓___,                                           ↓___, ↓___,
                          DELT, ENTR,                         __↓_,
                             LSFT, ↓___,          ↓___,       EMOJ,
                             LSFT, ↓___,                RSFT,
], [
  CTAB, ESCP, CLOS, _🚫_, RLOD, NTAB,                   MSSN, _URL, PGUP, OPEN, PRNT, APPN,
  ↓___, _ALL, SAVE, MTSL, FIND, LCLK,                   BKLN, BKWD, SKSL, FWWD, FWLN, ↓___,
  ↓___, UNDO, _CUT, COPY, PAST, RCLK,                   NEW_, _🚫_, _🚫_, _🚫_, CMNT, ↓___,
              ↓___, ↓___,                                           ↓___, ↓___,
                          DLWD, ↓___,                         PGDN,
                             LSFT, ↓___,          ↓___,       LNCH,
                             LSFT, ↓___,                RSFT,
], [
  TTAB, _🚫_, _🚫_, _🚫_, _🚫_, _🚫_,                   _🚫_, _🚫_, _🚫_, _🚫_, _🚫_, _🚫_,
  _🚫_, _🚫_, _🚫_, _🚫_, _🚫_, _🚫_,                   _🚫_, BKLN, _🚫_, FWLN, _🚫_, _🚫_,
  _🚫_, _🚫_, _🚫_, _🚫_, _🚫_, _🚫_,                   _🚫_, _🚫_, _🚫_, _🚫_, _🚫_, _🚫_,
              _🚫_, _🚫_,                                           _🚫_, _🚫_,
                          DLLN, _🚫_,                         _🚫_,
                             LSFT, _🚫_,          _🚫_,       _🚫_,
                             LSFT, _🚫_,                _🚫_,
], [
  _TAB, __Q_, __W_, __E_, __R_, __T_,                   __Y_, __U_, __I_, __O_, __P_, QUOT,
  LSFT, __A_, __S_, __D_, __F_, __G_,                   __H_, __J_, __K_, __L_, SCLN, ENTR,
  LCTL, __Z_, __X_, __C_, __V_, __B_,                   __N_, __M_, COMA, PERD, SLSH, RSFT,
              LALT, LCMD,                                           LCMD, LALT,
                          BKSP, SPCE,                         SPCE,
                             LCLK, _L2_,          LCLK,       _L2_,
                                RCLK, _L3_,              RCLK,
]]

if __name__ == '__main__':
  print('starting kmk...')
  keyboard.go()
  print('returned from kmk...')
