import mechanize
import cookielib
from bs4 import BeautifulSoup
import csv
import urllib2
import io

def escrever_arquivo(array):
		with io.open ('ufsc1_1.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    for i in range(0, len(array)):
			    writer.writerow(array[i])

array = []
with open('ufsc.csv' , 'rt') as f:
	reader = csv.reader(f)
	for n, row in enumerate(reader):
		if n != 0:
			print row[34]
			br = mechanize.Browser()
			url = row[34]
			try:
				encontrado = False
				page = br.open(url)
				html = page.read()
				soup = BeautifulSoup(html)
				for i in soup.findAll('a'):
				    if 'Visualizar/Abrir' in i.text:
				        pdf =  'https://repositorio.ufsc.br' + i['href']
				        resp = urllib2.urlopen(pdf)
				        if resp.code == 200:
				        	encontrado = True
				        	row[41] = 'OpenAccess'
				        	print 'OpenAccess'
				        else:
				        	row[41] = '*'
				        	print '*'
				if not encontrado:
					for j in soup.findAll('img'):
						if '/bitstream/handle' in j['src']:
							print 'imagem aberta'
							row[41] = 'OpenAccess'
							encontrado = True

			        if not encontrado:
			        	row[41] = '-'
			        	print 'sem registro de download'
			except:
				row[41] = 'ClosedAccess'
				print 'ClosedAccess'

			array.append(row)
		else:
			array.append(row)

	escrever_arquivo(array)
