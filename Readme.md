
## How to build the Spyder MacOS X application

**Important note**: These instructions have only been tested on MacOS X 10.14.6

To build the Spyder standalone Mac application you need:
* Python 3.x installed, *not* from Anaconda
* A local clone of the [spyder](https://github.com/spyder-ide/spyder) repository
* A local clone of the [spyder-kernels](https://github.com/spyder-ide/spyder-kernels) repository
* A local clone of this repository

Once you have the above requirements, you will create a virtual environment from which to build the application.

### Python 3.x installation

In principle, it doesn't matter where your Python installation comes from except that it cannot come from Anaconda.
I do not know exactly why an Anaconda installation does not work except that it has something to do with hardlinks.

I recommend using [Homebrew](http://brew.sh/) to install pyenv and pyenv-virtualenv (if you plan to use these for virtual environment management).
If you plan to use pyenv, you don't even need to install Python from Homebrew, since pyenv will install whatever python version you request.
If you don't plan to use pyenv, then you will need to install Python from Homebrew or elsewhere.

After installing Homebrew, run:
```
$ brew install pyenv, pyenv-virtualenv, xz
```
`xz` is a package that provides compression algorithms that Python should be built with to satisfy some packages, namely `pandas`.

The Python frameworks must be copied to the stand-alone application, so if you use pyenv you must enable frameworks in any Python installation that you plan to use to build the Spyder app.
```
$ PYTHON_CONFIGURE_OPTS=--enable-framework pyenv install <python version>
```

### Create Virtual Environment

First, change your current working directory to your local clone of this repository.
If you currently have any conda environment(s) activated, then deactivate them completely, i.e. you should not be in any conda environment, not even base.

Next, create the virtual environment and populate it with the necessary package requirements.
If you are using pyenv with pyenv-virtualenv, it will look like this:
```
$ pyenv virtualenv <python version> env-spy-dev
$ pyenv local env-spy-dev
(env-spy-dev) $ pip install -r req-base.txt -r req-build.txt -r req-user.txt
```
If you are using venv, it will look like this:
```
$ python -m venv --clear --copies env-spy-dev
$ source env-spy-dev/bin/activate
(env-spy-dev) $ pip install -r req-base.txt -r req-build.txt -r req-user.txt
```

`req-base.txt` contains the minimum required packages for Spyder to run.
`req-build.txt` contains only those packages required to build the stand-alone application.
`req-user.txt` contains optional packages to include, if desired, for use in iPython consoles launched from the "Same as Spyder" environment.
If you use external environments, such as conda, for your iPython consoles, you don't need `req-user.txt`.
The build command also provides an option to exclude these packages, so you may include them and still build the application without them, if you choose.

### Create the Standalone Application

For the build to work properly, your local clones of both `spyder` and `spyder-kernels` must be at the same directory level as your local clone of this repository.
To create the standalone application and package it in a dmg disk image run:
```
(env-spy-dev) $ python setup.py py2app
```

After a whole lot of screen dump, and if everything went well, you should now have two files in the `dist` folder of this repository:
* Spyder.app
* Spyder-\<Spyder version\> Py-\<Python version\>.dmg

The following commandline optional arguments are available:
* `py2app`: this causes the bundled app to be produced. Omitting this argument will run `setup.py` without building the app.
* `-A`: This causes py2app to build the application in "alias" mode; basically a quicker way to build the app for debugging, but is not very reliable.
* `--lite`: This will cause py2app to exclude the optional user packages from the application bundle (approximately 250MB).
* `--no-dmg`: This will prevent the dmg disk-image from being created.
