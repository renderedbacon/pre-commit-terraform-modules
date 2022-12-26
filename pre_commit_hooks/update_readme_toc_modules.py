#!/usr/bin/env python
from argparse import ArgumentParser
from pathlib import Path

from .module_dirs import is_valid_module
from .module_dirs import list_module_paths


def generate_modules_toc_md(root: Path, all_module_paths: list[Path]):
    modules_toc_md = []
    stack_paths = sorted([m for m in all_module_paths if "stacks" in m.parts])
    module_paths = sorted([m for m in all_module_paths if "modules" in m.parts])

    modules_toc_md.append("## Stacks")

    # render stacks
    for stack in stack_paths:
        modules_toc_md.append(f"* [{stack.name}]({str(stack / 'README.md').replace(str(root), '.')})")

    modules_toc_md.append("## Modules")

    # render modules
    for module in module_paths:

        # for each instance of modules in the path in crease the indent
        depth = len([m for m in module.parts if m == "modules"]) - 1
        indent = 1 if depth == 0 else (depth * 4) + 1
        modules_toc_md.append(f"{'*':>{indent}} [{module.name}]({str(module / 'README.md').replace(str(root), '.')})")

    return "\n\n".join(modules_toc_md)


def update_root_readme(root: Path, readme: str, module_toc_md: str, start_marker: str, end_marker: str):
    module_toc_md_with_markers = f"{start_marker}\n{module_toc_md}\n{end_marker}"

    # read in the readme
    readme_path = root / readme
    with open(readme_path) as readme_file:
        readme_contents = readme_file.read()

    # find start and end markers
    start_index = readme_contents.index(start_marker)
    end_index = readme_contents.index(end_marker) + len(end_marker)

    # update readme contents
    readme_contents = readme_contents[:start_index] + module_toc_md_with_markers + readme_contents[end_index:]

    print(readme_contents)

    # write updated readme
    with open(readme_path, "w") as readme_file:
        readme_file.write(readme_contents)


def main():
    parser = ArgumentParser(
        description="Find all the Modules and update README.md at root.",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Root directory to start searching from",
    )
    parser.add_argument(
        "--readme",
        type=str,
        default="README.md",
        help="Readme filename.  Default: README.md",
    )
    parser.add_argument(
        "--start-replace",
        type=str,
        default="<!-- BEGIN_MODULES_TOC -->",
        help="Start of replace for Modules TOC.",
    )
    parser.add_argument(
        "--end-replace",
        type=str,
        default="<!-- END_MODULES_TOC -->",
        help="End of replace for Modules TOC.",
    )
    args = parser.parse_args()
    root = Path(args.root)
    readme = args.readme
    start_marker = args.start_replace
    end_marker = args.end_replace

    # get list of validated modules
    module_paths = list_module_paths(root)
    valid_module_paths = [module_path for module_path in module_paths if is_valid_module(module_path)]

    # generate tf-docs hooks for each module
    module_toc_md = generate_modules_toc_md(root, valid_module_paths)

    # update the README.md in root
    update_root_readme(root, readme, module_toc_md, start_marker, end_marker)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
