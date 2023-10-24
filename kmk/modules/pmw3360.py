import math

from kmk.keys import AX
from kmk.modules import Module
import PMW3360 as PMW3360Lib
from kmk.utils import Debug

debug = Debug(__name__)

max_delta = 65536

class PMW3360(Module):
    def __init__(self, sck, mosi, miso, cs, invert_x=False, invert_y=False, offset_angle=90):
        print(dir(PMW3360Lib))
        self.sensor = PMW3360Lib.PMW3360(sck, mosi, miso, cs)
        self.invert_x = invert_x
        self.invert_y = invert_y
        self.offset_angle = math.radians(offset_angle)

    def during_bootup(self, keyboard):
        if self.sensor.begin():
            if debug.enabled:
                print("sensor ready")
        else:
            if debug.enabled:
                print("firmware upload failed")

    def before_matrix_scan(self, keyboard):
        data = self.sensor.read_burst()
        if not data["is_on_surface"] or not data["is_motion"]:
            return
        raw_x = data["dx"]
        raw_y = data["dy"]

        if raw_x > 65536/2:
            raw_x = raw_x - 65536
        if raw_y > 65536/2:
            raw_y = raw_y - 65536
        # x was coming out inverted
        raw_x = -raw_x
        
        dx = math.floor(raw_x * math.cos(self.offset_angle) - raw_y * math.sin(self.offset_angle))
        dy = math.floor(raw_x * math.sin(self.offset_angle) + raw_y * math.cos(self.offset_angle))


        if self.invert_x:
            dx *= -1
        if self.invert_y:
            dy *= -1

        if keyboard.debug_enabled and (dx != 0 or dy != 0):
            print('Delta: ', dx, ' ', dy)
            if dx:
                AX.X.move(keyboard, dx)

            if dy:
                AX.Y.move(keyboard, dy)

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
