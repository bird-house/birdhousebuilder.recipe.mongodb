# -*- coding: utf-8 -*-

"""Recipe mongodb"""

import os
from mako.template import Template

import zc.buildout
from birdhousebuilder.recipe import conda, supervisor
from birdhousebuilder.recipe.conda import conda_env_path

templ_config = Template(filename=os.path.join(os.path.dirname(__file__), "mongodb.conf"))
templ_cmd = Template('${env_path}/bin/mongod --config ${etc_prefix}/mongodb.conf') 

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs mongodb as conda package and inits mongodb database."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        deployment = self.deployment = options.get('deployment')
        if deployment:
            self.options['prefix'] = buildout[deployment].get('prefix')
            self.options['etc_prefix'] = buildout[deployment].get('etc-prefix')
            self.options['var_prefix'] = buildout[deployment].get('var-prefix')
        else:
            self.options['prefix'] = os.path.join(buildout['buildout']['parts-directory'], self.name)
            self.options['etc_prefix'] = os.path.join(self.options['prefix'], 'etc')
            self.options['var_prefix'] = os.path.join(self.options['prefix'], 'var')
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

        conda.makedirs( os.path.join(self.options['var_prefix'], 'lib', 'mongodb') )
        #conda.makedirs( os.path.join(self.prefix, 'var', 'log', 'mongodb') )
        
        return script.install()
        
    def install_config(self):
        """
        install mongodb config file
        """
        result = templ_config.render(**self.options)
    
        output = os.path.join(self.options['etc_prefix'], 'mongodb.conf')
        conda.makedirs(os.path.dirname(output))
        
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_program(self):
        script = supervisor.Recipe(
            self.buildout,
            self.name,
            {'user': self.options.get('user'),
             'deployment': self.deployment,
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

