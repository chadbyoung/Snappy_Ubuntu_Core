# This is a work in progress.

# Read the BIOS vendor
bios_vendor = open("/sys/class/dmi/id/bios_vendor","r")
string_input = bios_vendor.readline()
BiosVendor = str(string_input)
bios_vendor.close

# Read   the BIOS date
bios_date = open("/sys/class/dmi/id/bios_date","r")
string_input = bios_date.readline()
BiosDate = str(string_input)
bios_date.close

# Read the BIOS version
bios_version = open("/sys/class/dmi/id/bios_version","r")
string_input = bios_version.readline()
BiosVersion = str(string_input)
bios_version.close


# Display the BIOS information
print(BiosVendor)
print(BiosDate)
print(BiosVersion)


#Read the "in_temp_raw" file 
in_temp_raw = open("/sys/bus/iio/devices/iio\:device0/in\_temp\_raw","r")
int_raw_input = in_temp_raw.readline()
InTempRaw = int(int_raw_input)
in_temp_raw.close

#Display the file information
print(InTempRaw)

