import requests
from bs4 import BeautifulSoup
import csv

class Craw:
    def __init__(self, filelink,namaFile):
        self.data = []
        self.noAbstrak = []
        links=[]
        f = open(filelink)
        for line in f:
            links.append('https://repository.unej.ac.id'+line.strip())
        f.close()
        #nanti coba "" buat nama file
        with open(f"{namaFile}.csv", 'w', newline='', encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(('judul', 'abstrak', 'fakultas', 'bahasa', 'keywords', 'link'))
            ss=1
            for link in links:
                for i in self.bulkCraw(link):
                    writer.writerow(i)
                    print('-'+str(ss))
                    ss+=1

        print('total link ='+str(ss-1))
        print(self.noAbstrak)
        
    def bulkCraw(self, link): 
        a = []
        data = requests.get(link)
        soup = BeautifulSoup(data.text, 'html.parser')
        if not soup.find("meta", {'name':"citation_title"}) or not soup.find("meta", {'name':"DCTERMS.abstract"}):
            self.noAbstrak.append(link)
        else:
            a.append(soup.find("meta", {'name':"citation_title"})["content"])
            abstrak=soup.find("meta", {'name':"DCTERMS.abstract"})["content"]
            a.append(str(" ".join(line.strip() for line in abstrak.split("\n"))))
            a.append(8)
            if not soup.find("meta", {'name':"citation_language"}):
                a.append('other')
            else:
                a.append(soup.find("meta", {'name':"citation_language"})["content"])
            if not soup.find("meta", {'name':"citation_keywords"}):
                a.append(' ')
            else:
                a.append(soup.find("meta", {'name':"citation_keywords"})["content"])
            # a.append(soup.find("meta", {'name':"citation_keywords"})["content"])
            a.append(link+' ')
            yield a

coba = Craw('list link fakultas/listUT-Faculty of  Teacher Training and Education.txt','fkip')

