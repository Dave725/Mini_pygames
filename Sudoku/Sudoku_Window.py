import pygame as p
import time
from Sudoku_Solver import solve, valid
import tkinter as tk
from tkinter import messagebox

p.init()
p.font.init()
ROWS = 9
COLUMNS = 9
WIDTH = 540
HEIGHT = 540
test_board = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
			  [6, 0, 0, 0, 7, 5, 0, 0, 9],
			  [0, 0, 0, 6, 0, 1, 0, 7, 8],
			  [0, 0, 7, 0, 4, 0, 2, 6, 0],
			  [0, 0, 1, 0, 5, 0, 9, 3, 0],
			  [9, 0, 4, 0, 6, 0, 0, 0, 5],
			  [0, 7, 0, 3, 0, 0, 0, 1, 2],
			  [1, 2, 0, 0, 0, 7, 4, 0, 0],
			  [0, 4, 9, 2, 0, 6, 0, 0, 7]]

# To-do list:
# 1. Random board and reset board
# 2. Potential record system
# 3. Main menu GUI with pyQt5
# 4. Create different mode (time, strike)
# 5. Visualizing solving process

class Grid:
	def __init__ (self, board):
		self.rows = ROWS
		self.cols = COLUMNS
		self.width = WIDTH
		self.height = HEIGHT
		self.board = board
		self.model = None
		self.selected = None
		self.sketch_mode = False
		self.cubes = [[Cube(self.board[i][j], i, j) for j in range(COLUMNS)] for i in range(ROWS)]
		for i in range(ROWS):
			for j in range(COLUMNS):
				if self.board[i][j] != 0:
					self.cubes[i][j].permanent = True

	def draw (self, win):
		# draw grid
		gap = self.width / 9
		for i in range(self.rows + 1):
			if i % 3 == 0 and i != 0:
				thickness = 4
			else:
				thickness = 1
			p.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thickness)  # draw horizontal grid
			p.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thickness)  # draw vertical grid
		# draw cubes
		for i in range(ROWS):
			for j in range(COLUMNS):
				self.cubes[i][j].draw(win)

	def update_model (self):
		model = [[self.cubes[i][j].value for j in range(COLUMNS)] for i in range(ROWS)]
		self.model = model
		return model

	def place (self, val):
		# insert the number
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].value = val
			self.update_model()

		if valid(self.model, val, (row, col)) and solve(self.model):
			return True
		else:
			# self.cubes[i][j].value = 0
			# self.update_model()
			return False

	def sketch (self, num):
		row, col = self.selected
		self.cubes[row][col].set_temp(num)

	def click (self, pos):
		# check the mouse position is on display, pos is relative to origin of pygame window
		if self.width > pos[0] > 0 and 0 < pos[1] < self.height:
			gap = self.width / 9
			x = pos[0] // gap
			y = pos[1] // gap
			return int(y), int(x)
		else:
			return None

	def select (self, x, y):
		for i in range(ROWS):
			for j in range(COLUMNS):
				self.cubes[i][j].selected = False
		self.cubes[x][y].selected = True
		self.selected = (x, y)

	def is_done (self):
		for i in range(ROWS):
			for j in range(COLUMNS):
				if self.cubes[i][j].value == 0:
					return False
		return True

	def clear_val (self):
		row, col = self.selected
		if not self.cubes[row][col].permanent:
			self.cubes[row][col].value = 0

class Cube:
	def __init__ (self, value, row, col):
		self.row = row
		self.col = col
		self.width = WIDTH
		self.height = HEIGHT
		self.value = value
		self.temp1 = False
		self.temp2 = False
		self.temp3 = False
		self.temp4 = False
		self.temp5 = False
		self.temp6 = False
		self.temp7 = False
		self.temp8 = False
		self.temp9 = False
		self.selected = False  # This selected is different to the one in Grid class
		self.permanent = False

	def draw (self, win):
		fnv = p.font.SysFont('comicsans', 40)
		fnt = p.font.SysFont('comicsans', 20)
		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap
		# display sketch
		if self.value == 0:
			if self.temp1:
				text = fnt.render('1', True, (128, 128, 128))
				win.blit(text, (x + 10, y + 8))
			if self.temp2:
				text = fnt.render('2', True, (128, 128, 128))
				win.blit(text, (x + 25, y + 8))
			if self.temp3:
				text = fnt.render('3', True, (128, 128, 128))
				win.blit(text, (x + 42, y + 8))
			if self.temp4:
				text = fnt.render('4', True, (128, 128, 128))
				win.blit(text, (x + 10, y + 25))
			if self.temp5:
				text = fnt.render('5', True, (128, 128, 128))
				win.blit(text, (x + 25, y + 25))
			if self.temp6:
				text = fnt.render('6', True, (128, 128, 128))
				win.blit(text, (x + 42, y + 25))
			if self.temp7:
				text = fnt.render('7', True, (128, 128, 128))
				win.blit(text, (x + 10, y + 42))
			if self.temp8:
				text = fnt.render('8', True, (128, 128, 128))
				win.blit(text, (x + 25, y + 42))
			if self.temp9:
				text = fnt.render('9', True, (128, 128, 128))
				win.blit(text, (x + 42, y + 42))
		# display permanent value
		elif self.value != 0:
			if self.permanent:
				text = fnv.render(str(self.value), True, (0, 0, 0))
				win.blit(text, ((x + (gap / 2 - text.get_width() / 2)), (y + (gap / 2 - text.get_height() / 2))))
			else:
				text = fnv.render(str(self.value), True, (0, 0, 255))
				win.blit(text, ((x + (gap / 2 - text.get_width() / 2)), (y + (gap / 2 - text.get_height() / 2))))
		# highlight selected square
		if self.selected:
			p.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

	def set_temp (self, num):
		if num == 1:
			if self.temp1:
				self.temp1 = False
			else:
				self.temp1 = True
		if num == 2:
			if self.temp2:
				self.temp2 = False
			else:
				self.temp2 = True
		if num == 3:
			if self.temp3:
				self.temp3 = False
			else:
				self.temp3 = True
		if num == 4:
			if self.temp4:
				self.temp4 = False
			else:
				self.temp4 = True
		if num == 5:
			if self.temp5:
				self.temp5 = False
			else:
				self.temp5 = True
		if num == 6:
			if self.temp6:
				self.temp6 = False
			else:
				self.temp6 = True
		if num == 7:
			if self.temp7:
				self.temp7 = False
			else:
				self.temp7 = True
		if num == 8:
			if self.temp8:
				self.temp8 = False
			else:
				self.temp8 = True
		if num == 9:
			if self.temp9:
				self.temp9 = False
			else:
				self.temp9 = True

class Button:
	def __init__ (self, x, y, width, height, fg = (0, 0, 0), bg = (255, 255, 255), text = '', size = 40,
				  font = 'arial'):
		self.fg = fg
		self.bg = bg
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.size = size
		self.font = font
		self.bd = None

	def draw (self, win, outline = None, border = 2):
		self.bd = border
		# Call this method to draw the button on the screen
		if outline:
			p.draw.rect(win, outline,
						(self.x - self.bd, self.y - self.bd, self.width + self.bd * 2, self.height + self.bd * 2), 0)

		p.draw.rect(win, self.bg, (self.x, self.y, self.width, self.height), 0)

		if self.text != '':
			font = p.font.SysFont(self.font, self.size)
			text = font.render(self.text, True, self.fg)
			win.blit(text, (
				self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

	def isOver (self, pos):
		# Pos is the mouse position or a tuple of (x,y) coordinates
		if self.x < pos[0] < self.x + self.width:
			if self.y < pos[1] < self.y + self.height:
				return True

		return False

def format_time ():
	global start
	timer = round(time.time() - start)
	seconds = timer % 60
	minutes = timer // 60
	return str(minutes) + ':' + str(seconds)

def update_win (win):
	win.fill((255, 255, 255))
	global bd, solve_button, write_button, check_button, sketch_button
	# draw time
	fnt = p.font.SysFont('courier', 25)
	text = fnt.render('Time: ' + format_time(), True, (0, 0, 0))
	win.blit(text, (380, 555))
	# draw Grid
	bd.draw(win)
	# draw button
	write_button = Button(20, 550, 60, 40, text = 'Write', size = 20)
	sketch_button = Button(20, 550, 60, 40, text = 'Sketch', size = 20)
	if bd.sketch_mode:
		sketch_button.draw(win, outline = True)
	elif not bd.sketch_mode:
		write_button.draw(win, outline = True)
	check_button = Button(100, 550, 60, 40, text = 'Check', size = 20)
	check_button.draw(win, outline = True)
	solve_button = Button(180, 550, 60, 40, text = 'Solve', size = 20)
	solve_button.draw(win, outline = True)
	p.display.update()

def message_box (subject, content):
	root = tk.Tk()
	root.attributes('-topmost', True)
	root.withdraw()
	tk.messagebox.showinfo(subject, content)

def main (board):
	global bd, start, solve_button, mode_button, check_button
	start = time.time()
	win = p.display.set_mode((540, 600))
	p.display.set_caption("Sudoku")
	bd = Grid(board)
	key = None
	flag = True
	while flag:
		for event in p.event.get():
			if event.type == p.QUIT:
				flag = False
			elif event.type == p.KEYDOWN:
				if event.key == p.K_1:
					key = 1
				if event.key == p.K_2:
					key = 2
				if event.key == p.K_3:
					key = 3
				if event.key == p.K_4:
					key = 4
				if event.key == p.K_5:
					key = 5
				if event.key == p.K_6:
					key = 6
				if event.key == p.K_7:
					key = 7
				if event.key == p.K_8:
					key = 8
				if event.key == p.K_9:
					key = 9
				if event.key == p.K_BACKSPACE:
					bd.clear_val()

			elif event.type == p.MOUSEBUTTONDOWN:
				pos = p.mouse.get_pos()
				if check_button.isOver(pos):
					model = bd.update_model()
					if solve(model):
						message_box('Hooray!', 'There exists a valid solution')
					else:
						message_box('Oh no...', 'Something went wrong')
				elif sketch_button.isOver(pos) or write_button.isOver(pos):
					if bd.sketch_mode:
						bd.sketch_mode = False
					else:
						bd.sketch_mode = True
				elif solve_button.isOver(pos):
					model = bd.update_model()
					solution = solve(model)
					if solution:
						bd.cubes = [[Cube(solution[i][j], i, j) for j in range(COLUMNS)] for i in range(ROWS)]
					else:
						message_box('Unsolved', 'Current board does not have a solution')
				else:
					clicked = bd.click(pos)
					if clicked:
						bd.select(clicked[0], clicked[1])
		if bd.selected and key is not None:
			if bd.sketch_mode:
				bd.sketch(key)
			else:
				bd.place(key)
				if bd.is_done():
					message_box('Game over', 'You have solved the Sudoku. Well done!')
					flag = False
		key = None
		update_win(win)
	GUI()

def custom_board ():
	win = p.display.set_mode((540, 600))
	p.display.set_caption('Custom Window')
	empty = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
	cusbd = Grid(empty)
	key = None
	start_solve = False
	start_button = Button(100, 550, 60, 40, text = 'Start', size = 20)
	while not start_solve:
		win.fill((255, 255, 255))
		start_button.draw(win, outline = True)
		cusbd.draw(win)
		p.display.update()
		for event in p.event.get():
			if event.type == p.KEYDOWN:
				if event.key == p.K_1:
					key = 1
				if event.key == p.K_2:
					key = 2
				if event.key == p.K_3:
					key = 3
				if event.key == p.K_4:
					key = 4
				if event.key == p.K_5:
					key = 5
				if event.key == p.K_6:
					key = 6
				if event.key == p.K_7:
					key = 7
				if event.key == p.K_8:
					key = 8
				if event.key == p.K_9:
					key = 9
				if event.key == p.K_BACKSPACE:
					cusbd.clear_val()
			elif event.type == p.MOUSEBUTTONDOWN:
				pos = p.mouse.get_pos()
				if start_button.isOver(pos):
					start_solve = True
				else:
					clicked = cusbd.click(pos)
					if clicked:
						cusbd.select(clicked[0], clicked[1])
			elif event.type == p.QUIT:
				p.quit()
		if key is not None:
			cusbd.place(key)
		key = None
	board = [[cusbd.cubes[i][j].value for j in range(COLUMNS)] for i in range(ROWS)]
	main(board)

def random_board ():
	# probably need API link or using solve()
	pass

def GUI():
	pass

main(test_board)
