# xeyes.py

"""
Description: xeyes-like widget (with help from ChatGPT)
Author: David COBAC
Date Created: January 10, 2026
Date Modified: January 10, 2026
Version: 1.0
Python Version: 3.13
Dependencies:
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/qtile_alt_widgets
"""
import math as _math

from libqtile.widget import base


class Xeyes(base._Widget):
    defaults = [
        ("eye_radius", 15),
        ("iris_radius", 5),
        ("pupil_radius", 3),
        ("padding", 0),
        ("gap", 3),
        ("update_interval", 0.04),
        ("eye_color", "ffffff"),
        ("iris_color", "aaaaff"),
        ("pupil_color", "000000"),
    ]

    def __init__(self, **config):
        super().__init__(length=1, **config)
        self.add_defaults(self.defaults)
        self._timer = None
        self._mouse_pos = (0, 0)

    @staticmethod
    def str2rgb(c):
        c = c.lstrip("#")
        return tuple(int(c[i:i+2], 16) / 255 for i in (0, 2, 4))

    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)
        self.length = self.eye_radius*4 + self.gap + self.padding*2
        self._tick()

    def finalize(self):
        if self._timer:
            self._timer.cancel()
        super().finalize()

    def _tick(self):
        if self._timer:
            self._timer.cancel()
        self._timer = self.timeout_add(self.update_interval, self._update)

    def _update(self):
        try:
            self._mouse_pos = self.qtile.core.get_mouse_position()
            self.draw()
        finally:
            self._tick()

    def _iris(self, local_cx, local_cy):
        mx, my = self._mouse_pos

        eye_x = self.bar.x + self.offsetx + local_cx
        eye_y = self.bar.y + local_cy

        dx = mx - eye_x
        dy = my - eye_y

        dist = _math.hypot(dx, dy)
        maxd = self.eye_radius - max(self.iris_radius, self.pupil_radius) - 2

        if dist == 0:
            return 0, 0

        scale = min(1, maxd / dist)
        return dx * scale, dy * scale

    def draw(self):
        self.drawer.clear(self.bar.background)
        ctx = self.drawer.ctx

        cy = self.bar.height // 2
        r = self.eye_radius
        d = r * 2

        x1 = self.padding + r
        x2 = x1 + d + self.gap

        for cx in (x1, x2):
            ctx.set_source_rgb(*self.str2rgb(self.eye_color))
            ctx.arc(cx, cy, r, 0, 2*_math.pi)
            ctx.fill()

            px, py = self._iris(cx, cy)
            ctx.set_source_rgb(*self.str2rgb(self.iris_color))
            ctx.arc(cx + px, cy + py, self.iris_radius, 0, 2*_math.pi)
            ctx.fill()
            
            ctx.set_source_rgb(*self.str2rgb(self.pupil_color))
            ctx.arc(cx + px, cy + py, self.pupil_radius, 0, 2*_math.pi)
            ctx.fill()

        self.draw_at_default_position()
