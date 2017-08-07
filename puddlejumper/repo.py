"""All git repository management happens here"""
import os
import subprocess
from pygit2 import Keypair, clone_repository, RemoteCallbacks


class Repo(object):
    """Initialization takes three argments.

    Args:
        url (str): The git repo url.  Not HTTPS. git://hostname:port/path
        name (str): The name of the repository.  No spaces.  This becomes
            the name of the packfile in the tarball.
        privkey (str): This is the text of the private key used to access the
            repository.
    """
    def __init__(self, url, basepath, name, username, privkey, pubkey,
                 branch="master"):
        self.name = name
        self.url = url
        self.branch = branch
        self.repo_path = os.path.join(basepath, name)
        self.callbacks = RemoteCallbacks(credentials=Keypair(username, pubkey,
                                                             privkey, ""))
        self.repo = self.clone_repo()
        self.packed_path = "%s.packed" % self.repo_path


    def clone_repo(self):
        """Clone the repo to the local machine.

        Args:
            basepath (str): Path to clone repository into.  For instance, if
                the URL is ``git@gitserver:/mine/app_repo.git``, and the
                basepath is ``/tmp/dropfiles/`` then the repo will appear on
                disk under ``/tmp/dropfiles/app_repo``.
            branch (str): The name of the branch to clone.  Defaults to
                ``master``.
        """

        repo = clone_repository(self.url, self.repo_path,
                                checkout_branch=self.branch,
                                callbacks=self.callbacks)
        return repo

    def pack_repo(self, packfile_path):
        """Pack the repo using ``git bundle``.

        Args:
            packfile_path (str): Path for the resulting packfile.

        """

        command_string = "git bundle create %s %s" % (packfile_path,
                                                      self.branch)
        p = subprocess.Popen(command_string.split(' '), cwd=self.repo_path)
        p.communicate()
        return

    @classmethod
    def verify_repo(cls, packfile_path):
        """Verify the bundled repo.

        Args:
            packfile_path (str): Path of packfile to verify.

        """

        success = True
        command_string = "git bundle verify %s" % packfile_path
        p = subprocess.Popen(command_string.split(' '))
        try:
            p.communicate()
        except subprocess.CalledProcessError:
            success = False
        return success
