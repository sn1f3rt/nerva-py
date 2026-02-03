# Nerva (XNV) Python Library

[![Ruff](https://github.com/sn1f3rt/nerva-py/actions/workflows/ruff.yml/badge.svg)](https://github.com/sn1f3rt/nerva-py/actions/workflows/ruff.yml)
[![Build](https://github.com/sn1f3rt/nerva-py/actions/workflows/build.yml/badge.svg)](https://github.com/sn1f3rt/nerva-py/actions/workflows/build.yml)

## Table of Contents

- [About](#about)
- [Installation](#installation)
    * [Requirements](#requirements)
    * [Setup](#setup)
- [Documentation](#documentation)
- [Support](#support)
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

from nerva.daemon import Daemon


async def main():
    daemon = Daemon(
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

## License

[![License](https://img.shields.io/github/license/sn1f3rt/nerva-py)](LICENSE)

Copyright &copy; 2024-present [Sayan "sn1f3rt" Bhattacharyya](https://sn1f3rt.dev)
