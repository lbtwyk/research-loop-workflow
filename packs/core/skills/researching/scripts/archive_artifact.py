#!/usr/bin/env python3
"""Safely archive a public paper PDF or a shallow source repository."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path


def fail(message):
    raise SystemExit(message)


def run(*args, **kwargs):
    cwd = kwargs.get("cwd")
    result = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return result.stdout.strip()


def archive_pdf(url, destination, max_mib):
    if destination.exists():
        fail(f"refusing to overwrite existing path: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Grok research archiver/1.0"})
    limit = max_mib * 1024 * 1024
    digest = hashlib.sha256()
    size = 0
    temporary = None
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            declared = response.headers.get("Content-Length")
            if declared and int(declared) > limit:
                fail(f"download exceeds {max_mib} MiB limit")
            with tempfile.NamedTemporaryFile(
                dir=destination.parent, prefix=f".{destination.name}.", delete=False
            ) as output:
                temporary = Path(output.name)
                first = True
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    if first and b"%PDF-" not in chunk[:1024]:
                        fail("download is not a PDF (missing PDF signature)")
                    first = False
                    size += len(chunk)
                    if size > limit:
                        fail(f"download exceeds {max_mib} MiB limit")
                    output.write(chunk)
                    digest.update(chunk)
        if size == 0:
            fail("downloaded file is empty")
        os.replace(temporary, destination)
        temporary = None
    finally:
        if temporary is not None:
            if temporary.exists():
                temporary.unlink()
    print(json.dumps({
        "kind": "pdf",
        "path": str(destination.resolve()),
        "bytes": size,
        "sha256": digest.hexdigest(),
        "source": url,
    }))


def archive_repo(url, destination, ref):
    if destination.exists():
        fail(f"refusing to overwrite existing path: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        run(
            "git", "clone", "--depth", "1", "--filter=blob:none", "--no-tags",
            "--no-recurse-submodules", url, str(destination),
        )
        if ref:
            run("git", "fetch", "--depth", "1", "origin", ref, cwd=destination)
            run("git", "checkout", "--detach", "FETCH_HEAD", cwd=destination)
        commit = run("git", "rev-parse", "HEAD", cwd=destination)
        remote = run("git", "remote", "get-url", "origin", cwd=destination)
        license_files = sorted(
            path.name
            for path in destination.iterdir()
            if path.is_file() and path.name.lower().startswith(("license", "copying"))
        )
    except Exception:
        if destination.exists():
            shutil.rmtree(destination)
        raise
    print(json.dumps({
        "kind": "repo",
        "path": str(destination.resolve()),
        "remote": remote,
        "commit": commit,
        "license_files": license_files,
    }))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")

    pdf = subparsers.add_parser("pdf", help="download and validate a public PDF")
    pdf.add_argument("url")
    pdf.add_argument("destination", type=Path)
    pdf.add_argument("--max-mib", type=int, default=100)

    repo = subparsers.add_parser("repo", help="make a shallow source snapshot")
    repo.add_argument("url")
    repo.add_argument("destination", type=Path)
    repo.add_argument("--ref", help="branch, tag, or commit to fetch and check out")

    args = parser.parse_args()
    if not args.command:
        parser.error("a command is required")
    if args.command == "pdf":
        if args.max_mib <= 0:
            fail("--max-mib must be positive")
        archive_pdf(args.url, args.destination, args.max_mib)
    else:
        archive_repo(args.url, args.destination, args.ref)


if __name__ == "__main__":
    main()
