import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time
import xlsxwriter

workbook = xlsxwriter.Workbook('loerrach.xlsx')
ws = workbook.add_worksheet()
dryscrape.start_xvfb()									# Start dryscrape session
session = dryscrape.Session()

session.visit("https://www.dhbw-loerrach.de/informatik-duale-partner.html?no_cache=1")
response = session.body()
soup = BeautifulSoup(response)

def has_colspan(tag):
    return tag.has_attr('colspan')
ws.write(0,0,'Firmenname')
ws.set_column(0,0,35)
ws.write(0,1,'Adresse')
ws.set_column(1,20,40)
ws.write(0,2,'Kontaktperson')
ws.write(0,3,'Kontaktemail')
row = 1
col = 0
for company in soup.find_all("div", class_="company_set",limit=3):
	ws.set_row(row, 20)
	#print (company.prettify())
	for addr in company.find_all("td", class_="company_addr"):
		#print (td.prettify())
		for namestring in addr.h3.stripped_strings:
			print namestring
			ws.write(row,col,namestring)
			col += 1
		addresslist = []
		for addrstring in addr.p.stripped_strings:
			addresslist.append(addrstring)
			addresslist.append(" ")
		address = "".join(addresslist)
		print address
		if address != None:
			ws.write(row,col,address)
			col += 1
	
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
		notestr = " \n".join(notelist)
		ws.write(row,col,notestr)
		print notestr
		col += 1
		for link in note.p.find_all('a'):
			href = link.get('href')
			if re.search("www", href) != None:
				ws.write(row,col,href)
			col += 1
	for cnt in company.find_all("td", class_="company_contact"):
		for cnt_name in cnt.find_all("h5"):
			name = unicode(cnt_name)
			name = name.replace('<h5>','')
			name = name.replace('</h5>','')
			print name
			ws.write(row,col,name)
			col += 1
		#for string in cnt.h5.strings:
		#	print ('Kontaktname: ' + string)
		for link in cnt.find_all("a"):
			if re.search("document.write",link.text) != None :
				b_string = str(link.text)
				b_string = b_string.replace('document.write(\'&#64;\');','')
				ws.write(row,col,b_string)
				print b_string
				col += 1
			link = link.get('href')
			if re.search("www", link) != None :
				ws.write_url(row,col,link,string='HP')
				print link
			col += 1

	for num in company.find_all("td", has_colspan, class_="company_contact"):
		if num.p.string != None:
			ws.write(row,col,num.p.string)
			print num.p.string

	print ("\n")
	row += 1
	col = 0
workbook.close()
		
			