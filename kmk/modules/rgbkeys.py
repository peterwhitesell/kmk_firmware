from kmk.extensions.RGB import RGB
from kmk.modules import Module
from kmk.modules.split import SplitSide
from kmk.keys import KC, make_argumented_key

class RGBKeysKeyMeta:
  def __init__(
    self,
    key,
    hsa=None,
    rgb=None,
  ):
    self.key = key
    self.hsa = hsa
    self.rgb = rgb

class RGBKeys(Module):
  split_offset=0
  split_side=None
  layers=None
  coord_mapping=None
  last_top_layer=None
  def __init__(
    self,
    split_offset=None,
    split_side=None,
    coord_mapping=None,
  ):
    if split_offset:
      self.split_offset = split_offset
    if split_side is not None:
      self.split_side = split_side
    if coord_mapping is not None:
      self.coord_mapping = coord_mapping
    if not KC.get('RGB'):
      make_argumented_key(
        validator=RGBKeysKeyMeta,
        names=('RGB',),
        on_press=self.rgb_pressed,
        on_release=self.rgb_released,
      )
  def rgb_pressed(self, key, keyboard, *args, **kwargs):
    if hasattr(key.meta.key, 'on_press'):
      key.meta.key.on_press(keyboard, args, **kwargs)
    return keyboard
  def rgb_released(self, key, keyboard, *args, **kwargs):
    if hasattr(key.meta.key, 'on_release'):
      key.meta.key.on_release(keyboard, args, **kwargs)
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
    for l in reversed(keyboard.active_layers):
      for i, key in enumerate(keyboard.keymap[l]):
        if hasattr(key.meta, 'hsa') or hasattr(key.meta, 'hsa'):
          rgb_i = self.coord_mapping[i]
          if self.split_side == SplitSide.LEFT:
            if rgb_i >= self.split_offset:
              continue
            if hasattr(key.meta, 'hsa') and key.meta.hsa is not None:
              self.rgb.set_hsv(key.meta.hsa[0], key.meta.hsa[1], key.meta.hsa[2], rgb_i)
            if hasattr(key.meta, 'rgb') and key.meta.rgb is not None:
              self.rgb.set_rgb(key.meta.rgb, rgb_i)
          if self.split_side == SplitSide.RIGHT:
            if rgb_i < self.split_offset:
              continue
            rgb_i -= self.split_offset
            if hasattr(key.meta, 'hsa') and key.meta.hsa is not None:
              self.rgb.set_hsv(key.meta.hsa[0], key.meta.hsa[1], key.meta.hsa[2], rgb_i)
            if hasattr(key.meta, 'rgb') and key.meta.rgb is not None:
              self.rgb.set_rgb(key.meta.rgb, rgb_i)
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