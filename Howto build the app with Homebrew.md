
# How to build the Spyder MacOS X application

## Installation

### Install Homebrew

Follow the instructions on this page
https://github.com/mxcl/homebrew/wiki/installation

### Install Python2 (for now)

* `brew install python`

### Install Qt and PyQt4

* Download and install Qt from the Qt
  [site](http://qt-project.org/downloads) directly. This is very
  important because the Homebrew versions are not compatible between
  MacOS versions.

* Run the script `symlink-qt.py`

* `brew install pyqt`

### Add Homebrew formulas for scientific and Python scientific libraries

* `brew tap homebrew/science`
* `brew tap samueljohn/python`

### Install gfortran

`brew install gcc`

### Install the main Python scientific libraries

* `pip install nose`
* `brew link --force openblas`
* `pip install numpy`
* `pip install scipy`

### Install matplotlib

* Just in Lion (To have these libraries included in the app)

  * `brew install freetype`
  * `brew install libpng`
  * `brew link --force freetype`
  * `brew link --force libpng`

* `brew install matplotlib`

### Install IPython

* `brew install zmq`
* `pip install cython`
* `pip install pyzmq`
* `pip install pygments`

* Stable release: `pip install --no-deps ipython`
* From git: `pip install https://github.com/ipython/ipython/tarball/master`

### Install other scientific libraries

* `pip install pillow`
* `pip install scikit-learn`
* `pip install scikit-image`
* `pip install pandas`
* `pip install sympy`
* `pip install patsy`
* `pip install statmodels`

### Install Spyder deps

* `pip install pyflakes`
* `pip install rope`
* `pip install sphinx`
* `pip install pylint`
* `pip install pep8`
* `pip install psutil`

### Install py2app (to build the app)

* `pip install py2app`

*Note*: It's not necessary to install Spyder


## Create the app

* Move to the root of your Spyder repo

* Run
  * `python setup.py build_doc`
  * `python create_app.py py2app`

* Caveats:
  * Fix possible Python 3 incompatible syntax if reported by py2app
  * Add an `__init__.py` to the mpl_toolkits package so that py2app
    can add it to the app