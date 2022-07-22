FROM ubuntu:20.04
RUN apt-get -y update && apt-get -y upgrade

# For Magic
RUN apt install python3 m4 libx11-dev gcc mesa-common-dev libglu1-mesa-dev csh git -y
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -q -y install tcl-dev tk-dev

RUN git clone git://opencircuitdesign.com/magic && \
    cd magic && ./configure && make && make install

# For Netgen
RUN git clone git://opencircuitdesign.com/netgen && \
    cd netgen && ./configure && make && make install

# For OpenROAD app
RUN git clone --recursive https://github.com/The-OpenROAD-Project/OpenROAD.git && \
    cd OpenROAD && ./etc/DependencyInstaller.sh -dev && ./etc/Build.sh && \
    cp ./build/src/openroad /usr/bin/.

# For skywater-pdk
RUN mkdir /pdks && git clone https://github.com/google/skywater-pdk && cd skywater-pdk && \
    git submodule init libraries/sky130_fd_io/latest && \
    git submodule init libraries/sky130_fd_pr/latest && \
    git submodule init libraries/sky130_fd_sc_hd/latest && \
    git submodule init libraries/sky130_fd_sc_hvl/latest && \
    git submodule update && make timing && cd ../

# For open_pdks
RUN git clone https://github.com/RTimothyEdwards/open_pdks.git && cd open_pdks && \
    ./configure --enable-sky130-pdk=/skywater-pdk --prefix=/pdks && \
    make && make install

ENV PDK_ROOT=/pdks/share/pdk/

# For yosys
RUN apt-get install clang -y && \
    git clone https://github.com/YosysHQ/yosys.git && \
    cd yosys && make config-clang && \
    make && make install

# For Klayout
RUN apt-get install klayout -y

# For OpenFASOC
RUN apt-get install time -y 
