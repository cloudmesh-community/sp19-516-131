###############################################################
# pytest -v --capture=no tests/test_aws_fail.py
# pytest -v  tests/test_aws_fail.py
# pytest -v --capture=no -v --nocapture tests/test_aws_fail.py:Test_aws.<METHIDNAME>
###############################################################
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.util import HEADING
from pprint import pprint
import textwrap
import oyaml as yaml
import munch
import re
import time

from cloudmesh.common.Shell import Shell
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.mongo.CmDatabase import CmDatabase
import pytest
from cloudmesh.common.StopWatch import StopWatch

@pytest.mark.incremental
class Test_aws:

    def setup(self):
        conf = Config("~/.cloudmesh/cloudmesh4.yaml")["cloudmesh"]
        cred = conf["cloud"]['aws']["credentials"]
        self.key = (cred['EC2_PRIVATE_KEY_FILE_NAME']).split('.')[0]

    def test_04_stop(self):
        HEADING("this test will fail, press Ctrl-C to skip")

        StopWatch.start("cms aws stop")
        result = Shell.execute("cms aws stop test_boot_02 --parallel --processors=3", shell=True)
        StopWatch.stop("cms aws stop")

        VERBOSE(result)

        assert "'name': 'test_boot_02'" in result

    def test_04_start(self):
        HEADING("this test will fail, press Ctrl-C to skip")

        StopWatch.start("cms aws start")
        result = Shell.execute("cms aws start test_boot_02 --parallel --processors=3", shell=True)
        StopWatch.stop("cms aws start")

        VERBOSE(result)

        assert "'name': 'test_boot_02'" in result

    def test_04_terminate(self):
        HEADING("this test will fail, press Ctrl-C to skip")

        StopWatch.start("cms aws terminate")
        result = Shell.execute("cms aws terminate test_boot_01 --parallel --processors=3", shell=True)
        StopWatch.stop("cms aws terminate")

        VERBOSE(result)

        assert "'name': 'test_boot_01'" in result

    def test_04_delete(self):
        HEADING("this test will fail, press Ctrl-C to skip")

        StopWatch.start("cms aws delete")
        result = Shell.execute("cms aws delete test_boot_02 --parallel --processors=3", shell=True)
        StopWatch.stop("cms aws delete")

        VERBOSE(result)

        assert "'name': 'test_boot_02'" in result
