*******************************
birdhousebuilder.recipe.mongodb
*******************************

.. image:: https://travis-ci.org/bird-house/birdhousebuilder.recipe.mongodb.svg?branch=master
   :target: https://travis-ci.org/bird-house/birdhousebuilder.recipe.mongodb
   :alt: Travis Build


Introduction
************

``birdhousebuilder.recipe.mongodb`` is a `Buildout`_ recipe to install and setup `MongoDB`_ with `Anaconda`_.
This recipe is used by the `Birdhouse`_ project. 


.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://continuum.io/
.. _`MongoDB`: http://www.mongodb.org/
.. _`Supervisor`: http://supervisord.org/
.. _`Birdhouse`: http://bird-house.github.io/

Usage
*****

The recipe requires that Anaconda is already installed. You can use the buildout option ``anaconda-home`` to set the prefix for the anaconda installation. Otherwise the environment variable ``CONDA_PREFIX`` (variable is set when activating a conda environment) is used as conda prefix. 

The recipe will install the ``mongodb`` package from a conda channel in a conda environment defined by ``CONDA_PREFIX``. It setups a `MongoDB`_ database in ``{{prefix}}/var/lib/mongodb``. It deploys a `Supervisor`_ configuration for MongoDB in ``{{prefix}}/etc/supervisor/conf.d/mongodb.conf``. Supervisor can be started with ``{{prefix}}/etc/init.d/supervisor start``.

The recipe depends on ``birdhousebuilder.recipe.conda`` and ``birdhousebuilder.recipe.supervisor``.

Supported options
=================

The recipe supports the following options:

**anaconda-home**
   Buildout option pointing to the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.

Buildout options for ``mongodb``:

**bind-ip**
  The IP address that mongodb binds to in order to listen for connections from applications. Default: 127.0.0.1

**port**
  The TCP port on which the MongoDB instance listens for client connections. Default: 27017


Example usage
=============

The following example ``buildout.cfg`` installs MongoDB with Anaconda::

  [buildout]
  parts = myapp_mongodb

  [myapp_mongodb]
  recipe = birdhousebuilder.recipe.mongodb
  port = 27020

