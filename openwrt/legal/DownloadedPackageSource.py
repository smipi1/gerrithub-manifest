import subprocess
import os
import shutil
from PackageSource import PackageSource

class DownloadedPackageSource(PackageSource):
    
    def __init__(self, downloadedFile, patchesDir):
        self.downloadedFile = downloadedFile
        self.patchesDir = patchesDir

    def copyTo(self, qsdkRoot, name, version, destPath):
        print "Package: ", name, version

        if version:
            versionString="-" + version
        else:
            versionString=""
            
        if self.downloadedFile:
            fileExt = os.path.splitext(self.downloadedFile)[1] 
            # Copy downloaded file
            srcFileName = os.path.join(qsdkRoot, "dl", self.downloadedFile)
            dstFilename = os.path.join(destPath, "%s%s.sources.tar%s" %(name, versionString, fileExt))
            shutil.copy(srcFileName, dstFilename)
        
        # tar and copy patches
        if self.patchesDir: 
            p = subprocess.Popen([ "tar", "-cJf", "%s/%s%s.patches.tar.xz" % (os.path.abspath(destPath), name, versionString), "."], 
                                 cwd=os.path.join(qsdkRoot,self.patchesDir),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode:
                raise Exception("tar -cJf failed: %s" % err)
