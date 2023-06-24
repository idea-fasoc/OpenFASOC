#!/bin/sh
# https://github.com/Xyce/Xyce/discussions/4#discussioncomment-169255

###########################################################################
# References:
#
# https://xyce.sandia.gov/documentation/BuildingGuide.html
# https://github.com/Xyce/Xyce
#
###########################################################################

###########################################################################
#Install Dependancies
###########################################################################

yum install -y wget git make gcc-c++ python3
yum install -y gcc-gfortran bison flex libtool-ltdl-devel
yum install -y fftw-devel suitesparse-devel blas-devel lapack-devel
yum install -y openmpi-devel openmpi
yum install -y cmake
yum install -y lapack-devel
yum install -y lapack
yum install -y bison
yum install -y flex
yum install -y blas
yum install -y fftw
yum install -y fftw-devel
yum install -y suitesparse-devel
yum install -y suitesparse
yum install -y autoconf
yum install -y automake
yum install -y libtool
yum install -y openmpi
yum install -y openmpi-devel

# gcc v7 necessary for successful build of Xyce
yum install -y centos-release-scl
yum install -y devtoolset-8
source /opt/rh/devtoolset-8/enable

###########################################################################
#Install Trilinos from source
###########################################################################

wget https://github.com/trilinos/Trilinos/archive/trilinos-release-12-12-1.tar.gz
tar zxvf trilinos-release-12-12-1.tar.gz

SRCDIR=$PWD/Trilinos-trilinos-release-12-12-1
LIBDIR=/opt/xyce/xyce_lib
INSTALLDIR=/opt/xyce/xyce_serial
FLAGS="-O3 -fPIC"

cmake \
-G "Unix Makefiles" \
-DCMAKE_C_COMPILER=gcc \
-DCMAKE_CXX_COMPILER=g++ \
-DCMAKE_Fortran_COMPILER=gfortran \
-DCMAKE_CXX_FLAGS="$FLAGS" \
-DCMAKE_C_FLAGS="$FLAGS" \
-DCMAKE_Fortran_FLAGS="$FLAGS" \
-DCMAKE_INSTALL_PREFIX=$LIBDIR \
-DCMAKE_MAKE_PROGRAM="make" \
-DTrilinos_ENABLE_NOX=ON \
-DNOX_ENABLE_LOCA=ON \
-DTrilinos_ENABLE_EpetraExt=ON \
-DEpetraExt_BUILD_BTF=ON \
-DEpetraExt_BUILD_EXPERIMENTAL=ON \
-DEpetraExt_BUILD_GRAPH_REORDERINGS=ON \
-DTrilinos_ENABLE_TrilinosCouplings=ON \
-DTrilinos_ENABLE_Ifpack=ON \
-DTrilinos_ENABLE_Isorropia=ON \
-DTrilinos_ENABLE_AztecOO=ON \
-DTrilinos_ENABLE_Belos=ON \
-DTrilinos_ENABLE_Teuchos=ON \
-DTeuchos_ENABLE_COMPLEX=ON \
-DTrilinos_ENABLE_Amesos=ON \
-DAmesos_ENABLE_KLU=ON \
-DTrilinos_ENABLE_Sacado=ON \
-DTrilinos_ENABLE_Kokkos=OFF \
-DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES=OFF \
-DTrilinos_ENABLE_CXX11=ON \
-DTPL_ENABLE_AMD=ON \
-DAMD_LIBRARY_DIRS="/usr/lib" \
-DTPL_AMD_INCLUDE_DIRS="/usr/include/suitesparse" \
-DTPL_ENABLE_BLAS=ON \
-DTPL_ENABLE_LAPACK=ON \
$SRCDIR

make

mkdir -p $LIBDIR
make install

###########################################################################
#Install Xyce from Source
###########################################################################

#Clone Xyce
git clone https://github.com/Xyce/Xyce.git

#Build Xyce
cd Xyce
./bootstrap
./configure CXXFLAGS="-O3 -std=c++11" ARCHDIR=$LIBDIR --prefix=$INSTALLDIR CPPFLAGS="-I/usr/include/suitesparse"
make
mkdir -p $INSTALLDIR
make install

#Test installation
$INSTALLDIR/bin/Xyce
