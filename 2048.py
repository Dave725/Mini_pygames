import tkinter as tk
import Color2048 as c
import pygame as p

WIDTH = 600
ROWS = 4
surface = p.display.set_mode(size = (WIDTH,WIDTH))
p.display.set_caption('Normal')

def mainGUI():
    root = tk.Tk()
    root.geometry('600x600')
    root.title('2048')


def drawGrid(surface):
    gridsize = WIDTH // ROWS
    x, y = 0, 0
    for i in range(4):
        x += gridsize
        y += gridsize
        p.draw.line(surface, (255, 255, 255), (x, 0), (x, WIDTH))
        p.draw.line(surface, (255, 255, 255), (0, y), (WIDTH, y))

def updateWin(win):
    pass

def skeleton():
    pass
