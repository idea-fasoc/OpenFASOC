FROM ubuntu:22.04

RUN apt-get -y update
RUN apt-get -y upgrade
ENV DEBIAN_FRONTEND=noninteractive
COPY ./packages.txt .
RUN xargs apt-get install -y < packages.txt

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash ./Miniconda3-latest-Linux-x86_64.sh -b -p /usr/bin/miniconda3 \
    && rm ./Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/usr/bin/miniconda3/bin:${PATH}
RUN conda update conda --all -y
RUN conda install python=3.11 \
                   open_pdks.sky130a \
                   open_pdks.gf180mcuC \
                   magic \
                   netgen \
                   openroad \
                   -c litex-hub \
                   -c conda-forge \
                   -c anaconda \
                   -y
ENV PDK_ROOT=/usr/bin/miniconda3/share/pdk/

RUN wget https://www.klayout.org/downloads/Ubuntu-22/klayout_0.28.17-1_amd64.deb
RUN dpkg -i klayout_0.28.17-1_amd64.deb
RUN pip install glayout==0.0.9
RUN pip install --force-reinstall numpy==1.24
#RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

COPY ./scripts /scripts

RUN git clone http://git.code.sf.net/p/ngspice/ngspice && \
    cd ngspice && \
    ./compile_linux.sh
