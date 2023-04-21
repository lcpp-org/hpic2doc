Diagnostics
===========

This page describes possible outputs from hPIC2.

Moments of distribution functions
---------------------------------

For a distribution :math:`f`, define

.. math::

    M_{ijk} (\vec{x}, t) = \int_{\mathbb{R}^3} m v_1^i v_2^j v_3^k f \, \mathrm{d} \vec{v}

as the generalized moment corresponding to the multiindex :math:`(i,j,k)`,
where :math:`m` is the mass of the species.
Note that a number of macroscopic physical quantities can be written in terms of
generalized moments,
such as the mass density

.. math::

    nm = M_{000},

the momentum density

.. math::

    nm \vec{u} = (M_{100}, M_{010}, M_{001})^t,

and the total energy density for species with no internal degrees of freedom

.. math::

    nmE = \frac{1}{2} (M_{200} + M_{020} + M_{002}).

Similarly, with :math:`\vec{w} = \vec{v} - \vec{u}` as the peculiar velocity,
define the rest-frame moments as

.. math::

    \hat{M}_{ijk} (\vec{x}, t) = \int_{\mathbb{R}^3} m w_1^i w_2^j w_3^k f \, \mathrm{d} \vec{v}.

Again, many typical macroscopic physical quantities can be written in terms of
rest-frame moments,
such as the scalar pressure

.. math::

    p = \frac{1}{3} (\hat{M}_{200} + \hat{M}_{020} + \hat{M}_{002}).

It is sometimes useful to compute the flux of a moment through a surface
defined by some unit normal.
In this case, define

.. math::

    M_{\hat{n}, ijk} (\vec{x}, t) = \int_{\vec{v} \cdot \hat{n} > 0} m v_1^i v_2^j v_3^k (\vec{v} \cdot \hat{n}) f \, \mathrm{d} \vec{v},

    \hat{M}_{\hat{n}, ijk} (\vec{x}, t) = \int_{\vec{w} \cdot \hat{n} > 0} m w_1^i w_2^j w_3^k (\vec{w} \cdot \hat{n}) f \, \mathrm{d} \vec{v},

as the lab-frame and rest-frame directional moments, respectively.

hPIC2 is capable of computing the element averages of these moments;
that is, for each element :math:`T` in the mesh, hPIC2 calculates

.. math::

    \bar{M}_{ijk}^T = \frac{1}{V} \int_T M_{ijk} \, \mathrm{d} \vec{x},

where :math:`V` is the volume of element :math:`T`,
and similarly for the other types of moments.

These moments are computed differently for each species.
The sections below describe their computation.

Engery-angle at boundaries
--------------------------

Point-like probes
-----------------

Fields output
--------------

Particle output
----------------

For particle-based species, we can simply write all information
about each particle at some instant to disk.
Particle information includes positions, velocities,
indices of the elements containing the particles,
charge numbers, *etc*.
Since simulations may have many particles,
this is extremely slow, and should not be done often.
