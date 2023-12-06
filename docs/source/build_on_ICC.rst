
Building hpic2 on the Illinois Campus Cluster (ICC)
===================================================

The Illinois Campus Cluster (`ICC <https://campuscluster.illinois.edu/>`_)
is a high-performance computing (HPC) cluster that is available to the students,
faculty, and staff at the University of Illinois at Urbana-Champaign. The ICC is managed by
the `National Center for Supercomputing Applications (NCSA) <https://www.ncsa.illinois.edu/>`_.
Full documentation for the ICC is available at the following link,
`ICC Documentation <https://docs.ncsa.illinois.edu/systems/icc/en/latest/index.html>`_.
The ICC is a shared resource, and users are expected to abide by the
`ICC User Policy <https://docs.ncsa.illinois.edu/systems/icc/en/latest/user_guide/policies.html>`_.

Step 1: Get an account on the ICC
---------------------------------

If you do not already have an account on the Illinois Campus Cluster,
request access for Research here,

* `ICC Request Access for Research <https://campuscluster.illinois.edu/new_forms/user_form.php>`_

specifying to be added to the following group: ``dcurreli-npre-eng``

Read the ICC `resources <https://campuscluster.illinois.edu/resources/docs/>`_\ , such as:

* `ICC Getting started <https://docs.ncsa.illinois.edu/systems/icc/en/latest/getting_started.html>`_
* `ICC User Guide <https://docs.ncsa.illinois.edu/systems/icc/en/latest/getting_started.html>`_
* `ICC Access <https://docs.ncsa.illinois.edu/systems/icc/en/latest/user_guide/accessing.html>`_
* `ICC Running Jobs <https://docs.ncsa.illinois.edu/systems/icc/en/latest/user_guide/running_jobs.html>`_
* `ICC Storage and Data Guide <https://docs.ncsa.illinois.edu/systems/icc/en/latest/user_guide/storage_data.html>`_
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

In order to build hPIC2, you need to load the necessary modules.
The past few versions of hPIC2 and its dependencies are available as modules.
The most recent version is also marked as ``latest``.
These are provided in a shared folder of the campus cluster.
To see them, you need to use the `module use` command:

.. code-block:: bash

   module use /scratch/users/logantm2/share/modulefiles

(It is recommended to add this line to your ``.bashrc`` file.)
Now the list of available modules should include also the hPIC2 dependencies
in the form ``hpic2deps/<desired configuration>/<version date>``,
where ``<version date>`` refers to the date when the module was generated.
To see the list of available configurations,
type:

.. code-block:: bash

   module avail

The output should now have a block that looks like this:

.. code-block:: bash

   ------------------ /scratch/users/logantm2/share/modulefiles -------------------
   cmake
   hpic2/+openmp-cuda-arch-70/2023-12-05
   hpic2/+openmp-cuda-arch-70/latest
   hpic2/+openmp-cuda-arch-86/2023-12-05
   hpic2/+openmp-cuda-arch-86/latest
   hpic2/+openmp-cuda-arch-None/2023-12-05
   hpic2/+openmp-cuda-arch-None/latest
   hpic2/~openmp-cuda-arch-70/2023-12-05
   hpic2/~openmp-cuda-arch-70/latest
   hpic2/~openmp-cuda-arch-86/2023-12-05
   hpic2/~openmp-cuda-arch-86/latest
   hpic2/~openmp-cuda-arch-None/2023-12-05
   hpic2/~openmp-cuda-arch-None/latest
   hpic2deps/+openmp-cuda-arch-70/Debug/2023-12-05
   hpic2deps/+openmp-cuda-arch-70/Debug/latest
   hpic2deps/+openmp-cuda-arch-70/Release/2023-12-05
   hpic2deps/+openmp-cuda-arch-70/Release/latest
   hpic2deps/+openmp-cuda-arch-86/Debug/2023-12-05
   hpic2deps/+openmp-cuda-arch-86/Debug/latest
   hpic2deps/+openmp-cuda-arch-86/Release/2023-12-05
   hpic2deps/+openmp-cuda-arch-86/Release/latest
   hpic2deps/+openmp-cuda-arch-None/Debug/2023-12-05
   hpic2deps/+openmp-cuda-arch-None/Debug/latest
   hpic2deps/+openmp-cuda-arch-None/Release/2023-12-05
   hpic2deps/+openmp-cuda-arch-None/Release/latest
   hpic2deps/~openmp-cuda-arch-70/Debug/2023-12-05
   hpic2deps/~openmp-cuda-arch-70/Debug/latest
   hpic2deps/~openmp-cuda-arch-70/Release/2023-12-05
   hpic2deps/~openmp-cuda-arch-70/Release/latest
   hpic2deps/~openmp-cuda-arch-86/Debug/2023-12-05
   hpic2deps/~openmp-cuda-arch-86/Debug/latest
   hpic2deps/~openmp-cuda-arch-86/Release/2023-12-05
   hpic2deps/~openmp-cuda-arch-86/Release/latest
   hpic2deps/~openmp-cuda-arch-None/Debug/2023-12-05
   hpic2deps/~openmp-cuda-arch-None/Debug/latest
   hpic2deps/~openmp-cuda-arch-None/Release/2023-12-05
   hpic2deps/~openmp-cuda-arch-None/Release/latest

The configuration specifies whether OpenMP is enabled
(``+openmp`` for enabled and ``~openmp`` for disabled),
whether CUDA is enabled and the Compute Capability (CC) of the target NVIDIA GPU
(``cuda-arch-70`` for CC 7.0, ``cuda-arch-86`` for CC 8.6, and ``cuda-arch-None`` for no CUDA),
and whether the dependencies are for a debug or release build
(``Debug`` for debug and ``Release`` for release).

Now you can load the desired modules, for example:

.. code-block:: bash

   module purge
   module load hpic2deps/+openmp-cuda-arch-None/Release/latest

will load the latest version of the hPIC2 dependencies
in release mode, with OpenMP but without CUDA.

A ``module list`` command should now show the loaded modules, for example:

.. code-block:: bash

   Currently Loaded Modulefiles:
   1) gcc/8.2.0
   2) openmpi/4.1.4-gcc-8.2.0
   3) cmake
   4) anaconda/3
   5) hpic2deps/+openmp-cuda-arch-None/Release/latest

Which modules to load?
^^^^^^^^^^^^^^^^^^^^^^

In order to fully utilize the hybrid parallelism of hpic2 on the ICC,
you need to load modules including either OpenMP or CUDA.
For example, to use the OpenMP backend, you can load the module
``hpic2deps/+openmp-cuda-arch-None/Release/latest``.
For a debug build, you can load a module including ``Debug``, such as
``hpic2deps/+openmp-cuda-arch-None/Debug/latest``.

A little bit more work is required to use CUDA.
There are two main GPU types on the cluster:
V100s and A10s.
The V100s have Compute Capability (CC) 7.0,
whereas the A10s have CC 8.6.
You must load the module corresponding to the nodes you intend to run on.
For example, to run on the V100 nodes, you can load the module
``hpic2deps/+openmp-cuda-arch-70/Release/latest``.

How to load the modules automatically?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can add the following lines to your ``.bashrc`` file:

.. code-block:: bash

   module use /scratch/users/logantm2/share/modulefiles
   module purge
   module load hpic2deps/+openmp-cuda-arch-None/Release/latest

Known issues
^^^^^^^^^^^^

* Cannot build with MFEM pending an issue with link order.

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
   cmake $HOME/hpic2 -DWITH_RUSTBCA=ON -DWITH_PUMIMBBL=ON

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
   make -j4

This will compile hpic2 using 4 cores and produce the ``hpic2`` executable
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
