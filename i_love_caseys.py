
#
#
# Python code to read Casey's Times
#
#
##############################################
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

def get_max_name_length(np_names_week):
    maxl=10
    for i in range (0,len(np_names_week)):
      if len(np_names_week[i]) > maxl:
        maxl=len(np_names_week[i])
    print (maxl)    
    return maxl    
    

import re
from bs4 import BeautifulSoup
import datetime
import urllib.request as ur
import numpy as np

#Looping over the different weeks in each year
### THIS CODE WILL HELP US TO READ IN THE URL 
### AND THEN TO LOOP OVER THE URL
ann_link='http://www.srr.org/events/thursday-night-run/2016/'
page = ur.urlopen(ann_link)
page_html = page.read()
tmp = str(page_html,'utf-8')
soup = BeautifulSoup(page_html, 'html.parser')
url_links=([])
for a in soup.find_all('a', href=True):
    url_links.append(ann_link+a['href'])
print (url_links)
###############################################

#This is the web page to read from
#link = 'http://www.srr.org/events/thursday-night-run/2016/2016.01.28.htm'
link = url_links[5]

#now pull out the date from the url info
datex=link.replace('.htm','')
datex=link.replace('.html','')
datex=datex.split('/')
datex2=datex[6]
datex2=datex2.split('.')
if len(datex2) == 1:
    datex2=datex2[0].split('-')
run_date = (datetime.date(int(datex2[0]),int(datex2[1]),int(datex2[2])))

###Read the raw html code from the webpage
###  -- This does not work on local pc 
#source = urllib.urlopen(link)
#page = source.read()

page = ur.urlopen(link)
page_html = page.read()

#Use the below with beautiful soup
#print (page_html)
#soup = BeautifulSoup(page_html, 'html.parser')
#tmp = soup.split("\n")

#Clean the html text 
tmp = str(page_html,'utf-8') #You need this on a windows pc
cleantext = remove_html_markup(tmp)

#divide up the text
tmp2 = cleantext.split("\n")

#find the first athlete
try:
  start = tmp2.index('  Notes')+1
except ValueError:
  start=-1
if start == -1:  
  try:
    start = tmp2.index('              Notes')+1
  except ValueError:
    start=-1

np_names_week =np.array([]) #initialize data_tmp 
np_towns_week =np.array([])
np_times_week =np.array([])

#now loop over the number of athletes
n_athletes = len(tmp2)
for p in range(start,n_athletes) :
  x=tmp2[p]
  y=x.strip()
  z=y.lstrip()
  xyz=z.split(":")
  
  #only test for a number if xyz has 2 elements == otherwise this is age
  if len(xyz) > 1 :  
    test=xyz[0] 
 
    #check if element contain a time is_number(test)
    if(is_number(test)) :  
      print( tmp2[p-1],tmp2[p],tmp2[p+1])
      #We cannot rm whitspace from a list
      tmpname=tmp2[p-1]
      tmpname=tmpname.lstrip()
      tmpname=tmpname.lstrip()
      tmptown=tmp2[p+1]
      tmptown=tmptown.lstrip()
      tmptown=tmptown.rstrip()
      np_names_week=np.append(np_names_week,tmpname)
      np_towns_week=np.append(np_towns_week,tmptown)
    
    
      #For the time we need to time hh:mm:ss format
      m,s = re.split(':',tmp2[p])
      h=0
      if int(m) < 21: #if mins time < 21 then set hours =1
        h = 1      
      np_times_week=np.append(np_times_week,datetime.time(h,int(m),int(s)))    

#get max length of names string
maxl=get_max_name_length(np_names_week)

#print the resuls in      
for i in range (0,len(np_names_week)) :    
    print ('{:<{}s}'.format(np_names_week[i],maxl),np_times_week[i],run_date)

print (url_links)
#print f.text
