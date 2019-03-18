import pygame as pg
pg.init()
vec = pg.math.Vector2

# Window settings
class Window:
    def __init__(self):
        self.height = 400
        self.width = 600

WINDOW = Window()

# Text box
class TextBox:
    def __init__(self):
        self.height = 1
        self.width = 35

        self.pos = vec(WINDOW.width / 2 - 20, WINDOW.height - 20)

TEXT_BOX = TextBox()


# Text display
class TextDisplay:
    def __init__(self):
        self.height = 22
        self.width = 40

        self.pos = vec(WINDOW.width / 2, WINDOW.height / 2 - 20)

TEXT_DISPLAY = TextDisplay()

class ButtoN:
    def __init__(self):
        self.pos = vec(WINDOW.width / 2 + 110, WINDOW.height - 20)

BUTTON = ButtoN()

# Users
USERS = ["Lalli", "Palli", "LEP"]
