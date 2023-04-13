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

Types of problems hPIC2 can solve
----------------------------------
