
# Install/Read Me File

This code is designed to demonstrate functionalities relating to trans-ionospheric propagation, specifically *ray-tracing* at low RF frequencies. The rays here operate in three-dimensions, and in a ellipsiodal ionosphere (ellipsodial shells). 

## Prerequisites

Fortran compiler--any modern Fortran compiler will do. Here's how to get Gfortran:
Linux: apt install gfortran
Mac: brew install gcc
Windows: consider MSYS2

and then install latest:


## IRI2016
pip install iri201

You'll need to download a fortran compiler to your machine, I've used gfortran so far. 
If you are using a virtual environment for python, you might need to, inside of that enviroment, open venv/Lib/site-packages/iri2016/src/CMakeLists.txt

- set(CMAKE_Fortran_COMPILER C:/msys64/usr/bin/gfortran)
- set(CMAKE_C_COMPILER C:/msys64/usr/bin/gcc)
- set(CMAKE_CXX_COMPILER C:/msys64/usr/bin/g++)
- add_library(iri2016 OBJECT irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for)
- target_compile_options(iri2016 PRIVATE ${OLD_FLAGS})

where C:/msys64/usr/bin/gfortran is the location of my complier; mind the / being correct

go to venv\Lib\site-pages\iri2016 

run 

ctest -S .\setup.cmake -VV 

## IGRF 
pip install igrf

You'll need to download a fortran compiler to your machine, I've used gfortran so far. If you are using a virtual environment for python, you might need to update the folder and.... add a setup.cmake (which I borrowed from the IRI2016 package) (this package comes with a CMakeLists.txt that worked for me but I needed add)

go to venv\Lib\site-pages\igrf 

run 

ctest -S .\setup.cmake -VV 
