
# Overview

This code is designed to demonstrate functionalities relating to trans-ionospheric propagation, specifically *ray-tracing* at low RF frequencies. The rays here operate in three-dimensions, and in a ellipsiodal ionosphere (ellipsodial shells). 

## Known Issues
* None

### Programming language
* Python >= 3.9

# Setup

We recommend for initial installization of development environment the following tools (in this order):
1. Python: https://www.python.org/downloads/
2. Git: https://git-scm.com/downloads
3. Visual Studio Code: https://code.visualstudio.com/download

OR

Use Codespaces on Github https://github.com/features/codespaces

## Prerequisites

The import IRI2016 (https://pypi.org/project/iri2016/) reuqires a Fortran compiler--any modern Fortran compiler will do. Here's how to get Gfortran:
Linux: apt install gfortran
Mac: brew install gcc
Windows: consider MSYS2

If using codespaces:
sudo apt-get update
sudo apt-get install gfortran

https://github.com/modflowpy/install-gfortran-action

- Build a virtual environment ([How-To](https://python.plainenglish.io/python-virtual-environments-explained-78d5a040f963))
  -  in a terminal window: python -m venv venv
  -  activate the virtual env: 
    - Linux: `source ./venv/bin/activate`  
    - Windows: `.\venv\Scripts\activate`
    - (if issue occurs see: [fix](https://www.sharepointdiary.com/2014/03/fix-for-powershell-script-cannot-be-loaded-because-running-scripts-is-disabled-on-this-system.html))
  -  In Linux, you'll see your terminal window you'll get a new start to the line (venv). In Windows, you can run a Python command (e.g. `python -c "print (\"Hello World\")"` and you should see (venv) display when the execution finishes.

- Imports: from the terminal window (with the venv prefix) install your updates  
  - Check to see if you have pip installed, if not: Install/Update [pip](https://pip.pypa.io/en/stable/installation/)
  - Run: pip install -r requirements.txt (potentially you might need to do this within python; i.e. python/py/python3 -m in front of pip)
  - Alternatively Ensure that you have pipreqs installed locally (pip install pipreqs)
  - to generate freeze of requirements "pipreqs --force"

- To test your distributon run all tests: python -m unittest discover -s unittests


## Coverage
- coverage run -m unittest discover
- coverage html

## Unit Tests
- python -m unittest discover -s unittests