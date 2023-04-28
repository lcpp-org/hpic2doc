
Building hpic2 on Ubuntu from source
=====================================

Developers should build hPIC2 from source so that they can
make changes, compile, and test locally.
We have found that it is easiest to install dependencies via Spack,
then manually run ``cmake`` to set up the hPIC2 build.

It is highly recommended installing all the dependencies of 
hPIC2 via Spack, even if you already have some of them installed
on your system. This will ensure that the correct versions are used.
Before installing hPIC2 from source, set up Spack and the dependencies 
as follows.

.. Follow the instructions for
.. :ref:`build_on_ubuntu:Building hpic2 on Ubuntu via spack`
.. up until running ``spack install hpic2``,
.. in order to set up the Spack repo.

Setting up your Spack environment for hPIC2 dependencies
----------------------------------------------------------

Download the Spack repository 
(suggested location, your ``$HOME`` directory):

.. code-block:: bash

   git clone -c feature.manyFiles=true https://github.com/spack/spack.git


Source the spack environment:

.. code-block:: bash

   source $HOME/spack/share/spack/setup-env.sh

.. note:: 
   
   Since the source step is needed every time, 
   we suggest to add the source command to your ``.bashrc`` file
   to avoid forgetting to re-tyoe it every time you open a new terminal.

   .. code-block:: bash

      echo "source $HOME/spack/share/spack/setup-env.sh" >> ~/.bashrc


make a new spack repository for hpic2,

.. code-block:: bash

   spack repo create hpic2_dev


register a Spack repository for hpic2,

.. code-block:: bash

   spack repo add hpic2_dev


change to the spack repository ``packages`` directory,

.. code-block:: bash

   cd /hpic2_dev/packages


Download the hpic2 source with its submodules,

.. code-block:: bash

   git clone --recurse-submodules https://github.com/lcpp-org/hpic2.git


Optionally, download the rustbca source at the same location, 

.. code-block:: bash

   git clone https://github.com/lcpp-org/RustBCA.git


and rename it to ``rustbca``

.. code-block::

   mv RustBCA rustbca



Building hPIC2 with OpenMP
---------------------------

Create and enter a spack env

.. code-block:: bash

   spack env create hpic2_omp_opt
   spack env activate hpic2_omp_opt

Add dependencies to spack env

.. code-block:: bash

   spack add googletest
   spack add hypre+openmp
   spack add kokkos~cuda+openmp
   spack add mfem~cuda+openmp~zlib
   spack add mpi
   spack add rustbca
   spack add spdlog

and install them

.. code-block:: bash

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

.. note:: 
   
   Note that when you open a fresh terminal, you must ``spacktivate``
   the Spack env or source the configure script again before you can ``make``.
