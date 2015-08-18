import subprocess
import os
from PackageSource import PackageSource

class OpenWrtPackageSource(PackageSource):
    
    def __init__(self):
        pass

    def copyTo(self, qsdkRoot, name, version, destPath):
        p = subprocess.Popen([ "git", "ls-tree", "-r", "HEAD", "--name-only" ],
                             cwd=qsdkRoot,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode:
            raise Exception("git ls-tree failed: %s" % err)
        versionedFiles=out.strip().split("\n")
        if version:
            versionString="-" + version
        else:
            versionString=""
        p = subprocess.Popen([ "tar", "-czf", "%s/%s%s.tar.gz" % (os.path.abspath(destPath), name, versionString) ] + versionedFiles,
                             cwd=qsdkRoot,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode:
            raise Exception("tar -czf failed: %s" % err)

