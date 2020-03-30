
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

I recommend using [Homebrew](http://brew.sh/) to install Python, along with pyenv and pyenv-virtualenv (if you plan to use these for virtual environment management).

After installing Homebrew, run:
```
$ brew install python3, pyenv, pyenv-virtualenv
```

If you use pyenv must enable frameworks in your Python installation, as follows.
If you are using venv, you can ignore this.
```
$ PYTHON_CONFIGURE_OPTS='--enable-framework'
$ pyenv install <python version>
```

### Create Virtual Environment

First, change your current working directory to your local clone of this repository.
If you currently have any conda environment(s) activated, then deactivate them completely, i.e. you should not be in any conda environment, not even base.

Next, create the virtual environment and populate it with the necessary package requirements.
If you are using pyenv with pyenv-virtualenv, it will look like this:
```
$ pyenv virtualenv <python version> env-spy-dev
$ pyenv local env-spy-dev
(env-spy-dev) $ pip install --upgrade pip
(env-spy-dev) $ pip install -r requirements.txt
```

If you are using venv, it will look like this:
```
$ python -m venv --clear --copies env-spy-dev
$ source env-spy-dev/bin/activate
(env-spy-dev) $ pip install --upgrade pip
(env-spy-dev) $ pip install -r requirements.txt
```

### Create the Standalone Application

For the build to work properly, your local clones of both spyder and spyder-kernels must be at the same directory level as your local clone of this repository.
To create the standalone application and package it in a dmg disk image run:
```
(env-spy-dev) $ python setup.py py2app
```

After a whole lot of screen dump, and if everything went well, you should now have two files in the `dist` folder of this repository:
* Spyder.app
* Spyder-\<Spyder version\> Py-\<Python version\>.dmg
