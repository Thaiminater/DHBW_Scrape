#!/usr/bin/env python # -*- coding: UTF-8 -*-
import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time
import xlsxwriter
from kununu import kununu

workbook = xlsxwriter.Workbook('mannheim.xlsx') #Create Excel File
ws = workbook.add_worksheet()
dryscrape.start_xvfb()									# Start dryscrape session
session = dryscrape.Session()
session2 = dryscrape.Session()

ws.set_column(0,0,35)
ws.set_column(1,1,40)
ws.set_column(2,2,22)
ws.set_column(3,3,33)
ws.set_column(4,20,45)

ws.write(0,0,'Firmenname')
ws.write(0,1,'Adresse')
ws.write(0,2,'Kontaktperson')
ws.write(0,3,'Kontakt')
ws.write(0,4,'Kununu')

session.visit("https://www.dhbw-mannheim.de/duales-studium/duale-partner-suchen.html") #Visit DHBW Site
showfree = session.at_xpath('//*[@id="onlyFree"]')		#get the html to analyse
showfree.click()
inf = session.at_xpath('//*[@id="courseIds"]/option[30]')
inf.select_option()
infbi = session.at_xpath('//*[@id="courseIds"]/option[31]')
infbi.select_option()
submit = session.at_xpath('//*[@id="btn_submit"]/input')
submit.click()
time.sleep(4)
num = session.at_xpath('//*[@id="onziboe"]/div[1]/div[3]/div[2]/div[4]/div[2]/a[3]')
num.click()
time.sleep(2)

response = session.body()
soup = BeautifulSoup(response)
soup = soup.find('table',class_="contenttable list-by-course")
row = 1
for comp in soup.find_all('td',class_="company"):
	print row
	xpath = '//*[@id="onziboe"]/div[1]/div[3]/div[2]/table[1]/tbody/tr[{0}]/td[1]/span[1]/a'.format(row)
	company = session.at_xpath(xpath)
	company.click()
	time.sleep(2)
	infbody = session.body()
	infsoup = BeautifulSoup(infbody)
	infsoup = infsoup.find('div',class_='box-enterprise')
	infotable = infsoup.find('table',class_='ent',id='firmeninfo')
	name = infotable.find('td',class_="name",id="enterprise-name")
	name = unicode(name.text)
	#ws.write(row,0,name.text)
	address = infotable.find('td',class_="address", id="fi-enterprise-address")
	ws.write(row,1,address.text)
	print address.text
	web = infotable.find('td',class_='www')
	if web != None:
		try:
			ws.write_url(row,0,web.a.get('href'),string=name)
			print web.a.get('href')
		except:
			ws.write(row,0,name)
	else:
		ws.write(row,0,name)
	cntinfo = infsoup.find('span',class_='contact')
	#print cntinfo
	cntname = None
	mail = None
	if cntinfo != None:
		cntname = cntinfo.find('span',class_='name')
		mail = cntinfo.find('span',class_='mail')

	#print cntname
	#print type(cntname)
	if cntname != None:
		ws.write(row,2,cntname.text)
		print cntname.text
	if mail != None:
		ws.write(row,3,mail.text)
		print mail.text
	#print infotable.prettify()
	zurueck = session.at_xpath('//*[@id="onziboe"]/div[1]/div[4]/div/a')
	zurueck.click()
	kununu(session2,ws,name,row,4,"&country=COUNTRY_DE")
	row += 1


#session.render("mannheim.png")
workbook.close()
