import tkinter as tk
from random import randint

class Raindrop:
    def __init__(self, canvas, x, y, speed, length, color='blue'):
        self.x = x
        self.y = y
        self.speed = speed
        self.length = length
        self.canvas = canvas
        self.line = canvas.create_line(self.x, self.y, self.x + 5, self.y+length, fill=color)

    def move(self):
        self.y += self.speed
        self.canvas.move(self.line, 1, self.speed)

        if self.y > 500:
            self.canvas.move(self.line, 0, -(500+self.length))
            self.y -= 500 + self.length


def redraw():
    for drop in drops:
        drop.move()

    root.after(10, redraw)


root = tk.Tk()
root.title("Практика 2")
canvas = tk.Canvas(root, width=700, height=500, bg="black")
canvas.pack()

drops = [Raindrop(canvas, x=randint(-1300, 700), y=randint(0, 700),
                  speed=randint(8, 11), length=randint(5, 23)) for i in range(800)]

redraw()

root.mainloop()