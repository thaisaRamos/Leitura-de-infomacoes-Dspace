import mechanize
import cookielib
from bs4 import BeautifulSoup
import csv
import urllib2
import io
import re
import sys
def escrever_arquivo(array):
		with io.open ('rep2.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    for i in range(0, len(array)):
			    writer.writerow(array[i])

lista = []
with open('Lista-DSpace.csv' , 'rt') as f:
	reader = csv.reader(f)
	for n, row in enumerate(reader):
		if row[1] == 'DSpace' and n > 45:
			print row[0]
			numint = 0
			array = []
			formats = dict()
			br = mechanize.Browser()
			urlbase = row[0]
			try:
				encontrado = False
				page = br.open(urlbase)
				html = page.read()
				soup = BeautifulSoup(html)
				for i in soup.findAll('a'):
					if ('Data de defesa' or 'Issue Date' ) in i:
						while True:
							url = urlbase + '/browse?type=dateissued&sort_by=2&order=ASC&rpp=20&etal=-1&null=&offset=' + str(numint)
							#print url
							try:
								page = br.open(url)
								html = page.read()
								soup = BeautifulSoup(html)
								if numint == 0:
									for row in soup.find_all('div',attrs={"class" : "panel-heading text-center"}):
										total = re.findall('\d+', row.text)
										print total
										total = int(total[2])
										print total
								for i in soup.findAll('a'):
									tede = i.get('href')
									if tede!=None and 'handle/tede' in tede:
										num = re.findall('\d+', tede)
										num = int(num[0])
										if num not in array and num != '':
											array.append(num)
								numint += 20
								print numint , ' -- ' , total
								if (numint > total):
									if ((numint-19) == total):
										print 'finalizado'
										break
									else:
										n = numint - total
										numint = numint -n -1
										print 'ultimo' , n , '--' , numint
										print numint , ' eh dif de ' , total
							except:
								print 'error'
								break
						for count,i in enumerate(array):
							try:
								url = urlbase + '/handle/tede/' + str(i)
								page = br.open(url)
								html = page.read()
								soup = BeautifulSoup(html)
								for n,row in enumerate(soup.find_all('td',attrs={"headers" : "t4"})):
									if n == 0:
										print n,count, '---',row.text
										if formats.has_key(row.text):
											formats[row.text] +=  1
										else:
											formats[row.text] = 1
							except:
								print 'error'

						lista.append([ urlbase, formats, len(array)])
			except:
				print sys.exc_info()[0]
				raise

