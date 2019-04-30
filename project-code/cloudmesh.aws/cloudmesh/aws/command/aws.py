# from cloudmesh.aws.api.manager import Manager
from cloudmesh.aws.api.VmProvider import Provider

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
from cloudmesh.common3.Shell import Shell as Shell3
from cloudmesh.common.error import Error
from pprint import pprint

from datetime import datetime
import hashlib

from libcloud.compute.base import NodeSize
class AwsCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_aws(self, args, arguments):
        """
        ::

            Usage:
                vm ping [NAMES] [--cloud=CLOUDS] [--count=N] [--processors=PROCESSORS]
                vm check [NAMES] [--cloud=CLOUDS] [--username=USERNAME] [--processors=PROCESSORS]
                vm status [NAMES] [--cloud=CLOUDS]
                vm console [NAME] [--force]
                vm start [NAMES] [--cloud=CLOUD] [--parallel] [--processors=PROCESSORS] [--dryrun]
                vm stop [NAMES] [--cloud=CLOUD] [--parallel] [--processors=PROCESSORS] [--dryrun]
                vm terminate [NAMES] [--cloud=CLOUD] [--parallel] [--processors=PROCESSORS] [--dryrun]
                vm delete [NAMES] [--cloud=CLOUD] [--parallel] [--processors=PROCESSORS] [--dryrun]
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
                           [--cloud=CLOUD],
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
                vm debug [NAMES]

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
                --parallel       execute commands in parallel


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

        """

        map_parameters(arguments,
                       'active',
                       'cloud',
                       'command',
                       'dryrun',
                       'flavor',
                       'force',
                       'output',
                       'group',
                       'image',
                       'interval',
                       'ip',
                       'key',
                       'modify-knownhosts',
                       'n',
                       'name',
                       'public',
                       'quiet',
                       'secgroup',
                       'size',
                       'username')

        # VERBOSE.print(arguments, verbose=9)

        variables = Variables()

        # pprint(arguments)
        # pprint(variables)

        provider = Provider()
        database = CmDatabase()

        # ok, but not tested
        if arguments.refresh:
            """vm refresh [--cloud=CLOUDS]"""
            provider.list()
            provider.flavors()
            provider.images()

        # ok
        elif arguments.ping:
            """vm ping [NAMES] [--cloud=CLOUDS] [--count=N] [--processors=PROCESSORS]"""
            # cms aws ping t --cloud=aws --count=3 --processors=3
            if arguments.NAMES:
                variables['vm'] = arguments.NAMES
            clouds, names = Arguments.get_cloud_and_names("ping", arguments, variables)

            params = {}

            count = arguments['--count']
            if count:
                params['count'] = int(count)

            processors = arguments['--processors']
            if processors:
                params['processors'] = int(processors[0])

            # gets public ips from database
            public_ips = []
            cursor = database.db['aws-node']
            for name in names:
                for node in cursor.find({'name':name}):
                    public_ips.append(node['public_ips'])
            public_ips = [y for x in public_ips for y in x]
            # print(public_ips)

            Shell3.pings(ips=public_ips, **params)

        # ok
        elif arguments.check:
            """vm check [NAMES] [--cloud=CLOUDS] [--username=USERNAME] [--processors=PROCESSORS]"""
            # cms aws check t --cloud=aws --username=ubuntu --processors=3
            if arguments.NAMES:
                variables['vm'] = arguments.NAMES
            clouds, names = Arguments.get_cloud_and_names("ping", arguments, variables)

            params = {}

            params['key'] = provider.p.spec["credentials"]['EC2_PRIVATE_KEY_FILE_PATH'] + provider.p.spec["credentials"]['EC2_PRIVATE_KEY_FILE_NAME']

            params['username'] = arguments['--username']  # or get from db

            processors = arguments['--processors']
            if processors:
                params['processors'] = int(processors[0])

            # gets public ips from database
            public_ips = []
            cursor = database.db['aws-node']
            for name in names:
                for node in cursor.find({'name':name}):
                    public_ips.append(node['public_ips'])
            public_ips = [y for x in public_ips for y in x]

            Shell3.checks(hosts=public_ips, **params)

        # ok
        elif arguments.status:
            """vm status [NAMES] [--cloud=CLOUDS]"""
            if arguments.NAMES:
                variables['vm'] = arguments.NAMES
            clouds, names = Arguments.get_cloud_and_names("status", arguments, variables)

            # gets status from database
            status = {}
            cursor = database.db['aws-node']
            for name in names:
                for node in cursor.find({'name':name}):
                    status[name] = node['state']

            pprint(status)

        #ok
        elif arguments.start:
            """vm start [NAMES] [--cloud=CLOUD] [--parallel] [--processors=PROCESSORS] [--dryrun]"""
            # cms aws start t --parallel --processors=3
            if arguments.NAMES:
                variables['vm'] = arguments.NAMES
            clouds, names = Arguments.get_cloud_and_names("start", arguments, variables)

            params = {}

            processors = arguments['--processors']

            if arguments['--parallel']:
                params['option'] = 'pool'
                if processors:
                    params['processors'] = int(processors[0])
            else:
                params['option'] = 'iter'

            if arguments['--dryrun']:
                print("start nodes {}\noption - {}\nprocessors - {}".format(names, params['option'], processors))
            else:
                pprint(provider.start(names, **params))

        #ok
        elif arguments.stop:
            """vm stop [NAMES] [--cloud=CLOUD] [--parallel] [--processors=PROCESSORS] [--dryrun]"""
            # cms aws stop t --parallel --processors=2
            if arguments.NAMES:
                variables['vm'] = arguments.NAMES
            clouds, names = Arguments.get_cloud_and_names("stop", arguments, variables)

            params = {}

            processors = arguments['--processors']

            if arguments['--parallel']:
                params['option'] = 'pool'
                if processors:
                    params['processors'] = int(processors[0])
            else:
                params['option'] = 'iter'

            if arguments['--dryrun']:
                print("stop nodes {}\noption - {}\nprocessors - {}".format(names, params['option'], processors))
            else:
                pprint(provider.stop(names, **params))

        #ok
        elif arguments.terminate:
            """vm terminate [NAMES] [--cloud=CLOUD] [--parallel] [--processors=PROCESSORS] [--dryrun]"""
            # cms aws terminate t --parallel --processors=2
            if arguments.NAMES:
                variables['vm'] = arguments.NAMES
            clouds, names = Arguments.get_cloud_and_names("terminate", arguments, variables)

            params = {}

            processors = arguments['--processors']

            if arguments['--parallel']:
                params['option'] = 'pool'
                if processors:
                    params['processors'] = int(processors[0])
            else:
                params['option'] = 'iter'

            if arguments['--dryrun']:
                print("terminate nodes {}\noption - {}\nprocessors - {}".format(names, params['option'], processors))
            else:
                pprint(provider.destroy(names, **params))

        #ok
        elif arguments.delete:
            """vm delete [NAMES] [--cloud=CLOUD] [--parallel] [--processors=PROCESSORS] [--dryrun]"""
            if arguments.NAMES:
                variables['vm'] = arguments.NAMES
            clouds, names = Arguments.get_cloud_and_names("terminate", arguments, variables)

            params = {}

            processors = arguments['--processors']

            if arguments['--parallel']:
                params['option'] = 'pool'
                if processors:
                    params['processors'] = int(processors[0])
            else:
                params['option'] = 'iter'

            if arguments['--dryrun']:
                print("delete nodes {}\noption - {}\nprocessors - {}".format(names, params['option'], processors))
            else:
                pprint(provider.destroy(names, **params))

        # TODO: username, secgroup
        elif arguments.boot:
            """
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
            """
            if arguments['--name']:
                # cms aws boot --name=t --cloud=aws --username=root --image=ami-08692d171e3cf02d6  --flavor=t2.micro --public --secgroup=group1 --key=aws_cert
                names = Parameter.expand(arguments['--name'])

            elif arguments['n']:
                # cms aws boot --n=2 --cloud=aws --username=root --image=ami-08692d171e3cf02d6  --flavor=t2.micro --public --secgroup=group1 --key=aws_cert
                n = int(arguments['n'])
                names = []
                for i in range(n):  # generate random names
                    m = hashlib.blake2b(digest_size=8)
                    m.update(str(datetime.utcnow()).encode('utf-8'))
                    names.append(m.hexdigest())

            else:
                print("please provide name or count to boot vm")

            params = {}
            # username = arguments['--username']
            params['image'] = arguments['--image']
            params['flavor'] = arguments['--flavor']

            public = arguments['--public']
            if public:
                params['ex_assign_public_ip'] = public

            secgroup = Parameter.expand(arguments['--secgroup'])
            if secgroup:
                params['ex_security_groups'] = secgroup

            key = arguments['--key']
            if key:
                params['ex_keyname'] = key

            if arguments['--dryrun']:
                print("""create nodes {}
image - {}
flavor - {}
assign public ip - {}
security groups - {}
keypair name - {}""".format(names, params['image'], params['flavor'], public, secgroup, key))
            else:
                pprint(provider.create(names=names, **params))

        # TODO: OUTPUT
        elif arguments.list:
            """
            vm list [NAMES]
                    [--cloud=CLOUDS]
                    [--output=OUTPUT]
                    [--refresh]
            """
            # cms aws t --cloud=aws --refresh
            if arguments.NAMES:
                variables['vm'] = arguments.NAMES
            clouds, names = Arguments.get_cloud_and_names("list", arguments, variables)

            if arguments['--refresh']:
                provider.list()

            if names:
                res = []
                cursor = database.db['aws-node']
                for name in names:
                    for node in cursor.find({'name':name}):
                        res.append(node)
            else:
                print("list all nodes in db, not implemented")

            pprint(res)

        # TODO
        elif arguments.info:
            """
            vm info [--cloud=CLOUD]
                    [--output=OUTPUT]
            """
            print("functionality not implemented")

        # TODO
        elif arguments.rename:
            """vm rename [OLDNAMES] [NEWNAMES] [--force] [--dryrun]"""
            print("functionality not implemented")

        # TODO
        elif arguments.ip and arguments.show:
            """vm ip show [NAMES]
                       [--group=GROUP]
                       [--cloud=CLOUD]
                       [--output=OUTPUT]
                       [--refresh]
            """
            clouds, names = Arguments.get_cloud_and_names("ip", arguments, variables)
            pprint(get_publicIPs(names))

        # TODO
        elif arguments.ip and arguments.assign:
            """
            vm ip assign [NAMES]
                      [--cloud=CLOUD]
            """
            clouds, names = Arguments.get_cloud_and_names("ip", arguments, variables)

            pprint(provider.assign_public_ip(names))

        # TODO
        elif arguments.ip and arguments.inventory:
            """vm ip inventory [NAMES]"""
            print("list ips that could be assigned")

        # TODO
        elif arguments.default:
            """vm default [options...]"""
            print("functionality not implemented")

        # ok
        elif arguments.run:
            """vm run [--name=VMNAMES] [--username=USERNAME] [--dryrun] [COMMAND ...]"""
            # cms aws run --name=t --username=ubuntu uname
            clouds, names = Arguments.get_cloud_and_names("run", arguments, variables)
            username = arguments['--username']
            command = arguments.COMMAND

            name_ips = {}
            cursor = database.db['aws-node']
            for name in names:
                for node in cursor.find({'name':name}):
                    name_ips[name] = node['public_ips']

            if arguments['--dryrun']:
                print("run command {} on vms: {}".format(command, names))
            else:
                provider.ssh(name_ips, username=username, command=command)

        # BUG in call command
        elif arguments.script:
            """vm script [--name=NAMES] [--username=USERNAME] [--dryrun] SCRIPT"""
            # cms aws script --name=t --username=ubuntu tests/test_aws.sh
            clouds, names = Arguments.get_cloud_and_names("run", arguments, variables)
            username = arguments['--username']
            script = arguments.SCRIPT

            name_ips = {}
            cursor = database.db['aws-node']
            for name in names:
                for node in cursor.find({'name':name}):
                    name_ips[name] = node['public_ips']

            if arguments['--dryrun']:
                print("run script {} on vms: {}".format(script, names))
            else:
                provider.ssh(name_ips, username=username, script=script)

        # TODO
        elif arguments.resize:
            """vm resize [NAMES] [--size=SIZE]"""
            pass

        # TODO
        # shh run command in implemented as aws run
        # not sure what to do with this command
        # since ssh into multiple vms at the same time doesn't make a lot of sense
        elif arguments.ssh:
            """
            vm ssh [NAMES] [--username=USER]
                     [--quiet]
                     [--ip=IP]
                     [--key=KEY]
                     [--command=COMMAND]
                     [--modify-knownhosts]
            """
            if arguments.NAMES:
                variables['vm'] = arguments.NAMES
            clouds, names = Arguments.get_cloud_and_names("list", arguments, variables)

            ips = {}
            cursor = database.db['aws-node']
            for name in names:
                for node in cursor.find({'name':name}):
                    pprint(node)

            username = arguments['--username']
            ip = arguments['--ip']

            params = {}

            quiet = arguments['--quiet']
            if quiet:
                params['quiet'] = quiet

            command = arguments['--command']
            if command:
                params['command'] = command

            modify_host = arguments['--modify-knownhosts']
            if modify_host:
                params['modify_host'] = modify_host

            provider.ssh(username=username, ip=ip, **params)

        # TODO
        elif arguments.wait:
            """vm wait [--cloud=CLOUD] [--interval=SECONDS]"""
            print("waits for the vm till its ready and one can login")

        # TODO
        elif arguments.username:
            """vm username USERNAME [NAMES] [--cloud=CLOUD]"""
            print("sets the username for the vm")

        elif arguments.debug:
            print(provider.p.cloudman.ex_list_floating_ips())
            # print(provider.loop(names, abs, option='iter',processors=3))

        return
