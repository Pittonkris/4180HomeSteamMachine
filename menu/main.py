import os
import os.path
import subprocess

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget

class GameButton(Button):
    def on_press(self):
        subprocess.run(['bash', f'../apps/{self.text}/run.sh'])

class Menu(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        gamelist = self.ids.gamelist

        for f in os.listdir("../apps"):
            if not os.path.isfile(f):
                gamelist.add_widget(GameButton(text=f, height=80, size_hint_y=None))

        # self.ids.gamelist.add_widget(Button(text="Test button"))
        # self.ids.gamelist.add_widget(Button(text="Test button"))

class MenuApp(App):
    def build(self):
        return Menu()

MenuApp().run()
