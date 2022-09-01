#/bin/bash

ma_ver=$(python -c"import sys; print(str(sys.version_info.major))")
mi_ver=$(python -c"import sys; print(str(sys.version_info.minor))")

if [[ "$ma_ver" -lt 3 ]]
then
    echo "[Warning] python version less than 3.* . Not compatible. You atleast need version above or equal to 3.7."
    sed -i 's/gdsfactory==5.1.1/#gdsfactory==5.1.1/g' requirements.txt
    echo "[Warning] Skipping installing the gdsfactory python package because of that error. Continuing installation..."
elif [[ "$mi_ver" -lt 6 ]]
then
    echo "[Warning] python version less than 3.6 . Not compatible. You atleast need version above or equal to 3.7."
    sed -i 's/gdsfactory==5.1.1/#gdsfactory==5.1.1/g' requirements.txt
    echo "[Warning] Skipping installing the gdsfactory python package because of that error. Continuing installation..."
else
    echo "Compatible python version exists: $ma_ver . $mi_ver"
fi


if which pip3 >> /dev/null
then
        echo "Pip3 exists"
        pip3 install -r requirements.txt

else
        if cat /etc/os-release | grep "ubuntu" >> /dev/null
        then
                echo "Ubuntu"
                apt install python3-pip -y
                if [ $? == 0 ]
                then
                       pip3 install -r requirements.txt
                       apt install wget -y
                else
                        echo "Pip3 installation failed.. exiting"
                        exit
                fi

        elif cat /etc/os-release | grep -e "centos" -e "el7" -e "el8" >> /dev/null
        then
                echo "Centos"
                yum install python3-pip -y
                if [ $? == 0 ]
                then
                       pip3 install -r requirements.txt
		       yum install wget -y
                else
                        echo "Pip3 installation failed.. exiting"
                        exit
                fi
        else
                echo "This script is not compatabile with your Linux Distribution"
		exit
        fi
fi

if [ $? == 0 ]
then
 echo "Python packages installed successfully. Continuing the installation...\n"
if ! [ -x /usr/bin/miniconda3 ]
then
      wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.12.0-Linux-x86_64.sh \
    && bash Miniconda3-py37_4.12.0-Linux-x86_64.sh -b -p /usr/bin/miniconda3/ \
    && rm -f Miniconda3-py37_4.12.0-Linux-x86_64.sh
else
    echo "Found miniconda3. Continuing the installation...\n"
fi
else
	echo "Failed to install python packages. Check above for error messages."
	exit
fi


if [ $? == 0 ] && [ -x /usr/bin/miniconda3 ]
then
        echo "miniconda3 installed successfully. Continuing the installation...\n"
	export PATH=/usr/bin/miniconda3/bin:$PATH
	conda update -y conda
        if [ $? == 0 ];then conda install -c litex-hub yosys open_pdks.sky130a magic netgen -y ; else echo "Failed to update conda" ; fi
        if [ $? == 0 ];then conda install -c litex-hub openroad -y ; else echo "Failed to install conda packages" ; fi
        conda install -c conda-forge ngspice -y
else
	echo "Failed to install miniconda. Check above for error messages."
	exit
fi

if [ $? == 0 ]
then
 echo "Magic, Netgen, OpenROAD, Yosys, Ngspice are installed. Checking pending. Continuing the installation...\n"
else
 echo "Failed to install Magic, Netgen, OpenROAD, Yosys, Ngspice"
 exit
fi

if cat /etc/os-release | grep "ubuntu" >> /dev/null
then
	apt install qt5-default qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3-dev libz-dev build-essential -y
	wget https://www.klayout.org/downloads/Ubuntu-20/klayout_0.27.10-1_amd64.deb
	dpkg -i klayout_0.27.10-1_amd64.deb
	apt install time -y
	strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5
elif cat /etc/os-release | grep -e "centos" >> /dev/null
then
	yum group install "Development Tools" -y
	yum install qtbase5-dev qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3-dev libz-dev qt-x11 -y
	wget https://www.klayout.org/downloads/CentOS_7/klayout-0.27.10-0.x86_64.rpm
	rpm -i klayout-0.27.10-0.x86_64.rpm
	yum install time -y
elif cat /etc/os-release | grep -e "el7" -e "el8" >> /dev/null
then
	echo "Please install Klayout manually if not installed already. This script can't support KLayout installations on RHEL distribution yet"
else
	echo "Cannot install klayout for other linux distrbutions via this script"
fi

if [ $? == 0 ]
then
 echo "Installed Klayout successfully. Checking pending..."
else
 echo "Failed to install Klayout successfully"
 exit
fi

export PATH=/usr/bin/miniconda3/bin:$PATH

if [ -x /usr/bin/miniconda3/share/pdk/ ]
then
 export PDK_ROOT=/usr/bin/miniconda3/share/pdk/
 echo "PDK_ROOT is set to /usr/bin/miniconda3/share/pdk/"
else
 echo "PDK not installed"
fi

echo "To access the installed binaries, please run this command - export PATH=/usr/bin/miniconda3/bin:\$PATH"
