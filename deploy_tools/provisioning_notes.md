Provisioning a new site
=======================

## Required packages:

* Web server
* Python 3
* Git
* pip
* virtualenv

I'm using free service provided by PythonAnywhere and it already has all the
these packages installed.

## Server configuration

* Edit WSGI config file to disable the demo site and enable superlists
* Point to the location of virtualenv (~/sites/SITENAME/virtualenv)
* Configure the URL and path to the static files

## Create virtualenv and install needed packages

* $ cd sites/SITENAME
* $ virtualenv -p python3.4 virtualenv
* (virtualenv)$ pip install -r source/requirements.txt

## Folder structure:

/home/USERNAME
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv

