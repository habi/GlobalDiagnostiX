#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib2
import matplotlib.pylab as plt

URL = 'http://physics.nist.gov/PhysRefData/XrayMassCoef/ComTab/muscle.html'

response = urllib2.urlopen(URL)
html = response.read()
soup = BeautifulSoup(html)

#~ ascii = soup.find('pre') # extract ASCII formatted table
#~ for line in ascii:
    #~ print len(str(line).split())

Energy = []
Mu = []
Muen = []
table = soup.find('table')
for row in table.findAll('tr'):
    col = row.findAll('td')
    if len(str(col).split()) == 3:
        Energy.append(col[0].find(text=True))
        Mu.append(col[1].find(text=True))
        Muen.append(col[2].find(text=True))
print col[1]

# plt.loglog(Energy,Mu,label='Mu')
# plt.loglog(Energy,Muen,label='Muen')
# plt.title(soup.title(text=True))
# plt.legend()
# plt.show()

URL = 'http://physics.nist.gov/PhysRefData/XrayMassCoef/ComTab/bone.html'
response = urllib2.urlopen(URL)
html = response.read()
soup = BeautifulSoup(html)

Energy = []
Mu = []
Muen = []
table = soup.find('table')
for row in table.findAll('tr'):
    col = row.findAll('td')
    if len(str(col).split()) == 3:
        Energy.append(col[0].find(text=True))
        Mu.append(col[1].find(text=True))
        Muen.append(col[2].find(text=True))
asdf = col[1](text=True)
print type(unicode.join(u'\n', map(unicode, asdf)))
