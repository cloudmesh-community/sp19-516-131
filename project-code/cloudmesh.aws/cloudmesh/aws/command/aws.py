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
                aws info [NAMES]
                aws ip show [NAMES]
                aws ping [--timer=TIMEOUT]
                         [--name=NAMES]
                aws ppp

          Arguments:
                NAMES  server name.
                IPS  ip addresses

          Options:
                --name=NAMES    give the name of the virtual machine
                --timer=TIMEOUT    specify the wait time for processes

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
            names = Parameter.expand(arguments.NAMES)
            pprint(provider.info(names))

        elif arguments.ip and arguments.show:
            names = Parameter.expand(arguments.NAMES)
            pprint(provider.get_publicIPs(names))

        elif arguments.ping:
            variable = Variables()

            names = Parameter.expand(arguments['--name'])
            if names == None:
                names = variable['vm']
            else:
                variable['vm'] = arguments['--name']

            timer = Parameter.expand(arguments['--timer'])
            if timer == None:
                timer = variable['timer']
            else:
                variable['timer'] = arguments['--timer']

            public_ips = list(provider.get_publicIPs(names).values())
            public_ips = [i[0] for i in public_ips] #flatten

            def console_response(x):
                if x[1] == 0:
                    Console.ok("ping " + x[0] + ' successful.')
                else:
                    Console.error("ping " + x[0] + ' failure. return code: ' + str(x[1]))

            list(map(console_response, provider.ping(public_ips, timeout=timer)))

        else:
            # variable = Variables()
            # print(variable['vm'])
            # for k in variable:
            #     print(k)
            # print(variable.vm)
            Console.error("function not available")
