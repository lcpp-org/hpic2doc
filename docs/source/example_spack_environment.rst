Example Developer Bash file
===========================
This document contains example bash files for loading hpic2 for development using Spack environments. 

Centos 7 Example
----------------
This is an example Centos 7 bash file

.. code-block:: bash

    #!/bin/bash
    cd ~/<PATH_to_HPIC2_build_location>/hpic2_build/hpic2_dev/packages/hpic2/
    git pull     #Auto pulling from github the latest version/branch of hpic2
    cd ..        #Moving back out to the hpic2_build location
    cd ..
    cd ..
    . spack/share/spack/setup-env.sh #Source the spack environment so that all of the other stuff works if you haven't added it to your bashrc
    source ~/.bashrc   #
    alias spack="/home/pccentos/Desktop/hpic2_build/spack/bin/spack"
    spack env activate hpic2_serial 
    #spack add googletest  #These only need to be run the first time before you run the spack install command
    #spack add hypre
    #spack add kokkos
    #spack add mpi
    #spack add spdlog
    #spack add rustbca
    spack install 

    #sudo cmake -DCMAKE_BUILD_TYPE=Debug -DWITH_TESTS=ON -DWITH_RUSTBCA=ON ./hpic2_dev/packages/hpic2/ #This only needs to be run the first time also
    sudo make -j 

    mpiexec -np 1 ./hpic2 --i ~/<PATH_to_HPIC2_build_location>/hpic2_build/hpic2_dev/packages/hpic2/examples/<name_example_file.txt> #This is where you actually run hpic2, see other sections of the docs to understand syntax

Some Stuff at the End
---------------------

Some stuff at the end
