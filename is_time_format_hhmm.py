
#
# Code to check if a string has the 
# time format HH:MM.
# Return True or False
##################################################

def is_time_format_hhmm(my_string):
  my_string=my_string.lstrip()       #strip the left and right white space
  my_string=my_string.rstrip()      #strip the left and right white space
  tmp=my_string.split(":")  #split the string
  #only test for a number if xyz has 2 elements == otherwise this is age
  if len(tmp) > 1 :
    test_string=tmp[0]
    try:
        float(test_string)
        return True
    except ValueError:
        return False
