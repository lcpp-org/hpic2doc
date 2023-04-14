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
The

Runge-Kutta Time Stepping and Sub-stepping
------------------------------------------

Riemann solvers
---------------

Boundary Conditions
-------------------

Slope limiters
--------------
