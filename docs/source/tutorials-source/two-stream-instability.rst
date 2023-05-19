Two-Stream Instability
======================

Problem Description
-------------------

Two-stream instability is one of the classical examples of beam-type instability that occurs in plasma physics.
Streaming instabilities are a special case of instability whereby the thermal non-equilibrium
is caused by relative drift velocities between two plasma species.

In this problem, we consider a plasma made of the following species:

* Two electron populations, ``"e-_red"`` and ``"e-_blue"``, with equal but opposite drift velocities :math:`\vec{v}_0 = \pm v_0 \hat{x}`, each with number density :math:`n_0/2`
* A charge-neutralizing hydrogen background ``"h+"`` and number density :math:`n_0`

The two electron populations interact electrostatically with each other and with the
stationary ion background.

Theory
------

The dispersion relation for the two-stream instability can be derived using linearized Vlasov-Poisson theory as

.. math::
   :label: TSI_dispersion_relation

   1 = \frac{1}{2} \omega_p^2 \left[ \frac{1}{\left(\omega - k v_0 \right)^2} + \left(\frac{1}{\omega - k v_0}\right)^2 \right],

Where :math:`\omega` and :math:`k` are respectively the angular frequency and wave-number of the unstable electrostatic wave,
:math:`\omega_p^2 \approx n_e e^2/(m_e \epsilon_0)`
is the plasma frequency of electrons with number density :math:`n_e`
and mass :math:`m_e` , and :math:`v_0` is the initial drift speed of the electron streams

Simulation Setup
----------------

* One-dimensional periodic domain

* Uniform mesh

* Plasma density :math:`n_0 = 10^{16} \; [m^{-3}]`

* Number of computational particles = 50,000 particles/population

* Beam flow speed: :math:`\vec{v}_0 = 3.2 \times 10^{5} \hat{x} \; [m/s]`


Input File (TOML)
-----------------

.. literalinclude:: ../../../examples/twostream.toml
   :language: toml
   :lines: 1-

The mesh used in this example is ``type = "uniform"``.
The domain size :math:`L` was selected to match the wavelength of interest,
where :math:`k = 2 \pi/L`.
:math:`dx` is computed using :math:`dx = v_0 \Delta t`,
and is represented in the toml file as ``x1_elem_size = 2.97e-6``.

Time step is computed as :math:`dt = 2\pi/(\omega_p 120)`.
1800 time steps, or 15 plasma oscillation periods, are simulated:

Three species are specified under ``[species]``: two electrons populations,
``"e-_red"`` and ``"e-_blue"``; with a hydrogen background ``"h+"``.
For each electron population, 50,000 computational particles are used,
and specified using ``num_particles`` block.
``mass`` is the species mass.
``type`` is the way which the species is represented or simulated.


Running
-------

To run the simulation, use the following command:

.. code-block:: bash

   $ hpic2 --i twostream.toml

The simulation will run for 15 plasma oscillation periods,
and all outputs will be tagged with the ``twostream`` prefix.

The standard output will show the simulation progress:

.. code-block:: bash

   $ ./hpic2 --i twostream.toml
   2023-05-19 14:18:51.005513 UTC-05:00     info [main] [mpi rank 0] starting simulation.
   2023-05-19 14:18:51.008076 UTC-05:00     info [State] [mpi rank 0] At timestep 1
   2023-05-19 14:18:51.013872 UTC-05:00     info [State] [mpi rank 0] At timestep 2
   2023-05-19 14:18:51.019758 UTC-05:00     info [State] [mpi rank 0] At timestep 3
   2023-05-19 14:18:51.025716 UTC-05:00     info [State] [mpi rank 0] At timestep 4
   2023-05-19 14:18:51.031703 UTC-05:00     info [State] [mpi rank 0] At timestep 5
   2023-05-19 14:18:51.037660 UTC-05:00     info [State] [mpi rank 0] At timestep 6
   2023-05-19 14:18:51.043784 UTC-05:00     info [State] [mpi rank 0] At timestep 7
   2023-05-19 14:18:51.049955 UTC-05:00     info [State] [mpi rank 0] At timestep 8
   2023-05-19 14:18:51.055793 UTC-05:00     info [State] [mpi rank 0] At timestep 9
   ...


Plotting the results
---------------------

The simulation results are stored in the ``twostream_example_out`` folder.
This folder contains four files:

* ``twostream_ENERGY_ELECTROSTATIC.dat``, an ASCII file that contains
  a zero-padded timestep alongside the total electrostatic energy at that
  time step on each line.
* ``twostream_fields.hdf``, a VTKHDF file that contains the fields.
* ``twostream_e-_red.h5part``, an h5part file that contains the ``e-_red`` particles.
* ``twostream_e-_blue.h5part``, an h5part file that contains the ``e-_blue`` particles.

The latest version of ParaView can read VTKHDF and h5part files.
It is also possible to read these files
using Python and the ``h5py`` package.
Note that this example only wrote results at the last time step.

.. code-block:: python

   import h5py
   import matplotlib.pyplot as plt
   import numpy as np

   field_file = h5py.File("twostream_example_out/twostream_fields.hdf", 'r')
   red_particle_file = h5py.File("twostream_example_out/twostream_e-_red.h5part", 'r')
   blu_particle_file = h5py.File("twostream_example_out/twostream_e-_blue.h5part", 'r')

   nsteps = field_file["VTKHDF/Steps"].attrs["NSteps"]
   node_coords = field_file["VTKHDF/Points"]
   node_coords = np.reshape(node_coords, (-1, 3))

   # Plot the x1-component of the electric field at the last time step
   field_E = field_file["VTKHDF/PointData/field_E"]
   field_E = np.reshape(field_E, (nsteps, -1, 3))
   plt.plot(node_coords[:,0], field_E[-1,:,0], label="E_x")
   plt.legend()
   plt.xlabel("x_1")
   plt.ylabel("E")
   plt.savefig("twostream_E.png")
   plt.close('all')

   # Plot the potential at the last time step
   field_phi = field_file["VTKHDF/PointData/field_phi"]
   field_phi = np.reshape(field_phi, (nsteps, -1))
   plt.plot(node_coords[:,0], field_phi[-1,:])
   plt.xlabel("x_1")
   plt.ylabel("phi")
   plt.savefig("twostream_phi.png")
   plt.close('all')

   # Plot the particles in phase space at the last time step
   red_x1 = red_particle_file["Step#0/x"][:]
   red_v1 = red_particle_file["Step#0/v1"][:]
   blu_x1 = blu_particle_file["Step#0/x"][:]
   blu_v1 = blu_particle_file["Step#0/v1"][:]
   plt.plot(red_x1, red_v1, 'r,')
   plt.plot(blu_x1, blu_v1, 'b,')
   plt.xlabel("x_1")
   plt.ylabel("v_1")
   plt.savefig("twostream_particles.png")
   plt.close('all')

   field_file.close()
   red_particle_file.close()
   blu_particle_file.close()
