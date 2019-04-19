# from cloudmesh.aws.api.manager import Manager
from cloudmesh.aws.api.Provider import Provider

from cloudmesh.common.Printer import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.parameter import Parameter
from cloudmesh.management.configuration.config import Active
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.variables import Variables
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.management.configuration.arguments import Arguments
from cloudmesh.common.Shell import Shell
from cloudmesh.common.error import Error
from pprint import pprint



class AwsCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_aws(self, args, arguments):
        """
        ::

            Usage:
                vm ping [NAMES] [--cloud=CLOUDS] [--count=N] [--processors=PROCESSORS]
                vm check [NAMES] [--cloud=CLOUDS] [--processors=PROCESSORS]
                vm status [NAMES] [--cloud=CLOUDS]
                vm console [NAME] [--force]
                vm start [NAMES] [--cloud=CLOUD] [--dryrun]
                vm stop [NAMES] [--cloud=CLOUD] [--dryrun]
                vm terminate [NAMES] [--cloud=CLOUD] [--dryrun]
                vm delete [NAMES] [--cloud=CLOUD] [--dryrun]
                vm refresh [--cloud=CLOUDS]
                vm list [NAMES]
                        [--cloud=CLOUDS]
                        [--output=OUTPUT]
                        [--refresh]
                vm boot [--name=VMNAMES]
                        [--cloud=CLOUD]
                        [--username=USERNAME]
                        [--image=IMAGE]
                        [--flavor=FLAVOR]
                        [--public]
                        [--secgroup=SECGROUPs]
                        [--key=KEY]
                        [--dryrun]
                vm boot [--n=COUNT]
                        [--cloud=CLOUD]
                        [--username=USERNAME]
                        [--image=IMAGE]
                        [--flavor=FLAVOR]
                        [--public]
                        [--secgroup=SECGROUPS]
                        [--key=KEY]
                        [--dryrun]
                vm run [--name=VMNAMES] [--username=USERNAME] [--dryrun] COMMAND
                vm script [--name=NAMES] [--username=USERNAME] [--dryrun] SCRIPT
                vm ip assign [NAMES]
                          [--cloud=CLOUD]
                vm ip show [NAMES]
                           [--group=GROUP]
                           [--cloud=CLOUD]
                           [--output=OUTPUT]
                           [--refresh]
                vm ip inventory [NAMES]
                vm ssh [NAMES] [--username=USER]
                         [--quiet]
                         [--ip=IP]
                         [--key=KEY]
                         [--command=COMMAND]
                         [--modify-knownhosts]
                vm rename [OLDNAMES] [NEWNAMES] [--force] [--dryrun]
                vm wait [--cloud=CLOUD] [--interval=SECONDS]
                vm info [--cloud=CLOUD]
                        [--output=OUTPUT]
                vm username USERNAME [NAMES] [--cloud=CLOUD]
                vm resize [NAMES] [--size=SIZE]

            Arguments:
                OUTPUT         the output format
                COMMAND        positional arguments, the commands you want to
                               execute on the server(e.g. ls -a) separated by ';',
                               you will get a return of executing result instead of login to
                               the server, note that type in -- is suggested before
                               you input the commands
                NAME           server name. By default it is set to the name of last vm from database.
                NAMES          server name. By default it is set to the name of last vm from database.
                KEYPAIR_NAME   Name of the vm keypair to be used to create VM. Note this is
                               not a path to key.
                NEWNAMES       New names of the VM while renaming.
                OLDNAMES       Old names of the VM while renaming.

            Options:
                --output=OUTPUT   the output format [default: table]
                -H --modify-knownhosts  Do not modify ~/.ssh/known_hosts file
                                      when ssh'ing into a machine
                --username=USERNAME   the username to login into the vm. If not
                                      specified it will be guessed
                                      from the image name and the cloud
                --ip=IP          give the public ip of the server
                --cloud=CLOUD    give a cloud to work on, if not given, selected
                                 or default cloud will be used
                --count=COUNT    give the number of servers to start
                --detail         for table, a brief version
                                 is used as default, use this flag to print
                                 detailed table
                --flavor=FLAVOR  give the name or id of the flavor
                --group=GROUP          give the group name of server
                --secgroup=SECGROUP    security group name for the server
                --image=IMAGE    give the name or id of the image
                --key=KEY        specify a key to use, input a string which
                                 is the full path to the private key file
                --keypair_name=KEYPAIR_NAME   Name of the vm keypair to
                                              be used to create VM.
                                              Note this is not a path to key.
                --user=USER      give the user name of the server that you want
                                 to use to login
                --name=NAME      give the name of the virtual machine
                --force          rename/ delete vms without user's confirmation
                --command=COMMAND
                                 specify the commands to be executed


            Description:
                commands used to boot, start or delete servers of a cloud

                vm default [options...]
                    Displays default parameters that are set for vm boot either
                    on the default cloud or the specified cloud.

                vm boot [options...]
                    Boots servers on a cloud, user may specify flavor, image
                    .etc, otherwise default values will be used, see how to set
                    default values of a cloud: cloud help

                vm start [options...]
                    Starts a suspended or stopped vm instance.

                vm stop [options...]
                    Stops a vm instance .

                vm delete [options...]

                    Delete servers of a cloud, user may delete a server by its
                    name or id, delete servers of a group or servers of a cloud,
                    give prefix and/or range to find servers by their names.
                    Or user may specify more options to narrow the search

                vm floating_ip_assign [options...]
                    assign a public ip to a VM of a cloud

                vm ip show [options...]
                    show the ips of VMs

                vm ssh [options...]
                    login to a server or execute commands on it

                vm list [options...]
                    same as command "list vm", please refer to it

                vm status [options...]
                    Retrieves status of last VM booted on cloud and displays it.

                vm refresh [--cloud=CLOUDS]
                    this command refreshes the data for virtual machines,
                    images and flavors for the specified clouds.

                vm ping [NAMES] [--cloud=CLOUDS] [--count=N] [--processors=PROCESSORS]
                     pings the specified virtual machines, while using at most N pings.
                     The ping is executed in parallel.
                     If names are specifies the ping is restricted to the given names in
                     parameter format. If clouds are specified, names that are not in
                     these clouds are ignored. If the name is set in the variables
                     this name is used.

            Tip:
                give the VM name, but in a hostlist style, which is very
                convenient when you need a range of VMs e.g. sample[1-3]
                => ['sample1', 'sample2', 'sample3']
                sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']

            Quoting commands:
                cm vm login gvonlasz-004 --command=\"uname -a\"

            Limitations:

                Azure: rename is not supported
        """
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

        # VERBOSE.print(arguments, verbose=9)

        variables = Variables()

        pprint(arguments)
        # pprint(variables)

        provider = Provider()

        if arguments.refresh:

            names = []

            clouds, names = Arguments.get_cloud_and_names("refresh", arguments, variables)

            return ""

        elif arguments.ping:
            pings = int(arguments.N or 3)

            clouds, names = Arguments.get_cloud_and_names("ping", arguments, variables)

            public_ips = list(provider.get_publicIPs(names).values())
            public_ips = [y for x in public_ips for y in x]

            def console_response(x):
                if x[1] == 0:
                    Console.ok("ping " + x[0] + ' success.')
                else:
                    Console.error("ping " + x[0] + ' failure. return code: ' + str(x[1]))

            list(map(console_response, provider.ping(public_ips)))

        elif arguments.check:

            names = []

            clouds, names = Arguments.get_cloud_and_names("check", arguments, variables)

            return ""

        elif arguments.status:
            clouds, names = Arguments.get_cloud_and_names("status", arguments, variables)

            pprint(provider.status(names))

        elif arguments.start:
            clouds, names = Arguments.get_cloud_and_names("start", arguments, variables)

            pprint(provider.start(names))

        elif arguments.stop:
            clouds, names = Arguments.get_cloud_and_names("stop", arguments, variables)

            pprint(provider.stop(names))

        elif arguments.terminate:
            clouds, names = Arguments.get_cloud_and_names("terminate", arguments, variables)

            pprint(provider.destroy(names))

        ## terminate & delete difference??
        elif arguments.delete:
            clouds, names = Arguments.get_cloud_and_names("delete", arguments, variables)

            pprint(provider.destroy(names))

        elif arguments.boot:

            clouds, names = Arguments.get_cloud_and_names("boot", arguments, variables)

            pprint(provider.reboot(names))

        elif arguments.list:
            clouds, names = Arguments.get_cloud_and_names("list", arguments, variables)

            pprint(provider.info(names))

        elif arguments.info:
            clouds, names = Arguments.get_cloud_and_names("info", arguments, variables)

            pprint(provider.info(names))

        elif arguments.rename:
            print("rename")

        elif arguments.ip and arguments.show:
            print("show ips")

        elif arguments.ip and arguments.assign:
            print("assign ip address")
            clouds, names = Arguments.get_cloud_and_names("ip", arguments, variables)

            pprint(provider.assign_public_ip(names))

        elif arguments.ip and arguments.inventory:
            print("list ips that could be assigned")

        elif arguments.username:

            """
            vm username USERNAME [NAMES] [--cloud=CLOUD]
            """
            print("sets the username for the vm")

        elif arguments.default:

            print("sets defaults for the vm")

        elif arguments.run:
            """
            vm run [--name=NAMES] [--username=USERNAME] [--dryrun] COMMAND

            """
            pass
        elif arguments.script:

            """
            vm script [--name=NAMES] [--username=USERNAME] [--dryrun] SCRIPT
            """
            pass

        elif arguments.resize:
            """
            vm resize [NAMES] [--size=SIZE]
            """
            pass

        elif arguments.ssh:
            print("ssh")
            print(variables['--ip'])
            print(arguments['--username'])

            provider.ssh('ec2user', '52.43.129.118')

        elif arguments.console:
            # vm console [NAME] [--force]

            names = Arguments.get_names(arguments, variables)

            for name in names:
                # r = vm.console(name,force=argument.force)
                Console.msg("{label} {name}".format(label="console", name=name))
            return

        elif arguments.wait:
            """
            vm wait [--cloud=CLOUD] [--interval=SECONDS]
            """
            print("waits for the vm till its ready and one can login")

        return
        # if arguments.flavor and arguments.list:
        #     pprint(provider.flavors())
        #
        # elif arguments.image and arguments.list:
        #     pprint(provider.images())
        #
        # elif arguments.list:
        #     pprint(provider.list())
        #
        # elif arguments.info:
        #     names = self.get_variables(arguments, variables, '--name', 'vm')
        #     pprint(provider.info(names))
        #
        # elif arguments.reboot:
        #     names = self.get_variables(arguments, variables, '--name', 'vm')
        #     pprint(provider.reboot(names))
        #
        # elif arguments.ip and arguments.show:
        #     names = self.get_variables(arguments, variables, '--name', 'vm')
        #     pprint(provider.get_publicIPs(names))

        # elif arguments.ping:
        #     names = self.get_variables(arguments, variables, '--name', 'vm')
        #     timer = self.get_variables(arguments, variables, '--timer', 'timer')
        #
        #     public_ips = list(provider.get_publicIPs(names).values())
        #     public_ips = [y for x in public_ips for y in x]
        #
        #     def console_response(x):
        #         if x[1] == 0:
        #             Console.ok("ping " + x[0] + ' success.')
        #         else:
        #             Console.error("ping " + x[0] + ' failure. return code: ' + str(x[1]))
        #
        #     list(map(console_response, provider.ping(public_ips, timeout=timer)))
        #
        # elif arguments.check:
        #     keypair_name = self.get_variables(arguments, variables, '--keypair_name', 'keypair')[0]
        #     names = self.get_variables(arguments, variables, '--name', 'vm')
        #     timer = self.get_variables(arguments, variables, '--timer', 'timer')
        #
        #     print(provider.check(names=names, keypair=keypair_name, timeout=timer))
        #
        # else:
        #     Console.error("function not available")
