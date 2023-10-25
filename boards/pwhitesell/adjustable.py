import board
# D0 D1 D10 D11 D12 D13 D2 D3 D4 D5 D6 D7 D8 D9
# A0 A1 A2 A3
# TX RX
# MISO MOSI SCK
# SCL SDA
import PMW3360
import time

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.modules.layers import Layers
from kmk.modules.capsword import CapsWord
from kmk.modules.oneshot import OneShot
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.sticky_mod import StickyMod
from kmk.modules.holdtap import HoldTap
from kmk.modules.tapdance import TapDance
from kmk.modules.mouse_keys import MouseKeys

from kmk.modules.pmw3360 import PMW3360
from kmk.modules.rgbkeys import RGBKeys, Color
from keys import get_keys, key_colors

class KBAKeyboard(KMKKeyboard):
  keymap = [[ 
    KC.RGB_TOG, KC.J, KC.X, KC.N1, KC.N4, KC.N7,
    KC.B, KC.K, KC.Y, KC.N2, KC.N5, KC.N8,
    KC.C, KC.L, KC.Z, KC.N3, KC.N6, KC.N9,
  ]]
  def __init__(self, rows=0, columns=0) -> None:
    super().__init__()
    self.debug_enabled = True
    self.rows = rows
    self.columns = columns
    self.rgb_pixels = self.rows * self.columns
    self.rgb_pixels = 3
    self.ks = get_keys()
    self.assign_pins()
    self.init_modules()
    self.init_rgb()

  def assign_pins(self):
    self.col_pins = tuple(( board.SDA, board.D9, board.D8, board.D7, board.D6, board.D5, board.D4, board.D3, )[0:self.columns])
    self.row_pins = tuple(( board.A3, board.A2, board.A1, board.A0, board.SCL )[0:self.rows])
    self.diode_orientation = DiodeOrientation.COL2ROW
    self.rgb_pin = board.D2
  
  def init_modules(self):
    self.modules.append(StickyMod())
    self.modules.append(MouseKeys())
    self.modules.append(HoldTap())
    self.modules.append(TapDance())
    self.modules.append(OneShot())
    self.modules.append(Layers())
    # self.modules.append(PMW3360(board.SCK, board.MOSI, board.MISO,board.D10))

  def init_rgb(self):
    self.rgb = RGB(
      pixel_pin=self.rgb_pin,
      num_pixels=self.rgb_pixels,
      sat_default=99,
      val_default=99,
      val_limit=99,
      animation_mode=AnimationModes.STATIC,
    )
    self.extensions.append(self.rgb)

    # self.modules.append(RGBKeys(
    #   coord_mapping=[
    #     0, 3, 6, 9,  12, 15,
    #     1, 4, 7, 10, 13, 16,
    #     2, 5, 8, 11, 14, 17,
    #   ],
    #   key_colors=key_colors(self.ks),
    #   default_color=Color(h=0, s=255, v=255),
    #   split_offset=6,
    # ))
  
  def during_bootup(self) -> None:
    super().during_bootup()
    print('-----======-----booted')
    # time.sleep(5)
    # self.rgb.set_rgb_fill([255, 255, 255])
    # self.rgb.set_rgb([255, 255, 255], 2)
    self.rgb.show()
    # self.rgb.set_rgb_fill((255, 255, 255))
    self.rgb.set_rgb((99, 99, 99), 1)
    # self.rgb.set_rgb((80, 80, 80), 2)
    # self.rgb.set_rgb((70, 70, 70), 3)
    self.rgb.show()
    print('----after show')


if __name__ == '__main__':
  print("⌨️~⌨️ adjustable keyboard")
  print(dir(board))
  KBAKeyboard(3, 6).go()
  print('exit')