import math

from kmk.keys import AX
from kmk.modules import Module
import PMW3360 as PMW3360Lib
from kmk.utils import Debug

debug = Debug(__name__)

max_int16 = 65536
_REG_Lift_Config = const(0x63)

class PMW3360(Module):
    def __init__(self, sck, mosi, miso, cs, invert_x=False, invert_y=False, offset_angle=90, lift_config=0x01, cpi=1000, scroll_layers=[]):
        self.sensor = PMW3360Lib.PMW3360(sck, mosi, miso, cs)
        self.invert_x = invert_x
        self.invert_y = invert_y
        self.offset_angle = math.radians(offset_angle)
        self.lift_config = lift_config
        self.cpi = cpi
        self.scroll_layers = scroll_layers
        self.v_scroll_ctr = 0
        self.h_scroll_ctr = 0
        self.scroll_res = 10

    def during_bootup(self, keyboard):
        if self.sensor.begin(self.cpi):
            if debug.enabled:
                debug("sensor ready")
        else:
            if debug.enabled:
                debug("firmware upload failed")

    def before_matrix_scan(self, keyboard):
        data = self.sensor.read_burst()
        if not data["is_on_surface"] or not data["is_motion"]:
            return
        raw_x = data["dx"]
        raw_y = data["dy"]
        if raw_x > max_int16/2:
            raw_x = raw_x - max_int16
        if raw_y > max_int16/2:
            raw_y = raw_y - max_int16
        # x was coming out inverted
        raw_x = -raw_x
        dx = math.floor(raw_x * math.cos(self.offset_angle) - raw_y * math.sin(self.offset_angle))
        dy = math.floor(raw_x * math.sin(self.offset_angle) + raw_y * math.cos(self.offset_angle))
        if self.invert_x:
            dx *= -1
        if self.invert_y:
            dy *= -1
        if dx == 0 and dy == 0:
            return
        if keyboard.debug_enabled:
            debug('Delta: ', dx, ' ', dy)
        if keyboard.active_layers[0] in self.scroll_layers:
            self.v_scroll(keyboard, dy)
            self.h_scroll(keyboard, dx)
        else:
            if dx:
                AX.X.move(keyboard, dx)
            if dy:
                AX.Y.move(keyboard, dy)

    def v_scroll(self, keyboard, delta):
        self.v_scroll_ctr += delta
        if self.v_scroll_ctr >= self.scroll_res:
            AX.W.move(keyboard, -1)
            self.v_scroll_ctr = 0
        if self.v_scroll_ctr <= -self.scroll_res:
            AX.W.move(keyboard, 1)
            self.v_scroll_ctr = 0

    def h_scroll(self, keyboard, delta):
        self.h_scroll_ctr += delta
        if self.h_scroll_ctr >= self.scroll_res:
            AX.P.move(keyboard, 1)
            self.h_scroll_ctr = 0
        if self.h_scroll_ctr <= -self.scroll_res:
            AX.P.move(keyboard, -1)
            self.h_scroll_ctr = 0

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
