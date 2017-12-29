from random import randint
from tkinter import *

WIDTH = 800
HEIGHT = 300
SEG_SIZE = 20
IN_GAME = True

def create_block():
    global BLOCK
    posx = SEG_SIZE * (randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE))
    posy = SEG_SIZE * (randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE))

    BLOCK = c.create_oval(posx, posy,
                          posx + SEG_SIZE,
                          posy + SEG_SIZE,
                          fill="red")

def notif(value):
    output.delete("0.0","end")
    output.insert("0.0",value)

def main():
    global IN_GAME

    if IN_GAME:
        s.move()

        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        if x1 < 0:
            x1 = WIDTH - 20
            x2 = WIDTH
            c.coords(s.segments[-1].instance, x1, y1, x2, y2)

        elif x2 > WIDTH:
            x1 = 0
            x2 = 20
            c.coords(s.segments[-1].instance, x1, y1, x2, y2)

        elif y1 < 0:
            y1 = HEIGHT - 20
            y2 = HEIGHT
            c.coords(s.segments[-1].instance, x1, y1, x2, y2)

        elif y2 > HEIGHT:
            y1 = 0
            y2 = 20
            c.coords(s.segments[-1].instance, x1, y1, x2, y2)

        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            s.score += 1
            print(s.score)
            root.update_idletasks()
            c.delete(BLOCK)
            print()
            create_block()

        else:
            for index in range(len(s.segments) - 1):
                if c.coords(s.segments[index].instance) == head_coords:
                    IN_GAME = False


        root.after(100, main)

    else:
        c.create_text(WIDTH / 2, HEIGHT / 2,
                      text="GAME OVER!",
                      font="Arial 20",
                      fill="#ff0000")


class Segment():
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill='#333333')


class Snake():
    def __init__(self, segments):
        self.segments = segments
        self.turns = {"Down": (0, 1), "Right": (1, 0), "Up": (0, -1), "Left": (-1, 0)}
        self.vector = self.turns["Right"]
        self.score = 1
    def move(self):
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)

        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0] * SEG_SIZE,
                 y1 + self.vector[1] * SEG_SIZE,
                 x2 + self.vector[0] * SEG_SIZE,
                 y2 + self.vector[1] * SEG_SIZE)

    def change_direction(self, event):
        if event.keysym in self.turns:
            if self.turns[event.keysym] == self.turns["Up"] and self.vector != self.turns["Down"]:
                self.vector = self.turns[event.keysym]
            elif self.turns[event.keysym] == self.turns["Right"] and self.vector != self.turns["Left"]:
                self.vector = self.turns[event.keysym]
            elif self.turns[event.keysym] == self.turns["Down"] and self.vector != self.turns["Up"]:
                self.vector = self.turns[event.keysym]
            elif self.turns[event.keysym] == self.turns["Left"] and self.vector != self.turns["Right"]:
                self.vector = self.turns[event.keysym]

    def add_segment(self):
        last_seg = c.coords(self.segments[0].instance)

        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

        notif(self.score)


root = Tk()
root.title('Snake')

c = Canvas(root, width=WIDTH, height=HEIGHT, bg='#dedede')
c.grid()

c.focus_set()

segments = [Segment(SEG_SIZE, SEG_SIZE),
            Segment(SEG_SIZE*2, SEG_SIZE),
            Segment(SEG_SIZE*3, SEG_SIZE)]
s = Snake(segments)

output = Text(root, bg="#fff", font="Arial 14", width=45, height=3)
output.insert("0.0",'0')
output.grid(row=3, columnspan=8)

c.bind("<KeyPress>", s.change_direction)

create_block()
main()

root.mainloop()
