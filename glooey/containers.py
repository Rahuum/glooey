""" 
Widgets whose primary role is to contain other widgets.  Most of these widgets 
don't draw anything themselves, they just position children widgets.
"""

import pyglet
import vecrec
import autoprop

from vecrec import Vector, Rect
from collections import defaultdict
from debugtools import p, pp, pv
from . import drawing
from .widget import Widget
from .helpers import *

def align_widget_in_box(widget, box_rect, key_or_func='fill', widget_rect=None):
    alignment_func = drawing.cast_to_alignment(key_or_func)

    if widget_rect is None:
        widget_rect = widget.claimed_rect

    alignment_func(widget_rect, box_rect)
    widget.resize(widget_rect)

def claim_stacked_widgets(*widgets):
    max_widget_width = 0
    max_widget_height = 0

    for widget in widgets:
        max_widget_width = max(max_widget_width, widget.claimed_width)
        max_widget_height = max(max_widget_height, widget.claimed_height)

    return max_widget_width, max_widget_height


@autoprop
class Bin (Widget):

    def __init__(self):
        super().__init__()
        self._child = None

    def add(self, child):
        if self._child is not None:
            self._detach_child(self._child)

        self._child = self._attach_child(child)
        assert len(self) == 1
        self._repack_and_regroup_children()

    def clear(self):
        if self._child is not None:
            self._detach_child(self._child)
        self._child = None
        assert len(self) == 0
        self._repack_and_regroup_children()

    def do_claim(self):
        if self.child is not None:
            return self.child.claimed_size
        else:
            return 0, 0

    def do_resize_children(self):
        if self.child is not None:
            align_widget_in_box(self.child, self.rect)

    def get_child(self):
        return self._child


@autoprop
class Viewport (Bin):

    class PanningGroup (pyglet.graphics.Group):

        def __init__(self, viewport, parent=None):
            pyglet.graphics.Group.__init__(self, parent)
            self.viewport = viewport

        def set_state(self):
            translation = -self.viewport.get_child_coords(0, 0)
            pyglet.gl.glPushMatrix()
            pyglet.gl.glTranslatef(translation.x, translation.y, 0)

        def del_state(self):
            pyglet.gl.glPopMatrix()

    def __init__(self, sensitivity=3):
        super().__init__()

        # The panning_vector is the displacement between the bottom-left corner 
        # of this widget and the bottom-left corner of the child widget.

        self._panning_vector = Vector.null()
        self._deferred_center_of_view = None
        self.sensitivity = sensitivity

        # The stencil_group, mask_group, and visible_group members manage the 
        # clipping mask to make sure the child is only visible inside the 
        # viewport.  The panning_group member is used to translate the child in 
        # response to panning events.

        self.stencil_group = None
        self.mask_group = None
        self.visible_group = None
        self.panning_group = None
        self.mask_artist = None

    def do_attach(self):
        # If this line raises a pyglet EventException, you're probably trying 
        # to attach this widget to a GUI that doesn't support mouse pan events.  
        # See the Viewport documentation for more information.
        self.root.push_handlers(self.on_mouse_pan)

    def do_detach(self):
        self.window.remove_handler(self.on_mouse_pan)

    def do_claim(self):
        # The widget being displayed in the viewport can claim however much 
        # space it wants.  The viewport doesn't claim any space, because it can 
        # be as small as it needs to be.
        return 0, 0

    def do_resize(self):
        # Set the center of view if it was previously specified.  The center of 
        # view cannot be directly set until the size of the viewport is known, 
        # but this limitation is hidden from the user by indirectly setting the 
        # center of view as soon as the viewport has a size.
        if self._deferred_center_of_view is not None:
            self.set_center_of_view(self._deferred_center_of_view)

    def do_resize_children(self):
        # Make the child whatever size it wants to be.
        if self.child is not None:
            self.child.resize(self.child.claimed_rect)

    def do_regroup(self):
        self.stencil_group = drawing.StencilGroup(self.group)
        self.mask_group = drawing.StencilMask(self.stencil_group)
        self.visible_group = drawing.WhereStencilIs(self.stencil_group)
        self.panning_group = Viewport.PanningGroup(self, self.visible_group)

        if self.mask_artist is not None:
            self.mask_artist.group = self.mask_group

    def do_regroup_children(self):
        self.child.regroup(self.panning_group)

    def do_draw(self):
        if self.mask_artist is None:
            self.mask_artist = drawing.Rectangle(
                    self.rect,
                    batch=self.batch,
                    group=self.mask_group)

        self.mask_artist.rect = self.rect

    def do_undraw(self):
        if self.mask_artist is not None:
            self.mask_artist.delete()

    def on_mouse_press(self, x, y, button, modifiers):
        x, y = self.get_child_coords(x, y)
        super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        x, y = self.get_child_coords(x, y)
        super().on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        x, y = self.get_child_coords(x, y)
        super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_enter(self, x, y):
        x, y = self.get_child_coords(x, y)
        super().on_mouse_enter(x, y)

    def on_mouse_leave(self, x, y):
        x, y = self.get_child_coords(x, y)
        super().on_mouse_leave(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        x, y = self.get_child_coords(x, y)
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_drag_enter(self, x, y):
        x, y = self.get_child_coords(x, y)
        super().on_mouse_drag_enter(x, y)

    def on_mouse_drag_leave(self, x, y):
        x, y = self.get_child_coords(x, y)
        super().on_mouse_drag_leave(x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        x, y = self.get_child_coords(x, y)
        super().on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_mouse_pan(self, direction, dt):
        self.panning_vector += direction * self.sensitivity * dt


    @vecrec.accept_anything_as_vector
    def get_child_coords(self, screen_coords):
        viewport_origin = self.rect.bottom_left
        viewport_coords = screen_coords - viewport_origin
        child_origin = self.child.rect.bottom_left
        child_coords = child_origin + self.panning_vector + viewport_coords
        return child_coords

    @vecrec.accept_anything_as_vector
    def get_screen_coords(self, child_coords):
        child_origin = self.child.rect.bottom_left
        viewport_origin = self.rect.bottom_left
        viewport_coords = child_coords - child_origin - self.panning_vector
        screen_coords = view_port_coords + viewport_origin
        return screen_coords

    def get_visible_area(self):
        left, bottom = self.get_child_coords(self.rect.left, self.rect.bottom)
        return Rect.from_dimensions(
                left, bottom, self.rect.width, self.rect.height)

    def get_panning_vector(self):
        return self._panning_vector

    def set_panning_vector(self, vector):
        self._panning_vector = vector

        if self._panning_vector.x < self.child.rect.left:
            self._panning_vector.x = self.child.rect.left

        if self._panning_vector.x > self.child.rect.right - self.rect.width:
            self._panning_vector.x = self.child.rect.right - self.rect.width

        if self._panning_vector.y < self.child.rect.bottom:
            self._panning_vector.y = self.child.rect.bottom

        if self._panning_vector.y > self.child.rect.top - self.rect.height:
            self._panning_vector.y = self.child.rect.top - self.rect.height

    @vecrec.accept_anything_as_vector
    def set_center_of_view(self, child_coords):
        # In order to set the center of view, the size of the viewport widget 
        # is needed.  Unfortunately this information is not available until the 
        # viewport has been attached to a root widget.  To allow this method to 
        # be called at any time, the _deferred_center_of_view member is used in 
        # conjunction with do_resize() to cache the desired center of view.

        if self.rect is None:
            self._deferred_center_of_view = child_coords
        else:
            viewport_center = self.rect.center - self.rect.bottom_left
            self.panning_vector = child_coords - viewport_center
            self._deferred_center_of_view = None


Viewport.register_event_type('on_mouse_pan')

@autoprop
class Grid (Widget):
    custom_cell_padding = None
    custom_cell_alignment = 'fill'

    def __init__(self, rows=0, cols=0):
        super().__init__()
        self._children = {}
        self._children_can_overlap = False
        self._grid = drawing.Grid(
                num_rows=rows,
                num_cols=cols,
        )
        self.cell_padding = first_not_none((
                self.custom_cell_padding, self.custom_padding, 0))
        self.cell_alignment = self.custom_cell_alignment

    def __getitem__(self, row_col):
        return self._children[row_col]

    def __setitem__(self, row_col, child):
        row, col = row_col
        self.add(row, col, child)

    def add(self, row, col, child):
        if (row, col) in self._children:
            self._detach_child(self._children[row, col])

        self._attach_child(child)
        self._children[row, col] = child
        self._repack_and_regroup_children()

    def remove(self, row, col):
        child = self._children[row, col]
        self._detach_child(child)
        del self._children[row, col]
        self._repack_and_regroup_children()

    def clear(self):
        for child in self._children.values():
            self._detach_child(child)
        self._children = {}
        self._repack_and_regroup_children()

    def do_claim(self):
        min_cell_rects = {
                row_col: child.claimed_rect
                for row_col, child in self._children.items()
        }
        return self._grid.make_claim(min_cell_rects)

    def do_resize_children(self):
        cell_rects = self._grid.make_cells(self.rect)
        for ij in self._children:
            align_widget_in_box(
                    self._children[ij],
                    cell_rects[ij],
                    self._cell_alignment_func)

    def do_find_children_under_mouse(self, x, y):
        cell = self._grid.find_cell_under_mouse(x, y)
        child = self._children.get(cell)

        if cell is None:
            return
        if child is None:
            return
        if not child.is_under_mouse(x, y):
            return

        yield child

    def get_num_rows(self):
        return self._grid.num_rows

    def set_num_rows(self, new_num):
        self._grid.num_rows = new_num
        self.repack()

    def get_num_cols(self):
        return self._grid.num_cols

    def set_num_cols(self, new_num):
        self._grid.num_cols = new_num
        self.repack()

    def get_padding(self):
        return super().get_padding() + (self.cell_padding,)

    def set_padding(self, all=None, *, horz=None, vert=None,
            left=None, right=None, top=None, bottom=None, cell=None):
        super().set_padding(
                all=all, horz=horz, vert=vert, left=left, right=right,
                top=top, bottom=bottom)
        self._grid.inner_padding = first_not_none((cell, all, 0))
        self.repack()

    def get_cell_padding(self):
        return self._grid.inner_padding

    def set_cell_padding(self, new_padding):
        self._grid.inner_padding = new_padding
        self.repack()

    def get_cell_alignment(self):
        return self._cell_alignment_func

    def set_cell_alignment(self, new_alignment):
        self._cell_alignment_func = drawing.cast_to_alignment(new_alignment)
        self.repack()

    def get_row_height(self, row):
        return self._grid.row_heights[row]

    def set_row_height(self, row, new_height):
        """
        Set the height of the given row.  You can provide the height as an 
        integer or the string 'expand'.
        
        If you provide an integer, the row will be that many pixels tall, so 
        long as all the cells in that row fit in that space.  If the cells 
        don't fit, the row will be just tall enough to fit them.  For this 
        reason, it is common to specify a height of "0" to make the row as 
        short as possible.

        If you provide the string 'expand', the row will grow to take up any 
        extra space allocated to the grid but not used by any of the other 
        rows.  If multiple rows are set the expand, the extra space will 
        be divided evenly between them.
        """
        self._grid.set_row_height(row, new_height)
        self.repack()

    def del_row_height(self, row):
        """
        Unset the height of the specified row.  The default height will be 
        used for that row instead.
        """
        self._grid.del_row_height(row)
        self.repack()

    def get_col_width(self, col):
        return self._grid.col_widths[col]

    def set_col_width(self, col, new_width):
        """
        Set the width of the given column.  You can provide the width as an 
        integer or the string 'expand'.
        
        If you provide an integer, the column will be that many pixels wide, so 
        long as all the cells in that column fit in that space.  If the cells 
        don't fit, the column will be just wide enough to fit them.  For this 
        reason, it is common to specify a width of "0" to make the column as 
        narrow as possible.

        If you provide the string 'expand', the column will grow to take up any 
        extra space allocated to the grid but not used by any of the other 
        columns.  If multiple columns are set the expand, the extra space will 
        be divided evenly between them.
        """
        self._grid.set_col_width(col, new_width)
        self.repack()

    def del_col_width(self, col):
        """
        Unset the width of the specified column.  The default width will be 
        used for that column instead.
        """
        self._grid.del_col_width(col)
        self.repack()

    def get_default_row_height(self):
        return self._grid.default_row_height

    def set_default_row_height(self, new_height):
        """
        Set the default row height.  This height will be used for any rows 
        that haven't been given a specific height.  The meaning of the height 
        is the same as for set_row_height().
        """
        self._grid.default_row_height = new_height
        self.repack()

    def get_default_col_width(self):
        return self._grid.default_col_width

    def set_default_col_width(self, new_width):
        """
        Set the default column width.  This width will be used for any columns 
        that haven't been given a specific width.  The meaning of the width is 
        the same as for set_col_width().
        """
        self._grid.default_col_width = new_width
        self.repack()


@autoprop
class HVBox (Widget):
    custom_cell_padding = None
    custom_cell_alignment = 'fill'
    custom_default_cell_size = 'expand'

    def __init__(self):
        super().__init__()
        self._children = []
        self._children_can_overlap = False
        self._sizes = {}
        self._grid = drawing.Grid()

        self.cell_padding = first_not_none((
                self.custom_cell_padding, self.custom_padding, 0))
        self.cell_alignment = self.custom_cell_alignment
        self.default_cell_size = self.custom_default_cell_size

    def add(self, child, size=None):
        self.add_back(child, size)

    def add_front(self, child, size=None):
        self.insert(child, 0, size)

    def add_back(self, child, size=None):
        self.insert(child, len(self._children), size)

    def insert(self, child, index, size=None):
        self._attach_child(child)
        self._children.insert(index, child)
        self._sizes[child] = size
        self._repack_and_regroup_children()

    def replace(self, old_child, new_child):
        old_index = self._children.index(old_child)
        old_size = self._sizes[old_child]
        with self.hold_updates():
            self.remove(old_child)
            self.insert(new_child, old_index, old_size)

    def remove(self, child):
        self._detach_child(child)
        self._children.remove(child)
        del self._sizes[child]
        self._repack_and_regroup_children()

    def clear(self):
        for child in self._children:
            self._detach_child(child)
        self._children = []
        self._sizes = {}
        self._repack_and_regroup_children()

    def do_claim(self):
        self.do_set_row_col_sizes({
                i: self._sizes[child]
                for i, child in enumerate(self._children)
                if self._sizes[child] is not None
        })
        min_cell_rects = {
                self.do_get_row_col(i): child.claimed_rect
                for i, child in enumerate(self._children)
        }
        return self._grid.make_claim(min_cell_rects)

    def do_resize_children(self):
        cell_rects = self._grid.make_cells(self.rect)
        for i, child in enumerate(self._children):
            box = cell_rects[self.do_get_row_col(i)]
            align_widget_in_box(child, box, self._cell_alignment_func)

    def do_find_children_under_mouse(self, x, y):
        cell = self._grid.find_cell_under_mouse(x, y)
        if cell is None:
            return

        child = self._children[self.do_get_index(*cell)]
        if child is None:
            return
        if not child.is_under_mouse(x, y):
            return

        yield child

    def do_get_index(self, row, col):
        raise NotImplementedError

    def do_get_row_col(self, index):
        raise NotImplementedError

    def do_set_row_col_sizes(self, sizes):
        raise NotImplementedError

    def get_children(self):
        # Return a tuple so the list of children won't be mutable, and so the 
        # caller can't somehow inadvertently change the list of children held 
        # by the HVBox.
        return tuple(self._children)

    def get_padding(self):
        return super().get_padding() + (self.cell_padding,)

    def set_padding(self, all=None, *, horz=None, vert=None,
            left=None, right=None, top=None, bottom=None, cell=None):
        super().set_padding(
                all=all, horz=horz, vert=vert, left=left, right=right,
                top=top, bottom=bottom)
        self._grid.inner_padding = first_not_none((cell, all, 0))
        self.repack()

    def get_cell_padding(self):
        return self._grid.inner_padding

    def set_cell_padding(self, new_padding):
        self._grid.inner_padding = new_padding
        self.repack()

    def get_cell_alignment(self):
        return self._cell_alignment_func

    def set_cell_alignment(self, new_alignment):
        self._cell_alignment_func = drawing.cast_to_alignment(new_alignment)
        self.repack()

    def get_default_cell_size(self):
        raise NotImplementedError

    def set_default_cell_size(self, size):
        raise NotImplementedError


@autoprop
class HBox (HVBox):
    add_left = HVBox.add_front
    add_right = HVBox.add_back

    def do_get_index(self, row, col):
        return col

    def do_get_row_col(self, index):
        return 0, index

    def do_set_row_col_sizes(self, sizes):
        self._grid.col_widths = sizes

    def get_default_cell_size(self):
        return self._grid.default_col_width

    def set_default_cell_size(self, size):
        self._grid.default_col_width = size


@autoprop
class VBox (HVBox):
    add_top = HVBox.add_front
    add_bottom = HVBox.add_back

    def do_get_index(self, row, col):
        return row

    def do_get_row_col(self, index):
        return index, 0

    def do_set_row_col_sizes(self, sizes):
        self._grid.row_heights = sizes

    def get_default_cell_size(self):
        return self._grid.default_row_height

    def set_default_cell_size(self, size):
        self._grid.default_row_height = size


@autoprop
class Stack (Widget):
    """
    Have any number of children, claim enough space for the biggest one, and 
    just draw them all in layers.
    """

    def __init__(self):
        Widget.__init__(self)
        self._children = {} # {child: layer}

    def add(self, widget):
        self.add_front(widget)

    def add_front(self, widget):
        layer = max(self.layers) + 1 if self.layers else 0
        self.insert(widget, layer)

    def add_back(self, widget):
        layer = min(self.layers) - 1 if self.layers else 0
        self.insert(widget, layer)

    def insert(self, widget, layer):
        self._attach_child(widget)
        self._children[widget] = layer
        self._repack_and_regroup_children()

    def remove(self, widget):
        self._detach_child(widget)
        del self._children[widget]
        self._repack_and_regroup_children()

    def clear(self):
        for child in self.children:
            self._detach_child(child)
        self._children = {}
        self._repack_and_regroup_children()

    def do_claim(self):
        return claim_stacked_widgets(*self.children)

    def do_resize_children(self):
        for child in self.children:
            align_widget_in_box(child, self.rect)

    def do_regroup_children(self):
        # If there's only one child, don't bother making an ordered group.  As 
        # I understand it, it's best to use as few groups as possible because 
        # forcing OpenGL to change states is inefficient.

        if len(self) == 1:
            child = next(iter(self.children))
            child.regroup(self.group)
        else:
            for child, layer in self._children.items():
                child.regroup(pyglet.graphics.OrderedGroup(layer, self.group))

    def get_children(self):
        """
        Return a list of the children making up this stack.  The list is sorted 
        such that the widgets in the foreground come first.
        """
        # Cast to a tuple so that basic indexing operations are supported and 
        # so that the list is immutable.
        return sorted(self._children.keys(),
                key=lambda x: self._children[x], reverse=True)

    def get_layers(self):
        return sorted(self._children.values(), reverse=True)


@autoprop
class Deck(Widget):
    """
    Display one of a number of child widgets depending on the state specified 
    by the user.
    """

    def __init__(self, initial_state, **states):
        super().__init__()
        self._current_state = initial_state
        self._previous_state = initial_state
        self._states = {}
        self.add_states(**states)

    def do_claim(self):
        # Claim enough space for the biggest child, so that we won't need to 
        # repack when we change states.  (Also, I can't think of any reason why 
        # you'd want states of different sizes.)
        return claim_stacked_widgets(*self._states.values())

    def add_state(self, state, widget):
        self._remove_state(state)
        self._add_state(state, widget)
        self._repack_and_regroup_children()

    def add_states(self, **states):
        for state, widget in states.items():
            self._remove_state(state)
            self._add_state(state, widget)
        self._repack_and_regroup_children()

    def add_states_if(self, predicate, **states):
        filtered_states = {
                k: w for k,w in states.items()
                if predicate(w)
        }
        self.add_states(**filtered_states)

    def reset_states(self, **states):
        for state in list(self.known_states):
            self._remove_state(state)
        for state, widget in states.items():
            self._add_state(state, widget)
        self._repack_and_regroup_children()

    def reset_states_if(self, predicate, **states):
        filtered_states = {
                k: w for k,w in states.items()
                if predicate(w)
        }
        self.reset_states(**filtered_states)

    def remove_state(self, state):
        self.remove_states(state)

    def remove_states(self, *states):
        for state in states:
            self._remove_state(state)
        self._repack_and_regroup_children()

    def clear(self):
        self.remove_states(*self.known_states)

    def _add_state(self, state, widget):
        widget.unhide() if state == self.state else widget.hide()
        self._states[state] = widget
        self._attach_child(widget)

    def _remove_state(self, state):
        if state in self._states:
            self._detach_child(self._states[state])
            # Unhide the child so it'll show up if the user tries to reattach 
            # it somewhere else.
            self._states[state].unhide(draw=False)
            del self._states[state]

    def get_state(self):
        return self._current_state

    def set_state(self, new_state):
        if new_state not in self.known_states:
            raise ValueError(f"unknown state '{new_state}'")

        self._previous_state = self._current_state
        self._current_state = new_state

        if self._current_state != self._previous_state:
            self._states[self._current_state].unhide()

            # The previous state could've been removed since the state was last 
            # changed.  In this case it will have already been hidden, so we 
            # don't need to do anything.
            try: self._states[self._previous_state].hide()
            except KeyError: pass

    def get_widget(self, state):
        return self._states[state]

    def get_previous_state(self):
        return self._previous_state

    def get_known_states(self):
        return self._states.keys()

