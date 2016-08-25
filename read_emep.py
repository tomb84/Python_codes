

# This file will read measurements of from the 
# European Monitoring and Evaluation Programme (EMEP) 
#
#
#
# Written by Tom Breider August 2016
###########################################

#import the packages
import os 
import fileinput
import numpy as np

#define the data directory
datadir="/home/tbreider/DATA/EMEP_1980_2013/TOMS_IDL_CODES/DATA_FILES/"

#set the first station code to a dummy value
MY_STATION_CODE='DUMMY'
#np_data_site_will hold data for the site over multiple years
np_data_site=np.array([])

#loop over the files in the data directory
for file in os.listdir(datadir):

   # Use to limit the read to a certain station
   if file.startswith("NO000"):


     #Initialize ignore_data
     ignore_data=False

     filename=datadir+file 
     #Get the station code from the filename
     tmp2=filename.split('/')
     tmp3=tmp2[-1].split('.')
     station_code = tmp3[0]

     #If we are reading data from a new station = write the previous stations data to a file
     if station_code != MY_STATION_CODE:
        print'All obs data for this site'
        print(len(np_data_site))
        #Save out the file containing the array
        fname='EMEP_xso4_observations_'+MY_STATION_CODE+'_startyr_2010.npy'
        np.save(fname,np_data_site)
        np_data_site=np.array([])

     #Update my station code
     MY_STATION_CODE = station_code

     #Get the obs year from the filename
     tmp4=tmp3[1]
     year=float(tmp4[:4])

     #if(year == 1998.) :

     #initialize data_tmp
     np_data_tmp=np.array([])
     print("Reading File "+file)
     # initialize read data
     read_data=0

     #Loop over the file lines 
     for line in open(datadir+file).readlines():
 
         #remove whitespace from left edge of line
         #tmp=line.lstrip()
         #split the string by blank spaces
         tmp2=line.split()

         if(tmp2[0] == 'Station' and tmp2[1] == 'name:') :
           station_name=tmp2[2]

         #starttime always appears on the last line before the start of the dat
         if(tmp2[0] == 'starttime') :
           read_data=read_data+1
         
         #Check this line for the location of the species that we want to read  
         if read_data == 1 :
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
              #print("found SO4 index = ",tmp2.index('XSO4--')) 
             except ValueError:
              so4_index=-1
    
           #Set ignore_data = True is dpecies is not present in the file
           if so4_index == -1 :
              ignore_data=True            
              
         #start reading the data now we know the position of the species in the file
         elif read_data == 2 :

            # Read the data only if XSO4 is present
            if not ignore_data:
               so4_index_flag = so4_index+1
               if(float(tmp2[so4_index_flag]) == 0.) :
                 np_data_tmp=np.append(np_data_tmp,float(tmp2[so4_index]))
               else : #Set the obs to np.nan 
                 np_data_tmp=np.append(np_data_tmp,np.nan)


  ############################################################
  ##   STATISTICS
  ##
     #Write statistics if data is present in the file
     if not ignore_data:
         #np_data=np.array(data_tmp)

         #print 'Results for EMEP station ',station_name,' ',station_code,' year:',year
         print 'num days=',len(np_data_tmp)
         print 'Num obs =',len(np_data_tmp)-np.count_nonzero(np.isnan(np_data_tmp))
         print 'mean    =','%1.3f' %np.nanmean(np_data_tmp)
         print 'std dev =','%1.3f' %np.nanstd(np_data_tmp)
         print 'median  =','%1.3f' %np.median(np_data_tmp)
         print ''

     #If data is not found then print an error message
     if ignore_data:
         print 'Ignored data for this file since the desired species is not available '
         print ''

     #append the data to a continuous array for this station
     np_data_site=np.append(np_data_site,np_data_tmp)

     #Save out the file containing the array
     #fname='EMEP_xso4_observations_'+station_name+'_'+station_code+'_startyr_2010.npy'
     #np.save(fname,np_data_site)


#Now use matplot lib to plot the data
#import matplotlib as plt


