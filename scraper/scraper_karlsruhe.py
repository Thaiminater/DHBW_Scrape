import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time
import xlsxwriter
import pdb
dryscrape.start_xvfb()									# Start dryscrape session
session = dryscrape.Session()

workbook = xlsxwriter.Workbook('karlsruhe.xlsx')
ws = workbook.add_worksheet()

with open("dhbw_karlsruhe_2018.html") as response:
	soup = BeautifulSoup(response)

for company in soup.find_all("tr",class_="googleMapsCoordinates",limit = 2):
	for link in company.find_all('a'):
		print link.string
		dhbwlink = "https://www.karlsruhe.dhbw.de" + link.get('href')
		print dhbwlink
	for td in company.find('td',class_='free-places'):
		state = td.string
		state = state.strip()
		print state
	print "visit dhbw"
	session.visit(dhbwlink) #Visit DHBW Site
	response = session.body()
	compsoup = BeautifulSoup(response)
	compsoup = compsoup.find('div', id="onziboe")
	print compsoup.prettify()

ws.set_row(0, 24)
ws.set_column(0,0,35)
ws.set_column(1,2,40)
ws.set_column(3,3,40)
ws.set_column(4,4,22)
ws.set_column(5,5,20)
ws.set_column(6,6,40)
ws.set_column(7,7,17)
ws.set_column(8,8,25)

ws.write(0,0,'Firmenname')
ws.write(0,1,'Adresse')
ws.write(0,2,'Bemerkung')
ws.write(0,3,'Website mit Infos')
ws.write(0,4,'Kontaktperson')
ws.write(0,5,'Kontaktemail')
ws.write(0,6,'Homepage')
ws.write(0,7,'Telefonnummer')
row = 0
col = 0

ws.set_row(0, 19)
workbook.close()
