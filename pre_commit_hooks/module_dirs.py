#!/usr/bin/env python
from argparse import ArgumentParser
from json import dumps
from os import walk
from pathlib import Path


def is_valid_module(module_path: Path) -> bool:
    # check for minimal files
    module_files = [
        "README.md",
        "main.tf",
        "outputs.tf",
        "versions.tf",
    ]

    file_check = all((module_path / file).exists() for file in module_files)

    return file_check


def list_module_paths(root: Path) -> list[Path]:
    modules_paths: list[Path] = []

    for base, _, files in walk(root):
        base_path = Path(base)

        # check if we have versions.tf
        if "versions.tf" in files:
            modules_paths.append(base_path)

    return sorted(modules_paths, key=lambda p: str(p))


def main():
    parser = ArgumentParser(
        description="Find all the Modules and send a JSON formatted list to StdOut.",
    )
    parser.add_argument(
        "root",
        type=str,
        default=".",
        help="Root directory to start searching from",
    )
    args = parser.parse_args()

    root = Path(args.root)

    module_paths = [str(mp) for mp in list_module_paths(root)]
    print(dumps(module_paths, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
