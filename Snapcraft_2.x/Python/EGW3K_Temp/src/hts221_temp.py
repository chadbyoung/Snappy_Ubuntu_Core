######################################################################
#
#
# Created on: July 17, 2017
# Author: Chad Young
# Contact: chad.young@dell.com
# File name: hts221_temp.py
# File ver: 0.0300
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
# This program is written for the Dell Edge Gateway 300X series. This
# program may not work on other Dell Edged Gateways as I do not know
# what io device address is being used for the ST HTS221.
#
# In this program three files are read. The floats from these files
# will then be run through a formula and temperature in degrees
# celsius will be the result. The formula used is:
#
#   T = ((in_temp_raw + in_temp_offset) * in_temp_scale))/1000
#
#
######################################################################

from os import path

# set the main loop count to 0
i = 0

# DEBUG
# set the divider to 1k
# div1k = 1000

# The main loop is set to 4, and may need to be increased. I have not seen an
# EGW3K with more than 4 devices.
while i < 4:
    # DEBUG
    # print("Primary while loop #", i)

    # DEBUG
    PATH = "/sys/bus/iio/devices/iio:device%s/name" % i

    # if path.exists('./device%s/name' % i) and
    # -- path.isfile('./device%s/name' % i):
    if path.exists('/sys/bus/iio/devices/iio:device%s/name' % i) and \
            path.isfile('/sys/bus/iio/devices/iio:device%s/name' % i):

        # DEBUG
        # print("First IF Loop")
        # print("The path exists and it is a file")
        # print("PATH =", PATH)

        # fline = open('./device%s/name' % i, "r")
        isfile = open('/sys/bus/iio/devices/iio:device%s/name' % i, "r")
        isfile_text = isfile.readline().strip()
        sttemp = str(isfile_text)
        isfile.close

        # DEBUG
        # print("sttemp is", sttemp)

        if str(sttemp) == "hts221":
            # DEBUG
            # print("Second IF loop")
            # print("The file with the text hts221 what found here:", PATH)

            # Read the "in_temp_raw" file
            in_temp_raw = open('/sys/bus/iio/devices/iio:device%s/in_temp_raw' % i, "r")
            flt_raw_input = in_temp_raw.readline()
            InTempRaw = float(flt_raw_input)
            # DEBUG
            # print("InTempRaw =", InTempRaw)
            in_temp_raw.close

            # Read the "in_temp_offset" file
            in_temp_offset = open('/sys/bus/iio/devices/iio:device%s/in_temp_offset' % i, "r")
            flt_offset_input = in_temp_offset.readline()
            InTempOffset = float(flt_offset_input)
            # DEBUG
            # print("InTempOffset =", InTempOffset)
            in_temp_offset.close

            # Read the "in_temp_scale" file
            in_temp_scale = open('/sys/bus/iio/devices/iio:device%s/in_temp_scale' % i, "r")
            flt_scale_input = in_temp_scale.readline()
            InTempScale = float(flt_scale_input)
            # DEBUG
            # print("InTempScale =", InTempScale)
            in_temp_scale.close

            # The next few line are setting up the def and the math for the
            # -- main temperature function
            def phase1(num1, num2):
                return num1 + num2

            def phase2(num1, num2):
                return num1 * num2

            # DEBUG
            # def phase3(num1, num2):
            #     return num1 / num2

            # Get the sum of the numbers
            total1 = phase1(InTempRaw, InTempOffset)

            # Multiply the numbers
            total2 = phase2(total1, InTempScale)

            # DEBUG
            # Divide by 1000 - may be needed
            # total3 = phase3 (total2, div1k)

            # Format and print the temperature data, should look like 35.51 and
            # is in degrees celcius
            print(format(total2, ',.2f'))

            # No need to run anymore
            exit()

        else:
            # DEBUG
            # print("Second Else loop")
            # print("The file exists but the text is wrong")
            pass
    else:
        # DEBUG
        # print("first Else loop")
        # print("The file that this program is looking for cannot be found")
        pass

        # need to add the counter so that the main loop will continue
    i = i + 1

exit()
