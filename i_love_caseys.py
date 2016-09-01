
# Python code to read Casey's Times
#########################################

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
    
def get_max_name_length(np_names_week):
    maxl=10 #initialize to 10 
    for i in range (0,len(np_names_week)):
      if len(np_names_week[i]) > maxl:
        maxl=len(np_names_week[i])
    print (maxl)    
    return maxl    

###########################################
#       M A I N   C O D E
###########################################    

location='work' 
year='2016'

import re
import datetime
import numpy as np
import is_time_format_hhmm
import get_date_from_url
import unicodedata

if location == "home":
  import urllib.request as ur  #home
  from bs4 import BeautifulSoup
if location == "work":
  import urllib

###Looping over the different weeks in each year
### THIS CODE WILL HELP US TO READ IN THE URL 
### AND THEN TO LOOP OVER THE URL
if location == "home":
  ann_link='http://www.srr.org/events/thursday-night-run/'+year+'/'
  page = ur.urlopen(ann_link)
  page_html = page.read()
  tmp = str(page_html,'utf-8')
  soup = BeautifulSoup(page_html, 'html.parser')
  url_links=([])
  for a in soup.find_all('a', href=True):
    chktmp=(a['href'])
    chktmp2=chktmp.split(".")
    if len(chktmp2) > 1 :
      url_links.append(ann_link+a['href'])
      print (ann_link+a['href'])

if location == "work":
  if year == '2016': #This only works for 2016 so far
    ann_link='http://www.srr.org/events/thursday-night-run/'+year+'/'
    page = urllib.urlopen(ann_link)
    page_html = page.read()
    cleantext = remove_html_markup(page_html)
    tmp2 = cleantext.split("\n")
    #print tmp2
    url_links=([])
    for i in range (0,len(tmp2)):
      x=tmp2[i]
      x2=x.split()
      for p in range (0,len(x2)): 
        x3=x2[p]
        if is_time_format_hhmm.is_time_format_hhmm(x3) :
          url_links.append(ann_link+x2[p-2])

np_names_year =np.array([]) #initialize data_tmp
np_towns_year =np.array([])
np_times_year =np.array([])
nlastwk=0

#loop over the url links
#for url in url_links:
for l in range (0,1):
  #page = urllib.urlopen(url)
  #page_html = page.read()
  #cleantext = remove_html_markup(page_html)
  #tmp2 = cleantext.split("\n")
  #print tmp2[0:30]

###############################################

  #This is the web page to read from
  #link = 'http://www.srr.org/events/thursday-night-run/2016/2016.01.28.htm'
  link ='http://www.srr.org/events/thursday-night-run/2016/2016.05.12.htm'
  #link = url
  print 'reading url :',link

  if location == "home":
    page = ur.urlopen(link) 
    page2 = page.read()
    page_html = str(page2,'utf-8')        #home only

  if location == "work":
    page = urllib.urlopen(link) 
    #page2 = page.read()
    #page_html = str(page2,'utf-8')
    page_html = page.read()

  #clean the html text
  cleantext = remove_html_markup(page_html)

  #now pull out the date from the url info
  run_date=get_date_from_url.get_date_from_url(link)

  #divide up the text
  tmp2 = cleantext.split("\n")
  print tmp2

  #strip the left and right whitespace away from each element in the list
  tmp3 = [x.lstrip(' ') for x in tmp2]
  tmp3 = [x.rstrip(' ') for x in tmp3]
  text_find='Notes'
  start = tmp3.index(text_find)+1
  print 'found start',start

  np_names_week =np.array([]) #initialize data_tmp
  np_towns_week =np.array([])
  np_times_week =np.array([])

  #now loop over the number of athletes
  n_athletes = len(tmp2)
  for p in range(start,n_athletes) :
    x=tmp2[p]
    #x=x.decode('latin-1')
    #x = unicodedata.normalize("\xa0", x)
    #x=x.strip()
    #x=x.decode('ascii','ignore')
    print x

    if is_time_format_hhmm.is_time_format_hhmm(x) :
      np_names_week=np.append(np_names_week,tmp3[p-1])
      np_towns_week=np.append(np_towns_week,tmp3[p+1])
    
      #Convert time to hh:mm:ss format
      m,s = re.split(':',tmp2[p])
      h=0
      if int(m) < 21: #if mins time < 21 then set hours =1
        h = 1      
      np_times_week=np.append(np_times_week,datetime.time(h,int(m),int(s)))    


  #get max length of names string
  maxl=get_max_name_length(np_names_week)+1

  #print the resuls in      
  for i in range (0,len(np_names_week)) :    
    print ('{:<{}s}'.format(np_names_week[i],maxl),np_times_week[i],run_date)

  np_names_year = np.append(np_names_year,np_names_week)
  np_towns_year = np.append(np_towns_year,np_towns_week)
  np_times_year = np.append(np_times_year,np_towns_week)

  #Save the output to a file for a single week
  print ''
  fname='SRR_Caseys_results_'+str(run_date)
  print ('Number of Runners this week=',len(np_names_week))
  print ''

  if len(np_names_week) > 0 :
    np.savez(fname,np_names_week=np_names_week,np_times_week=np_times_week,np_towns_week=np_towns_week)
  else :
    print 'No file output : There is no data available for the week : ',str() 

#get max length of names string
maxl=get_max_name_length(np_names_year)
print ('')
print ('Number of Weeks =',len(url_links))
print ('Total Number of Runners this year=',len(np_names_year))


fname='SRR_Caseys_results_'+year
np.savez(fname,np_names_year=np_names_year,np_times_year=np_times_year,np_towns_year=np_towns_year)

#npzfile = np.load('SRR_Caseys_results_2016-01-28.npz')
#npzfile.files
#npzfile['np_names_week'] # to show an array


