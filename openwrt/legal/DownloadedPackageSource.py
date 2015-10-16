import subprocess
import os
import shutil
from PackageSource import PackageSource

class DownloadedPackageSource(PackageSource):
    
    def __init__(self, downloadedFile, patchesDir):
        self.downloadedFile = downloadedFile
        self.patchesDir = patchesDir

    def copyTo(self, args, name, version, packagePath, destPath):
        print "Package: ", name, version

        if self.downloadedFile:
            # Copy downloaded file
            srcFileName = os.path.join(args.qsdkRootDir, "dl", self.downloadedFile)
            dstFilename = os.path.join(destPath, self.downloadedFile)
            shutil.copy(srcFileName, dstFilename)
            self.splitFileIfNeeded(dstFilename)

        if self.patchesDir:
            tarBasename, cmpExt = os.path.splitext(self.downloadedFile)
            basename, tarExt = os.path.splitext(tarBasename)
            self.tar(os.path.join(args.qsdkRootDir, self.patchesDir), destPath, basename, "", "patches") 
