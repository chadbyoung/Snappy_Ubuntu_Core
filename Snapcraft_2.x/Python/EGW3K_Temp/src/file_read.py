######################################################################
#
# 
# Created on: July 7, 2017
# Author: Chad Young
# Contact: chad.young@dell.com
# File name: hts221_temp.py
# File ver: 0.02
# 
#  *** Important Notice ***
#
# This program should not be used commercially as I am hacking together
# what ever it takes to make this program work. This program is for  
# test purposes only. Use it with caution as you would with anything 
# that you find on the internet for free :)
#
#
######################################################################
#
#
# This program is written for the Dell Edge Gateway 3002. This program 
# will not work on other systems due to the iio:device being on a 
# different address - iio:device[0,1,2]
#
# In this program three files are read. The integer and floats from 
# these files will then be run throught a formula and temperature will
# be the result. The formula is:
#    T = ((in_temp_raw + in_temp_offset) * in_temp_scale))/1000
#
#
######################################################################

###########
# STATUS
# I am in the process of adding the capability of the program
# to detect what model of gateway it is running on and from that
# use the correct formula to get the temperature 
###########

# needed to find a file later on
import os.path

# This the device you are testing for
sensor = "hts221"

# The variable below is need for finial formula 
div1k = 1000


def main():
    
    #print'DEBUG'
    #print'Dev0 is', Dev0
    #print'DEBUG'
 
    ### find the device(#) with a folder titled "name" and it contents are "hts221"
    # TODO
    # Create loop to load # in "iio:device[X]" where X = 0,1,2.
    # Create a variable for this path /sys/bus/iio/devices/iio:device0/name","r"
    # Standardize on a name for "iio_dev0 = open...."
    # Standardize on a name for "iio_dev0_model..."

    filename = "/sys/bus/iio/devices/iio:device0/name"

    def file_or_directory(filename)
        if os.path.isfile(filename):
            print('Filename {0} is a file'.format(filename))
        else:
            print('Filename {0} is a directory'format(filename))






    
    # Read the model of the gateway you are working on
    # Read iio:device0
    iio_dev0 = open("/sys/bus/iio/devices/iio:device0/name","r")
    iio_dev0_model = iio_dev0.readline().strip()
    Dev0 = str(iio_dev0_model)
    iio_dev0.close
    
    # Read iio:device1
    iio_dev1 = open("/sys/bus/iio/devices/iio:device1/name","r")
    iio_dev1_model = iio_dev1.readline().strip()
    Dev1 = str(iio_dev1_model)
    iio_dev1.close
    
    # Read iio:device2
    iio_dev2 = open("/sys/bus/iio/devices/iio:device2/name","r")
    iio_dev2_model = iio_dev2.readline().strip()
    Dev2 = str(iio_dev2_model)
    iio_dev2.close
    
    ### Read the three file names using the loop variable names from above
    # TODO
    # Use the same loop from above to read the files
    # Use the variable path like you did looking for the contents above
    # The number of lines needed to read the file can be reduced with a loop
    

    # Read the "in_temp_raw" file 
    in_temp_raw = open("/sys/bus/iio/devices/iio:device0/in_temp_raw","r")
    flt_raw_input = in_temp_raw.readline()
    InTempRaw = float(flt_raw_input)
    in_temp_raw.close
         
    # Read the "in_temp_offset" file 
    in_temp_offset = open("/sys/bus/iio/devices/iio:device0/in_temp_offset","r")
    flt_offset_input = in_temp_offset.readline()
    InTempOffset = float(flt_offset_input)
    in_temp_offset.close
         
    # Read the "in_temp_scale" file 
    in_temp_scale = open("/sys/bus/iio/devices/iio:device0/in_temp_scale","r")
    flt_scale_input = in_temp_scale.readline()
    InTempScale = float(flt_scale_input)
    in_temp_scale.close
    
    # Use this for Debug
    ######################################################################
    # Display the in_temp_raw number
    #print'The in_temp_raw number is', InTempRaw
    # Display the in_temp_offset number
    #print'The in_temp_offset number is', InTempOffset
    # Display the in_temp_scale number
    #print'The in_temp_scale number is', InTempScale
    ######################################################################
    
   ### Get the components of the temperature and do the math
   # TODO 
   # The if/else command will have to change as the you should not have a loop now since the loop(s) above will yield
   #   all the data that you need to get the temperature
   # One thing to look into is the "Div by 1K" stuff as this could be model specific.

    if Dev0 == "hts221":
    
       def phase1(num1, num2):
           return num1 + num2
    
       def phase2 (num1, num2):
           return num1 * num2
    
       def phase3 (num1, num2):
          return num1 / num2

       # Get the sum of the numbers
       total1 = phase1(InTempRaw, InTempOffset)

       # Multiply the numbers
       total2 = phase2(total1, InTempScale)

       # Divide by 1000
       total3 = phase3(total2, div1k)

       # Print the temp
       print ''
       print 'The internal temperature of the EGW3002 is', format(total2, ',.2f'), 'degrees celsius'
       print ''

    else:
	print'The ST HTS221 is not installed on this machine'
        print'The device found was a:', Dev0
        print'The equiv of Dev0 is:', str(iio_dev0_model)
        print'The device tested against was:', sensor


# Call the main function
main()
