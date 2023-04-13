Species
========

This page describes the different models that hPIC2 can use for
a plasma species.

Full-orbit particles
----------------------

Boltzmann electrons
----------------------

Euler fluid
------------

Many important physical quantities can be computed as moments
of a distribution in velocity space.
The number density :math:`n = n(\vec{x}, t)` of a species
described by the distribution :math:`f` can be computed as

.. math::

    n = \int_{\mathbb{R}^3} f \, \mathrm{d} \vec{v};

the momentum density :math:`n m \vec{u} = n m \vec{u}(\vec{x}, t)` is

.. math::

    n m \vec{u} = \int_{\mathbb{R}^3} m \vec{v} f \, \mathrm{d} \vec{v};

the stress tensor :math:`P_{ij} = P_{ij} (\vec{x}, t)` is

.. math::

    P_{ij} = \int_{\mathbb{R}^3} m v_i v_j f \, \mathrm{d} \vec{v};

and the energy flux density :math:`\vec{Q} = \vec{Q}(\vec{x}, t)` is

.. math::

    \vec{Q} = \int_{\mathbb{R}^3} \frac{1}{2} m v^2 \vec{v} f \, \mathrm{d} \vec{v}.

It is also useful to name some moments in the reference frame of the
moving species.
With :math:`\vec{w} = \vec{v} - \vec{u}`, let

.. math::

    p_{ij} = \int_{\mathbb{R}^3} m w_i w_j f \, \mathrm{d} \vec{v}

be the pressure tensor,
and let

.. math::

    \vec{q} = \int_{\mathbb{R}^3} \frac{1}{2} m w^2 \vec{w} f \, \mathrm{d} \vec{v}

be the heat flux density.
For convenience, let :math:`p = p_{ii}/3` be the scalar pressure
and decompose the pressure tensor as

.. math::

    p_{ij} = p \delta_{ij} + \pi_{ij},

where :math:`\pi_{ij}` is the generalized viscosity tensor.
Finally,

.. math::

    n m E = \int_{\mathbb{R}^3} H f \, \mathrm{d} \vec{v}

with the single-particle Hamiltonian
:math:`H = \frac{1}{2} m v^2`
is the total energy density.

The Euler equations can be derived from the
:ref:`overview:Boltzmann kinetic equation`
by computing moments as

.. math::

    \int_{\mathbb{R}^3} \psi \left[ \frac{\partial f}{\partial t} +
    \vec{v} \cdot \frac{\partial f}{\partial \vec{x}} +
    \frac{q}{m} \left( \vec{E} + \vec{v} \times \vec{B} \right) \cdot \frac{\partial f}{\partial \vec{v}}
    \right] \, \mathrm{d} \vec{v} = \int_{\mathbb{R}^3} \psi \mathcal{C} [f] \, \mathrm{d} \vec{v},

where :math:`\psi = \psi(\vec{v})` is a polynomial.
In particular, take :math:`\psi = m`, :math:`m \vec{v}`,
and :math:`\frac{1}{2} m v^2`.
This ultimately yields

.. math::

    \frac{\partial}{\partial t} (nm) + \nabla \cdot (n m \vec{u}) = \int_{\mathbb{R}^3} m \mathcal{C}[f] \, \mathrm{d} \vec{v},

    \frac{\partial}{\partial t} (nmu_i) + \frac{\partial}{\partial x_j} P_{ij} - q n (\vec{E} + \vec{u} \times \vec{B})_i = \int_{\mathbb{R}^3} m \vec{v} \mathcal{C}[f] \, \mathrm{d} \vec{v},

    \frac{\partial}{\partial t} (nmE) + \nabla \cdot \left(nmE \vec{u} + \vec{q} + p \vec{u} + \pi_{ij} u_j \right) - q n \vec{u} \cdot \vec{E} = \int_{\mathbb{R}^3} H \mathcal{C}[f] \, \mathrm{d} \vec{v}.

These equations are closed by assuming that the heat flux density and
generalized viscosity tensor are zero
and relating the scalar pressure to the remaining fluid state variables
through an equation of state (EOS), resulting in

.. math::

    \frac{\partial}{\partial t} (nm) + \nabla \cdot (n m \vec{u}) = \int_{\mathbb{R}^3} m \mathcal{C}[f] \, \mathrm{d} \vec{v},

    \frac{\partial}{\partial t} (nmu_i) + \frac{\partial}{\partial x_j} \left( n m u_i u_j + p \delta_{ij} \right) = q n (\vec{E} + \vec{u} \times \vec{B})_i + \int_{\mathbb{R}^3} m \vec{v} \mathcal{C}[f] \, \mathrm{d} \vec{v},

    \frac{\partial}{\partial t} (nmE) + \nabla \cdot \left(nmE \vec{u} + p \vec{u} \right) = q n \vec{u} \cdot \vec{E} + \int_{\mathbb{R}^3} H \mathcal{C}[f] \, \mathrm{d} \vec{v}.

A common analytic EOS is the ideal gas law

.. math::

    p = n k T,

where :math:`k` is the Boltzmann constant
and :math:`T` is the temperature,
combined with the equipartition theorem for calorically perfect gases

.. math::

    n m E = \frac{1}{2} n m u^2 + \frac{1}{\gamma - 1} n k T,

which yields

.. math::

    p = (\gamma - 1) \left( n m E - \frac{1}{2} n m u^2 \right).

Uniform background
-------------------

This model assumes that the species follows a Maxwellian
distribution everywhere in space,
so that the distribution is

.. math::

    f = n \sqrt{\frac{m}{2 \pi k T}} \exp \left( - \frac{m v^2}{2 k T} \right)

for a given number density :math:`n` and temperature :math:`T`.
The charge density is therefore simply :math:`\rho = q n`.
