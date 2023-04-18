Fluids
======

This page desecribes the numerical methods used to solve the Euler
equations described in the :ref:`species:Euler fluid` section.
The fluid equations are solved broadly using the method of lines,
in which the system is first partially discretized in space,
and the resulting system of ordinary differential equations
is then discretized in time.

Discontinuous Galerkin spatial
------------------------------

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

    \vec{u}^{n+1} = \vec{u}^n + \Delta t \sum_{i=1}^s b_i \vec{k}_i,

where

.. math::

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

Boundary Conditions
-------------------

Slope limiters
--------------
