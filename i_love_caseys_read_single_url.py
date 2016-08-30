
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

#############################################################
#       M A I N   C O D E
#
# This python script will read Somerville Road Runners
# Thursday evening Caseys run names, times and towns
# 
# inputs
# ------
# url : specify the url that you want to read from
#
# outputs
# -------
# .npz file containing numpy arrays for names, time and date
##############################################################    

#This is the web page to read from
url = 'http://www.srr.org/events/thursday-night-run/2016/2016.01.28.htm'

location='work' #this depends on your available python packages 
                # and if you are using a linux or windows machine

#import packages
import re
import datetime
import numpy as np
import is_time_format_hhmm
import get_date_from_url

if location == "home":
  import urllib.request as ur 
if location == "work":
  import urllib

if location == "home":
  page = ur.urlopen(url) 
  page2 = page.read()
  page_html = str(page2,'utf-8')        #home only
  cleantext = remove_html_markup(page_html)

if location == "work":
  page = urllib.urlopen(url) 
  page_html = page.read()

#clean the html text
cleantext = remove_html_markup(page_html)

#now pull out the date of the run from the url 
run_date=get_date_from_url.get_date_from_url(url)

#split up the text string
tmp2 = cleantext.split("\n")

#strip the left and right whitespace away from each element in the list
tmp3 = [x.lstrip(' ') for x in tmp2]
tmp3 = [x.rstrip(' ') for x in tmp3]
text_find='Notes'  # 'Notes' always appears before the 1st runner
start = tmp3.index(text_find)+1

np_names_week =np.array([]) #initialize names
np_towns_week =np.array([])
np_times_week =np.array([])

#loop over the number of athletes // check for the hh:mm format and append info to np arrays
n_athletes = len(tmp2)
for p in range(start,n_athletes) :
  x=tmp2[p]
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

#print the number of runners
print ''
fname='SRR_Caseys_results_'+str(run_date)
print fname
print 'Number of runners  =',len(np_names_week)
print ''
#print the formatted results       
for i in range (0,len(np_names_week)) :
    print ('{:<{}s}'.format(np_names_week[i],maxl),np_times_week[i],run_date)

#Save the output to a file for a single week
if len(np_names_week) > 0 :
  np.savez(fname,np_names_week=np_names_week,np_times_week=np_times_week,np_towns_week=np_towns_week)
else :
  print 'No file output : There is no data available for the week : ',str() 

#To load this file use
#npzfile = np.load('SRR_Caseys_results_2016-01-28.npz')
#npzfile.files
#npzfile['np_names_week'] # to show an array


