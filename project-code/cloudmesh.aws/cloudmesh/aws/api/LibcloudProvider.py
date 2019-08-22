from cloudmesh.compute.libcloud.Provider import Provider as LibCloudProvider
from cloudmesh.mongo.CmDatabase import CmDatabase
import subprocess
from libcloud.compute.base import NodeSize
from libcloud.compute.base import NodeImage

from pprint import pprint

class Provider(LibCloudProvider):
    def __init__(self, name='aws', configuration="~/.cloudmesh/cloudmesh.yaml"):
        super().__init__(name=name, configuration=configuration)

    # moved to cloudmesh-cloud
    # def create(self, name=None, image=None, size=None, location=None,  timeout=360, **kwargs):
    #     if image == None:
    #         image = self.spec["default"]['flavor']
    #     if size == None:
    #         size = self.spec["default"]['size']
    #
    #     database = CmDatabase()
    #     image_dict = database.find(collection='{}-image'.format('aws'), name=image)[0]
    #     flavor_dict = database.find(collection='aws-flavor', name=size)[0]
    #
    #     image_use = NodeImage(id=image_dict['id'],
    #                         name=image_dict['name'],
    #                         driver=self.driver)
    #     flavor_use = NodeSize(id=flavor_dict['id'],
    #                         name=flavor_dict['name'],
    #                         ram=flavor_dict['ram'],
    #                         disk=flavor_dict['disk'],
    #                         bandwidth=flavor_dict['bandwidth'],
    #                         price=flavor_dict['price'],
    #                         driver=self.driver)
    #
    #     node = self.cloudman.create_node(name=name, image=image_use, size=flavor_use, **kwargs)
    #
    #     return self.update_dict(node, kind='node')[0]
    #
    # def ssh(self, name, ips, username=None, key=None, quiet=None, command=None, script=None, modify_knownhosts=None):
    #     if key == None:
    #         key = self.spec['credentials']['EC2_PRIVATE_KEY_FILE_PATH'] + self.spec['credentials']['EC2_PRIVATE_KEY_FILE_NAME']
    #     for ip in ips:
    #         location = username + '@' + ip
    #         if command != None:
    #             ssh_command = ['ssh', '-i', key, location, command]
    #             subprocess.run(ssh_command)
    #         elif script != None:
    #             # BUG, doesn't work#
    #             ssh_command = ['ssh', '-i', key, location, 'bash', '-s', '<', script]
    #             subprocess.call(ssh_command, shell=True)
    #
    # def start(self, name=None):
    #     """
    #     Start a node
    #
    #     :param name: node name
    #     :return: A dict representing the node
    #     """
    #     node = self.find(self.list(raw=True), name=name, raw=True)
    #     self.cloudman.ex_start_node(node)
    #     return self.update_dict(node, kind='node')[0]
    #
    # def stop(self, name=None):
    #     """
    #     Stop a node
    #
    #     :param name: node name
    #     :return: A dict representing the node
    #     """
    #     node = self.find(self.list(raw=True), name=name, raw=True)
    #     self.cloudman.ex_stop_node(node)
    #     return self.update_dict(node, kind='node')[0]
    #
    # def destroy(self, name=None):
    #     """
    #     Destroy a node
    #
    #     :param name: node name
    #     :return: A dict representing the node
    #     """
    #     node = self.find(self.list(raw=True), name=name, raw=True)
    #     self.cloudman.destroy_node(node)
    #     return self.update_dict(node, kind='node')[0]
