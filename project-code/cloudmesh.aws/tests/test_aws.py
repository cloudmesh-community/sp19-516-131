###############################################################
# pytest -v --capture=no tests/test_aws.py
# pytest -v  tests/test_aws.py
# pytest -v --capture=no -v --nocapture tests/test_aws.py:Test_aws.<METHIDNAME>
###############################################################
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.util import HEADING
from pprint import pprint
import textwrap
import oyaml as yaml
import munch
import re

from cloudmesh.common.Shell import Shell
from cloudmesh.DEBUG import VERBOSE
import pytest

@pytest.mark.incremental
class TestConfig:
    """
        PROCESS NOT FULLY IMPLEMENTED
    """

    def test_01_boot(self):
        HEADING()

        result = Shell.execute("cms aws boot --name=t01 --image=ami-0bbe6b35405ecebdb --flavor=t2.micro", shell=True)

        VERBOSE(result)

        assert "name=t01" in result

    def test_02_boot(self):
        HEADING()

        result = Shell.execute("cms aws boot --name=t02 --image=ami-0bbe6b35405ecebdb --flavor=t2.micro", shell=True)

        VERBOSE(result)

        assert "name=t02" in result

    def test_03_boot(self):
        HEADING()

        result = Shell.execute("cms aws boot --name=t03 --image=ami-0bbe6b35405ecebdb --flavor=t2.micro", shell=True)

        VERBOSE(result)

        assert "name=t03" in result

    def test_01_wait(self):
        HEADING()

        result = Shell.execute("cms aws wait --interval=60", shell=True)

    def test_01_ping(self):
        HEADING()

        result = Shell.execute("cms aws ping t1 --count=4 --processors=5", shell=True)

        VERBOSE(result)

        assert "ping" in result
        assert "success" in result
        assert "4 packets transmitted" in result

    def test_01_start(self):
        HEADING()

        result = Shell.execute("cms aws start t0", shell=True)

        VERBOSE(result)

        assert "t0" in result
        assert "running" in result

    def test_01_stop(self):
        HEADING()

        result = Shell.execute("cms aws stop t1", shell=True)

        VERBOSE(result)

        assert "t1" in result
        assert "stopped" in result

    def test_01_terminate(self):
        HEADING()

        result = Shell.execute("cms aws terminate t2", shell=True)

        VERBOSE(result)

        assert "t2" in result
        assert "terminated" in result

    def test_01_status(self):
        HEADING()

        result = Shell.execute("cms aws status t0", shell=True)

        VERBOSE(result)

        assert "running" in result

    def test_02_status(self):
        HEADING()

        result = Shell.execute("cms aws status t1", shell=True)

        VERBOSE(result)

        assert "stopped" in result

    def test_02_status(self):
        HEADING()

        result = Shell.execute("cms aws status t3", shell=True)

        VERBOSE(result)

        assert "terminated" in result

    def test_01_list(self):
        HEADING()

        result = Shell.execute("cms aws list t0", shell=True)

        VERBOSE(result)

        assert "'name': 't0'" in result
        assert "'id': 'i-032d5c07fcfaf5b8b'" in result
