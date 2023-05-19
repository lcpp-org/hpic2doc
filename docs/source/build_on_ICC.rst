
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
Dependencies are handled via `spack <https://spack.io/>`_.
A spack environment is provided in a shared folder of the campus cluster.
To use it, you need to source the spack environment:

.. code-block:: bash

   source /home/logantm2/share/spack/share/spack/setup-env.sh

Now the list of available modules should include also the hpic2 dependencies
in the form ``hpic2deps/<desired-configuration>``\ , where ``<desired-configuration>``
is a combination of the libraries and compilers. For example, to use the GCC
compiler and the OpenMPI library, you can load the module
``hpic2deps/gcc-8.2.0/openmpi-4.1.4/<additional options>``.
To see the list of available configurations,
type:

.. code-block:: bash

   module avail

The output should now look like this:

.. code-block:: bash

   --------------------------------------------------------------------- /home/logantm2/share/spack/share/spack/modules/linux-rhel7-sandybridge ----------------------------------------------------------------------
   berkeley-db/ywedesyuksbao2hvydby5petbnkkp5h5                        hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos~openmp+pthread~cuda/~debug mfem/3ig32fska5si27kqokjkfmmq7gkdh6wr
   bzip2/umydrl2hddhx4aox4agypqochacdvylh                              hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos~openmp~pthread~cuda/+debug mfem/3ss6fvwftbpy7anqa2rx3wqnwvtnx3jf
   ca-certificates-mozilla/hz7uokisoulr4xxkxzedm4fh25akvzsa            hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos~openmp~pthread~cuda/~debug mfem/h7dalt34tv2qjhoxhlmruqsuowasvdck
   cmake/oguolevxfkshg7pesak6j6txrqmbcif6                              hypre/6kog5ghteysufv4tept7iw3axzhqbld5                              mfem/hiagqk42kkj7u67f2xjwdrddciaoypel
   cuda/ldovkahimo3jbs65cjlfkloxo5mwlaf6                               kokkos/3lxmkn4opoy3345pkwfkssjrbqzvowl5                             ncurses/dkehzhlmhfilyytqrbjvlfec6xp2lkg6
   diffutils/t25bet7qlskfjj4n6u777uwtmwefvmyi                          kokkos/3s2pu2uf767j2dp5apfatxdogqzlb6jm                             openblas/6iismk3yomdzrjokiouvdxgufssch3ys
   gdbm/2jjcrmy7lmtypzdlhyqlzgopiabc5e2n                               kokkos/76l2z2pz3rowdykwjjboikzr4ylhbiv3                             openmpi/dszsfg2fbkalv7pp3husb7y562o3hpw3
   gmake/d3osoidv7oklhch3o6x3urzpu7xvhwsw                              kokkos/bv4ymtu6u4kqyktglga5m7445vjjqogd                             openssl/2solcz7zwzdld4l7a6ugcj5ggtg5aqyn
   googletest/jrls53uwhvtla2y4nyxj5nmm4hlvuusv                         kokkos/fgz5g5kuyxtfs74io4lezp4c55r5aifp                             perl/zyo4ghspyxb2kk7hdppm4rjn7tvwugoo
   hdf5/adlpghib4yxif3r3nzl3n7fqcgyeiied                               kokkos/r6bp3uwgktrqe26jyiw2tmeh5efcafz2                             pkgconf/dubwtb3eulxgo3bkpeqs5plnxaxencju
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread+cuda/+debug kokkos/szd4fwkv3vcmyhf4r4np7axdq4wyxnrw                             readline/gzx2j4omsdomqyaezyu5mizgkmzghhkm
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread+cuda/~debug kokkos/vfenl2e6g4pd25l3fezsmqeno7jtwo52                             spdlog/snfoztnizhqurhkhrx5zrxt54sphzzlb
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread~cuda/+debug kokkos-nvcc-wrapper/tg27x6bflvlu2lpwv5n7cu3oip7wjahi                zlib/dyc2g2hml2v42bwcuxpxt65n7ytpjtj6
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread~cuda/~debug libiconv/vawybcva23n3seeqy4bmuylxfl3rgrhh
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos~openmp+pthread~cuda/+debug metis/qulheqtvkr6hdh52nhtl5tjrlc3j7mrv


Now you can load the desired modules, for example:

.. code-block:: bash

   module purge
   module load hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread~cuda/~debug

A ``module list`` command should now show the loaded modules, for example:

.. code-block:: bash

   Currently Loaded Modulefiles:
   1) zlib/dyc2g2hml2v42bwcuxpxt65n7ytpjtj6                                 9) metis/qulheqtvkr6hdh52nhtl5tjrlc3j7mrv
   2) spdlog/snfoztnizhqurhkhrx5zrxt54sphzzlb                              10) mfem/3ig32fska5si27kqokjkfmmq7gkdh6wr
   3) pkgconf/dubwtb3eulxgo3bkpeqs5plnxaxencju                             11) kokkos/76l2z2pz3rowdykwjjboikzr4ylhbiv3
   4) openssl/2solcz7zwzdld4l7a6ugcj5ggtg5aqyn                             12) hdf5/adlpghib4yxif3r3nzl3n7fqcgyeiied
   5) openmpi/dszsfg2fbkalv7pp3husb7y562o3hpw3                             13) googletest/jrls53uwhvtla2y4nyxj5nmm4hlvuusv
   6) openblas/6iismk3yomdzrjokiouvdxgufssch3ys                            14) cuda/ldovkahimo3jbs65cjlfkloxo5mwlaf6
   7) ncurses/dkehzhlmhfilyytqrbjvlfec6xp2lkg6                             15) cmake/oguolevxfkshg7pesak6j6txrqmbcif6
   8) hypre/6kog5ghteysufv4tept7iw3axzhqbld5                               16) hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread~cuda/~debug

The modules with long hashes are dependent submodules of the ``hpic2deps`` module.

Which modules to load?
^^^^^^^^^^^^^^^^^^^^^^

In order to fully utilize the hybrid parallelism of hpic2 on the ICC,
you need to load modules including either ``+openmp`` or ``+cuda`` in the name.
For example, to use the OpenMP backend, you can load the module
``hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread~cuda/~debug``.
To use the CUDA backend, you can load the module
``hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread+cuda/~debug``.
For a debug build, you can load a module including the ``+debug``\ , such as
``hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread~cuda/+debug``.
For a release build, you can load a module including the ``~debug``\ , such as
``hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread~cuda/~debug``.

How to load the modules automatically?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can add the following lines to your ``.bashrc`` file:

.. code-block:: bash

   source /home/logantm2/share/spack/share/spack/setup-env.sh
   module purge
   module load hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~pthread~cuda/~debug

How to generate new modules for hpic2?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
----------------------------------

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

   -- The C compiler identification is GNU 8.2.0
   -- The CXX compiler identification is GNU 8.2.0
   -- Detecting C compiler ABI info
   -- Detecting C compiler ABI info - done
   -- Check for working C compiler: /usr/local/gcc/8.2.0/bin/gcc - skipped
   -- Detecting C compile features
   -- Detecting C compile features - done
   -- Detecting CXX compiler ABI info
   -- Detecting CXX compiler ABI info - done
   -- Check for working CXX compiler: /usr/local/gcc/8.2.0/bin/c++ - skipped
   -- Detecting CXX compile features
   -- Detecting CXX compile features - done
   -- Enabled Kokkos devices: OPENMP;SERIAL
   -- Found MPI_C: /usr/local/mpi/openmpi/4.1.4/gcc/8.2.0/lib/libmpi.so (found version "3.1")
   -- Found MPI_CXX: /usr/local/mpi/openmpi/4.1.4/gcc/8.2.0/lib/libmpi.so (found version "3.1")
   -- Found MPI: TRUE (found version "3.1")
   -- Performing Test CMAKE_HAVE_LIBC_PTHREAD
   -- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
   -- Looking for pthread_create in pthreads
   -- Looking for pthread_create in pthreads - not found
   -- Looking for pthread_create in pthread
   -- Looking for pthread_create in pthread - found
   -- Found Threads: TRUE
   -- Found Hypre: /home/logantm2/share/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.2.0/hypre-2.28.0-6kog5ghteysufv4tept7iw3axzhqbld5/lib/libHYPRE.so
   -- Found HDF5: hdf5_cpp-shared (found version "1.14.1") found components: CXX
   -- Configuring done (2.4s)
   -- Generating done (0.0s)
   -- Build files have been written to: /home/logantm2/hpic2_openmp_release

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
