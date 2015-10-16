import subprocess
import os
from PackageSource import PackageSource

class GitPackageSource(PackageSource):
    
    def __init__(self, gitRoot):
        self.gitRoot = gitRoot

    def copyTo(self, args, name, version, packagePath, destPath):
        
        absGitRoot = os.path.join(args.qsdkRootDir, self.gitRoot)
        
        # Get list of files
        p = subprocess.Popen([ "git", "ls-tree", "-r", "HEAD", "--name-only" ],
                             cwd=absGitRoot,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode:
            raise Exception("git ls-tree failed: %s" % err)
        versionedFiles=out.strip().split("\n")
        
        self.tar(absGitRoot, destPath, name, version, sourceFiles=versionedFiles)

