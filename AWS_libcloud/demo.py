from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from cloudmesh.management.configuration.config import Config
import sys

class Demo():
    def __init__(self):
        print("start")
        cloud = Config().__dict__['data']['cloudmesh']['cloud']['aws']

        credentials = cloud['credentials']
        self.ACCESS_ID = credentials['EC2_ACCESS_ID']
        self.SECRET_KEY = credentials['EC2_SECRET_KEY']
        self.REGION = credentials['EC2_REGION']

        default = cloud['default']
        self.IMAGE_ID = default['image']
        self.SIZE_ID = default['size']

        print('this is gonna take a while')
        images = self.driver.list_images()
        sizes = self.driver.list_sizes()

        cls = get_driver(Provider.EC2)
        self.driver = cls(self.ACCESS_ID, self.SECRET_KEY, region = self.REGION)

    def sizes(self):
        return self.driver.list_sizes()

    def images(self):
        return self.driver.list_images()

    def create(self, name, image_id, size_id):
        image_id = self.IMAGE_ID
        size_id = self.SIZE_ID

        image = [i for i in images if i.id == image_id][0]
        size = [s for s in sizes if s.id == size_id][0]

        return self.driver.create_node(name=name, image=image, size=size)

    def list(self):
        return self.driver.list_nodes()

    def node_operation(self, name, operator):
        for node in self.list():
            if node.name == name:
                self.driver.operator(node=node)

    def start(self, name):
        self.node_operation(name, ex_start_node)

    def stop(self, name):
        self.node_operation(name, ex_stop_node)

    def reboot(self, name):
        self.node_operation(name, reboot_node)

    def destroy(self, name):
        self.node_operation(name, destroy_node)
