pl-mgz_converter
================================

.. image:: https://badge.fury.io/py/mgz_converter.svg
    :target: https://badge.fury.io/py/mgz_converter

.. image:: https://travis-ci.org/FNNDSC/mgz_converter.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/mgz_converter

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-mgz_converter

.. contents:: Table of Contents


Abstract
--------

``mgz_converter.py`` is a ChRIS-based application that takes Brain MRI images present in mgz format from the input diretctory, converts them to png or npy format based on the conversion type and saves output to the output directory.


Synopsis
--------

.. code::

    python mgz_converter.py                                         \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        [--conversion_type <conversion_type>]                       \
        <inputDir>                                                  \
        <outputDir>                                                 \

Agruments
---------

.. code::

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.

    [--conversion_type <conversion_type>]     
    Should be specified,
    If the <conversion_type> is 1, converts the input mgz images to png
    If the <conversion_type> is 2, converts the input mgz images to npy

Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install mgz_converter

and run with

.. code:: bash

    mgz_converter.py --man /tmp /tmp

to get inline help. The app should also understand being called with only two positional arguments

.. code:: bash

    mgz_converter.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash
    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/out:/outgoing                                                                 \
            pl-mgz_converter mgz_converter.py --conversion_type <conversion_type>                           \
            /incoming /outgoing                                                                             

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing                                          \
            pl-mgz_converter mgz_converter.py --conversion_type <conversion_type>                           \
            --man                                                                                           \
            /incoming /outgoing

Examples
--------

Convert mgz images to png 
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/out:/outgoing                                             \
            pl-mgz_converter mgz_converter.py --conversion_type 1                                                       \
            /incoming /outgoing   


This will convert the ``*.mgz`` images present in the input directory to ``*.png`` format and saves them inside out/png directory

Convert mgz images to npy 
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash
    
    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/out:/outgoing                                             \
            pl-mgz_converter mgz_converter.py  --conversion_type 2                      \
            /incoming /outgoing   

This will convert the ``*.mgz`` images present in the input directory to ``*.npy`` format and saves them inside out/numpy directory


