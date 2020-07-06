import pygame as p
import random
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import time

p.init()

class Cube(object):
    def __init__ (self, pos, color = (250, 5, 5)):
        self.pos = pos
        self.color = color
        self.xdirn = 1
        self.ydirn = 0

    def move (self, xdirn, ydirn):
        self.xdirn = xdirn
        self.ydirn = ydirn
        self.pos = (self.pos[0] + self.xdirn, self.pos[1] + self.ydirn)

    def draw (self, surface, head = False):
        global width, rows
        dis = width // rows
        x, y = self.pos[0], self.pos[1]
        p.draw.rect(surface, self.color, (x * dis + 1, y * dis + 1, dis - 2, dis - 2))
        if head:
            p.draw.rect(surface, (148, 0, 211), (x * dis + 1, y * dis + 1, dis - 2, dis - 2))

# the snake object would contain the cube object
class Snake(object):

    def __init__ (self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.xdirn = 0
        self.ydirn = 0
        self.body = []
        self.turns = { }
        self.body.append(self.head)

    def move (self):
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
            p.init()
            keys = p.key.get_pressed()
            for _ in keys:
                if keys[p.K_LEFT]:
                    self.xdirn, self.ydirn = -1, 0
                    self.turns[self.head.pos[:]] = [self.xdirn, self.ydirn]  # create new dictionary item
                elif keys[p.K_RIGHT]:
                    self.xdirn, self.ydirn = 1, 0
                    self.turns[self.head.pos[:]] = [self.xdirn, self.ydirn]
                elif keys[p.K_UP]:
                    self.xdirn, self.ydirn = 0, -1
                    self.turns[self.head.pos[:]] = [self.xdirn, self.ydirn]
                elif keys[p.K_DOWN]:
                    self.xdirn, self.ydirn = 0, 1
                    self.turns[self.head.pos[:]] = [self.xdirn, self.ydirn]

        for index, cube in enumerate(self.body):
            position = cube.pos[:]
            if position in self.turns:
                turn = self.turns[position]  # get the dirn value at that position
                cube.move(turn[0], turn[1])
                if index == len(self.body) - 1:
                    self.turns.pop(position)  # needs to remove the last for some reason
            else:
                # check whether the snake hits the boundary
                global fail
                if cube.xdirn == -1 and cube.pos[0] <= 0:
                    fail = True
                elif cube.xdirn == 1 and cube.pos[0] >= rows - 1:
                    fail = True
                elif cube.ydirn == 1 and cube.pos[1] >= rows - 1:
                    fail = True
                elif cube.ydirn == -1 and cube.pos[1] <= 0:
                    fail = True
                if not fail:
                    cube.move(cube.xdirn, cube.ydirn)

    def addCube (self):
        tail = self.body[-1]
        dx, dy = tail.xdirn, tail.ydirn
        # check the direction and move the tail accordingly
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))
        self.body[-1].xdirn = dx
        self.body[-1].ydirn = dy

    def draw (self, surface):
        for i, cube in enumerate(self.body):
            if i == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)

    def reset (self):
        self.head = Cube((10, 10))
        self.body = []
        self.turns = { }
        self.xdirn = 0
        self.ydirn = 0
        self.body.append(self.head)

# All miscellaneous functions here
def drawGrid (surface):
    global width, rows
    gridsize = width // rows
    x, y = 0, 0
    for i in range(rows):
        x += gridsize
        y += gridsize
        p.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        p.draw.line(surface, (255, 255, 255), (0, y), (width, y))

def updateWin (surface, s, li):
    global width, rows, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(surface)
    highest = record(len(s.body), li)
    p.display.set_caption(f'Current score: {len(s.body)}. Highest score: {highest}')
    timeGUI(surface)
    p.display.update()

def newCube (snake):
    global rows
    position = snake.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # check whether this location is on the snake body
        if len(list(filter(lambda z: z.pos == (x, y), position))) > 0:
            continue
        else:
            break
    return x, y

def message (subject, content):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    tk.messagebox.showinfo(subject, content)

def close (s):
    message('Game Over!', f'Your score is {len(s.body)}')
    s.reset()
    p.display.quit()
    p.quit()

def record (score = 0, line = 2):
    with open("snake record.txt", "r") as f:
        lines = f.readlines()
        x = lines[line].split(': ')
        highest = int(x[-1])
    if score > highest:
        highest = score
        if line == 1:
            lines[line] = f'Easy: {highest}'
        elif line == 2:
            lines[line] = f'Medium: {highest}'
        elif line == 3:
            lines[line] = f'Hard: {highest}'
        with open('record file.txt', 'w') as f:
            f.truncate(0)
            for i in range(len(lines)):
                f.write(lines[i])
    return highest

# main function
def skeleton (w, r, tick, li):
    # set up
    global width, rows, snack, fail, start
    width = w
    win = p.display.set_mode((width, width))
    rows = r
    s = Snake((255, 5, 5), (10, 10))
    snack = Cube(newCube(s), color = (5, 250, 5))
    fail = False
    clock = p.time.Clock()
    start = time.time()
    # main loop
    while True:
        p.time.delay(50)
        clock.tick(tick)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(newCube(s), color = (5, 250, 5))

        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda z: z.pos, s.body[i + 1:])):  # check whether it hits its own body
                fail = True
                break

        if fail:
            close(s)
            break
        else:
            updateWin(win, s, li)

def easy ():
    skeleton(500, 20, 6, 1)

def medium ():
    skeleton(500, 20, 8, 2)

def hard ():
    skeleton(500, 20, 12, 3)

def custom (w, r, s):
    skeleton(w, r, s, 4)

def customGUI ():
    root = tk.Tk()
    root.title('Custom Game')
    canvas = tk.Canvas(master = root, bg = 'black', width = 300, height = 300)
    canvas.pack()

    back = Image.open('custom cover.jpg')
    back = back.resize((300, 300))
    img = ImageTk.PhotoImage(back)
    # bgimg = tk.Label(master=canvas, image = img)
    # bgimg.place(relwidth = 1, relheight = 1)

    frame1 = tk.Frame(master = canvas)
    frame1.place(relx = 0.2, rely = 0.15, relwidth = 0.6, relheight = 0.1)
    label1 = tk.Label(master = frame1, text = 'Width', bg = 'grey')
    label1.place(relwidth = 0.3, relheight = 1)
    entry1 = tk.Entry(master = frame1)
    entry1.place(relx = 0.3, relheight = 1, relwidth = 0.7)

    frame2 = tk.Frame(master = canvas)
    frame2.place(relx = 0.2, rely = 0.35, relwidth = 0.6, relheight = 0.1)
    label2 = tk.Label(master = frame2, text = 'Rows', bg = 'grey')
    label2.place(relwidth = 0.3, relheight = 1)
    entry2 = tk.Entry(master = frame2)
    entry2.place(relx = 0.3, relheight = 1, relwidth = 0.7)

    frame3 = tk.Frame(master = canvas)
    frame3.place(relx = 0.2, rely = 0.55, relwidth = 0.6, relheight = 0.1)
    label3 = tk.Label(master = frame3, text = 'Speed', bg = 'grey')
    label3.place(relwidth = 0.3, relheight = 1)
    entry3 = tk.Entry(master = frame3)
    entry3.place(relx = 0.3, relheight = 1, relwidth = 0.7)

    button = tk.Button(master = canvas, bg = 'green', text = 'Confirm',
                       command = lambda: custom(int(entry1.get()), int(entry2.get()), int(entry3.get())))
    button.place(relx = 0.4, rely = 0.75, relwidth = 0.2, relheight = 0.1)

    root.mainloop()

def timeGUI (win):
    global start
    font = p.font.SysFont('Courier', 20)
    timer = time.time() - start
    text = font.render('{:.3f}s'.format(timer), True, (255, 255, 255))
    win.blit(text, (10, 10))
    pass

def mainGUI ():
    root = tk.Tk()
    root.title('Snake Game Menu')
    canvas = tk.Canvas(master = root, bg = 'black', width = 590, height = 314)
    canvas.pack()

    im = Image.open("snake game cover.png")
    img = im.resize((590, 314))
    bgimg = ImageTk.PhotoImage(img)
    background = tk.Label(master = canvas, image = bgimg)
    background.place(relwidth = 1, relheight = 1)

    frame = tk.Frame(master = canvas, bg = '#94a8a5')
    frame.place(rely = 0.2, relheight = 0.7, relwidth = 0.3, relx = 0.1)

    easybutton = tk.Button(master = frame, text = 'Easy', bg = '#2fde1b', command = easy)
    easybutton.place(relx = 0.25, rely = 0.05, relwidth = 0.5, relheight = 0.15)

    medbutton = tk.Button(master = frame, text = 'Medium', bg = '#37d4ac', command = medium)
    medbutton.place(relx = 0.25, rely = 0.3, relwidth = 0.5, relheight = 0.15)

    hardbutton = tk.Button(master = frame, text = 'Hard', bg = '#94209e', command = hard)
    hardbutton.place(relx = 0.25, rely = 0.55, relwidth = 0.5, relheight = 0.15)

    quitbutton = tk.Button(master = frame, text = 'Quit', bg = '#cc273a', command = root.destroy)
    quitbutton.place(relx = 0.25, rely = 0.8, relwidth = 0.5, relheight = 0.15)

    scoreframe = tk.Frame(master = canvas, bg = '#94a8a5')
    scoreframe.place(relx = 0.55, rely = 0.52, relwidth = 0.2, relheight = 0.3)

    score = f'Highest Score\nEasy: {record(line = 1)}\nMedium: {record()}\nHard: {record(line = 3)}'
    label = tk.Label(master = scoreframe, bg = '#94a8a5', text = score)
    label.place(relx = 0.05, rely = 0.05, relwidth = 0.9, relheight = 0.9)

    custombutton = tk.Button(master = canvas, bg = 'white', text = 'Custom', command = customGUI)
    custombutton.place(relx = 0.75, rely = 0.3, relwidth = 0.12, relheight = 0.075)

    root.mainloop()

mainGUI()

# display time if can
