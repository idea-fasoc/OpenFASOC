FROM ubuntu:20.04

RUN apt-get -y update
RUN apt-get -y upgrade
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y wget autoconf libtool automake g++
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py37_23.1.0-1-Linux-x86_64.sh \
    && bash Miniconda3-py37_23.1.0-1-Linux-x86_64.sh -b -p /usr/bin/miniconda3/ \
    && rm -f Miniconda3-py37_23.1.0-1-Linux-x86_64.sh

ENV PATH=/usr/bin/miniconda3/bin:${PATH}
RUN conda update -y conda
RUN conda install -y -c litex-hub yosys \
                                open_pdks.sky130a \
                                magic \
                                netgen \
                                openroad \
                                ngspice


RUN apt install qt5-default qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev -y
RUN apt install ruby ruby-dev -y
RUN apt install python3-dev -y
RUN apt install libz-dev -y
RUN apt install build-essential -y

RUN wget https://www.klayout.org/downloads/Ubuntu-20/klayout_0.28.6-1_amd64.deb
RUN dpkg -i klayout_0.28.6-1_amd64.deb
RUN apt install time git -y
ENV PDK_ROOT=/usr/bin/miniconda3/share/pdk/
RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

COPY ./scripts /scripts
