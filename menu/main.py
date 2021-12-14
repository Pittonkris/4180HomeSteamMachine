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

class GameButton(Button):
    def on_press(self):
        subprocess.Popen(['bash', f'../apps/{self.text}/run.sh'])

class Menu(Widget):
    buttons = []
    selected_index = 0

    def refresh_list(self):
        gamelist = self.ids.gamelist

        for f in os.listdir("../apps"):
            if not os.path.isfile(f) and not f.startswith('.'):
                button = GameButton(text=f, height=80, size_hint_y=None)
                buttons.append(button)
                gamelist.add_widget(button)

    def move_bg(self, dt):
        self.bg_texture.uvpos = (self.bg_texture.uvpos[0] - (dt / 2), self.bg_texture.uvpos[1] + (dt / 2))
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(1,1,1,0.4))
            Rectangle(texture=self.bg_texture, size=self.size, pos=self.pos)

    def selection_up():
        self.buttons[self.selected_index].state = 'normal'

        if self.selected_index == 0:
            self.selected_index = len(self.buttons) - 1
        else:
            self.selected_index -= 1

        self.buttons[self.selected_index].state = 'down'

    def selection_down():
        self.buttons[self.selected_index].state = 'normal'

        if self.selected_index == len(self.buttons) - 1:
            self.selected_index = 0
        else:
            self.selected_index += 1

        self.buttons[self.selected_index].state = 'down'

    def on_joy_button_down(win, stickid, buttonid):
        if not Window.focus: return

        if buttonid == 11:
            selection_up()
        elif buttonid == 12:
            selection_down()
        elif buttonid == 0:
            self.buttons[self.selected_index].on_press()

    def __init__(self, **kwargs):
        self.bg_texture = Image(source="bg.png").texture
        self.bg_texture.wrap = 'repeat'
        self.bg_texture.uvsize = ((1920 / 1080) * 8, -8)

        super().__init__(**kwargs)

        self.refresh_list()

        self.buttons[0].state = 'down'

        Clock.schedule_interval(self.move_bg, 0)

        Window.bind(on_joy_button_down=self.on_joy_button_down)


class MenuApp(App):
    def build(self):
        return Menu()

MenuApp().run()
