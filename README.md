# Nerva (XNV) Python Library

[![Lint](https://github.com/sn1f3rt/nerva-py/actions/workflows/lint.yml/badge.svg)](https://github.com/sn1f3rt/nerva-py/actions/workflows/lint.yml)
[![Type Check](https://github.com/sn1f3rt/nerva-py/actions/workflows/typecheck.yml/badge.svg)](https://github.com/sn1f3rt/nerva-py/actions/workflows/typecheck.yml)
[![Build](https://github.com/sn1f3rt/nerva-py/actions/workflows/build.yml/badge.svg)](https://github.com/sn1f3rt/nerva-py/actions/workflows/build.yml)

## Table of Contents

- [About](#about)
- [Installation](#installation)
    * [Requirements](#requirements)
    * [Setup](#setup)
- [Documentation](#documentation)
- [Support](#support)
- [Funding](#funding)
- [License](#license)

## About

Python bindings for the JSON RPC interface of the [Nerva (XNV)](https://nerva.one/) cryptocurrency.

## Installation

### Requirements

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) (for development only)

### Setup

To install current latest release you can use following command:
```sh
pip install nerva-py
```

To install the latest development version you can use following command:
```sh
uv add git+https://github.com/Sn1F3rt/nerva-py.git --branch main
```

## Documentation

Developers please refer to the docstrings in the code for more information. Full API reference will be available soon.

Here is a simple example to get you started:

```python
import asyncio

from nerva.daemon import DaemonRPC


async def main():
    daemon = DaemonRPC(
        host="localhost",
        port=17566,
        ssl=False,
        username="rpcuser", # omit if daemon was not started with the rpc-login flag
        password="rpcpassword" # omit if daemon was not started with the rpc-login flag
    )

    print(await daemon.get_info())


asyncio.run(main())
```

## Support

- [Issues](https://github.com/sn1f3rt/nerva-py/issues)
- [Discord](https://discord.gg/ufysfvcFwe) - `Development > #nerva-py`

## Funding

The library itself is free to use but its development is not. If you find it useful, please consider donating:

- **Nerva (XNV):** `NV1PqtQwRik7FFeAJ5n7iKbHtve3nkeM99x3Q31wjBAm7twvRv6NYkbbP7vSG3n8N3fsUh2gpfZG2PRi4gYhxL4h2r2SnhUoX`
- **Monero (XMR):** `48SSQzEcvQPK7H69vUvwReFT7tCDESdRhPFGubTgJ8WeXUUPQRWjY8oZk3wHfLhsUnChJ1BYyYfoLKQh8epYsupAAWCnDKh`
- **Bitcoin (BTC):** `bc1qzg4jjtxq6cg22pmlaesyva64nrjzcaqud968vf`
- **Ethereum (ETH):** `0x97173e82df1d9Cc76946241D63A9f9231Dea1566`

or if you prefer, you can support using fiat currency:

- **GitHub Sponsors:** [Sponsor](https://github.com/sponsors/Sn1F3rt)
- **Patreon:** [Support](https://www.patreon.com/sn1f3rt)
- **Buy Me A Coffee:** [Donate](https://www.buymeacoffee.com/sn1f3rt)

## License

[![License](https://img.shields.io/github/license/sn1f3rt/nerva-py)](LICENSE)

Copyright &copy; 2024-present [Sayan "sn1f3rt" Bhattacharyya](https://sn1f3rt.dev)
