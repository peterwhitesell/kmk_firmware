print("Starting TB - split mode ⌨️~⌨️")

import board
# print(dir(board))
# ['__class__', '__name__', 'A0', 'A1', 'A2', 'A3', 'D0', 'D1', 'D10', 'D11', 'D12', 'D13', 'D24', 'D25', 'D4', 'D5', 'D6', 'D9', 'I2C', 'LED', 'MISO', 'MOSI', 'NEOPIXEL', 'RX', 'SCK', 'SCL', 'SDA', 'SPI', 'STEMMA_I2C', 'TX', 'UART', 'board_id']

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
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.sticky_mod import StickyMod
from kmk.modules.rgbkeys import RGBKeys, Color
from storage import getmount
from kmk.modules.holdtap import HoldTap
from kmk.modules.tapdance import TapDance
from kmk.utils import Debug
import traceback
side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

print("split side is:", side)
rgb_pin = board.D11
if side == SplitSide.RIGHT:
  print("~⌨️  RIGHT")
  rgb_pixels = 24
else:
  print("LEFT  ⌨~")
  rgb_pixels = 24

keyboard = KMKKeyboard()
keyboard.debug_enabled = True

keyboard.modules.append(StickyMod())
keyboard.modules.append(MouseKeys())
keyboard.modules.append(HoldTap())

td = TapDance()
keyboard.modules.append(td)
keyboard.modules.append(OneShot())
layers = Layers()
keyboard.modules.append(layers)

capsWord = CapsWord(timeout=5000)
keyboard.modules.append(capsWord)
keyboard.diode_orientation = DiodeOrientation.ROW2COL
keyboard.col_pins = (
  board.SDA, board.SCL, board.D5, board.D6, board.D9, board.D10,
)
keyboard.row_pins = (
  board.D24,
  board.A3,
  board.A2,
  board.A1,
  board.A0,
)

keyboard.coord_mapping = [
     0,    1,    2,    3,    4,    5,                    30,   31,   32,   33,   34,   35,
     6,    7,    8,    9,   10,   11,                    36,   37,   38,   39,   40,   41,
    12,   13,   14,   15,   16,   17,                    42,   43,   44,   45,   46,   47,
                          21,   22,   23,             48,   49,   50,
                          27,   28,   29,             54,   55,   56,
]

if side == SplitSide.RIGHT:
  pmw3360 = PMW3360(
    cs=board.RX,      # SS Yellow
    miso=board.MISO,  # MI Green
    mosi=board.MOSI,  # MO Brown
    sclk=board.SCK,   # SC White
    lift_config=0x04,
    invert_x=True,
    invert_y=True,
    flip_xy=True,
  )
  keyboard.modules.append(pmw3360)

split = Split(
  split_side=side,
  split_target_left=False,
  # uart_flip=True,
  uart_flip=False,
  split_flip=False,
  # use_pio=True,
  use_pio=False,
  data_pin=board.D13,
  data_pin2=board.D12,
)
keyboard.modules.append(split)

_L1_ = KC.MO(1)
_L2_ = KC.MO(2)
_L3_ = KC.MO(3)
_L4_ = KC.MO(4)
SP_1 = KC.HT(KC.SPACE, KC.MO(1), tap_time=200)
SPC1 = KC.HT(KC.SPACE, KC.MO(1), tap_time=200)
BSP2 = KC.HT(KC.BSPC, KC.MO(2), tap_time=200)
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
CTAB = KC.SM(KC.TAB, KC.LCMD)
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
SPCE = KC.SPACE
✂__← = KC.BSPC
QUOT = KC.QUOT
SCLN = KC.SCLN
EXLM = KC.EXLM
LSFT = KC.TD(KC.HT(KC.OS(KC.LSFT, tap_time=None), KC.LSFT), KC.CW)
RSFT = KC.TD(KC.HT(KC.OS(KC.RSFT, tap_time=None), KC.RSFT), KC.CW)
RCMD = KC.HT(KC.OS(KC.RCMD, tap_time=None), KC.RCMD)
LCMD = KC.HT(KC.OS(KC.LCMD, tap_time=None), KC.LCMD)
RALT = KC.HT(KC.OS(KC.RALT, tap_time=None), KC.RALT)
LALT = KC.HT(KC.OS(KC.LALT, tap_time=None), KC.LALT)
RCTL = KC.RCTL
LCTL = KC.HT(KC.OS(KC.LCTL, tap_time=None), KC.LCTL)
LCLK = KC.MB_LMB
CCLK = simple_key_sequence((
  KC.LCMD(no_release=True),
  KC.MACRO_SLEEP_MS(30),
  KC.MB_LMB,
  KC.MACRO_SLEEP_MS(30),
  KC.LCMD(no_press=True),
))
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
_↑↑_ = KC.PGUP
_↓↓_ = KC.PGDN
_←←_ = KC.LALT(KC.LEFT)
_→→_ = KC.LALT(KC.RIGHT)
↑↑↑_ = KC.LCMD(KC.UP)
↓↓↓_ = KC.LCMD(KC.DOWN)
←←←_ = KC.LCMD(KC.LEFT)
→→→_ = KC.LCMD(KC.RIGHT)
S_↑_ = KC.LSFT(KC.UP)
S_↓_ = KC.LSFT(KC.DOWN)
S_←_ = KC.LSFT(KC.LEFT)
S_→_ = KC.LSFT(KC.RIGHT)
S↑↑_ = KC.LSFT(KC.PGUP)
S↓↓_ = KC.LSFT(KC.PGDN)
S←←_ = KC.LSFT(KC.LALT(KC.LEFT))
S→→_ = KC.LSFT(KC.LALT(KC.RIGHT))
S↑↑↑ = KC.LSFT(KC.LCMD(KC.UP))
S↓↓↓ = KC.LSFT(KC.LCMD(KC.DOWN))
S←←← = KC.LSFT(KC.LCMD(KC.LEFT))
S→→→ = KC.LSFT(KC.LCMD(KC.RIGHT))
PGUP = KC.PGUP
PGDN = KC.PGDN
✂__← = KC.BKSP
✂__→ = KC.DEL
✂_←← = KC.LALT(KC.BKSP)
✂_→→ = KC.LALT(KC.DEL)
✂←←← = KC.LCMD(KC.BKSP)
✂→→→ = KC.LCMD(KC.DEL)
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
  def __init__(self, keyboard, keys):
    self.timeout = None
    self.keyboard = keyboard
    for key in keys:
      key.after_press_handler(self.on_word_key)
  def on_word_key(self, key, keyboard, *args):
    if self.timeout is None:
      self.keyboard.keymap[0][43] = SPCE
    if self.timeout is not None:
      self.keyboard.cancel_timeout(self.timeout)
    self.timeout = self.keyboard.set_timeout(300, self.release)
    return key
  def release(self):
    self.keyboard.keymap[0][43] = SP_1
    self.timeout = None

wt = WordsTimeout(
  keyboard, 
  [KC.A, KC.B, KC.C, KC.D, KC.E, KC.F, KC.G, KC.H, KC.I, KC.J, KC.K, KC.L, KC.M, KC.N, KC.O, KC.P, KC.Q, KC.S, KC.R, KC.T, KC.U, KC.V, KC.W, KC.X, KC.Y, KC.Z]
)

class MouseLayer():
  def __init__(self, keyboard, keys):
    self.timeout = None
    self.keyboard = keyboard
    for key in keys:
      key.after_press_handler(self.on_mouse_key)
    self.pmw3360 = next(x for x in keyboard.modules if type(x) is PMW3360)
    if self.pmw3360 is not None:
      self.pmw3360.on_move = self.on_mouse_move
  def on_mouse_key(self, key, keyboard, *args):
    self.on_mouse_move(keyboard)
    return key
  def on_mouse_move(self, keyboard):
    if self.timeout is None:
      self.keyboard.keymap[0][28] = CCLK
      self.keyboard.keymap[0][16] = LCLK
      self.keyboard.keymap[0][15] = RCLK
      self.keyboard.keymap[0][19] = LCLK
      self.keyboard.keymap[0][20] = RCLK
      self.refresh_keys()
    if self.timeout is not None:
      self.keyboard.cancel_timeout(self.timeout)
    self.timeout = self.keyboard.set_timeout(300, self.release)
  def release(self):
    self.keyboard.keymap[0][28] = __G_
    self.keyboard.keymap[0][16] = __F_
    self.keyboard.keymap[0][15] = __D_
    self.keyboard.keymap[0][19] = __J_
    self.keyboard.keymap[0][20] = __V_
    self.timeout = None
    self.refresh_keys()
  def refresh_keys(self):
    rgbkeys_module = next(x for x in self.keyboard.modules if type(x) is RGBKeys)
    if rgbkeys_module is None:
      return
    for i in [15, 16, 28, 19, 20]:
      try:
        rgbkeys_module.refresh_key(i, self.keyboard)
      except Exception as e:
        print(e)
        traceback.print_exception(e)

# if side == SplitSide.RIGHT:
#   ml = MouseLayer(keyboard, [LCLK, RCLK])

def ball_scroll_enable(key, keyboard, *args):
    pmw3360.start_v_scroll()
    return True

def ball_scroll_disable(key, keyboard, *args):
    pmw3360.start_v_scroll(False)
    return True

if side == SplitSide.RIGHT:
  BSP2.before_press_handler(ball_scroll_enable)
  BSP2.before_release_handler(ball_scroll_disable)
  _L4_.before_press_handler(ball_scroll_enable)
  _L4_.before_release_handler(ball_scroll_disable)

rgb = RGB(
  animation_mode=AnimationModes.STATIC_STANDBY,
  pixel_pin=rgb_pin,
  num_pixels=rgb_pixels,
  hue_default=56,
  sat_default=255,
  val_default=0,
  val_limit=255,
  split=split,
)
keyboard.extensions.append(rgb)

class KeyColors:
  Off = Color(v=0)
  Letter = Color(h=140, s=100)
  Number = Color(h=18)
  Math = Color(h=18)
  Bracket = Color(h=42, s=200)
  Punctuation = Color(h=42)
  Mod = Color(h=205)
  Mouse = Color(h=20)
  Danger = Color(h=0)
  Space = Color(s=0)
  Nav = Color(h=150)
  Edit = Color(h=110)
  Browse = Color(s=150)
  ClipBoard = Color(h=88)
  Window = Color(h=45)
  SPC1 = Color(s=0, other=Mod)
  SP_1 = Color(s=0, other=Mod)
  BackSpace_L2 = Color(h=0, other=Mod)

if side == SplitSide.RIGHT:
  rgbkeys = RGBKeys(
    coord_mapping=[
        26,    27,    32,   33,   42,   43,                      2,    3,    8,    9,   14,   15,
        25,    28,    31,   34,   41,   44,                      1,    4,    7,   10,   13,   16,
        24,    29,    30,   35,   40,   45,                      0,    5,    6,   11,   12,   17,
                                36,   39,   46,             18,   20,   22,
                                37,   38,   47,             19,   21,   23,
    ],
    key_colors = {
      _🚫_: KeyColors.Off,
      _L1_: KeyColors.Mod,
      _L2_: KeyColors.Mod,
      _L3_: KeyColors.Mod,
      _L4_: KeyColors.Mod,
      __1_: KeyColors.Number,
      __2_: KeyColors.Number,
      __3_: KeyColors.Number,
      __4_: KeyColors.Number,
      __5_: KeyColors.Number,
      __6_: KeyColors.Number,
      __7_: KeyColors.Number,
      __8_: KeyColors.Number,
      __9_: KeyColors.Number,
      __0_: KeyColors.Number,
      __A_: KeyColors.Letter,
      __B_: KeyColors.Letter,
      __C_: KeyColors.Letter,
      __D_: KeyColors.Letter,
      __E_: KeyColors.Letter,
      __F_: KeyColors.Letter,
      __G_: KeyColors.Letter,
      __H_: KeyColors.Letter,
      __I_: KeyColors.Letter,
      __J_: KeyColors.Letter,
      __K_: KeyColors.Letter,
      __L_: KeyColors.Letter,
      __M_: KeyColors.Letter,
      __N_: KeyColors.Letter,
      __O_: KeyColors.Letter,
      __P_: KeyColors.Letter,
      __Q_: KeyColors.Letter,
      __S_: KeyColors.Letter,
      __R_: KeyColors.Letter,
      __T_: KeyColors.Letter,
      __U_: KeyColors.Letter,
      __V_: KeyColors.Letter,
      __W_: KeyColors.Letter,
      __X_: KeyColors.Letter,
      __Y_: KeyColors.Letter,
      __Z_: KeyColors.Letter,
      _TAB: KeyColors.Space,
      CTAB: KeyColors.Space,
      TTAB: KeyColors.Space,
      SPCE: KeyColors.Space,
      SPC1: KeyColors.SPC1,
      SP_1: KeyColors.SP_1,
      BSP2: KeyColors.BackSpace_L2,
      QUOT: KeyColors.Punctuation,
      SCLN: KeyColors.Punctuation,
      EXLM: KeyColors.Punctuation,
      LSFT: KeyColors.Mod,
      RSFT: KeyColors.Mod,
      RCMD: KeyColors.Mod,
      LCMD: KeyColors.Mod,
      RCTL: KeyColors.Mod,
      LCTL: KeyColors.Mod,
      LALT: KeyColors.Mod,
      RALT: KeyColors.Mod,
      LCLK: KeyColors.Mouse,
      CCLK: KeyColors.Mouse,
      RCLK: KeyColors.Mouse,
      ENTR: KeyColors.Space,
      CENT: KeyColors.Space,
      PERD: KeyColors.Punctuation,
      COMA: KeyColors.Punctuation,
      SLSH: KeyColors.Math,
      __↑_: KeyColors.Nav,
      __↓_: KeyColors.Nav,
      __←_: KeyColors.Nav,
      __→_: KeyColors.Nav,
      _↑↑_: KeyColors.Nav,
      _↓↓_: KeyColors.Nav,
      _←←_: KeyColors.Nav,
      _→→_: KeyColors.Nav,
      ↑↑↑_: KeyColors.Nav,
      ↓↓↓_: KeyColors.Nav,
      ←←←_: KeyColors.Nav,
      →→→_: KeyColors.Nav,
      S_↑_: KeyColors.Nav,
      S_↓_: KeyColors.Nav,
      S_←_: KeyColors.Nav,
      S_→_: KeyColors.Nav,
      S↑↑_: KeyColors.Nav,
      S↓↓_: KeyColors.Nav,
      S←←_: KeyColors.Nav,
      S→→_: KeyColors.Nav,
      S↑↑↑: KeyColors.Nav,
      S↓↓↓: KeyColors.Nav,
      S←←←: KeyColors.Nav,
      S→→→: KeyColors.Nav,
      ✂__←: KeyColors.Danger,
      ✂__→: KeyColors.Danger,
      ✂_←←: KeyColors.Danger,
      ✂_→→: KeyColors.Danger,
      ✂←←←: KeyColors.Danger,
      ✂→→→: KeyColors.Danger,
      PGUP: KeyColors.Nav,
      PGDN: KeyColors.Nav,
      _EQL: KeyColors.Math,
      MINS: KeyColors.Math,
      UNDS: KeyColors.Punctuation,
      LCBR: KeyColors.Bracket,
      RCBR: KeyColors.Bracket,
      LPRN: KeyColors.Bracket,
      RPRN: KeyColors.Bracket,
      LBRC: KeyColors.Bracket,
      RBRC: KeyColors.Bracket,
      LABK: KeyColors.Bracket,
      RABK: KeyColors.Bracket,
      BSLS: KeyColors.Punctuation,
      COPY: KeyColors.ClipBoard,
      _CUT: KeyColors.ClipBoard,
      PAST: KeyColors.ClipBoard,
      UNDO: KeyColors.Edit,
      _ALL: KeyColors.Edit,
      SAVE: KeyColors.Edit,
      MTSL: KeyColors.Edit,
      FIND: KeyColors.Edit,
      SKSL: KeyColors.Edit,
      CLOS: KeyColors.Danger,
      RLOD: KeyColors.Browse,
      NTAB: KeyColors.Browse,
      TICK: KeyColors.Punctuation,
      ESCP: KeyColors.Danger,
      EMOJ: KeyColors.Edit,
      _URL: KeyColors.Browse,
      LNCH: KeyColors.Window,
      CLPB: KeyColors.ClipBoard,
      CMNT: KeyColors.Edit,
      PRNT: KeyColors.Browse,
      PTSC: KeyColors.Window,
      VDSC: KeyColors.Window,
      OPEN: KeyColors.Browse,
      CMCT: KeyColors.Mod,
      NEW_: KeyColors.Edit,
      MSSN: KeyColors.Window,
      APPN: KeyColors.Window,
    },
    default_color=Color(h=0, s=255, v=255),
    split_side=side,
    split_offset=24,
  )
  keyboard.modules.append(rgbkeys)

keyboard.keymap = [[
  _TAB, __Q_, __W_, __E_, __R_, __T_,                   __Y_, __U_, __I_, __O_, __P_, QUOT,
  LSFT, __A_, __S_, __D_, __F_, __G_,                   __H_, __J_, __K_, __L_, SCLN, ENTR,
  LCTL, __Z_, __X_, __C_, __V_, __B_,                   __N_, __M_, COMA, PERD, SLSH, RSFT,
                       LCTL, LALT, LCMD,             _🚫_, _🚫_, _🚫_,
                       BSP2, SP_1, _L3_,             _🚫_, _🚫_, _🚫_,
], [
  CTAB, ESCP, _🚫_, EMOJ, _🚫_, _🚫_,                   _URL, _↑↑_, __↑_, OPEN, _🚫_, APPN,
  ↓___, _ALL, SAVE, RCLK, LCLK, ←←←_,                   _←←_, __←_, MSSN, __→_, _→→_, →→→_,
  ↓___, UNDO, _🚫_, _🚫_, CCLK, _🚫_,                   _🚫_, _↓↓_, __↓_, _🚫_, _🚫_, _🚫_,
                       _🚫_, _L4_, LNCH,             _🚫_, _🚫_, _🚫_,
                       _🚫_, _🚫_, _🚫_,             _🚫_, _🚫_, _🚫_,
], [
  TTAB, ESCP, CLOS, _🚫_, RLOD, NTAB,                   _🚫_, _🚫_, _🚫_, _🚫_, PRNT, _🚫_,
  ↓___, _🚫_, SAVE, MTSL, FIND, ✂←←←,                   ✂_←←, ✂__←, SKSL, ✂__→, ✂_→→, ✂→→→,
  ↓___, UNDO, _CUT, COPY, PAST, _🚫_,                   NEW_, _🚫_, _🚫_, _🚫_, CMNT, ↓___,
                       ✂_←←, ↓___, ↓___,             _🚫_, _🚫_, _🚫_,
                       ↓___, LSFT, LSFT,             _🚫_, _🚫_, _🚫_,
], [
  _🚫_, _🚫_, __7_, __8_, __9_, LCBR,                   RCBR, _🚫_, _🚫_, _🚫_, _🚫_, TICK,
  ↓___, __0_, __4_, __5_, __6_, LPRN,                   RPRN, _🚫_, EXLM, _🚫_, _🚫_, CENT,
  _🚫_, _🚫_, __1_, __2_, __3_, LBRC,                   RBRC, MINS, _EQL, UNDS, BSLS, RSFT,
                       ↓___, ↓___, ↓___,             _🚫_, _🚫_, _🚫_,
                       _🚫_, _🚫_, ↓___,             _🚫_, _🚫_, _🚫_,
], [
  _🚫_, ↓___, _🚫_, _🚫_, _🚫_, _🚫_,                   _🚫_, S↑↑_, S_↑_, _🚫_, _🚫_, _🚫_,
  ↓___, ↓___, ↓___, ↓___, ↓___, S←←←,                   S←←_, S_←_, _🚫_, S_→_, S→→_, S→→→,
  _🚫_, UNDO, _CUT, COPY, PAST, _🚫_,                   _🚫_, S↓↓_, S_↓_, _🚫_, _🚫_, _🚫_,
                       _🚫_, _🚫_, _🚫_,             _🚫_, _🚫_, _🚫_,
                       _🚫_, ↓___, _🚫_,             _🚫_, _🚫_, _🚫_,
]]

if __name__ == '__main__':
  print('starting kmk...')
  keyboard.go()
  print('returned from kmk...')
