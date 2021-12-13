import os
import os.path
import subprocess
import functools

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window

buttons = []
test_label = None
selected_index = 0

class GameButton(Button):
    def on_press(self):
        subprocess.run(['bash', f'../apps/{self.text}/run.sh'])

class Menu(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        gamelist = self.ids.gamelist

        first = True
        for f in os.listdir("../apps"):
            if not os.path.isfile(f):
                button = GameButton(text=f, height=80, size_hint_y=None)
                buttons.append(button)
                gamelist.add_widget(button)

        buttons[0].state = 'down'

        global test_label
        test_label = self.ids.testlabel


class MenuApp(App):
    def build(self):
        return Menu()

def selection_up():
    global selected_index, buttons
    buttons[selected_index].state = 'normal'

    if selected_index == 0:
        selected_index = len(buttons) - 1
    else:
        selected_index -= 1

    buttons[selected_index].state = 'down'

def selection_down():
    global selected_index, buttons
    buttons[selected_index].state = 'normal'

    if selected_index == len(buttons) - 1:
        selected_index = 0
    else:
        selected_index += 1

    buttons[selected_index].state = 'down'

def on_joy_hat(win, stickid, axisid, value):
    test_label.text = f'axisid: {str(axisid)} value: {str(value)}'

    if value[1] == 1:
        selection_up()
    elif value[1] == -1:
        selection_down()

def on_joy_axis(win, stickid, axisid, value):
    test_label.text = f'axisid: {str(axisid)} value: {str(value)}'

    if axisid != 1:
        return

    if value[1] > 500:
        selection_up()
    elif value[1] < -500:
        selection_down()

Window.bind(on_joy_hat=on_joy_hat, on_joy_axis=on_joy_axis)

MenuApp().run()
