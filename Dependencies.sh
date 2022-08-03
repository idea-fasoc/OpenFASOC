#/bin/bash

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

        elif cat /etc/os-release | grep "centos" >> /dev/null
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
      wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.12.0-Linux-x86_64.sh \
    && bash Miniconda3-py37_4.12.0-Linux-x86_64.sh -b -p /usr/bin/miniconda3/ \
    && rm -f Miniconda3-py37_4.12.0-Linux-x86_64.sh
else
	echo "Failed to install conda"
	exit
fi


if [ $? == 0 ] && [ -x /usr/bin/miniconda3 ]
then
	export PATH=/usr/bin/miniconda3/bin:$PATH
	conda update -y conda
        if [ $? == 0 ];then conda install -c litex-hub yosys open_pdks.sky130a magic netgen -y ; else echo "Failed to install conda packages" ; fi
        if [ $? == 0 ];then conda install -c litex-hub openroad -y ; else echo "Failed to install openroad conda package" ; fi
else
	echo "Failed to install conda packages"
	exit
fi

if cat /etc/os-release | grep "ubuntu" >> /dev/null
then

	apt install qt5-default qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3-dev libz-dev build-essential -y
	wget https://www.klayout.org/downloads/Ubuntu-20/klayout_0.27.10-1_amd64.deb
	dpkg -i klayout_0.27.10-1_amd64.deb
	apt install time -y
	strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5
elif cat /etc/os-release | grep "centos" >> /dev/null
then
	yum group install "Development Tools" -y
	yum install qtbase5-dev qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3-dev libz-dev qt-x11 -y
	wget https://www.klayout.org/downloads/CentOS_7/klayout-0.27.10-0.x86_64.rpm
	rpm -i klayout-0.27.10-0.x86_64.rpm
	yum install time -y
else
	echo "Cannot install klayout for other linux distrbutions via this script"
fi

export PDK_ROOT=/usr/bin/miniconda3/share/pdk/
