# PuddleJumper

## Packs and unpacks git repos for air-gapped transmission.

This tool produces a single gzipped tarball of git repositories saved in
`git bundle` format.  The archive can be expanded (using this tool, or using
the `tar` command) on the other side of the air gap, and the repositories can
be cloned back out of the bundle file.  For details on the bundle format, look
[here](https://git-scm.com/docs/git-bundle) or section 15:07
[here](https://www.alchemistowl.org/pocorgtfo/pocorgtfo15.pdf)

### Requirements

* Python 2.7.13 or newer
* Linux or Mac OS
* libgit2 (Mac: ``brew install libgit2``)
* Install Python dependencies: `pip install -r ./requirements.txt`

### Configuration

Configuration is stored in the `config.yaml` file.  Be sure to change
`privkey_path` and `pubkey_path` in `config.yaml` to valid paths for SSH keys.

### Getting Help

python ./pj.py -h

### Usage

python ./pj.py unpack

python ./pj.py pack
