FROM ubuntu:20.04

RUN apt-get -y update
RUN apt-get -y upgrade
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install wget bison flex libx11-dev libx11-6 libxaw7-dev libreadline6-dev autoconf libtool automake git -y

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.12.0-Linux-x86_64.sh \
    && bash Miniconda3-py37_4.12.0-Linux-x86_64.sh -b -p /usr/bin/miniconda3/ \
    && rm -f Miniconda3-py37_4.12.0-Linux-x86_64.sh

ENV PATH=/usr/bin/miniconda3/bin/:${PATH}
RUN conda update -y conda
RUN conda install -c litex-hub yosys open_pdks.sky130a magic netgen -y
RUN conda install -c litex-hub openroad -y
RUN openroad -version


RUN apt install qt5-default qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev -y
RUN apt install ruby ruby-dev -y
RUN apt install python3-dev -y
RUN apt install libz-dev -y
RUN apt install build-essential -y

RUN wget https://www.klayout.org/downloads/Ubuntu-20/klayout_0.28.2-1_amd64.deb 
RUN dpkg -i klayout_0.28.2-1_amd64.deb
RUN apt install time -y
ENV PDK_ROOT=/usr/bin/miniconda3/share/pdk/
RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

RUN git clone http://git.code.sf.net/p/ngspice/ngspice
RUN cd ngspice && ./compile_linux.sh

COPY ./scripts /scripts
