Overview
========

This page describes the basic physics models that are solved by hPIC2.

Boltzmann kinetic equation
----------------------------

A plasma species is generally well described by the single-particle distribution
function :math:`f = f(\vec{x}, \vec{v}, t)`,
sometimes referred to simply as the distribution.
The distribution is a quasiprobability distribution;
the quantity
:math:`f(\vec{x}, \vec{v}, t) \, \mathrm{d}\vec{x} \, \mathrm{d} \vec{v}`
is the number of particles in a neighborhood of the coordinates :math:`\vec{x}`
with velocity in the neighborhood of :math:`\vec{v}`
at time :math:`t`.
In other words, the distribution can be interpreted as a time-dependent
density in phase space.
More generally, the distribution's arguments can range over internal degrees
of freedom, such as vibrational modes,
but we are primarily concerned with translational degrees of freedom.

The time evolution of the distribution is given by the Boltzmann equation 
:cite:t:`fitzpatrick2014plasma`,

.. math::

    \frac{\partial f}{\partial t} +
    \vec{v} \cdot \frac{\partial f}{\partial \vec{x}} +
    \frac{\vec{F}}{m} \cdot \frac{\partial f}{\partial \vec{v}} =
    \mathcal{C} [f],

where :math:`\vec{F} = \vec{F}(\vec{x}, \vec{v}, t)`
is a macroscopic force field,
:math:`m` is the mass of particles of the species,
and :math:`\mathcal{C}` is a functional which encodes collisions and
interactions.
Gravity is typically ignored in plasma physics,
so the only macroscopic force field is the Lorentz force

.. math::

    \vec{F} = q \vec{E} + q \vec{v} \times \vec{B},

where :math:`q` is the charge of particles of the species,
:math:`\vec{E} = \vec{E}(\vec{x}, t)` is the electric field,
and :math:`\vec{B} = \vec{B}(\vec{x}, t)` is the magnetic field.
Hence the Boltzmann equation becomes

.. math::

    \frac{\partial f}{\partial t} +
    \vec{v} \cdot \frac{\partial f}{\partial \vec{x}} +
    \frac{q}{m} \left( \vec{E} + \vec{v} \times \vec{B} \right) \cdot \frac{\partial f}{\partial \vec{v}} =
    \mathcal{C} [f].

Electrostatic approximation
-----------------------------

The time evolution of the electromagnetic fields is governed by
Maxwell's equations

.. math::

    \nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0},

    \nabla \times \vec{E} = - \frac{\partial \vec{B}}{\partial t},

    \nabla \cdot \vec{B} = 0,

    \nabla \times \vec{B} = \mu_0 \left( \vec{J} + \epsilon_0 \frac{\partial \vec{E}}{\partial t} \right),

where :math:`\rho = \rho(\vec{x}, t)` is the charge density,
:math:`\epsilon_0` is the vacuum permittivity,
:math:`\mu_0` is the vacuum permeability,
and :math:`\vec{J} = \vec{J}(\vec{x}, t)` is the current density.
In the case where the magnetic field varies slowly compared to plasma
evolution timescales,
the electric field is approximately irrotational
and can therefore be represented as the gradient of a scalar potential.
Traditionally, the electric field is written as

.. math::

    \vec{E} = - \nabla \phi,

where :math:`\phi = \phi(\vec{x}, t)` is the electric potential.
This electrostatic approximation yields Poisson's equation for the potential

.. math::

    \nabla^2 \phi = - \frac{\rho}{\epsilon_0}.

The electrostatic approximation is valid when currents are small,
which generally occurs when particles are non-relativistic.

Note that the charge density can be computed from every species' distribution as

.. math::

    \rho = \sum \int_{\mathbb{R}^3} q f \, \mathrm{d} \vec{v},

where the sum is over species.

Types of problems hPIC2 can solve
----------------------------------

.. bibliography::
    :all:
