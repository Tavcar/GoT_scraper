# -*- coding: utf-8 -*-
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Game_of_Thrones"
url_wiki = "https://en.wikipedia.org"

response = urlopen(url).read()
soup = BeautifulSoup(response)

ogledi = []
tabela = soup.find("table", attrs={"class": "wikitable"})

for link in tabela.findAll("a", href=True, title=True):
    if 'season' in link["href"]:
        sezone = link["href"] #[21:]
        levi = sezone.replace("(", "%28")
        desni = levi.replace(")", "%29")
        sezona_url = url_wiki + desni
        sezona_html = urlopen(sezona_url).read()
        sezona_soup = BeautifulSoup(sezona_html)

        if sezona_soup.find("table", attrs={"class": "wikitable plainrowheaders wikiepisodetable"}):
            gledalci=sezona_soup.find("table", attrs={"class": "wikitable plainrowheaders wikiepisodetable"})
            for row in gledalci.findAll("tr"):
                cells = row.findAll("td")
                if len(cells) == 6:
                    zadnja = cells[5]
                    references = zadnja.findAll("sup", {"class": "reference"})
                    if references:
                        for ref in references:
                            ref.extract()

                            views = zadnja.text
                            tv_ogledi = float(views)
                            ogledi.append(tv_ogledi)

vsi_ogledi = sum(ogledi)
print "Število vseh ogledov (v milijonih):"
print vsi_ogledi