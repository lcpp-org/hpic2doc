Running hPIC2
=============

Serial
------

Don't run serial, move on to MPI. But if you really have to,
just run the executable with the ``--i`` option and the path to
your input deck as an argument. For example, to run your hpic2
executable with the input deck ``myinput.toml``,

.. code-block:: sh

   hpic2 --i myinput.toml


MPI
---

Running ``hpic2`` with no arguments or with the ``--help`` option
prints a help message describing usage of the executable.
Typically, running an hPIC2 problem consists of running

.. code-block:: sh

   mpiexec -np n <hpic2-executable> --i <path-to-input-deck>

where ``n`` is the number of MPI procs across which to distribute the run.
hPIC2 reads all the necessary physics information about your problem
from the input deck;
the format of these input decks is described in subsequent sections.
For example, to run your hpic2 executable with 4 MPI processes,

.. code-block:: sh

   mpiexec -np 4 hpic2 --i myinput.toml

As a program that uses both MPI for distributed-memory parallelism
and Kokkos for shared-memory parallelism,
the hPIC2 executable accepts options for both to customize the
state of the runtime environment.
MPI runtime options differ depending on the implementation.
For most workstation runs, the above command is sufficient to fully utilize
the system.
As an example for further runtime customization,
`OpenMPI's documentation <https://www.open-mpi.org/doc/v4.0/man1/mpirun.1.php>`_
provides many more options.
For runs on supercomputers, consult the documentation of
the MPI implementation for proper use,
or contact an hPIC2 developer for advice.
hPIC2 also accepts options from the Kokkos
`list <https://github.com/kokkos/kokkos/wiki/Initialization#table-51-command-line-options-for-kokkosinitialize->`_
of initialization options.
Generally, if Kokkos is enabled with a thread-parallel host backend,
hPIC2 will attempt to utilize all available threads unless
otherwise specified.


Illinois Campus Cluster
-----------------------

hPIC2 is installed on the Illinois Campus Cluster (ICC)
and available to LCPP users.
The past few versions of hPIC2 and its dependencies are available as modules.
The most recent version is also marked as ``latest``.
You can expose the relevant modules by running the following command:

.. code-block:: bash

   module use /projects/illinois/eng/npre/dcurreli/campuscluster_spack/modulefiles

(It is recommended to add this line to your ``.bashrc`` file.)
Now the list of available modules should include hPIC2
in the form ``hpic2/<desired configuration>/<version date>``,
where ``<version date>`` refers to the date when the module was generated.
To see the list of available configurations,
type:

.. code-block:: bash

   module avail

The output should now have a block that looks like this:

.. code-block:: bash

   ------------------ /projects/illinois/eng/npre/dcurreli/campuscluster_spack/modulefiles -------------------
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
(``+openmp`` for enabled and ``~openmp`` for disabled) and
whether CUDA is enabled and the Compute Capability (CC) of the target NVIDIA GPU
(``cuda-arch-70`` for CC 7.0, ``cuda-arch-86`` for CC 8.6, and ``cuda-arch-None`` for no CUDA).
Now you can load the desired modules, for example:

.. code-block:: bash

   module purge
   module load hpic2/+openmp-cuda-arch-None/latest

will load the latest version of hPIC2 with OpenMP but without CUDA.
After loading any of the ``hpic2/*`` modules,
the ``hpic2`` executable will be available in your ``PATH``.

To run hPIC2 on the ICC, you will need to submit a job to the SLURM scheduler.
Check out this example bash script

.. literalinclude:: ../../scripts/icc_openmp_example.sbatch
   :language: bash

and modify it to suit your needs. Here are some notes on the script:
the ``--time`` option specifies the maximum runtime of the job,
the ``--nodes`` option specifies the number of nodes to use,
the ``--tasks-per-node`` option specifies the number of MPI processes per node,
the ``--cpus-per-task`` option specifies the number of threads per MPI process,
the ``--mem-per-cpu`` option specifies the amount of memory per thread,
the ``--job-name`` option specifies the name of the job,
the ``--partition`` option specifies the partition to run on (e.g. ``eng-research``),
the ``--output`` option specifies the name of the output file,
and the ``--error`` option specifies the name of the error file.

To submit the job, run the following command:

.. code-block:: sh

   sbatch <name-of-script>.sbatch

To check the status of the job, run the following command:

.. code-block:: sh

   squeue --me

To cancel the job, run the following command:

.. code-block:: sh

   scancel <job-id>
