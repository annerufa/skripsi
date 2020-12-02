from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# open a connection to a URL using urllib
base_url = 'https://repository.unej.ac.id'
webUrl = urlopen('https://repository.unej.ac.id/handle/123456789/15')

# get result code
print("result code :" + str(webUrl.getcode()))

#
data = webUrl.read()
soup = BeautifulSoup(data, 'html.parser')

# ambil semua link untuk tiap fakultas
fakultass = []
for link in soup.find_all('a'):
    if link.find("span", class_="Z3988"):
        fakultass.append((link.span.text, link.get('href')))

#ambil link semua dokumen tiap fakultas
for fakultas in fakultass:
    links = []
    halPertama = '/discover?rpp=100'
    url = base_url + str(fakultas[1]) + halPertama
    while url :
        webUrl = urlopen(url)
        data = webUrl.read()
        soup = BeautifulSoup(data, 'html.parser')
        for link in soup.find_all("div", {"class": "artifact-description"}):
            links.append(link.find('a').get('href'))
        if soup.find("a", class_="next-page-link"):
            a = soup.find("a", class_="next-page-link")['href']
            url = base_url + str(fakultas[1]) + '/'+ a
        else:
            url = ''
    
    #simpan ke txt
    with open(f"list{str(fakultas[0])}.txt", 'w') as output:
        for row in links:
            output.write(str(row) + '\n')
    print('selesai. total dokumen :'+ str(len(links)))
