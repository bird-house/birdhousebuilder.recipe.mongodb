# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe mongodb"""

       
class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.anaconda_home = b_options.get('anaconda-home', anaconda_home)
        self.conda_channels = b_options.get('conda-channels')

    def install(self):
        """
        install conda packages
        """
        pkgs = self.options.get('pkgs', '')
        return install_pkgs(self.anaconda_home, pkgs, self.conda_channels) 

    def update(self):
        return self.install()

def uninstall(name, options):
    pass

