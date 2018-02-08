import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time

dryscrape.start_xvfb()									# Start dryscrape session
session = dryscrape.Session()

session.visit("https://www.dhbw-loerrach.de/informatik-duale-partner.html?no_cache=1")
response = session.body()
soup = BeautifulSoup(response)

def has_colspan(tag):
    return tag.has_attr('colspan')

for company in soup.find_all("div", class_="company_set",limit=2):
	#print (company.prettify())
	for adr in company.find_all("td", class_="company_addr"):
		#print (td.prettify())
		for string in adr.h3.stripped_strings:
			print ('Firmenname: ' + string)
		for string in adr.p.stripped_strings:
			print ('Firmenadresse: ' + string)
	for note in company.find_all("td", class_="company_note"):
		#print (td.prettify())
		for string in note.p.stripped_strings:
			b_string = unicode(string)
			b_string = re.sub('Bemerkungen:','',b_string)
			print (b_string)
			#print ('new string')
		for link in note.p.find_all('a'):
			print (link.get('href')) 
	for cnt in company.find_all("td", class_="company_contact"):
		for cnt_name in cnt.find_all("h5"):
			name = unicode(cnt_name)
			name = name.replace('<h5>','')
			name = name.replace('</h5>','')
			print name
		#for string in cnt.h5.strings:
		#	print ('Kontaktname: ' + string)
		for link in cnt.find_all("a"):
			if re.search("document.write",link.text) != None :
				b_string = str(link.text)
				b_string = b_string.replace('document.write(\'&#64;\');','')
				print b_string
			link = link.get('href')
			if re.search("www", link) != None :
				print link

	for num in company.find_all("td", has_colspan, class_="company_contact"):
		if num.p.string != None:
			print num.p.string
		
			