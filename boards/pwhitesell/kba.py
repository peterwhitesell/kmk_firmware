import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.modules.rgbkeys import RGBKeys, Color
from keys import get_keys, key_colors


from kmk.modules.layers import Layers
from kmk.modules.capsword import CapsWord
from kmk.modules.oneshot import OneShot
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.sticky_mod import StickyMod
from kmk.modules.holdtap import HoldTap
from kmk.modules.tapdance import TapDance
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.pmw3360 import PMW3360

class KBAKeyboard(KMKKeyboard):
  keymap = [[ 
    KC.A, KC.X,
    KC.B, KC.Y,
    KC.C, KC.Z,
  ]]
  def __init__(self, rgb_pixels=6) -> None:
    super().__init__()
    self.debug_enabled = True
    self.rgb_pixels = rgb_pixels
    self.assign_pins()
    self.init_modules()
    self.ks = get_keys()
    self.init_rgb()

  def assign_pins(self):
    self.col_pins = ( board.SDA, board.D9, )
    self.row_pins = ( board.A3, board.A2, board.A1 )
    self.diode_orientation = DiodeOrientation.COL2ROW
    self.rgb_pin = board.D2
  
  def init_modules(self):
    self.modules.append(StickyMod())
    self.modules.append(MouseKeys())
    self.modules.append(HoldTap())
    self.modules.append(TapDance())
    self.modules.append(OneShot())
    self.modules.append(Layers())
    self.modules.append(PMW3360(
      cs=board.D10,      # SS Yellow
      miso=board.MISO,  # MI Green
      mosi=board.MOSI,  # MO Brown
      sclk=board.SCK,   # SC White
      lift_config=0x04,
      invert_x=True,
      invert_y=True,
      flip_xy=True,
      scroll_layers=[1],
    ))

  def init_rgb(self):
    rgb = RGB(
      # animation_mode=AnimationModes.STATIC_STANDBY,
      pixel_pin=self.rgb_pin,
      num_pixels=self.rgb_pixels,
      # hue_default=56,
      sat_default=0,
      val_default=0,
      # val_default=255,
      # val_limit=255,
    )
    self.extensions.append(rgb)
    # rgb.show()
    # rgb.set_rgb([255, 255, 255], 1)
    # self.modules.append(RGBKeys(
    #   coord_mapping=[
    #     0, 3,
    #     1, 4,
    #     2, 5,
    #   ],
    #   key_colors=key_colors(self.ks),
    #   default_color=Color(h=0, s=255, v=255),
    #   split_offset=6,
    # ))

if __name__ == '__main__':
  print("KBA ⌨️~⌨️")
  print(dir(board))
  KBAKeyboard().go()
  print('exit')
