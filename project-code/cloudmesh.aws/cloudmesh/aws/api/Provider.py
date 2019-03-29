from cloudmesh.compute.libcloud.Provider import Provider as LibCloudProvider
import platform
from subprocess import run
from multiprocessing import Pool

from pprint import pprint

class Provider(LibCloudProvider):
    def __init__(self, name='aws', configuration="~/.cloudmesh/cloudmesh4.yaml"):
        super().__init__(name=name, configuration=configuration)

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

    def get_publicIPs(self, names=None):
        """
        get public ip addresses of a given list of nodes

        :param names: list of node names
        :return: A dict representing the public ips
        """
        return dict((x['name'], x['public_ips']) for x in self.info(names))

    def __partial_ping__(self, ip, timeout=None):
        """
        ping a vm from given ip address

        :param ip: str of ip address
        :param timeout: given in seconds. if timeout expires, the process is killed
        :return: a str representing the ping result
        """
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', ip]
        ret_code = run(command, capture_output=False).returncode
        # return ip, ret_code
        if ret_code == 0:
            return "\n\x1b[6;30;42m Ping " + ip + " Successful \x1b[0m"
        else:
            return "\n\x1b[0;30;41m Ping" + ip + " Failure. Return code:" + str(ret_code) + " \x1b[0m"

    def ping(self, public_ips=None, timeout=None):
        """
        ping a list of given ip addresses

        :param public_ips: a list of ip addresses
        :param timeout: given in seconds. if timeout expires, a process is killed
        :return: none
        """
        ###                                    ###
        ### need to check security group first ###
        ###                                    ###
        with Pool(len(public_ips)) as p:
            res = p.map(self.__partial_ping__, public_ips)
        list(map(print, res))

# p = Provider()
# names = ['t1', 't2']
# ips = [['54.212.216.196'], ['54.245.42.58']]
# # pprint(p.info(names))
# # pprint(p.ping(['t1', 't2']))
# p.ping(ips)
