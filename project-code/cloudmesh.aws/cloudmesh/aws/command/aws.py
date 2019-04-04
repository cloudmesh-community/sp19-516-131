from __future__ import print_function
# from cloudmesh.shell.command import command
# from cloudmesh.shell.command import PluginCommand
# from cloudmesh.common.console import Console
# from cloudmesh.common.util import path_expand

from cloudmesh.common.Printer import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.parameter import Parameter

# from cloudmesh.aws.api.manager import Manager
from cloudmesh.aws.api.Provider import Provider

from cloudmesh.management.configuration.config import Active
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.shell.variables import Variables
from cloudmesh.terminal.Terminal import VERBOSE
from cloudmesh.management.configuration.arguments import Arguments
from cloudmesh.common.Shell import Shell

from pprint import pprint


class AwsCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_aws(self, args, arguments):
        """
        ::

          Usage:
                aws flavor list
                aws image list
                aws list
                aws info [--name=NAMES]
                aws reboot [--name=NAMES]
                aws ip show [--name=NAMES]
                aws ping [--name=NAMES]
                         [--timer=TIMEOUT]
                aws check [--name=NAMES]
                          [--keypair_name=KEYPAIR_NAME]
                          [--timer=TIMEOUT]
                aws ppp [--name=NAMES]

          Arguments:
            NAMES       server name. By default it is set to the name of last vm from database.
            TIMEOUT     wait time. By default it is set to the last timer used.


          Options:
                --name=NAMES        give the name of the virtual machine
                --timer=TIMEOUT     specify the wait time for processes

          Description:
                commands used to boot, start or delete servers of a cloud

                aws list flavors
                    list the flavors from the cloud

                aws list images
                    list the images from the cloud

                aws list
                    list the vms on the cloud
        """

        map_parameters(arguments,
                       'flavor',
                       'image')

        VERBOSE.print(arguments, verbose=9)

        variables = Variables()

        pprint(arguments)

        provider = Provider()

        if arguments.flavor and arguments.list:
            pprint(provider.flavors())

        elif arguments.image and arguments.list:
            pprint(provider.images())

        elif arguments.list:
            pprint(provider.list())

        elif arguments.info:
            names = self.get_variables(arguments, variables, '--name', 'vm')
            pprint(provider.info(names))

        elif arguments.reboot:
            names = self.get_variables(arguments, variables, '--name', 'vm')
            pprint(provider.reboot(names))

        elif arguments.ip and arguments.show:
            names = self.get_variables(arguments, variables, '--name', 'vm')
            pprint(provider.get_publicIPs(names))

        elif arguments.ping:
            names = self.get_variables(arguments, variables, '--name', 'vm')
            timer = self.get_variables(arguments, variables, '--timer', 'timer')

            public_ips = list(provider.get_publicIPs(names).values())
            public_ips = [y for x in public_ips for y in x]

            def console_response(x):
                if x[1] == 0:
                    Console.ok("ping " + x[0] + ' success.')
                else:
                    Console.error("ping " + x[0] + ' failure. return code: ' + str(x[1]))

            list(map(console_response, provider.ping(public_ips, timeout=timer)))

        elif arguments.check:
            keypair_name = self.get_variables(arguments, variables, '--keypair_name', 'keypair')[0]
            names = self.get_variables(arguments, variables, '--name', 'vm')
            timer = self.get_variables(arguments, variables, '--timer', 'timer')

            print(provider.check(names=names, keypair=keypair_name, timeout=timer))

        else:
            Console.error("function not available")

    def get_variables(self, arguments, variables, arg_key, var_key):
        ret = Parameter.expand(arguments[arg_key])
        if ret == None:
            return Parameter.expand(variables[var_key])
        else:
            variables[var_key] = arguments[arg_key]
            return ret
