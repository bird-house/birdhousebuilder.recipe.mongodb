# -*- coding: utf-8 -*-

"""Recipe mongodb"""

import os
from mako.template import Template
import logging

import zc.buildout
import zc.recipe.deployment
from birdhousebuilder.recipe import conda, supervisor
from birdhousebuilder.recipe.conda import conda_env_path

templ_config = Template(filename=os.path.join(os.path.dirname(__file__), "mongodb.conf"))
templ_cmd = Template('${env_path}/bin/mongod --config ${etc_directory}/mongodb.conf') 

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs mongodb as conda package and inits mongodb database."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.options['name'] = self.options.get('name', self.name)
        self.name = self.options['name']

        self.logger = logging.getLogger(name)

        deployment = zc.recipe.deployment.Install(buildout, 'mongodb', {
                                                'prefix': self.options['prefix'],
                                                'user': self.options['user'],
                                                'etc-user': self.options['user']})
        deployment.install()
        
        self.options['etc-prefix'] = self.options['etc_prefix'] = deployment.options['etc-prefix']
        self.options['var-prefix'] = self.options['var_prefix']  = deployment.options['var-prefix']
        self.options['etc-directory'] = self.options['etc_directory'] = deployment.options['etc-directory']
        self.options['lib-directory'] = self.options['lib_directory'] = deployment.options['lib-directory']
        self.prefix = self.options['prefix']

        self.env_path = conda_env_path(buildout, options)
        self.options['env_path'] = self.env_path

        self.options['user'] = self.options.get('user', '')
        self.options['bind_ip'] = self.options.get('bind_ip', '127.0.0.1')
        self.options['port'] = self.options.get('port', '27017')
        #self.options['logstdout'] = conda.as_bool(self.options.get('logstdout', 'true'))
        
        self.conda_channels = b_options.get('conda-channels')

    def install(self):
        installed = []
        installed += list(self.install_mongodb())
        installed += list(self.install_config())
        installed += list(self.install_program())
        return installed

    def install_mongodb(self):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'mongodb'})

        return script.install()
        
    def install_config(self):
        """
        install mongodb config file
        """
        text = templ_config.render(**self.options)
        conf_path = os.path.join(self.options['etc-directory'], 'mongodb.conf')
        
        with open(conf_path, 'wt') as fp:
            fp.write(text)
        return [conf_path]

    def install_program(self):
        script = supervisor.Recipe(
            self.buildout,
            self.name,
            {'prefix': self.options['prefix'],
             'user': self.options.get('user'),
             'program': 'mongodb',
             'command': templ_cmd.render(**self.options),
             'priority': '10',
             'autostart': 'true',
             'autorestart': 'false',
             })
        return script.install()

    def update(self):
        return self.install()

def uninstall(name, options):
    pass

