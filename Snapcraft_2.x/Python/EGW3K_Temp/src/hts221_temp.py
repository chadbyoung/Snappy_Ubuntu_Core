# Version 0.0200

from os import path

i = 0

while i < 3:
    # DEBUG
    # print "while pass", i

    # PATH = "./device%s/name" % i
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

            def phase1(num1, num2):
                return num1 + num2

            def phase2(num1, num2):
                return num1 * num2

            def phase3(num1, num2):
                return num1 / num2

            # Get the sum of the numbers
            total1 = phase1(InTempRaw, InTempOffset)

            # Multiply the numbers
            total2 = phase2(total1, InTempScale)

            # Divide by 1000 - may be needed
            # total3 = phase3 (total2, div1k)

            # Print the temp
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
