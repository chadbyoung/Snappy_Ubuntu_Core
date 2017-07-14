# Readme for EGW3K-HTS221 snap
*For questions, please email chad.young@dell.com*  

This program will try to find the ST HTS221 sensor on a Dell Edge Gateway 300X by looking for a specific iio directory with  
a file labeled "name" and its contents being "hts221". After finding this directory with said file, the program will read the int  
and float numbers in the three files located here:

    /sys/bus/iio/devices/iio:device[0,1,2,3]

The files that are read are:

    in_temp_raw (int)
    in_temp_offset (int)
    in_temp_scale (float)

The int/floats in the files above are then run through the following formula:

    T = (((in_temp_raw + in_temp_offset) * in_temp_scale))  
    Where T is in degrees celsius

## Instructions
To display the temperature, run the following commmand:

    egw3k-hts221.temperature

