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
    :label: eq_1stdev5
    
    \frac {\partial \phi}{\partial x}|_i = \frac{\phi_{i+1}-\phi_{i-1}}{\Delta x_i + \Delta x_{i-1}} = \frac{r(\phi_{i+1}-\phi_{i-1})}{(r+1)\Delta x_i} = \frac{\phi_{i+1}-\phi_{i-1}}{(r+1)\Delta x_{i-1}}

Therefore, from equation :eq:`eq_1stdev1` we can write,

.. math::
    :label: eq_1stdev6
    
    E_i = - \frac {\partial \phi}{\partial x}|_i = - \frac{\phi_{i+1}-\phi_{i-1}}{\Delta x_i + \Delta x_{i-1}} = - \frac{r(\phi_{i+1}-\phi_{i-1})}{(r+1)\Delta x_i} = - \frac{\phi_{i+1}-\phi_{i-1}}{(r+1)\Delta x_{i-1}}

1D Non-uniform Mesh Stencil for Poisson Solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Let's consider the problem,

.. math::
   :label: eq_2nddev1

   \nabla^2 \phi(x) = - \frac{\rho}{\epsilon_0}

where, :math:`\rho` is the charge density and :math:`\epsilon_0` is the permittivity of free space.

Full Poisson problem: Dirichlet boundary conditions 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's consider the boundary conditions and grading ratio are,

.. math::
   :label: eq_2nddev2

   \begin{aligned}
   \phi{(x_0)} = left\  bc = 0;\\
   \phi{(x_{n-1})} = right\  bc = 0;\\
   \Delta{x_i} = x_{i+1} - x_i = r\Delta{x_{i-1}};\\
   r = Grading\ ratio =\frac{\Delta{x_i}}{\Delta{x_{i-1}}};
   \end{aligned}

Now, using Taylor series expansion at :math:`\phi_{i+1}` we get,

.. math::
   :label: eq_2nddev3

   \phi_{i+1} = \phi_i+(\Delta x_i) \frac{\partial \phi}{\partial x}|_{i}+\frac{\Delta x_i^2}{2!}\frac{\partial^2\phi}{\partial x^2}|_i + \frac{\Delta x_i^3}{3!}\frac{\partial^3\phi}{\partial x^3}|_i + ......

And, using Taylor series expansion at :math:`\phi_{i-1}` we get,

.. math::
   :label: eq_2nddev4

   \phi_{i-1} = \phi_i-(\Delta x_{i-1}) \frac{\partial \phi}{\partial x}|_{i}+\frac{\Delta x_{i-1}^2}{2!}\frac{\partial^2\phi}{\partial x^2}|_i - \frac{\Delta x_{i-1}^3}{3!}\frac{\partial^3\phi}{\partial x^3}|_i + ......

Multiplying equation :eq:`eq_2nddev4` by :math:`r` and adding with equation :eq:`eq_2nddev3` we get,

.. math::
   :label: eq_2nddev5

   \phi_{i+1}+r\phi_{i-1} = (1+r)\phi_i+(\Delta x_i - r\Delta x_{i-1})\frac{\partial \phi}{\partial x}|_{i} +\frac{(\Delta x_i)^2 + r(\Delta x_{i-1})^2}{2}\frac{\partial^2\phi}{\partial x^2}|_i 

Since :math:`\Delta{x_i} = r\Delta{x_{i-1}}`, second term of the right hand side is  eliminated and we get,

.. math::
   :label: eq_2nddev6

   \phi_{i+1}+r\phi_{i-1} = (1+r)\phi_i+\frac{(\Delta x_i)^2 + r(\Delta x_{i-1})^2}{2}\frac{\partial^2\phi}{\partial x^2}|_i

.. math::
   :label: eq_2nddev7

   => r\phi_{i-1}-(r+1)\phi_i+\phi_{i+1} = \frac{(\Delta x_i)^2 + r(\frac{\Delta x_{i}}{r})^2}{2}\frac{\partial^2\phi}{\partial x^2}|_i
   
.. math::
   :label: eq_2nddev8

   => r\phi_{i-1}-(r+1)\phi_i+\phi_{i+1} = \frac{(\Delta x_i)^2 + \frac{(\Delta x_{i})^2}{r}}{2}\frac{\partial^2\phi}{\partial x^2}|_i

.. math::
    :label: eq_2nddev9
    
    => \frac{\partial^2\phi}{\partial x^2}|_i = \frac{r\phi_{i-1}-(r+1)\phi_i+\phi_{i+1}}{(\frac{r+1}{2r})(\Delta x_i)^2} 

.. math::
    :label: eq_2nddev10
    
    => \frac{\partial^2\phi}{\partial x^2}|_i = \frac{(\frac{2r^2}{r+1})\phi_{i-1}-2r\phi_i+(\frac{2r}{r+1})\phi_{i+1}}{(\Delta x_i)^2}

So, the discrete finite difference form of equation :eq:`eq_2nddev1` is, 

.. math::
   :label: eq_2nddev11

   => \frac{\partial^2\phi}{\partial x^2}|_i = \frac{(\frac{2r^2}{r+1})\phi_{i-1}-2r\phi_i+(\frac{2r}{r+1})\phi_{i+1}}{(\Delta x_i)^2} = -(\frac{\rho}{\epsilon_0})_i 

Corresponding stencil is :math:`((\frac{2r^2}{r+1}), -2r, (\frac{2r}{r+1}))`.

So, the system of linear equations are,

.. math::

    \label{eq_2nddev12} 
    \phi_0 = 0;

.. math::

    \label{eq_2nddev13}
    (\frac{2r^2}{r+1})\phi_0-2r\phi_1+(\frac{2r}{r+1})\phi_2 = (\Delta x_1)^2 (-(\frac{\rho}{\epsilon_0})|_1);

.. math::

    \label{eq_2nddev14}
    (\frac{2r^2}{r+1})\phi_1-2r\phi_2+(\frac{2r}{r+1})\phi_3 = (\Delta x_2)^2 (-(\frac{\rho}{\epsilon_0})|_2);

.. math::

    \label{eq_2nddev15}
    (\frac{2r^2}{r+1})\phi_2-2r\phi_3+(\frac{2r}{r+1})\phi_4 = (\Delta x_3)^2 (-(\frac{\rho}{\epsilon_0})|_3);

.. math::

    \label{eq_2nddev16}
   .......................................\\
   .......................................

.. math::

    \label{eq_2nddev17}
    (\frac{2r^2}{r+1})\phi_{n-3}-2r\phi_{n-2}+(\frac{2r}{r+1})\phi_{n-1} = (\Delta x_{n-2})^2 (-(\frac{\rho}{\epsilon_0})|_{n-2});

.. math::

    \label{eq_2nddev18}
    \phi_{n-1} = 0;

Corresponding matrix-vector representation of system of linear equations will be,

.. math::
    :label: eq_2nddev19

    Ax = b

Where, the matrix :math:`A` is,

.. math::
    :label: eq_2nddev20

    A = \begin{vmatrix}
    1&0&0&0&..&..&..&0\\
    \frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&0&..&..&..\\
    0&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&..&..&..\\
    ..&..&..&..&..&..&..&..\\
    ..&..&..&..&..&..&..&..\\
    0&..&..&..&..&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}\\
    0&0&..&..&..&..&0&1\\
    \end{vmatrix}

The vector :math:`\vec x` is,

.. math::
    :label: eq_2nddev21

    \vec x = \begin{vmatrix}
    \phi_0\\
    \phi_1\\
    \phi_2\\
    ..\\
    ..\\
    \phi_{n-2}\\
    \phi_{n-1}
    \end{vmatrix}

The vector :math:`\vec b` is,

.. math::
    :label: eq_2nddev22

    \vec b = \begin{vmatrix}
    0\\
    -((\Delta x_1)^2 (\frac{\rho}{\epsilon_0})_1)\\
    -((\Delta x_2)^2 (\frac{\rho}{\epsilon_0})_2)\\
    ..\\
    ..\\
    -((\Delta x_{n-2})^2 (\frac{\rho}{\epsilon_0})_{n-2})\\
    0
    \end{vmatrix} + \begin{vmatrix}
    left \ bc\\
    0\\
    0\\
    ..\\
    ..\\
    0\\
    right \ bc
    \end{vmatrix}

.. math::
    :label: eq_2nddev23

    => \vec b = \begin{vmatrix}
    left \ bc\\
    -((\Delta x_1)^2 (\frac{\rho}{\epsilon_0})_1)\\
    -((\Delta x_2)^2 (\frac{\rho}{\epsilon_0})_2)\\
    ..\\
    ..\\
    -((\Delta x_{n-2})^2 (\frac{\rho}{\epsilon_0})_{n-2})\\
    right \ bc
    \end{vmatrix}

Therefore the :math:`A \vec x = \vec b` system of equations will be, 

.. math::
    :label: eq_2nddev24

    \begin{vmatrix}
    1&0&0&0&..&..&..&0\\
    \frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&0&..&..&..\\
    0&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&..&..&..\\
    ..&..&..&..&..&..&..&..\\
    ..&..&..&..&..&..&..&..\\
    0&..&..&..&..&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}\\
    0&0&..&..&..&..&0&1\\
    \end{vmatrix} 
    \begin{vmatrix}
    \phi_0\\
    \phi_1\\
    \phi_2\\
    ..\\
    ..\\
    \phi_{n-2}\\
    \phi_{n-1}
    \end{vmatrix} = \begin{vmatrix}
    left \ bc\\
    -((\Delta x_1)^2 (\frac{\rho}{\epsilon_0})_1)\\
    -((\Delta x_2)^2 (\frac{\rho}{\epsilon_0})_2)\\
    ..\\
    ..\\
    -((\Delta x_{n-2})^2 (\frac{\rho}{\epsilon_0})_{n-2})\\
    right \ bc
    \end{vmatrix}

This is for Dirichlet boundary condition on both ends. 

1D Full Poisson problem: Neumann boundary condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's consider the Neumann boundary condition on left boundary,

.. math::

    \frac{\partial \phi}{\partial x} = g

Where, :math:`g` is the value of the derivative at the boundary.

Now, to deal the boundary simply, we consider a ghost node at the left of :math:`x_0` so that, :math:`x_0 - x_{-1} = x_1 - x_0`, that is, 
even though our mesh is nonuniform (graded), we consider uniform grid for ghost node. This will make calculation easier for boundary condition. 
So, now using central difference scheme on the boundary node and considering direction as towards left, this equation can be written as, 

.. math::

    \frac{\phi_{-1} - \phi_1}{2\Delta x_0} = g \notag \\
    \implies \phi_{-1} = 2 \Delta x_0 g + \phi_1

Considering a ghost node at :math:`x_{-1}` and uniform mesh for first three nodes, at the boundary node we can write,

.. math::

    \frac{\phi_{-1} - 2\phi_0 + \phi_1}{(\Delta x_0)^2} = (-(\frac{\rho}{\epsilon_0})|_0) \notag    \\
    \implies \phi_{-1} - 2\phi_0 + \phi_1 = \Delta x_0^2 (-(\frac{\rho}{\epsilon_0})|_0)  \notag    \\
    \implies 2\Delta x_0 g + \phi_1 -2\phi_0 + \phi_1 = \Delta x_0^2 (-(\frac{\rho}{\epsilon_0})|_0) \notag \\
    \implies -2 \phi_0 + 2\phi_1 = \Delta x_0^2 (-(\frac{\rho}{\epsilon_0})|_0) - 2\Delta x_0\ g     

Similar treatment at right boundary gives,

.. math::

    2x_{n-2} - 2x_{n-1} = \Delta x_{n-2}^2 (-(\frac{\rho}{\epsilon_0})|_{n-1}) - 2\Delta x_{n-2}\ g 

Therefore the :math:`A\vec x = \vec b` system of equations will be, 

.. math::
    :label: eq_2nddev24

    \begin{vmatrix}
    -2&2&0&0&..&..&..&0\\
    \frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&0&..&..&..\\
    0&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}&0&..&..&..\\
    ..&..&..&..&..&..&..&..\\
    ..&..&..&..&..&..&..&..\\
    0&..&..&..&..&\frac{2r^2}{(r+1)}&-2r&\frac{2r}{r+1}\\
    0&0&..&..&..&..&2&-2\\
    \end{vmatrix} 
    \begin{vmatrix}
    \phi_0\\
    \phi_1\\
    \phi_2\\
    ..\\
    ..\\
    \phi_{n-2}\\
    \phi_{n-1}
    \end{vmatrix} = \begin{vmatrix}
    -((\Delta x_0)^2 (\frac{\rho}{\epsilon_0})_0) - 2g\Delta x_0\\
    -((\Delta x_1)^2 (\frac{\rho}{\epsilon_0})_1)\\
    -((\Delta x_2)^2 (\frac{\rho}{\epsilon_0})_2)\\
    ..\\
    ..\\
    -((\Delta x_{n-2})^2 (\frac{\rho}{\epsilon_0})_{n-2})\\
    -((\Delta x_{n-2})^2 (\frac{\rho}{\epsilon_0})_{n-1}) - 2g\Delta x_{n-2}
    \end{vmatrix}

This is for Neumann boundary condition on both ends. 
Please note that, we can't set both the boundaries as Neumann in the implementation at the moment. 
At least one should be Dirichlet for now. 

1D Boltzmann electron problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For Boltzmann electrons, equation :eq:`eq_2nddev1` will be, 

.. math::
    
    \Delta^2 \phi (x) = -\frac{\rho}{\epsilon_0} + \frac{n_0 e}{\epsilon_0}\ exp\ (\frac{e\phi}{k_B T_e})

Where :math:`n_0` is the electron density, :math:`e` is the elementary charge, :math:`k_B` is the Boltzmann constant and :math:`T_e` is the electron temperature. 

Following similar treatment for nonuniform mesh, using equation :eq:`eq_2nddev11` we can write, 

.. math::

    \frac{\partial^2\phi}{\partial x^2}|_i = \frac{(\frac{2r^2}{r+1})\phi_{i-1}-2r\phi_i+(\frac{2r}{r+1})\phi_{i+1}}{(\Delta x_i)^2} = -(\frac{\rho}{\epsilon_0})_i + \frac{n_0 e}{\epsilon_0}\ exp\ (\frac{e\phi_i}{k_B T_e}) \notag \\
    \implies (\frac{2r^2}{r+1})\phi_{i-1}-2r\phi_i+(\frac{2r}{r+1})\phi_{i+1} = -(\frac{\rho}{\epsilon_0})_i (\Delta x_i)^2 + \frac{n_0 e}{\epsilon_0} (\Delta x_i)^2 \ exp\ (\frac{e\phi_i}{k_B T_e}) \notag \\
    \implies (\frac{2r^2}{r+1})\phi_{i-1}-2r\phi_i+(\frac{2r}{r+1})\phi_{i+1} + (\frac{\rho}{\epsilon_0})_i (\Delta x_i)^2 - \frac{n_0 e}{\epsilon_0} (\Delta x_i)^2 \ exp\ (\frac{e\phi_i}{k_B T_e}) = 0 \notag  \\
    \implies F(\phi_i) =  (\frac{2r^2}{r+1})\phi_{i-1}-2r\phi_i+(\frac{2r}{r+1})\phi_{i+1} + (\frac{\rho}{\epsilon_0})_i (\Delta x_i)^2 - \frac{n_0 e}{\epsilon_0} (\Delta x_i)^2 \ exp\ (\frac{e\phi_i}{k_B T_e}) = 0 \notag 

Considering :math:`\vec \phi = (\phi_0, \phi_1, ....., \phi_{n-1})^t`, we need to solve the following equation for :math:`\phi_i`, 

.. math::
    :label: `eq_boltzmann_nonlinear`

    F_i(\vec{\phi}) =  (\frac{2r^2}{r+1})\phi_{i-1}-2r\phi_i+(\frac{2r}{r+1})\phi_{i+1} + (\frac{\rho}{\epsilon_0})_i (\Delta x_i)^2 - \frac{n_0 e}{\epsilon_0} (\Delta x_i)^2 \ exp\ (\frac{e\phi_i}{k_B T_e})

This is a nonlinear problem and we can solve it using Newton-Raphson method. With some initial guess :math:`x^0`, accoding to Newton-Raphson method, consecutive iterative solution will be, 

.. math::

    x^{n+1} = x^{n} - \frac{f(x^{n})}{f^{'}(x^{n})}
    \implies f^{'}(x^{n}) (x^{n} - x^{n+1}) = f(x^{n})

For system of equations :math:`f(\vec x) = \vec(0)`, this equation becomes, 

.. math::

    f^{'}(\vec x^n) (\vec x^n - \vec x^{n+1}) = f(\vec x^n)

Considering, :math:`\delta \vec x = \vec x^n - \vec x^{n+1}`, the equation becomes, 

.. math::

    f^{'}(\vec x^n) \delta \vec x = f(\vec x^n) \notag \\
    \implies \frac{\partial f(\vec x^n)}{\partial \vec x^n} \delta \vec x = f(\vec x^n)


Applying this treatment on equation :eq:`eq_boltzmann_nonlinear` for :math:`i^{th}` term of potential, we can write, 

.. math::
    :label: 'eq_boltz_elec'

    (\frac{2r^2}{r+1})\delta \phi_{i-1}-2r\delta \phi_i+(\frac{2r}{r+1})\delta \phi_{i+1} - \frac{n_0 e^2}{\epsilon_0 k_B T_e} (\Delta x_i)^2 \delta \phi_i \ exp\ (\frac{e\phi^n_i}{k_B T_e}) = \notag \\ (\frac{2r^2}{r+1})\phi^n_{i-1}-2r\phi^n_i+(\frac{2r}{r+1})\phi^n_{i+1} + (\frac{\rho}{\epsilon_0})_i (\Delta x_i)^2 - \frac{n_0 e}{\epsilon_0} (\Delta x_i)^2 \ exp\ (\frac{e\phi^n_i}{k_B T_e})

Solving this equation for :math:`\delta \vec \phi` for all nodes and computing :math:`\vec \phi^{n+1} = \vec \phi^n - \delta \vec \phi` for consecutive iteration 
we can solve for :math:`\vec \phi` for a required tolerance. 

 The Dirichlet boundary condition at each time steps for the left boundary can be applied as,

 .. math::
     :label: 'eq_dirichlet'

     \delta \phi_0 = \phi^n_0 - left\ boundary\ value \notag \\
     \implies \delta \phi_0 = \phi^n_0 - C

 Where :math:`C` is the left boundary value.
 Similar condition is also applicable for Dirichlet right boundary.








Finite element method Poisson equation
---------------------------------------
