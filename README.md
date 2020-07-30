# VakioMax 4

This time with PyQt5

Use [pyenv](https://github.com/pyenv/pyenv#installation):

    env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.7.8

Then use poetry:

    poetry install
    poetry shell

Inside the virtualenv, use fbs:

    fbs run

Build with fbs:

    fbs freeze
    fbs installer
