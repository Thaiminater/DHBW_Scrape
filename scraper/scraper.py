import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time

if  sys.argv[1] == "" :			# Show scheme if no parameters are given
	print("python scrape.py URL")
	sys.exit(0)
dryscrape.start_xvfb()									# Start dryscrape session
session = dryscrape.Session()

my_url = sys.argv[1]
session.visit(my_url)
response = session.body()
soup = BeautifulSoup(response)

for company in soup.find_all("div", class_="company_set"):
	#print (company.prettify())
	for adr in company.find_all("td", class_="company_addr"):
		#print (td.prettify())
		for string in adr.h3.strings:
			print ('Firmenname: ' + string)
		for string in adr.p.strings:
			print ('Firmenadresse: ' + string)
	for note in company.find_all("td", class_="company_note"):
		#print (td.prettify())
		for string in note.p.strings:
			b_string = unicode(string)
			b_string = re.sub('Bemerkungen:','',b_string)
			print (b_string)
			print ('new string')
		for link in note.p.find_all('a'):
			print (link.get('href'))
	for cnt in company.find_all("td", class_="company_contact"):
		#print (td.prettify())
		cnt_name = cnt.find_all("h5")
		print cnt_name
		#for string in cnt.h5.strings:
		#	print ('Kontaktname: ' + string)
		links = cnt.find_all("a")
		print links
		
			