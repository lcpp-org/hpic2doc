
Input decks
===========

A description of the problem to be simulated by hPIC2 is read from
external files, called input decks.
The following sections describe their format and available options.
A number of example input decks are provided in the ``examples`` directory.
New users are encouraged to find an example that mostly closely
resembles their desired problem and suitably modify it.

TOML
----

hPIC2 reads from input decks written in the
`TOML <https://toml.io/en/>`_
format.
The TOML format is intended to be a minimal, human-readable
configuration file format that is
unambiguously mappable to a hash table.
This makes generating hPIC2 inputs from scripts easier:
a large number of scripting languages have packages that support
conversion from hash tables to TOML files and back.

TOML's `full spec <https://toml.io/en/v1.0.0>`_ is fairly brief,
so this manual will not cover it in depth.
However, it is useful to mention a few features:


* TOML is built off of key/value pairs.
  In their simplest form, they comprise a key and value separated by an
  equals sign on a single, unique line:

  .. code-block:: toml

     key = "value"

* A set of key/value pairs is a table.
  An ordered list of values is an array.
  The value in a key/value pair can be any one of a number of POD types,
  a table,
  or an array.
* Arrays are defined by lists of values in square brackets:

  .. code-block:: toml

     array = ["value1", "value2", "value3"]

* A table is defined by a header, which is a key contained in
  square brackets on a unique line:

  .. code-block:: toml

     [table]
     key1 = "value1"
     key2 = "value2"

* Since values can be tables, it is valid to have an array of tables.
  Shorthand for defining these uses headers with the key of the array
  in double square brackets. The following defines an array
  ``tablearray`` which contains two tables,
  each of which contains two key/value pairs:

  .. code-block:: toml

     [[tablearray]]
     key1 = "value1"
     key2 = "value2"

     [[tablearray]]
     key3 = "value3"
     key4 = "value4"

* TOML specifies that TOML files should use the ``.toml`` file extension.
  Indentation is generally ignored, and is purely for aesthetics.

General structure of hPIC2 input decks
------------------------------------------

At the top level, an hPIC2 input deck must contain the following tables,
and no more:

``input_mode``
: Determines high-level operation modes for hPIC2.

``mesh``
: Defines the geometry of the domain and the mesh used for the field solve.

``time``
: Defines the time grid.

``species``
: Specifies the plasma species in the problem and their simulation models.

``magnetic_field``
: Describes the magnetic field to apply in the domain.

``electric_potential``
: Defines boundary conditions and numerical solver parameters for the
Poisson solver.

``output_diagnostics``
: Specifies the desired level and type of output during simulation.

``interactions``
: (Optional) Defines interactions between species.

Each of these tables contains key/value pairs which determine options
for the simulation.
Available options for each are described respectively in the following
sections.

Throughout this manual,
required datatypes for values are delimited by angled brackets.
If an option has a default value, it will be indicated in parentheses
within the datatype angled brackets.
In cases where values must take on one of a limited number of options,
the angle brackets will indicate this and
the description of the key will contain a table with the valid values.
For example,

  .. code-block:: toml

      required = #<integer>
      optional = #<float (0.5)>
      limited = #<options below>

indicates that the value of ``required`` must be a TOML integer and must
be provided by the user;
the value of ``optional`` must be a TOML float and can be omitted
from the input deck,
in which case it take the default value ``0.5``\ ;
and the value of ``limited`` must be one of a limited number of options.

There are many cases where selecting one option allows for
the selection of a new set of options.
For example, when the user desires a uniform mesh,
they must also provide options parametrizing the mesh.
Typically, the first option is specified as a simple key/value pair,
and then a separate table provides the selections for the new set of
options:

.. code-block:: toml

   [table]
   type = "type1"
       [table.type_specification]
       type1_option1 = 1.0
       type1_option2 = true

``input_mode``
--------------

The ``input_mode`` table specifies high-level options governing the running
mode of hPIC2.

.. code-block:: toml

   [input_mode]
   start_mode = #<options below>
   units = #<options below>
   simulation_tag = #<string>
   rng_seed = #<integer (default determined from current system time)>
   override_input_warnings = #<boolean (false)>

``start_mode``
: Currently must be set to ``"pic"``.

``units``
: Tells hPIC2 that all inputs are, and outputs should be, in the given
unit system. Currently only ``"si"`` is supported,
which specifies `SI <https://en.wikipedia.org/wiki/International_System_of_Units>`_ units.

``simulation_tag``
: A tag which is applied to all output to differentiate it from other simulations.

``rng_seed``
: A seed for all random number generation,
provide a capability for exact reproducibility.
If no seed is provided, a seed is generated from the current time.
Note that reproducibility is not anticipated if any level of parallelism
is used.

``override_input_warnings``
: If set to true, ignores warnings in the input deck that arise
due to the inclusion of unrecognized keys.

``mesh``
--------

The ``mesh`` table defines the problem domain and the mesh used for
the fields.

.. code-block:: toml

   [mesh]
   type = #<options below>
       [mesh.type_specification]
       #<options specific to mesh type>

Available types of meshes and type-specific options are described in
subsequent sections.

Uniform mesh
^^^^^^^^^^^^

The native uniform mesh allows for simple meshes of line segments
in one dimension and rectangular domains in two dimensions.
These meshes must use finite difference solvers.

..

   hPIC2 currently restricts 2D uniform meshes to have exactly square
   elements.


.. code-block:: toml

   [mesh]
   type = "uniform"
       [mesh.type_specification]
       # Specify two of the following three options
       #---------------------------------------------------------------------#
       x1_points = #[ <float>, <float> ]
       x1_elem_size = #<float>
       x1_num_elems = #<integer>
       #---------------------------------------------------------------------#

       # (Optional) For 2D meshes, specify two of the following three options
       # Omitting all of these options creates a 1D mesh
       #---------------------------------------------------------------------#
       x2_points = #[ <float>, <float> ]
       x2_elem_size = #<float>
       x2_num_elems = #<integer>
       #---------------------------------------------------------------------#

``x1_points``
: The first float defines the lower bound for the domain in the x1-direction. The second float defines the upper bound.

``x1_elem_size``
: Size of elements in the x1-direction.

``x1_num_elems``
: Number of elements in the x1-direction.

``x2_points``
: The first float defines the lower bound for the domain in the
x2-direction. The second float defines the upper bound.

``x2_elem_size``
: Size of elements in the x2-direction.

``x2_num_elems``
: Number of elements in the x2-direction.

pumiMBBL
^^^^^^^^

The `pumiMBBL <https://github.com/SCOREC/pumiMBBL>`_
(Multi-Block Boundary-Layer)
meshing utility allows for finite difference solvers
to be applied to complex, block-structured domains
with non-uniform meshes.
pumiMBBL can be used for both 1D and 2D problems.
This mesh is only available if hPIC2 was compiled with pumiMBBL support.

.. code-block:: toml

   [mesh]
   type = "pumi"
       [mesh.type_specification]
       domain_min_points = #<array of float>
           [[mesh.type_specification.x1_blocks]]
           submesh_type = #<options below>
           #<further options specific to submesh type>

           [[mesh.type_specification.x2_blocks]]
           submesh_type = #<options below>
           #<further options specific to submesh type>

``domain_min_points``
: An array of length either 1 or 2,
which determines the number of dimensions in the mesh.
Provides the lower bounds in the x1- and (if length 2) x2-directions.

``x1_blocks`` and ``x2_blocks`` are arrays of tables.
Each table defines a submesh or block in the corresponding direction.
The entire mesh is construced as a tensor product of the blocks in both
directions.
The available available submesh types are:

``"minBL"``
: A block whose element size increases as x1 (or x2, as applicable) increases.

``"maxBL"``
: A block whose element size decreases as x1 (or x2, as applicable) increases.

``"uniform"``
: A block with uniform element sizing.

``"arbitrary"``
: A block with arbitrary element sizing.

Further options for each of these types are described in the following
sections.

``"minBL"``
~~~~~~~~~~~

.. code-block:: toml

   [[mesh.type_specification.x1_blocks]]
   submesh_type = "minBL"
   length = #<float>
   max_elem_size = #<float>
   min_elem_size = #<float>

``length``
: Length of the block.

``max_elem_size``
: Length of the largest element in the block.

``min_elem_size``
: Length of the smallest element in the block.

``"maxBL"``
~~~~~~~~~~~

.. code-block:: toml

   [[mesh.type_specification.x1_blocks]]
   submesh_type = "minBL"
   length = #<float>
   max_elem_size = #<float>
   min_elem_size = #<float>

``length``
: Length of the block.

``max_elem_size``
: Length of the largest element in the block.

``min_elem_size``
: Length of the smallest element in the block.

``"uniform"``
~~~~~~~~~~~~~

.. code-block:: toml

   [[mesh.type_specification.x1_blocks]]
   submesh_type = "minBL"
   length = #<float>
   elem_size = #<float>

``length``
: Length of the block.

``elem_size``
: Length of the each element in the block.
Must divide ``length``.

``"arbitrary"``
~~~~~~~~~~~~~~~

.. code-block:: toml

   [[mesh.type_specification.x1_blocks]]
   submesh_type = "arbitrary"
   length = #<float>
   elem_size_file = #<string>

``length``
: Length of the block.

``elem_size_file``
: Path to file from which to read element sizes.
These should be ASCII files containing a list of element sizes
separated by newlines.
The sum of these element sizes should be equal to ``length`` to
within a 0.1% relative error.

MFEM
^^^^

`MFEM <https://mfem.org/>`_
is a scalable library for finite element methods,
which allows the use of unstructured meshes in complex domains.
This mesh is only available if hPIC2 was compiled with MFEM support.

.. code-block:: toml

   [mesh]
   type = "mfem"
       [mesh.type_specification]
       mesh_filename = #<string>

``mesh_filename``
: Path to a mesh file.
MFEM supports a number of common mesh `formats <https://mfem.org/mesh-formats/>`_.
hPIC2 requires that the mesh be a conforming mesh comprising a single element type
with flat faces in two or three dimensions.
Adaptive mesh refinement is not supported.
Currently, hPIC2 requires that the mesh has not been decomposed prior to
the simulation;
hPIC2 performs the mesh decomposition for distributed runs.
Similarly, hPIC2 requires that the mesh is not periodic.

Uniform MFEM
^^^^^^^^^^^^

If hPIC2 was compiled with MFEM support,
a uniform finite element mesh can be quickly generated from the input deck
without the need for external meshing software.
Triangular and tetrahedral meshes are formed from quadrilateral
and hexahedral meshes by splitting elements into two triangles
in 2D and six tetrahedra in 3D.

.. code-block:: toml

   [mesh]
   type = "mfem_uniform"
       [mesh.type_specification]
       type = #<string>
       nx1 = #<integer>
       sx1 = #<float>
       nx2 = #<integer>
       sx2 = #<float>
       # Below is optional, but both must be specified if either one is present
       nx3 = #<integer>
       sx3 = #<float>

``type``
: Type of mesh element. Acceptable options are ``"quadrilateral"`` or ``"triangle"`` in 2D and ``"tetrahedron"`` or ``"hexahedron"`` in 3D.
For triangular meshes, the total number of elements is ``2 * nx1 * nx2``\ ;
for quadrilateral meshes, the total number of elements is ``nx1 * nx2``\ ;
for tetrahedral meshes, the total number of elements is ``6 * nx1 * nx2 * nx3``\ ;
for hexahedral meshes, the total number of elements is ``nx1 * nx2 * nx3``.

``nx1``
: Number of mesh edges in the x1-direction.

``sx1``
: Length of the domain in the x1-direction.

``nx2``
: Number of mesh edges in the x2-direction.

``sx2``
: Length of the domain in the x2-direction.

``nx3``
: Number of mesh edges in the x3-direction.
Generates a 3D mesh.
``sx3`` must also be specified if this is provided.
Otherwise, a 2D mesh is generated.

``sx3``
: Length of the domain in the x3-direction.
Generates a 3D mesh.
``nx3`` must also be specified if this is provided.
Otherwise, a 2D mesh is generated.

``time``
--------

The ``time`` table governs the time discretization.
hPIC2 does not support adaptive time stepping.
Hence, an hPIC2 time grid consists of an interval of time,
assumed to start at 0,
that is uniformly partitioned.

.. code-block:: toml

   [time]
   # Specify two of the following three options
   num_time_steps = #<integer>
   dt = #<float>
   termination_time = #<float>
   # Optional, only valid when built with MFEM and with at least one fluid species.
   fluid_integrator = #<options below ("ForwardEulerSolver")>
       [time.fluid_integrator_params]
       #<options specific to fluid integrator>

``num_time_steps``
: Number of time steps into which the simulation should be partitioned.

``dt``
: Length of time step to use.

``termination_time``
: Length of total simulation time.

``fluid_integrator``
: ODE integrator used to integrate fluid species.
Some integrators require additional parameters.
Options are described in the table below,
and additional parameters for each one will be described in subsequent sections.

.. list-table::
   :header-rows: 1

   * - Integrator
     - Description
   * - ``"ForwardEulerSolver"``
     - Forward Euler integrator. First order. No parameters required.
   * - ``"RK2Solver"``
     - Explicit, two-stage Runge-Kutta integrator. Second order. Parameters described below.
   * - ``"RK3SSPSolver"``
     - Explicit, three-stage, strong stability preserving Runge-Kutta integrator. Third order. No parameters required.
   * - ``"RK4Solver"``
     - Classic Runge-Kutta method. Fourth order. No parameters required.
   * - ``"RK6Solver"``
     - Explicit, six-stage Runge-Kutta method. No parameters required.


RK2 parameters
^^^^^^^^^^^^^^^

The user is able to specify the parameter for generic RK2 methods.

.. code-block:: toml

   [time.fluid_integrator_params]
   a = #<float>

``a``
: Exposes the RK2 parameter.
``0.5`` corresponds to the explicit midpoint method;
``0.666667`` corresponds to Ralston's method;
``1.0`` corresponds to Heun's method.

``species``
-----------

The ``species`` table governs the list of plasmas species that will be
simulated.
It is unique in that its contents are tables themselves,
each of which has a unique user-provided key that is used to name
the species and tag all output for that species.

.. code-block:: toml

   [species.<string>]
   mass = #<float>
   type = #<options below>
       [species.<string>.type_params]
       #<options specific to species type>

``mass``
: Mass of individual particles of this species.

Available types and type-specific options are provided in the following sections.

Full orbit, Boris-Buneman
^^^^^^^^^^^^^^^^^^^^^^^^^^

This type models the species with a PIC method,
using the Boris-Buneman time integrator to push the particles.
The "full orbit" modifier refers to the fact that particle trajectories
are tracked in the full six-dimensional phase space,
as opposed to five dimensions as in a gyrokinetic model.
This type is the workhorse of kinetic plasma modeling in hPIC2.

.. code-block:: toml

   [species.<string>]
   mass = #<float>
   type = "boris_buneman"
       [species.<string>.type_params]
       atomic_number = #<integer (0)>
       initial_condition = #<options below>
           [species.<string>.type_params.initial_condition_params]
           #<options specific to initial condition type>

           [[species.<string>.type_params.boundary_conditions]]
           boundary = #<integer or alias>
           type = #<options below>
               [species.<string>.type_params.boundary_conditions.type_params]

           [[species.<string>.type_params.volumetric_sources]]
           type = #<options below>
           #<more options specific to volumetric source type>

``atomic_number``
: Atomic number of the species.
For electrons or other species where there is no notion of atomic number,
this can typically be safely omitted.

Each full orbit species must specify exactly one initial condition.
Available options are described in subsequent sections.

``boundary_conditions`` is an array of tables whose length must be equal
to the number of boundaries in the mesh.
The ``boundary`` key must be paired with a unique positive integer boundary ID.
For uniform meshes and pumi meshes without inactive blocks,
the aliases ``"west"``\ , ``"east"``\ , ``"north"``\ , and ``"south"`` can be used instead
of integers in the corresponding directions.
In all other cases, the value of ``boundary`` must be a boundary ID that
exists in the mesh.

``volumetric_sources`` is an array of tables, each of which adds a volumetric
particle source to the simulation.
It is not necessary to have any sources, and the array can be completely
omitted if no sources are desired.

Uniform beam initial condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This initial condition distributes particles uniformly in space,
according to a drifting Maxwellian distribution in velocity space.

.. code-block:: toml

   initial_condition = "uniform_beam"
       [species.<string>.type_params.initial_condition_params]
       # Choose one of the following
       #------------------------------------------------------------------------#
       num_particles = #<integer>
       weight = #<float>
       #------------------------------------------------------------------------#

       flow_velocity_1 = #<float>
       flow_velocity_2 = #<float>
       flow_velocity_3 = #<float>

       # Specify temperature in each direction at once,
       # or isotropic temperature,
       # or omit temperature entirely for zero temperature.
       #------------------------------------------------------------------------#
       temperature_1 = #<float>
       temperature_2 = #<float>
       temperature_3 = #<float>
       #------------------------------------------------------------------------#
       temperature = #<float>
       #------------------------------------------------------------------------#

           [[species.<string>.type_params.initial_condition_params.charge_states]]
           charge_number = #<integer>
           density = #<float>

``num_particles``
: Number of macroparticles to populate throughout the mesh.
Particle weight is computed from this and the total number of physical particles
in the domain.
If this is set to zero, and the ``charge_states`` array is empty
or contains only populations whose ``density`` are zero,
no particles are populated.

``weight``
: Weight of each macroparticle.
Number of macroparticles is computed from this and the total number of
physical particles in the domain.

``flow_velocity_1``
: Average, bulk, or flow velocity of the drifting Maxwellian distribution in
the x1-direction.

``flow_velocity_2``
: Average, bulk, or flow velocity of the drifting Maxwellian distribution in
the x2-direction.

``flow_velocity_3``
: Average, bulk, or flow velocity of the drifting Maxwellian distribution in
the x3-direction.

``temperature_1``
: Temperature of drifting Maxwellian distribution in the x1-direction.

``temperature_2``
: Temperature of drifting Maxwellian distribution in the x2-direction.

``temperature_3``
: Temperature of drifting Maxwellian distribution in the x3-direction.

``temperature``
: Isotropic temperature of drifting Maxwellian distribution from which
to sample particle velocities.

``charge_states`` is an array of tables,
each of which corresponds to a population of particles with a desired charge.
If ``num_particles`` was previously set to zero and
this array is empty or contains only populations with zero ``density``\ ,
no particles are created.

``charge_number``
: Charge number of particles of this population.
The charge of particles is the product of this and the elementary charge.
Negative integer values are allowed,
corresponding to anions, electrons, or other negatively charged particles.
This must not exceed the previously defined ``atomic_number``.

``density``
: Number density of particles of this population.

Initial condition from file
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This initial condition populates particles according to a drifting
Maxwellian distribution in velocity space,
but with number density, temperature, and flow velocity that
can vary in space.
These parameters are read from file as nodal fields.

.. code-block:: toml

   initial_condition = "from_file"
       [species.<string>.type_params.initial_condition_params]
       num_particles = #<integer>
       charge_number = #<integer>
       density_filename = #<string>
       flow_velocity_filename = #<string>
       temperature_filename = #<string>

``num_particles``
: Total number of macroparticles used to discretize this species.

``charge_number``
: Charge number of particles.

``density_filename``
: Path to file specifying the number density at each node.
The file format should be a simple space-separated value format
with exactly one floating point value on each line.
Each line in the file corresponds to the node of the same index.
If there are fewer lines in the file than there are nodes,
the number density is assumed to be zero on remaining nodes;
if, on the other hand, there are more lines in the file than there are
nodes,
extra lines are ignored.
If the simulation uses more than one MPI process and a distributed mesh
(for example, MFEM),
local node orderings differ on each process.
Hence, each MPI process appends ``.<rank>`` to the end of the given filename
and attempts to read from that file.
The user must ensure that all such files exist and that
the number of lines in each file is equal to the number of local
nodes on each corresponding MPI process.

``flow_velocity_filename``
: Path to file specifying flow (or average or bulk) velocity at each node.
The file format is identical to that of the number density
except that each line must have three space-separated floating point
values,
specifying each of the three velocity components.
The same file rules apply.

``temperature_filename``
: Path to file specifying the temperature at each node.
The file format is identical to that of the number density.
The same file rules apply.

Periodic boundary condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Periodic boundaries always come in pairs.
A periodic boundary condition is associated with a measure-preserving
diffeomorphism between the boundaries.
When a particle is incident on a periodic boundary,
its position and velocity are updated according to the periodic mapping
between the boundaries.
hPIC2 currently only supports periodic mappings
in cardinal directions,
i.e. purely in one of the x1-, x2-, or x3-directions.
Note that if one boundary is marked as periodic,
the boundary to which it is mapped must also be periodic;
hPIC2 does not attempt to intuit periodic mappings.
See the ``examples`` directory for examples of use.

..

   Periodic boundaries are not supported for pumi or MFEM meshes.


.. code-block:: toml

   [[species.<string>.type_params.boundary_conditions]]
   boundary = #<integer or alias>
   type = "periodic"

The ``type_params`` subtable is not required for periodic boundaries
and should be omitted.

Absorbing boundary condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a particle is incident on an absorbing boundary,
it is removed from the simulation.

.. code-block:: toml

   [[species.<string>.type_params.boundary_conditions]]
   boundary = #<integer or alias>
   type = "absorbing"

The ``type_params`` subtable is not required for absorbing boundaries
and should be omitted.

Reflecting boundary condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a particle is incident on a reflecting boundary,
its velocity is reflected off of the boundary.
Reflecting boundaries are assumed to be perfectly reflecting,
so that no portion of the macroparticle is absorbed by the boundary.

.. code-block:: toml

   [[species.<string>.type_params.boundary_conditions]]
   boundary = #<integer or alias>
   type = "reflecting"

The ``type_params`` subtable is not required for reflecting boundaries
and should be omitted.

RustBCA boundary condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`RustBCA <https://github.com/lcpp-org/RustBCA>`_
models the effects of ion impacts on materials.
All particles incident on a RustBCA boundary are collected over the course of a
time step,
and then a RustBCA simulation is performed.
The RustBCA simulation models sputtering, implantation, and reflection.
Sputtered and reflected particles are then returned to the hPIC2 simulation
for the next time step with zero charge.
The RustBCA boundary supports compound, or multi-component, targets.
This capability is effected by RustBCA's
`C bindings <https://github.com/lcpp-org/RustBCA/wiki/Bindings:-C>`_.

RustBCA requires the cutoff energy and surface binding energy
of the incident species
and the number density, cutoff energy,
surface binding energy,
and bulk binding energy
of each of the target species that compose the boundary.

.. code-block:: toml

   [[species.<string>.type_params.boundary_conditions]]
   boundary = #<integer or alias>
   type = "rust_bca"
       [species.<string>.type_params.boundary_conditions.type_params]
       incident_species_cutoff_energy = #<float>
       incident_species_surface_binding_energy = #<float>
           [[species.<string>.type_params.boundary_conditions.type_params.targets]]
           species = #<string>
           wall_density = #<float>
           cutoff_energy = #<float>
           surface_binding_energy = #<float>
           bulk_binding_energy = #<float>

``incident_species_cutoff_energy``
: Cutoff energy of incident species.

``incident_species_surface_binding_energy``
: Surface binding energy of incident species.

``targets`` is an array of tables, each of which corresponds to a component
of the boundary.
The array must contain at least one target.

``species``
: Name of the target species in hPIC2.
This must correspond to an existing ``"boris_buneman"`` species defined
elsewhere in the input deck.
New sputtered particles will be created in this species.
It is common to initialize this species with zero particles
in order to model pure sputtering.

``wall_density``
: Number density of target species in the boundary.

``cutoff_energy``
: Cutoff energy of target species.

``surface_binding_energy``
: Surface binding energy of target species.

``bulk_binding_energy``
: Bulk binding energy of target species.

Minimum mass volumetric source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A useful feature of hPIC was the ability to populate particles each time step
in order to maintain a constant average number density.
This is equivalent to adding sufficiently many particles per time step
in order to maintain a minimum total mass of a given species.
This capability is referred to in hPIC2 as the minimum mass source.
At the end of each time step, the number of particles is counted,
and if it is less than the initial number of particles,
sufficiently many particles are added to maintain at least the initial number
of particles.
This is done on a per-charge state basis,
meaning that the number of particles of each charge state is counted
and replenished.
Particles are generated uniformly in space,
according to a drifting Maxwellian distribution in velocity space.

.. code-block:: toml

   [[species.<string>.type_params.volumetric_sources]]
   type = "minimum_mass"
   flow_velocity_1 = #<float (0.0)>
   flow_velocity_2 = #<float (0.0)>
   flow_velocity_3 = #<float (0.0)>

   # Specify temperature in each direction at once,
   # or isotropic temperature,
   # or omit temperature entirely for zero temperature.
   #--------------------------------------------------------------------------#
   temperature_1 = #<float>
   temperature_2 = #<float>
   temperature_3 = #<float>
   #--------------------------------------------------------------------------#
   temperature = #<float>
   #--------------------------------------------------------------------------#

``flow_velocity_1``
: Average, bulk, or flow velocity of the drifting Maxwellian distribution in
the x1-direction.

``flow_velocity_2``
: Average, bulk, or flow velocity of the drifting Maxwellian distribution in
the x2-direction.

``flow_velocity_3``
: Average, bulk, or flow velocity of the drifting Maxwellian distribution in
the x3-direction.

``temperature_1``
: Temperature of drifting Maxwellian distribution in the x1-direction.

``temperature_2``
: Temperature of drifting Maxwellian distribution in the x2-direction.

``temperature_3``
: Temperature of drifting Maxwellian distribution in the x3-direction.

``temperature``
: Isotropic temperature of drifting Maxwellian distribution from which
to sample particle velocities.

Minimum mass volumetric source, spatially varying source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This replicates the original minimum-mass volumetric source,
but allows the user to define a probability density function
in space for new particles,
along with spatially-varying temperature and flow velocity.
The probability density function,
temperature,
and flow velocity are all specified as nodal fields.

.. code-block:: toml

   [[species.<string>.type_params.volumetric_sources]]
   type = "minimum_mass_from_file"
   profile_filename = #<string>
   flow_velocity_filename = #<string>
   temperature_filename = #<string>

``profile_filename``
: Path to file specifying the probability density function
for new particles at each node.
The file format should be a simple space-separated value format
with exactly one floating point value on each line.
The PDF does not need to be normalized;
hPIC2 internally normalizes the PDF.
Notably, when paired with the ``"from_file"`` initial condition,
this allows a user to provide ``density_filename`` of the initial condition
for this PDF.
Each line in the file corresponds to the node of the same index.
If there are fewer lines in the file than there are nodes,
the PDF is assumed to be zero on remaining nodes;
if, on the other hand, there are more lines in the file than there are
nodes,
extra lines are ignored.
If the simulation uses more than one MPI process and a distributed mesh
(for example, MFEM),
local node orderings differ on each process.
Hence, each MPI process appends ``.<rank>`` to the end of the given filename
and attempts to read from that file.
The user must ensure that all such files exist and that
the number of lines in each file is equal to the number of local
nodes on each corresponding MPI process.

``flow_velocity_filename``
: Path to file specifying flow (or average or bulk) velocity at each node.
The file format is identical to that of the PDF
except that each line must have three space-separated floating point
values,
specifying each of the three velocity components.
The same file rules apply.

``temperature_filename``
: Path to file specifying the temperature at each node.
The file format is identical to that of the PDF.
The same file rules apply.

Boltzmann electrons
^^^^^^^^^^^^^^^^^^^^^

To step over typical electron thermalization timescales,
hPIC2 can assume that the electrons follow a Maxwell-Boltzmann distribution.
This augments the potential solve with a nonlinear term,
but means that the electrons themselves do not need to be explicitly evolved.
At most one Boltzmann electron species is allowed.

.. code-block:: toml

   [species.<string>]
   type = "boltzmann"
       [species.<string>.type_params]
       temperature = #<float (0.0)>
       charge_conservation_scheme = #<options below ("hagelaar")>

``temperature``
: Temperature of the electrons.

``charge_conservation_scheme``
: Scheme used to update the electron reference density. There are two options:
``"hagelaar"``\ , the default, which is fast but physically limited to problems
with static boundary conditions for the electric potential;
and ``"elias"``\ , which is somewhat slow but is better suited to more general
problems.

..

   The ``"elias"`` charge conservation scheme currently only works for 1D problems.


Uniform charge background
^^^^^^^^^^^^^^^^^^^^^^^^^^

This species adds a uniform charge density to the electric potential solve.
The species is assumed to be uniform and static.

.. code-block:: toml

   [species.<string>]
   mass = #<float>
   type = "uniform_background"
       [species.<string>.type_params]
       charge_number = #<integer>
       density = #<float>

``charge_number``
: Charge number for this species.
The charge of each particle is taken as the product of this and the
elementary charge.

``density``
: Number density of this species.

MFEM Euler Fluid
^^^^^^^^^^^^^^^^^

This models the species with the compressible Euler equations.
The Euler equations are discretized using a
discontinuous Galerkin (DG) formulation.
Momentum density components in three dimensions are tracked regardless
of mesh dimensionality.
This is commensurate with the full orbit particle velocity tracking strategy.

..

   This type only works with MFEM meshes.


.. code-block:: toml

   [species.<string>]
   mass = #<float>
   type = "mfem_euler_fluid"
       [species.<string>.type_params]
       charge_number = #<integer>
       gamma = #<float>
       order = #<integer>
       riemann_solver = #<options below>
       initial_condition = #<options below>
           [species.<string>.type_params.initial_condition_params]
           #<options specific to initial condition type>

           [[species.<string>.type_params.boundary_conditions]]
           boundary = #<integer>
           type = #<options below>
               [species.<string>.type_params.boundary_conditions.type_params]
               #<options specific to boundary condition type>

           [[species.<string>.type_params.volumetric_sources]]
           type = #<options below>
               [species.<string>.type_params.volumetric_sources.volumetric_source_params]
               #<options specific to volumetric source type>

``charge_number``
: Charge number for this species.
The charge of this species is computed as the product of this and the
elementary charge.
Set to 0 for a neutral fluid.

``gamma``
: The adiabatic index or specific heat ratio of the species.
Generally, for monatomic species, this should be 5/3;
for diatomic species (which approximates air), 7/5 is appropriate.

``order``
: The order of DG polynomial interpolation.
To some extent, solution fidelity can be maintained in coarse meshes by
compensating with a higher polynomial order.

``riemann_solver``
: Numerical fluxes at element interfaces are computed by approximately solving
a Riemann problem.
This option selects a Riemann solver to use for this calculation.
The table below lists the options and some notes.

.. list-table::
   :header-rows: 1

   * - Riemann solver option
     - Description
   * - ``"rusanov"``
     - Solver from Rusanov. Also known as local Lax-Friedrichs. Extremely robust.
   * - ``"hll"``
     - Harten-Lax-van Leer. Sometimes more accurate than Rusanov.


``initial_condition``
: Specifies the initial fluid state throughout the computational domain.
Options will be described in subsequent sections.

``boundary_conditions``
: An array of tables whose length must be equal
to the number of boundaries in the mesh.
The ``boundary`` key must be paired with a unique positive integer boundary ID.

``volumetric_sources``
: An array of tables, each of which adds a volumetric
particle source to the simulation.
It is not necessary to have any sources, and the array can be completely
omitted if no sources are desired.
Options will be described in subsequent sections.

Uniform beam initial condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like the uniform beam initial condition for full orbit particles,
this sets the initial state to have uniform density,
bulk velocity, and temperature throughout the computational domain.
Although hPIC2 internally uses so-called conservative variables for
its Euler equation formulation,
the user specifies the initial fluid state in primitive variables for
convenience.

.. code-block:: toml

   initial_condition = "uniform_beam"
       [species.<string>.type_params.initial_condition_params]
       density = #<float>
       flow_velocity_1 = #<float>
       flow_velocity_2 = #<float>
       flow_velocity_3 = #<float>
       temperature = #<float>

``density``
: Number density.

``flow_velocity_1``
: Average, bulk, or flow velocity in the x1-direction.

``flow_velocity_2``
: Average, bulk, or flow velocity in the x2-direction.

``flow_velocity_3``
: Average, bulk, or flow velocity in the x3-direction.

``temperature``
: Temperature.

RTC initial condition
~~~~~~~~~~~~~~~~~~~~~

A spatially dependent initial condition can be specified using the
RTC language from Trilinos' PAMGEN package.

..

   The RTC initial condition is only available if RTC is enabled.


.. code-block:: toml

   initial_condition = "rtc"
       [species.<string>.type_params.initial_condition_params]
       function_body = #<string>

``function_body``
: The body of a function in the RTC language.
The RTC language is essentially a subset of C++.
For more information, see the Trilinos/PAMGEN documentation on the RTC
language.
Within the function body, the variables ``x1``\ , ``x2``\ , and ``x3``
store the coordinates.
The output variables ``density``\ ,
``flow_velocity_1``\ ,
``flow_velocity_2``\ ,
``flow_velocity_3``\ ,
and ``temperature`` should be set to
the desired initial number density,
flow velocity,
and temperature at the given coordinates.
That is, the user should treat the ``function_body`` as the body
of a C++ function like

.. code-block:: c++

   void evalInitialCondition(
       const double x1,
       const double x2,
       const double x3,
       double &density,
       double &flow_velocity_1,
       double &flow_velocity_2,
       double &flow_velocity_3,
       double &temperature
   ) {
       // function_body here
   }

Since the RTC language ignores most whitespace like C++,
it is suggested that the user exploit the triple quoted string
in the TOML spec:

.. code-block:: toml

   function_body = """
       // function_body here
   """

Reflecting boundary condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Models an impermeable wall.

.. code-block:: toml

   [[species.<string>.type_params.boundary_conditions]]
   boundary = #<integer>
   type = "reflecting"

The ``type_params`` subtable is not required for reflecting boundaries
and should be omitted.

Copy-out boundary condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Outflow boundaries are notoriously difficult to numerically model
with the Euler equations.
A cheap approximation is to copy the fluid state just on the inside of
the boundary to the outside in order to compute a numerical flux.

.. code-block:: toml

   [[species.<string>.type_params.boundary_conditions]]
   boundary = #<integer>
   type = "copy_out"

The ``type_params`` subtable is not required for copy-out boundaries
and should be omitted.

Far-field boundary condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This boundary condition approximates contact with a fluid reservoir
with a constant and uniform state.

.. code-block:: toml

   [[species.<string>.type_params.boundary_conditions]]
   boundary = #<integer>
   type = "far_field"
       [species.<string>.type_params.boundary_conditions.type_params]
       density = #<float>
       flow_velocity_1 = #<float>
       flow_velocity_2 = #<float>
       flow_velocity_3 = #<float>
       temperature = #<float>

``density``
: Number density of fluid reservoir.

``flow_velocity_1``
: First component of bulk, average, or flow velocity of fluid reservoir.

``flow_velocity_2``
: Second component of bulk, average, or flow velocity of fluid reservoir.

``flow_velocity_3``
: Third component of bulk, average, or flow velocity of fluid reservoir.

``temperature``
: Temperature of fluid reservoir.

No-flux boundary condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sets the flux of all fluid state variables to zero across the boundary.
Despite the name, this does not accurately represent an impermeable wall
or reflecting boundary.
It rarely behaves as one would expect and should generally be avoided unless
the user has a specific reason to use it.
Notably, because its implementation is faster than any other boundary condition,
it can be useful for modeling supersonic outflow.

.. code-block:: toml

   [[species.<string>.type_params.boundary_conditions]]
   boundary = #<integer>
   type = "no_flux"

The ``type_params`` subtable is not required for no-flux boundaries
and should be omitted.

RTC volumetric source
~~~~~~~~~~~~~~~~~~~~~

The RTC language from Trilinos' PAMGEN package
can be used to specify space- and time-dependent source terms
for the Euler equations.

..

   The RTC initial condition is only available if RTC is enabled.


.. code-block:: toml

   [[species.<string>.type_params.volumetric_sources]]
   type = "rtc"
       [species.<string>.type_params.volumetric_sources.volumetric_source_params]
       function_body = #<string>

``function_body``
: The body of a function in the RTC language.
The RTC language is essentially a subset of C++.
For more information, see the Trilinos/PAMGEN documentation on the RTC
language.
Within the function body, the variables ``x1``\ , ``x2``\ , and ``x3``
store the coordinates,
and the ``t`` variable stores the current simulation time.
The output variables ``drhodt``\ ,
``dp1dt``\ ,
``dp2dt``\ ,
``dp3dt``\ ,
and ``drho_Edt`` should be set to
the desired source for the
mass density,
momentum density,
and total energy density at the given coordinates and time, respectively.
That is, the user should treat the ``function_body`` as the body
of a C++ function like

.. code-block:: c++

   void evalSource(
       const double t,
       const double x1,
       const double x2,
       const double x3,
       double &drhodt,
       double &dp1dt,
       double &dp2dt,
       double &dp3dt,
       double &drho_Edt
   ) {
       // function_body here
   }

Since the RTC language ignores most whitespace like C++,
it is suggested that the user exploit the triple quoted string
in the TOML spec:

.. code-block:: toml

   function_body = """
       // function_body here
   """

``magnetic_field``
------------------

The ``magnetic_field`` table governs the specification of the externally-applied
magnetic (B) field.

.. code-block:: toml

   [magnetic_field]
   type = #<options below>
       [magnetic_field.type_params]
       #<options specific to mesh type>

Available magnetic field types are described in the following sections.

Uniform magnetic field
^^^^^^^^^^^^^^^^^^^^^^^^

The uniform magnetic field applies a magnetic field that is constant in space
and time.

.. code-block:: toml

   [magnetic_field]
   type = "uniform"
       [magnetic_field.type_params]
       b1 = #<float>
       b2 = #<float>
       b3 = #<float>

``b1``
: x1-component of the magnetic field.

``b2``
: x2-component of the magnetic field.

``b3``
: x3-component of the magnetic field.

Magnetic field from file
^^^^^^^^^^^^^^^^^^^^^^^^^^

Allows the user to apply a magnetic field that is constant in time,
but varies in space.
The magnetic field is specified as a nodal field.

.. code-block:: toml

   [magnetic_field]
   type = "from_file"
       [magnetic_field.type_params]
       filename = #<string>

``filename``
: Path to file specifying the magnetic field at each node.
The file format should be a simple space-separated value format
with exactly three floating point values on each line,
specifying the three vector components.
Each line in the file corresponds to the node of the same index.
If there are fewer lines in the file than there are nodes,
the magnetic field is assumed to be zero on remaining nodes;
if, on the other hand, there are more lines in the file than there are
nodes,
extra lines are ignored.
If the simulation uses more than one MPI process and a distributed mesh
(for example, MFEM),
local node orderings differ on each process.
Hence, each MPI process appends ``.<rank>`` to the end of the given filename
and attempts to read from that file.
The user must ensure that all such files exist and that
the number of lines in each file is equal to the number of local
nodes on each corresponding MPI process.

``electric_potential``
----------------------

The ``electric_potential`` table governs the behavior of the potential solver
and its boundary conditions.

.. code-block:: toml

   [electric_potential]
   poisson_solver = #<options below>
       [electric_potential.solver_params]
       #<options specific to solver>

       [[electric_potential.boundary_conditions]]
       boundary = #<integer or alias>
       type = #<options below>
       function = #<options below>
           [electric_potential.boundary_conditions.function_params]
           #<options specific to function>

``poisson_solver``
: The solver to use for the field solve.
Certain solvers are compatible with only specific meshes
or are not compatible with Boltzmann electrons.
The tables below show the available solvers
and their compatibility with various meshes and Boltzmann electrons.
An X indicates that the solver works with that mesh with Boltzmann electrons,
and O indicates that the solver works with that mesh without Boltzmann electrons,
and no symbol indicates that the mesh is completely incompatible.

.. list-table::
   :header-rows: 1

   * - Solver\Mesh
     - 1D uniform
     - 2D uniform
     - 1D pumi
     - 2D pumi
     - MFEM
   * - ``"hockney"``
     - O
     -
     -
     -
     -
   * - ``"tridiag"``
     - X
     -
     - X
     -
     -
   * - ``"hypre"``
     - X
     - X
     - X
     - X
     -
   * - ``"mfem"``
     -
     -
     -
     -
     - X


Further details about each of the solvers is provided in subsequent sections.

``boundary_conditions`` is an array of tables whose length must be equal
to the number of boundaries in the mesh.
The ``boundary`` key must be paired with a unique positive integer boundary ID.
For uniform meshes and pumi meshes without inactive blocks,
the aliases ``"west"``\ , ``"east"``\ , ``"north"``\ , and ``"south"`` can be used instead
of integers in the corresponding directions.
In all other cases, the value of ``boundary`` must be a boundary ID that
exists in the mesh.
Available boundary condition types and functions are described in
subsequent sections.

Hockney solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Hockney solver is a fast direct solver for
uniform meshes of 1D domains with periodic boundary conditions.
It therefore must be paired with periodic boundary conditions on either
side of the domain.
Although it is absolutely fast, it is not parallelized and not scalable.
Users should therefore consider using the hypre solver for
extremely large 1D problems with periodic boundary conditions.

There are no solver options for the Hockney solver,
so the ``solver_params`` subtable should be omitted.

Tridiag solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The tridiag solver is a fast direct solver for
1D domains with at least one Dirichlet boundary condition.
Although it is absolutely fast, it is not parallelized and not scalable.
Users should therefore consider using the hypre solver for
extremely large 1D problems with periodic boundary conditions.

There are no solver options for this solver,
so the ``solver_params`` subtable should be omitted.

Hypre solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The
`hypre <https://hypre.readthedocs.io/en/latest/#>`_
solver uses hypre's
`struct <https://hypre.readthedocs.io/en/latest/ch-struct.html>`_
interface to solve for the potential in uniform and block-structured meshes.
hPIC2 uses hypre's BiCGSTAB solver,
which is a Krylov solver that exhibits good scalability on large problems
with RF boundary conditions.

..

   Currently, with the exception of 1D meshes with periodic boundary conditions,
   at least one boundary condition must be Dirichlet.


.. code-block:: toml

   [electric_potential]
   poisson_solver = "hypre"
       [electric_potential.solver_params]
       relative_convergence_tolerance = #<float (hypre default)>
       absolute_convergence_tolerance = #<float (hypre default)>
       maximum_iterations = #<integer (hypre default)>

To use default values provided by hypre,
the entire ``solver_params`` subtable can be omitted.

``relative_convergence_tolerance``
: Set relative tolerance for convergence criterion.
If not specified, hypre's default is used.

``absolute_convergence_tolerance``
: Set absolute tolerance for convergence criterion.
If not specified, hypre's default is used.

``maximum_iterations``
: Set the maximum number of iterations for the iterative solve.
If not specified, hypre's default is used.

MFEM solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The MFEM solver differs from the other solvers in that it uses
the finite element method rather than the finite difference method.
It can therefore only be used with MFEM meshes.

..

   Periodic boundary conditions are currently not supported with MFEM meshes.


There are no solver options for this solver,
so the ``solver_params`` subtable should be omitted.

Periodic boundary condition type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Periodic boundaries always come in pairs.
A periodic boundary condition is associated with a measure-preserving
diffeomorphism between the boundaries.
The potential and the component of its gradient normal to the boundary
at every point on the boundary is constrained to be equal to those
at the point under the periodic mapping.
hPIC2 currently only supports periodic mappings
in cardinal directions,
i.e. purely in one of the x1-, x2-, or x3-directions.
Note that if one boundary is marked as periodic,
the boundary to which it is mapped must also be periodic;
hPIC2 does not attempt to intuit periodic mappings.
See the ``examples`` directory for examples of use.

.. code-block:: toml

   [[electric_potential.boundary_conditions]]
   boundary = #<integer or alias>
   type = "periodic"

Dirichlet boundary condition type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dirichlet boundary conditions constrain the value of the potential
at points on the boundary.

.. code-block:: toml

   [[electric_potential.boundary_conditions]]
   boundary = #<integer or alias>
   type = "dirichlet"
   function = #<options below>
       [electric_potential.boundary_conditions.function_params]
       #<options specific to function>

Neumann boundary condition type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Neumann boundary conditions constrain the component of the gradient of the
potential normal to the boundary.

.. code-block:: toml

   [[electric_potential.boundary_conditions]]
   boundary = #<integer or alias>
   type = "neumann"
   function = #<options below>
       [electric_potential.boundary_conditions.function_params]
       #<options specific to function>

Constant boundary condition function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The constant boundary condition constrains the value of the type
of boundary condition
to a constant.

.. code-block:: toml

   function = "constant"
       [electric_potential.boundary_conditions.function_params]
       value = #<float>

``value``
: Constant to set the boundary condition.

Sine boundary condition function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The sine boundary condition function sets the value of the boundary condition
to a value that is constant in space,
but sinusoidal in time.
In particular,
this can be used to impose RF biases on plasmas.

.. code-block:: toml

   function = "sine"
       [electric_potential.boundary_conditions.function_params]
       amplitude = #<float (1.0)>
       angular_frequency = #<float (1.0)>
       phase_shift = #<float (0.0)>
       y_offset = #<float (0.0)>

``amplitude``
: The amplitude of the sine function.

``angular_frequency``
: Angular frequency of the sine function.

``phase_shift``
: Phase shift of the sine function.

``y_offset``
: Adds a constant to the sine function.

``output_diagnostics``
-----------------------

The ``output_diagnostics`` table governs the type, level, and frequency of output.

.. code-block:: toml

   [output_diagnostics]
   output_dir = #<string (current working directory)>

       # (Optional, omit to pipe "info" level logs to stdout with no timing)
       [output_diagnostics.logging]
       log_level = #<options below ("info")>
       log_file = #<string (stdout)>
       timing_log_enabled = #<boolean (false)>

       # (Optional, omit to suppress particle output)
       [output_diagnostics.particle_output]
       stride = #<integer>
       first_step = #<boolean (true)>
       final_step = #<boolean (false)>
       species = #<array of string>
       source_counters = #<boolean (false)>

       # (Optional, omit to suppress field output)
       [output_diagnostics.field_output]
       stride = #<integer>
       first_step = #<boolean (true)>
       final_step = #<boolean (false)>

       # (Optional, omit for no field probes)
       [[output_diagnostics.field_probes]]
       stride = #<integer>
       first_step = #<boolean (false)>
       final_step = #<boolean (false)>
       tag = #<string>
       field = #<string>
       x1 = #<float>
       # Only needed in 2D or 3D
       x2 = #<float>
       # Only needed in 3D
       x3 = #<float>

       # (Optional, omit to suppress moment output)
       [output_diagnostics.moment_output]
       stride = #<integer>
       first_step = #<boolean (true)>
       final_step = #<boolean (false)>
       species = #<array of string>
       lab_frame_moment_exponents = #<array of array of integer>
       rest_frame_moment_exponents = #<array of array of integer>
       lab_frame_directional_moment_exponents = #<array of array of integer>
       lab_frame_nhat_directions = #<array of array of float>
       rest_frame_directional_moment_exponents = #<array of array of integer>
       rest_frame_nhat_directions = #<array of array of float>

       # (Optional, omit to suppress IEAD output)
       [output_diagnostics.iead_output]
       stride = #<integer>
       first_step = #<boolean (true)>
       final_step = #<boolean (false)>
           # (Optional, omit to set max_energy_te to 24 and num_energy_bins to 240)
           [output_diagnostics.iead_output.<string>]
           max_energy_te = #<integer>
           num_energy_bins = #<integer>

``output_dir``
: Path to directory for output.
If the directory does not exist, hPIC2 will create it.
If this option is omitted, the current working directory will be used.

``logging``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``logging`` subtable tells hPIC2's logger how much to output
and where to output.
If it is omitted, ``"info"`` level log messages will be printed to the console,
and no kernel timing will be performed.

.. code-block:: toml

   [output_diagnostics.logging]
   log_level = #<options below ("info")>
   log_file = #<string (stdout)>
   timing_log_enabled = #<boolean (false)>

``log_level``
: The following options are available, from most to least output:


#. ``"trace"``\ : Most verbose, all possible logging messages.
#. ``"debug"``\ : Debugging messages.
#. ``"info"``\ : Verbose information messages.
#. ``"warn"``\ : Warnings, which are typically recoverable but notable.
#. ``"error"``\ : Errors, which typically force termination.
#. ``"critical"``\ : Critical errors, which always force potentially unsafe termination.
#. ``"off"``\ : No logging.

All logging messages of the chosen level and below on this list are output.
For example, if ``"error"`` is chosen, then both errors and critical errors
will be output.

``log_file``
: Logging output will be written to this file.
If not provided, output will be printed to console.

``timing_log_enabled``
: If true, some critical kernels will be timed.
This is printed to ``hpic2_timing.json``\ , a file in the JSON format.
Each row represents an entry in the timing log
and contains a JSON object.
Each object takes the form

.. code-block::

   {
       "mpi rank": <rank>,
       "thread": <thread>,
       "event": <event name>,
       "message": {
           "ID": <event ID>,
           "event_end": <event end epoch in ns>,
           "duration_nanos": <event walltime in ns>,
           "workload_unit": <name of workload type>,
           "workload": <number of workload units>
       }
   }

The timing log capability is intended mostly for developer use
and tracks the walltime of various kernels in hPIC2.
It also tracks the type of work done during the kernel
(for example, ``"workload_unit"`` is set to ``"particle"`` for the particle push)
and how many units of work were performed during the kernel.
These are written into the source code and not adjustable by users.

``particle_output``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``particle_output`` subtable governs particle output.
For a particle-based species, this will periodically output information about
every particle currently active particle in the simulation.
For simulations that are not parallelized with MPI,
output filenames take the form
``<simulation tag>_<species name>_particles_t<time step zero padded to 7 digits>.dat``
where the simulation tag is taken from the ``input_mode`` table.
For MPI-parallelized runs, each MPI process outputs a separate file,
and ``.<rank>`` is appended to the end of the above filename for each MPI process.
The files themselves are a space-separated value format.
Each row represents a particle and takes the form

.. code-block::

   <charge number> <element index> <submesh ID> <weight> <x1> <x2> <x3> <v1> <v2> <v3>

with the understanding that the submesh ID is a dummy output for
non-pumi meshes.

.. code-block:: toml

   [output_diagnostics.particle_output]
   stride = #<integer>
   first_step = #<boolean (true)>
   final_step = #<boolean (false)>
   species = #<array of string>
   source_counters = #<boolean (false)>

``stride``
: Time step interval for output.
For example, if this is set to 5, output will be printed every 5 time steps.
If set to 0, no output will be printed.

``first_step``
: If true, forces output on the first time step,
even if the choice of stride would normally suppress output.
Notably, this prints output even if the stride is set to 0.

``final_step``
: If true, forces output on the final time step,
even if the choice of stride would normally suppress output.

``species``
: An array of species names.
These species must have been defined in the ``species`` top-level table.
The user should take care that only particle-based species are listed
in this array.
Non-particle-based species can be placed in this array,
but a warning will be printed,
and there will be no output for that species.

``source_counters``
: Enables a log of all particle sources in the simulation.
This is printed to ``hpic2_particle_source_counters.json``\ ,
a JSON file.
Each row represents a particle source event and contains a JSON object.
Each object takes the form

.. code-block::

   {
       "event": <event name>,
       "species": <species affected>,
       "timestep": <time step of event>,
       "counts": [
           {
               "charge": <charge number of new particles>,
               "macro": <number of added macroparticles>,
               "phys": <number of added physical particles>
           },
           ...
       ]
   }

This capability is mostly intended as a debugging tool for developers.
The sources which are tracked are written into the source code
and are not configurable by the user.

``field_output``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``field_output`` subtable governs frequency of field output.
The electric and magnetic fields, along with the electric potential
and electrostatic energy, are printed.
For MFEM meshes, fields are output to the
`PVTU <https://vtk.org/wp-content/uploads/2015/04/file-formats.pdf>`_
format,
which is most easily read by
`ParaView <https://www.paraview.org/>`_.
This output is placed in a directory with the name of the simulation tag,
which itself is placed in the user-specified output directory.
For all other meshes,
electric field output is placed in files with filenames of the form
``<simulation tag>_EFIELD_t<time step zero padded to 7 digits>.dat``\ ;
magnetic field output is placed in files with filenames of the form
``<simulation tag>_BFIELD_t<time step zero padded to 7 digits>.dat``\ ;
electric potential output is placed in files with filenames of the form
``<simulation tag>_PHI_t<time step zero padded to 7 digits>.dat``\ ;
and electrostatic energy output is placed in files with filenames of the form
``<simulation tag>_ENERGY_ELECTROSTATIC.dat``.
The electric and magnetic field output files
are all in a space-separated value format.
Each line represents a node in the mesh and takes the form

.. code-block::

   <x1-component> <x2-component> <x3-component>

The potential is similar, but each line contains only a single scalar value.
The electrostatic energy output differs, since there is a single scalar value
to output per time step.
It is also in a space-separated value format,
but of the form

.. code-block::

   <time step zero padded to 7 digits> <total electrostatic energy>

..

   MFEM meshes currently do not compute or print the electrostatic energy.


.. code-block:: toml

   [output_diagnostics.field_output]
   stride = #<integer>
   first_step = #<boolean (true)>
   final_step = #<boolean (false)>

``stride``
: Time step interval for output.
For example, if this is set to 5, output will be printed every 5 time steps.
If set to 0, no output will be printed.

``first_step``
: If true, forces output on the first time step,
even if the choice of stride would normally suppress output.
Notably, this prints output even if the stride is set to 0.

``final_step``
: If true, forces output on the final time step,
even if the choice of stride would normally suppress output.

``field_probes``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Field probes print the value of a field at a fixed position in the domain
at a user-specified frequency.
Field probes are specified as an array of tables,
each entry of which defines the parameters for a single probe.
Any number of field probes may be requested.
Output is in a space-separated format.
The first column gives the timestep for output.
Subsequent columns give the value of the field at that timestep.
For scalar fields, there is one subsequent column.

.. code-block:: toml

   [[output_diagnostics.field_probes]]
   stride = #<integer>
   first_step = #<boolean (false)>
   final_step = #<boolean (false)>
   tag = #<string>
   field = #<string>
   x1 = #<float>
   # Only needed in 2D or 3D
   x2 = #<float>
   # Only needed in 3D
   x3 = #<float>

``stride``
: Time step interval for output.
For example, if this is set to 5, output will be printed every 5 time steps.
If set to 0, no output will be printed.

``first_step``
: If true, forces output on the first time step,
even if the choice of stride would normally suppress output.
Notably, this prints output even if the stride is set to 0.

``final_step``
: If true, forces output on the final time step,
even if the choice of stride would normally suppress output.

``tag``
: Unique tag for output. Determines output filename.

``field``
: Field to output.
Options are in the table below.

.. list-table::
   :header-rows: 1

   * - Option
     - Description
   * - ``"phi"``
     - Electric scalar potential.
   * - ``"B"``
     - Magnetic (B) field.


``x1``
: x1-coordinate of probe position.

``x2``
: x2-coordinate of probe position.
Ignored in 1D simulations.

``x3``
: x3-coordinate of probe position.
Ignored in 1D and 2D simulations.

``moment_output``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``moment_output`` subtable governs the frequency and type of output
for kinetic moments.
At each requested time step, kinetic moments are computed and printed.
Moments can be computed in the frame of reference of the domain,
the moving frame of reference of the species itself,
or both. Directional moments can also be computed along a specified direction
vector.
The user provides a list of species for which moment output is desired
and a list of moment orders in either frame of reference.
The moment orders are specified as a triple of nonnegative integers,
indicating the order in each direction separately. In case of directional
moments, a list of direction vectors (one for each moment-order triple)
is needed. More details are provided in the list of options below.
In case of standard moments, the output is placed in files with filenames of the form
``<simulation tag>_<species name>_<lab or rest>_frame_moment_<order triple>.dat``. For
directional moments, the output file name will be of the form
``<simulation tag>_<species name>_<lab or rest>_frame_directional_moment_<order triple>_n<direction_number>.dat`` where the ``direction_number`` refers to the index
of a direction in the list of direction vectors. The files are in a space-separated value format where each row represents an output time step and
each column represents a node in the mesh.

..

   Moment output is currently not supported on MFEM meshes.


.. code-block:: toml

   [output_diagnostics.moment_output]
   stride = #<integer>
   first_step = #<boolean (true)>
   final_step = #<boolean (false)>
   species = #<array of string>
   lab_frame_moment_exponents = #<array of array of integer>
   rest_frame_moment_exponents = #<array of array of integer>
   lab_frame_directional_moment_exponents = #<array of array of integer>
   lab_frame_nhat_directions = #<array of array of float>
   rest_frame_directional_moment_exponents = #<array of array of integer>
   rest_frame_nhat_directions = #<array of array of float>

``stride``
: Time step interval for output.
For example, if this is set to 5, output will be printed every 5 time steps.
If set to 0, no output will be printed.

``first_step``
: If true, forces output on the first time step,
even if the choice of stride would normally suppress output.
Notably, this prints output even if the stride is set to 0.

``final_step``
: If true, forces output on the final time step,
even if the choice of stride would normally suppress output.

``species``
: An array of species names.
These species must have been defined in the ``species`` top-level table.

``lab_frame_moment_exponents``
: An array of integer triples.
A triple determines the order of the moment computed in each direction.
For example, ``[0,0,0]`` gives the zero-th order moment in all directions,
which is the density;
similarly, ``[1,0,0]`` gives the first order moment in the x1-direction,
which is that component of the momentum density.
This computes moments in the lab or static frame of reference.

``rest_frame_moment_exponents``
: An array of integer triples.
A triple determines the order of the moment computed in each direction.
For example, ``[0,0,0]`` gives the zero-th order moment in all directions,
which is the density;
similarly, ``[1,0,0]`` gives the first order moment in the x1-direction,
which is that component of the momentum density.
This computes moments in the frame of reference of the species itself;
it first computes the average velocity of particles of the species,
then shifts into that frame of reference for the output moment calculation.

``lab_frame_directional_moment_exponents``
: An array of integer triples.
Same as ``lab_frame_moment_exponents`` with the exception that a list of directions
is needed to be specified one for each moment exponent triple. This computes the
moment in the lab or static frame of reference for every species crossing a plane
along it's normal direction which is specified in ``lab_frame_nhat_directions``

``lab_frame_nhat_directions``
: An array of float triples representing the normal direction vector of a plane
about which lab-frame directional moments are to be computed. It is not necessary to provide
a unit-vector as direction inputs. For example, the input ``[1.0,0.0,-1.0]`` is equivalent
to the unit-vector ``[0.7071,0.0,-0.7071]``

``rest_frame_directional_moment_exponents``
: An array of integer triples.
Same as ``rest_frame_moment_exponents`` with the exception that a list of directions
is needed to be specified one for each moment exponent triple. This computes the
moments in the frame of reference of a given species crossing a plane
along it's normal direction which is specified in ``rest_frame_nhat_directions``

``rest_frame_nhat_directions``
: An array of float triples representing the normal direction vector of a plane
about which rest-frame directional moments are to be computed. It is not necessary to provide
a unit-vector as direction inputs. For example, the input ``[1.0,0.0,-1.0]`` is equivalent
to the unit-vector ``[0.7071,0.0,-0.7071]``

``iead_output``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``iead_output`` subtable governs the frequency and parameters for
ion energy/angle distribution output. An ion energy/angle distribution is a 2D histogram of particles of a particular species impacting a simulation boundary, where bins are angles and energies. If this TOML table is present and ``stride`` is
greater than 0, one IEAD file will be saved per boundary per stride for all Boris
Buneman (kinetic) species.

The filenames are formatted as
``<SPECIES_NAME>_dE_eV_<ENERGY_LEVEL>_<BOUNDARY_NAME>_t<TIMESTEP>.dat``. Each file
contains a 2D histogram in ASCII text. The matrix has ``NUM_ANGLE_BINS`` columns and ``NUM_ENERGY_BINS`` rows.
Each value in the matrix represents the number of physical
particles which have struck that boundary at that particular energy and that
particular angle. The angle value is determined by (column number) * ``dAngle_deg``\ , where ``dAngle_deg = 90/NUM_ANGLE_BINS`` , while the energy
value is determined by (row number) * ``de_eV``\ , where ``de_eV`` is determined by
``MAX_ENERGY_TE`` and ``NUM_ENERY_BINS`` (see below). For user convenience, ``de_eV``
is included in the output  filename. Note that the IEAD file output at
each timestep is cumulative: values in the histogram represent total number of physical particles
which have impacted the boundary since the start of the simulation. The final row of the
IEAD is used as an accumulation point, meaning all particles greater than
``MAX_ENREGY_TE`` will be binned into this row.

Explanation of Fields
~~~~~~~~~~~~~~~~~~~~~~~~

``stride``\ : (required) IEADs will be output every ``stride`` timesteps.

``first_step``\ : if true, the IEAD will be output on the first step of the simlation
(defualt: true)

``final_step``\ : if true, IEADs will be output on the final step of the simulation
(default: false)

``iead_output.<SPECIES_NAME>.max_energy_te``\ : the energy of the final row of the
IEAD for species ``SPECIES_NAME``\ , in electron volts. This row will serve as an
accumulation point. All particles impacting the boundary with energy greater
than ``MAX_ENERGY_TE`` will be binned into the final row. (default 24)

``iead_output.<SPECIES_NAME>.num_energy_bins``\ : the number of rows, or energy bins,
in the IEAD histogram for species ``SPECIES_NAME``. ``de_eV`` is therefore
``MAX_ENERGY_TE`` / ``NUM_ENERGY_BINS`` (default: 240).

Example TOML Subtable
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: toml

   [output_diagnostics.iead_output]
   stride = #<integer>
   first_step = #<boolean (true)>
   final_step = #<boolean (false)>
       # (Optional, omit to set max_energy_te to 24, num_energy_bins to 240, and num_angle_bins to 90)
       [output_diagnostics.iead_output.<string>]
       max_energy_te = #<integer (24)>
       num_energy_bins = #<integer (240)>
       num_angle_bins = #<integer (90)>

A helper script in the ``scripts/`` in the hpic2 source repository is provided to view an IEAD file. Usage:

.. code-block:: bash

   python3 scripts/plot_iead.py IEAD_FILE

``interactions``
----------------

The ``interactions`` table governs interactions and collisions between species.
Available interactions and interaction-specific options are presented
in subsequent sections.

Electron impact ionization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Electron impact ionizations between a ``"boris_buneman"`` ion species
and ``"boltzmann"`` electrons is handled using Monte Carlo collisions (MCC).
The cross sections used are from Bell (1983).
For each ion charge state, the cross section is parametrized by 7 constants:
A, B1, B2, B3, B4, B5, and I.
The first six of these are fitting parameters to a semi-empirical formula,
whereas the latter of these is the ionization energy.

.. code-block:: toml

   [interactions.electron_impact_ionization.<string>]
   electron_species = #<string>
   A = #<array of float>
   B = #<array of array of float>
   I = #<array of float>

The key of the table is the name of the desired ``"boris_buneman"`` species,
which must have been defined in the ``species`` table.

``electron_species``
: Name of the ``"boltzmann"`` electron species.

``A``
: An array of floats,
representing the value of the A parameter in Bell's formula for each charge
state.
The array must be no longer than the atomic number
of the ion species,
which reflects the maximum ionization of the species.
The array may be shorter than the atomic number;
in this case, omitted values of A are taken to be zero.

``B``
: Array of quintuples of floats,
representing the values of the five B parameters in Bell's formula for each
charge state.
The array must be no longer than the atomic number
of the ion species,
which reflects the maximum ionization of the species.
The array may be shorter than the atomic number;
in this case, omitted values of B are taken to be zero.
Similarly, each quintuple may actually have length less than five,
in which case omitted values of B are taken to be zero.

``I``
: Array of floats,
representing the values of the I parameter in Bell's formula for each charge
state.
The array must be no longer than the atomic number
of the ion species,
which reflects the maximum ionization of the species.
The array may be shorter than the atomic number;
in this case, omitted values of I are taken to be zero.

Coulomb collision force
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coulomb collisions between two species can be approximately treated using
an effective force on each particle.

..

   The Coulomb collision force currently only works with a ``"boris_buneman"``
   source species and a ``"boltzmann"`` target species.
   (The target species exerts a force on particles of the source species.)


.. code-block:: toml

   [interactions.coulomb_collision_force.<string>]
   target_species = #<string>

The key of the table is the name of the desired ``"boris_buneman"`` source
species,
which must have been defined in the ``species`` table.

``target_species``
: Name of the target species,
which must have been defined in the ``species`` table.
