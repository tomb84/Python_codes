
#
# Function will return the date from a url
#

import datetime

def get_date_from_url(link):
    datex=link.replace('.htm','')
    datex=link.replace('.html','')
    datex=datex.split('/')
    datex2=datex[len(datex)-1]
    datex2=datex2.split('.')
    if len(datex2) == 1:
      datex2=datex2[0].split('-')
    run_date = (datetime.date(int(datex2[0]),int(datex2[1]),int(datex2[2])))
    return run_date
