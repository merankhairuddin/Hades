import argparse
from dissect.target import container, filesystem, volume
from pathlib import Path
from os import listdir, path, geteuid
import json

# Ignore /run since it may produce large numbers of false positives
IGNORE_RUN = True

def get_filesystem(path: str) -> str:
    try:
        return filesystem.open(open(path, "rb"))
    except:
        try:
            return filesystem.open(volume.open(open(path, "rb")))
        except:
            disk = container.open(path)
            vol = volume.open(disk)
            vol_i = 0
            if len(vol.volumes) > 1:
                for v in vol.volumes:
                    print(f"[{vol.volumes.index(v)}] {v.name} ({v.size} bytes)")
                vol_i = int(input("$ "))
            return filesystem.open(vol.volumes[vol_i])

def is_visible(path: str) -> bool:
    p = Path(path)
    parent = p.parent.absolute()
    try:
        return p.name in listdir(parent)
    except:
        print("Failed to open", path)
        return True

def whitelist(path: str) -> bool:
    if path == "/":
        return True
    p = Path(path)
    if str(p.parents[-2]) == "/run" and IGNORE_RUN:
        return True
    return False

def extract_file(file: filesystem.FilesystemEntry, path: str) -> None:
    with open(path, "wb") as out:
        out.write(file.open().read())

def scan_filesystem(disk_path: str, mount_point: str, extract_path: str) -> int:
    try:
        fs = get_filesystem(disk_path)
        print("Filesystem:", fs.__type__)
    except:
        print(disk_path, "is not a valid volume/disk OR does not contain a supported filesystem")
        exit(-1)

    hidden_files = 0
    extract = []

    for _, dirs, files in fs.walk_ext("/", True, None, False):
        for entry in dirs + files:
            full_path = path.join(mount_point, str(entry))
            if not is_visible(full_path) and not whitelist(full_path):
                out_path = path.join(extract_path, full_path[1:])
                print(f"Hidden: {full_path} ({entry.stat(False).st_ino})")
                hidden_files += 1
                extract.append([entry, out_path])

    for entry, out_path in extract:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        if entry.is_file(False):
            try:
                extract_file(entry, out_path)
                print(f"Extracted: {out_path} | MD5={entry.md5()} SHA256={entry.sha256()}")
            except:
                print("Failed to extract:", out_path)
        else:
            Path(out_path).mkdir(parents=True, exist_ok=True)
            print("Created:", out_path)

    return hidden_files

def main():
    parser = argparse.ArgumentParser(description="Hades: Hidden file detection using Dissect")
    parser.add_argument("disk", help="Disk, volume, or filesystem path (e.g., /dev/sda1)")
    parser.add_argument("mount_point", help="Mount point (e.g., /)")
    parser.add_argument("extract_path", help="Directory to extract hidden files to")
    parser.add_argument("--output-format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--state-file", help="Optional state file for incremental scan")
    parser.add_argument("--audit-log", help="Optional path to audit log (JSONL)")

    args = parser.parse_args()

    if geteuid() != 0:
        print("This script must be run as root.")
        exit(-1)

    hidden_files = scan_filesystem(args.disk, args.mount_point, args.extract_path)

    if args.output_format == "json":
        result = {
            "disk": args.disk,
            "mount_point": args.mount_point,
            "extract_path": args.extract_path,
            "hidden_files": hidden_files
        }
        print(json.dumps(result, indent=2))

    return hidden_files

if __name__ == "__main__":
    exit(main())
