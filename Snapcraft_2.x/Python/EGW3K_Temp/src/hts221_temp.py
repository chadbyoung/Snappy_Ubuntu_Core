######################################################################
#
# 
# Created on: July 4, 2017
# Author: Chad Young
# Contact: chad.young@dell.com
# File name: hts221_temp.py
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

# This the device you are testing for
sensor = "hts221"

# The variable below is need for finial formula 
div1k = 1000


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


# Debug
######################################################################
# Display the in_temp_raw number
#print('The in_temp_raw number is', InTempRaw)
# Display the in_temp_offset number
#print('The in_temp_offset number is', InTempOffset)
# Display the in_temp_scale number
#print('The in_temp_scale number is', InTempScale)
######################################################################

def main():
    
    #print'DEBUG'
    #print'Dev0 is', Dev0
    #print'DEBUG'
    
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
       print 'The internal temperature of the EGW3002 is', format(total3, ',.2f'), 'degrees celsius'
       print ''

    else:
	print'The ST HTS221 is not installed on this machine'
        print'The device found was a:', Dev0
        print'The equiv of Dev0 is:', str(iio_dev0_model)
        print'The device tested against was:', sensor


# Call the main function
main()
