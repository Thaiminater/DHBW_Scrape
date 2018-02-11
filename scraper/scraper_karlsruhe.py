import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time
import xlsxwriter
import pdb

workbook = xlsxwriter.Workbook('karlsruhe.xlsx')
ws = workbook.add_worksheet()
dryscrape.start_xvfb()									# Start dryscrape session
session = dryscrape.Session()

session.visit("https://www.karlsruhe.dhbw.de/duale-partner/liste-der-dualen-partner.html?tx_dhbwenterprise20_pi2%5Bpage%5D=1&tx_dhbwenterprise20_pi2%5Baction%5D=indexSearch&tx_dhbwenterprise20_pi2%5Bcontroller%5D=Job&cHash=aecf0bcd6b534bcd6d4a99e1519e280f#tx_dhbwenterprise20_Filter")
response = session.body()
soup = BeautifulSoup(response)
print soup.prettify()
table = soup.find_all(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="NavDHBWEnterpriseTableEntries")
#rows = table.findAll(lambda tag: tag.name == 'tr')

#for company in rows:
#	print company
print table

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
		
			