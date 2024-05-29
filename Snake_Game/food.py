from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape('turtle')
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.color("navy")
        self.speed('fastest')
        self.refresh()

    def refresh(self):
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.teleport(random_x, random_y)
