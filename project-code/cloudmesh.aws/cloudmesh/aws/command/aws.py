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
                -f    specify the file
                --name=NAMES    give the name of the virtual machine
                --timer=TIMEOUT    specify the wait time for processes

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

        pprint(arguments)

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
            print('ping')
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

            def f(x):
                if x[1] == 0:
                    Console.ok("ping " + x[0] + ' successful.')
                else:
                    Console.error("ping " + x[0] + ' failure. return code: ' + str(x[1]))

            list(map(f, provider.ping(public_ips, timeout=timer)))

        else:
            # variable = Variables()
            # print(variable['vm'])
            # for k in variable:
            #     print(k)
            # print(variable.vm)
            Console.error("function not available")
