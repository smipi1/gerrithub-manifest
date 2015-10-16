import subprocess
import os
from PackageSource import PackageSource

class OpenWrtPackageSource(PackageSource):
    
    def __init__(self):
        pass

    def copyTo(self, args, name, version, packagePath, destPath):
        p = subprocess.Popen([ "git", "ls-tree", "-r", "HEAD", "--name-only" ],
                             cwd=args.qsdkRootDir,
                             stdout=subprocess.PIPE)
        out = p.communicate()
        if p.returncode:
            raise Exception("git ls-tree failed: %s" % err)
        versionedFiles=out.strip().split("\n")
        if version:
            basename = name + "-" + version
        else:
            basename = name
        
        self.tar(os.path.join(getattr(args, self.rootAttribute), packageDir), destPath, name, version)

