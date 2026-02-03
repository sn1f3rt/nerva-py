from typing import Literal, NamedTuple

from . import (
    utils as utils,
    daemon as daemon,
    wallet as wallet,
)


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal[
        "alpha", "beta", "release-candidate", "post", "dev", "final"
    ]
    serial: int

    def __str__(self) -> str:
        v = f"{version_info.major}.{version_info.minor}.{version_info.micro}"

        if version_info.releaselevel != "final":
            if version_info.releaselevel == "alpha":
                v += "a"
            elif version_info.releaselevel == "beta":
                v += "b"
            elif version_info.releaselevel == "release-candidate":
                v += "rc"
            elif version_info.releaselevel == "post":
                v += "post"
            elif version_info.releaselevel == "dev":
                v += "dev"

            v += str(version_info.serial)

        return v


version_info: VersionInfo = VersionInfo(
    major=1, minor=1, micro=1, releaselevel="final", serial=0
)

__version__ = str(version_info)

del NamedTuple, Literal, VersionInfo
