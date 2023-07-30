FROM ubuntu:20.04

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y wget autoconf libtool automake g++ qt5-default qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3-dev libz-dev build-essential time git && \
    apt-get clean

ENV DEBIAN_FRONTEND=noninteractive

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py37_23.1.0-1-Linux-x86_64.sh && \
    bash Miniconda3-py37_23.1.0-1-Linux-x86_64.sh -b -p /usr/bin/miniconda3/ && \
    rm -f Miniconda3-py37_23.1.0-1-Linux-x86_64.sh

ENV PATH=/usr/bin/miniconda3/bin:${PATH}
RUN conda update -y conda && \
    conda install -y -c litex-hub yosys open_pdks.sky130a magic netgen openroad ngspice

RUN wget https://www.klayout.org/downloads/Ubuntu-20/klayout_0.28.6-1_amd64.deb && \
    dpkg -i klayout_0.28.6-1_amd64.deb && \
    rm -f klayout_0.28.6-1_amd64.deb

ENV PDK_ROOT=/usr/bin/miniconda3/share/pdk/
RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

COPY ./scripts /scripts
