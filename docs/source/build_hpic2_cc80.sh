module load cmake
module load hdf5

# install hypre
# TODO build cuda-aware hypre
mkdir hypre_dev && cd hypre_dev
git clone git@github.com:hypre-space/hypre.git
cd hypre/src
./configure
make -j64
make install
cd ../../..

# install spdlog
git clone --branch v1.11.0 git@github.com:gabime/spdlog.git
cd spdlog && mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install && make -j64
make install
cd ../..

# install kokkos
mkdir Kokkos && cd Kokkos
git clone git@github.com:kokkos/kokkos.git
mkdir cuda_opt_cc80 && cd cuda_opt_cc80
cmake ../kokkos \
-DKokkos_ENABLE_CUDA=ON \
-DKokkos_ENABLE_OPENMP=ON \
-DKokkos_ENABLE_SERIAL=ON \
-DKokkos_ENABLE_COMPILER_WARNINGS=ON \
-DKokkos_ENABLE_CUDA_LAMBDA=ON \
-DKokkos_ARCH_ZEN3=ON \
-DKokkos_ARCH_AMPERE80=ON \
-DCMAKE_INSTALL_PREFIX=install
make -j64
make install
cd ../..

# install metis 5
wget http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz
tar -xvf metis-5.1.0.tar.gz
cd metis-5.1.0
make config prefix=install
make -j64
make install
cd ..

# install mfem
mkdir mfem_dev && cd mfem_dev
git clone git@github.com:mfem/mfem.git
mkdir cuda_opt_cc80 && cd cuda_opt_cc80
cmake ../mfem -DMFEM_USE_CUDA=YES -DMFEM_USE_MPI=YES -DCUDA_ARCH=sm_80 -DMETIS_DIR=../../metis-5.1.0/build/Linux-x86_64/install -DHYPRE_DIR=../../hypre_dev/hypre/src/hypre -DCMAKE_INSTALL_PREFIX=install
make -j64
make install
cd ../..

# install pumimbbl
mkdir pumiMBBL_dev && cd pumiMBBL_dev
git clone git@github.com:SCOREC/pumiMBBL.git
mkdir cuda_opt_cc80 && cd cuda_opt_cc80
cmake ../pumiMBBL \
-DCMAKE_INSTALL_PREFIX=install \
-DKokkos_ROOT=../../Kokkos/cuda_opt_cc80/install
make -j64
make install
cd ../..

# install rustbca (must have installed rustup by this point)
git clone git@github.com:lcpp-org/RustBCA.git
cd RustBCA
cargo build --release --lib
mkdir include && cd include
ln -s ../RustBCA.h .
cd ..
mkdir lib && cd lib
ln -s ../target/release/liblibRustBCA.so .
cd ../..

# install hpic2
mkdir hpic2_dev && cd hpic2_dev
git clone --recurse-submodules git@github.com:lcpp-org/hpic2.git
mkdir cuda_opt_cc80 && cd cuda_opt_cc80
cmake ../hpic2 \
-DKokkos_ROOT=../../Kokkos/cuda_opt_cc80/install \
-DHYPREROOT=../../hypre_dev/hypre/src/hypre \
-Dspdlog_DIR=../../spdlog/install/lib64/cmake/spdlog \
-DWITH_PUMIMBBL=ON \
-DWITH_MFEM=ON \
-DWITH_RUSTBCA=ON \
-DRUSTBCA_ROOT=../../RustBCA \
-DMFEM_ROOT=../../mfem_dev/cuda_opt_cc80/install \
-DPUMIMBBL_ROOT=../../pumiMBBL_dev/cuda_opt_cc80/install \
-DMETIS_ROOT=../../metis-5.1.0/build/Linux-x86_64/install
make -j64

