
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

   ---------------------------------------------------------------------- /home/logantm2/share/spack/share/spack/modules/linux-rhel7-broadwell -----------------------------------------------------------------------
   berkeley-db/whkl34dyhiyyucnodtq7d54hponalu77                                kokkos/i5kpt4sbuqsqx2lsu76t2snogwihyfyq
   bzip2/kru65z26vmowdfncpkuxcu4jrhlqoryn                                      kokkos/igd6mhtohiaheudyhjcqufeyrxlziskb
   ca-certificates-mozilla/6epw3wprmf7pqjr77wsnwu7z3ct2ghvh                    kokkos/inqgneifiafoo65sibdgzc4tvap4kcn4
   cmake/ris452uafjevbjmzsb3omuaappxhinih                                      kokkos/ok4jr4u4bdrwq62kaomhuulxrv4cpztv
   cuda/ajg3d2xhe7uqpwadrdtogqfuguxww7cv                                       kokkos/wmtrpdeuqaivzzrtzu534ixqgxxhmrus
   curl/b6uexft6mivyzgoivsf5swqtvefhrius                                       kokkos-nvcc-wrapper/f4ehc24wnng6pa4ni3mpfwuc2l5lw3co
   diffutils/zhg75e4qwyf7kc32duquzn4sn6xzug6p                                  libiconv/rwnetmcbalo6jf54gthchpkoowmq7ozb
   gdbm/54wyi4k4m4zluhy3gk5zcgnecdjv6uj5                                       metis/pzlmomifruqqjhsakamas4aheufrko6t
   gmake/wl36mnohkox5kkv4tvkjxl5zvq7w77s2                                      mfem/dv5vqt7pfbffkopbw6uebw4ddr4dtzrm
   googletest/b7qf5czgre7jevqlzwnd3wxe2urmb5qe                                 mfem/mi5wvude2vji3bue6rpv35qxi6g5orxf
   hdf5/vhky5innywdthi467axsqpqloak4wyh3                                       mfem/nbubqg3pziugqyyn55bc62hlu44wilmc
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads+cuda/+debug/ijx5e5y mfem/nk5lwti2vixj6vjpjwq3eawjiw7p37x3
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads+cuda/+debug/kfqouuu mfem/qn3wwoel7wbaiq5gvatbrmxdrvwq6bhq
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads+cuda/~debug/b4qghgu mfem/qobvaalki6xfmqz6vwgwr74csyhdry6g
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads+cuda/~debug/wx7itr2 mfem/torsksjujw7z6p7wkejpmtvyi24rcsd5
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads~cuda/+debug/6gwnr4g mfem/vgrl656pcwokw2meciitihadvf3e33dn
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads~cuda/~debug/po3ggco ncurses/3zojnvbmscs65qscuwx6vfyfd5sg62r6
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos~openmp+threads~cuda/+debug/dh7ayxh nghttp2/po2ilhiczysycq3kadhdbgi74b4qnnpq
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos~openmp+threads~cuda/~debug/4e4xvri openblas/sqs52e3y3tg4ppytdetxhiihdfrog5q6
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos~openmp~threads~cuda/+debug/5b33jls openmpi/mly6sy3dfrpugef4o74lz3un7uv7ht2j
   hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos~openmp~threads~cuda/~debug/vkhnyhd openssl/7qnyy7z2zlnga7uxnjislgtizyhw3mo7
   hypre/5i5vubkv73svzy3tp5eppqklc2vxnm7f                                      perl/24ggfycduqqit434cd5qcxmbnlex7erz
   kokkos/3nmmtfthwymyvqk2e5up54xpeyguwu6k                                     pkgconf/nrzd3nbpvy7674cl7vhngj6ylkmmxuxc
   kokkos/3ptpc5eifcdlmqqo2n43nezge7mvlmzy                                     readline/ta46if5eireyg6csugdxu5u4uvwmtslu
   kokkos/6xt5rs2ekms74tkek3yi2wjzqquw3y4g                                     spdlog/r26kz7hh4coo23rod7swiuh2c6we3pk3
   kokkos/gwsttvjdixkxf3cutanez4l5w633lvpv                                     zlib-ng/stvfbiik54rfrphpc2uq7xygaaq4hj3g
   kokkos/he2ijnnxyhbqvmkefnsmyixgfbxlfbmx


Now you can load the desired modules, for example:

.. code-block:: bash

   module purge
   module load hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads~cuda/~debug/po3ggco

A ``module list`` command should now show the loaded modules, for example:

.. code-block:: bash

   Currently Loaded Modulefiles:
   1) zlib-ng/stvfbiik54rfrphpc2uq7xygaaq4hj3g                                     10) metis/pzlmomifruqqjhsakamas4aheufrko6t
   2) spdlog/r26kz7hh4coo23rod7swiuh2c6we3pk3                                      11) mfem/nk5lwti2vixj6vjpjwq3eawjiw7p37x3
   3) pkgconf/nrzd3nbpvy7674cl7vhngj6ylkmmxuxc                                     12) kokkos/wmtrpdeuqaivzzrtzu534ixqgxxhmrus
   4) openssl/7qnyy7z2zlnga7uxnjislgtizyhw3mo7                                     13) hdf5/vhky5innywdthi467axsqpqloak4wyh3
   5) openmpi/mly6sy3dfrpugef4o74lz3un7uv7ht2j                                     14) googletest/b7qf5czgre7jevqlzwnd3wxe2urmb5qe
   6) openblas/sqs52e3y3tg4ppytdetxhiihdfrog5q6                                    15) curl/b6uexft6mivyzgoivsf5swqtvefhrius
   7) nghttp2/po2ilhiczysycq3kadhdbgi74b4qnnpq                                     16) cuda/ajg3d2xhe7uqpwadrdtogqfuguxww7cv
   8) ncurses/3zojnvbmscs65qscuwx6vfyfd5sg62r6                                     17) cmake/ris452uafjevbjmzsb3omuaappxhinih
   9) hypre/5i5vubkv73svzy3tp5eppqklc2vxnm7f                                       18) hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads~cuda/~debug/po3ggco

The modules with long hashes are dependent submodules of the ``hpic2deps`` module.

Which modules to load?
^^^^^^^^^^^^^^^^^^^^^^

In order to fully utilize the hybrid parallelism of hpic2 on the ICC,
you need to load modules including either ``+openmp`` or ``+cuda`` in the name.
For example, to use the OpenMP backend, you can load the module
``hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads~cuda/~debug/po3ggco``.
For a debug build, you can load a module including the ``+debug``\ , such as
``hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads~cuda/+debug/6gwnr4g``.
For a release build, you can load a module including the ``~debug``\ , such as
``hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads~cuda/~debug/po3ggco``.

A little bit more work is required to use CUDA.
There are two main GPU types on the cluster:
V100s and A10s.
The V100s have Compute Capability (CC) 7.0,
whereas the A10s have CC 8.6.
You must load the module corresponding to the nodes you intend to run on.
To check which CC a module is built for, run ``spack spec`` on the short hash
at the end of the module name.
For example, ``spack spec /b4qghgu`` returns

.. code-block::

   Input spec
   --------------------------------
   -   /b4qghgu

   Concretized
   --------------------------------
   [+]  hpic2deps@main%gcc@8.2.0 build_system=bundle arch=linux-rhel7-broadwell
   [+]      ^cmake@3.26.3%gcc@8.2.0~doc+ncurses+ownlibs build_system=generic build_type=Release arch=linux-rhel7-broadwell
   [+]          ^curl@8.1.2%gcc@8.2.0~gssapi~ldap~libidn2~librtmp~libssh~libssh2+nghttp2 build_system=autotools libs=shared,static tls=openssl arch=linux-rhel7-broadwell
   [+]              ^nghttp2@1.52.0%gcc@8.2.0 build_system=autotools arch=linux-rhel7-broadwell
   [+]              ^openssl@3.1.2%gcc@8.2.0~docs+shared build_system=generic certs=mozilla arch=linux-rhel7-broadwell
   [+]                  ^ca-certificates-mozilla@2023-05-30%gcc@8.2.0 build_system=generic arch=linux-rhel7-broadwell
   [+]          ^ncurses@6.4%gcc@8.2.0~symlinks+termlib abi=none build_system=autotools arch=linux-rhel7-broadwell
   [+]          ^zlib-ng@2.1.3%gcc@8.2.0+compat+opt build_system=autotools patches=299b958,ae9077a,b692621 arch=linux-rhel7-broadwell
   [e]      ^cuda@11.7.1%gcc@8.2.0~allow-unsupported-compilers~dev build_system=generic arch=linux-rhel7-broadwell
   [+]      ^googletest@1.12.1%gcc@8.2.0+gmock~ipo+pthreads+shared build_system=cmake build_type=Release cxxstd=11 generator=make arch=linux-rhel7-broadwell
   [+]          ^gmake@4.4.1%gcc@8.2.0~guile build_system=autotools arch=linux-rhel7-broadwell
   [+]      ^hdf5@1.14.2%gcc@8.2.0+cxx~fortran~hl~ipo~java~map+mpi+shared~szip~threadsafe+tools api=default build_system=cmake build_type=Release generator=make arch=linux-rhel7-broadwell
   [+]          ^pkgconf@1.9.5%gcc@8.2.0 build_system=autotools arch=linux-rhel7-broadwell
   [+]      ^hypre@2.29.0%gcc@8.2.0~caliper~complex~cuda~debug+fortran~gptune~int64~internal-superlu~mixedint+mpi~openmp~rocm+shared~superlu-dist~sycl~umpire~unified-memory build_system=autotools arch=linux-rhel7-broadwell
   [+]          ^openblas@0.3.10%gcc@8.2.0~bignuma~consistent_fpcsr~ilp64+locking+pic+shared build_system=makefile patches=865703b symbol_suffix=none threads=none arch=linux-rhel7-broadwell
   [+]              ^perl@5.38.0%gcc@8.2.0+cpanm+opcode+open+shared+threads build_system=generic patches=714e4d1 arch=linux-rhel7-broadwell
   [+]                  ^berkeley-db@18.1.40%gcc@8.2.0+cxx~docs+stl build_system=autotools patches=26090f4,b231fcc arch=linux-rhel7-broadwell
   [+]                  ^bzip2@1.0.8%gcc@8.2.0~debug~pic+shared build_system=generic arch=linux-rhel7-broadwell
   [+]                      ^diffutils@3.9%gcc@8.2.0 build_system=autotools arch=linux-rhel7-broadwell
   [+]                          ^libiconv@1.17%gcc@8.2.0 build_system=autotools libs=shared,static arch=linux-rhel7-broadwell
   [+]                  ^gdbm@1.23%gcc@8.2.0 build_system=autotools arch=linux-rhel7-broadwell
   [+]                      ^readline@8.2%gcc@8.2.0 build_system=autotools patches=bbf97f1 arch=linux-rhel7-broadwell
   [+]      ^kokkos@3.7.02%gcc@8.2.0~aggressive_vectorization+compiler_warnings+cuda~cuda_constexpr+cuda_lambda~cuda_ldg_intrinsic~cuda_relocatable_device_code~cuda_uvm~debug~debug_bounds_check~debug_dualview_modify_check~deprecated_code~examples~hpx~hpx_async_dispatch~hwloc~ipo~memkind~numactl+openmp~openmptarget+pic~rocm+serial+shared~sycl~tests~threads~tuning+wrapper build_system=cmake build_type=Release cuda_arch=86 cxxstd=17 generator=make intel_gpu_arch=none arch=linux-rhel7-broadwell
   [+]          ^kokkos-nvcc-wrapper@4.0.01%gcc@8.2.0 build_system=generic arch=linux-rhel7-broadwell
   [+]      ^metis@5.1.0%gcc@8.2.0~gdb~int64~ipo~real64+shared build_system=cmake build_type=Release generator=make patches=4991da9,93a7903,b1225da arch=linux-rhel7-broadwell
   [+]      ^mfem@4.5.2%gcc@8.2.0~amgx~conduit+cuda~debug~examples~exceptions~fms~ginkgo~gnutls~gslib~hiop~lapack~libceed~libunwind+metis~miniapps~mpfr+mpi~netcdf~occa~openmp~petsc~pumi~raja~rocm~shared~slepc+static~strumpack~suite-sparse~sundials~superlu-dist~threadsafe~umpire~zlib build_system=generic cuda_arch=86 timer=auto arch=linux-rhel7-broadwell
   [e]      ^openmpi@4.1.4%gcc@8.2.0~atomics~cuda~cxx~cxx_exceptions~gpfs~internal-hwloc~internal-pmix~java~legacylaunchers~lustre~memchecker~openshmem~orterunprefix+romio+rsh~singularity+static+vt+wrapper-rpath build_system=autotools fabrics=none schedulers=none arch=linux-rhel7-broadwell
   [+]      ^spdlog@1.11.0%gcc@8.2.0~fmt_external~ipo+shared build_system=cmake build_type=Release generator=make arch=linux-rhel7-broadwell

Note that ``kokkos`` is enabled with ``cuda_arch=86``
(this can be seen on the line starting with ``^kokkos``),
which means that it is compiled for CC 8.6.
The command
``module load hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads+cuda/~debug/b4qghgu``
therefore loads the dependencies for GPUs with CC 8.6.

How to load the modules automatically?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can add the following lines to your ``.bashrc`` file:

.. code-block:: bash

   source /home/logantm2/share/spack/share/spack/setup-env.sh
   module purge
   module load hpic2deps/gcc-8.2.0/openmpi-4.1.4/kokkos+openmp~threads~cuda/~debug/po3ggco

How to generate new modules for hpic2?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The modules were generated using the scripts in the
`campuscluster_spack <https://github.com/logantm2/campuscluster_spack>`_
github repo.
Add additional lines in ``install_hpic2deps.sh``
before running ``. setup.sh`` to register new modules.

Known issues
^^^^^^^^^^^^

* The dependencies have only been built with CUDA for CC 7.0.
  Your mileage may vary on GPUs with other Compute Capabilities.
* Cannot build with both CUDA and MFEM pending an issue with cusparse.

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
