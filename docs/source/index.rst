Welcome to hPIC2
================

`hPIC2 <https://doi.org/10.1016/j.cpc.2022.108569>`_ is a hybrid plasma 
simulation code written in C++ developed by the Laboratory of Computational  
Plasma Physics at the University of Illinois at Urbana-Champaign. 
The hPIC2 code investigates the simultaneous use of 
different plasma models on the same domain, making it a hybrid code. 
hPIC2 supports an arbitrary number of plasma species, 
each of which can be modeled using a different plasma model.

hPIC2 is a successor to the `hPIC <https://doi.org/10.1016/j.cpc.2018.03.028>`_ 
code, previously developed by the Laboratory of Computational Plasma Physics 
at the University of Illinois. hPIC2 is a complete rewrite of hPIC, 
and is designed to be more modular, more extensible, and more performant. 

hPIC2 targets high-performance computing platforms,
exploiting `Kokkos <https://github.com/kokkos>`_ (Performance Portability 
Programming EcoSystem: The Programming Model - Parallel Execution and Memory Abstraction)
for performance portability across a wide range of heterogeneous computing architectures, 
including CPUs, GPUs, and more.

hPIC2 supports three different types of meshes: uniform meshes for one- 
and two-dimensional domains; block-structured non-uniform meshes furnished 
by the `pumiMBBL <https://github.com/SCOREC/pumiMBBL>`_ 
mesh library developed in collaboration with RPI; 
and unstructured meshes composed of simplex or tensor product elements for arbitrary 
two- and three-dimensional domains, which are facilitated by 
the `MFEM <https://mfem.org/>`_ finite-element method library. 

Furthermore, hPIC2 optionally dynamically couples (in-memory)
to the `RustBCA <https://github.com/lcpp-org/RustBCA>`_ code, 
which efficiently models plasma-material interactions such as 
sputtering, implantation, and reflection. 

.. warning:: 

   Documentation pages of hPIC2 are under construction.
   

Contents
--------

.. toctree::
   :maxdepth: 1

   build
   running
   input_deck
   tutorials 
   preprocessing
   postprocessing
   contributing
   hpic

.. figure:: figures/dalle2hpic.png
  :width: 100%
  :align: center

  (Image credits: DALL-E-2)
