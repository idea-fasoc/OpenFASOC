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
RUN conda install python=3.10 \
                    yosys \
                    open_pdks.sky130a \
                    magic \
                    netgen \
                    openroad \
                    ngspice \ 
                    -c litex-hub \
                    -c anaconda \
                    -y
ENV PDK_ROOT=/usr/bin/miniconda3/share/pdk/

RUN wget https://www.klayout.org/downloads/Ubuntu-22/klayout_0.28.12-1_amd64.deb
RUN dpkg -i klayout_0.28.12-1_amd64.deb
RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

COPY ./scripts /scripts
