import dryscrape
from bs4 import BeautifulSoup
from kununu import kununu
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

ws.set_row(0, 24)
ws.set_column(0,0,35)
ws.set_column(1,2,23)
ws.set_column(3,3,21)
ws.set_column(4,4,40)
ws.set_column(5,5,20)
ws.set_column(6,6,8)
ws.set_column(7,7,6)
ws.set_column(8,8,25)

ws.write(0,0,'Firmenname')
ws.write(0,1,'Adresse')
ws.write(0,2,'Kontaktemail')
ws.write(0,3,'Kontakt')
ws.write(0,4,'Extrainfo')
ws.write(0,5,'DHBW')
ws.write(0,6,'Kununu')
ws.write(0,7,'Status')
ws.write(0,8,'Maps')
row = 1

name = ''

with open("dhbw_karlsruhe_2018.html") as response:
	soup = BeautifulSoup(response)



for company in soup.find_all("tr",class_="googleMapsCoordinates"):
	print row
	for link in company.find_all('a'):
		dhbwlink = "https://www.karlsruhe.dhbw.de" + link.get('href')
		name = link.string
		print name
		ws.write_url(row,5,dhbwlink,string='DHBW')
	for td in company.find('td',class_='free-places'):
		state = td.string
		state = state.strip()
		ws.write(row,7,state)
		if 'frei' in state:
			ws.write(row,8,'large_green')
		else:
			ws.write(row,8,'large_red')
		print state
	print "Visit dhbw"
	session.visit(dhbwlink) #Visit DHBW Site
	response = session.body()
	compsoup = BeautifulSoup(response)
	compsoup = compsoup.find('div', id="onziboe")
	bodydiv = compsoup.find('div',  class_='box-body')
	address =""
	addresslist = []
	for addrstring in bodydiv.p.stripped_strings:
		addresslist.append(addrstring)
		addresslist.append(" ")
		address = "".join(addresslist)
	ws.write(row,1,address)
	print 'Adresse: '  + address
	nolink = True
	for link in bodydiv.find_all('a'):
		nolink = False
		hplink = False
		temptext = link.text
		if 'noSpam' in temptext:
			temptext = re.sub('noSpam','',temptext)
			ws.write(row,2,temptext)
		if 'www' in temptext:
			hplink = True
			temptext = "http://" + temptext
			ws.write_url(row,0,temptext,string=name)
		if hplink == False:
			ws.write(row,0,name)
		print temptext
	if nolink == True:
		ws.write(row,0,name)
	index = 0
	for descr in compsoup.find_all('h3', class_='jobs-at-course-headline'):
		deshead = descr.text
		if 'Angewandte Informatik' in deshead :
			rowindex = index
		index += 1
	# contact = descr.find('div', class_='col-md-5 no-padding')
	# print contact
	index = 0
	for info in compsoup.find_all('div',class_='row job-info'):
		if rowindex == index:
			infsoup = info
		index += 1
	cnt =""
	cntlist = []
	for contact in infsoup.find('div',class_='col-md-5 no-padding'):
		if contact.string != None:
			tempstr = unicode(contact.string)
			tempstr = tempstr.strip()

			if '(Kein spezieller Ansprechpartner hinterlegt.)' not in tempstr and name not in tempstr :
				cntlist.append(tempstr)
				cntlist.append("\n")
	cnt = "".join(cntlist)
	ws.write(row,3,cnt)
	print cnt
	for note in infsoup.find('div',class_='col-md-4 no-padding'):
		tempstring = note.string
		tempstring = tempstring.strip()
		ws.write(row,4,tempstring)
		print tempstring
	# for text in bodydiv.stripped_strings:
	# 	print text
	# for text in bodydiv.find_all('p'):
	# 	temptext = text.text
	# 	temptext = temptext.strip()
	# 	print temptext
	kununu(session,ws,name,row,6,"&country=COUNTRY_DE")
	row += 1
ws.set_row(0, 19)
workbook.close()
