import sys
import argparse
import platform

import httpx

import nerva


def show_version() -> None:
    entries = []

    v = sys.version_info
    entries.append(
        f"- Python v{v.major}.{v.minor}.{v.micro}"
        + (f"-{v.releaselevel}{v.serial}" if v.releaselevel != "final" else "")
    )

    entries.append(f"- nerva-py v{nerva.__version__}")

    entries.append(f"- httpx v{httpx.__version__}")

    uname = platform.uname()
    entries.append(f"- System Info: {uname.system} {uname.release} {uname.version}")

    print("\n".join(entries))


def core(*, parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.version:
        show_version()
    else:
        parser.print_help()


def parse_args() -> tuple[argparse.ArgumentParser, argparse.Namespace]:
    parser = argparse.ArgumentParser(
        prog="pyxnv", description="Tools for helping with the library"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Shows the library version"
    )
    parser.set_defaults(func=core)

    return parser, parser.parse_args()


def main() -> None:
    parser, args = parse_args()
    args.func(parser=parser, args=args)


if __name__ == "__main__":
    main()
