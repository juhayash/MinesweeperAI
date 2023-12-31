# game.py
from levels import generate_best_level

import random
from pprint import pprint
from functools import partial
from datetime import datetime

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
from tkinter import messagebox
 
msg = 'Click a square, you get a number.\
That number is the number of how many mines are surrounding it.\
If you find the mine, you can open "unopened" squares around it, opening more areas.'

class Application(tk.Frame):

	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.grid()
		self.initialize_variables()
		self.draw_main_frame()
		self.set_best_level() # set the best level

	def initialize_variables(self):
		self.level = tk.StringVar(value='easy') # level is initially set as easy
		self.level_dict = {'easy': 'easy', 'medium': 'medium', 'hard': 'hard'}
		self.mine_dict = {'easy': 8, 'medium': 10, 'hard': 12}
		self.highscore = 0
    
	def draw_main_frame(self):
		self.main_frame = self.create_frame(self, 345, 485, row=0, column=0) # height = 485
		self.logo = tk.Label(self.main_frame, image=minesweeper_logo)
		self.logo.grid(row=0, column=0, columnspan=6, padx=22, pady=40)
		self.draw_level_frame()
		self.draw_buttons()

	def draw_level_frame(self):
		self.level_frame = self.create_frame(self.main_frame, 250, 60, row=2, column=1, columnspan=4, pady=15)
		for i, (text, value) in enumerate(self.level_dict.items()):
			tk.Radiobutton(self.level_frame, text=text, value=value, variable=self.level).grid(row=0, column=i, pady=6, padx=7)

	def draw_buttons(self):
		self.create_button(self.main_frame, 'Start Game', self.start_playing, row=3, column=2, columnspan=2, pady=10)
		self.create_button(self.main_frame, 'Help', self.help_window, row=4, column=2, columnspan=2, pady=10)
		self.create_button(self.main_frame, 'Quit', self.master.destroy, row=5, column=2, columnspan=2, pady=10)
		self.create_button(self.main_frame, 'Best Level', self.set_best_level, row=6, column=2, columnspan=2, pady=10)
  
	def create_frame(self, parent, width, height, **grid_options):
		frame = tk.Frame(parent, width=width, height=height)
		frame.grid(**grid_options)
		frame.grid_propagate(False)
		return frame
 
	def create_button(self, parent, text, command, **grid_options):
		btn = ttk.Button(parent, text=text, width=15, command=command)
		btn.grid(**grid_options)
  
	def set_best_level(self):
		best_level = generate_best_level()
		self.level.set(best_level)
    
	def draw_game_frames(self):
		self.header_frame = tk.Frame(self, width=345, height=85)
		self.body_frame = tk.LabelFrame(self, width=345, height=365, bg='gray70',
						relief=tk.RIDGE) # chnage height = 400 to height = 365 according to 
  										 # the size of the grame of the game

		self.header_frame.grid(row=0, column=0)
		self.body_frame.grid(row=1, column=0)

		self.header_frame.grid_propagate(False)
		self.body_frame.grid_propagate(False)

	def draw_header_frame(self):
		self.score_frame = tk.LabelFrame(self.header_frame, width=130, height=85, bg='dodgerblue',
					relief=tk.FLAT)
		self.score_frame.grid(row=0, column=0, rowspan=2)

		self.current_score_frame = tk.Frame(self.score_frame, width=80, height=85, bg='white')
		self.current_score_frame.grid(row=0, column=0, rowspan=2)

		self.highscore_frame = tk.Frame(self.score_frame, width=50, height=41, bg='white')
		self.highscore_frame.grid(row=1, column=1, sticky='W')

		self.timer_frame = tk.Frame(self.header_frame, width=215, height=35, bg='dodgerblue')
		self.timer_frame.grid(row=0, column=1)

		self.others = tk.Frame(self.header_frame, width=215, height=50, bg='white')
		self.others.grid(row=1, column=1)

		self.score_frame.grid_propagate(False)
		self.current_score_frame.grid_propagate(False)
		self.highscore_frame.grid_propagate(False)
		self.timer_frame.grid_propagate(False)
		self.others.grid_propagate(False)

		self.score_label = tk.Label(self.current_score_frame, font=('verdana', 42, 'bold'),
						fg='dodgerblue3', text='0', width=2, bg='white')
		self.score_label.grid(row=0, column=0, pady=8)

		self.highscore_label = tk.Label(self.highscore_frame, font=('verdana', 24), fg='#E8175D',
						text=self.highscore, width=2, bg='white', anchor='w')
		self.highscore_label.grid(row=0, column=0, pady=2)

		self.timer_label = tk.Label(self.timer_frame, font=('verdana', 14), fg='black',
						text='00:00:00', width=10, bg='white')
		self.timer_label.grid(row=0, column=0, padx=55, pady=3)

		self.others_label = tk.Label(self.others, font=('verdana', 12), fg='black',
						width=10, bg='white')
		self.others_label.grid(row=0, column=0, pady=14, padx=110)

	# he start_playing method initializes the game based on the selected level.
	def start_playing(self):
		self.main_frame.destroy()

		self.draw_game_frames()
		self.draw_header_frame()

		self.score = 0
		self.buttons_list = []
		self.draw_cells()

		# Retrieves the current game level
		m = self.level.get()
		# Sets the number of mines based on the selected level
		self.numMines = self.mine_dict[m]
		self.others_label['text'] = f'Mines : {self.numMines}'
		# Calls start_game method to set up the game board
		self.start_game()
		
	def draw_cells(self):
		for row in range(9):
			buttons = []
			for col in range(9):
				if row == 0:
					pady = 3
				else:
					pady = 0
				btn = tk.Button(self.body_frame, text=f'', width=2, height=1,
						relief=tk.RAISED, command = partial(self.check_cell, row, col),
						highlightthickness=4, fg='blue', font=('verdana'),
						highlightcolor="#37d3ff", 
						highlightbackground="#37d3ff", 
						borderwidth=3)
				btn.grid(row=row, column=col, padx=(0,0), pady=(pady,0))
				btn.bind('<Button-3>', partial(self.mark_bomb, row, col))
				buttons.append(btn)
			self.buttons_list.append(buttons)

	# This method initializes some variables for the game and calls place_mines
	def start_game(self):
		self.board = [[' ' for i in range(9)] for j in range(9)] # Initializing the game board
		self.mines = [] # List to keep track of where the mines are placed
		self.flags = [[False for _ in range(9)] for _ in range(9)] # Initialize flag grid with False values

		self.first_click = True
		self.gameRunning = True
		self.score = 0

		self.place_mines(self.numMines)

		self.start_time = datetime.now()
		self.timer_label['text'] = '00:00:00'
		self.after(1000, self.update_timer)

	# This method is responsible for placing mines on the board randomly
	def place_mines(self, num):
		if num > 0:
			x = random.randint(0, 8)
			y = random.randint(0, 8)

			if (x,y) in self.mines:
				self.place_mines(num)
			else:
				self.board[x][y] = 'X'
				self.mines.append((x,y))
				self.place_mines(num-1)
				# print("Mines placed at:", self.mines)


	def check_cell(self, x, y):
		if not self.isValidCell(x, y):
			return

		if self.first_click:
			# Ensure first click is not a mine.
			while self.isMine(x, y):
				self.board[x][y] = ' '  # Reset current cell
				self.mines.remove((x, y))  # Remove the mine coordinate from mines list
				self.place_mines(1)  # Place a new mine somewhere else
			self.first_click = False  # Set first_click to False

		btn = self.buttons_list[x][y]

		if btn['relief'] == tk.RAISED:
			adjacent_mines = self.checkAdjecentCells(x, y)

			if adjacent_mines == -1:
				# It's a mine
				btn.config(width=24, height=26)
				btn['bg'] = 'red'
				btn['image'] = mine_icon
				self.showAllMines()
				self.game_lost()
			else:
				# Update score only for newly clicked cells.
				self.update_score(1)

		# print(f"Cell at ({x}, {y}) clicked")


	def isMine(self, row, col):
		is_mine = True if (row, col) in self.mines else False
		# print(f"Cell at ({row}, {col}) is a mine: {is_mine}")
		return is_mine


	def isValidCell(self, row, col):
		is_valid = (row >= 0 and row < 9) and (col >= 0 and col < 9)
		# print(f"Cell at ({row}, {col}) is valid: {is_valid}")
		return is_valid


	def updateAdjecentCells(self, btn, row, col):
		num = self.checkAdjecentCells(row, col)
		if num:
			if num == 1:
				color = 'green'
			elif num == 2:
				color = 'blue'
			elif num >=3:
				color = 'red'
			btn['fg'] = color
			btn['text'] = str(num)

	def update_score(self, point):
		self.score += point
		self.score_label['text'] = self.score
		if self.score >= self.highscore:
			self.highscore = self.score
			self.highscore_label['text'] = self.highscore

	def update_timer(self):
		if self.gameRunning:
			now =  datetime.now()
			minutes, seconds = divmod((now - self.start_time).total_seconds(),60)
			string = f"00:{int(minutes):02}:{round(seconds):02}"
			self.timer_label['text'] = string
			self.after(1000, self.update_timer)

	"""
	1. Initialize a mine variable to 0.
	2. Loop through the adjacent cells around (row, col).
	3. If an adjacent cell contains a mine,
		increment the mine variable.
	4. If no mines are adjacent,
		attempt to open the surrounding cells.
	5. If there are adjacent mines,
		return the count.
	"""
	def checkAdjecentCells(self, row, col):
		# initialize mine to 0
		mine = 0
		if not self.isValidCell(row, col):
			return 0

		# If it's a mine, return -1 to signal a mine.
		if self.isMine(row, col):
			return -1

		btn = self.buttons_list[row][col]
		# If the button was already clicked, return 0 to avoid re-checking.
		if btn['relief'] == tk.FLAT:
			return 0

		# Check adjacent cells for mines.
		for i in range(row - 1, row + 2):
			for j in range(col - 1, col + 2):
				if self.isValidCell(i, j) and self.isMine(i, j):
					mine += 1

		# Update the current cell and expand further if no adjacent mines.
		btn.config(relief=tk.FLAT, bg='gray')
		if mine == 0:
			for i in range(row - 1, row + 2):
				for j in range(col - 1, col + 2):
					self.checkAdjecentCells(i, j)
		else:
			btn['text'] = str(mine)

		return mine

 		# # increment mine count if a mine is adjacent
		# for i in range(row-1, row+2):
		# 	for j in range(col-1, col+2):
		# 		if not (row == i and col == j):
		# 			if self.isValidCell(i, j):
		# 				if self.isMine(i,j):
		# 					mine += 1 

		# if mine == 0:  # No adjacent mines
		# 	score = 0
		# 	for i in range(row-1, row+2):
		# 		for j in range(col-1, col+2):
		# 			if not (row == i and col == j):
		# 				if self.isValidCell(i, j):
		# 					btn = self.buttons_list[i][j]
		# 					if btn['relief'] == tk.RAISED:
		# 						btn.config(relief=tk.FLAT)
		# 						btn['bg'] = 'gray'
		# 						score += 1
		# 	self.update_score(score)  # Update score
		# else:  # There are adjacent mines
		# 	print(f"Number of mines around cell at ({row}, {col}): {mine}")
		# 	return mine # Return the number of adjacent mines

	def showAllMines(self):
		for x,y in self.mines:
			btn = self.buttons_list[x][y]
			if btn['relief'] == tk.RAISED:
				btn.config(relief=tk.FLAT)
				btn['bg'] = 'red'
				btn.config(width=24, height=26)
				# mine_icon = PhotoImage(file="icons/mine.png")
				btn['image'] = mine_icon

	def redraw_body_frame(self):
		self.body_frame.destroy()
		self.body_frame = tk.LabelFrame(self, width=345, height=400, bg='gray70',
						relief=tk.RIDGE)
		self.body_frame.grid(row=1, column=0)
		self.body_frame.grid_propagate(False)
		
		self.score = 0
		self.buttons_list = []
		self.draw_cells()
		self.start_game()

	def game_lost(self):
		self.gameRunning = False
		self.game_lost_window()

	def restart_game(self):
		self.top.destroy()
		self.start_game()
		self.after(100, self.redraw_body_frame)
		self.score_label['text'] = 0
		self.first_click = True


	def go_home(self):
		self.top.destroy()
		self.highscore = 0

		self.header_frame.destroy()
		self.body_frame.destroy()
		self.draw_main_frame()

	def game_lost_window(self):
		self.top = tk.Toplevel(self)
		self.top.geometry('200x100+580+355')
		self.top.title('Minesweeper')
		self.top.resizable(0,0)
		self.top.protocol("WM_DELETE_WINDOW", self.master.destroy)

		# sad_face = PhotoImage(file='icons/sad.png')
		tk.Label(self.top, text=' You Lost', image=sad_face, fg='black',
				font=('verdana', 10, 'bold'), compound=tk.LEFT,
				).grid(row=0, column=0, padx=50, pady=5,
						columnspan=4)

		ttk.Button(self.top, text='Play Again', command=self.restart_game, 
				width=10).grid(row=1,column=0, columnspan=2, pady=15)

		ttk.Button(self.top, text='Home', command=self.go_home, 
				width=8).grid(row=1,column=2, columnspan=2, pady=15)

	def help_window(self):
		win = tk.Toplevel(self)
		win.geometry('200x120+580+355')
		win.title('Minesweeper')
		win.resizable(0,0)

		tk.Label(win, text=msg, wraplength=180, anchor='w').grid(row=0, column=0, padx=10, pady=4)

	def mark_bomb(self, row, col, event):
		if self.gameRunning:
			btn = self.buttons_list[row][col]
			self.flags[row][col] = not self.flags[row][col] # Toggle the flag state for the clicked cell

			if btn['relief'] == tk.RAISED: # Ensure the cell is not already opened
				if self.flags[row][col]:
					btn.config(width=24, height=26)
					btn['bg'] = 'red'
					btn['image'] = flag_icon
					# btn.config(image=bomb_icon, relief=tk.SUNKEN) # Mark as bomb_icon

			if not self.flags[row][col]:
				btn.config(text='', relief=tk.RAISED, background='gray70') # Reset to original state
			# if btn['relief'] == tk.RAISED: # Ensure the cell is not already opened
			# 	btn.config(image=bomb_icon, relief=tk.SUNKEN)


if __name__ == '__main__':
	root = tk.Tk()
	ttk.Style().theme_use('clam')
	root.title('Minesweeper')
	root.geometry('345x450+500+150')

	mine_icon = PhotoImage(file='icons/mine.png')
	flag_icon = PhotoImage(file='icons/bomb_icon.png')

	minesweeper_logo = PhotoImage(file='icons/logo.png')
	sad_face = PhotoImage(file='icons/sad.png')

	app = Application(master=root)
	app.mainloop()