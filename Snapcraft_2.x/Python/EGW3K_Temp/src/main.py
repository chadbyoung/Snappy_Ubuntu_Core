# In this program you will read three files. The integer and floats from these file will 
# then be run throught a formula and temperature will be the result. 


def main():
    
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
     
     
     # Display the in_temp_raw number
     print('The in_temp_raw number is', InTempRaw)
     
     # Display the in_temp_offset number
     print('The in_temp_offset number is', InTempOffset)
     
     # Display the in_temp_scale number
     print('The in_temp_scale number is', InTempScale)

     # Calculate the temperature
     total = cal_temp(InTempRaw, InTempOffset, InTempScale)

     # See if num1 and num2 add up
     sumab = cal_ab(InTempRaw, InTempOffset)

     # Display the sum of num1 and num2
     print('num1 + num2 =', sumab)

     # Display the temperature
     print ('The temperature is', total, ' degrees celsius')


def cal_ab(num1, num2):
    result = num1 + num2
    return result


def cal_temp(num1, num2, num3):
    result = ((num1 + num2) * num3)
    return result

# Call the main function
main()
