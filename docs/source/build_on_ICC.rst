
Building hpic2 on the Illinois Campus Cluster (ICC)
===================================================

The Illinois Campus Cluster (ICC) is a high-performance computing (HPC) 
cluster that is available to the students, faculty, and staff at the 
University of Illinois at Urbana-Champaign. The ICC is a shared resource, 
and users are expected to abide by the 
`ICC User Policy <https://campuscluster.illinois.edu/resources/docs/policies/>`_.

Step 1: Get an account on the ICC
---------------------------------

If you do not already have an account on the Illinois Campus Cluster, 
request access for Research here,


* `ICC Request Access for Research <https://campuscluster.illinois.edu/new_forms/user_form.php>`_

specifying to be added to the following group: ``dcurreli-npre-eng``

Read the ICC `resources <https://campuscluster.illinois.edu/resources/docs/>`_\ , such as: 


* `ICC Getting started <https://campuscluster.illinois.edu/resources/docs/start/>`_
* `ICC User Guide <https://campuscluster.illinois.edu/resources/docs/user-guide/>`_ 
* `ICC Storage and Data Guide <https://campuscluster.illinois.edu/resources/docs/storage-and-data-guide/>`_
* `ICC Training and Tutorials <https://campuscluster.illinois.edu/resources/training/>`_

Step 2: Connect to the ICC
--------------------------

The Campus Cluster can be accessed via Secure Shell (SSH) to the head nodes 
using your official University NetID login and password:

.. code-block:: bash

   ssh <yournetid>@cc-login.campuscluster.illinois.edu

Step 3: Check your login environment
------------------------------------

Once you login to the ICC, you normally land on a folder named after your NetID. 

.. code-block:: bash

   $ echo $HOME
   /home/<yournetid>

The login environment is set up to provide a minimal set of tools and libraries. 
The necessary modules have to be loaded to use the software. 
To see what is available:

.. code-block:: bash

   module avail

Step 4: Load the necessary modules
----------------------------------

In order to use the software, you need to load the necessary modules. 
Dependencies are hanldes via `spack <https://spack.io/>`_. 
A spack environment is provided in a shared folder of the campus cluster. 
To use it, you need to source the spack environment:

.. code-block:: bash

   source /home/dcurreli/lcpp/hpic2/spack/share/spack/setup-env.sh

Now the list of available modules should include also the hpic2 dependencies 
in the form ``hpic2deps/<desired-configuration>``\ , where ``<desired-configuration>`` 
is a combination of the libraries and compilers. For example, to use the GCC 
compiler and the MVAPICH2 MPI library, you can load the module 
``hpic2deps/gcc-7.2.0/mvapich2-2.3.5``. To see the list of available configurations, 
type:

.. code-block:: bash

   module avail

The output should now look like this:

.. code-block:: bash

   --------------------- /home/dcurreli/lcpp/hpic2/spack/share/spack/modules/linux-rhel7-sandybridge --------------------
   cuda/qcqjn52irigxuxymgaj2esjwrhzga2nd                                          kokkos/72z7t2rw7lpazlo5ewqjel7dip3gkdcz
   googletest/thxshjk2cy3djebhfarv567blmhazvs2                                    kokkos/7haeqcoi4d2ie32pdioe6gtvh2p7cw7j
   googletest/ul2hvjsx3qkgbzchjcoia2jrgfwxjbkg                                    kokkos/7ytomdkkwoxrwmvzutjhulfyh4w6ytzq
   hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=35/+debug   kokkos/bcvdiuc2smud5dlm3k5cvmxnjb45ehcr
   hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=35/~debug   kokkos/buqhmtbppfgjtwfd4g5vxew2qwqft7xm
   hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=37/+debug   kokkos/c7m6o26u2sn5wbzlihmdzfhg646hwzsv
   hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=37/~debug   kokkos/cp44r62ukspb4odkf4xwfmccwuwyhxlu
   hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=60/+debug   kokkos/ct3hf5rwhaj7npkir6gr3gkkk2oi255b
   hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=60/~debug   kokkos/dozyczjvmfu2vwcrcdgrdccd6okh6apw
   hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=70/+debug   kokkos/dphrrmtm5jyaxtvy4tnbhwf2xojltlwv
   hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=70/~debug   kokkos/eg5eigg7ttkdq34ednbbcda4edgsloj3
   ...
   ...
   etc.

Now you can load the desired modules, for example:

.. code-block:: bash

   module load cmake
   module load hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=70/~debug

A ``module list`` command should now show the loaded modules, for example:

.. code-block:: bash

   $ module list
   Currently Loaded Modulefiles:
     1) gcc/7.2.0                                           5) kokkos/mn3h6o774qymfi6iv5wiedwk7k7jlkyg
     2) cmake/3.18.4                                        6) openmpi/tpcwumes5rjhwpzkf3pvog5j2rdxxroh
     3) googletest/thxshjk2cy3djebhfarv567blmhazvs2         7) spdlog/yyst4bxqpyoiv4ktc7pmqnk2yvh5t3y5
     4) hypre/2olp2oaczn3zf4nzq47qlkiqhrr6l6ec              8) hpic2deps/gcc-7.2.0/openmpi-4.1.0/kokkos+openmp~pthread-cuda_arch=none/+debug

Which modules to load?
^^^^^^^^^^^^^^^^^^^^^^

In order to fully utilize the hybrid parallelism of hpic2 on the ICC, 
you need to load modules including either ``+openmp`` or ``+cuda`` in the name. 
For example, to use the OpenMP backend, you can load the module 
``hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=70/~debug``. 
To use the CUDA backend, you can load the module 
``hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+cuda~pthread-cuda_arch=70/~debug``. 
For a debug build, you can load a module including the ``+debug``\ , such as 
``hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=70/+debug``. 
For a release build, you can load a module including the ``~debug``\ , such as 
``hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=70/~debug``.

How to load the modules automatically?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can add the following lines to your ``.bashrc`` file:

.. code-block:: bash

   module load cmake
   source /home/dcurreli/lcpp/hpic2/spack/share/spack/setup-env.sh
   module load hpic2deps/gcc-7.2.0/mvapich2-2.3.5/kokkos+openmp~pthread-cuda_arch=70/~debug

How to generate new modules for hpic2?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New modules can be generated using ``spack``. In order to use spack, 
load the python3 module, ``module load python3``. If you would like to 
generate new modules for hpic2, you can start from the following script:

.. code-block:: bash

   ./home/dcurreli/lcpp/hpic2/spack/install_hpic2deps.sh

Example:

.. code-block:: bash

   spack install hpic2deps%gcc@7.2.0 ^openmpi@4.1.0%gcc@7.2.0+pmi ^googletest%gcc@7.2.0 ^hypre%gcc@7.2.0 ^spdlog%gcc@7.2.0 ^kokkos%gcc@7.2.0+compiler_warnings+debug+debug_bounds_check+debug_dualview_modify_check
   ...
   ...

This script will generate the modules for all the configurations in the 
``configurations`` folder. The script will also generate a ``modulefiles`` folder 
with the modules. You can then copy the ``modulefiles`` folder to the shared 
folder of the campus cluster:

.. code-block:: bash

   cp -r modulefiles /home/dcurreli/lcpp/hpic2/spack/share/spack/modules/linux-rhel7-sandybridge

Check that the list of available moduels now includes the new modules, 

.. code-block:: bash

   less /home/dcurreli/lcpp/hpic2/spack/share/spack/modules/module-index.yaml

Known issues
^^^^^^^^^^^^


* When using OpenMPI with the Intel compiler, must manually ``module load intel/18.0``
* When using CUDA, must manually ``module load cuda``

Step 5: Clone the hpic2 repository
--------------------------------==

Clone the hpic2 repository to your home directory:

.. code-block:: bash

   cd $HOME
   git clone --recurse-submodules https://github.com/lcpp-org/hpic2.git

Step 6: Make a build directory
------------------------------

Make a build directory for hpic2:

.. code-block:: bash

   cd $HOME
   mkdir hpic2-build

Step 7: Configure hpic2
-----------------------

Move to the build directory and configure hpic2:

.. code-block:: bash

   cd $HOME/hpic2-build
   cmake $HOME/hpic2

Example of expected output:

.. code-block:: bash

   $ cmake $HOME/hpic2
   -- The C compiler identification is GNU 7.2.0
   -- The CXX compiler identification is GNU 7.2.0
   -- Detecting C compiler ABI info
   -- Detecting C compiler ABI info - done
   -- Check for working C compiler: /usr/local/gcc/7.2.0/bin/gcc - skipped
   -- Detecting C compile features
   -- Detecting C compile features - done
   -- Detecting CXX compiler ABI info
   -- Detecting CXX compiler ABI info - done
   -- Check for working CXX compiler: /usr/local/gcc/7.2.0/bin/c++ - skipped
   -- Detecting CXX compile features
   -- Detecting CXX compile features - done
   -- Enabled Kokkos devices: OPENMP;SERIAL
   -- Found MPI_C: /usr/local/mpi/rh7/openmpi/4.1.0/gcc/7.2.0/pmi2/lib/libmpi.so (found version "3.1") 
   -- Found MPI_CXX: /usr/local/mpi/rh7/openmpi/4.1.0/gcc/7.2.0/pmi2/lib/libmpi.so (found version "3.1") 
   -- Found MPI: TRUE (found version "3.1")  
   -- Looking for pthread.h
   -- Looking for pthread.h - found
   -- Performing Test CMAKE_HAVE_LIBC_PTHREAD
   -- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
   -- Looking for pthread_create in pthreads
   -- Looking for pthread_create in pthreads - not found
   -- Looking for pthread_create in pthread
   -- Looking for pthread_create in pthread - found
   -- Found Threads: TRUE  
   -- Found Hypre: /home/dcurreli/lcpp/hpic2/spack/opt/spack/linux-rhel7-sandybridge/gcc-7.2.0/hypre-2.20.0-2olp2oaczn3zf4nzq47qlkiqhrr6l6ec/lib/libHYPRE.so  
   -- Configuring done
   -- Generating done
   -- Build files have been written to: /home/dcurreli/hpic2_build_tmp

Step 8: Compile hpic2
---------------------

Compile hpic2 from the build directory:

.. code-block:: bash

   cd $HOME/hpic2-build
   cmake $HOME/hpic2
   make -j8

This will compile hpic2 using 8 cores and produce the ``hpic2`` executable 
in the ``$HOME/hpic2-build`` folder. You can change the number of cores to 
use by changing the number after the ``-j`` flag.

Step 9: Check the executable
----------------------------

Check that the executable is present in the ``$HOME/hpic2-build`` folder:

.. code-block:: bash

   ls $HOME/hpic2-build

If the executable is present, you can check it runs correctly simply as follows:

.. code-block:: bash

   $ ./hpic2

   hpic2: a Hybrid Particle-in-Cell code.
   Developed at Laboratory of Computational Plasma Physics, University of Illinois
    at Urbana-Champaign.

   usage: ./hpic2 -i|--input-deck INPUT_DECK [options]

   options:
       --override-input-warnings: ignore all warnings related to unrecognized
                                  fields found in the input deck. If present, this
                                  flag disables the required user acknowledgement
                                  of input warnings, and the simulation will be
                                  launched despite them.

   For full documentation, see: https://github.com/lcpp-org/hpic2

Acknowledgements
----------------

To cite the ICC in your publications, use the following 
`acknowledgement statement <https://campuscluster.illinois.edu/science/acknowledging/>`_\ : 
"This work made use of the Illinois Campus Cluster, a computing resource that 
is operated by the Illinois Campus Cluster Program (ICCP) in conjunction with 
the National Center for Supercomputing Applications (NCSA) and which is 
supported by funds from the University of Illinois at Urbana-Champaign."
