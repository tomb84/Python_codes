
#
#
# Python code to read Casey's Times
#
#
def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

def cleanhtml(raw_html):
  cleanr =re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', raw_html)
  return cleantext

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

import re
import urllib

link = 'http://www.srr.org/events/thursday-night-run/2016/2016.01.28.htm'

#f = urllib.urlopen(link)           
#myfile = f.readline()  
#print myfile

source = urllib.urlopen(link)
page = source.read()

cleantext = remove_html_markup(page)

#THIS METHOD WORKS OK
#import requests
#f = requests.get(link)
#print f.text

#clean=cleanhtml(f.text)
#Beautiful soup does not work as the package is not available
#from BeautifulSoup import BeautifulSoup
#cleantext = BeautifulSoup(f).text

##clear the html text
#cleantext = remove_html_markup(tmp)

#print cleantext
##clear the html text
#mytext=f.text
#mytext.replace("City","")
#cleantext = remove_html_markup(mytext)

#print cleantext
#print len(cleantext)

#cleantext.replace("&nbsp;","")
#cleantext.replace("Name","")
#cleantext.replace("Time","")
#cleantext.replace("Notes","")

tmp = cleantext.split("\n")
#tmp = filter(' ', tmp) # fastest
#tmp.lstrip()

#print len(tmp)
print tmp
print len(tmp)

#print f.text
start = tmp.index('  Notes')+1
#print start

n_athletes = len(tmp)
for p in range(start,n_athletes) :
  x=tmp[p]
  y=x.strip()
  z=y.lstrip()
  xyz=z.split(":")
  test=xyz[0] 
 
  #print is_number(test)
  if(is_number(test)) :
    print tmp[p-1],tmp[p],tmp[p+1]

   #The probelm is that the code does not understand the : = can't convert to float so use
  
#print f.text
