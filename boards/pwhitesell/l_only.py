import board
from kmk.utils import Debug
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
# from kmk.modules.layers import Layers
# from kmk.modules.rgbkeys import RGBKeys, Color
from kmk.modules.holdtap import HoldTap
from kmk.modules.oneshot import OneShot
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.RGB import RGB, AnimationModes

Debug.disable('kmk.modules.split', 'kmk.modules.holdtap', 'kmk.hid')
debug = Debug('main')

keyboard = KMKKeyboard()
keyboard.debug_enabled = True
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
# keyboard.coord_mapping = [
#   4, 5,
#   2, 3,
#   0, 1,
# ]
# keyboard.coord_mapping = [
#      0,    1,    2,    3,    4,    5,
#      6,    7,    8,    9,   10,   11,
#     12,   13,   14,   15,   16,   17,
#                           # 20,   19,   18,
#                           # 26,   25,   24,
# ]
keyboard.modules.append(HoldTap())
keyboard.modules.append(OneShot())
keyboard.modules.append(MouseKeys())
keyboard.extensions.append(RGB(
  animation_mode=AnimationModes.STATIC_STANDBY,
  pixel_pin=board.D11,
  num_pixels=24,
  hue_default=56,
  sat_default=255,
  val_default=100,
  val_limit=255,
))

# import keys as k
# keyboard.keymap = [[
#   k._TAB, k.__Q_, k.__W_, k.__E_, k.__R_, k.__T_,
#   k.LSFT, k.__A_, k.__S_, k.__D_, k.__F_, k.__G_,
#   k.LCTL, k.__Z_, k.__X_, k.__C_, k.__V_, k.__B_,
#                       # k.LCTL, k.LALT, k.LCMD,
#                       # k.✂__←, k.SPCE, k.ENTR,
# ]]

if __name__ == '__main__':
  print('starting kmk...')
  keyboard.go()
  print('returned from kmk...')
