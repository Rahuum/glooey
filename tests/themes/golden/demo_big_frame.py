#!/usr/bin/env python3

import pyglet
import demo_helpers
import glooey.themes.golden as golden

window = pyglet.window.Window()
gui = golden.Gui(window)
frame = golden.BigFrame()
gui.add(frame)

@demo_helpers.interactive_tests(window, gui.batch)
def test_big_frame():
    frame.clear()
    yield "Empty frame."

    label = golden.Label("Lorem ipsum")
    label.alignment = 'center'
    frame.add(label)
    yield "One line of text."

    label.text = "Lorem ipsum\ndolor sit amet."
    yield "Two lines of text."

pyglet.app.run()


