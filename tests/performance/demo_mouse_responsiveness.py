#!/usr/bin/env python3

"""\
Test how smoothly mouse events are handled by a large number of widgets.

This demo fills the screen with a grid of 4x4 px widgets that change color in 
response to rollover events.  The test is to see how responsive the widgets 
are.

Note that these color-changing widgets are custom-written to be simple and 
performant.  If this test were to use Button widgets instead, it would be a 
lot less responsive because Button has a lot more repacking and regrouping 
overhead in order to be flexible.  Since filling up a screen like this is not 
the intended use-case for buttons, I think it's fair to use a custom-written 
widget that allows mouse-responsiveness to come to the forefront.

It is important to note that this test uses a Grid to organize the widgets, and 
Grid uses a custom algorithm to detect mouse events.  The default algorithm (as 
implemented in Widget) involves an O(N) search for children that are under the 
mouse.  Grid instead searches for the row under the mouse, then for the column 
under the mouse, which is effectively O(√N).  That said, this layout is totally 
flat, and a "real" GUI would probably be much more hierarchical.  In that case, 
the search for widgets under the mouse would probably approach O(log(N))."""

import pyglet
import glooey
from pprint import pprint

print(__doc__)

window = pyglet.window.Window()
batch = pyglet.graphics.Batch()

class TestButton(glooey.Clickable):

    def __init__(self):
        super().__init__()
        self.rectangle = None

    def do_claim(self):
        return 4, 4

    def draw(self):
        if self.rectangle is None:
            self.rectangle = glooey.drawing.Rectangle(
                    rect=self.rect,
                    color='red',
                    batch=self.batch,
                    group=self.group,
                    usage='dynamic',
            )
        else:
            self.rectangle.unhide()

    def undraw(self):
        if self.rectangle is not None:
            self.rectangle.hide()

    def on_rollover(self, new_state, old_state):
        if new_state == 'base':
            self.rectangle.color = 'red'
        if new_state == 'over':
            self.rectangle.color = 'yellow'
        if new_state == 'down':
            self.rectangle.color = 'blue'



gui = glooey.Gui(window, batch=batch)
grid = glooey.Grid()

for i in range(window.height//4):
    for j in range(window.width//4):
        grid.add(i, j, TestButton())

gui.add(grid)
pyglet.app.run()

