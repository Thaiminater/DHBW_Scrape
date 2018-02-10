import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time
import xlsxwriter
import pdb

workbook = xlsxwriter.Workbook('loerrach.xlsx')
ws = workbook.add_worksheet()
dryscrape.start_xvfb()									# Start dryscrape session
session = dryscrape.Session()

session.visit("https://www.dhbw-loerrach.de/informatik-duale-partner.html?no_cache=1")
response = session.body()
soup = BeautifulSoup(response)

def has_colspan(tag):
    return tag.has_attr('colspan')
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
for company in soup.find_all("div", class_="company_set"):
	ws.set_row(row, 50)
	#print (company.prettify())
	for addr in company.find_all("td", class_="company_addr"):
		#print (td.prettify())
		namelist = []
		for namestring in addr.h3.stripped_strings:
			namelist.append(namestring)
			namelist.append(" ")
		name = "".join(namelist)
		ws.write(row,0,name)
		addresslist = []
		for addrstring in addr.p.stripped_strings:
			addresslist.append(addrstring)
			addresslist.append(" ")
		address = "".join(addresslist)
		print address
		ws.write(row,1,address)
	
	for note in company.find_all("td", class_="company_note"):
		#print (td.prettify())
		notelist = []
		for string in note.p.stripped_strings:
			b_string = unicode(string)
			b_string = re.sub('Bemerkungen:','',b_string)
			if b_string != None:
				notelist.append(b_string)
				#ws.write(row,col,b_string)
			#print ('new string')
		notestr = "".join(notelist)
		ws.write(row,2,notestr)
		print notestr
		linklist = []
		for link in note.p.find_all('a'):
			href = link.get('href')
			if re.search("www", href) != None:
				linklist.append(href)
				linklist.append(" ")
			linkstr = "".join(linklist)
			ws.write(row,3,linkstr)
	for cnt in company.find_all("td", class_="company_contact"):
		for cnt_name in cnt.find_all("h5"):
			name = unicode(cnt_name)
			name = name.replace('<h5>','')
			name = name.replace('</h5>','')
			print name
			ws.write(row,4,name)
		#for string in cnt.h5.strings:
		#	print ('Kontaktname: ' + string)
		#pdb.set_trace()
		for link in cnt.find_all("a"):
			if re.search("document.write",link.text) != None :
				b_string = unicode(link.text)
				b_string = b_string.replace('document.write(\'&#64;\');','')
				ws.write(row,5,b_string)
				print b_string
			link = link.get('href')
			if re.search("www", link) != None :
				ws.write_url(row,6,link)
				print link

	for num in company.find_all("td", has_colspan, class_="company_contact"):
		if num.p.string != None:
			ws.write(row,7,num.p.string)
			print num.p.string

	for state in company.find_all("td", has_colspan, class_="company_tl"):
		statestr = state.img['title']
		ws.write(row,8,statestr)
	print ("\n")
	row += 1
ws.set_row(0, 19)
workbook.close()
		
			