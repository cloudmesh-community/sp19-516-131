from cloudmesh.aws.api.LibcloudProvider import Provider as LibCloudProvider
from cloudmesh.compute.vm.Provider import Provider as VmProvider

class Provider(VmProvider):

    def __init__(self, name='aws', configuration="~/.cloudmesh/.cloudmesh4.yaml"):
        super().__init__(name=name, configuration=configuration)
        self.p = LibCloudProvider(name=name, configuration=configuration)

    # deprecated
    # def get_public_ips(self, names=None):
    #     return self.p.get_public_ips(names)

    # deprecated
    # def status(self, names=None):
    #     return self.p.status(names)

    def f(self):
        return self.p.cloudman.list_sizes()

    def stop(self, names=None, **kwargs):
        return self.loop(names, self.p.stop, **kwargs)

    def start(self, names=None, **kwargs):
        return self.loop(names, self.p.start, **kwargs)

    def destroy(self, names=None, **kwargs):
        return self.loop(names, self.p.destroy, **kwargs)
