Running hPIC2
=============

Serial
------

Don't run serial. Move on to MPI. 

MPI
---

Running ``hpic2`` with no arguments or with the ``--help`` option
prints a help message describing usage of the executable.
Typically, running an hPIC2 problem consists of running

.. code-block:: sh

   mpiexec -np n ./hpic2 --i /path/to/input/deck

where ``n`` is the number of MPI procs across which to distribute the run.
hPIC2 reads all the necessary physics information about your problem
from the input deck;
the format of these input decks is described in subsequent sections.

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


Delta
-----


IPS
---

