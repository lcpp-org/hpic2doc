Field Solvers
=============

Finite difference Poisson equation
----------------------------------

Solvers on uniform grid
~~~~~~~~~~~~~~~~~~~~~~~

Solvers on non-uniform grid
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section was prepared by

-  Huq Md Fazlul, UIUC

1D Non-uniform Grid
~~~~~~~~~~~~~~~~~~~


FD Stencil for 1D First Derivative
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let’s consider the problem,


.. math:: 
   :label: eq_1stdev1

   E_i = - \frac{d\phi}{dx}|_i 



.. figure:: figures/nonuniform_mesh.png
   :alt:

Let’s consider the boundary conditions and grading ratio are,

.. math::

   \begin{aligned}
   \phi{(x_0)} = left\  bc = 0;\\
   \phi{(x_{n-1})} = right\  bc = 0;\\
   \Delta{x_i} = x_{i+1} - x_i = r\Delta{x_{i-1}};\\
   r = Grading\ ratio =\frac{\Delta{x_i}}{\Delta{x_{i-1}}};
   \end{aligned}

Now, using Taylor series expansion at :math:`\phi_{i+1}` we get,

.. math::
   :label: eq_1stdev2
   
   \phi_{i+1} = \phi_i+(\Delta x_i) \frac{\partial \phi}{\partial x}|_{i}+\frac{\Delta x_i^2}{2!}\frac{\partial^2\phi}{\partial x^2}|_i +......

And, using Taylor series expansion at :math:`\phi_{i-1}` we get,

.. math::
   :label: eq_1stdev3

   \phi_{i-1} = \phi_i-(\Delta x_{i-1}) \frac{\partial \phi}{\partial x}|_{i}+\frac{\Delta x_{i-1}^2}{2!}\frac{\partial^2\phi}{\partial x^2}|_i -......

Subtracting equation :eq:`eq_1stdev3` from equation :eq:`eq_1stdev2` and ignoring higher order terms we get,

.. math::
   :label: eq_1stdev4

   \phi_{i+1}-\phi_{i-1} = (\Delta x_i + \Delta x_{i-1})\frac{\partial \phi}{\partial x}|_{i}

Rearranging we get,

.. math::
   \label{eq:1stdev5}
   \frac {\partial \phi}{\partial x}|_i = \frac{\phi_{i+1}-\phi_{i-1}}{\Delta x_i + \Delta x_{i-1}} = \frac{r(\phi_{i+1}-\phi_{i-1})}{(r+1)\Delta x_i} = \frac{\phi_{i+1}-\phi_{i-1}}{(r+1)\Delta x_{i-1}}

Therefore, from equation :eq:`eq_1stdev1` we can write,

.. math::
   \label{eq:1stdev6}
   E_i = - \frac {\partial \phi}{\partial x}|_i = - \frac{\phi_{i+1}-\phi_{i-1}}{\Delta x_i + \Delta x_{i-1}} = - \frac{r(\phi_{i+1}-\phi_{i-1})}{(r+1)\Delta x_i} = - \frac{\phi_{i+1}-\phi_{i-1}}{(r+1)\Delta x_{i-1}}

1D Non-uniform Mesh Stencil for Poisson Solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Let's consider the problem,

.. math::
   :label: eq_poisson1

   \nabla^2 \phi(x) = - \frac{\rho}{\epsilon_0}

where, :math:`\rho` is the charge density and :math:`\epsilon_0` is the permittivity of free space.

For full Poisson problem
~~~~~~~~~~~~~~~~~~~~~~~~
For Dirichlet boundary conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Let's consider the boundary conditions and grading ratio are,

.. math::
   :label: eq_poisson2

   \begin{aligned}
   \phi{(x_0)} = left\  bc = 0;\\
   \phi{(x_{n-1})} = right\  bc = 0;\\
   \Delta{x_i} = x_{i+1} - x_i = r\Delta{x_{i-1}};\\
   r = Grading\ ratio =\frac{\Delta{x_i}}{\Delta{x_{i-1}}};
   \end{aligned}

Now, using Taylor series expansion at :math:`\phi_{i+1}` we get,

.. math::
   :label: eq_poisson3

   \phi_{i+1} = \phi_i+(\Delta x_i) \frac{\partial \phi}{\partial x}|_{i}+\frac{\Delta x_i^2}{2!}\frac{\partial^2\phi}{\partial x^2}|_i + \frac{\Delta x_i^3}{3!}\frac{\partial^3\phi}{\partial x^3}|_i + ......



Finite element method Poisson equation
---------------------------------------
