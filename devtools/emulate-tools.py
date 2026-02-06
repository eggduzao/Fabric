#!/usr/bin/env python3
"""
This script can be symlinked to samtools, bcftools, bgzip, or tabix.
When invoked under one of those names, it will emulate that tool's
behaviour by using fabric's facilities.
"""

import argparse
import gzip
import os
import sys
import tempfile

import fabric

command = os.path.basename(sys.argv[0])

if command in ("samtools", "bcftools"):
    if len(sys.argv) > 1:
        try:
            tool = fabric.utils.FabricDispatcher(command, sys.argv[1])
            tool(*sys.argv[2:], catch_stdout=None)
            print(tool.stderr, end="", file=sys.stderr)
        except fabric.utils.SamtoolsError as e:
            sys.exit(f"emulate-tools.py: {e}")

    else:
        version = getattr(fabric.version, f"__{command}_version__")
        print(f"Program: {command}\nVersion: {version}", file=sys.stderr)

else:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--stdout", action="store_true")
    parser.add_argument("-d", "--decompress", action="store_true")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("-p", "--preset")
    parser.add_argument("input_file", nargs="?")
    opt = parser.parse_args()

    if command == "bgzip":
        if opt.decompress:
            with gzip.open(sys.stdin.buffer, "rb") as f:
                sys.stdout.buffer.write(f.read())

        elif opt.input_file and opt.stdout:
            fabric.tabix_compress(opt.input_file, "-", force=True)

        else:
            f = tempfile.NamedTemporaryFile(delete=False)
            f.write(sys.stdin.buffer.read())
            f.close()
            fabric.tabix_compress(f.name, "-", force=True)
            os.remove(f.name)

    elif command == "tabix":
        fabric.tabix_index(opt.input_file, preset=opt.preset, force=opt.force)

    else:
        sys.exit(f"emulate-tools.py: unknown command {command!r}")
