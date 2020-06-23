"""
Simple Hello World app to test Buildozer Action.

It builds Kivy app with file main.kv.
"""

from kivy.app import App
from kivy.lang import Builder


class MainApp(App):
    def build(self):
        return Builder.load_file("main.kv")


if __name__ == "__main__":
    MainApp().run()
