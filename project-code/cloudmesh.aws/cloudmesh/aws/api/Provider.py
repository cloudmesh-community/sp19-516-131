from cloudmesh.compute.libcloud.Provider import Provider as LibCloudProvider
import platform
from subprocess import run
from multiprocessing import Pool

from pprint import pprint

class Provider(LibCloudProvider):
    def __init__(self, name='aws', configuration="~/.cloudmesh/cloudmesh4.yaml"):
        super().__init__(name=name, configuration=configuration)

    def apply(self, fname, names):
        """
        apply a function to a given list of nodes

        :param fname: Name of the function to be applied to the given nodes
        :param names: A list of node names
        :return:  A list of dict representing the nodes
        """
        if self.cloudman:
            nodes = self.find(elements=self.list(raw=True), names=names, raw=True)
            map(fname, nodes)
            return self.info(names)
        else:
            return None

    def find(self, elements, names=None, raw=False):
        """
        finds a list of elements in elements with the specified names
        :param elements: The elements
        :param name: The names to be found
        :param: If raw is True, elements is a libcloud object.
                Otherwise elements is a dict
        :param raw: if raw is used the return from the driver is used and not a cleaned dict, not implemented
        :return: a list of elements with the given names
        """
        res = []
        for element in elements:
            if (raw and element.name) or element["name"] in names:
                res.append(element)
        return res

    def info(self, names=None):
        """
        Gets the information of a list of nodes with a given name

        :param name: The names of the virtual machine
        :return: The dict representing the nodes including updated status
        """
        return self.find(self.list(), names=names)

    def status(self, names=None):
        """
        Get status of nodes
        :param names: The names of the virtual machine
        :return: list of status
        """
        return list(map(lambda x: x['state'], self.info(names)))

    def assign_public_ip(self, names=None):
        """
        Assign public IP to nodes
        :param names: The names of the virtual machine
        :return: The dict representing the nodes including updated status
        """
        return self.apply(self.cloudman.ex_assign_public_ip, names)

    def images(self, raw=False, ex_image_ids=None):
        """
        Lists the images on the cloud
        :param raw: If raw is set to True the lib cloud object is returned
                    otherwise a dict is returened.
        :return: dict or libcloud object
        """
        if self.cloudman:
            entries = self.cloudman.list_images(ex_image_ids=ex_image_ids)
            if raw:
                return entries
            else:
                return self.update_dict(entries, kind="image")

        return None

    def get_publicIPs(self, names=None):
        """
        get public ip addresses of a given list of nodes

        :param names: list of node names
        :return: A dict representing the public ips
        """
        return dict((x['name'], x['public_ips']) for x in self.info(names))

    def __partial_ping__(self, args):
        """
        ping a vm from given ip address

        :param args: tuple of (ip address, count)
        :return: a tuple representing the ping result
        """
        ip = args[0]
        count = args[1]
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, str(count), args[0]]
        ret_code = run(command, capture_output=False).returncode
        return ip, ret_code

    def ping(self, public_ips=None, count=3, processors=10):
        """
        ping a list of given ip addresses

        :param public_ips: a list of ip addresses
        :param timeout: given in seconds. if timeout expires, a process is killed
        :return: A list of tuples representing the ping result
        """
        args = [(ip, count) for ip in public_ips]

        with Pool(processors) as p:
            res = p.map(self.__partial_ping__, args)
        return res

    def get_dns_names(self, names=None):
        """
        get dns names given node names

                NOT YET IMPLEMENTED

        :param names: A list of node names
        :return: A dict representing the dns names
        """
        return dict((x['name'], x['extra']['dns_name']) for x in self.info(names))

    def ssh(self, username=None, quiet=None, ip=None, key=None, command=None, modify_knownhosts=None):
        if key == None:
            key = self.spec['credentials']['EC2_PRIVATE_KEY_FILE_PATH'] + self.spec['credentials']['EC2_PRIVATE_KEY_FILE_NAME']
        location = username + '@' + ip
        ssh_command = ['ssh', '-i', key, location]
        run(ssh_command)

    def __partial_check__(self, location, timeout=None):
        """
        check a vm from given keypair and vm location

                IMPLEMENTION IN PROGRESS

        :param keypair: path name to keypair
        :param location: location of instance, in the form of username@public_dns_name
        :param timeout: given in seconds. if timeout expires, the process is killed
        :return: a str representing the check result
        """
        return ""
        keypair = self.cred['EC2_PRIVATE_KEY_FILE_PATH'] + self.cred['EC2_PRIVATE_KEY_FILE_NAME']
        command = ['ssh', '-i', keypair, location]
        ret_code = run(command, capture_output=False).returncode
        run(['exit'])
        return location, ret_code

    def check(self, names=None, keypair=None, timeout=None):
        """
        check a list of given node names and keypair

                IMPLEMENTION IN PROGRESS

        :param names: a list of node names
        :param keypair: path name to keypair
        :param timeout: given in seconds. if timeout expires, a process is killed
        :return: A list of tuples representing the check result
        """
        return ""
        user_names = list(self.get_ssh_usernames(names).values())
        dns_names = list(self.get_dns_names(names).values())

        u = user_names[0]
        n = dns_names[0]
        location = u+'@'+n
        command = ['ssh', '-i', keypair, location]
        run(command)
        ### need to figure out how to exit vm once sshed.
        ret_code = run(['ls', '-a'], capture_output=False).returncode
        run(['exit'])
        return ret_code
        #
        # with Pool(len(names)) as p:
        #     res = p.map(lambda u,d : self.__partial_check__(keypair, u+'@'+d ,timeout=timeout), user_names, dns_names)
        # return res
