from dearpygui.core import *
from dearpygui.simple import *

with window("Tutorial"):

    add_text("Right Click Me")

    with popup("Right Click Me", "Popup ID", mousebutton=mvMouseButton_Right):
        add_text("A popup")

start_dearpygui()