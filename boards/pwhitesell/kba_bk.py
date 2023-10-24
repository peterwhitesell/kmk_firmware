print("Starting KBA - split mode ⌨️~⌨️")

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
from keys import get_keys, key_colors
side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

print("split side is:", side)
if side == SplitSide.RIGHT:
  print("~⌨️  RIGHT")
  rgb_pixels = 24
else:
  print("LEFT  ⌨~")
  rgb_pixels = 24

keyboard = KMKKeyboard()
keyboard.debug_enabled = True
Debug.disable('kmk.modules.split', 'kmk.modules.holdtap', 'kmk.hid', 'kmk.extensions.RGB')

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
if side == SplitSide.RIGHT:
  rgb_pin = board.D2
  split_pins = [board.D0, board.D1]
  keyboard.col_pins = (
    board.SDA, board.D9,# board.D8, board.D7, board.D6, board.D5, board.D4, board.D3,
  )
  keyboard.row_pins = (
    board.A3,
    board.A2,
    board.A1,
    # board.A0,
    # board.SCL,
  )
else: # TODO remove this after both halves are identical
  rgb_pin = board.A3
  split_pins = [board.GP1, board.GP0]
  keyboard.col_pins = (
    board.GP7, board.GP6, board.GP5, board.GP4, board.GP3, board.GP2
  )
  keyboard.row_pins = (
    board.GP23,
    board.GP20,
    board.GP22,
    board.A0,
    board.A1
  )

keyboard.coord_mapping = [
  0,  1,
  8,  2,
  16, 17,
]
# keyboard.coord_mapping = [
#      0,    1,    2,    3,    4,    5,                    30,   31,   32,   33,   34,   35,
#      6,    7,    8,    9,   10,   11,                    36,   37,   38,   39,   40,   41,
#     12,   13,   14,   15,   16,   17,                    42,   43,   44,   45,   46,   47,
#                 20,    21,
#                             22,   23,
#                                28,   29,
#                                   26,  27,
# ]

# if side == SplitSide.RIGHT:
#   pmw3360 = PMW3360(
#     cs=board.D10,      # SS Yellow
#     miso=board.MISO,  # MI Green
#     mosi=board.MOSI,  # MO Brown
#     sclk=board.SCK,   # SC White
#     lift_config=0x04,
#     invert_x=True,
#     invert_y=True,
#     flip_xy=True,
#     scroll_layers=[1],
#   )
#   keyboard.modules.append(pmw3360)

split = None
# split = Split(
#   split_side=side,
#   split_target_left=False,
#   # uart_flip=True,
#   uart_flip=False,
#   split_flip=False,
#   # use_pio=True,
#   use_pio=False,
#   data_pin=split_pins[0],
#   data_pin2=split_pins[1],
# )
# keyboard.modules.append(split)

k = get_keys()
class WordsTimeout():
  def __init__(self, keyboard, keys):
    self.timeout = None
    self.keyboard = keyboard
    for key in keys:
      key.after_press_handler(self.on_word_key)
  def on_word_key(self, key, keyboard, *args):
    if self.timeout is None:
      self.keyboard.keymap[0][39] = k['SPCE']
    if self.timeout is not None:
      self.keyboard.cancel_timeout(self.timeout)
    self.timeout = self.keyboard.set_timeout(300, self.release)
    return key
  def release(self):
    self.keyboard.keymap[0][39] = k['SP_1']
    self.timeout = None

# wt = WordsTimeout(
#   keyboard,
#   [KC.A, KC.B, KC.C, KC.D, KC.E, KC.F, KC.G, KC.H, KC.I, KC.J, KC.K, KC.L, KC.M, KC.N, KC.O, KC.P, KC.Q, KC.S, KC.R, KC.T, KC.U, KC.V, KC.W, KC.X, KC.Y, KC.Z]
# )

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
      self.keyboard.keymap[0][17] = k['CCLK']
      self.keyboard.keymap[0][16] = k['LCLK']
      self.keyboard.keymap[0][15] = k['RCLK']
      self.keyboard.keymap[0][19] = k['LCLK']
      self.keyboard.keymap[0][20] = k['RCLK']
      self.refresh_keys()
    if self.timeout is not None:
      self.keyboard.cancel_timeout(self.timeout)
    self.timeout = self.keyboard.set_timeout(300, self.release)
  def release(self):
    self.keyboard.keymap[0][17] = k['__G_']
    self.keyboard.keymap[0][16] = k['__F_']
    self.keyboard.keymap[0][15] = k['__D_']
    self.keyboard.keymap[0][19] = k['__J_']
    self.keyboard.keymap[0][20] = k['__K_']
    self.timeout = None
    self.refresh_keys()
  def refresh_keys(self):
    rgbkeys_module = next(x for x in self.keyboard.modules if type(x) is RGBKeys)
    if rgbkeys_module is None:
      return
    for i in [15, 16, 17, 19, 20]:
      try:
        rgbkeys_module.refresh_key(i, self.keyboard)
      except Exception as e:
        print(e)
        traceback.print_exception(e)

# if side == SplitSide.RIGHT:
#   ml = MouseLayer(keyboard, [k['LCLK'], k['RCLK']])

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

if side == SplitSide.RIGHT:
  rgbkeys = RGBKeys(
    coord_mapping=[
      0, 3,
      1, 4,
      2, 5,
    ],
#     coord_mapping=[
# 29,    28,    27,   26,   25,   24,                      2,    3,    8,    9,   14,   15,
# 30,    31,    32,   33,   34,   35,                      1,    4,    7,   10,   13,   16,
# 41,    40,    39,   38,   37,   36,                      0,    5,    6,   11,   12,   17,
#                     42,   43,
#                                 44,   45,
#                                   47,   46,
#                                   48,   49,
#     ],
    key_colors=key_colors(k),
    default_color=Color(h=0, s=255, v=255),
    split_side=side,
    split_offset=18,
  )
  # keyboard.modules.append(rgbkeys)

keyboard.keymap = [[
  k['__1_'], k['__2_'],
  k['__A_'], k['__B_'],
  k['COMA'], k['PERD'],
# k['_TAB'], k['__Q_'], k['__W_'], k['__E_'], k['__R_'], k['__T_'],         k['__Y_'], k['__U_'], k['__I_'], k['__O_'], k['__P_'], k['QUOT'],
# k['LSFT'], k['__A_'], k['__S_'], k['__D_'], k['__F_'], k['__G_'],         k['__H_'], k['__J_'], k['__K_'], k['__L_'], k['SCLN'], k['ENTR'],
# k['LCTL'], k['__Z_'], k['__X_'], k['__C_'], k['__V_'], k['__B_'],         k['__N_'], k['__M_'], k['COMA'], k['PERD'], k['SLSH'], k['RSFT'],
#             k['RCLK'], k['LCLK'],
#                         k['BSP2'], k['SP_1'],
#                             k['EMOJ'], k['LCMD'],
#                             k['LNCH'], k['LALT'],
# # ], [
# # k['TTAB'], k['ESCP'], k['__7_'], k['__8_'], k['__9_'], k['→→→_'],         k['←←←_'], k['_←←_'], k['__↑_'], k['_↑↑_'], k['_→→_'], k['TICK'],
# # k['↓___'], k['__0_'], k['__4_'], k['__5_'], k['__6_'], k['LPRN'],         k['RPRN'], k['__←_'], k['__↓_'], k['_↓↓_'], k['__→_'], k['CENT'],
# # k['↓___'], k['_L🚫'], k['__1_'], k['__2_'], k['__3_'], k['LBRC'],         k['RBRC'], k['MINS'], k['_EQL'], k['UNDS'], k['BSLS'], k['↓___'],
# #             k['↓___'], k['↓___'],
# #                         k['✂__→'], k['ENTR'],
# #                             k['↓___'], k['↓___'],
# #                             k['↓___'], k['↓___'],
# # ], [
# # k['CTAB'], k['ESCP'], k['CLOS'], k['SKSL'], k['RLOD'], k['NTAB'],         k['MSSN'], k['_URL'], k['_🚫s'], k['OPEN'], k['PRNT'], k['APPN'],
# # k['↓___'], k['_ALL'], k['SAVE'], k['MTSL'], k['FIND'], k['LCLK'],         k['✂←←←'], k['✂_←←'], k['✂__←'], k['✂__→'], k['✂_→→'], k['✂→→→'],
# # k['↓___'], k['UNDO'], k['_CUT'], k['COPY'], k['PAST'], k['RCLK'],         k['NEW_'], k['_L🚫'], k['PTSC'], k['VDSC'], k['CMNT'], k['↓___'],
# #             k['↓___'], k['↓___'],
# #                         k['✂_←←'], k['↓___'],
# #                             k['↓___'], k['↓___'],
# #                             k['↓___'], k['↓___'],
]]

if __name__ == '__main__':
  print('starting kmk...')
  keyboard.go()
  print('returned from kmk...')
