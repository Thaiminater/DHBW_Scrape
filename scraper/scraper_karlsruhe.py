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

session.visit("https://www.karlsruhe.dhbw.de/inf/duale-partner-finden.html?tx_dhbwenterprise20_pi1%5Baction%5D=index&tx_dhbwenterprise20_pi1%5Bcontroller%5D=Job&cHash=a40e347542d46be5990f646bb347cceb#tx_dhbwenterprise20_Filter")
Input = session.at_xpath('//*[@name="email"]') #for find input
Input.set('<input value>')
Input.form().submit() #for submit
time.sleep(5) #response = session.body()
soup = BeautifulSoup(response)

session.render("dhbw.png")

table = soup.find_all(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="NavDHBWEnterpriseTableEntries")

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
		
			