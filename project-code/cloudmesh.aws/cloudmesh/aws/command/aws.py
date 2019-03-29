from __future__ import print_function
# from cloudmesh.shell.command import command
# from cloudmesh.shell.command import PluginCommand
# from cloudmesh.common.console import Console
# from cloudmesh.common.util import path_expand

from cloudmesh.common.Printer import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.parameter import Parameter

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
                aws list
                aws info [NAMES]
                aws ip show [NAMES]
                aws ping -n [--wait=TIMEOUT] [NAMES]
                aws ping -p [--wait=TIMEOUT] [IPS]
                aws ppp

          Arguments:
                NAMES  server name.
                IPS  ip addresses

          Options:
                -f    specify the file
                -p    specify ip addresses
                -n    specify vm names
                -wait=TIMEOUT    specify the wait time for processes


          Description:
                commands used to boot, start or delete servers of a cloud

                aws list
                    list the vms on the cloud
        """

        map_parameters(arguments,
                       'flavor',
                       'image')

        VERBOSE.print(arguments, verbose=9)

        variables = Variables()

        # pprint(arguments)

        provider = Provider()

        if arguments.list:
            pprint(provider.list())

        elif arguments.info:
            names = Parameter.expand(arguments.NAMES)
            pprint(provider.info(names))

        # elif arguments.create:
        #     print("bug in create function")
        ##     cms aws create --name=test --image=ami-0bbe6b35405ecebdb --flavor=t2.micro
        #     provider.create(name=arguments.name, image=arguments.image, size=arguments.size)

        elif arguments.ip and arguments.show:
            names = Parameter.expand(arguments.NAMES)
            pprint(provider.get_publicIPs(names))

        elif arguments.ping:
            ## if given node names
            timeout = int(arguments['--wait'])

            if arguments['-n']:
                names = Parameter.expand(arguments.NAMES)
                public_ips = list(provider.get_publicIPs(names).values())
                public_ips = [i[0] for i in public_ips] #flatten
            ## if given ips
            if arguments['-p']:
                public_ips = Parameter.expand(arguments.IPS)
            provider.ping(public_ips, timeout=timeout)

        else:
            Console.error("function not available")
