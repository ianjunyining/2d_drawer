from functools import partial
import turtle
from src.drawer import Drawer

turtle.hideturtle()
turtle.speed(0)

screen = turtle.Screen()
screen.tracer(0)
drawer = Drawer(screen)
screen.onclick(drawer.onclick)
screen.onkeypress(drawer.onkeyup, "Up")
screen.onkeypress(drawer.onkeydown, "Down")
screen.onkeypress(drawer.onkeyleft, "Left")
screen.onkeypress(drawer.onkeyright, "Right")
screen.onkeypress(drawer.onkeyupbig, "w")
screen.onkeypress(drawer.onkeydownbig, "s")
screen.onkeypress(drawer.onkeyleftbig, "a")
screen.onkeypress(drawer.onkeyrightbig, "d")
screen.onkeypress(drawer.onkeydelete, "BackSpace")
screen.listen()
screen.mainloop()
