
Building hpic2 on Ubuntu from source
=====================================

Developers should build hPIC2 from source so that they can
make changes, compile, and test locally.
We have found that it is easiest to install dependencies via Spack,
then manually run ``cmake`` to set up the hPIC2 build.

Follow the instructions for
:ref:`build_on_ubuntu:Building hpic2 on Ubuntu via spack`
up until running ``spack install hpic2``,
in order to set up the Spack repo.

Building hPIC2 with OpenMP
---------------------------

Create and enter a spack env

.. code-block:: bash

   spack env create hpic2_omp_opt
   spack env activate hpic2_omp_opt

Add dependencies to spack env and install them

.. code-block:: bash

   spack add googletest
   spack add hypre+openmp
   spack add kokkos~cuda+openmp
   spack add mfem~cuda+openmp~zlib
   spack add mpi
   spack add rustbca
   spack add spdlog
   spack install

Create a build directory

.. code-block:: bash

   mkdir ~/hpic2_dev/hpic2_omp_opt

Create a CMake script to configure the build

.. code-block:: bash

   cat > ~/hpic2_dev/hpic2_omp_opt.sh << 'EOF'
   spacktivate hpic2_omp_opt
   cmake -DCMAKE_BUILD_TYPE=Release -DWITH_MFEM=ON -DWITH_TESTS=ON -DWITH_RUSTBCA=ON ~/hpic2_dev/hpic2
   EOF

Source the configure script from the build directory

.. code-block:: bash

   cd ~/hpic2_dev/hpic2_omp_opt
   . ../hpic2_omp_opt.sh

Compile

.. code-block:: bash

   make

When you make changes to the source code in ``~/hpic2_dev/hpic2``,
you need only run ``make`` from the build directory again to recompile.
Note that when you open a fresh terminal, you must ``spacktivate``
the Spack env or source the configure script again before you can ``make``.

Building hPIC2 with CUDA
---------------------------

Look up your GPU on the
`CUDA GPUs website <https://developer.nvidia.com/cuda-gpus>`_.
Remove the decimal from its Compute Capability,
so that 3.7 becomes 37, for example.
Store this temporarily as an environment variable

.. code-block:: bash

   export MY_CC = <compute capability without decimal>

Create and enter a spack env

.. code-block:: bash

   spack env create hpic2_cuda_opt
   spack env activate hpic2_cuda_opt

Add dependencies to spack env and install them

.. code-block:: bash

   spack add googletest
   spack add hypre+openmp+cuda cuda_arch=$MY_CC
   spack add kokkos+cuda+cuda_lambda+openmp+wrapper cuda_arch=$MY_CC
   spack add mfem+cuda+openmp~zlib cuda_arch=$MY_CC
   spack add openmpi +cuda cuda_arch=$MY_CC
   spack add rustbca
   spack add spdlog
   spack install

Create a build directory

.. code-block:: bash

   mkdir ~/hpic2_dev/hpic2_cuda_opt

Create a CMake script to configure the build

.. code-block:: bash

   cat > ~/hpic2_dev/hpic2_cuda_opt.sh << 'EOF'
   spacktivate hpic2_cuda_opt
   cmake -DCMAKE_BUILD_TYPE=Release -DWITH_MFEM=ON -DWITH_TESTS=ON -DWITH_RUSTBCA=ON ~/hpic2_dev/hpic2
   EOF

Source the configure script from the build directory

.. code-block:: bash

   cd ~/hpic2_dev/hpic2_cuda_opt
   . ../hpic2_cuda_opt.sh

Compile

.. code-block:: bash

   make

When you make changes to the source code in ``~/hpic2_dev/hpic2``,
you need only run ``make`` from the build directory again to recompile.
Note that when you open a fresh terminal, you must ``spacktivate``
the Spack env or source the configure script again before you can ``make``.
