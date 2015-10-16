import subprocess
import os
import shutil
from PackageSource import PackageSource

class SymlinkedPackageSource(PackageSource):
    
    def __init__(self, destFile):
        self.destFile = destFile

    def copyTo(self, args, name, version, packagePath, destPath):
        print "Package: ", name, version

        if version:
            basename = name + "-" + version
        else:
            basename = name
            
        extension = ".tar" + os.path.splitext(self.destFile)[1]
        
        os.symlink(self.destFile, os.path.join(destPath, basename + extension))
