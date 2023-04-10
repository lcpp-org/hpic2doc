Models
======

Model Hierarchy
---------------

Full Orbit
~~~~~~~~~~

The basic particle model of hPIC2 is a classical (non-relativistic)
full-orbit Lagrangian particle of mass :math:`m` and charge :math:`q`,
with dynamics described by the classical Newton-Lorentz equation,

.. math::

   m \frac{d^2  \mathbf{x} }{dt^2} = q  \mathbf{E}  + q  \mathbf{v}  \times  \mathbf{B}

where the electric field :math:`\mathbf{E}` and the magnetic field
:math:`\mathbf{B}` are either calculated self-consistently by solving the
Maxwell Equations, or provided externally by the user (eg. an imposed
magnetic field).

The Newton-Lorentz equation is integrated by means of the Boris-Bunemann
numerical method, with linearized tangent.

Guiding Center
~~~~~~~~~~~~~~

This section was prepared by

-  Xin Zhi Tan, UIUC

In guiding center formalism, the particles can be advanced using
equation of motion by Littlejohn, Boozer, White and others:

.. math:: \dot{X} = \frac{1}{D}\left( \frac{q_s}{m_s}\rho_s\mathbf{B} + \frac{\mathbf{F}\times\mathbf{B}}{B^2} + \frac{q_s}{m_s}\rho_s^2B\nabla\times\hat{b}  \right)

.. math:: \dot{\rho_s} = \frac{\mathbf{F}\cdot\mathbf{\dot{X}}}{B\rho_s}, \ \ \rho_s \equiv \frac{v_{||s}m_s}{q_sB}

.. math:: \dot{\mu_s}= 0,

where :math:`X` is the position of the guiding center, :math:`\rho_s` is
the normalized parallel speed, :math:`\mu_s` is the magnetic moment,
:math:`\mathbf{F}=\mathbf{E} - \mu_s\nabla B` and
:math:`D = 1+\rho_s\hat{\mathbf{b}}\cdot\nabla \times \hat{\mathbf{b}}`.

Fluid Model internal to hPIC2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section was prepared by:

-  Logan Meredith, UIUC

While hPIC2 is designed primarily as a PIC code, it also has hybrid
fluid-kinetic capabilities, which allows hPIC2 to model the plasma as
fluids in suitable parts of the domain. Fluid solvers tend to be faster
than PIC solvers, but impose stricter constraints on the allowed shape
of the particle distribution, and therefore are valid in a narrower
regime than PIC. In this section, we describe the fluid model used by
hPIC2 and assumptions made by hPIC2 on the particle distribution.

Fluid equations
^^^^^^^^^^^^^^^

We adopt an Einstein-like tensor notation throughout this section,
whereby repeated indices are summed except where noted.

hPIC2 uses a collisionless 5-moment fluid model, which means that five
conserved fluid quantities are computed. These fluid quantities are the
**mass density** :math:`\rho`, the vector **momentum density**
:math:`p_i`, and the **total energy density** :math:`e`. The equations
governing these quantities are derived in
`Theory`_. The relevant
equations are

.. math::

   \begin{aligned}
     \frac{\partial \rho}{\partial t} &= - \frac{\partial p_i}{\partial x_i}, \\
     \frac{\partial p_i}{\partial t} &= - \frac{\partial P_{ij}}{\partial x_j} + \frac{q}{m} \left( \rho E_i + \epsilon_{ijk} p_j B_k \right), \\
     \frac{\partial e}{\partial t} &= - \frac{\partial Q_i}{\partial x_i} + \frac{q}{m} p_i E_i,
   \end{aligned}

where :math:`E_i` is the electric field, :math:`B_i` is the magnetic
field, :math:`P_{ij}` is the **stress tensor**, and :math:`Q_i` is the
**energy flux density**. Note that, while the electric and magnetic
fields are known in this context, the stress tensor and energy flux
density are unknown fluid quantities. The fluid model must be closed by
assuming a relation between them and the fluid quantities of interest.

This is accomplished in hPIC2 by assuming the particle distribution to be
a drifting Maxwellian. With this assumption, the stress tensor and
energy flux density are related to the mass, momentum, and total energy
density via the following equations:

.. math::
   :label: fluid_eos

   \begin{aligned}
     P_{ij} &= \frac{1}{3} \delta_{ij} \left( 2 e - \frac{p_k p_k}{\rho} \right) + \frac{p_i p_j}{\rho}, \label{stress}\\
     Q_i &= \frac{p_i}{2 \rho} \left( \frac{10}{3} e - \frac{2}{3} \frac{p_j p_j}{\rho} \right). \label{energyflux}
   \end{aligned}

Altogether, these equations provide
a self-consistent model for the time evolution of the noted fluid
quantities.

In the one-dimensional version of hPIC2, the fluid equations can be
further simplified. Constraining the domain to lie along the
:math:`x`-axis in a Cartesian coordinate system, the derivatives in
orthogonal directions can be discarded, and the fluid equations reduce
to

.. math::
   :label: fluid_eqs

   \begin{aligned}
     \frac{\partial \rho}{\partial t} &= - \frac{\partial p_x}{\partial x}, \label{ltm:eq:rho1d} \\
     \frac{\partial p_i}{\partial t} &= - \frac{\partial P_{xi}}{\partial x} + \frac{q}{m} \left( \rho E_i + \epsilon_{ijk} p_j B_k \right), \label{ltm:eq:p1d} \\
     \frac{\partial e}{\partial t} &= - \frac{\partial Q_x}{\partial x} + \frac{q}{m} p_x E_x, \label{ltm:eq:e1d}
   \end{aligned}

again where :math:`P_{ij}` and :math:`Q_{i}` satisfy
Eqs. :eq:`fluid_eos`, respectively.

While hPIC2 explicitly models the conservative quantities listed above,
some non-conservative quantities are of interest, notably the **number
density** :math:`n`, **bulk velocity** :math:`u_i`, and **temperature**
:math:`T`. The conservative quantities can be expressed in terms of
these via the following invertible relations:

.. math::

   \begin{aligned}
     \rho &= n m, \\
     p_i &= n m u_i, \\
     e &= \frac{n k T}{\gamma - 1} + \frac{1}{2} n m u_i u_i,
   \end{aligned}

where :math:`k` is Boltzmann’s constant and :math:`\gamma` is the heat
capacity ratio of the species. For a monatomic species,
:math:`\gamma = 5/3`.

Lax-Friedrichs solver
^^^^^^^^^^^^^^^^^^^^^

We forgo the Einstein-like tensor notation and adopt a standard finite
difference index notation in this section. Subscripts involving
:math:`i` denote indices of spatial grid points and superscripts
involving :math:`n` denote indices of temporal grid points. Since the
fluid solver in hPIC2 currently functions only on a uniform,
one-dimensional mesh with uniform timestepping, this means that
:math:`y_i^n \equiv y(x_{\mathrm{min}} + i \Delta x, n \Delta t)` for
any quantity :math:`y` defined on the hPIC2 domain. We constrain the
domain to have :math:`N` grid points and :math:`M` time steps.

The fluid
equations :eq:`fluid_eqs`
are hyperbolic equations of the form

.. math::
   :label: lfexample

   \label{ltm:eq:lfexample}
     \frac{\partial y}{\partial t} = - \frac{\partial g(y)}{\partial x} + h(y).

A numerical method that is forward in time is desirable for solving the
fluid equations, as it would allow for simultaneous particle pushing in
hybrid applications. Furthermore, since fluid quantities evolve slowly
compared to the electric and magnetic fields, possible instabilities
arising from the use of explicit finite difference schemes present
little trouble. We therefore adopt the Lax-Friedrichs finite difference
scheme as the primary hPIC2 fluid solver. The scheme gives the solution
of Eq. :eq:`lfexample` at grid points
:math:`x_i = x_{\mathrm{min}} + i \Delta x` and time steps
:math:`t_n = n \Delta t` to be

.. math:: y_i^{n+1} = \frac{1}{2} \left( y_{i+1}^n + y_{i-1}^n \right) - \frac{\Delta t}{2 \Delta x} \left( g (y_{i+1}^n) - g (y_{i-1}^n) \right) + \Delta t \, h(y_i^n).

The Lax-Friedrichs scheme is a forward in time, centered in space finite
difference scheme with an artificial viscosity of :math:`1/2`.
Importantly, it is also valid when :math:`y` is a vector. It is explicit
and, when :math:`h=0`, first order accurate in both time and space,
which is acceptable for the present application.

Applying the Lax-Friedrichs scheme to the fluid equations results in the
following equations:

.. math::

   \begin{aligned}
     \rho_i^{n+1} &= \frac{1}{2} \left( \rho_{i+1}^n + \rho_{i-1}^n \right) - \frac{\Delta t}{2 \Delta x} \left( (p_x)_{i+1}^n - (p_x)_{i-1}^n \right), \\
     (p_x)_i^{n+1} &= \frac{1}{2} \left( (p_x)_{i+1}^n + (p_x)_{i-1}^n \right) - \frac{\Delta t}{2 \Delta x} \left( (P_{xx})_{i+1}^n - (P_{xx})_{i-1}^n \right) \nonumber \\
     &\quad + \Delta t \frac{q}{m} \left( \rho_i^n (E_x)_i^n + (p_y)_i^n (B_z)_i^n - (p_z)_i^n (B_y)_i^n \right), \\
     (p_y)_i^{n+1} &= \frac{1}{2} \left( (p_y)_{i+1}^n + (p_y)_{i-1}^n \right) - \frac{\Delta t}{2 \Delta x} \left( (P_{xy})_{i+1}^n - (P_{xy})_{i-1}^n \right) + \Delta t \frac{q}{m} \left( (p_z)_i^n (B_x)_i^n - (p_x)_i^n (B_z)_i^n \right), \\
     (p_z)_i^{n+1} &= \frac{1}{2} \left( (p_z)_{i+1}^n + (p_z)_{i-1}^n \right) - \frac{\Delta t}{2 \Delta x} \left( (P_{xz})_{i+1}^n - (P_{xz})_{i-1}^n \right) + \Delta t \frac{q}{m} \left( (p_x)_i^n (B_y)_i^n - (p_y)_i^n (B_x)_i^n \right), \\
     e_i^{n+1} &= \frac{1}{2} \left( e_{i+1}^n + e_{i-1}^n \right) - \frac{\Delta t}{2 \Delta x} \left( (Q_x)_{i+1}^n - (Q_x)_{i-1}^n \right) + \Delta t \frac{q}{m} (p_x)_i^n (E_x)_i^n,
   \end{aligned}

where the stress tensor and energy flux density formulas on the mesh are

.. math::

   \begin{aligned}
     (P_{xx})_i^n &\equiv \frac{2}{3} e_i^n + \frac{2}{3} \frac{(p_x)_i^n (p_x)_i^n}{\rho_i^n} - \frac{1}{3} \frac{(p_y)_i^n (p_y)_i^n + (p_z)_i^n (p_z)_i^n}{\rho_i^n}, \\
     (P_{xy})_i^n &\equiv \frac{(p_x)_i^n (p_y)_i^n}{\rho_i^n}, \\
     (P_{xz})_i^n &\equiv \frac{(p_x)_i^n (p_z)_i^n}{\rho_i^n}, \\
     (Q_x)_i^n &\equiv \frac{(p_x)_i^n}{2 \rho_i^n} \left( \frac{10}{3} e_i^n - \frac{2}{3} \frac{(p_x)_i^n (p_x)_i^n + (p_y)_i^n (p_y)_i^n + (p_z)_i^n (p_z)_i^n}{\rho_i^n} \right),
   \end{aligned}

as computed from Eqs. :eq:`fluid_eos`.

In PIC mode, hPIC2 initializes particles according to a Maxwellian
distribution with constant number density :math:`n_0` and temperature
:math:`T_0`. The fluid model agrees with this by imposing the initial
conditions

.. math::

   \begin{aligned}
     \rho_i^0 &= n_0 m, \\
     (p_x)_i^0 &= 0, \\
     (p_y)_i^0 &= 0, \\
     (p_z)_i^0 &= 0, \\
     e_i^0 &= \frac{3}{2} n_0 k T_0
   \end{aligned}

for all :math:`i \in [0,N-1]`.

The walls in hPIC2 are absorbing, which implies that the fluid quantities
are zero everywhere outside the domain. This is enforced by imposing the
boundary conditions

.. math::

   \begin{aligned}
     \rho_{-1}^n &= \rho_{N}^n = 0, \\
     (p_x)_{-1}^n &= (p_x)_N^n = 0, \\
     (p_y)_{-1}^n &= (p_y)_N^n = 0, \\
     (p_z)_{-1}^n &= (p_z)_N^n = 0, \\
     e_{-1}^n &= e_N^n = 0
   \end{aligned}

for all :math:`n \in [0,M-1]`.

Boltzmann Electrons
~~~~~~~~~~~~~~~~~~~

This section was prepared by:

-  Moutaz Elias, UIUC

On ion-transport time scales, the electron behavior can in first
approximation be described simply considering a balance between
electrostatic forces and pressure forces on an isothermal fluid:
:math:`-k_B T_e \nabla n_e + e n_e\nabla \phi \approx 0`, with usual
meaning of symbols as in
`Chen <https://doi.org/10.1007/978-3-319-22309-4_1>`_.
Integrating the balance of forces leads to a relation between the
electron particle density and the plasma potential in the form of
equation

.. math::
   :label: botlzmann.equation1

   \begin{aligned}
   n_e(\mathbf{x})=n_0 \exp( e \phi(\mathbf{x})/k_B T_e),\label{botlzmann.equation1}
   \end{aligned}

where :math:`n_0` is the reference electron density corresponding to
:math:`\phi=0`. Boltzmann electrons hold an advantage in terms of
computational cost over the alternative approximations used in PIC
simulations. While alternative methods capture the physical phenomena of
electron motion to a higher degree of accuracy, the added simulation
complexity makes it computationally expensive to run large timescale
simulations.

Time advancement schemes calculate unknown time-dependent variables at
time :math:`t^{k+1} = t^k + \Delta t` from known variables at time
:math:`t^k`. Common time advancement algorithm in PIC codes calculates
the ion density :math:`n_i^{k+1}` using plasma potential :math:`\phi^k`.
Subsequently, the plasma potential :math:`\phi^{k+1}` is solved using
the newly calculated ion density :math:`n_i^{k+1}` and
equation :eq:`botlzmann.equation1`, i.e,;

.. math::
   :label: poision.equation

   \begin{aligned}
   \epsilon_0 \nabla^2\phi^{k+1}(\mathbf{x})&=-\rho^{k+1}(\mathbf{x})\label{poision.equation}\\
   &=en_e^{k+1}(\mathbf{x})-en_i^{k+1}(\mathbf{x})\label{poision.equation1}\\
   &=en_0^{k+1} \exp(\phi^{k+1}(\mathbf{x})/T_e)-en_i^{k+1}(\mathbf{x})\label{poision.equation2}.
   \end{aligned}

Equation :eq:`poision.equation` can be solved
using Newton-Raphson, or other methods, to calculate the plasma
potential for the next iteration. Problems arise when the reference
electron density :math:`n_0` varies with time as is the case in the
presence of a volumetric source/loss, or a boundary flux. A
self-consistent numerical scheme to calculate :math:`n_0^{k+1}` is
required to maintain charge conservation. Breaking charge conservation
leads to numerical oscillations and simulation divergence.

Particle Tracing
~~~~~~~~~~~~~~~~

Charge Conservation with Boltzmann Electrons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section was prepared by:

-  Moutaz Elias, UIUC

The charge conservation scheme is derived from the
`Ampere-Maxwell equation <https://doi.org/10.1017/9781108333511>`_ in
differential form,

.. math::
   :label: max.equation1

   \begin{aligned}
   \nabla \times \mathbf{B}&= \mu_0 \mathbf{J} + \epsilon_0 \mu_0 \frac{\partial \mathbf{E}}{\partial t}\label{max.equation1}
   \end{aligned}

As usual, local charge conservation is obtained by taking the divergence
of equation :eq:`max.equation1` and calling the
displacement current as
:math:`\mathbf{J_D}=\epsilon_0 \frac{\partial \mathbf{E}}{\partial t}`

.. math::
   :label: globalcharge.equation1

   \begin{aligned}
   \nabla \cdot (\nabla \times \mathbf{B})&= \mu_0 \nabla \cdot \mathbf{J}  +\mu_0 \nabla \cdot \left( \epsilon_0  \frac{\partial \mathbf{E}}{\partial t} \right) \label{max.equation2}\\
   0 &=\nabla \cdot \mathbf{J} + \nabla \cdot \mathbf{J}_D, \label{globalcharge.equation1}
   \end{aligned}

where the conduction current
:math:`\mathbf{J}=\mathbf{J}_i + \mathbf{J}_e` is the sum of the
contributions from the ion current :math:`\mathbf{J}_i` and the electron
current :math:`\mathbf{J}_e`.
Equation :eq:`globalcharge.equation1` can
equivalently be expressed as

.. math::

   \begin{aligned}
    \nabla \cdot (\mathbf{J}_e + \mathbf{J}_i  + \mathbf{J}_D)&=0 \label{globalcharge.equation2}
   \end{aligned}

or using its integral form,

.. math::
   :label: displacemen.equation1

   \begin{aligned}
   \int_V \nabla \cdot (\mathbf{J}_e + \mathbf{J}_i  + \mathbf{J}_D) dV&= 0  \label{displacemen.equation1}
   \end{aligned}

In the presence of volumetric source :math:`G` and loss :math:`L` terms,
equation :eq:`displacemen.equation1` becomes

.. math::
   :label: displacemen.equation2

   \begin{aligned}
   \int_V \nabla \cdot (\mathbf{J}_e + \mathbf{J}_i  + \mathbf{J}_D) dV&= G-L \label{displacemen.equation2}
   \end{aligned}

The Boltzmann electron model described in
equation :eq:`botlzmann.equation1` implicitly
assumes the electron distribution is at a Maxwellian thermal
equilibrium. For a Maxwellian thermal distribution, with a mean thermal
electron velocity :math:`\mathbf{u_e}=\sqrt{\frac{8 K_b T_e}{\pi m_e}}`,
the current density at the location :math:`\mathbf{x}` can,
as in `Chen <https://doi.org/10.1007/978-3-319-22309-4_1>`_,
be expressed as

.. math::
   :label: boundaryflux

   \begin{aligned}
   \mathbf{J}_e(\mathbf{x})=-e \boldsymbol{\Gamma}_e(\mathbf{x})=-e n_0 \mathbf{u}_e \exp(e\Phi(\mathbf{x})/T_e) \label{boundaryflux}
   \end{aligned}

By substituting Equation :eq:`boundaryflux` into
Equation :eq:`displacemen.equation2` and
solving for :math:`n_0`, immediately yields an expression for the
reference Boltzmann electron density :math:`n_0`

.. math::
   :label: density_update

   \begin{aligned}
   n_0= \frac{\int_V \nabla \cdot (\mathbf{J}_i  + \mathbf{J}_D) dV - G + L }{\int_V \nabla \cdot e \mathbf{u}_e \exp(e\Phi(\mathbf{x})/T_e) dV}
   \label{density_update}
   \end{aligned}

Equation :eq:`density_update` can be directly used to
enforce global charge conservation in explicit PIC schemes with
Boltzmann electrons. An example algorithm is discussed hereafter.

A simple explicit algorithm implementing
Equation :eq:`density_update` for updating the
Boltzmann density :math:`n_0` from time step :math:`t^{k}` to time step
:math:`t^{k+1}` is as follows.

#. Calculate ion density :math:`n_i^{k+1}` using the plasma potential
   :math:`\phi^k` at the previous time step, using the classical
   explicit PIC scheme;

#. Calculate reference Boltzmann electron density at :math:`n_0^{k+1}`
   at time step :math:`t^{k+1}` using
   equation :eq:`density_update` and boundary
   conditions for :math:`\phi^{k+1}`;

   .. math::

      \begin{aligned}
          n_0^{k+1}= \frac{\int_V \nabla \cdot (\mathbf{J}_i^{k+1} + \mathbf{J}_D^{k}) dV - G^{k+1} + L^{k+1} }{\int_V \nabla \cdot e \mathbf{u_e} \exp(e\phi^{k+1}/T_e) dV}
          \label{density_update1}

      \end{aligned}

#. Solve the plasma potential :math:`\phi^{k+1}` using ion density
   :math:`n_i^{k+1}`, boundary conditions for :math:`\phi^{k+1}`, the
   Poisson equation and reference Boltzmann electron reference density
   :math:`n_0^{k+1}`.

The algorithm can be equally applied to plasma domains of arbitrary
dimensionality in 1D, 2D or 3D without any loss of accuracy. However,
the conventional Courant–Friedrichs–Lewy (CFL) condition on the time
step remains necessary to ensure accuracy on the particle pusher, and to
resolve ion-timescale phenomena. In the next section we apply this
algorithm to two cases, a steady-state plasma sheath and a
radio-frequency plasma sheath.

Interfaces with external Fluid Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SOLPS
^^^^^

Zapdos-CRANE
^^^^^^^^^^^^

Hybrid Methods
--------------

Particle Moments
~~~~~~~~~~~~~~~~

This section was prepared by:

-  Logan Meredith, UIUC

The hybrid fluid-kinetic capability implemented in hPIC2 requires
communication between PIC cells, which compute the Newtonian dynamics of
individual particles sampled from the particle distribution, and fluid
cells, which model the time evolution of only certain statistical
moments of the distribution. In order to correctly account for particle
diffusion from PIC cells to fluid cells, hPIC2 requires a routine that
can compute the moments of a discrete particle distribution. In this
section, we introduce the definition of the moment tensor and describe
some details of implementing a moment calculator in hPIC2.

Theory
^^^^^^

In plasma physics, **moments** are polynomials integrated against the
particle distribution in velocity space. We refer to the polynomial
corresponding to a given moment as that moment’s **moment polynomial**.
For a multi-dimensional plasma, a moment is generally a tensor whose
order depends on the order of its moment polynomial. In principle,

hPIC2 specifies that elements of the moment tensor of order :math:`N` are
given by

.. math::
   :label: momdef

   \label{ltm:eq:momdef}
     M_{i_1 i_2 \cdots i_N}^s (\vec{x},t) \equiv \int \mathrm{d} \vec{v} \, f^s(\vec{x}, \vec{v}, t) \psi_{i_1 i_2 \cdots i_N}^s (\vec{v}),

where :math:`f^s` is the particle distribution for species :math:`s` and

.. math::
   :label: polydef

   \label{ltm:eq:polydef}
     \psi_{i_1 i_2 \cdots i_N}^s (\vec{v}) = m^s v_{i_1} v_{i_2} \cdots v_{i_N}

is the moment polynomial of order :math:`N` in our convention. The
indices :math:`i_1, i_2, \ldots, i_N`, denote components in velocity
space. The full moment of order :math:`N` of a plasma is simply the sum
of the moments of each species:

.. math:: M_{i_1 i_2 \cdots i_N} = \sum_s M_{i_1 i_2 \cdots i_N}^s.

Henceforth we drop the superscript :math:`s` and restrict our attention
to moments of individual species.

Some low order moments have direct physical interpretations as fluid
quantities. For example, the moment of order :math:`0` is the **mass
density**

.. math:: \rho \equiv M = \int \mathrm{d} \vec{v} \, f(\vec{x}, \vec{v}, t) m;

the moment of order :math:`1` is the **momentum density**

.. math:: p_i \equiv M_i = \int \mathrm{d} \vec{v} \, f(\vec{x}, \vec{v}, t) m v_i;

the moment of order :math:`2` is the **stress tensor**

.. math:: P_{ij} \equiv M_{ij} = \int \mathrm{d} \vec{v} \, f(\vec{x}, \vec{v}, t) m v_i v_j;

its tensor contraction is the **total energy density**

.. math:: e \equiv \frac{1}{2} P_{ii};

and, a tensor contraction of the moment of order :math:`3` is the
**energy flux density**

.. math:: Q_i \equiv \frac{1}{2} M_{ijj}.

Higher order moments tend not to have such direct physical
interpretations, but still impose independent constraints on the shape
of the distribution. This is related to the Hamburger moment problem,
which asks whether or not a distribution can be uniquely identified from
knowledge of all of its moments. The first few low order moments
constrain the distribution sufficiently to allow for accurate modeling
of plasmas, and so the Hamburger moment problem is beyond our scope.

In PIC methods, each particle’s position in phase space is known
exactly, so the plasma’s distribution takes the form

.. math:: f(\vec{x}, \vec{v}, t) = \sum_{\alpha \in \textrm{particles}} \delta (\vec{x} - \vec{x}_\alpha (t)) \delta(\vec{v} - \vec{v}_\alpha(t)),

where :math:`\vec{x}_\alpha` and :math:`\vec{v}_\alpha` are the
Lagrangian spatial coordinates and velocity of particle :math:`\alpha`,
respectively, as functions of time. Substituting this into
Eq. :eq:`momdef` results in moments of the form

.. math:: M_{i_1 i_2 \cdots i_N} (\vec{x},t) = \sum_{\alpha \in \textrm{particles}} \delta (\vec{x} - \vec{x}_\alpha (t)) \psi_{i_1 i_2 \cdots i_N} (\vec{v}_\alpha(t)).

This form is not conducive to computer simulation, as it is unclear how
to handle the delta distribution. The PIC strategy is to coarse-grain it
by replacing it with a **particle shape factor**, whose purpose is to
approximate the delta distribution. Intuitively, shape factors smooth
out the sharp peak of the delta into a cloud of finite width. Generally,
the shape factor takes the form of a convolution kernel:

.. math:: \delta(\vec{x} - \vec{x}_\alpha) \rightarrow S(\vec{x}_\alpha, \vec{x}).

Thus the moments measured at :math:`\vec{x}` can be computed as

.. math:: M_{i_1 i_2 \cdots i_N} (\vec{x},t) = \sum_{\alpha \in \textrm{particles}} S(\vec{x}_\alpha (t), \vec{x}) \psi_{i_1 i_2 \cdots i_N} (\vec{v}_\alpha(t)).

Further simplification is dependent on the PIC implementation.

Using a uniform mesh allows us to write the shape function in a simpler
form:

.. math:: S(\vec{x}_\alpha,\vec{x}) = \frac{W(\vec{x}_\alpha - \vec{x})}{\Delta x^d},

where :math:`\Delta x` is the grid spacing, :math:`d` is the dimension
of the configuration space, and :math:`W` is some weighting function.
hPIC2 defaults to a linear weighting or cloud-in-cell (CIC) scheme, where
:math:`W` is defined as

.. math::

   W\left(\vec{\xi}\right) =
     \begin{cases}
       \prod_{i=1}^d \left( 1 - \frac{|\xi_i|}{\Delta x} \right) & \textrm{if } |\xi_i| < \Delta x \textrm{ for all } i \in \{ 1,2, \ldots, d \}, \\
       0 & \textrm{otherwise.}
     \end{cases}

For :math:`d=1`, :math:`W` takes the form of a tent function of width
:math:`2 \Delta x`.

While the shape factor is not required to be isotropic or symmetric, it
is required to be normalized in an :math:`L^p` sense. That is, it must
be the case that

.. math:: \int \mathrm{d} \vec{x} \, S(\vec{x}', \vec{x}) = 1.

This ensures that physical conservation laws, such as conservation of
charge, are satisfied.

Moments of the Boltzmann equation
'''''''''''''''''''''''''''''''''

Fluid equations are derived by taking moments of the Boltzmann equation.
To motivate the fluid method used by hPIC2, we will derive the general
form of the equation for the time evolution of moments of arbitrary
moment :math:`N`. In this section, we use an Einstein-like summation
convention and suppress function arguments for brevity where obvious.

The Boltzmann equation for a single species is given by

.. math:: \frac{\partial f}{\partial t} + v_i \frac{\partial f}{\partial x_i} + \frac{F_i}{m} \frac{\partial f}{\partial v_i} = \mathcal{C},

where :math:`F_i = q ( E_i + \epsilon_{ijk} v_j B_k )` is the Lorentz
force and :math:`\mathcal{C}` is a functional that encodes changes in
the distribution due to collisions. Note that

.. math::

   \frac{\partial F_i}{\partial v_i} = 0, \quad
     \frac{\partial v_i}{\partial x_i} = 0,

so that the Boltzmann equation can be rewritten as

.. math:: \frac{\partial f}{\partial t} + \frac{\partial}{\partial x_i} ( v_i f ) + \frac{\partial}{\partial v_i} \left( \frac{F_i}{m} f \right) = \mathcal{C}.

In order to obtain moments of the equation, we integrate both sides
against a moment polynomial. Multiplying both sides by the moment
polynomial :math:`\psi_{i_1 i_2 \cdots i_N}` results in

.. math::
   :label: boltzpoly

   \label{ltm:eq:boltzpoly}
     \frac{\partial}{\partial t} \left( \psi_{i_1 i_2 \cdots i_N} f \right) + \frac{\partial}{\partial x_k} \left( \psi_{i_1 i_2 \cdots i_N k} f \right) + \psi_{i_1 i_2 \cdots i_N} \frac{\partial}{\partial v_k} \left( \frac{F_k}{m} f \right) = \psi_{i_1 i_2 \cdots i_N} \mathcal{C}.

Integrating the last term on the left hand side by parts yields

.. math:: \psi_{i_1 i_2 \cdots i_N} \frac{\partial}{\partial v_k} \left( \frac{F_k}{m} f \right) = \cancel{\frac{\partial}{\partial v_k} \left( \frac{F_k}{m} \psi_{i_1 i_2 \cdots i_N} f \right)} - \frac{F_k}{m} f \frac{\partial \psi_{i_1 i_2 \cdots i_N}}{\partial v_k}.

We drop the first term on the right hand side because, when integrated,
the divergence theorem will allow us to integrate over the surface of a
sphere with radius extending to infinity, and :math:`f` is constrained
to decay faster than every polynomial. Using
Eq. :eq:`polydef`, the remaining term can be
manipulated to yield

.. math::
   :label: momlorentz

   \begin{aligned}
     \frac{F_k}{m} f \frac{\partial \psi_{i_1 i_2 \cdots i_N}}{\partial v_k}
     &= f \frac{q}{m} \left[ E_{i_1} \psi_{i_2 i_3 \cdots i_N} + E_{i_2} \psi_{i_1 i_3 \cdots i_N} + \cdots + E_{i_N} \psi_{i_1 i_2 \cdots i_{N-1}} \right. \nonumber \\
       &\quad + \left. B_k \epsilon_{j k i_1} \psi_{i_2 i_3 \cdots i_N j} + B_k \epsilon_{j k i_2} \psi_{i_1 i_3 \cdots i_N j} + \cdots + B_k \epsilon_{j k i_N} \psi_{i_1 i_2 \cdots i_{N-1} j} \right] \\
     &= N f \frac{q}{m} \left[ E_{\left( i_1 \right.} \psi_{\left. i_2 i_3 \cdots i_N \right)} + B_k \epsilon_{jk \left( i_1 \right.} \psi_{\left. i_2 i_3 \cdots i_N \right) j} \right], \label{ltm:eq:momlorentz}
   \end{aligned}

where the parentheses around the indices indicate a sum over all
permutations of these indices divided by :math:`N!`. Substituting
Eq. :eq:`momlorentz` into
Eq. :eq:`boltzpoly` results in

.. math:: \frac{\partial}{\partial t} \left( \psi_{i_1 i_2 \cdots i_N} f \right) + \frac{\partial}{\partial x_k} \left( \psi_{i_1 i_2 \cdots i_N k} f \right) - N f \frac{q}{m} \left[ E_{\left( i_1 \right.} \psi_{\left. i_2 i_3 \cdots i_N \right)} + B_k \epsilon_{jk \left( i_1 \right.} \psi_{\left. i_2 i_3 \cdots i_N \right) j} \right] = \psi_{i_1 i_2 \cdots i_N} \mathcal{C}.

Integrating this equation over velocity space finally yields

.. math::
   :label: momevol

   \label{ltm:eq:momevol}
     \frac{\partial M_{i_1 i_2 \cdots i_N}}{\partial t} + \frac{\partial M_{i_1 i_2 \cdots i_N k}}{\partial x_k} - N \frac{q}{m} \left[ E_{\left( i_1 \right.} M_{\left. i_2 \cdots i_N \right)} + B_k \epsilon_{jk \left( i_1 \right.} M_{\left. i_2 \cdots i_N \right) j} \right] = \int \mathrm{d} \vec{v} \, \psi_{i_1 i_2 \cdots i_N} \mathcal{C},

which is the equation for the time evolution of the moments of
:math:`f`.

The fluid solver internal to hPIC2 uses a 5-moment fluid model. These
moments are the fluid quantities mass density, momentum density
(comprising 3 quantities with :math:`d=3`), and total energy density.
Eq. :eq:`momevol` with suitable substitutions
and minor algebraic manipulations gives the equations governing these
quantities in a collisionless plasma:

.. math::

   \begin{aligned}
     \frac{\partial \rho}{\partial t} &= - \frac{\partial p_i}{\partial x_i}, \label{ltm:eq:rho} \\
     \frac{\partial p_i}{\partial t} &= - \frac{\partial P_{ij}}{\partial x_j} + \frac{q}{m} \left( \rho E_i + \epsilon_{ijk} p_j B_k \right), \label{ltm:eq:p} \\
     \frac{\partial e}{\partial t} &= - \frac{\partial Q_i}{\partial x_i} + \frac{q}{m} p_i E_i, \label{ltm:eq:e}
   \end{aligned}

where the collision term has been removed.

Implementation
^^^^^^^^^^^^^^

hPIC2 runs in a three dimensional velocity space, so we restrict our
attention to :math:`d=3` in this section.

A moment tensor of order :math:`N` contains :math:`3^N` entries. For
higher order moments, this consumes large amounts of memory, and is an
infeasible storage solution. However, not every element of a moment
tensor is unique. Note from Eqs. :eq:`momdef`
and :eq:`polydef` that the moment polynomials
(and, therefore, the moments themselves) are invariant under interchange
of two indices. In fact, if the indices of a moment tensor element are a
permutation the indices of another element, those two elements are
equal. That is,

.. math:: M_{i_1 i_2 \cdots i_N} = M_{i_{\sigma(1)} i_{\sigma(2)} \cdots i_{\sigma(N)}},

for any permutation :math:`\sigma` on :math:`\mathbb{Z}_3^N`.

To reduce memory use, it is desirable to store only unique tensor
elements. Since the moment tensors are symmetric, the number of unique
tensor elements is equal to the dimension of the space of symmetric
tensors, given by

.. math:: \dim \mathop{\mathrm{Sym}}^N \left( \mathbb{R}^3 \right) = \frac{(N+1)(N+2)}{2}.

This is always less than :math:`3^N` and is guaranteed to reduce memory
usage.

This memory reduction method introduces a problem for memory allocation.
The original :math:`3^N` tensor elements conveniently occupy a
:math:`3 \times 3 \times \cdots \times 3` array, where the number of
:math:`3`\ ’s is equal to :math:`N`. However, allocating and sparsely
populating such an array is time-consuming and wasteful. Instead, hPIC2
defines two two-dimensional arrays, which we shall call here
``momentsArray`` and ``indicesArray``. ``momentsArray`` is an array with
shape (number of unique tensor elements) :math:`\times` (number of hPIC2
nodes) that is used to store the value of each unique moment tensor
element at each grid point. Meanwhile, ``indicesArray`` is an array with
shape (number of unique tensor elements) :math:`\times` (moment order)
that is used to store the indices corresponding to the moment tensor
element of the same row in ``momentsArray``. As an example, if
``indicesArray[2] = [2 1 0]``, then ``momentsArray[2]`` contains the
values of :math:`M_{zyx}` at each grid point, since the indices 0, 1,
and 2 correspond to :math:`x`-, :math:`y`-, and :math:`z`-components,
respectively.

These two techniques allow hPIC2 to efficiently store the value of every
moment tensor element of arbitrary order at every grid point.

Hybrid-by-Species
~~~~~~~~~~~~~~~~~

Hybrid-by-Regions
~~~~~~~~~~~~~~~~~

Mesh
----

1D Non-uniform Grid
~~~~~~~~~~~~~~~~~~~

This section was prepared by

-  Huq Md Fazlul, UIUC

FD Stencil for 1D First Derivative
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let’s consider the problem,

.. math:: E_i = - \frac{d\phi}{dx}|_i

.. figure:: figures/nonuniform_mesh.png
   :alt:

Let’s consider the boundary conditions and grading ratio are,

.. math::

   \label{eq:1stdev1}
   \begin{aligned}
   \phi{(x_0)} = left\  bc = 0;\\
   \phi{(x_{n-1})} = right\  bc = 0;\\
   \Delta{x_i} = x_{i+1} - x_i = r\Delta{x_{i-1}};\\
   r = Grading\ ratio =\frac{\Delta{x_i}}{\Delta{x_{i-1}}};
   \end{aligned}

Now, using Taylor series expansion at :math:`\phi_{i+1}` we get,

.. math::

   \label{eq:1stdev2}
   \phi_{i+1} = \phi_i+(\Delta x_i) \frac{\partial \phi}{\partial x}|_{i}+\frac{\Delta x_i^2}{2!}\frac{\partial^2\phi}{\partial x^2}|_i +......

And, using Taylor series expansion at :math:`\phi_{i-1}` we get,

.. math::

   \label{eq:1stdev3}
   \phi_{i-1} = \phi_i-(\Delta x_{i-1}) \frac{\partial \phi}{\partial x}|_{i}+\frac{\Delta x_{i-1}^2}{2!}\frac{\partial^2\phi}{\partial x^2}|_i -......

Subtracting equation (`[eq:1stdev3] <#eq:1stdev3>`__) from equation
(`[eq:1stdev2] <#eq:1stdev2>`__) and ignoring higher order terms we get,

.. math::

   \label{eq:1stdev4}
   \phi_{i+1}-\phi_{i-1} = (\Delta x_i + \Delta x_{i-1})\frac{\partial \phi}{\partial x}|_{i}

Rearranging we get,

.. math::

   \label{eq:1stdev5}
   \frac {\partial \phi}{\partial x}|_i = \frac{\phi_{i+1}-\phi_{i-1}}{\Delta x_i + \Delta x_{i-1}} = \frac{r(\phi_{i+1}-\phi_{i-1})}{(r+1)\Delta x_i} = \frac{\phi_{i+1}-\phi_{i-1}}{(r+1)\Delta x_{i-1}}

Therefore, from equation (`[eq:1stdev1] <#eq:1stdev1>`__) we can write,

.. math::

   \label{eq:1stdev6}
   E_i = - \frac {\partial \phi}{\partial x}|_i = - \frac{\phi_{i+1}-\phi_{i-1}}{\Delta x_i + \Delta x_{i-1}} = - \frac{r(\phi_{i+1}-\phi_{i-1})}{(r+1)\Delta x_i} = - \frac{\phi_{i+1}-\phi_{i-1}}{(r+1)\Delta x_{i-1}}

FD Stencil for 1D Second Derivative
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let’s consider the problem,

.. math::
   :label: 2nddev1

   \label{eq:2nddev1}
   \nabla^2 \phi(x) = - \frac{\rho}{\epsilon_0}

.. figure:: figures/nonuniform_mesh.png
   :alt:

Let’s consider the boundary conditions and grading ratio are,

.. math::
   :label: 2nddev2

   \label{eq:2nddev2}
   \begin{aligned}
   \phi{(x_0)} = left\  bc = 0;\\
   \phi{(x_{n-1})} = right\  bc = 0;\\
   \Delta{x_i} = x_{i+1} - x_i = r\Delta{x_{i-1}};\\
   r = Grading\ ratio =\frac{\Delta{x_i}}{\Delta{x_{i-1}}};
   \end{aligned}

Now, using Taylor series expansion at :math:`\phi_{i+1}` we get,

.. math::
   :label: 2nddev3

   \label{eq:2nddev3}
   \phi_{i+1} = \phi_i+(\Delta x_i) \frac{\partial \phi}{\partial x}|_{i}+\frac{\Delta x_i^2}{2!}\frac{\partial^2\phi}{\partial x^2}|_i + \frac{\Delta x_i^3}{3!}\frac{\partial^3\phi}{\partial x^3}|_i + ......

And, using Taylor series expansion at :math:`\phi_{i-1}` we get,

.. math::
   :label: 2nddev4

   \label{eq:2nddev4}
   \phi_{i-1} = \phi_i-(\Delta x_{i-1}) \frac{\partial \phi}{\partial x}|_{i}+\frac{\Delta x_{i-1}^2}{2!}\frac{\partial^2\phi}{\partial x^2}|_i - \frac{\Delta x_{i-1}^3}{3!}\frac{\partial^3\phi}{\partial x^3}|_i + ......

Multiplying equation :eq:`2nddev4` by :math:`r` and
adding with equation :eq:`2nddev3` we get,

.. math::

   \label{eq:2nddev5}
   \phi_{i+1}+r\phi_{i-1} = (1+r)\phi_i+(\Delta x_i - r\Delta x_{i-1})\frac{\partial \phi}{\partial x}|_{i} +\frac{(\Delta x_i)^2 - r(\Delta x_{i-1})^2}{2}\frac{\partial^2\phi}{\partial x^2}|_i

Since :math:`\Delta{x_i} = r\Delta{x_{i-1}}`, second term of the right
hand side eliminated and we get,

.. math::

   \label{eq:2nddev6}
   \phi_{i+1}+r\phi_{i-1} = (1+r)\phi_i+\frac{(\Delta x_i)^2 - r(\Delta x_{i-1})^2}{2}\frac{\partial^2\phi}{\partial x^2}|_i

.. math::

   \label{eq:2nddev7}
   => r\phi_{i-1}-(r+1)\phi_i+\phi_{i+1} = \frac{(\Delta x_i)^2 - r(\frac{\Delta x_{i}}{r})^2}{2}\frac{\partial^2\phi}{\partial x^2}|_i

.. math::

   \label{eq:2nddev8}
   => r\phi_{i-1}-(r+1)\phi_i+\phi_{i+1} = \frac{(\Delta x_i)^2 - \frac{(\Delta x_{i})^2}{r}}{2}\frac{\partial^2\phi}{\partial x^2}|_i

.. math::

   \label{eq:2nddev9}
   => \frac{\partial^2\phi}{\partial x^2}|_i = \frac{r\phi_{i-1}-(r+1)\phi_i+\phi_{i+1}}{(\frac{r+1}{2r})(\Delta x_i)^2}

.. math::

   \label{eq:2nddev10}
   => \frac{\partial^2\phi}{\partial x^2}|_i = \frac{(\frac{2r^2}{r+1})\phi_{i-1}-2r\phi_i+(\frac{2r}{r+1})\phi_{i+1}}{(\Delta x_i)^2}

So, the discrete finite difference form of equation
:eq:`2nddev1` is,

.. math::

   \label{eq:2nddev11}
   => \frac{\partial^2\phi}{\partial x^2}|_i = \frac{(\frac{2r^2}{r+1})\phi_{i-1}-2r\phi_i+(\frac{2r}{r+1})\phi_{i+1}}{(\Delta x_i)^2} = -(\frac{\rho}{\epsilon_0})_i

Corresponding stencil is
(:math:`(\frac{2r^2}{r+1}), -2r, (\frac{2r}{r+1})`). So, the system of
linear equations are,

.. math::

   \phi_0 = 0;

   (\frac{2r^2}{r+1})\phi_0-2r\phi_1+(\frac{2r}{r+1})\phi_2 = (\Delta x_1)^2 (-(\frac{\rho}{\epsilon_0})|_1);

   (\frac{2r^2}{r+1})\phi_1-2r\phi_2+(\frac{2r}{r+1})\phi_3 = (\Delta x_2)^2 (-(\frac{\rho}{\epsilon_0})|_2);

   (\frac{2r^2}{r+1})\phi_2-2r\phi_3+(\frac{2r}{r+1})\phi_4 = (\Delta x_3)^2 (-(\frac{\rho}{\epsilon_0})|_3);

   \vdots

   (\frac{2r^2}{r+1})\phi_{n-3}-2r\phi_{n-2}+(\frac{2r}{r+1})\phi_{n-1} = (\Delta x_{n-2})^2 (-(\frac{\rho}{\epsilon_0})|_{n-2});

   \phi_{n-1} = 0;

Corresponding matrix-vector representation of system of linear equations
will be,

.. math::

   \label{eq:2nddev19}
   Ax = b

Where, the matrix :math:`A` is,

.. math::

   \label{eq:2nddev20}
   A = \begin{vmatrix}
   1&0&0&0&..&..&..&0\\
   \frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&0&..&..&..\\
   0&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&..&..&..\\
   ..&..&..&..&..&..&..&..\\
   ..&..&..&..&..&..&..&..\\
   0&..&..&..&..&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}\\
   0&0&..&..&..&..&0&1\\
   \end{vmatrix}

The vector :math:`x` is,

.. math::

   \label{eq:2nddev21}
   x = \begin{vmatrix}
   \phi_0\\
   \phi_1\\
   \phi_2\\
   ..\\
   ..\\
   \phi_{n-2}\\
   \phi_{n-1}
   \end{vmatrix}

The vector :math:`b` is,

.. math::

   \label{eq:2nddev22}
   b = \begin{vmatrix}
   0\\
   -((\Delta x_1)^2 (\frac{\rho}{\epsilon_0})_1)\\
   -((\Delta x_2)^2 (\frac{\rho}{\epsilon_0})_2)\\
   ..\\
   ..\\
   -((\Delta x_{n-2})^2 (\frac{\rho}{\epsilon_0})_{n-2})\\
   0
   \end{vmatrix} + \begin{vmatrix}
   left \ bc\\
   0\\
   0\\
   ..\\
   ..\\
   0\\
   right \ bc
   \end{vmatrix}

.. math::

   \label{eq:2nddev23}
   => b = \begin{vmatrix}
   left \ bc\\
   -((\Delta x_1)^2 (\frac{\rho}{\epsilon_0})_1)\\
   -((\Delta x_2)^2 (\frac{\rho}{\epsilon_0})_2)\\
   ..\\
   ..\\
   -((\Delta x_{n-2})^2 (\frac{\rho}{\epsilon_0})_{n-2})\\
   right \ bc
   \end{vmatrix}

Therefore the :math:`Ax = b` system of equations will be,

.. math::

   \label{eq:2nddev24}
   \begin{vmatrix}
   1&0&0&0&..&..&..&0\\
   \frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&0&..&..&..\\
   0&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&..&..&..\\
   ..&..&..&..&..&..&..&..\\
   ..&..&..&..&..&..&..&..\\
   0&..&..&..&..&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}\\
   0&0&..&..&..&..&0&1\\
   \end{vmatrix}
   \begin{vmatrix}
   \phi_0\\
   \phi_1\\
   \phi_2\\
   ..\\
   ..\\
   \phi_{n-2}\\
   \phi_{n-1}
   \end{vmatrix} = \begin{vmatrix}
   left \ bc\\
   -((\Delta x_1)^2 (\frac{\rho}{\epsilon_0})_1)\\
   -((\Delta x_2)^2 (\frac{\rho}{\epsilon_0})_2)\\
   ..\\
   ..\\
   -((\Delta x_{n-2})^2 (\frac{\rho}{\epsilon_0})_{n-2})\\
   right \ bc
   \end{vmatrix}

2D Nonuniform Grid
~~~~~~~~~~~~~~~~~~

Field Solver
------------

Collisions
----------

Coulomb collisions
~~~~~~~~~~~~~~~~~~

This section was prepared by:

-  Logan Meredith, UIUC

Coulomb collisions are long-range collisions that act under the Coulomb
potential between charged particles. In certain plasma regimes, Coulomb
collisions contribute significantly to plasma thermalization, especially
in strongly collisional plasmas where fluid approximations are
appropriate. Since hPIC2 assumes that electrons follow an analytical
Maxwell-Boltzmann distribution, collisions between ions and electrons
must be treated differently than those between ions and other ions. This
section will provide the necessary background for Coulomb collisions and
present the algorithms used for ion-electron and ion-ion Coulomb
collisions in both PIC and fluid solvers.

Recall that the Boltzmann equation for a single charged species
:math:`s` under only electromagnetic external forces is given by

.. math:: \frac{\partial f_s}{\partial t} + \vec{v} \cdot \frac{\partial f_s}{\partial \vec{x}} + \frac{q_s}{m_s} \left( \vec{E} + \vec{v} \times \vec{B} \right) \cdot \frac{\partial f_s}{\partial \vec{v}} = \mathcal{C}[f_s],

where :math:`f_s` is the single-particle distribution function,
:math:`q_s` and :math:`m_s` are the charge and mass of the species,
respectively, :math:`\vec{E}` and :math:`\vec{B}` are the
self-consistent electric and magnetic fields, respectively, and
:math:`\mathcal{C}` is a functional that encodes changes in the
distribution due to collisions, hereafter referred to as the collision
operator. Generally the collision operator takes the form

.. math:: \mathcal{C}[f_s] = \sum C_{\alpha} [f_s, f_t],

where :math:`C_\alpha [f_s, f_t]` is the collision operator for a single
collision type :math:`\alpha` occuring between species :math:`s` and
:math:`t`. Hence the full collision operator is properly the sum over
individual collision operators for all possible collisions.

Throughout this section, consider only Coulomb collisions operating
between species :math:`1` and mass :math:`2` with distributions
:math:`f_s, m_s, q_s` for :math:`s=1,2`. Henceforth the corresponding
Coulomb collision operator acting on species :math:`1` shall be denoted
:math:`C_{12}`.

Ion-electron Coulomb collisions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ion-electron collisions are handled differently in the PIC and fluid
versions of hPIC2. This section will describe the algorithms in both. We
also substitute subscripts :math:`1 \rightarrow i` and
:math:`2 \rightarrow e` to make the ion (:math:`i`) and electron
(:math:`e`) species notations more explicit.

A discussion of the role of the Coulomb logarithm is beyond the scope of
this document, but a sensible definition
from `Fitzpatrick <https://doi.org/10.1201/9781003268253>`_ is

.. math::

   \ln \Lambda =
       \begin{cases}
           30 - \ln \left( \sqrt{\frac{n_e Z_i^3}{(kT_i)^3}} A_i \right) & kT_e < kT_i m_e / m_i, \\
           23 - \ln \left( \sqrt{\frac{n_e}{(kT_e)^3}} Z_i \right) & kT_i m_e / m_i < kT_e < 10 Z_i^2 \text{ eV}, \\
           24 - \ln \left( \sqrt{n_e} (kT_e)^{-1} \right) & kT_e > 10 Z_i^2 \text{ eV},
       \end{cases}

where :math:`n_s` is the number density of species :math:`s`,
:math:`T_s` is the temperature of species :math:`s`,
:math:`Z_i \equiv q_i / q_e` is the ion charge number, and :math:`A_i`
is the ion mass number.

PIC
'''

Define the functions

.. math::

   \begin{aligned}
       F_1(\zeta) &= \mathop{\mathrm{erf}}(\zeta) - \zeta \frac{d \mathop{\mathrm{erf}}}{d \zeta}, \\
       F_2(\zeta) &= \left( 1 - 2 \zeta^2 \right) \mathop{\mathrm{erf}}(\zeta) - \zeta \frac{d \mathop{\mathrm{erf}}}{d \zeta}, \\
       F_3(\zeta) &= \left( 1 - \frac{2}{3} \zeta^2 \right) \mathop{\mathrm{erf}}(\zeta) - \zeta \frac{d \mathop{\mathrm{erf}}}{d \zeta},
   \end{aligned}

where :math:`\mathop{\mathrm{erf}}` is the error function. Also define
the constant

.. math:: \gamma_{ie} = \left( \frac{q_i q_e}{4 \pi \epsilon_0} \right)^2 2 \pi \ln \Lambda.

Exploiting the fact that :math:`m_e/m_i \ll 1` and the Maxwell-Boltzmann
electron distribution assumption yields an approximation for
:math:`C_{ie}` as

.. math:: C_{ie} = - \frac{1}{m_i} \frac{\partial}{\partial \vec{v}} \cdot \vec{A}_{ie},

where

.. math:: \vec{A}_{ie} = - \frac{\gamma_{ie} n_e}{m_e} \left\{ 2 F_1 \left( \frac{v}{v_{te}} \right) \frac{\vec{v}}{v^3} f_i(\vec{v}) + \frac{m_e}{m_i} \frac{v_{te}^2}{2 v^3} \left[ - F_2 \left( \frac{v}{v_{te}} \right) \stackrel{\leftrightarrow}{I} + 3 F_3 \left( \frac{v}{v_{te}} \right) \frac{\vec{v} \vec{v}}{v^2} \right] \cdot \frac{\partial f_i}{\partial \vec{v}} \right\},

where :math:`\stackrel{\leftrightarrow}{I}` is the identity tensor and
:math:`v_{te} = \sqrt{2 k T_e/m_e}`.

Suppose that :math:`f_i(\vec{v})` is a Maxwellian distribution of
characteristic number density :math:`n_i`, mean flow velocity
:math:`\vec{V}`, and temperature :math:`T_i`, so that

.. math:: f_i (\vec{v}) = n_i \left( \frac{m_i}{2 \pi T_i} \right)^{3/2} \exp \left( - \frac{m_i (\vec{v} - \vec{V})^2}{2 T_i} \right).

Using the fact that

.. math:: \frac{\partial f_i}{\partial \vec{v}} = - \frac{m_i}{T_i} ( \vec{v} - \vec{V} ) f_i,

we can write :math:`\vec{A}_{ie}` as

.. math::

   \begin{aligned}
   \vec{A}_{ie} (\vec{v}) &= - \frac{\gamma_{ie} n_e}{m_e} \left\{ 2 F_1 \left( \frac{v}{v_{te}} \right) \frac{\vec{v}}{v^3} - \frac{m_e}{T_i} \frac{v_{te}^2}{2 v^3} \left[ - F_2\left( \frac{v}{v_{te}} \right) (\vec{v} - \vec{V}) + 3 F_3\left( \frac{v}{v_{te}} \right) \frac{\vec{v}}{v^2} (v^2 - \vec{v} \cdot \vec{V}) \right] \right\} f_i (\vec{v}) \nonumber \\
   &= - \frac{\gamma_{ie} n_e}{m_e} \left\{ 2 F_1 \left( \frac{v}{v_{te}} \right) \vec{v} \frac{v_{te}^2}{v^3} \frac{m_e}{2 T_e} - \vec{v} \frac{v_{te}^2}{v^3} \frac{m_e}{2 T_i} \left[ 3 F_3 \left( \frac{v}{v_{te}} \right) - F_2 \left( \frac{v}{v_{te}} \right) \right] - \frac{m_e}{T_i} \frac{v_{te}^2}{2 v^3} \left[ F_2\left( \frac{v}{v_{te}} \right) \vec{V} - 3 F_3\left( \frac{v}{v_{te}} \right) \frac{\vec{v} \cdot \vec{V}}{v^2} \vec{v} \right] \right\} f_i(\vec{v}) \nonumber \\
   &= - \frac{\gamma_{ie} n_e}{m_e} \left\{ 2 F_1\left( \frac{v}{v_{te}} \right) \vec{v} \frac{T_i - T_e}{v^3 T_i} + \frac{T_e}{T_i} \left[ - \frac{F_2\left( \frac{v}{v_{te}} \right)}{v^3} \vec{V} + \frac{3 F_3\left( \frac{v}{v_{te}} \right)}{v^5} (\vec{v} \cdot \vec{V}) \vec{v} \right] \right\} f_i.
   \end{aligned}

Hence the collision operator can be written as

.. math:: C_{ie} = - \frac{1}{m_i} \frac{\partial}{\partial \vec{v}} \cdot \vec{A}_{ie} = - \frac{1}{m_i} \frac{\partial}{\partial \vec{v}} \cdot ( \vec{R}_{ie} f_i ),

where :math:`\vec{R}_{ie}` is a velocity-dependent effective force

.. math:: \vec{R}_{ie} = - \frac{\gamma_{ie} n_e}{m_e} \left\{ 2 F_1\left( \frac{v}{v_{te}} \right) \vec{v} \frac{T_i - T_e}{v^3 T_i} + \frac{T_e}{T_i} \left[ - \frac{F_2\left( \frac{v}{v_{te}} \right)}{v^3} \vec{V} + \frac{3 F_3\left( \frac{v}{v_{te}} \right)}{v^5} (\vec{v} \cdot \vec{V}) \vec{v} \right] \right\}.

Ion-electron Coulomb collisions are implemented in PIC by selecting a
stride :math:`N` and accelerating each affected ion macroparticle by
this effective force over :math:`N` time steps. Hence a given
macroparticle’s velocity :math:`\vec{v}` is incremented by
:math:`N \Delta t \vec{R}_{ie} / m_i`, where :math:`\Delta t` is the
simulation time step.

Fluid
'''''

In a seminal paper, `Braginskii <http://jetp.ras.ru/cgi-bin/dn/e_006_02_0358.pdf>`_
computed the fluid moments of :math:`C_{ie}` under the assumption that
both the ion and electron distributions were Maxwellian, which is
conveniently congruent with hPIC2’s assumptions for its internal fluid
solver. The relevant moments are

.. math::

   \begin{aligned}
       \int_{\mathbb{R}^3} d \vec{v} \, m_i C_{ie} &= 0, \\
       \int_{\mathbb{R}^3} d \vec{v} \, m_i \vec{v} C_{ie} &= - \vec{R}, \\
       \int_{\mathbb{R}^3} d \vec{v} \, \frac{1}{2} m_i v^2 C_{ie} &= - \vec{R} \cdot \vec{V} + Q_{\Delta},
   \end{aligned}

where

.. math::

   \begin{aligned}
       \vec{R} &= \frac{m_e n_e}{\tau_e} \vec{V}, \\
       Q_{\Delta} &= \frac{3 m_e}{m_i} \frac{n_e}{\tau_e} k (T_e - T_i),
   \end{aligned}

with

.. math:: \tau_e = \frac{6 \sqrt{2} \pi^{3/2} \epsilon_0^2 \sqrt{m_e} (kT_e)^{3/2}}{\ln \Lambda q_e^4 n_i},

as derived by `Fitzpatrick <https://doi.org/10.1201/9781003268253>`_.
These moments are added as sources to the relevant fluid moment
evolution equations.

Application Programming Interface
=================================

Data Structures
---------------

Functions
---------

PUMI Mesh Routines
~~~~~~~~~~~~~~~~~~

This section was prepared by:

-  Vignesh Vittal Srinivasaragavan, RPI

The following routines are implemented in PUMI to calculate the element
size, nodal grading ratio and nodal covolume.

-  | ``pumi_BL_elemsize_ON(*pumi_mesh)``
   | Allocates memory for BL element size arrays (for each submesh),
     calculates/stores them

-  | ``pumi_BL_elemsize_OFF(*pumi_mesh)``
   | Deallocates memory for BL element size arrays (for each submesh)

-  | ``pumi_return_elemsize(*pumi_mesh, index, offset)``
   | Returns element size for a given global node/element index

-  | ``pumi_return_gradingratio(*pumi_mesh, index)``
   | Returns grading ratio for a given global node index

-  | ``pumi_return_covolume(pumi_mesh_t* pumi_mesh, int inode)``
   | Returns the covoume assocaited with a given node

Some comments/remarks on routine that calculates the element size

-  ``pumi_return_elemsize()`` routine returns the element size for a
   given global index

-  If nodal index is passed as the argument, an offset, either 0 or -1,
   will be defined such that it returns the size of right or left
   element associated with the node respectively

-  If the index corresponds to a boundary layer element, the function
   will return the appropriate value from the BL element size array
   calculated by ``pumi_BL_elemsize_ON()``

-  If ``pumi_BL_elemsize_ON()`` was not previously called by user, then
   the routine will compute the BL element size using ``pow()`` function
   (which is inefficient)

-  In case of uniform elements, the routine directly accesses and
   returns the element size from ``struct pumi_submesh1D``

-  ``enum pumi_elemsize_index_offset`` is defined in ``pumi_routines.h``
   to avoid the confusion in specifying the offset argument in the
   routine

-  If element index is passed to the routine (i.e in place of
   ``index``), the offset can be specified as ``elem_input_offset``
   (which corresponds to value 0)

-  If node index is passed to the routine, then to calculate size of
   element to the left of the node, offset should be
   ``node_input_right_elem_offset`` (which corresponds to value 0)

-  If node index is passed to the routine, then to calculate size of
   element to the right of the node, offset should be
   ``node_input_left_elem_offset`` (which corresponds to value -1)

-  ``pumi_return_gradingratio()`` routine will return the ratio between
   the element sizes associated with a given node

-  For a given node index :math:`i`, the grading ratio (GR) is

   .. math:: GR(i) = \frac{\Delta x(i)}{\Delta x(i-1)}

   where :math:`\Delta x(i)` is the size of :math:`i^{th}` element

-  The routine will take into account if the node is shared between
   submeshes and return the appropriate grading ratio

-  Grading ratio is not defined at first and last node of the domain

Workflow
--------
