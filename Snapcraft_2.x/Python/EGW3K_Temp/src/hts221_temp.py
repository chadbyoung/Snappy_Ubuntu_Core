######################################################################
#
#
# Created on: July 10, 2017
# Author: Chad Young
# Contact: chad.young@dell.com
# File name: hts221_temp.py
# File ver: 0.0201
#
#  *** Important Notice ***
#
# This program should not be used commercially as I am hacking together
# what ever it takes to make this program work. This program is for••
# test purposes only. Use it with caution as you would with anything•
# that you find on the internet for free :)
#
#
######################################################################
#
#
# This program is written for the Dell Edge Gateway 3002. This program•
# will not work on other systems due to the iio:device being on a•
# different address - iio:device[0,1,2]
#
# In this program three files are read. The integer and floats from•
# these files will then be run throught a formula and temperature will
# be the result. The formula is:
#   T = ((in_temp_raw + in_temp_offset) * in_temp_scale))/1000
#
#
######################################################################

from os import path

# set the main loop count to 0
i = 0

# set the divider to 1k
# div1k = 1000

# The main loop is set to 4, and may need to be increased. I have not seen an
# EGW3K with more than 4 devices.
while i < 4:
    # DEBUG
    # print "while pass", i

    # PATH = "./device%s/name" % i
    # This is the main path to the directory & file name that will be looked for
    PATH = "/sys/bus/iio/devices/iio:device%s/name" % i

    # if path.exists('./device%s/name' % i) and
    # -- path.isfile('./device%s/name' % i):
    if path.exists('/sys/bus/iio/devices/iio:device%s/name' % i) and \
            path.isfile('/sys/bus/iio/devices/iio:device%s/name' % i):

        # DEBUG
        # print "PATH =", PATH

        # fline = open('./device%s/name' % i, "r")
        isfile = open('/sys/bus/iio/devices/iio:device%s/name' % i, "r")
        isfile_text = isfile.readline().strip()
        sttemp = str(isfile_text)
        isfile.close

        if str(sttemp) == "hts221":
            # DEBUG
            # print "The file with the text hts221 what found here:", PATH

            # Read the "in_temp_raw" file
            in_temp_raw = open("/sys/bus/iio/devices/iio:device0/in_temp_raw", "r")
            flt_raw_input = in_temp_raw.readline()
            InTempRaw = float(flt_raw_input)
            in_temp_raw.close

            # Read the "in_temp_offset" file
            in_temp_offset = open("/sys/bus/iio/devices/iio:device0/in_temp_offset", "r")
            flt_offset_input = in_temp_offset.readline()
            InTempOffset = float(flt_offset_input)
            in_temp_offset.close

            # Read the "in_temp_scale" file
            in_temp_scale = open("/sys/bus/iio/devices/iio:device0/in_temp_scale", "r")
            flt_scale_input = in_temp_scale.readline()
            InTempScale = float(flt_scale_input)
            in_temp_scale.close

            # The next few line are setting up the def and the math for the
            # -- main temperature function
            def phase1(num1, num2):
                return num1 + num2

            def phase2(num1, num2):
                return num1 * num2

            # def phase3(num1, num2):
            #     return num1 / num2

            # Get the sum of the numbers
            total1 = phase1(InTempRaw, InTempOffset)

            # Multiply the numbers
            total2 = phase2(total1, InTempScale)

            # Divide by 1000 - may be needed
            # total3 = phase3 (total2, div1k)

            # Format and print the temperature data, should look like 35.51
            # The temperature is in degrees celcius
            print(format(total2, ',.2f'))

        else:
            # DEBUG
            # print "The file exists but the text is wrong"
            break
    else:
        print("The file that this program is looking for cannot be found")

        # need to add the counter so that the main loop will continue
        i = i + 1
    exit()
