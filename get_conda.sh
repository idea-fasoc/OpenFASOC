#!/bin/bash 

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

# install miniconda3
if ! [ -x /home/$(logname)/miniconda3 ]
then
      wget https://repo.anaconda.com/miniconda/Miniconda3-py37_23.1.0-1-Linux-x86_64.sh \
    && bash Miniconda3-py37_23.1.0-1-Linux-x86_64.sh -b -p /home/$(logname)/miniconda3/ \
    && rm -f Miniconda3-py37_23.1.0-1-Linux-x86_64.sh
else
    echo "[OpenFASoC] Found miniconda3. Continuing the installation...\n"
fi

if [ $? == 0 ] && [ -x /home/$(logname)/miniconda3/ ]
then
        echo "[OpenFASoC] miniconda3 installed successfully. Continuing the installation...\n"
        if ! grep -q "/home/$(logname)/miniconda3/bin" /home/$(logname)/.bashrc || ! echo "$PATH" | grep -q "/home/$(logname)/miniconda3/bin"; then
                echo "" >> /home/$(logname)/.bashrc
                echo 'export PATH="/home/$(logname)/miniconda3/bin:$PATH"' >> /home/$(logname)/.bashrc
                echo "[OpenFASoC] miniconda3 added to PATH"
        fi
	export PATH=/home/$(logname)/miniconda3/bin:$PATH
else
	echo "[OpenFASoC] Failed to install miniconda. Check above for error messages."
	exit
fi
