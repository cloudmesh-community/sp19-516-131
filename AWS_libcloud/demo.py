from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from cloudmesh.management.configuration.config import Config
from pprint import pprint
import sys

config = Config()
ACCESS_ID = config.__dict__['data']['cloudmesh']['cloud']['aws']['credentials']['EC2_ACCESS_ID']
SECRET_KEY = config.__dict__['data']['cloudmesh']['cloud']['aws']['credentials']['EC2_SECRET_KEY']

IMAGE_ID = config.__dict__['data']['cloudmesh']['cloud']['aws']['default']['image']
SIZE_ID = config.__dict__['data']['cloudmesh']['cloud']['aws']['default']['size']

cls = get_driver(Provider.EC2)
driver = cls(ACCESS_ID, SECRET_KEY, region = config.__dict__['data']['cloudmesh']['cloud']['aws']['credentials']['EC2_REGION'])

def print_sizes():
    sizes = driver.list_sizes()
    pprint(sizes)

def print_images():
    images = driver.list_images()
    pprint(images)

arg = sys.argv[1]

if arg == 'size':
    print_sizes()
elif arg == 'image':
    print_images()
