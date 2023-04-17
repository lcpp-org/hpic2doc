Fluids
======

This page desecribes the numerical methods used to solve the Euler
equations described in the :ref:`species:Euler fluid` section.

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

    \frac{\mathrm{d} \vec{u}}{\mathrm{d} t} =
    R (\vec{u}, t).

Since the basis functions are usually taken to be polynomials,
these integrals are typically computed using Gaussian quadrature.

Runge-Kutta Time Stepping and Sub-stepping
------------------------------------------

Riemann solvers
---------------

Boundary Conditions
-------------------

Slope limiters
--------------
