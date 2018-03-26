import magic
import hashlib
import io

from .submodule_base import SubmoduleBaseclass
from ssdeep import Hash


class MetadataSubmodule(SubmoduleBaseclass):
    def __init__(self):
        SubmoduleBaseclass.__init__(self)
        self.name = 'Metadata'

    def check_file(self, path):
        """
        Metadata submodule will analyze every file, therefore it will always return true.

        :return: True
        """
        return True

    def analyze_file(self, path):
        # Hash the file
        with io.open(path, 'rb') as fh:
            buf = fh.read()
            md5 = hashlib.md5()
            md5.update(buf)
            sha1 = hashlib.sha1()
            sha1.update(buf)
            sha256 = hashlib.sha256()
            sha256.update(buf)
            ssdeep = Hash()
            ssdeep.update(buf)

        self.add_result_subsection('Hashes', {
            'md5': md5.hexdigest(),
            'sha1': sha1.hexdigest(),
            'sha256': sha256.hexdigest(),
            'ssdeep': ssdeep.digest()
        })

        # Get libmagic info
        magicliteral = magic.Magic().from_file(path)
        mimetype = magic.Magic(mime=True).from_file(path)
        self.add_result_subsection('Libmagic information', {
            'Magic literal': magicliteral,
            'MimeType': mimetype
        })

        return self.results
