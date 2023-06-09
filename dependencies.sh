#!/bin/bash


if ! [ -x /usr/bin/miniconda3 ]
then
      wget https://repo.anaconda.com/miniconda/Miniconda3-py37_23.1.0-1-Linux-x86_64.sh \
    && bash Miniconda3-py37_23.1.0-1-Linux-x86_64.sh -b -p /usr/bin/miniconda3/ \
    && rm -f Miniconda3-py37_23.1.0-1-Linux-x86_64.sh
else
    echo "[OpenFASoC] Found miniconda3. Continuing the installation...\n"
fi

if [ $? == 0 ] && [ -x /usr/bin/miniconda3/ ]
then
        echo "[OpenFASoC] miniconda3 installed successfully. Continuing the installation..."
	export PATH=/usr/bin/miniconda3/bin:$PATH
	conda update -y conda

        if [ $? == 0 ];then conda install -c litex-hub --file conda_versions.txt -y ; else echo "[OpenFASoC] Failed to update conda version." ; exit ; fi
        if [ $? == 0 ];then echo "[OpenFASoC] Installed OpenROAD, Yosys, Skywater PDK, Magic and Netgen successfully" ; else echo "[OpenFASoC] Failed to install conda packages" ; exit ; fi
else
	echo "[OpenFASoC] Failed to install miniconda. Check above for error messages."
	exit
fi

if cat /etc/os-release | grep "ubuntu" >> /dev/null
then
	apt install bison flex libx11-dev libx11-6 libxaw7-dev libreadline6-dev autoconf libtool automake -y
	git clone http://git.code.sf.net/p/ngspice/ngspice
	cd ngspice && ./compile_linux.sh

        if [ $? == 0 ]
        then
                echo "[OpenFASoC] Ngspice is installed. Checking pending. Continuing the installation..."
                cd ../
                echo "[OpenFASoC] Installing necessary python packages"
                pip3 install -r requirements.txt
        else
                echo "[OpenFASoC] Failed to install Ngspice"
                exit
        fi

        if [ $? == 0 ]
        then
                export DEBIAN_FRONTEND=noninteractive
                cd docker/conda/scripts
                ./xyce_install.sh
        else
                echo "[OpenFASoC] Failed to install python packages successfully"
        fi

        if [ $? == 0 ]
        then
                echo "[OpenFASoC] Xyce is installed. Checking pending. Continuing the installation...\n"
        else
                echo "[OpenFASoC] Failed to install Xyce"
                exit
        fi
else
        echo "[OpenFASoC] Ngspice, Xyce simulators are not installed"
        sed -i 's/gdsfactory==5.1.1/#gdsfactory==5.1.1/g' requirements.txt
        sed -i 's/ltspice/#ltspice/g' requirements.txt
        pip3 install -r requirements.txt

        if [ $? == 0 ]
        then
                echo "[OpenFASoC] Installed python packages except 'ltspice and gdsfactory'. You need to install GCC packages first and then install both these packages"
        else
                echo "[OpenFASoC] Failed to install python packages successfully"
        fi


if cat /etc/os-release | grep "ubuntu" >> /dev/null
then
	apt install qt5-default qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3-dev libz-dev build-essential -y
	wget https://www.klayout.org/downloads/Ubuntu-20/klayout_0.28.6-1_amd64.deb
	dpkg -i klayout_0.28.6-1_amd64.deb
	apt install time -y
	strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5 #https://stackoverflow.com/questions/63627955/cant-load-shared-library-libqt5core-so-5
elif cat /etc/os-release | grep -e "centos" >> /dev/null
then
	yum group install "Development Tools" -y
	yum install qtbase5-dev qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3-dev libz-dev qt-x11 -y
	wget https://www.klayout.org/downloads/CentOS_7/klayout-0.28.6-1.x86_64.rpm
	rpm -i klayout-0.28.6-1.x86_64.rpm
	yum install time -y
elif cat /etc/os-release | grep -e "el7" -e "el8" >> /dev/null
then
	echo "[OpenFASoC] Please install Klayout manually if not installed already. This script can't support KLayout installations on RHEL distribution yet"
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

export PATH=/usr/bin/miniconda3/:$PATH

if [ -x /usr/bin/miniconda3/share/pdk/ ]
then
 export PDK_ROOT=/usr/bin/miniconda3/share/pdk/
 echo "[OpenFASoC] PDK_ROOT is set to /usr/bin/miniconda3/share/pdk/. If this variable is empty, try setting PDK_ROOT variable to /usr/bin/miniconda3/share/pdk/"
else
 echo "[OpenFASoC] PDK not installed"
fi
echo "[OpenFASoC] "
echo "[OpenFASoC] "
echo "[OpenFASoC] To access the installed binaries, please run this command or add this to your .bashrc file - export PATH=/usr/bin/miniconda3/bin:\$PATH"
echo "[OpenFASoC] To access xyce binary, create an alias - xyce='/opt/xyce/xyce_serial/bin/Xyce'"

echo "[OpenFASoC] ################################"
echo "[OpenFASoC] Installation completed"
echo "[OpenFASoC] Thanks for using OpenFASOC dependencies script. To submit feedback, feel free to open a github issue on OpenFASOC repo"
echo "[OpenFASoC] To know more about generators, go to openfasoc.readthedocs.io"
echo "[OpenFASoC] ################################"
