Two-Stream Instability
======================

Problem Description
-------------------

Two-stream instability is one of the classical examples of beam-type instability that occurs in plasma physics. 
Streaming instabilities are a special case of instability whereby the thermal non-equilibrium
is caused by relative drift velocities between two plasma species.
In this problem, we consider the two-stream instability, which occurs when two populations of cold electrons,
each with number density :math:`n_0/2` and equal but opposite velocities :math:`\vec{v}_0 = \pm v_0 \hat{x}`,
interact electrostatically with each other and a stationary ion background with number density n0. 

Theory
------

The dispersion relation for the two-stream instability can be derived using linearized Vlasov-Poisson theory as

.. math::
   :label: TSI_dispersion_relation

   1 = \frac{1}{2} \omega_p^2 \left[ \frac{1}{\left(\omega - k v_0 \right)^2} + \left(\frac{1}{\omega - k v_0}\right)^2 \right],

Where :math:`\omega` and :math:`k` are respectively the angular frequency and wave-number of the unstable electrostatic wave,
:math:`\omega_p \approx n_e e^2/(m_e \epsilon_0)` 
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

   $ hpic2 --i twostream.toml
   [INFO] [2021-05-18 15:00:00] [twostream] [twostream.toml] [twostream]
   [INFO] [2021-05-18 15:00:00] [twostream] [twostream.toml] [twostream] Running simulation
   ...

Plotting the results
---------------------

The simulation results are stored in the ``twostream.h5`` file.
The ``twostream.h5`` file contains the following datasets:

* ``/fields``: contains the electric field :math:`\vec{E}` and electric potential :math:`\phi`.
* ``/particles``: contains the particle positions and velocities.

You can visualize the results in multiple ways, for example 
using Python and the ``h5py`` package (follow instructions, etc.).

.. code-block:: python

   import h5py
   import matplotlib.pyplot as plt
   import numpy as np

   f = h5py.File("twostream.h5", "r")

   # Plot the electric field
   fig, ax = plt.subplots()
   ax.plot(f["/fields/E/x"][:, 0], label="E_x")
   ax.plot(f["/fields/E/y"][:, 0], label="E_y")
   ax.plot(f["/fields/E/z"][:, 0], label="E_z")
   ax.legend()
   ax.set_xlabel("x")
   ax.set_ylabel("E")
   fig.savefig("twostream_E.png")

   # Plot the electric potential
   fig, ax = plt.subplots()
   ax.plot(f["/fields/phi"][:, 0], label="phi")
   ax.legend()
   ax.set_xlabel("x")
   ax.set_ylabel("phi")
   fig.savefig("twostream_phi.png")

   # Plot the particle positions
   fig, ax = plt.subplots()
   ax.scatter(f["/particles/e-_red/x"][:, 0], np.zeros_like(f["/particles/e-_red/x"][:, 0]), label="e-_red")
   ax.scatter(f["/particles/e-_blue/x"][:, 0], np.zeros_like(f["/particles/e-_blue/x"][:, 0]), label="e-_blue")
   ax.scatter(f["/particles/h+/x"][:, 0], np.zeros_like(f["/particles/h+/x"][:, 0]), label="h+")
   ax.legend()
   ax.set_xlabel("x")
   ax.set_ylabel("y")
   fig.savefig("twostream_particles.png")

   f.close()