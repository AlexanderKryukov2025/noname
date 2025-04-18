import os
import pytest

from data.const.sys import *


class GetBrowserVersion:

    def __init__(self):
        self.browser_binary = pytest.CFG[BROWSER_BINARY]

    def from_windows(self):
        command_cmd = f'&{{(Get-Item "{self.browser_binary}").VersionInfo.ProductVersion}}'
        command_powershell = f'powershell -command "{command_cmd}"'
        version = os.popen(command_powershell).read()

        return version.strip("\n")
