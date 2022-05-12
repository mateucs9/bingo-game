import os
from random import random
import numpy as np
import pdfkit

class CardPrinter():
	def __init__(self, columns):
		self.rows = 3
		self.columns = columns
		self.cell_size = '100px'
		self.cards_per_sheet = 3
		self.html_name = 'bingo_cards.html'
		self.pdf_name = 'bingo_cards.pdf'
		self.css_cell_style = [
			'width:{}'.format(self.cell_size),
			'height:{}'.format(self.cell_size),
			'background-color: beige',
			'border:black',
			'border-width:1px',
			'border-style:solid',
			'font-size: 3rem',
			'font-weight: bold',
			'vertical-align: center',
			'text-align: center'
		]

		self.wkhtml_path = pdfkit.configuration(wkhtmltopdf = os.path.dirname(__file__)+"/wkhtmltopdf.exe")

	def get_cards_html(self, cards_num):
		html = "<div style='margin-bottom:120px; margin-left: 60px;'>"
		count = 1
		for i in range(cards_num):
			data = np.zeros(shape=(3, self.columns))
			for col in range(1, self.columns+1):
				empty_cell = int(random()*(self.rows-1))
				num_range = list(range(col*10+1, col*10+10))
				for row in range(self.rows):
					if row != empty_cell:
						number = num_range[int(random()*len(num_range))]
						data[row][col-1] = number
						num_range.remove(number)
			html += "<div style='border:black; border-size:5px; border-style:solid; margin-top: 30px; padding: 20px; padding-top:0'>"
			html += '<h2>Card num. {}</h2><table style="border-spacing:0; border:black; border-size:5px; border-style:solid; margin-top: 20px">'.format(i+1)
			for row in range(self.rows):
				html += '<tr>'
				for col in range(data.shape[1]):
					if int(data[row][col]) == 0:
						cell = '<img src="empty_cells.png" width={} height={}>'.format(self.cell_size, self.cell_size)
					else:
						cell = int(data[row][col])
					html += "<td style='{}'>{}</td>".format(';'.join(self.css_cell_style), cell)
				html += '</tr>'
			html += '</table></div>'
			if count == self.cards_per_sheet:
				count = 0
				html += "</div><div style='margin-bottom:120px; margin-left: 60px;'>"
			
			count += 1

		html += '</div>'

		#Once we have the full html, we will then save it into a html file
		html_file = open(self.html_name, 'w')
		html_file.write(html)
		html_file.close()

		# This will create pdf from the html and we will use os to open it with the default program ready to be printed
		pdfkit.from_file(self.html_name, self.pdf_name, configuration= self.wkhtml_path, options = {"enable-local-file-access": None})
		os.startfile(self.pdf_name, 'open')

		os.remove(self.html_name)



