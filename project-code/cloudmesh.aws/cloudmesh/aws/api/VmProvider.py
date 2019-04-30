from cloudmesh.aws.api.LibcloudProvider import Provider as LibCloudProvider
from cloudmesh.compute.vm.Provider import Provider as VmProvider
import subprocess
class Provider(VmProvider):

    def __init__(self, name='aws', configuration="~/.cloudmesh/.cloudmesh4.yaml"):
        super().__init__(name=name, configuration=configuration)
        self.p = LibCloudProvider(name=name, configuration=configuration)

    def stop(self, names=None, **kwargs):
        return self.loop(names, self.p.stop, **kwargs)

    def start(self, names=None, **kwargs):
        return self.loop(names, self.p.start, **kwargs)

    def destroy(self, names=None, **kwargs):
        return self.loop(names, self.p.destroy, **kwargs)

    def ssh(self, name_ips, **kwargs):
        for name, ips in name_ips.items():
            self.p.ssh(name=name, ips=ips, **kwargs)
