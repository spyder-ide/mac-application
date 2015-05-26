
# How to build the Spyder MacOS X application

**Important note**: These instructions are valid only for MacOS X 10.9+

## Installation

### Install Homebrew

Follow the instructions on [this page](http://brew.sh/)

### Install Python

* `brew install python` or `brew install python3`

### Install Qt and PyQt4

* Download and install Qt from the [Qt site](http://download.qt.io/archive/qt/4.8/4.8.6/)
  directly. This is very important because the Homebrew versions are not compatible between
  MacOS versions.

* Run
  
  - `python symlink-qt.py` or
  - `python3 symlink-qt.py`

  to create a Homebrew package (using symlinks) from the Qt installation

* Install PyQt

  - For Python 2

    + `brew install --build-from-source --without-python3 sip`
    + `brew install --build-from-source --without-python3 pyqt`

  - For Python 3

    + `brew install --build-from-source --with-python3 --without-python sip`
    + `brew install --build-from-source --with-python3 --without-python pyqt`

* *Note*: Ignore the Homebrew warnings printed when installing PyQt4. They are
  not important

### Install the main Python scientific libraries

*Note*: If you are using Python 3, please use `pip3` instead of `pip`

* `pip install nose`
* `pip install numpy`
* `pip install scipy`
* `pip install matplotlib`

### Install IPython

* `pip install pyzmq`
* `pip install pygments`
* `pip install --no-deps ipython` (For the stable release)
* `pip install https://github.com/ipython/ipython/tarball/master` (From git)

### Install other scientific libraries

* `pip install pillow`
* `pip install scikit-learn`
* `pip install scikit-image`
* `pip install pandas`
* `pip install sympy`
* `pip install patsy`
* `pip install statsmodels`
* `pip install seaborn`

### Install Spyder deps

* `pip install pyflakes`
* `pip install rope`
* `pip install sphinx==1.2.1`
* `pip install pylint`
* `pip install pep8`
* `pip install psutil`

### Install py2app (to build the app)

* `pip install py2app`

### Finally: Don't install Spyder

It will be added to the app by `py2app`.


## Create the app

* Move to the root of your Spyder repo

* Run
  
    * `python setup.py build`
    * `python create_app.py py2app`

* Fix a possible IPython Qt crash

  Sometimes IPython is unable to detect PyQt4, which makes the app to crash
  immediately on startup. To fix it run

  `nano -w dist/Spyder.app/Contents/Resources/lib/python3.4/IPython/external/qt_loaders.py`

  then look for the function `has_binding` and make it return True after its
  first line, like this

  ```python
  def has_binding(api):
      """Safely check for PyQt4/5 or PySide, without importing
      submodules

      Parameters
      ----------
      api : str [ 'pyqtv1' | 'pyqt' | 'pyqt5' | 'pyside' | 'pyqtdefault']
           Which module to check for

      Returns
      -------
      True if the relevant module appears to be importable
      """
      return True
      ...
  ```

* If everything has gone well, you should see an `Spyder` or `Spyder-Py2` file
  under the `dist` dir. You can run it by double clicking on it on Finder or
  with this command in a terminal

  - `open dist/Spyder.app` or
  - `open dist/Spyder-Py2.app`


## Create the DMG

* Clone this repo and `cd` to its root

* Run `create_dmg.sh` with the appropiate options, e.g.

    `./create_dmg.sh --app=../spyder/dist/Spyder.app --name=spyder-2.3.0-py3.4.dmg`

* If everything has gone well, you should see a file called
  `spyder-2.3.0-py3.4.dmg` in the same dir. This is the file ready to upload
  to our downloads site.
