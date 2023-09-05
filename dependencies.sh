#!/bin/bash 

printf "Function: \nIf this script runs smoothly, all necessary dependencies for OpenFASoC will be 
downloaded at once. If you've already downloaded all dependencies with this script, 
you can run this script again to update the installed dependencies.\n
Basic Requirements (not exhaustive): 
(1) Python 3.6 or higher is required.
(2) Intel x86 architecture is required, as this script will use Conda to download several
Python packages for which versions compatible with ARM architecture currently do not
exist for installation in Conda's package repository. If your machine does not run 
on Intel x86 architecture, this script will likely not work.
(3) CentOS and Ubuntu are the only operating systems this script has been verified to work on.
We cannot guarantee successful compilation on other systems.\n\n"

proceed_confirmed=false
update_confirmed=false
while ! $proceed_confirmed
do
        echo "[OpenFASoC] Do you wish to proceed with the installation? 
[y] Yes. Install for the first time.
[u] Yes. Update already-installed dependencies.
[n] No. Exit this script." 
        read -p "Select the desired option: " selection
        if [ "$selection" == "y" ] || [ "$selection" == "Y" ]; then 
        echo "Beginning installation..."; proceed_confirmed=true
        elif [ "$selection" == "n" ] || [ "$selection" == "N" ]; then
        echo "Quitting script."; exit
        elif [ "$selection" == "u" ] || [ "$selection" == "U" ]; then
        update_confirmed=true
        proceed_confirmed=true
        else
        echo "[OpenFASoC] Invalid selection. Choose y or n."
        fi
done

if $update_confirmed; then
        if ! [ -x /home/$(logname)/miniconda3 ]; then
                echo "[OpenFASoC] Conda could not be found. If you have not yet successfully installed the dependencies, you cannot update the dependencies."
                exit
        fi
        export PATH=/home/$(logname)/miniconda3/bin:$PATH

        printf "\n[OpenFASoC] Attempting to update Conda using: conda update conda -y \n\n"
        conda update conda -y
        if [ $? == 0 ]
        then
        printf "\n\n[OpenFASoC] Conda updated successfully with: conda update conda -y."
        else 
        printf "\n\n[OpenFASoC] Failed to update Conda using: conda update conda -y."
        printf "[OpenFASoC] Attempting instead to update Conda using: install -c anaconda conda -y"
        conda install -c anaconda conda -y; if [ $? == 0 ]; then 
        printf "\n\n[OpenFASoC] Conda updated successfully with: install -c anaconda conda -y"
        else
        printf "\n\n[OpenFASoC] Conda could not be updated."; fi
        fi

        update_successful=true
        printf "\n\n[OpenFASoC] Attempting to update packages using: conda update --all -y \n"
        conda update --all -y
        if [ $? == 0 ]; then 
        printf "[OpenFASoC] Packages updated successfully with: conda update --all -y"
        else 
        printf "\n\n[OpenFASoC] Failed to update packages using: conda update --all -y."
        printf "Attempting instead to install core packages individually..."
        conda install -c litex-hub magic -y; if [ $? != 0 ]; then update_successful=false; echo "magic could not be updated"; fi
        conda install -c litex-hub netgen -y; if [ $? != 0 ]; then update_successful=false; echo "netgen could not be updated"; fi
        conda install -c litex-hub open_pdks.sky130a -y; if [ $? != 0 ]; then update_successful=false; echo "open_pdks could not be updated"; fi
        conda install -c litex-hub openroad -y; if [ $? != 0 ]; then update_successful=false; echo "openroad could not be updated"; fi
        conda install -c litex-hub yosys -y; if [ $? != 0 ]; then update_successful=false; echo "yosys could not be updated"; fi
        fi

        # ngspice_updated=false
        # echo "Updating ngspice..."
        # cd ngspice
        # git pull
        # ./compile_linux.sh 
        # if [ $? == 0 ]; then
        # ngspice_updated=true
        # echo "ngspice updated successfully."
        # else 
        # echo "nspice could not be updated."
        # fi
        # cd ..
        
        # cd ./docker/conda/scripts/Xyce
        # echo "Updating xyce..."
        # SRCDIR=$PWD/Trilinos-trilinos-release-12-12-1
        # LIBDIR=/opt/xyce/xyce_lib
        # INSTALLDIR=/opt/xyce/xyce_serial
        # FLAGS="-O3 -fPIC"
        # if cat /etc/os-release | grep "centos" >> /dev/null
        # then
        #         yum install -y centos-release-scl
        #         yum install -y devtoolset-7
        #         scl enable devtoolset-7 bash
        # fi
        # git pull
        # ./bootstrap
        # ./configure CXXFLAGS="-O3 -std=c++11" ARCHDIR=$LIBDIR --prefix=$INSTALLDIR CPPFLAGS="-I/usr/include/suitesparse"
        # make
        # make install
        #         if [ $? == 0 ]; then
        # echo "xyce updated successfully."
        # else 
        # echo "xyce could not be updated."
        # fi

        # if [ $ngspice_updated ]; then
        # echo "nspice was successfully updated."
        # fi
        if [ $update_successful ]; then
        printf "\n\nMagic, netgen, open_pdks, openroad, and yosys updated successfully to latest releases possible given user's Python version (most recent releases if version >=3.8).\n"
        fi
        exit
fi


if which python3 >> /dev/null
then
	echo "Python3 exists. Continuing..."
else
	echo "Python3 could not be found. Please install python3 and try again. Exiting..."
	exit
fi

ma_ver=$(python3 -c"import sys; print(str(sys.version_info.major))")
mi_ver=$(python3 -c"import sys; print(str(sys.version_info.minor))")

if [ "$ma_ver" -lt 3 ]
then
    echo "[Warning] python version less than 3.* . Not compatible. You atleast need version above or equal to 3.7."
    sed -i 's/gdsfactory==5.1.1/#gdsfactory==5.1.1/g' requirements.txt
    echo "[Warning] Skipping installing the gdsfactory python package because of that error. Continuing installation..."
elif [ "$mi_ver" -lt 6 ]
then
    echo "[Warning] python version less than 3.6 . Not compatible. You atleast need version above or equal to 3.7."
    sed -i 's/gdsfactory==5.1.1/#gdsfactory==5.1.1/g' requirements.txt
    echo "[Warning] Skipping installing the gdsfactory python package because of that error. Continuing installation..."
else
    echo "Compatible python version exists: $ma_ver.$mi_ver"
fi


if cat /etc/os-release | grep "ubuntu" >> /dev/null; then

	apt-get update -y
        apt-get install -y autoconf libtool automake make g++ gcc

elif cat /etc/os-release | grep -e "centos" >> /dev/null; then

        yum update -y

        yum install -y autoconf libtool automake make gcc gcc-c++

fi


if cat /etc/os-release | grep "ubuntu" >> /dev/null
then
 apt install bison flex libx11-dev libx11-6 libxaw7-dev libreadline6-dev autoconf libtool automake -y
 git clone http://git.code.sf.net/p/ngspice/ngspice
 currentver="$(lsb_release -rs)"
 requiredver="22.04"
 if [ $currentver == $requiredver ]
 then
  cd ngspice
  sed -i -e 's/--with-readline=yes//g' compile_linux.sh
  ./compile_linux.sh
 else
  cd ngspice && ./compile_linux.sh
 fi
elif cat /etc/os-release | grep "centos" >> /dev/null
then
 sudo yum install bison flex libX11-devel libX11 libXaw-devel readline-devel autoconf libtool automake -y
 git clone http://git.code.sf.net/p/ngspice/ngspice
 cd ngspice && ./compile_linux.sh
fi

if [ $? == 0 ]
then
 echo "[OpenFASoC] Ngspice is installed. Checking pending. Continuing the installation...\n"
 cd ../
else
 echo "[OpenFASoC] Failed to install Ngspice"
 exit
fi

if cat /etc/os-release | grep "ubuntu" >> /dev/null
then
	export DEBIAN_FRONTEND=noninteractive
	cd docker/conda/scripts
	./xyce_install.sh
elif cat /etc/os-release | grep "centos" >> /dev/null
then
	cd docker/conda/scripts
        chmod +x xyce_install_centos.sh
	./xyce_install_centos.sh
fi

        if [ $? == 0 ]
        then
                echo "[OpenFASoC] Xyce is installed. Checking pending. Continuing the installation...\n"
        else
                echo "[OpenFASoC] Failed to install Xyce"
                exit
        fi

if cat /etc/os-release | grep "ubuntu" >> /dev/null
then
	currentver="$(lsb_release -rs)"
 	requiredver="22.04"
 	if [ $currentver == $requiredver ]
 	then
	 apt install qtbase5-dev qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3-dev libz-dev build-essential -y 
	 wget https://www.klayout.org/downloads/Ubuntu-22/klayout_0.28.8-1_amd64.deb
	 dpkg -i klayout_0.28.8-1_amd64.deb
	else 
	 apt install qt5-default qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3-dev libz-dev build-essential -y
	 wget https://www.klayout.org/downloads/Ubuntu-20/klayout_0.28.6-1_amd64.deb
	 dpkg -i klayout_0.28.6-1_amd64.deb
  	 strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5 #https://stackoverflow.com/questions/63627955/cant-load-shared-library-libqt5core-so-5
	fi
	apt install time -y
	elif cat /etc/os-release | grep -e "centos" >> /dev/null
then
	yum install qt5-qtbase-devel qt5-qttools-devel qt5-qtxmlpatterns-devel qt5-qtmultimedia-devel qt5-qtmultimedia-widgets-devel qt5-qtsvg-devel ruby ruby-devel python3-devel zlib-devel time -y
	wget https://www.klayout.org/downloads/CentOS_7/klayout-0.28.6-0.x86_64.rpm
	rpm -i klayout-0.28.6-0.x86_64.rpm
	yum install time -y
  strip --remove-section=.note.ABI-tag /usr/lib64/libQt5Core.so.5
else
	echo "[OpenFASoC] Cannot install klayout for other linux distrbutions via this script"
fi

if [ $? == 0 ]
then
 echo "[OpenFASoC] Installed Klayout successfully. Checking pending..."
else
 echo "[OpenFASoC] Failed to install Klayout successfully"
 exit
fi

export PATH=/home/$(logname)/miniconda3/:$PATH

if [ -x /home/$(logname)/miniconda3/share/pdk/ ]
then
        if ! grep -q "PDK_ROOT=/home/$(logname)/miniconda3/share/pdk/" /home/$(logname)/.bashrc; then
                echo "" >> /home/$(logname)/.bashrc
                echo 'export PDK_ROOT=/home/$(logname)/miniconda3/share/pdk/' >> /home/$(logname)/.bashrc
        fi
        export PDK_ROOT=/home/$(logname)/miniconda3/share/pdk/
        echo "[OpenFASoC] PDK_ROOT is set to /home/$(logname)/miniconda3/share/pdk/. If this variable is empty, try setting PDK_ROOT variable to /home/$(logname)/miniconda3/share/pdk/"
else
        echo "[OpenFASoC] PDK not installed"
fi
echo "[OpenFASoC] "
echo "[OpenFASoC] "
echo "[OpenFASoC] To access xyce binary, create an alias - xyce='/opt/xyce/xyce_serial/bin/Xyce'"

echo "################################"
echo "[OpenFASoC] Installation completed"
echo "[OpenFASoC] Thanks for using OpenFASOC dependencies script. To submit feedback, feel free to open a github issue on OpenFASOC repo"
echo "[OpenFASoC] To know more about generators, go to openfasoc.readthedocs.io"
echo "################################"
