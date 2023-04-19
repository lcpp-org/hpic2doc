Interactions
=============

This page describes methods for modeling collisions and interactions between
species in hPIC2.

Monte Carlo collisions
-----------------------

Monte Carlo collision (MCC) methods form a family of algorithms that model
collisions between a particle-based "source" species and a
continuum "target" species.
The industry standard is the null collision method :cite:`vahedi1993capacitive`;
throughout this section, when we refer to MCC,
we refer specifically to this method.

MCC allows a source species to collide with arbitrarily many target species,
but an individual source particle may only undergo a maximum of one
collision per time step.
For each source particle, a collision probability is computed from the sum
of collision rates over all :math:`N` possible collisions as

.. math::

    P = 1 - \exp \left( - \Delta t \sum_{i=1}^N n_i \sigma_i (\vec{g}_i) g_i \right),

where :math:`\Delta t` is the time step size,
:math:`n_i` is the local number density of the target for collision :math:`i`,
:math:`\sigma_i = \sigma_i(\vec{g})` is the collision cross section function,
and :math:`\vec{g}_i` is the relative velocity between the source particle
and its target collision partner.
Collision partners are drawn randomly from the target species' distribution.
Another random number is drawn uniformly from :math:`[0,1)`,
and if it is less than :math:`P`,
then we say that a collision will occur.

We must then decide which type of collision will occur.
Uniformly draw a random number :math:`U \in [0,1)`.
Then collision :math:`i` will occur if

.. math::

    \frac{\sum_{j=1}^{i-1} n_j \sigma_j (\vec{g}_j) g_j}{\sum_{j=1}^N n_j \sigma_j (\vec{g}_j) g_j} \leq
    U <
    \frac{\sum_{j=1}^{i} n_j \sigma_j (\vec{g}_j) g_j}{\sum_{j=1}^N n_j \sigma_j (\vec{g}_j) g_j}.

This strategy weights the possible collisions by their collision rates.

Many things can happen when a collision occurs.
If the collision is meant to model ionizing source electrons impinging on
a neutral target,
the collision may spawn a new electron and a new ion;
if the collision models elastic scattering events,
the source particle's trajectory may simply be skewed to reflect the collision.

Coulomb collision force
----------------------------
