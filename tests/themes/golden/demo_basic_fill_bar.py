#!/usr/bin/env python3

import pyglet
import glooey.themes.golden as golden
import demo_helpers

window = pyglet.window.Window()
gui = golden.Gui(window)
bar = golden.BasicFillBar()
bar.alignment = 'center'
gui.add(bar)

@demo_helpers.interactive_tests(window, gui.batch) #
def test_basic_fill_bar():
    colors = 'red', 'yellow', 'lime', 'green', 'teal', 'blue'
    fractions = [i/5 for i in range(6)]

    for color in colors:
        bar.color = color
        for frac in fractions:
            bar.fraction_filled = frac
            yield f"{int(100 * bar.fraction_filled)}% {color}."

pyglet.app.run()
