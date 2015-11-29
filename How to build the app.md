
# How to build the Spyder MacOS X application

**Important note**: These instructions are valid only for MacOS X 10.9+

## Installation

### Install Homebrew

Follow the instructions on [this page](http://brew.sh/)

### Install Python

* `brew install python`
* `brew install python3`

### Install Qt and PyQt4

* Install Qt

  `brew install qt`

* Install PyQt

  - `brew install --with-python3 sip`
  - `brew install --with-python3 pyqt`

### Install the main Python scientific libraries

*Note*: If you are using Python 3, please use `pip3` instead of `pip2`

* `pip2 install nose`
* `pip2 install numpy`
* `pip2 install scipy`
* `pip2 install matplotlib`

### Install Jupyter

* `pip2 install pyzmq`
* `pip2 install pygments`
* `pip2 install qtconsole`
* `pip2 install nbconvert`

### Install other scientific libraries

* `pip2 install pillow`
* `pip2 install scikit-learn`
* `pip2 install scikit-image`
* `pip2 install pandas`
* `pip2 install sympy`
* `pip2 install patsy`
* `pip2 install statsmodels`
* `pip2 install seaborn`

### Install Spyder deps

* `pip2 install pyflakes`
* `pip2 install rope`
* `pip2 install sphinx`
* `pip2 install pylint`
* `pip2 install pep8`
* `pip2 install psutil`

### Install py2app (to build the app)

* `pip2 install py2app`

### Finally: Don't install Spyder

It will be added to the app by `py2app`.


## Create the app

* Move to the root of your Spyder repo

* Run
  
    * `python2 setup.py build`
    * `python2 create_app.py py2app`

* Fix a bug in py2app 0.9 (See [this issue](https://bitbucket.org/ronaldoussoren/py2app/issue/137/py2app-problems-using-enthought-python)
  for the suggested solution)

  If you encounter a bug like this one, after running the last command:

  ```python-traceback
  Traceback (most recent call last):
    ...
    File "/usr/local/lib/python3.5/site-packages/macholib/MachOGraph.py", line 49, in locate
      loader=loader.filename)
  TypeError: dyld_find() got an unexpected keyword argument 'loader'
  ```

  Please run

  `nano -w /usr/local/lib/python3.5/site-packages/macholib/MachOGraph.py`

  look for the `locate` method of the `MachOGraph` class, then inside it identify
  a call for `dyld_find` and replace its `loader` kwarg for `loader_path`

* Fix a possible qtconsole crash

  Sometimes `qtconsole` is unable to detect PyQt4, which makes the app to crash
  immediately on startup. To fix it run

  `nano -w dist/Spyder.app/Contents/Resources/lib/python3.5/qtconsole/qt_loaders.py`

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
  with these commands on a terminal

  - `open dist/Spyder.app` or
  - `open dist/Spyder-Py2.app`


## Create the DMG

* Clone this repo and `cd` to its root

* Run `create_dmg.sh` with the appropiate options, e.g.

    `./create_dmg.sh --app=../spyder/dist/Spyder.app --name=spyder-2.3.8-py3.5.dmg`

* If everything has gone well, you should see a file called
  `spyder-2.3.8-py3.5.dmg` in the same dir. This is the file ready to upload
  to our downloads site.
