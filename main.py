from random import random
import time
from playsound import playsound
from gtts import gTTS
import os
import tkinter as tk


class BingoApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.title('Bingo Game')
		self.geometry('500x500')
		self.resizable(0,0)
		self.colors = {'dark-brown':  "#cb997e", 
						'brown': 	  "#ddbea9", 
						'light-brown': "#ffe8d6",
						'light-green': "#b7b7a4", 
						'green': 	  "#a5a58d", 
						'dark-green':  "#6b705c"}
		self.configure(bg=self.colors['brown'])
		[self.grid_rowconfigure(i, weight=1) for i in range(1)]
		[self.grid_columnconfigure(i, weight=1) for i in range(3)]
		self.total_numbers = 100
		self.numbers_per_row = 10
		self.available_numbers = []
		self.round = 0
		self.language = 'en'
		self.widgets = self.get_start_menu()
	
	def get_start_menu(self):
		tk.Label(self, text="Let's Play!", font=('Calibri', 45, 'bold'), bg=self.colors['brown']).pack(anchor='center', expand=True)
		tk.Button(self, text="Start Game", font=('Calibri', 15, 'bold'), bg='white', command=lambda self=self: self.start_playing()).pack(anchor='center', expand=True)
	
	def start_playing(self):
		self.get_playing_screen()
		self.after(2000, self.draw_number)
	
	
	def clear_screen(self, frame):
		for widget in frame.winfo_children():
			widget.destroy()

	def get_playing_screen(self):
		self.clear_screen(self)
		self.available_numbers = list(range(1, self.total_numbers+4))

		self.round_lbl = tk.Label(self, text='Round: 0', font=('Calibri', 20), bg=self.colors['brown'])
		self.last_draw_lbl = tk.Label(self, text='Last number drawn: -', font=('Calibri', 20), bg=self.colors['brown'])
		self.title_lbl = tk.Label(self, text='Bingo', font=('Calibri', 45), bg=self.colors['brown'])
		self.stop_btn = tk.Button(self, text='Pause game', command=lambda:print('hello'))
		self.numbers_frame = tk.Frame(self, bg=self.colors['brown'], height=400)

		#This will make every cell within the number grid to be the same size
		[self.numbers_frame.grid_rowconfigure(i, weight=1) for i in range(int(self.total_numbers/self.numbers_per_row))]
		[self.numbers_frame.grid_columnconfigure(i, weight=1) for i in range(self.numbers_per_row)]
		
		self.round_lbl.grid(row=0, column=0, pady=10, padx=10)
		self.last_draw_lbl.grid(row=0, column=4, columnspan=2, pady=10, padx=10)
		self.title_lbl.grid(row=1, column=0, columnspan=8, pady=10, padx=10)
		self.stop_btn.grid(row=1, column=6, columnspan=2, pady=10, padx=10)
		self.numbers_frame.grid(row=3, column=0, columnspan=12, rowspan=12, pady=10, padx=10)

		# We are creating the grid where the bingo numbers will be shown
		row = 0
		column = 0
		for i in range(1, self.total_numbers + 1):
			if column + 1 > self.numbers_per_row:
				row += 1
				column = 0
			
			tk.Label(self.numbers_frame, text = str(i), font=('Calibri', 14, 'bold'), relief='raised').grid(row=row, column=column, ipadx=10, sticky='nsew')
			column += 1
		
	
	def update_lbl(self, label, new_value):
		current_text = label.cget('text')
		current_value = current_text.split(': ')[1]
		label.configure(text=current_text.replace(str(current_value), str(new_value)))

	def draw_number(self):
		# We are getting a random index and we use it to take one number out of the available numbers
		number = self.available_numbers[int(random() * len(self.available_numbers))]

		# We update then the current round number and the label for the latest drawn number
		self.round += 1
		self.update_lbl(self.round_lbl, self.round)
		self.update_lbl(self.last_draw_lbl, number)
		
		for widget in self.numbers_frame.winfo_children():
			label = '!label' if number == 1 else '!label{}'.format(number)
			if widget._name == label:
				self.call_out_number(number)
				widget.config(bg='yellow')
				self.update_idletasks()
				self.available_numbers.remove(number)
		
		self.after(2000, self.draw_number)

		
	def call_out_number(self, number):
		mp3_name = 'number.mp3'
		
		# We are storing the voice data in the variable voice and after it's played, it's immediately removed
		voice = gTTS(text=str(number), lang=self.language)
		voice.save(mp3_name)
		playsound(mp3_name)
		os.remove(mp3_name)

		# If the number has 2 digits, this will spell out each of the digits within the number
		if len(str(number)) > 1:
			voice = gTTS(text=' '.join(list(str(number))), lang=self.language)
			voice.save(mp3_name)
			playsound(mp3_name)
			os.remove(mp3_name)


		

app = BingoApp()
app.mainloop()
