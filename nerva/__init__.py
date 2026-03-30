from typing import Literal, NamedTuple

from . import (
    utils as utils,
    daemon as daemon,
    wallet_rpc as wallet_rpc,
)
from .daemon import (
    DaemonRPC as DaemonRPC,
    DaemonHTTP as DaemonHTTP,
)
from .wallet_rpc import WalletRPC as WalletRPC


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal[
        "alpha", "beta", "release-candidate", "post", "dev", "final"
    ]
    serial: int

    def __str__(self) -> str:
        v = f"{self.major}.{self.minor}.{self.micro}"

        if self.releaselevel != "final":
            if self.releaselevel == "alpha":
                v += "a"
            elif self.releaselevel == "beta":
                v += "b"
            elif self.releaselevel == "release-candidate":
                v += "rc"
            elif self.releaselevel == "post":
                v += "post"
            elif self.releaselevel == "dev":
                v += "dev"

            v += str(self.serial)

        return v


version_info: VersionInfo = VersionInfo(
    major=1, minor=1, micro=1, releaselevel="final", serial=0
)

__version__ = str(version_info)

del NamedTuple, Literal, VersionInfo
