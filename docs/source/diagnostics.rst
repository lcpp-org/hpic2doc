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

PIC moments
~~~~~~~~~~~~

The distribution for a PIC species comprising :math:`N` particles
is assumed to be

.. math::

    f = \sum_{\alpha=1}^N W_\alpha \delta (\vec{x} - \vec{x}_\alpha) \delta (\vec{v} - \vec{v}_\alpha),

where :math:`\vec{x}_\alpha = \vec{x}_\alpha(t)`
and :math:`\vec{v}_\alpha = \vec{v}_\alpha(t)`
are the position and velocity of particle :math:`\alpha` at time :math:`t`,
respectively,
and :math:`W_\alpha` is the weight of particle :math:`\alpha`.
Hence

.. math::

    \bar{M}_{ijk}^T = \frac{1}{V} \int_T \int_{\mathbb{R}^3} m v_1^i v_2^j v_3^k \sum_{\alpha=1}^N \delta (\vec{x} - \vec{x}_\alpha) \delta (\vec{v} - \vec{v}_\alpha) \, \mathrm{d} \vec{v} \, \mathrm{d} \vec{x}
    = \frac{1}{V} \sum_{\alpha, \vec{x}_\alpha \in T} m W_\alpha v_{\alpha,1}^i v_{\alpha,2}^j v_{\alpha,3}^k.

Similarly,

.. math::

    \bar{\hat{M}}_{ijk}^T = \frac{1}{V} \sum_{\alpha, \vec{x}_\alpha \in T} m W_\alpha w_{\alpha,1}^i w_{\alpha,2}^j w_{\alpha,3}^k,

    \bar{M}_{\hat{n},ijk}^T = \frac{1}{V} \sum_{\alpha, \vec{x}_\alpha \in T, v_\alpha \cdot \hat{n} > 0} m W_\alpha v_{\alpha,1}^i v_{\alpha,2}^j v_{\alpha,3}^k \vec{v}_\alpha \cdot \hat{n},

    \bar{\hat{M}}_{\hat{n},ijk}^T = \frac{1}{V} \sum_{\alpha, \vec{x}_\alpha \in T, w_\alpha \cdot \hat{n} > 0} m W_\alpha w_{\alpha,1}^i w_{\alpha,2}^j w_{\alpha,3}^k \vec{w}_\alpha \cdot \hat{n}.

Boltzmann electron moments
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The distribution for Boltzmann electrons is given by

.. math::

    f = n_0 \left( \frac{m}{2 \pi k T} \right)^{3/2} \exp \left( \frac{e \phi}{kT} \right) \exp \left( - \frac{m v^2}{2 k T} \right),

where :math:`n_0` is the reference density described in
the section on :ref:`species:Boltzmann electrons`.
Using the fact that

.. math::

    \int_{\mathbb{R}} \xi^p \frac{1}{\sigma \sqrt{2 \pi}} \exp \left( - \frac{\xi^2}{2 \sigma^2} \right) \, \mathrm{d} \xi
    = \begin{cases}
        0 & \text{if} & p \text{ is odd}, \\
        \sigma^p (p-1)!! & \text{if} & p \text{ is even},
    \end{cases}

we can deduce

.. math::

    \bar{M}_{ijk}^T =
    \begin{cases}
        \frac{1}{V} n_0 m (i-1)!! (j-1)!! (k-1)!! \int_T \sqrt{\frac{kT}{m}}^{i+j+k} \exp \left( \frac{e \phi}{kT} \right) \, \mathrm{d} \vec{x} & \text{if } i,j,k \text{ are all even}, \\
        0 & \text{otherwise}.
    \end{cases}

Note that the temperature :math:`T` and potential :math:`\phi`
are both space-dependent.
The integral over the element is computed differently depending on whether
the field solver uses the finite difference method or the finite element method.
In the FDM case, the integral is taken to be the sum of the value at the nodes
times the node covolumes.
In the FEM case, the integral is approximated using the same quadrature
rule as in the field solver.

Since the Boltzmann electrons have zero bulk velocity,
the rest-frame moments are identical to the lab-frame moments,
so that

.. math::

    \bar{\hat{M}}_{ijk}^T = \bar{M}_{ijk}^T.

Directional moments have not yet been implemented,
although they can be expressed analytically
`with great difficulty <https://github.com/lcpp-org/hpic2/issues/253>`_.

Euler fluid moments
~~~~~~~~~~~~~~~~~~~

When deriving the Euler equations, we are careful not to assume too much
about the distribution.
However, to compute the moments, we must make some assumption.
It is safe to assume that the fluid distribution is a drifting Maxwellian,

.. math::

    f = n \left( \frac{m}{2 \pi k T} \right)^{3/2} \exp \left( - \frac{m (\vec{v} - \vec{u})^2}{2 k T} \right),

since that is the minimum-entropy distribution that satisfies
the Euler fluid hypotheses.

Using the fact that

.. math::

    \int_{\mathbb{R}} \xi^p \frac{1}{\sigma \sqrt{2 \pi}} \exp \left( - \frac{(\xi  - \mu)^2}{2 \sigma^2} \right) \, \mathrm{d} \xi
    = \left( - \frac{i \sigma}{\sqrt{2}} \right)^p H_p \left( \frac{i \mu}{\sigma \sqrt{2}} \right),

where :math:`H_p` is the physicists' Hermite polynomial of degree :math:`p`,
we can write

.. math::

    \bar{M}_{ijk}^T = \frac{1}{V} \int_T n m \left( - i \sqrt{\frac{kT}{2m}} \right)^{i+j+k} H_i \left( i u_1 \sqrt{\frac{m}{2kT}} \right) H_j \left( i u_2 \sqrt{\frac{m}{2kT}} \right) H_k \left( i u_3 \sqrt{\frac{m}{2kT}} \right) \, \mathrm{d} \vec{x},

where the integral is approximated with quadrature.
For rest-frame moments, we can substitute :math:`\vec{u} = \vec{0}`,
so that

.. math::

    \bar{\hat{M}}_{ijk}^T =
    \begin{cases}
        \frac{1}{V} n m (i-1)!! (j-1)!! (k-1)!! \int_T \sqrt{\frac{kT}{m}}^{i+j+k} \, \mathrm{d} \vec{x} & \text{if } i,j,k \text{ are all even}, \\
        0 & \text{otherwise}.
    \end{cases}

Directional moments have not yet been implemented,
although they can be expressed analytically
`with great difficulty <https://github.com/lcpp-org/hpic2/issues/253>`_.

Uniform background moments
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The distribution is

.. math::

    f = n \sqrt{\frac{m}{2 \pi k T}} \exp \left( - \frac{m v^2}{2 k T} \right),

where the temperature and density are uniform in space.
From analysis from the previous sections, this means that

.. math::

    \bar{M}_{ijk}^T =
    \bar{\hat{M}}_{ijk}^T =
    \begin{cases}
        n m (i-1)!! (j-1)!! (k-1)!! \sqrt{\frac{kT}{m}}^{i+j+k} & \text{if } i,j,k \text{ are all even}, \\
        0 & \text{otherwise}.
    \end{cases}

Directional moments have not yet been implemented,
although they can be expressed analytically
`with great difficulty <https://github.com/lcpp-org/hpic2/issues/253>`_.

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
