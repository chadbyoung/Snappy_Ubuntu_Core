#!/bin/bash
# High-Level System Profiler (HLSP)
# Copyright (c) 2016 Dell Inc. All rights reserved.
# Created by Rory Rudolph <rory_rudolph@dell.com>
VERSION="3.1"

###############
#  VARIABLES  #
###############

DEFAULT_DIR="."
DEFAULT_SAR_FILE="hlsp.bin"
DEFAULT_DMI_FILE="hlsp.info"
DEB_SYSSTAT="./sysstat_11.0.1-1_amd64.deb"
DEB_LIBSENSORS4="./libsensors4_3.3.5-2_amd64.deb"
DEB_DMIDECODE="./dmidecode_2.12-3_amd64.deb"

###############
#  FUNCTIONS  #
###############

# Prints the help text when -? or --help is used as a parameter
# Does not exit the program, just prints the text
print_help()
{
	local pad
	for (( i = 0; i < ${#0}; i++ )); do
		pad="$pad "
	done
	cat <<__HELP_TXT__
USAGE: $0 [-d|--dir DIR] [-s|--samples NUM] [-i|--interval SEC] \\
       $pad [--skip-dmi] [--skip-sar]
       $0 [--install] [--remove]
       $0 [-V|--version]
       $0 [-?|--help]

High-Level System Profiler (hlsp)
Copyright (c) 2016 Dell Inc. All rights reserved.
This script gathers system details and usage info using the dmidecode and
sysstat packages. If these two packages are not present on the system,
installation will be attempted. After successful installation of either
package, they will be used to gather data about the system:
(1) dmidecode will gather hardware information from the system's DMI table,
    if available. If a DMI table is not available, other *NIX utilities like
    lscpu may be run to gather info. On success, '$DEFAULT_DMI_FILE' is created.
(2) The System Activity Report (sar) utility will be used to collect system
    utilization, saturation, and error statistics. This utility will be run
    as a persistent background process and - by default - will collect data
    in one second intervals for two hours (totaling 7200 samples). On
    success, '$DEFAULT_SAR_FILE' will be created. This binary file can be post-
    processed with the 'sadf' utility (from sysstat).
You may be prompted for an administrative password on some systems. For more
information see man pages for 'sar', 'sadf', and 'dmidecode'.

OPTIONS:
    -d, --dir DIR       The directory to store output files. Can be relative
                        or absolute. Will be created if does not exist.
                        Defaults to current directory.
    -i, --interval SEC  Seconds between samples. Defaults to 1. Must be an
                        integer >= 1.
    -s, --samples NUM   Number of samples to record. Defaults to 7200. Must
                        be an integer >= 1.
        --force-dpkg    Force installation/removal  method to use dpkg instead
                        of apt-get
        --skip-dmi      Don't gather information using dmidecode utility
        --skip-sar      Don't gather information using sar utility
        --install       Runs the installation procedures for the needed .deb
                        packages (libsensors4, sysstat, dmidecode). Can only
                        be used with the --remove flag and no other operations
                        will be performed
        --remove        Runs the removal procedures for the .deb packages.
                        Can only be used with the --install flag and no other
                        operations will be performed
    -V, --version       Print the version and exits
    -?, --help          Print this help message and exits

Report bugs to Rory Rudolph <rory_rudolph@dell.com>
__HELP_TXT__
}

# Call this function with a string error message and exit code to print the
# message and quit the program with exit status. Defaults to "An unknown
# error occurred" and error code 1 if not specified.
# USAGE: errex [MSG [CODE]]
errex()
{
	local msg
	local code
	[[ -z $1 ]] && msg="An unknown error occurred" || msg="$1"
	printf "${RED}ERROR${RST}: $msg\n"
	[[ $2 =~ [0-9]+ ]] && code=$2 || code=1
	exit $code
}

# The first argument "$1" is used as the argument to "which"
# to determine if the argument $1 is installed and available
is_installed()
{
	local what
	local out
	local ret
	what="$1"
	out=$( which "$what" )
	ret=$?
	[[ $ret -eq 0 && -x $out ]] && return 0
	return 1
}

# The first argument "$1" is checked to determine if it is a valid
# file or not
is_file()
{
	local f="${1:-}"
	# must split up declaration and assignment for fname
	local fname
	fname=$( basename "$f" )
	[[ -z $fname ]] && errex "Invalid filename '$fname'"
	# do file exist test
	if [[ -e "$f" ]]; then
		echo "Found $fname"
		return 0
	else
		echo "Could not find $fname"
		return 1
	fi
}

# Tries to find 'sar' and installs it if not installed.
# If apt-get is not installed, it tries to use dpkg. If the deb files are
# not found, an error is thrown. If dpkg is not found, an error is thrown.
do_sar_install()
{
	if is_installed "sar" ; then
		# already installed, no need to install
		echo "Executable 'sar' is already installed. Nothing to do."
		return 0
	else
		# not installed, thus needs to be installed
		# check if the system is Snappy or if apt-get is not installed
		# if snappy or no apt-get, need to use dpkg instead of apt-get
		echo "Checking for installation method (apt-get or dpkg)"
		if [ $FORCE_DPKG -eq 1 ] || is_installed "snappy" || ! is_installed "apt-get" ; then
			# apt-get cannot be used on this system, need to use dpkg
			if is_installed "dpkg" ; then
				# dpkg is installed
				echo "Using dpkg to install sar"
				# make sure the .deb packages are found
				if is_file $DEB_SYSSTAT && is_file $DEB_LIBSENSORS4; then
					echo "Installing sar from the sysstat package"
					# remount as read-write
					sudo mount -v -o remount,rw /
					echo "Installing the libsensors4 dependency"
					sudo dpkg -i $DEB_LIBSENSORS4
					echo "Installing the sysstat package"
					sudo dpkg -i $DEB_SYSSTAT
				else
					errex "Could not find the *.deb files"
				fi
			else
				errex "Could not find an installation method"
			fi
		else
			echo "Using apt-get to install sar"
			# apt-get is installed
			# user will be prompted to continue installation
			sudo apt-get install sysstat
		fi

		# double-check to make sure sar is installed
		if is_installed "sar" ; then
			echo "Successfully installed sar"
			return 0
		fi

		errex "Problem installing sar"
		return 1 # should not be executed
	fi
}

# Removes the sysstat package via dpkg or apt-get
do_sar_remove()
{
	if is_installed "sar" ; then
		# sar is installed, need to uninstall
		echo "Found sar. Looking for removal method (apt-get or dpkg)"
		# check if system is snappy or if apt-get is not present
		# if either is true, need to use dpkg
		if [ $FORCE_DPKG -eq 1 ] || is_installed "snappy" || ! is_installed "apt-get" ; then
			echo "Using dpkg to remove"
			if is_installed "dpkg"; then
				echo "Removing the sysstat package"
				# remount as read-write
				sudo mount -v -o remount,rw /
				sudo dpkg -r sysstat
				echo "Removing the libsensors4 package"
				sudo dpkg -r libsensors4
			else
				errex "No removal method found"
			fi
		else
			# probably a redundant check for apt-get...
			if is_installed "apt-get"; then
				echo "Using apt-get for removal"
				# user will be prompted to continue remove
				echo "Removing sysstat"
				sudo apt-get purge sysstat
			else
				errex "No removal method found"
			fi
		fi

		# double-check to make sure it's gone
		if is_installed "sar" ; then
			errex "Problem removing sar"
		else
			echo "Successfully removed sar"
		fi
	else
		# sar is not installed, cannot remove
		echo "Executable sar is not installed. Nothing to do."
	fi
}

#
#
# TODO Document
do_dmi_install()
{
	local pkgname="dmidecode"
	if is_installed $pkgname ; then
		# already installed, no need to install
		echo "Executable '$pkgname' is already installed. Nothing to do."
		return 0
	else
		# not installed, thus needs to be installed
		# check if the system is Snappy or if apt-get is not installed
		# if snappy or no apt-get, need to use dpkg instead of apt-get
		echo "Checking for installation method (apt-get or dpkg)"
		if [ $FORCE_DPKG -eq 1 ] || is_installed "snappy" || ! is_installed "apt-get" ; then
			# apt-get cannot be used on this system, need to use dpkg
			if is_installed "dpkg" ; then
				# dpkg is installed
				echo "Using dpkg to install '$pkgname'"
				# make sure the .deb packages are found
				if is_file $DEB_DMIDECODE; then
					echo "Installing '$pkgname' from $DEB_DMIDECODE"
					# remount as read-write
					sudo mount -v -o remount,rw /
					sudo dpkg -i $DEB_DMIDECODE
				else
					errex "Could not find the deb file '$DEB_DMIDECODE'"
				fi
			else
				errex "Could not find an installation method"
			fi
		else
			echo "Using apt-get to install '$pkgname'"
			# apt-get is installed
			# user will be prompted to continue installation
			sudo apt-get install $pkgname
		fi

		# double-check to make sure installed correctly
		if is_installed $pkgname ; then
			echo "Successfully installed '$pkgname'"
			return 0
		fi

		errex "Problem installing '$pkgname'"
		return 1 # should never be executed, but just to be safe
	fi
} # end do_dmi_install()

#
#
# TODO Document
do_dmi_remove()
{
	local pkgname="dmidecode"
	if is_installed $pkgname ; then
		# is installed, need to uninstall
		echo "Found '$pkgname'. Looking for removal method (apt-get or dpkg)"
		# check if system is snappy or if apt-get is not present
		# if either is true, need to use dpkg
		if [ $FORCE_DPKG -eq 1 ] || is_installed "snappy" || ! is_installed "apt-get" ; then
			echo "Using dpkg to remove"
			if is_installed "dpkg"; then
				echo "Removing package '$pkgname'"
				# remount as read-write
				sudo mount -v -o remount,rw /
				sudo dpkg -r $pkgname
			else
				errex "No removal method found"
			fi
		else
			# probably a redundant check for apt-get... but oh well
			if is_installed "apt-get"; then
				echo "Using apt-get for removal"
				# user will be prompted to continue remove
				echo "Removing $pkgname"
				sudo apt-get purge $pkgname
			else
				errex "No removal method found"
			fi
		fi

		# double-check to make sure it's gone
		if is_installed $pkgname ; then
			errex "Problem removing '$pkgname'"
		else
			echo "Successfully removed '$pkgname'"
		fi
	else
		# is not installed, cannot remove
		echo "Executable '$pkgname' is not installed. Nothing to do."
	fi
} # end do_dmi_remove()

##################
#  MAIN PROGRAM  #
##################

# set these defaults
DO_DMI=1
DO_SAR=1
FORCE_DPKG=0

GREEN='\033[1;32m'
RED='\033[1;31m'
BLUE='\033[1;34m'
YELLOW='\033[1;33m'
RST='\033[0m'


# parse arguments
while [[ $# > 0 ]]; do
	case "$1" in
		-i|--interval )
			shift
			INTERVAL="$1"
			;;
		-d|--dir )
			shift
			DIR="$1"
			;;
		-s|--samples )
			shift
			SAMPLES="$1"
			;;
		--force-dpkg )
			FORCE_DPKG=1
			;;
		--skip-dmi )
			DO_DMI=0
			;;
		--skip-sar )
			DO_SAR=0
			;;
		--install )
			DO_INSTALL=1
			;;
		--remove )
			DO_REMOVE=1
			;;
		-V|--version )
			echo "$VERSION"
			exit 0
			;;
		-\?|--help )
			print_help
			exit 0
			;;
		* )
			errex "Invalid argument '$1'"
			;;
	esac
	shift
done

# if either --install or --remove is specified,
# then do those operations and exit
if [[ $DO_INSTALL -eq 1 || $DO_REMOVE -eq 1 ]]; then
	[[ $DO_INSTALL -eq 1 ]] && { do_sar_install; do_dmi_install; }
	[[ $DO_REMOVE -eq 1 ]] && { do_sar_remove; do_dmi_remove; }
	exit $?
fi

# arguments are parsed, now validate them before continuing
INTERVAL=${INTERVAL:-1}
[[ ! $INTERVAL =~ ^[0-9]+$ ]] && errex "Invalid interval '$INTERVAL'"
[[ $INTERVAL -lt 1 ]] && errex "Interval cannot be less than 1"
SAMPLES=${SAMPLES:-7200}
[[ ! $SAMPLES =~ ^[0-9]+$ ]] && errex "Invalid samples '$SAMPLES'"
[[ $SAMPLES -lt 1 ]] && errex "Samples cannot be less than 1"
# make sure these file names are set
[[ -z "$SARFILE" ]] && SARFILE="$DEFAULT_SAR_FILE"
[[ -z "$DMIFILE" ]] && DMIFILE="$DEFAULT_DMI_FILE"
[[ -z "$DIR" ]] && DIR="$DEFAULT_DIR"
# create the directory, if needed
[[ ! -d $DIR ]] && mkdir -vp "$DIR"

#-------------#
#  dmidecode  #
#-------------#

if [[ $DO_DMI -eq 1 ]]; then
	printf "${BLUE}Beginning dmidecode section${RST}\n"
	# check if dmidecode is installed/exists
	echo "Looking for executable 'dmidecode'"
	if is_installed "dmidecode" ; then
		# returned 0 (true, no error)
		echo "Found 'dmidecode'"
	else
		# returned 1 (false, error)
		echo "Did NOT find 'dmidecode'. Attempting to install"
		do_dmi_install
	fi

	# create a new empty output file
	DMIPATH="$DIR/$DMIFILE"
	echo "# SCRIPT VERSION=$VERSION" > "$DMIPATH"
	# loop through dmi types and get info
	for t in bios system baseboard chassis processor memory cache connector slot
	do
		echo "# ${t^^}" >> "$DMIPATH"
		sudo dmidecode -t $t >> "$DMIPATH"
		[[ $? -ne 0 ]] && errex "Problem executing 'dmidecode -t $t'"
	done
	if [[ -e $DMIPATH ]]; then
		printf "${GREEN}SUCCESS${RST}: Gathered DMI information\n"
		printf "Results found at ${YELLOW}$DMIPATH${RST}\n"
	else
		printf "${RED}ERROR${RST}: Could not gather DMI information\n"
	fi
else
	echo "Skipped dmidecode section"
fi

#-------#
#  sar  #
#-------#

if [[ $DO_SAR -eq 1 ]]; then
	printf "${BLUE}Beginning sar section${RST}\n"
	# check if sar is installed/exists
	echo "Looking for executable 'sar'"
	if is_installed "sar" ; then
		# returned 0 (true, no error)
		echo "Found 'sar'"
	else
		# returned 1 (false, error)
		echo "Did NOT find 'sar'. Attempting to install"
		do_sar_install
	fi

	SECONDS=$(( $INTERVAL * $SAMPLES ))
	SARPATH="$DIR/$SARFILE"

	# run sar in the background and redirect all output to /dev/null
	nohup sar -o "$SARPATH" $INTERVAL $SAMPLES >/dev/null 2>&1 3>&1 &
	SAR_PID=$!
	if ps -p $SAR_PID > /dev/null ; then
		printf "${GREEN}SUCCESS${RST}: Started background process $SAR_PID\n"
		echo "This process will run for $SECONDS seconds"
		echo "View this process with 'ps aux | grep $SAR_PID'"
		echo "Kill this process earlier with 'kill $SAR_PID'"
		printf "Results can be found at ${YELLOW}$SARPATH${RST}\n"
		echo "When finished, uninstall the software with '$0 --remove'"
	else
		printf "${RED}ERROR${RST}: Problem starting sar process.\n"
	fi

	# Here for reference.. Make CSV files from the binary data
	#sadf -d $SARFILE -- -dp     > sar-dp.csv     # storage
	#sadf -d $SARFILE -- -m TEMP > sar-mtemp.csv  # temperature
	#sadf -d $SARFILE -- -n DEV  > sar-ndev.csv   # network
	#sadf -d $SARFILE -- -r      > sar-r.csv      # memory
	#sadf -d $SARFILE -- -u ALL  > sar-uall.csv   # cpu
else
	echo "Skipped sar section"
fi

echo "Good-bye"
