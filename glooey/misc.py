import pyglet
import autoprop

from vecrec import Vector, Rect
from glooey import drawing
from glooey.widget import Widget
from glooey.buttons import Clickable
from glooey.images import Background
from glooey.helpers import *

@autoprop
class PlaceHolder(Clickable):
    custom_color = 'green'
    custom_alignment = 'fill'

    def __init__(self, min_width=0, min_height=0, color=None, align=None):
        super().__init__()
        self._color = color or self.custom_color
        self._min_width = min_width
        self._min_height = min_height
        self.vertex_list = None
        self.alignment = align or self.custom_alignment

    def do_claim(self):
        return self._min_width, self._min_height

    def do_regroup(self):
        if self.vertex_list is not None:
            self.batch.migrate(
                    self.vertex_list, pyglet.gl.GL_LINES,
                    self.group, self.batch)

    def do_draw(self):
        if self.vertex_list is None:
            self.vertex_list = self.batch.add(
                    12, pyglet.gl.GL_LINES, self.group, 'v2f', 'c4B')

        top_left = self.rect.top_left
        top_right = self.rect.top_right
        bottom_left = self.rect.bottom_left
        bottom_right = self.rect.bottom_right

        # Originally I used GL_LINE_STRIP, but I couldn't figure out how to 
        # stop the place holders from connecting to each other (i.e. I couldn't 
        # figure out how to break the line strip).  Now I'm just using GL_LINES 
        # instead.

        self.vertex_list.vertices = (
                # the outline
                bottom_left.tuple + bottom_right.tuple + 
                bottom_right.tuple + top_right.tuple + 
                top_right.tuple + top_left.tuple + 
                top_left.tuple + bottom_left.tuple + 

                # the cross
                bottom_left.tuple + top_right.tuple + 
                bottom_right.tuple + top_left.tuple
        ) 
        color = drawing.Color.from_anything(self.color)
        self.vertex_list.colors = 12 * color.tuple

    def do_undraw(self):
        if self.vertex_list is not None:
            self.vertex_list.delete()
            self.vertex_list = None

    def get_color(self):
        return self._color

    def set_color(self, new_color):
        self._color = new_color
        self.draw()

    def get_min_width(self):
        return self._min_width

    def set_min_width(self, new_width):
        self._min_width = new_width
        self.repack()

    def get_min_height(self):
        return self._min_height

    def set_min_height(self, new_height):
        self._min_height = new_height
        self.repack()


@autoprop
class EventLogger(PlaceHolder):

    def on_click(self, widget):
        print(f'{self}.on_click(widget={widget})')

    def on_double_click(self, widget):
        print(f'{self}.on_double_click(widget={widget})')

    def on_rollover(self, new_state, old_state):
        print(f'{self}.on_rollover(new_state={new_state}, old_state={old_state})')

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        print(f'{self}.on_mouse_press(x={x}, y={y}, button={button}, modifiers={modifiers})')

    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        print(f'{self}.on_mouse_release(x={x}, y={y}, button={button}, modifiers={modifiers})')

    def on_mouse_hold(self, dt):
        print(f'{self}.on_mouse_hold(dt={dt})')

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        print(f'{self}.on_mouse_motion(x={x}, y={y}, dx={dx}, dy={dy})')

    def on_mouse_enter(self, x, y):
        super().on_mouse_enter(x, y)
        print(f'{self}.on_mouse_enter(x={x}, y={y})')

    def on_mouse_leave(self, x, y):
        super().on_mouse_leave(x, y)
        print(f'{self}.on_mouse_leave(x={x}, y={y})')

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        print(f'{self}.on_mouse_drag(x={x}, y={y}, dx={dx}, dy={dy}, buttons={buttons}, modifiers={modifiers})')

    def on_mouse_drag_enter(self, x, y):
        super().on_mouse_drag_enter(x, y)
        print(f'{self}.on_mouse_drag_enter(x={x}, y={y})')

    def on_mouse_drag_leave(self, x, y):
        super().on_mouse_drag_leave(x, y)
        print(f'{self}.on_mouse_drag_leave(x={x}, y={y})')

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        super().on_mouse_scroll(x, y, scroll_x, scroll_y)
        print(f'{self}.on_mouse_scroll(x={x}, y={y}, scroll_x={scroll_x}, scroll_y={scroll_y})')


@autoprop
class FillBar(Widget):
    Base = Background
    Fill = Background

    def __init__(self, fraction_filled=0):
        super().__init__()

        self._base = self.Base()
        self._fill = self.Fill()
        self._fill_fraction = fraction_filled
        self._fill_group = None

        self._attach_child(self._base)
        self._attach_child(self._fill)

    def do_claim(self):
        min_width = max(self.base.claimed_width, self.fill.claimed_width)
        min_height = max(self.base.claimed_height, self.fill.claimed_height)
        return min_width, min_height

    def do_resize(self):
        self._update_fill()

    def do_regroup_children(self):
        base_layer = pyglet.graphics.OrderedGroup(1, self.group)
        fill_layer = pyglet.graphics.OrderedGroup(2, self.group)

        self._fill_group = drawing.ScissorGroup(parent=fill_layer)
        self._update_fill()

        self._base.regroup(base_layer)
        self._fill.regroup(self._fill_group)

    def do_draw(self):
        self._update_fill()

    def get_fill(self):
        return self._fill

    def get_base(self):
        return self._base

    def get_fraction_filled(self):
        return self._fill_fraction

    def set_fraction_filled(self, new_fraction):
        self._fill_fraction = new_fraction
        self._update_fill()

    def _update_fill(self):
        if self._fill_group and self.fill.rect:
            self._fill_group.rect = self.fill.rect.copy()
            self._fill_group.rect.width *= self._fill_fraction

