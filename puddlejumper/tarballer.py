"""All compression happens here."""
import os
import tarfile


class Tarballer(object):
    """Bundle a list of files into a single gzipped tarball.

    Args:
        tarfile (str): This is the absolute path to the tarball.

    """
    def __init__(self, tarfile):
        self.tarfile = tarfile

    def compress_all(self, file_list):
        """Compress a list of files.

        This will copy all files to a temporary directory (must be NO file name
        collisions) and include them all in a gzipped tarball.  The base path
        inside the tarball is ``export/``.  If a file already exists at the
        location, it will be overwritten!


        Args:
            file_list (list): List of absolute paths for files to be tarballed.

        """

        with tarfile.open(self.tarfile, "w:gz") as tar_file:
            for file_path in file_list:
                arcname = os.path.basename(file_path)
                print("Adding %s to archive %s\n\tfrom %s" % (arcname,
                                                              self.tarfile,
                                                              file_path))
                tar_file.add(file_path, arcname=arcname,
                             recursive=False)
        print("Done composing %s" % self.tarfile)
        return

    def decompress_all(self, decompress_path):
        """Extract all files from gzipped tarball.

        Args:
            decompress_path (str): Path to place files extracted from tarfile.

        """

        with tarfile.open(self.tarfile, "r") as tar_file:
            for member in tar_file.getmembers():
                print("Extracting %s to %s" % (member.name, decompress_path))
                tar_file.extract(member, path=decompress_path)
        print("Extraction complete!  Find results in %s" % decompress_path)
        return
