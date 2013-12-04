"""
Fetch SIMBAD Heat maps from the web
"""
import requests
from BeautifulSoup import BeautifulSoup

base_url = 'http://cdsannotations.u-strasbg.fr/ADSAllSkySurvey/SimbadHeatMaps/'
index = requests.get(base_url).text
index = BeautifulSoup(index)


files = [a['href'] for a in index.findAll('a')
         if a['href'].endswith('512.hpx')]


for f in files:
    url = base_url + f
    print "Fetching %s" % f
    path = f.split('/')[-1]
    with open(path, 'w') as outfile:
        outfile.write(requests.get(url).content)
