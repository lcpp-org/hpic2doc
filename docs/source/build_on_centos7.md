# Building hpic2 on Centos 7
This document contains the Centos 7 build instructions for HPIC2 as of March 2023 (3/31/2023). 

## CENTOS 7 as of Nov. 2024 is no longer maintained. Operability of these instructions is no longer guaranteed.

1. Update Dependencies and install gcc
Assuming in an administrator non-root account
```bash 
sudo yum update -y
sudo yum install -y epel-release
sudo yum update -y
sudo yum --enablerepo epel groupinstall -y "Development Tools"
sudo yum --enablerepo epel install -y curl findutils gcc-c++ gcc gcc-gfortran git gnupg2 hostname iproute redhat-lsb-core make patch python3 python3-pip python3-setuptools unzip
sudo python3 -m pip install boto3                                    #This will give an warning don't worry about it

sudo yum install -y centos-release-scl
sudo yum install -y devtoolset-N-gcc-*                               #The N should be replaced with a number >=7, 9 has been used before with success

su root                                                              #Switch to root for the next command
echo "source scl_source enable devtoolset-N" >> ~/.bashrc
exit                                                                 #leave root

source ~/.bashrc                                                     #reload bashrc file 
```
2. Install spack
```bash
git clone -c feature.manyFiles=true https://github.com/spack/spack.git # download spack
. spack/share/spack/setup-env.sh                                       # source spack env. consider adding this to your .bashrc
```
If the second command fails run this next set
```bash 
#su root #Go to root
echo "alias spack='<PATH TO SPACK FOLDER>/spack/bin/spack'" >> ~/.bashrc
#exit #leave root
```

3. Use spack to setup to install hpic2
Do wherever you want hpic2 saved
```bash
spack repo create hpic2_dev                                          # make a new spack repo
spack repo add hpic2_dev                                             # register spack repo
cd hpic2_dev/packages
git clone --recurse-submodules https://github.com/lcpp-org/hpic2.git # download hpic2 source
git clone https://github.com/lcpp-org/RustBCA.git                    # (optional) download rustbca source
mv RustBCA rustbca                                                   # rename rustbca dir to be spack-friendly
```

4. Remove old gcc compilers
```bash 
spack compiler list                                                  #check if there are old compiler versions (like 4.x.x)
spack compiler find                                                  #add new compilers / makesure they are all loaded
vim ~/.spack/linux/compilers.yaml                                    #open the spack compilers file (This may be different, the output of the previous two commands will tell you where this file is)
```
In the spack compilers.yaml delete the entries for the old (4.x.x) gcc compilers. 
In step one you should have installed a newer version, and this will force spack to use the new gcc compiler. 

5. Use Spack to install hpic2
```bash
cd hpic2_dev/packages
spack install hpic2+testing+rustbca ^kokkos+openmp                   # use spack to install hpic2. go nuts with options
```