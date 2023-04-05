from kmk.extensions.RGB import RGB, hsv_to_rgb
from kmk.modules import Module
from kmk.modules.split import SplitSide
from kmk.keys import KC, make_argumented_key
import traceback

def rgb_to_hsv(r, g, b):
  maxc = max(r, g, b)
  minc = min(r, g, b)
  rangec = (maxc-minc)
  v = maxc
  if minc == maxc:
    return 0.0, 0.0, v
  s = rangec / maxc
  rc = (maxc-r) / rangec
  gc = (maxc-g) / rangec
  bc = (maxc-b) / rangec
  if r == maxc:
    h = bc-gc
  elif g == maxc:
    h = 2.0+rc-bc
  else:
    h = 4.0+gc-rc
  h = (h/6.0) % 1.0
  return h, s, v

class Color():
  def __init__(self, r=None, g=None, b=None, h=None, s=None, v=None, other=None):
    self.r=r
    self.g=g
    self.b=b
    self.h=h
    self.s=s
    self.v=v
    self.original = {'h': h, 's': s, 'v': v, 'r': r, 'g': g, 'b': b}
    if other is not None:
      self.other = {'h': other.h, 's': other.s, 'v': other.v, 'r': other.r, 'g': other.g, 'b': other.b}
    else:
      self.other = None
    self.animate_toward_color = False
    self.target_color = self.original
  def hsv(self, h=None, s=None, v=None, r=None, g=None, b=None):
    if self.h is not None or self.s is not None or self.v is not None:
      return (
        self.h if self.h is not None else h,
        self.s if self.s is not None else s,
        self.v if self.v is not None else v,
      )
    if self.r is not None or self.g is not None or self.b is not None:
      return rgb_to_hsv(
        self.r if self.r is not None else r,
        self.g if self.g is not None else g,
        self.b if self.b is not None else b,
      )
  def update(self, other):
    self.h = other['h']
    self.s = other['s']
    self.v = other['v']
    self.r = other['r']
    self.g = other['g']
    self.b = other['b']

class RGBKeysKeyMeta:
  def __init__(
    self,
    tap,
    color=None,
    colors=None,
  ):
    self.tap = tap
    self.color = color

class RGBKeys(Module):
  split_offset=0
  split_side=None
  layers=None
  coord_mapping=None
  key_colors=None
  last_top_layer=None
  default_color=None
  def __init__(
    self,
    split_offset=None,
    split_side=None,
    coord_mapping=None,
    key_colors=None,
    default_color=None,
  ):
    if split_offset:
      self.split_offset = split_offset
    if split_side is not None:
      self.split_side = split_side
    if coord_mapping is not None:
      self.coord_mapping = coord_mapping
    if key_colors is not None:
      self.key_colors = key_colors
    if default_color is None:
      default_color=Color(h=0, s=255, v=255, r=255, g=0, b=0)
    self.default_color=default_color
    if not KC.get('RGB'):
      make_argumented_key(
        validator=RGBKeysKeyMeta,
        names=('RGB',),
        on_press=self.rgb_pressed,
        on_release=self.rgb_released,
      )
    self.animated_colors = {}

  def rgb_pressed(self, key, keyboard, *args, **kwargs):
    if hasattr(key.meta.tap, 'on_press'):
      key.meta.tap.on_press(keyboard, args, **kwargs)
    return keyboard

  def rgb_released(self, key, keyboard, *args, **kwargs):
    if hasattr(key.meta.tap, 'on_release'):
      key.meta.tap.on_release(keyboard, args, **kwargs)
    return keyboard

  # required methods
  def during_bootup(self, keyboard):
    self.rgb = next(x for x in keyboard.extensions if type(x) is RGB)
    try:
      self.refresh_rgb(keyboard)
    except Exception as e:
      print(e)
      traceback.print_exception(e)
    return

  def refresh_rgb(self, keyboard):
    # self.animate()
    if (self.last_top_layer is not None) and (self.last_top_layer == keyboard.active_layers[0]):
      return
    self.animated_colors = {}
    self.last_top_layer = keyboard.active_layers[0]
    rgbs = []
    # print('keyboard.active_layers', keyboard.active_layers)
    for i, _ in enumerate(keyboard.keymap[0]):
      rgb, rgb_i = self.get_key_rgb(i, keyboard)
      if rgb is None:
        continue
      rgbs.append([rgb, rgb_i])
    self.rgb.set_rgbs(rgbs)

  def refresh_key(self, i, keyboard):
    rgb, rgb_i = self.get_key_rgb(i, keyboard)
    if rgb is None:
      return
    self.rgb.set_rgb((rgb), rgb_i)
    # self.set_color(rgb_i, color)

  def get_key_rgb(self, i, keyboard):
    hsv = None
    has_color = False
    rgb_i = 0
    for l in reversed(keyboard.active_layers):
      key = keyboard.keymap[l][i]
      has_color = False
      if key in self.key_colors:
        has_color = True
        color = self.key_colors[key]
      if hasattr(key.meta, 'color'):
        has_color = True
        color = key.meta.color
      if not has_color:
        return None, None
      rgb_i = self.coord_mapping[i]
      # if color.other is not None:
      #   self.animated_colors[rgb_i] = color
      default_color = {
        'h': self.default_color.h,
        's': self.default_color.s,
        'v': self.default_color.v,
        'r': self.default_color.r,
        'g': self.default_color.g,
        'b': self.default_color.b,
      }
      hsv = color.hsv(**default_color)
    return [hsv_to_rgb(hsv[0], hsv[1], hsv[2]), rgb_i]

  # def set_color(self, i, color):
  #   default_color = {
  #     'h': self.default_color.h,
  #     's': self.default_color.s,
  #     'v': self.default_color.v,
  #     'r': self.default_color.r,
  #     'g': self.default_color.g,
  #     'b': self.default_color.b,
  #   }
  #   hsv = color.hsv(**default_color)
  #   if self.split_side == SplitSide.LEFT and i < self.split_offset:
  #     self.rgb.set_hsv(hsv[0], hsv[1], hsv[2], i)
  #   if self.split_side == SplitSide.RIGHT and i >= self.split_offset:
  #     i -= self.split_offset
  #     self.rgb.set_hsv(hsv[0], hsv[1], hsv[2], i)
  #   self.rgb.set_hsv(hsv[0], hsv[1], hsv[2], i)

  def before_matrix_scan(self, keyboard):
    return
  def after_matrix_scan(self, keyboard):
    return
  def process_key(self, keyboard, key, is_pressed, int_coord):
    return key
  def before_hid_send(self, keyboard):
    return
  def after_hid_send(self, keyboard):
    try:
      self.refresh_rgb(keyboard)
      return
    except Exception as e:
      print(e)
      traceback.print_exception(e)
  def on_powersave_enable(self, keyboard):
    return

  def on_powersave_disable(self, keyboard):
    self.refresh_rgb(keyboard)
    return

  # def animate(self):
  #   for rgb_i, color in self.animated_colors.items():
  #     v = color.v if color.v is not None else self.default_color.v
  #     target_v = color.target_color['v'] if color.target_color['v'] is not None else self.default_color.v
  #     if color.animate_toward_color:
  #       if v < target_v:
  #         color.v = v+3
  #       else:
  #         color.animate_toward_color = False
  #     else:
  #       if v > 0:
  #         color.v = v-3
  #       else:
  #         color.animate_toward_color = True
  #         if color.target_color == color.original:
  #           color.target_color = color.other
  #         else:
  #           color.target_color = color.original
  #         color.h = color.target_color['h']
  #         color.s = color.target_color['s']
  #     self.set_color(rgb_i, color)
  #   return