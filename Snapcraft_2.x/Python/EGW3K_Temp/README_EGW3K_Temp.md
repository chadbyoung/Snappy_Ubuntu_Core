# Readme for EGW3K-HTS221 snap
*For questions, please email chad.young@dell.com*
 
&nbsp;

This program will read the ST HTS221 sensor on the EGW3K 3002 and then display the
temperature. This is done by reading three files located here:
    
    /sys/bus/iio/devices/iio:device0

The files that are read are:

    in_temp_raw (int)

    in_temp_offset (int)

    in_temp_scale (float)

The int/floats in the files above are then run through the following formula:
    
    T = ((in_temp_raw + in_temp_offset) * in_temp_scale))

## Instructions
To display the temperature, run the following commmand:

    egw3k-hts221.temperature

