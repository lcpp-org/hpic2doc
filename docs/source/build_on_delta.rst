
Building hpic2 on Delta
==================================

Delta has nodes with two types of GPUs: A40s and A100s.
The A40s are optimized for double-precision computation and should be preferred.
In a pinch, the A100s can also be used.

Before attempting to build hPIC2 with RustBCA support,
ensure that you have installed Rust on Delta by running

.. code-block:: sh

   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

or, if you have already installed it, ensure that it is at the latest version:

.. code-block:: sh

   rustup update

Build hPIC2 for A40s
~~~~~~~~~~~~~~~~~~~~~

The following script will install the latest version of hPIC2 with MFEM,
pumiMBBL, and RustBCA support.

.. literalinclude:: build_hpic2_cc80.sh
   :language: sh

Build hPIC2 for A100s
~~~~~~~~~~~~~~~~~~~~~

The following script will install the latest version of hPIC2 with MFEM,
pumiMBBL, and RustBCA support.

.. literalinclude:: build_hpic2_cc86.sh
   :language: sh
