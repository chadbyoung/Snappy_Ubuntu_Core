# Version 0.0201

# TODO
# Import the file header from the previous file
# If the file header does not explain what the purpose of the program is
# -- then you will need to write a short  description

from os import path

# set the main loop count to 0
i = 0

# The main loop is set to 4 because as I have not seen a device with more
# than 4 devices on the EGW3K.
while i < 4:
    # DEBUG
    # print "while pass", i

    # PATH = "./device%s/name" % i
    # This is the main path to the directory & file name that will be looked for
    PATH = "/sys/bus/iio/devices/iio:device%s/name" % i

    # if path.exists('./device%s/name' % i) and path.isfile('./device%s/name' % i):
    if path.exists('/sys/bus/iio/devices/iio:device%s/name' % i) and path.isfile('/sys/bus/iio/devices/iio:device%s/name' % i):

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
            # Leave the line blank in production
            # print ""
            break
    else:
        print("The file that this program is looking for cannot be found")

        # need to add the couter so that the main loop will continue
        i = i + 1
    exit()
