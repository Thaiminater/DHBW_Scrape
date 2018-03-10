import openpyxl as op
import dryscrape
from bs4 import BeautifulSoup
dryscrape.start_xvfb()                                                         # Start dryscrape session
session = dryscrape.Session()

def northdata(input,col):
	wb = op.load_workbook(input)
	print type(wb)
	sheet = wb['Sheet1']
	session.visit('https://www.northdata.de/')
	searchinput = session.at_xpath('//*[@id="search"]/div[1]/form/div/div[1]/input')
	searchform = session.at_xpath('//*[@id="search"]/div[1]/form')
	for i in range(2,3):
		firma = sheet.cell(row=i, column=1).value
		searchinput.set('firma')
		searchform.submit()
		#session.render('north.png')
		sheet.cell(row=i, column=col).value = 'Test'
	out = input + '_update.xlsx'
	wb.save(out)

northdata('karlsruhe.xlsx',10)
