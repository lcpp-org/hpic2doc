
Building hpic2 on Centos 7
==========================

This document contains the Centos 7 build instructions for hPIC2 as of March 2023 (3/31/2023). 


CENTOS 7 as of Nov. 2024 is no longer maintained. Operability of these instructions is no longer guaranteed.
============================================================================================================


Update Dependencies and install gcc
-----------------------------------

Assuming in an administrator non-root account

.. code-block:: bash

   bash 
   sudo yum update -y
   sudo yum install -y epel-release
   sudo yum update -y
   sudo yum --enablerepo epel groupinstall -y "Development Tools"
   sudo yum --enablerepo epel install -y curl findutils gcc-c++ gcc gcc-gfortran git gnupg2 hostname iproute redhat-lsb-core make patch python3 python3-pip python3-setuptools unzip
   sudo python3 -m pip install boto3                                    #This will give an warning don't worry about it

.. code-block:: bash

   sudo yum install -y centos-release-scl
   sudo yum install -y devtoolset-N-gcc-*                               #The N should be replaced with a number >=7, 9 has been used before with success
   su root                                                              #Switch to root for the next command
   echo "source scl_source enable devtoolset-N" >> ~/.bashrc
   exit                                                                 #leave root
   source ~/.bashrc                                                     #reload bashrc file 


Install spack
-------------

Download spack, 

.. code-block:: bash

   git clone -c feature.manyFiles=true https://github.com/spack/spack.git

and source spack environment (consider adding this to your .bashrc)

.. code-block:: bash

   . spack/share/spack/setup-env.sh

If the second command fails run this next set

.. code-block:: bash

   #su root #Go to root
   echo "alias spack='<PATH TO SPACK FOLDER>/spack/bin/spack'" >> ~/.bashrc
   #exit #leave root


Use spack to setup to install hpic2
-----------------------------------

Do the following steps where you want hpic2 to be saved. First, make a new spack repo

.. code-block:: bash

      spack repo create hpic2_dev

Register spack repo

.. code-block:: bash

      spack repo add hpic2_dev
      cd hpic2_dev/packages

Download hpic2 source, making sure to include the submodules, and optionally also RustBCA

.. code-block:: bash

      git clone --recurse-submodules https://github.com/lcpp-org/hpic2.git
      git clone https://github.com/lcpp-org/RustBCA.git
      mv RustBCA rustbca

Remove old gcc compilers
------------------------

Check if there are old compiler versions (like 4.x.x),

.. code-block:: bash
   
   spack compiler list

Add new compilers / makesure they are all loaded

.. code-block:: bash
   
   spack compiler find 

Open the spack compilers file (This may be different, the output of the previous two commands will tell you where this file is)

.. code-block:: bash
   
   vim ~/.spack/linux/compilers.yaml

In the spack compilers.yaml delete the entries for the old (4.x.x) gcc compilers. 
In step one you should have installed a newer version, and this will force spack to use the new gcc compiler. 

Use Spack to install hpic2
--------------------------

Use spack to install hpic2. A list of the available variants can be found at the following link (link). 

.. code-block:: bash

   cd hpic2_dev/packages
   spack install hpic2+testing+rustbca ^kokkos+openmp                   