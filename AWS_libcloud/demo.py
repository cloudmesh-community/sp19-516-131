from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from cloudmesh.management.configuration.config import Config
import sys

config = Config()
ACCESS_ID = config.__dict__['data']['cloudmesh']['cloud']['aws']['credentials']['EC2_ACCESS_ID']
SECRET_KEY = config.__dict__['data']['cloudmesh']['cloud']['aws']['credentials']['EC2_SECRET_KEY']

IMAGE_ID = config.__dict__['data']['cloudmesh']['cloud']['aws']['default']['image']
SIZE_ID = config.__dict__['data']['cloudmesh']['cloud']['aws']['default']['size']

cls = get_driver(Provider.EC2)
driver = cls(ACCESS_ID, SECRET_KEY, region = config.__dict__['data']['cloudmesh']['cloud']['aws']['credentials']['EC2_REGION'])

# arg = sys.argv[1]
#
# if arg == 'size':
#     print_sizes()
# elif arg == 'image':
#     print_images()

def list_sizes():
    return driver.list_sizes()

def list_images():
    return driver.list_images()

def create_node(name, image_id = IMAGE_ID, size_id = SIZE_ID):
    images = driver.list_images()
    sizes = driver.list_sizes()

    image = [i for i in images if i.id == image_id][0]
    size = [s for s in sizes if s.id == size_id][0]

    return driver.create_node(name=name, image=image, size=size)

def list_nodes():
    return driver.list_nodes()

def stop_node(node_id):
    # stop node by name
    return driver.ex_stop_node(node=node)

def destroy_node(node):
    return driver.destroy_node(node=node)
