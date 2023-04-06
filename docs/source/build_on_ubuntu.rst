
Building hpic2 on Ubuntu via spack
==================================

Those instuctions were tested on Ubuntu 22.04 LTS jammy.

Download and source spack
-------------------------

Install the package manager 
`spack <https://spack.readthedocs.io/en/latest/index.html>`_ 
as described in the 
`spack documentation <https://spack.readthedocs.io/en/latest/getting_started.html>`_. 
Python 3.6 or later is required. Check also the 
`minimum system requirements <https://spack.readthedocs.io/en/latest/getting_started.html#system-prerequisites>`_
which are assumed to be present on the machine where Spack is run. 

Download the spack repository 
(suggested location, ``$HOME`` directory)

.. code-block::

   git clone -c feature.manyFiles=true https://github.com/spack/spack.git


Source the spack environment

.. code-block::

   source $HOME/spack/share/spack/setup-env.sh


Since the source step is needed every time, 
we suggest to add the source command to your ``.bashrc`` file. 

Install hpic2 via Spack
-----------------------

Make a new spack repository for hpic2

.. code-block::

   spack repo create hpic2_dev


Register spack repository

.. code-block::

   spack repo add hpic2_dev


Change to the spack repository ``packages`` directory

.. code-block::

   cd /hpic2_dev/packages


Download the hpic2 source with its submodules

.. code-block::

   git clone --recurse-submodules https://github.com/lcpp-org/hpic2.git


Optionally, download the rustbca source

.. code-block::

   git clone https://github.com/lcpp-org/RustBCA.git


and rename it to ``rustbca``

.. code-block::

   mv RustBCA rustbca


Use spack to install hpic2

.. code-block::

   spack install hpic2+testing+rustbca ^kokkos+openmp


The ``+testing`` option enables the tests and 
the ``+rustbca`` option enables the RustBCA solver. 
The ``^kokkos+openmp`` option enables the OpenMP backend of Kokkos
to allow for shared-memory parallelism. 
The ``+cuda`` option enables the CUDA backend of Kokkos. 

.. warning::

   The ``spack install`` command will take a while to
   complete. Depending on the speed your machine this can 
   take up to 10 hours. Plan accordingly. 
