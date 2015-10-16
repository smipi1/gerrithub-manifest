import subprocess
import os
import shutil
from PackageSource import PackageSource

class PlainPackageSource(PackageSource):
    
    def __init__(self, aDir=None, rootAttribute="preparedPackageRootDir", excludes=[]):
        self.aDir = aDir
        self.rootAttribute = rootAttribute
        self.excludes = excludes

    def copyTo(self, args, name, version, packagePath, destPath):
        print "Package: ", name, version

        if version:
            basename = name + "-" + version
        else:
            basename = name
        
        if self.aDir:
            packageDir = self.aDir
        else:
            packageDir = packagePath[0]

        self.tar(os.path.join(getattr(args, self.rootAttribute), packageDir), destPath, name, version, excludes = self.excludes)
