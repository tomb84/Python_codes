
# Python code to read Casey's Times
#########################################

def month_converter(mon):
#    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
#    return months.index(mon) + 1
     return{
        'jan' : '01',
        'feb' : '02',
        'mar' : '03',
        'apr' : '04',
        'may' : '05',
        'jun' : '06',
        'jul' : '07',
        'aug' : '08',
        'sep' : '09', 
        'oct' : '10',
        'nov' : '11',
        'dec' : '12',
        'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09',
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12'
}[mon]


def find_results(tmp3):
  try:
     start = tmp3.index('Notes')+1
  except ValueError:
     start=-1
  if start == -1 :
     try:
        start = tmp3.index('City')+1
     except ValueError:
        start=-1
  return start

def call_get_2016_urls(location):
  if location == "work":
    page = urllib.urlopen(ann_link)
    page_html = page.read()
    cleantext = remove_html_markup(page_html)
    tmp2 = cleantext.split("\n")
    #print tmp2
    for i in range (0,len(tmp2)):
      x=tmp2[i]
      x2=x.split()
      for p in range (0,len(x2)):
        x3=x2[p]
        if is_time_format_hhmm.is_time_format_hhmm(x3) :
          url_links.append(ann_link+x2[p-2])

  if location == "home":
     page = ur.urlopen(ann_link)
     page_html = page.read()
     tmp = str(page_html,'utf-8')
     soup = BeautifulSoup(page_html, 'html.parser')
     for a in soup.find_all('a', href=True):
       chktmp=(a['href'])
       chktmp2=chktmp.split(".")
       if len(chktmp2) > 1 :
         url_links.append(ann_link+a['href'])
     #print (ann_link+a['href'])

  return url_links 

def call_get_urls(year):

    yrdays = 366 if calendar.isleap(year) else 365
    get_jday = {
      2015: 0,
      2014: 1,
      2013: 2,
      2012: 4,
      2011: 5,
      2010: 6,
      2009: 0,
      2008: 2,
    }
    start_jday = get_jday.get(year)

    myd=0
    for jd in range (start_jday,yrdays):
       if myd%7 == 0:
          date = datetime.datetime(int(year), 1, 1) + datetime.timedelta(jd)
          #print (ann_link+'%s.html'%date.strftime('%Y-%m-%d'))
          tmp= date.strftime('%b')
          tmp2=tmp.lower()
          if year >= 2013:
            url_links.append(ann_link+'%s.html'%date.strftime('%Y-%m-%d'))
          elif year >=2011:
            url_links.append(ann_link+tmp2+'%s.htm'%date.strftime('%d'))
          else: 
            page = urllib.urlopen(ann_link+tmp2+'%s.html'%date.strftime('%d'))
            page_html = page.read()
            tmp4 = page_html.split("\n")
            if len(tmp4) >= 100:
              url_links.append(ann_link+tmp2+'%s.html'%date.strftime('%d'))
            else:
              page = urllib.urlopen(ann_link+tmp+'%s.html'%date.strftime('%d'))
              page_html = page.read()
              tmp4 = page_html.split("\n")
              if len(tmp4) >= 100:
                url_links.append(ann_link+tmp+'%s.html'%date.strftime('%d'))
              else:
                dtmp=date.strftime('%d')
                dtmp2=dtmp[1:]
                page = urllib.urlopen(ann_link+tmp+dtmp2+'.html')
                page_html = page.read()
                tmp4 = page_html.split("\n")
                if len(tmp4) >= 100:
                  url_links.append(ann_link+tmp+dtmp2+'.html')
                else:
                  page = urllib.urlopen(ann_link+tmp2+dtmp2+'.html')
                  page_html = page.read()
                  tmp4 = page_html.split("\n") 
                  if len(tmp4) >= 100:
                    url_links.append(ann_link+tmp2+dtmp2+'.html')
                  else:
                    page = urllib.urlopen(ann_link+tmp2+dtmp2+'.html')
                    page_html = page.read()
                    tmp4 = page_html.split("\n")
                    if len(tmp4) >= 100:
                      url_links.append(ann_link+tmp2+dtmp2+'.html')
                    else:
                      page = urllib.urlopen(ann_link+'June'+dtmp+'.html')
                      page_html = page.read()
                      tmp4 = page_html.split("\n")
                      if len(tmp4) >= 100:
                        url_links.append(ann_link+'June'+dtmp+'.html')
                      else:
                        page = urllib.urlopen(ann_link+'July'+dtmp+'.html')
                        page_html = page.read()
                        tmp4 = page_html.split("\n")
                        if len(tmp4) >= 100:
                          url_links.append(ann_link+'July'+dtmp+'.html')
                        else:
                          page = urllib.urlopen(ann_link+'July'+dtmp2+'.html')
                          page_html = page.read()
                          tmp4 = page_html.split("\n")
                          if len(tmp4) >= 100:
                            url_links.append(ann_link+'July'+dtmp2+'.html')
                          else:
                            print 'error',ann_link+tmp2+dtmp+'.html'
       myd=myd+1

    return url_links   

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
year=2008

import re
import datetime
import numpy as np
import is_time_format_hhmm
import get_date_from_url
import unicodedata
import calendar

if location == "home":
  import urllib.request as ur  #home
  from bs4 import BeautifulSoup
if location == "work":
  import urllib

### Get the urls
url_links=([])
ann_link='http://www.srr.org/events/thursday-night-run/'+str(year)+'/'
if year < 2011:
 ann_link='http://www.srr.org/events/khourys/'+str(year)+'/'
if year == 2016:
   call_get_2016_urls(location)
if year != 2016: #Other Years
   call_get_urls(year)

np_names_year =np.array([]) #initialize np arrays
np_towns_year =np.array([])
np_times_year =np.array([])
np_dates_year =np.array([])

#for l in range (0,1):
for url in url_links:
  if url == 'http://www.srr.org/events/khourys/2010/apr08.html': #This has an odd format
     continue

###############################################

  #This is the web page to read from
  #link ='http://www.srr.org/events/thursday-night-run/2016/2016.05.12.htm'
  link = url
  #link ='http://www.srr.org/events/khourys/2010/aug12.html'
  print 'reading url :',link


  if location == "home":
    page = ur.urlopen(link) 
    page2 = page.read()
    page_html = str(page2,'utf-8')        #home only
  if location == "work":
    page = urllib.urlopen(link)
    page_html = page.read()

  #clean the html text
  cleantext = remove_html_markup(page_html)

  #now pull out the date from the url info
  if year > 2012:
    run_date=get_date_from_url.get_date_from_url(link)
  else:
    datex=link.replace('.htm','')
    datex=link.replace('.html','')
    datex=datex.split('/')
    datex2=datex[len(datex)-1]
    datex2=datex2.split('.') 
    day = datex2[0][3:]
    strmon= datex2[0][:3]
    month=month_converter(strmon)
    run_date = (datetime.date(year,int(month),int(day))) 

  #divide up the text
  tmp2 = cleantext.split("\n")
  #print tmp2

  #strip the left and right whitespace away from each element in the list
  tmp3 = [x.lstrip(' ') for x in tmp2]
  tmp3 = [x.rstrip(' ') for x in tmp3]

  #Find the start of the results data
  start = find_results(tmp3)

  SET_PR_NIGHT=0
  np_names_week =np.array([]) #initialize the weekly arrays
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
    #print x
    if is_time_format_hhmm.is_time_format_hhmm(x) :
      np_names_week=np.append(np_names_week,tmp3[p-1])
      np_towns_week=np.append(np_towns_week,tmp3[p+1])

   
      #Error check for names = some weeks are mising first names
      #Look for first and last name = but this throws other errors that are no relevant
      #chknm  = tmp3[p-1]
      #chknm2 =  chknm.split(' ') 
      #if len(chknm2) == 1:
      #  print 'chknm2',chknm2
      #  if len(tmp3[p-2]) > 0:
      #    print tmp3[p-2],tmp3[p-1],len(tmp3[p-2])
      #    tmpname=tmp3[p-2]+' '+tmp3[p-1]
      #    print tmpname 
      #    print np_names_week
      #    np_names_week=np.append(np_names_week,tmpname)
      ##    print np_names_week
      #    exit()
   
      #Convert time to hh:mm:ss format
      try:
         m,s = re.split(':',tmp2[p])
         h=0
         timeerror=0
      except ValueError:
         timeerror=-1
      if timeerror == -1 :
         try:
            h,m,s = re.split(':',tmp2[p])
            if int(h) >1 :
              timeerror=-1
         except ValueError:
            timeerror=-1
      if timeerror == -1 :
         try:
            m,s,h = re.split(':',tmp2[p])
         except ValueError:
           timeerror=-1

      #print s,len(s)
     
      #Error check for typo in times 
      if len(s) >2:
        s=s[:2]
      try:
         if int(s) > 59:
           s=59
      except ValueError:
         s=59          

      if int(m) > 59:
         m=59

      #now handle the PR nights (2012 = Personal Record, 13,14+15 = Prediction run)
      if int(m) < 0:
        SET_PR_NIGHT = 1
      if SET_PR_NIGHT == 1:
        m = 10 + int(m)   # PR times are now stored as deviation from 10:00 mm:ss
 
      if int(m) < 21: #if mins time < 21 then set hours =1
        h = 1      
      np_times_week=np.append(np_times_week,datetime.time(int(h),int(m),int(s)))    


  #get max length of names string
  maxl=get_max_name_length(np_names_week)+1

  #print the resuls in      
  for i in range (0,len(np_names_week)) :    
    print ('{:<{}s}'.format(np_names_week[i],maxl),np_times_week[i],run_date)

  np_names_year = np.append(np_names_year,np_names_week)
  np_towns_year = np.append(np_towns_year,np_towns_week)
  np_times_year = np.append(np_times_year,np_towns_week)
  np_dates_year = np.append(np_dates_year,run_date)

  #Save the output to a file for a single week
  print ''
  fname='SRR_Caseys_results_'+str(run_date)
  print ('Number of Runners this week=',len(np_names_week))
  print ''

  if len(np_names_week) > 0 :
    #np.savez(fname,np_names_week=np_names_week,np_times_week=np_times_week,np_towns_week=np_towns_week)
    print (' ')
  else :
    print 'No file output : There is no data available for the week : ',str() 

#get max length of names string
maxl=get_max_name_length(np_names_year)
print ('')
print ('Number of Weeks =',len(url_links))
print ('Total Number of Runners this year=',len(np_names_year))


fname='SRR_Caseys_results_'+str(year)
np.savez(fname,np_names_year=np_names_year,np_times_year=np_times_year,np_towns_year=np_towns_year,np_dates_year=np_dates_year)

#npzfile = np.load('SRR_Caseys_results_2016-01-28.npz')
#npzfile.files
#npzfile['np_names_week'] # to show an array


