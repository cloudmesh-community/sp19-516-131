from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from cloudmesh.management.configuration.config import Config
import sys

class Demo():
    def __init__(self):
        cloud = Config().__dict__['data']['cloudmesh']['cloud']['aws']

        credentials = cloud['credentials']
        ACCESS_ID = credentials['EC2_ACCESS_ID']
        SECRET_KEY = credentials['EC2_SECRET_KEY']
        REGION = credentials['EC2_REGION']

        default = cloud['default']
        IMAGE_ID = default['image']
        SIZE_ID = default['size']

        cls = get_driver(Provider.EC2)
        driver = cls(ACCESS_ID, SECRET_KEY, region = REGION)

    def sizes(self):
        return driver.list_sizes()

    def images(self):
        return driver.list_images()

    def create(self,name, image_id = IMAGE_ID, size_id = SIZE_ID):
        images = driver.list_images()
        sizes = driver.list_sizes()

        image = [i for i in images if i.id == image_id][0]
        size = [s for s in sizes if s.id == size_id][0]

        return driver.create_node(name=name, image=image, size=size)

    def list(self):
        return driver.list_nodes()

    def node_operation(self, name, operator):
        for node in self.list():
            if node.name == name:
                driver.operator(node=node)

    def start(self, name):
        self.node_operation(name, ex_start_node)

    def stop(self, name):
        self.node_operation(name, ex_stop_node)

    def reboot(self, name):
        self.node_operation(name, reboot_node)

    def destroy(self, name):
        self.node_operation(name, destroy_node)
