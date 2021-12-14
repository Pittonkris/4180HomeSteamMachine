import os
import os.path
import subprocess
import functools

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

buttons = []
test_label = None
selected_index = 0

class GameButton(Button):
    def on_press(self):
        subprocess.run(['bash', f'../apps/{self.text}/run.sh'])

class Menu(Widget):
    def move_bg(self, dt):
        self.bg_texture.uvpos = (self.bg_texture.uvpos[0] - (dt / 2), self.bg_texture.uvpos[1] + (dt / 2))
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(1,1,1,0.3))
            Rectangle(texture=self.bg_texture, size=self.size, pos=self.pos)

    def __init__(self, **kwargs):
        self.bg_texture = Image(source="bg.png").texture
        self.bg_texture.wrap = 'repeat'
        self.bg_texture.uvsize = ((1920 / 1080) * 8, -8)

        super().__init__(**kwargs)

        gamelist = self.ids.gamelist

        for f in os.listdir("../apps"):
            if not os.path.isfile(f):
                button = GameButton(text=f, height=80, size_hint_y=None)
                buttons.append(button)
                gamelist.add_widget(button)

        buttons[0].state = 'down'

        global test_label
        test_label = self.ids.testlabel

        Clock.schedule_interval(self.move_bg, 0)


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

def on_joy_button_down(win, stickid, axisid, value):
    pass

def on_joy_button_up(win, stickid, axisid, value):
    pass

Window.bind(on_joy_hat=on_joy_hat, on_joy_button_down=on_joy_button_down, on_joy_button_up=on_joy_button_up)

MenuApp().run()
