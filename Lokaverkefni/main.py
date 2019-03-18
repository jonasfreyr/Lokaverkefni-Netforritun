'''
from tkinter import *
from settings import *

root = Tk()

class ChatApp:
    def __init__(self):
        root.geometry(str(WINDOW.width) + "x" + str(WINDOW.height))
        root.resizable(width=False, height=False)

    def clear_window(self):
        for a in root.winfo_children():
            a.destroy()

    def make_window(self):
        self.clear_window()


        Label(root, text="Helo wrld!", bg="WHITE", width=TEXT_DISPLAY.width, height=TEXT_DISPLAY.height).place(x=TEXT_DISPLAY.pos.x, y=TEXT_DISPLAY.pos.y, anchor=CENTER)

        Entry(root, width = TEXT_BOX.width).place(x=TEXT_BOX.pos.x, y=TEXT_BOX.pos.y, anchor=CENTER)

        Button(root, text="Send").place(x=BUTTON.pos.x, y=BUTTON.pos.y, anchor=CENTER)

h = ChatApp()
h.make_window()
root.mainloop()
'''

'''
kivy
kivy.deps.sdl2
kivy.deps.glew
kivy.deps.gstreamer
kivy.deps.angle
'''

'''
import kivy
kivy.require("1.8.0")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1

        self.add_widget(Label(text="Shat"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Button(text="Send"))


class ChatApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    ChatApp().run()
'''

import site, sys, os
print(os.path.dirname(sys.executable))