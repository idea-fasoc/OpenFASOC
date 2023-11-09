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

apt-get install wget git build-essential make python3 -y
apt-get install gfortran bison flex libfl-dev libtool -y
apt-get install libfftw3-dev libsuitesparse-dev libblas-dev liblapack-dev -y
apt-get install libopenmpi-dev openmpi-bin -y

wget -qO /etc/apt/trusted.gpg.d/kitware-key.asc https://apt.kitware.com/keys/kitware-archive-latest.asc
currentver="$(lsb_release -rs)"
requiredver="22.04"

if [ $currentver == $requiredver ]
then 
	echo "deb https://apt.kitware.com/ubuntu/ jammy main" | tee /etc/apt/sources.list.d/kitware.list
else 
	echo "deb https://apt.kitware.com/ubuntu/ focal main" | tee /etc/apt/sources.list.d/kitware.list
fi
apt install -y cmake

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
