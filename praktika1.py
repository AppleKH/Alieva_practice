from tkinter import *
from math import *

root = Tk()
root.title("Практика 1")
root.geometry("600x600")


def paint(event):
    x1, y1 = (event.x - 3), (event.y - 3)
    x2, y2 = (event.x + 3), (event.y + 3)
    color = "black"
    wn.create_oval(x1, y1, x2, y2, fill=color, outline=color)


wn = Canvas(root, width=600, height=600, bg='white')
wn.bind('<B1-Motion>', paint)
wn.pack()

radius = 200
center = 300, 300
wn.create_oval(center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius, outline="black", width=2)


class Point:
    def __init__(self, canvas, center, dist):
        self.angle = 0
        self.radius = 5
        self.canvas = canvas
        self.center = center
        self.dist = dist
        self.x, self.y = self.p2c()
        self.shape = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius,
                                        self.y + self.radius, fill='black')
        self.update()

    def update(self):
        new = self.p2c()
        self.canvas.move(self.shape, new[0] - self.x, new[1] - self.y)
        (self.x, self.y) = new
        self.canvas.after(5, self.update)
        self.angle += 0.03


    def p2c(self):
        return cos(self.angle) * self.dist + self.center[0], sin(self.angle) * self.dist + self.center[1]


point = Point(wn, (300, 300), 200)

root.mainloop()