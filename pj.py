"""Bundle or unbundle git repos for easy transmission across an air gap."""

import argparse
import os
import sys
import tempfile
import yaml

from puddlejumper.repo import Repo
from puddlejumper.tarballer import Tarballer

desc = "Bundle or unbundle git repos for easy transmission across an air gap."
separator = "######################################"

# Parse out CLI args
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("action",
                    type=str,
                    help="`pack` or `unpack`")
parser.add_argument("-c", "--configfile",
                    type=str,
                    default="./config.yaml",
                    help="Path to configuration file")
args = parser.parse_args()

if args.action not in ["pack", "unpack"]:
    print("Unrecognized action: %s" % args.action)
    sys.exit(1)

# Get configuration from file
with open(args.configfile) as config_file:
    config = yaml.load(config_file)


# Create a gzipped tarball object
tball = Tarballer(config["tarfile"])

if args.action == "pack":
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Retrieve and pack all repos
    packfile_paths = []
    for repo in config["repos"]:
        output_msg = "# Downloading and packing %s" % repo["name"]
        print("\n%s\n%s" % (separator, output_msg))
        packfile_name = "%s.packfile" % repo["name"]
        packfile_path = os.path.join(temp_dir, packfile_name)
        local_repo = Repo(repo["url"], temp_dir, repo["name"],
                          config["username"], config["privkey_path"],
                          config["pubkey_path"], repo["branch"])
        local_repo.pack_repo(packfile_path)
        if not local_repo.verify_repo(packfile_path):
            print("%s failed validation!" % packfile_path)
            sys.exit(1)
        packfile_paths.append(packfile_path)
        print(separator)

    # Bundle all the packfiles together
    print("\n\n")
    tball.compress_all(packfile_paths)

elif args.action == "unpack":
    tball.decompress_all(config["out_dir"])
else:
    print("I don't recognize this action: %s" % args.action)
    sys.exit(1)
print("Done!!")
