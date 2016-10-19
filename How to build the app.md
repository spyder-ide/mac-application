
# How to build the Spyder MacOS X application

**Important note**: These instructions are valid only for MacOS X 10.9+

## Installation

### Install Homebrew

Follow the instructions on [this page](http://brew.sh/)

### Install Python

* `brew install python3`

### Install PyQt

* `pip3 install pyqt5`

### Install the main Python scientific libraries

* `pip3 install nose`
* `pip3 install numpy`
* `pip3 install scipy`
* `pip3 install matplotlib`

### Install Jupyter

* `pip3 install pyzmq`
* `pip3 install pygments`
* `pip3 install qtconsole`
* `pip3 install nbconvert`

### Install other scientific libraries

* `pip3 install pillow`
* `pip3 install scikit-learn`
* `pip3 install scikit-image`
* `pip3 install pandas`
* `pip3 install sympy`
* `pip3 install patsy`
* `pip3 install statsmodels`
* `pip3 install seaborn`


### Install Spyder deps

* `pip3 install qtpy`
* `pip3 install qtawesome`
* `pip3 install pyflakes`
* `pip3 install rope`
* `pip3 install jedi`
* `pip3 install sphinx`
* `pip3 install pylint`
* `pip3 install pep8`
* `pip3 install psutil`

### Install py2app (to build the app)

* `pip3 install py2app`

### Finally: Don't install Spyder

It will be added to the app by `py2app`.


## Create the app

* Move to the root of your Spyder repo

* Run
  
    * `python3 setup.py build`
    * `python3 create_app.py py2app`

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

* Fix a bug in Babel

  If you encounter a bug like this one:

  ```python-traceback
  File "/Users/carlos/Projects/spyder/dist/Spyder.app/Contents/Resources/lib/python3.5/babel/localtime/_unix.py", line 73, in _get_localzone
  Oct  8 17:33:16 Carloss-Mac.local Spyder[28350] <Notice>: TypeError: cannot use a string pattern on a bytes-like object
  ```

  Please run

  nano -w dist/Spyder.app/Contents/Resources/lib/python3.5/babel/localtime/_unix.py

  look for this line

  ```python
  tz_match = _systemconfig_tz.search(sys_result)
  ```

  in the function `_get_localzone` and change it to

  ```python
  tz_match = None
  ```

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

* If everything has gone well, you should see an `Spyder` directory under
  the `dist` dir. You can run it by double clicking on it on Finder or
  with this command on a terminal

  - `open dist/Spyder.app`


## Create the DMG

* Clone this repo and `cd` to its root

* Run `create_dmg.sh` with the appropiate options, e.g.

    `./create_dmg.sh --app=../spyder/dist/Spyder.app --name=spyder-3.0.0-py3.5.dmg`

* If everything has gone well, you should see a file called
  `spyder-3.0.0-py3.5.dmg` in the same dir. This is the file ready to upload
  to our downloads site.
