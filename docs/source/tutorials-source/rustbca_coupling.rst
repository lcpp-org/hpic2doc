RustBCA Coupling
======================

Problem Description
-------------------

RustBCA is a plasma-surface interactions code which hPIC2 optionally couples to through its
boundary conditions. It models the sputtering, reflection, and implantation processes
resulting from incident ion impacts.

In this problem, we consider a plasma made of the following species:

* Two Boris-Buneman uniform beam ion species, ``"H"`` and ``"B"``, with equal temperatures :math:`T_i`
* One Boltzmann electron population ``"e-"`` with temperature :math:`T_e`

Both boundaries are hydrogen-boron RustBCA walls. Incident particle interactions are simulated in RustBCA, 
where sputtered, reflected, and deposited particles are subsequently added or removed from the hPIC2 
particle list. The two ion populations interact electrostatically with each other and with the 
electrons, in addition to through electron impact ionization events. 

Theory
------

The binary-collision approximation assumes that when charged particles impact a material 
surface, they undergo a cascade of elastic binary collisions with the surface atoms while experiencing 
inelastic electronic stopping. Each cascade continues until the particle has either been reflected out of the simulation 
domain or become implanted in the surface by dropping below a defined cutoff energy. Additionally, collisions 
can dislodge surface atoms which can sputter out from the surface. 

Simulation Setup
----------------

* One-dimensional domain

* Uniform mesh

* Hydrogen-boron RustBCA wall boundaries

* Plasma density :math:`n_0 = 10^{18} \; [m^{-3}]`

* Number of computational particles = 100,000 hydrogen particles/population, 10,000 boron particles/population

* Plasma temperature: :math:`T_i = T_e = 10 \; [eV]`

Input File (TOML)
-----------------

.. literalinclude:: ../../../examples/rustbca_coupling.toml 
   :language: toml
   :lines: 1-

The mesh used in this example is ``type = "uniform"``.
The domain size :math:`L` was set to :math:`0.01 \; [m]`.
:math:`dx` is set such that there are 100 total elements, 
and is represented in the toml file as ``x1_elem_size = 1.0e-4``.

Time step is set to :math:`2e-9 \; [s]`, for 1000 total steps.

Three species are specified under ``[species]``: two ion populations, 
``"H"`` and ``"B"``; with an electron background ``"e+"``. ``"H"`` ions are set to a charge state of +1 with a density of
:math:`1e18 \; [m^{-3}]` and 100,000 computational particles. ``"B"`` ions are set to charge states +1 through +5 with
densities batween :math:`1e12 \; [m^{-3}]` and :math:`9e13 \; [m^{-3}]`, split between 10,000 computational particles.
These parameters are listed in the ``"charge_states"`` and ``"num_particles"`` blocks, respectively, under each ``[species]`` 
table.
``mass`` is the species mass. 
``type`` is the way which the species is represented or simulated. 

Two RustBCA wall boundaries are specified under the ``[[boundary_conditions]]`` subtables of each ``[species]`` table. 
Each boundary consists of both ``"H"`` and ``"B"``, and requires the cutoff and surface binding energies of the 
incident species as well as the density, cutoff energy, surface binding energy, and bulk binding energy of each wall species. 

The ``[interactions.electron_impact_ionization]`` tables define coefficients for electron impact ionizations between each 
``"boris_buneman"`` ion population and the ``"boltzmann"`` electron population.

Running 
-------

To run the simulation, use the following command:

.. code-block:: bash

   $ mpiexec -np 1 ./hpic2 -i rustbca_coupling.toml

The simulation will run for :math:`2e-6 \; [s]` over 1000 time steps,
and all outputs will be tagged with the ``rustbca_coupling`` prefix.

The standard output will show the simulation progress:

.. code-block:: bash

   $ mpiexec -np 1 ~/hpic2_dev/omp_opt_build/hpic2 -i rustbca_coupling.toml
   2023-05-18 14:23:45.282732 UTC-05:00     info [main] [mpi rank 0] starting simulation.
   2023-05-18 14:23:45.310319 UTC-05:00     info [ElectricFieldTridiag] [mpi rank 0] saving potential
   2023-05-18 14:23:45.310503 UTC-05:00     info [ElectricFieldTridiag] [mpi rank 0] saving E field
   2023-05-18 14:23:45.310627 UTC-05:00     info [ElectricFieldTridiag] [mpi rank 0] saving B field
   2023-05-18 14:23:45.310728 UTC-05:00     info [ElectricFieldTridiag] [mpi rank 0] saving electrostatic energy to rustbca_coupling_example_out/rustbca_coupling_ENERGY_ELECTROSTATIC.dat
   2023-05-18 14:23:45.314217 UTC-05:00     info [State] [mpi rank 0] At timestep 1
   2023-05-18 14:23:45.433586 UTC-05:00     info [State] [mpi rank 0] At timestep 2
   2023-05-18 14:23:45.555824 UTC-05:00     info [State] [mpi rank 0] At timestep 3
   2023-05-18 14:23:45.669392 UTC-05:00     info [State] [mpi rank 0] At timestep 4
   2023-05-18 14:23:45.800298 UTC-05:00     info [State] [mpi rank 0] At timestep 5
   2023-05-18 14:23:45.922554 UTC-05:00     info [State] [mpi rank 0] At timestep 6
   2023-05-18 14:23:46.054694 UTC-05:00     info [State] [mpi rank 0] At timestep 7
   2023-05-18 14:23:46.188037 UTC-05:00     info [State] [mpi rank 0] At timestep 8
   2023-05-18 14:23:46.321542 UTC-05:00     info [State] [mpi rank 0] At timestep 9
   2023-05-18 14:23:46.457601 UTC-05:00     info [State] [mpi rank 0] At timestep 10 

   ...


Plotting the results
---------------------

The simulation results are stored in the ``rustbca_coupling_example_out`` folder.
The output files are split between a particle file for each ion species, a general fields file, and a 
total electrostatic energy file. Their structures and 
naming conventions are described :ref:`here <input_deck:\`\`output_diagnostics\`\`>`.

You can visualize the results in multiple ways, for example 
using Python and the ``h5py`` package (follow instructions, etc.).

.. code-block:: python

   import h5py
   import matplotlib.pyplot as plt
   import numpy as np

   output_prefix = 'rustbca_coupling_example_out/rustbca_coupling_'

   # Reading field data
   fields_file = h5py.File(output_prefix+'fields.hdf','r')
   points = fields_file["VTKHDF/Points"][:,0]
   nsteps = fields_file["VTKHDF/Steps"].attrs["NSteps"]

   Efield = fields_file["VTKHDF/PointData/field_E"]
   Ex = np.reshape(Efield[:,0], (nsteps,-1))

   phi = fields_file["VTKHDF/PointData/field_phi"]
   phi = np.reshape(phi,(nsteps,-1))

   # Reading particle data
   H_particle_file = h5py.File(output_prefix+'H.h5part', 'r')
   B_particle_file = h5py.File(output_prefix+'B.h5part', 'r')

   Hx = H_particle_file["Step#20/x"]
   Bx = B_particle_file["Step#20/x"]

   # Plot the final electric field
   fig, ax = plt.subplots()
   ax.plot(points, Ex[-1,:], label = 'E_x')
   ax.legend()
   ax.set_xlabel('x')
   ax.set_ylabel('E')
   fig.savefig('rustbca_coupling_E.png')

   # Plot the final electric potential
   fig, ax = plt.subplots()
   ax.plot(points, phi[-1,:], label = 'phi')
   ax.legend()
   ax.set_xlabel('x')
   ax.set_ylabel('phi')
   fig.savefig('rustbca_coupling_phi.png')

   # Plot the final particle positions
   fig, ax = plt.subplots()
   ax.scatter(Hx, np.zeros_like(Hx), label = 'H')
   ax.scatter(Bx, np.zeros_like(Bx), label = 'B')
   ax.legend()
   ax.set_xlabel('x')
   ax.set_ylabel('y')
   fig.savefig('rustbca_coupling_particles.png')

   fields_file.close()
   H_particle_file.close()
   B_particle_file.close()
