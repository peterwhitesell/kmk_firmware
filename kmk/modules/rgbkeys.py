from kmk.extensions.RGB import RGB, hsv_to_rgb
from kmk.modules import Module
from kmk.modules.split import SplitSide
from kmk.keys import KC, make_argumented_key

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
  def __init__(self, r=None, g=None, b=None, h=None, s=None, v=None):
    self.r=r
    self.g=g
    self.b=b
    self.h=h
    self.s=s
    self.v=v
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

class RGBKeysKeyMeta:
  def __init__(
    self,
    tap,
    color=None,
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
    self.refresh_rgb(keyboard)
    return
  def refresh_rgb(self, keyboard):
    if (self.last_top_layer is not None) and (self.last_top_layer == keyboard.active_layers[0]):
      return
    self.last_top_layer = keyboard.active_layers[0]
    self.rgb.disable_auto_write = True
    default_color = {
      'h': self.default_color.h,
      's': self.default_color.s,
      'v': self.default_color.v,
      'r': self.default_color.r,
      'g': self.default_color.g,
      'b': self.default_color.b,
    }
    for l in reversed(keyboard.active_layers):
      for i, key in enumerate(keyboard.keymap[l]):
        has_color = False
        if key in self.key_colors:
          has_color = True
          hsv = self.key_colors[key].hsv(**default_color)
        if hasattr(key.meta, 'color'):
          has_color = True
          hsv = key.meta.color.hsv(**default_color)
        rgb_i = self.coord_mapping[i]
        if self.split_side == SplitSide.LEFT and rgb_i < self.split_offset:
          if has_color:
            self.rgb.set_hsv(hsv[0], hsv[1], hsv[2], rgb_i)
          # else:
          #   self.rgb.set_hsv(0, 0, 0, rgb_i)
        if self.split_side == SplitSide.RIGHT and rgb_i >= self.split_offset:
          rgb_i -= self.split_offset
          if has_color:
            self.rgb.set_hsv(hsv[0], hsv[1], hsv[2], rgb_i)
          # else:
          #   self.rgb.set_hsv(0, 0, 0, rgb_i)
    self.rgb.show()
  def before_matrix_scan(self, keyboard):
    return
  def after_matrix_scan(self, keyboard):
    return
  def process_key(self, keyboard, key, is_pressed, int_coord):
    return key
  def before_hid_send(self, keyboard):
    return
  def after_hid_send(self, keyboard):
    self.refresh_rgb(keyboard)
    return
  def on_powersave_enable(self, keyboard):
    return
  def on_powersave_disable(self, keyboard):
    self.refresh_rgb(keyboard)
    return