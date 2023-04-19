Fluids
======

This page desecribes the numerical methods used to solve the Euler
equations described in the :ref:`species:Euler fluid` section.
The fluid equations are solved broadly using the method of lines,
in which the system is first partially discretized in space,
and the resulting system of ordinary differential equations
is then discretized in time.

Discontinuous Galerkin spatial discretization
----------------------------------------------

Discontinuous Galerkin (DG) methods can be thought of as finite element
methods that incorporate aspects of the finite volume method.
In contrast with the more common continuous Galerkin method,
DG methods define a separate finite element space for each element in
the mesh,
so that finite element solutions are not constrained to be continuous.
This renders the linear algebra extremely local,
since the finite element solution in a given element is influenced
only by immediately adjacent elements.
Parallelism is therefore relatively easy with DG methods.

Note that the Euler equations can be written in conservative form

.. math::
    :label: fluids:conservation

    \frac{\partial u}{\partial t} + \nabla \cdot \vec{F} = G,

where :math:`\vec{F} = \vec{F} (u)` is a flux functional
and the source :math:`G = G(\vec{x}, t, u, \nabla \phi, \vec{B})`
may depend on space, time, the fluid state, and the electromagnetic fields.

In hPIC2, fluids can only be used with
:ref:`admissible unstructured meshes <mesh:Unstructured mesh>`.
Let :math:`\mathcal{T}_h` be such a mesh on
the polyhedral problem domain :math:`\Omega`.
Let :math:`\mathcal{F}_I` be the set of interior faces in
:math:`\mathcal{T}_h`,
with the understanding that in two dimensions, edges are faces,
and in one dimension, vertices are faces.
Similarly, let :math:`\mathcal{F}_B` be the set of faces in
:math:`\mathcal{T}_h` that lie on :math:`\partial \Omega`.

Define

.. math::

    H^s(\mathcal{T}_h) = \left\{ \psi \in L^2(\Omega) \mid \forall T \in \mathcal{T}_h, \psi_{\mid T} \in H^s (T) \right\},

where :math:`H^s(T)` is a Sobolev space of order :math:`s > 1/2`
on the mesh element :math:`T`.
The weak form of :eq:`fluids:conservation`
are essentially derived by choosing an element :math:`T \in \mathcal{T}_h`,
multiplying both sides by some :math:`\psi \in H^2(T)`,
and integrating by parts over :math:`T` to yield

.. math::

    \frac{\mathrm{d}}{\mathrm{d} t} \int_T u \psi \, \mathrm{d} V +
    \int_{\partial T} \vec{F} \cdot \hat{n} \psi \, \mathrm{d} A -
    \int_T \vec{F} \cdot \nabla \psi \, \mathrm{d} V =
    \int_T G \psi \mathrm{d} V,

where :math:`\hat{n}` is the outward-facing unit normal on
:math:`\partial T`.

For fluids, it is appropriate to approximate the flux on faces as the flux
arising from the solution to the Riemann problem on that face,
so that

.. math::
    :label: fluids:numerical_flux

    \int_{\partial T} \vec{F} \cdot \hat{n} \psi \, \mathrm{d} A \approx
    \int_{\partial T} h(u^-, u^+) \psi \, \mathrm{d} A,

where :math:`h(u^-, u^+)` is the solution to the Riemann problem
for the flux at the interface,
using :math:`u^+`, the state just outside of :math:`T`,
as the "right" state,
and :math:`u^-`, the state just inside of :math:`T`,
as the "left" state.
Hence the weak form becomes

.. math::
    :label: fluids:dg_weak_form

    \frac{\mathrm{d}}{\mathrm{d} t} \int_T u \psi \, \mathrm{d} V +
    \int_{\partial T} h(u^-, u^+) \psi \, \mathrm{d} A -
    \int_T \vec{F} \cdot \nabla \psi \, \mathrm{d} V =
    \int_T G \psi \mathrm{d} V.

A weak solution :math:`u` satisfies :eq:`fluids:dg_weak_form`
for all :math:`T \in \mathcal{T}_h`
and for all :math:`\psi \in H^s(\mathcal{T}_h)`.

It is obviously impossible to verify a potential solution :math:`u`
against every :math:`psi` in an infinite-dimensional space.
We therefore constrain our attention to a finite-dimensional subspace
:math:`V_h \in H^s(\mathcal{T}_h)`,
for which there exists a finite basis.
:math:`V_h` is known as the finite element space.
In the DG method, it is convenient to choose a basis consisting of functions
that are supported on a single element.
For each :math:`T \in \mathcal{T}_h`, we construct a finite basis
:math:`\{\psi_1^T, \ldots, \psi_N^T\}` of size :math:`N = N(T)`.
Then the finite element space is the span of the union of bases in
every element,
:math:`V_h = \text{span } \cup_{T \in \mathcal{T}_h} \{\psi_1^T, \ldots, \psi_{N(T)}^T\}`.
Henceforth we suppress the :math:`T` dependence where it is clear, for brevity.

We are considering only weak solutions in the finite element space,
so that

.. math::

    u_h|_T (\vec{x}, t) = \sum_{i=1}^N u_i(t) \psi_i(\vec{x}),

for some :math:`u_i \in \mathbb{R}`.
:eq:`fluids:dg_weak_form` becomes

.. math::
    :label: fluids:finite_weak_form

    \frac{\mathrm{d}}{\mathrm{d} t} \sum_{i=1}^N u_i \int_T \psi_i \psi_j \, \mathrm{d} V +
    \int_{\partial T} h(u_h^-, u_h^+) \psi_j \, \mathrm{d} A -
    \int_T \vec{F}(u_h) \cdot \nabla \psi_j \, \mathrm{d} V =
    \int_T G(u_h) \psi_j \mathrm{d} V,

when tested against a basis function :math:`\psi_j`.

Let :math:`M` be the :math:`N \times N` matrix with entries

.. math::

    M_{ij} = \int_T \psi_i \psi_j \, \mathrm{d}V,

and let
:math:`K_{\mathrm{face}}`,
:math:`K_{\mathrm{flux}}`,
:math:`K_{\mathrm{source}}`
be the nonlinear maps defined by

.. math::

    K_{\mathrm{face}, j} (\vec{y}) =
    - \int_{\partial T} h \left( \sum_{i=1}^N y_i \psi_i, u_h^+ \right) \psi_j \, \mathrm{d} A,

    K_{\mathrm{flux}, j} (\vec{y}) =
    \int_T \vec{F}\left( \sum_{i=1}^N y_i \psi_i \right) \cdot \nabla \psi_j \, \mathrm{d} V

    K_{\mathrm{source}, j} (\vec{y}, t) =
    \int_T G\left( \sum_{i=1}^N y_i \psi_i \right) \psi_j \mathrm{d} V

Then, with :math:`\vec{u} = (u_1, \ldots, u_N)^t`
and :math:`R = M^{-1} (K_{\mathrm{face}} + K_{\mathrm{flux}} + K_{\mathrm{source}})`,
:eq:`fluids:finite_weak_form` can be written as

.. math::
    :label: fluids:ode

    \frac{\mathrm{d} \vec{u}}{\mathrm{d} t} =
    R (\vec{u}, t).

Since the basis functions are usually taken to be polynomials,
these integrals are typically computed using Gaussian quadrature.

Slope limiters
--------------

Godunov's theorem :cite:`godunov1959finite` states that a linear, monotone
scheme for partial differential equations can be at most first-order accurate.
The contrapositive of this statement is that linear high-order schemes
necessarily introduce spurious oscillations,
Gibbs phenomena, that do not appear in the exact solutions.
Though the RKDG discretization of the Euler equations is far from linear,
the specter of Godunov's theorem haunts us still:
the scheme suffers from Gibbs phenomena near discontinuities.

Many techniques have been introduced throughout the computational fluid
dynamics literature to reduce these oscillations.
Artificial viscosity introduces non-physical diffusive terms to the Euler
equations that are mostly quiescent in smooth regions but gradually
turn on near discontinuities in order to spread out shocks
:cite:`vonneumann1950method`.
Weighted essentially non-oscillatory schemes modify the polynomial interpolation
stencil in areas near discontinuities in order to reduce oscillations
:cite:`liu1994weighted`.
Limiters reduce either the fluxes (flux limiters) or the states themselves
(slope limiters) to reasonable values where gradients are great.
Limiters are generally difficult to extend to high-order DG spatial
discretizations,
but recent research has expanded the number of options.
Throughout this page, we will denote the action of the limiter as :math:`L`,
so that a limited solution is given by :math:`\tilde{u} = L(\vec{u})`.

Moe limiter
~~~~~~~~~~~~

The limiter due to Moe *et al.* is simple to implement and generalizable
to RKDG schemes of arbitrary order :cite:`moe2015simple`.
The procedure is as follows:

#. Select a set of variables to use for checking gradients, :math:`w`.
   The authors suggest using primitive variables in fluid dynamics
   because of their Galilean invariance.
   For the Euler equations, the primitive variables are the mass density
   :math:`mn`,
   the bulk velocity :math:`\vec{u}`,
   and the pressure :math:`p`.
   Also, for each element :math:`i`, select points :math:`\chi_i` at which
   :math:`w` will be interpolated to check cell extrema.
   The authors suggest using corners and both internal and edge quadrature
   points,
   *i.e.*, the points used for the numerical integration of the integrals
   in :eq:`fluids:dg_weak_form`.

#. For each mesh element :math:`i` and each component :math:`l` of :math:`w`,
   compute the cell-local extrema of :math:`w` as

   .. math::

      w_{M_i}^l = \max_{\vec{x} \in \chi_i} \left\{ w^l(\vec{x}) \right\},

      w_{m_i}^l = \min_{\vec{x} \in \chi_i} \left\{ w^l(\vec{x}) \right\}.

#. For each mesh element :math:`i` and each component :math:`l` of :math:`w`,
   compute extrema over the set of neighbors :math:`N_i`, excluding
   the element :math:`i` itself, as

   .. math::

      M_i^l = \max \left\{ \bar{w}_i^l + \alpha(h), \max_{j \in N_i} \left\{ w_{M_j}^l \right\} \right\},

      m_i^l = \min \left\{ \bar{w}_i^l - \alpha(h), \min_{j \in N_i} \left\{ w_{m_j}^l \right\} \right\},

   where :math:`\bar{w}_i^l` is the element average of :math:`w^l`
   in element :math:`i`
   and :math:`\alpha` is a function that adds a tolerance that decreases
   with characteristic element size :math:`h`.
   The authors generally suggest the use of

   .. math::

      \alpha(h) = 500 h^{3/2},

   but in examples with extreme gradients, they reduce the constant
   in front while maintaining the :math:`h^{3/2}` dependence.
   The authors also suggest defining :math:`N_i` to be the set of elements
   that share a common edge with element :math:`i` for Cartesian grids
   and the set of elements that share a common vertex with element :math:`i`
   for unstructured meshes.
   However, the additional coding difficulty of identifying elements sharing
   a common vertex means that hPIC2 simply always looks for common edges.
   The authors warn that the results are more diffusive,
   which is acceptable.

#. For each element :math:`i`, compute

   .. math::

      \theta_{M_i} = \min_l \left\{ \phi \left( \frac{M_i^l - \bar{w}_i^l}{w_{M_i}^l - \bar{w}_i^l} \right) \right\},

      \theta_{m_i} = \min_l \left\{ \phi \left( \frac{m_i^l - \bar{w}_i^l}{w_{m_i}^l - \bar{w}_i^l} \right) \right\},

   where :math:`\phi` is a cutoff function.
   The authors suggest the use of the function

   .. math::

      \phi(y) = \min \left\{ \frac{y}{1.1}, 1 \right\}.

#. For each element :math:`i`, compute

   .. math::

      \theta_i = \min \{ 1, \theta_{m_i}, \theta_{M_i} \}.

#. For each element :math:`i`,
   limit the finite element solution of the conservative variables
   :math:`u_h` as

   .. math::

      \tilde{u}_h|_{T_i} (\vec{x}, t) = \bar{u}_i + \theta_i \left( u_h|_{T_i} ( \vec{x}, t) - \bar{u}_i \right).

Runge-Kutta Time Stepping and Sub-stepping
------------------------------------------

Now that we have reduced our problem to a coupled system of ordinary
differential equations,
we may use one of a number of numerical methods for discretizing in time.
Runge-Kutta (RK) methods compute approximate solutions at intermediate
stages between the current simulation time step and the next time step,
then evaluate the solution at the next time step as a weighted average
of the estimates at the stages.
This is in contrast to linear multistep methods,
which use the solution from perhaps several previous time steps to
evaluate the solution at the next time step.
RK methods have the distinct advantage that initial conditions are simpler to
specify.

Throughout this section,
let :math:`\vec{u}^n = \vec{u}(t_0 + n \Delta t)`
and :math:`t^n = t_0 + n \Delta t`,
where :math:`t_0` is the initial time
and :math:`\Delta t` is the time step size.
Generally, RK methods proceed as

.. math::
    :label: fluids:rk_next_step

    \vec{u}^{n+1} = \vec{u}^n + \Delta t \sum_{i=1}^s b_i \vec{k}_i,

where

.. math::
    :label: fluids:stages

    \vec{k}_i = R(\vec{u}^n + \Delta t \sum_{j=1}^s a_{ij} \vec{k}_j, t^n + c_i \Delta t)

for real :math:`c_i`, :math:`a_{ij}`, and :math:`b_i`.
An RK method is uniquely specified by the choices of these constants,
which are often presented in a Butcher tableau

.. math::
    :nowrap:

    \begin{array}{c|cccc}
    c_1 & a_{11} & a_{12} & \cdots & a_{1s} \\
    c_2 & a_{21} & a_{22} & \cdots & a_{2s} \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    c_s & a_{s1} & a_{s2} & \cdots & a_{ss} \\
    \hline
        & b_1 & b_2 & \cdots & b_s
    \end{array}

The subset of explicit RK methods is particularly important for fluid solvers
in plasma physics.
For explicit methods, the stages are of the form

.. math::

    \vec{k}_i = R(\vec{u}^n + \Delta t \sum_{j=1}^{i-1} a_{ij} \vec{k}_j, t^n + c_i \Delta t),

*i.e.*, a given stage depends only on previous stages.
Butcher tableaus for explicit RK methods therefore appear lower triangular

.. math::
    :nowrap:

    \begin{array}{c|cccc}
    c_1 \\
    c_2 & a_{21} \\
    \vdots & \vdots & \ddots \\
    c_s & a_{s1} & \cdots & a_{s,s-1} \\
    \hline
        & b_1 & \cdots & b_{s-1} & b_s
    \end{array}

RK methods that are not explicit are implicit.
Implicit methods require the solution of systems of equations at at least
some stages,
which, in the case of the Euler equations, will be nonlinear.
However, explicit methods tend to have much smaller regions of
numerical stability than implicit methods;
that is, explicit methods typically demand a smaller time step for stability.

While different explicit RK methods have different regions of stability,
the stable time step is typically a linear function of the characteristic
timescales of the system.
We shall simply state them here.
Fluids are associated with a signal speed timescale that goes as

.. math::

    t_{\text{s}} = \frac{h}{c + u},

where :math:`h` is a characteristic length scale of the system
(usually the size of a mesh element),
:math:`c` is the sound speed,
and :math:`u` is the bulk or advection speed of the fluid.
Generally, the sound speed can be computed as

.. math::

    c = \sqrt{\frac{\partial p}{\partial (mn)}},

where the derivative is computed assuming constant entropy.
For the ideal gas law EOS presented in the :ref:`species:Euler fluid` section,
this reduces to

.. math::

    c = \sqrt{\gamma \frac{p}{mn}}.

The source terms :math:`G` in the Euler equations may introduce additional
timescales.
For example, the timescale associated with the electric field acceleration
in the Lorentz force term is the plasma oscillation period

.. math::

    t_{\text{p}} = 2 \pi \sqrt{\frac{m \epsilon_0}{n q^2}}.

Similarly, the timescale associated with the magnetic field
in the Lorentz force term is the cyclotron period

.. math::

    t_{\text{c}} = \frac{2 \pi m}{q B}.

In fluid solvers, the time step is usually chosen to be

.. math::

    \Delta t = C t_{\text{min}},

where :math:`C > 0` is called the Courant-Friedrichs-Lewy (CFL) number
and :math:`t_{\text{min}}` is the minimum timescale in the simulation.
Most explicit RK methods require :math:`C \leq 1`.
Implicit methods may permit much larger CFL numbers.

Fluids in plasmas are associated with widely varying timescales.
In most problems, :math:`t_{\text{p}} \ll t_{\text{c}} \ll t_{\text{s}}`.
In this case, we say that the stiffest timescale is associated with the
Lorentz force source term.
It is possible to implicitly evolve the stiff terms while explicitly
evolving the non-stiff ones.
This means that the time step is no longer constrained by the stiff timescales,
but the non-stiff terms are still efficiently evolved explicitly.
Such methods are called IMplicit-EXplicit (IMEX).
Suppose that we can write the operator in :eq:`fluids:ode` as

.. math::

    R = R_{\text{E}} + R_{\text{I}},

where :math:`R_{\text{E}} = R_{\text{E}}(\vec{u}, t)`
contains the terms to be evolved explicitly and
:math:`R_{\text{I}} = R_{\text{I}} (\vec{u}, t)`
contains the terms to be evolved implicitly.
(This is indeed possible for the Euler equations coupled to the
Lorentz force.)
IMEX methods proceed as

.. math::

    \vec{u}^{n+1} = \vec{u}^n + \Delta t \sum_{i=1}^s b_i \vec{k}_i + \Delta t \sum_{i=1}^s \hat{b}_i \hat{k}_i,

where

.. math::

    \vec{k}_i = R_{\text{I}}(\vec{u}^n + \Delta t \sum_{j=1}^s a_{ij} \vec{k}_j, t^n + c_i \Delta t),

    \hat{k}_i = R_{\text{E}}(\vec{u}^n + \Delta t \sum_{j=1}^{i-1} \hat{a}_{ij} \hat{k}_j, t^n + \hat{c}_i \Delta t),

and the hatted RK constants form a lower triangular Butcher tableau.

When limiters are used, it is actually more common to use limited values
in the stages, so that :eq:`fluids:stages` becomes

.. math::

    \vec{k}_i = R\left( L \left( \vec{u}^n + \Delta t \sum_{j=1}^s a_{ij} \vec{k}_j \right) , t^n + c_i \Delta t \right)

and :eq:`fluids:rk_next_step` becomes

.. math::

    \vec{u}^{n+1} = L \left( \vec{u}^n + \Delta t \sum_{i=1}^s b_i \vec{k}_i \right),

for some choice of limiter :math:`L`.

The use of an RK method allows us to adaptively change the time step
during the simulation.
If enabled, hPIC2 will perform a reduction over all fluid degrees of freedom
across the entire domain to determine the minimum numerical timescale,
and thence a suitable time step.
hPIC2 will then choose the minimum between this suitable fluid time step
and the overall PIC time step.
If the fluid's suitable time step is less than the PIC time step,
this process will continue until the fluid reaches the next PIC time step.
This process is called adaptive sub-stepping.

LTM after limiters are described, draw a diagram depicting the
interleaved PIC-fluid time stepper.

Riemann solvers
---------------

As desecribed in the `Discontinuous Galerkin spatial discretization`_ section,
the numerical flux through interfaces is approximated in
:eq:`fluids:numerical_flux`
as the solution to a Riemann problem.
Exact solutions to Riemann problems for the Euler equations can be difficult
to compute,
so a vast body of literature has been dedicated to approximate Riemann solvers
:cite:`toro2013riemann`.
Such Riemann solvers are used throughout the field of computational
fluid dynamics,
and the choice of Riemann solver can mean the difference between a
well resolved, stable solution and numerical catastrophes.

A Riemann problem is an initial value problem for a conservation equation
with piecewise constant inital conditions consisting of a
single discontinuity at the origin.
Consider :eq:`fluids:conservation` in an infinite domain with
initial data

.. math::

    u(\vec{x}, 0) =
    \begin{cases}
        u_{\text{L}} & \text{if} & x < 0, \\
        u_{\text{R}} & \text{if} & x > 0.
    \end{cases}

We are interested in the solution at the origin at some later time :math:`t>0`.
In fact, in :eq:`fluids:numerical_flux`,
we only need the *flux* of the solution at the origin.
Many Riemann solvers return the approximate flux solution without
stating the solution itself.

Some examples of Riemann solvers are described below.

Harten-Lax-van Leer solver
~~~~~~~~~~~~~~~~~~~~~~~~~~

The Harten-Lax-van Leer (HLL) solver estimates the state as

.. math::

    u(\vec{x}, t) =
    \begin{cases}
        u_{\text{L}} & \text{if} & \frac{x}{t} \leq s_{\text{L}}, \\
        u_{\text{HLL}} & \text{if} & s_{\text{L}} \leq \frac{x}{t} \leq s_{\text{R}}, \\
        u_{\text{R}} & \text{if} & \frac{x}{t} \geq s_{\text{R}},
    \end{cases}

where the :math:`s_{\cdot}` are signal speeds on either side of the
discontinuity and

.. math::

    u_{\text{HLL}} = \frac{s_{\text{R}} u_{\text{R}} - s_{\text{L}} u_{\text{L}} + F_x(u_\text{L}) - F_x(u_\text{R})}{s_{\text{R}} - s_{\text{L}}}.

By using the Rankine-Hugoniot conditions, we can compute the
corresponding fluxes for use as the numerical DG flux as

.. math::

    h_{\text{HLL}} (u^-, u^+) =
    \begin{cases}
        \vec{F}(u^-) \cdot \hat{n} & \text{if} & 0 \leq s^-, \\
        \frac{\left[ s^+ \vec{F}(u^-) - s^- \vec{F}(u^+) \right] \cdot \hat{n} + s^- s^+ (u^+ - u^-)}{s^+ - s^-} & \text{if} & s^- \leq 0 \leq s^+, \\
        \vec{F}(u^+) \cdot \hat{n} & \text{if} & 0 \geq s^+.
    \end{cases}

There are a number of possible estimates for the signal speeds.
A simple choice is :cite:`davis1988simplified`

.. math::

    s^- = \vec{u}^- \cdot \hat{n} - c^-,

    s^+ = \vec{u}^+ \cdot \hat{n} + c^+,

where :math:`\vec{u}^{\cdot}` and :math:`c^{\cdot}`
are the advection velocity and sound speed, respectively.

Rusanov solver
~~~~~~~~~~~~~~

The Rusanov solver :cite:`rusanov1961calculation`,
also known as the local Lax-Friedrichs (LLF) solver,
is an extremely robust though overly diffusive solver
that can be considered a special case of the HLL solver
for certain choices of signal speeds.
The numerical DG flux is given by

.. math::

    h_{\text{LLF}} (u^-, u^+) =
    \frac{1}{2} \left[ \vec{F}(u^-) + \vec{F}(u^+) \right] \cdot \hat{n} -
    \frac{1}{2} s^* (u^+ - u^-),

where :math:`s^*` is a single signal speed.
A typical choice is :cite:`davis1988simplified`

.. math::

    s^* = \max \{ |\vec{u}^-| + c^-, |\vec{u}^+| + c^+ \}.

Boundary Conditions
-------------------

Boundary conditions are typically applied by considering a "ghost" fluid state
just on the outside of the domain and computing the resulting numerical flux
in :eq:`fluids:numerical_flux`.
Some examples are described below.

Wall boundary conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

An impermeable wall boundary condition can be modeled by making the ghost
fluid state equal to the inner state,
but with a bulk velocity that has been reversed normal to the boundary.
That is, if the state just inside of the wall is

.. math::

    u^- =
    \begin{Bmatrix}
    mn^- \\
    mn\vec{u}^- \\
    nmE^-
    \end{Bmatrix},

the state just outside of the wall should be set to

.. math::

    u^+ =
    \begin{Bmatrix}
    mn^- \\
    mn\vec{u}^- - 2 \hat{n} ( mn \vec{u} \cdot \hat{n}) \\
    m n E^-
    \end{Bmatrix}.

This ensures that the boundary effectively acts as a wall.

Copy-out boundary conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Outflow boundary conditions are notoriously difficult to impose for
Euler fluids.
A crude approximation is to simply copy the inner fluid state to the ghost
state and compute the resulting numerical flux;
that is, :math:`u^+ = u^-`.
This is perfectly adequate for supersonic flows normal to the boundary,
whose characteristics all extend out of the domain.
For subsonic flows, this type of boundary will spuriously reflect some waves.

Far-field boundary conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another possible method for handling outflow boundaries is to specify that
the ghost state has zero density, momentum density, and total energy density.
If generalized to possibly nonzero ghost states,
this boundary condition approximates contact with a static fluid reservoir.
