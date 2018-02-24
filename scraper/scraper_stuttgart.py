#!/usr/bin/env python # -*- coding: UTF-8 -*-
import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time
import xlsxwriter
import pdb
from kununu import kununu
workbook = xlsxwriter.Workbook('stuttgart.xlsx') #Create Excel File
ws = workbook.add_worksheet()
dryscrape.start_xvfb()									# Start dryscrape session
session = dryscrape.Session()
session.visit("https://www.dhbw-stuttgart.de/themen/internationales/internationale-studiengaenge/informatik/duale-partner/?tx_cronbafirmen_pi%5Boffset%5D=0&cHash=99f439f6a246d843d3a32e86bb8b32ca") #Visit DHBW Site
response = session.body()
soup = BeautifulSoup(response)

def has_colspan(tag):
    return tag.has_attr('colspan')
ws.set_row(0, 24)
ws.set_column(0,0,35)
ws.set_column(1,1,20)
ws.set_column(2,2,40)
ws.set_column(3,3,40)
ws.set_column(4,4,22)
ws.set_column(5,5,20)
ws.set_column(6,6,17)
ws.set_column(7,7,25)

ws.write(0,0,'Firmenname')
ws.write(0,1,'Adresse')
ws.write(0,2,'Bemerkung')
ws.write(0,3,'Website mit Infos')
ws.write(0,4,'Kontaktperson')
ws.write(0,5,'Kontaktemail')
ws.write(0,6,'Telefonnummer')
ws.write(0,7,'Kununu Seite')
row = 1
col = 0

soup = soup.find('table', id='company-list')
for company in soup.find_all("tr"):
	informatik = False
	ws.set_row(row, 50)
	internallink = ''
	coursename = ''
	name = ''
	#print (company.prettify())
	for partner in company.find_all("td", attrs={"data-title": "Dualer Partner"}):
		link = partner.find('a')
		internallink = link.get('href')
		name = link.span.text
	# for loc in company.find_all("td", attrs={"data-title": "Standort"}):
	# 	location =  loc.text
	# 	print location
	for course in company.find_all("td", attrs={"data-title": "Studiengang/Studienrichtung"}):
		if course.text == 'Informatik':
			informatik = True
	if informatik == True :
		ws.write(row,0,name)
		informatik = False
		dhbwlink = 'https://www.dhbw-stuttgart.de' + internallink
		session.visit(dhbwlink)
		response = session.body()
		soup2 = BeautifulSoup(response)
		for iTable in soup2.find_all('table', class_= 'table table-responsive-html5'):
			for tr in iTable.find_all('tr'):
				for intcourse in tr.find_all("td", attrs={"data-title": "Studiengang/Studienrichtung"}):
					coursename = intcourse.span.get_text()
				if coursename == 'Informatik':
					info = tr.find("td", attrs={"data-title": "Anschrift/Ansprechpartner"})
					if info != None:
						#print info
						print info.find('strong').get_text()
						ws.write(row,0,name)
						url = info.find('a',itemprop = 'url')
						if url != None:
							urltxt = url.get('href')
							print urltxt
							ws.write_url(row,0,urltxt,string = name)
							#ws.write(row,8,urltxt)
						adr= info.find('span',itemprop = 'address')
						if adr != None:
							adrtxt = adr.get_text()
							print adrtxt
							ws.write(row,1,adrtxt)
						cnt = info.find('span',itemprop = 'name')
						if cnt != None:
							cnttxt = cnt.get_text()
							ws.write(row,4,cnttxt)
							print cnttxt
						tel = info.find('span',itemprop = 'telephone')
						if tel != None:
							teltxt = tel.get_text()
							ws.write(row,6,teltxt)
							print teltxt
						mail = info.find('a',class_ = 'mail')
						if mail != None:
							mailtxt = mail.get_text()
							print mailtxt
							ws.write(row,5,mailtxt)
					note = tr.find("td", attrs={"data-title": "Bemerkungen"})
					if note != None:
						notetxt = note.get_text()
						ws.write(row,2,notetxt)
						print notetxt
					#kununu(session,ws,name,row,7,"&country=COUNTRY_DE")
		row += 1
	#kununu(session,ws,companyname,row,8,country)

ws.set_row(0, 19)
workbook.close()
