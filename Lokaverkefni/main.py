from tkinter import *
from settings import *

root = Tk()

class ChatApp:
    def __init__(self):
        root.geometry(str(WINDOW_SIZE["width"]) + "x" + str(WINDOW_SIZE["height"]))
        root.resizable(width=False, height=False)

    def clear_window(self):
        for a in root.winfo_children():
            a.destroy()

    def make_window(self):
        self.clear_window()


        Label(root, text="Helo wrld!", bg="WHITE", width=TEXT_DISPLAY_SIZE["width"], height=TEXT_DISPLAY_SIZE["height"]).place(x=WINDOW_SIZE["width"]/2, y=WINDOW_SIZE["height"]/2, anchor=CENTER)

        Text(root, width = TEXT_BOX_SIZE["width"], height = TEXT_BOX_SIZE["height"]).place(x=WINDOW_SIZE["width"]/2, y=WINDOW_SIZE["height"]-20, anchor=CENTER)


h = ChatApp()
h.make_window()
root.mainloop()
