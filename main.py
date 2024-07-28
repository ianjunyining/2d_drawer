import turtle
from src.drawer import Drawer

turtle.hideturtle()
turtle.speed(0)

screen = turtle.Screen()
screen.tracer(0)
drawer = Drawer(screen)
screen.onclick(drawer.onclick)
screen.mainloop()
