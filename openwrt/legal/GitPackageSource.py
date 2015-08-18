import subprocess
import os
from PackageSource import PackageSource

class GitPackageSource(PackageSource):
    
    def __init__(self, gitRoot):
        self.gitRoot = gitRoot

    def copyTo(self, qsdkRoot, name, version, destPath):
        
        if version:
            versionString="-" + version
        else:
            versionString=""
            
        absGitRoot = os.path.join(qsdkRoot, self.gitRoot)
        absDestPath = "%s/%s%s.sources.tar.xz" % (os.path.abspath(destPath), name, versionString)
        
        # Get list of files
        p = subprocess.Popen([ "git", "ls-tree", "-r", "HEAD", "--name-only" ],
                             cwd=absGitRoot,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode:
            raise Exception("git ls-tree failed: %s" % err)
        versionedFiles=out.strip().split("\n")
        
        # Tar them
        p = subprocess.Popen([ "tar", "-cJf", absDestPath ] + versionedFiles,
                             cwd=absGitRoot,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode:
            raise Exception("tar -cJf failed: %s" % err)

