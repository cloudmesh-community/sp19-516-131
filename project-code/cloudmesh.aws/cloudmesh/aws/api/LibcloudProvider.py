from cloudmesh.compute.libcloud.Provider import Provider as LibCloudProvider
import platform
from subprocess import run
from multiprocessing import Pool
import time
from datetime import datetime
from libcloud.compute.base import NodeSize
from libcloud.compute.base import NodeImage

from pprint import pprint

class SimpleNodeProperty():
    def __init__(self, id):
        self.id = id

class Provider(LibCloudProvider):
    def __init__(self, name='aws', configuration="~/.cloudmesh/cloudmesh4.yaml"):
        super().__init__(name=name, configuration=configuration)

    def create(self, name=None, image=None, size=None, location=None,  timeout=360, **kwargs):
        if image == None:
            image = self.spec["default"]['image']
        if size == None:
            size = self.spec["default"]['size']

        # create image and flavor with property .id
        # since in ibcloud.compute.providers create_node method, only the .id property of image and size are used
        # this bypasses having to load NodeSizes and NodeImages
        image_use = SimpleNodeProperty(id=image)
        flavor_use = SimpleNodeProperty(id=size)

        node = self.cloudman.create_node(name=name, image=image_use, size=flavor_use, **kwargs)

        return self.update_dict(node, kind='node')[0]

    def start(self, name=None):
        node = self.find(self.list(raw=True), name=name, raw=True)
        self.cloudman.ex_start_node(node)
        return self.update_dict(node, kind='node')[0]

    def stop(self, name=None):
        node = self.find(self.list(raw=True), name=name, raw=True)
        self.cloudman.ex_stop_node(node)
        return self.update_dict(node, kind='node')[0]

    def destroy(self, name=None):
        node = self.find(self.list(raw=True), name=name, raw=True)
        self.cloudman.destroy_node(node)
        return self.update_dict(node, kind='node')[0]

    def ssh(self, username=None, quiet=None, ip=None, key=None, command=None, modify_knownhosts=None):
        if key == None:
            key = self.spec['credentials']['EC2_PRIVATE_KEY_FILE_PATH'] + self.spec['credentials']['EC2_PRIVATE_KEY_FILE_NAME']
        location = username + '@' + ip
        ssh_command = ['ssh', '-i', key, location]
        run(ssh_command)



    # DEPRECATED
    # def get_public_ips(self, names=None):
    #     """
    #     get public ip addresses of a given list of nodes
    #
    #     :param names: list of node names
    #     :return: A list of ips of nodes
    #     """
    #     # below returns a dict representing name and ip of nodes
    #     # nodes = dict((x.name, x.public_ips) for x in self.list(names) if x.name in names)
    #     return [x.public_ips for x in self.list(names) if x.name in names]

    # DEPRECATED
    # def create(self, name=None, image=None, flavor=None, **kwargs):
    #     if image == None:
    #         image = self.spec['default']['image']
    #     if flavor == None:
    #         flavor = self.spec['default']['size']
    #     image = [i for i in self.images(raw=True) if i.id == image][0]
    #     flavor = [s for s in self.flavors(raw=True) if s.id == flavor][0]
    #
    #     return self.cloudman.create_node(name=name, image=image, size=flavor, **kwargs)

    # DEPRECATED
    # def start(self, names=None, wait=0):
    #     """
    #     Start a list of nodes with the given names
    #
    #     :param names: A list of node names
    #     :return:  A list of dict representing the nodes
    #     """
    #     return self.apply(self.cloudman.ex_start_node, names, wait=wait)

    # DEPRECATED
    # def stop(self, names=None, wait=0):
    #     """
    #     Stop a list of nodes with the given names
    #
    #     :param names: A list of node names
    #     :return:  A list of dict representing the nodes
    #     """
    #
    #     return self.apply(self.cloudman.ex_stop_node, names, wait=wait)

    # DEPRECATED
    # def destroy(self, names=None, wait=0):
    #     """
    #     Destroys the node
    #     :param names: the name of the node
    #     :return: the dict of the node
    #     """
    #     return self.apply(self.cloudman.destroy_node, names, wait=wait)

    # DEPRECATED
    # def apply(self, fname, names, wait=0):
    #     """
    #     apply a function to a given list of nodes
    #
    #     :param fname: Name of the function to be applied to the given nodes
    #     :param names: A list of node names
    #     :return:  A list of dict representing the nodes
    #     """
    #     if self.cloudman:
    #         nodes = self.find(elements=self.list(raw=True), names=names, raw=True)
    #         for node in nodes:
    #             fname(node)
    #         time.sleep(wait)
    #         return self.info(names)
    #     else:
    #         return None

    # DEPRECATED
    # def find(self, elements, names=None, raw=False):
    #     """
    #     finds a list of elements in elements with the specified names
    #     :param elements: The elements
    #     :param name: The names to be found
    #     :param: If raw is True, elements is a libcloud object.
    #             Otherwise elements is a dict
    #     :param raw: if raw is used the return from the driver is used and not a cleaned dict, not implemented
    #     :return: a list of elements with the given names
    #     """
    #     res = []
    #     for element in elements:
    #         name = (raw and element.name) or element["name"]
    #         if name in names:
    #             res.append(element)
    #     return res

    # DEPRECATED
    # def info(self, names=None):
    #     """
    #     Gets the information of a list of nodes with a given name
    #
    #     :param name: The names of the virtual machine
    #     :return: The dict representing the nodes including updated status
    #     """
    #     return self.find(self.list(), names=names)

    # DEPRECATED
    # def status(self, names=None):
    #     """
    #     Get status of nodes
    #     :param names: The names of the virtual machine
    #     :return: list of status
    #     """
    #     return list(map(lambda x: x['state'], self.info(names)))

    # DEPRECATED
    # def assign_public_ip(self, names=None):
    #     """
    #     Assign public IP to nodes
    #     :param names: The names of the virtual machine
    #     :return: The dict representing the nodes including updated status
    #     """
    #     return self.apply(self.cloudman.ex_assign_public_ip, names)

    # DEPRECATED
    # def images(self, raw=False, ex_image_ids=None):
    #     """
    #     Lists the images on the cloud
    #     :param raw: If raw is set to True the lib cloud object is returned
    #                 otherwise a dict is returened.
    #     :return: dict or libcloud object
    #     """
    #     if self.cloudman:
    #         entries = self.cloudman.list_images(ex_image_ids=ex_image_ids)
    #         if raw:
    #             return entries
    #         else:
    #             return self.update_dict(entries, kind="image")
    #
    #     return None

    # DEPRECATED
    # def get_publicIPs(self, names=None):
    #     """
    #     get public ip addresses of a given list of nodes
    #
    #     :param names: list of node names
    #     :return: A dict representing the public ips
    #     """
    #     return dict((x['name'], x['public_ips']) for x in self.info(names))
    #
    # def entry_to_dict(self, entry, c=0):
    #     # pprint(entry)
    #     for i in entry:
    #         rep = repr(entry[i])
    #         if rep[0]=='<' and 'object at' in rep:
    #             # pprint(entry[i])
    #             entry[i] = self.entry_to_dict(entry[i].__dict__, c+1)
    #     return entry

    # DEPRECATED
    # def update_dict(self, elements, kind=None):
    #     """
    #     Libcloud returns an object or list of objects With the dict method
    #     this object is converted to a dict. Typically this method is used internally.
    #     :param elements: the elements
    #     :param kind: Kind is image, flavor, or node
    #     :return:
    #     """
    #     if elements is None:
    #         return None
    #     elif type(elements) == list:
    #         _elements = elements
    #     else:
    #         _elements = [elements]
    #     d = []
    #     for element in _elements:
    #         entry = element.__dict__
    #         del entry["extra"] #Remove extra from google node
    #         entry["cm"] = {
    #             "kind": kind,
    #             "driver": self.cloudtype,
    #             "cloud": self.cloud
    #         }
    #         if kind == 'node':
    #             entry["cm"]["updated"] = str(datetime.utcnow())
    #             entry["cm"]["name"] = entry["name"]
    #
    #             if "created_at" in entry:
    #                 entry["cm"]["created"] = str(entry["created_at"])
    #                 # del entry["created_at"]
    #             else:
    #                 entry["cm"]["created"] = entry["modified"]
    #         elif kind == 'flavor':
    #             entry["cm"]["created"] = entry["updated"] = str(
    #                 datetime.utcnow())
    #             entry["cm"]["name"] = entry["name"]
    #             entry = self.entry_to_dict(entry)
    #             # entry["driver"] = entry["driver"].__dict__
    #             # entry["driver"]['connection'] = entry["driver"]['connection'].__dict__
    #
    #         elif kind == 'image':
    #             entry['cm']['created'] = str(datetime.utcnow())
    #             entry['cm']['updated'] = str(datetime.utcnow())
    #             entry["cm"]["name"] = entry["name"]
    #         elif kind == 'secgroup':
    #             if self.cloudtype == 'openstack':
    #                 entry["cm"]["name"] = entry["name"]
    #             else:
    #                 pass
    #         elif kind == 'key':
    #             if self.cloudtype == 'openstack':
    #                 entry["cm"]["name"] = entry["name"]
    #             else:
    #                 pass
    #
    #         if "_uuid" in entry:
    #             del entry["_uuid"]
    #         # if "driver" in entry:
    #         #     del entry["driver"]
    #         pprint(entry)
    #
    #         d.append(entry)
    #         break
    #     return d

    # DEPRECATED
    # def status(self, names=None):
    #     return dict((x.name, x.state) for x in self.list(names) if x.name in names)
