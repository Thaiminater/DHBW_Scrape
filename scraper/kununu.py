import re
import time
import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time
import xlsxwriter

def kununu(session,ws,name,row,col,country):
	if row > 0 :
		try:
			name = str(name)
		except:
			print "Umlaut enthalten"
			return
		print "Visit Kununu Website"
		name = re.sub(" ","%20",name)
		url = "https://www.kununu.com/de/search#/?q=" + name + country
		session.visit(url)
		time.sleep(1)
		response = session.body()

		soup2 = BeautifulSoup(response)
		selectdic = {}
		index = 0
		for kuCompany in soup2.find_all("ku-company"):
			companyurl = ""
			acontainer = kuCompany.find("h2")
			companyurl = "https://www.kununu.com" + acontainer.a['href']+ "/kommentare"
			selectdic[index] = companyurl
			index += 1

		if 1 not in selectdic and 0 in selectdic:
			tempstr = selectdic[0]
			ws.write_url(row,col,tempstr,string='Kununu')
			print tempstr
		else:
			ws.write_url(row,col,url,string='Kununu search')
			print url
		#ws.write(row,6,companyurl)

	return
