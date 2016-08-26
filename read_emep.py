

## FUNCTION TO PRINT DATA STATISTICS
def print_stats(np_data_tmp):

         #print 'Results for EMEP station ',station_name,' ',station_code,' year:',year
         print 'num days=',len(np_data_tmp)
         print 'Num obs =',len(np_data_tmp)-np.count_nonzero(np.isnan(np_data_tmp))
         print 'mean    =','%1.3f' %np.nanmean(np_data_tmp)
         print 'std dev =','%1.3f' %np.nanstd(np_data_tmp)
         print 'median  =','%1.3f' %stats.nanmedian(np_data_tmp)
         print ''

## FUNCTION TO OUTPUT THE DATA ARRAY FOR EACH SITE
def save_to_data_file (station_code,get_year,np_data_site) :

  #Save out the file containing the array
  fname='EMEP_xso4_observations_'+station_code+'_'+str(get_year[0])+'_'+str(get_year[1])+'.npy'
  #np.save(fname,np_data_site)
  print'Total number of days at this station = ',(len(np_data_site))
  print 'Num obs =',len(np_data_site)-np.count_nonzero(np.isnan(np_data_site))
  print ''

  if len(np_data_site)-np.count_nonzero(np.isnan(np_data_site)) > 0 :
    np.save(fname,np_data_site)
  else :
    print 'No file output : There are no observations at station ',station_code,' for the period : ',str(get_year[0])+' '+str(get_year[1])

################################################################
#             M A I N  C O D E 
#
# This file will read measurements of from the 
# European Monitoring and Evaluation Programme (EMEP) 
# and output to .npy file
#
# Written by Tom Breider August 2016
#
# inputs 
# --------
# GET_SITE : allows user to restrict read to only certain sites (Default is all sites =  "" )
#          : e.g. "NO" = all sites in Norway // "NO0055" = Karasjok
# GET_YEAR : allows user to restrict the years the data is read in for (Default value is 1970-2015)
#          : e.g. GET_YEAR[1980] or GET_YEAR[1980,1990] = [order is [BeginYr,EndYr] 
#
# outputs
# -------
# .npy file with name 'EMEP_xso4_observations_[STATION_CODE]_[STARTYR]_[ENDYR].npy'
#
# to load this file back into python
# import numpy
# x = numpy.load([FILENAME])
#
############################################

#import the packages
import os 
import fileinput
import numpy as np
import calendar
from scipy import stats

#User defined options
GET_SITE="NO0055"
GET_YEAR=[1970,2015]
if len(GET_YEAR) == 1 :
  GET_YEAR.extend(GET_YEAR)

#define the data directory
datadir="/home/tbreider/DATA/EMEP_1980_2013/TOMS_IDL_CODES/DATA_FILES/"

#set the first station code to a dummy value
MY_STATION_CODE='DUMMY'

#np_data_site_will hold data for the site over multiple years
np_data_site=np.array([])

#loop over the files in the data directory
for file in os.listdir(datadir):

  np_data_tmp=np.array([])  #initialize data_tmp

  # Use to limit the read to a certain station
  if file.startswith(GET_SITE):

     #Initialize ignore_data
     ignore_data=False

     filename=datadir+file 
     #Get the station code from the filename
     tmp2=filename.split('/')
     tmp3=tmp2[-1].split('.')
     station_code = tmp3[0]

     #Get the obs year from the filename
     tmp4=tmp3[1]
     year=int(tmp4[:4])
     if MY_STATION_CODE == 'DUMMY': 
       start_yr=year
 
     if year >= GET_YEAR[0] and year <= GET_YEAR[1]:

       #If we are reading data from a new station = write the previous stations data to a file
       if station_code != MY_STATION_CODE and MY_STATION_CODE != 'DUMMY':
         #Save out the file containing the array
         save_to_data_file(station_code,start_yr,np_data_site)

         #reset np_data_site and start_yr
         np_data_site=np.array([])
         start_yr=year 

       #Update my station code
       MY_STATION_CODE = station_code

       #Call read data_file 
       print("Reading File "+filename)
       read_data=0 # initialize read data

       #Loop over the file lines 
       for line in open(filename).readlines():

         tmp2=line.split() #split the string by blank spaces

         if(tmp2[0] == 'Station' and tmp2[1] == 'name:') :
           station_name=tmp2[2]

         if(tmp2[0] == 'starttime') :  #starttime always appears on the last line before the start of the data
           read_data=read_data+1

         if read_data == 1 : #Check the line for the location of the species that we want to read
           read_data=read_data+1

           #look for index of value
           try:
             so4_index=tmp2.index('value')
           except ValueError:
             so4_index=-1
             #look for index of 'XSO4--' in line
           if so4_index == -1 :
             try:
              so4_index=tmp2.index('XSO4--')
              print("found SO4 index = ",tmp2.index('XSO4--'))
             except ValueError:
              so4_index=-1

           if so4_index == -1 : #Set ignore_data = True if species is not present in the file
              ignore_data=True

         #start reading the data now we know the position of the species in the file
         elif read_data >= 2 :

            #check that data starts on day 0
            if read_data == 2 :
              tmp3=tmp2[0].split('.')
              startday=int(tmp3[0])
              if startday != 0 :
                 for d in range (0,startday):
                   np_data_tmp=np.append(np_data_tmp,np.nan) # set vals to nans

            # Read the data only if XSO4 is present
            if not ignore_data:
               so4_index_flag = so4_index+1
               #only read the value if the error flag is 0.
               if(float(tmp2[so4_index_flag]) == 0.) :
                 np_data_tmp=np.append(np_data_tmp,float(tmp2[so4_index]))
               else : #Set the obs to np.nan 
                 np_data_tmp=np.append(np_data_tmp,np.nan)

            read_data=read_data+1 #

       #if the data ends before the end of the year then add in extra days
       yrdays = 366 if calendar.isleap(year) else 365
       if len(np_data_tmp) != yrdays :
         for d in range (len(np_data_tmp)+1,yrdays+1): 
           np_data_tmp=np.append(np_data_tmp,np.nan)    


     ############################################################
     ##   STATISTICS
       #Output statistics if data is present in the file
       if not ignore_data:
         print_stats(np_data_tmp)
       #If data is not found then print an error message
       if ignore_data:
         print 'Ignored data for this file since the desired species is not available '
         print ''

       ############################################################
       #append the data to a continuous timeseries array for this station
       np_data_site=np.append(np_data_site,np_data_tmp)


#This is the last station so save out the file containing the array
save_to_data_file(station_code,GET_YEAR,np_data_site)

