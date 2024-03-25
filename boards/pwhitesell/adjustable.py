import board
# D0 D1 D10 D11 D12 D13 D2 D3 D4 D5 D6 D7 D8 D9
# A0 A1 A2 A3
# TX RX
# MISO MOSI SCK
# SCL SDA

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.modules.layers import Layers
from kmk.modules.capsword import CapsWord
from kmk.modules.oneshot import OneShot
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.sticky_mod import StickyMod
from kmk.modules.holdtap import HoldTap
from kmk.modules.tapdance import TapDance
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.split import Split, SplitSide

from kmk.modules.pmw3360 import PMW3360
from kmk.modules.rgbkeys import RGBKeys, Color
from keys import get_keys, key_colors
from storage import getmount
# from kmk.utils import Debug

# Debug.disable('')
print('mount', getmount('/').label)
side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

class KBAKeyboard(KMKKeyboard):
  keymap = None
  def __init__(self, rows=0, columns=0, trackball=False) -> None:
    super().__init__()
    self.debug_enabled = False
    self.rows = rows
    self.columns = columns
    self.trackball = trackball
    self.rgb_pixels = self.rows * self.columns
    self.assign_pins()
    self.init_modules()
    self.keymap = self.init_keymap()
    self.coord_mapping = [
     0,    1,    2,    3,    4,    5,                    26,   25,   24,   27,   28,   29, # 30,   31,
     8,    9,   10,   11,   12,   13,                    34,   33,   32,   35,   36,   37, # 38,   39,
    16,   17,   18,   19,   20,   21,                    42,   41,   40,   43,   44,   45, # 42,   43,
                            23,   15,   7,
                            22,   14,   6,
    ]
    # self.init_rgb()

  def init_keymap(self):
    self.ks = ks = get_keys()
    return [[
ks['_TAB'], ks['__Q_'], ks['__W_'], ks['__E_'], ks['__R_'], ks['__T_'],         ks['__Y_'], ks['__U_'], ks['__I_'], ks['__O_'], ks['__P_'], ks['QUOT'],
ks['LSFT'], ks['__A_'], ks['__S_'], ks['__D_'], ks['__F_'], ks['__G_'],         ks['__H_'], ks['__J_'], ks['__K_'], ks['__L_'], ks['SCLN'], ks['ENTR'],
ks['LCTL'], ks['__Z_'], ks['__X_'], ks['__C_'], ks['__V_'], ks['__B_'],         ks['__N_'], ks['__M_'], ks['COMA'], ks['PERD'], ks['SLSH'], ks['RSFT'],
                                            ks['BSPC'], ks['SPCE'], ks['RCLK'],
                                            ks['_L2_'], ks['_L1_'], ks['LCLK'],
], [
ks['TTAB'], ks['ESCP'], ks['__7_'], ks['__8_'], ks['__9_'], ks['→→→_'],         ks['←←←_'], ks['_←←_'], ks['__↑_'], ks['_↑↑_'], ks['_→→_'], ks['TICK'],
ks['↓___'], ks['__0_'], ks['__4_'], ks['__5_'], ks['__6_'], ks['LPRN'],         ks['RPRN'], ks['__←_'], ks['__↓_'], ks['_↓↓_'], ks['__→_'], ks['CENT'],
ks['↓___'], ks['_L🚫'], ks['__1_'], ks['__2_'], ks['__3_'], ks['LBRC'],         ks['RBRC'], ks['MINS'], ks['_EQL'], ks['UNDS'], ks['BSLS'], ks['↓___'],
                                            ks['LCMD'], ks['EMOJ'], ks['↓___'],
                                            ks['LCTL'], ks['↓___'], ks['LALT'],
], [
ks['CTAB'], ks['ESCP'], ks['CLOS'], ks['SKSL'], ks['RLOD'], ks['NTAB'],         ks['MSSN'], ks['_URL'], ks['↓___'], ks['OPEN'], ks['PRNT'], ks['APPN'],
ks['↓___'], ks['_ALL'], ks['SAVE'], ks['MTSL'], ks['FIND'], ks['LCLK'],         ks['✂←←←'], ks['✂_←←'], ks['✂__←'], ks['✂__→'], ks['✂_→→'], ks['✂→→→'],
ks['↓___'], ks['UNDO'], ks['_CUT'], ks['COPY'], ks['PAST'], ks['RCLK'],         ks['NEW_'], ks['_L🚫'], ks['PTSC'], ks['VDSC'], ks['CMNT'], ks['↓___'],
                                            ks['LCMD'], ks['LALT'], ks['↓___'],
                                            ks['↓___'], ks['LNCH'], ks['↓___'],
]]

  def assign_pins(self):
    self.col_pins = tuple(( board.SDA, board.D9, board.D8, board.D7, board.D6, board.D5, board.D4, board.D3, )[0:self.columns])
    self.row_pins = tuple(( board.A3, board.A2, board.A1, board.A0, board.SCL )[0:self.rows])
    self.diode_orientation = DiodeOrientation.COL2ROW
    self.rgb_pin = board.D2
    self.sck_pin = board.SCK
    self.mosi_pin = board.MOSI
    self.miso_pin = board.MISO
    self.cs_pin = board.D10

  def init_modules(self):
    self.modules.append(StickyMod())
    self.modules.append(MouseKeys())
    self.modules.append(HoldTap())
    self.modules.append(TapDance())
    self.modules.append(OneShot())
    self.modules.append(Layers())
    if self.trackball:
      self.modules.append(PMW3360(
        self.sck_pin, self.mosi_pin, self.miso_pin,self.cs_pin,
        # invert_x=True,
        # invert_y=True,
        cpi=800,
        scroll_layers=[1],
      ))
    self.modules.append(Split(
      split_side=side,
      split_target_left=False,
      uart_flip=False,
      split_flip=False,
      data_pin=board.RX,
      data_pin2=board.TX,
    ))

  def init_rgb(self):
    self.rgb = RGB(
      pixel_pin=self.rgb_pin,
      num_pixels=self.rgb_pixels,
      hue_default=56,
      sat_default=255,
      val_default=0,
      val_limit=255,
      animation_mode=AnimationModes.STATIC_STANDBY,
    )
    self.extensions.append(self.rgb)
    self.modules.append(RGBKeys(
      coord_mapping=[
        0, 3, 6, 9,  12, 15, 18, 21,
        1, 4, 7, 10, 13, 16, 19, 22,
        2, 5, 8, 11, 14, 17, 20, 23,
      ],
      key_colors=key_colors(self.ks),
      default_color=Color(h=0, s=255, v=255),
      split_offset=6,
    ))
    # TODO fix startup dependency issue between extensions/rgb and modules/rgb_keys during_bootup

if __name__ == '__main__':
  print("⌨️~⌨️ adjustable keyboard")
  print(dir(board))
  if side == SplitSide.RIGHT:
    print('⌨️~ RIGHT')
    # KBAKeyboard(3, 6, trackball=True).go()
    KBAKeyboard(3, 8, trackball=True).go()
  else:
    print('⌨️~ LEFT')
    KBAKeyboard(3, 8).go()
  print('exit')