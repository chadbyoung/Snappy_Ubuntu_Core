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

# The variable below is need for finial formula 
div1k = 1000

# Read the "in_temp_raw" file 
in_temp_raw = open("/sys/bus/iio/devices/iio:device0/in_temp_raw","r")
int_raw_input = in_temp_raw.readline()
InTempRaw = int(int_raw_input)
in_temp_raw.close
     
# Read the "in_temp_offset" file 
in_temp_offset = open("/sys/bus/iio/devices/iio:device0/in_temp_offset","r")
int_offset_input = in_temp_offset.readline()
InTempOffset = int(int_offset_input)
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



# Call the main function
main()
