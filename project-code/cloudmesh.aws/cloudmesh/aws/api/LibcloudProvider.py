from cloudmesh.compute.libcloud.Provider import Provider as LibCloudProvider
import platform
import subprocess
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

    def ssh(self, name, ips, username=None, key=None, quiet=None, command=None, script=None, modify_knownhosts=None):
        if key == None:
            key = self.spec['credentials']['EC2_PRIVATE_KEY_FILE_PATH'] + self.spec['credentials']['EC2_PRIVATE_KEY_FILE_NAME']
        for ip in ips:
            location = username + '@' + ip
            if command != None:
                ssh_command = ['ssh', '-i', key, location, command]
                subprocess.run(ssh_command)
            elif script != None:
                # BUG, doesn't work#
                ssh_command = ['ssh', '-i', key, location, 'bash', '-s', '<', script]
                subprocess.call(ssh_command, shell=True)
