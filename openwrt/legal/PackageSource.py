import subprocess
import os

githubFileSizeLimit = 50 * 1024 * 1024

class PackageSource:
    
    def __init__(self):
        pass
    
    def copyTo(self, args, name, version, packagePath, destPath):
        print "warning: Package provider for %s not implemented yet!!" % name
    
    def splitFileIfNeeded(self, destFilepath):
        stat = os.stat(destFilepath)
        if stat.st_size > githubFileSizeLimit:
            print "warning: File size (%dMB) exceeds github file size limit (%dMB): %s" % (
                    stat.st_size / 1024 / 1024,
                    githubFileSizeLimit / 1024 / 1024,
                    os.path.basename(destFilepath) )
            print "         Split into:"
            noParts, noPartsRem = divmod(stat.st_size, githubFileSizeLimit)
            if noPartsRem:
                noParts += 1
            for part in range(0, noParts):
                destFilepathPart = "%s.part.%d" % (destFilepath, part)
                dd = [ "dd",
                       "if=%s" % destFilepath,
                       "of=%s" % destFilepathPart,
                       "bs=%d" % githubFileSizeLimit,
                       "skip=%d" % part, "count=1" ]
                p = subprocess.Popen(dd)
                p.communicate()
                if p.returncode:
                    raise Exception("error executing: " + " ".join(dd))
                print "         " + os.path.basename(destFilepathPart)
            os.unlink(destFilepath)

    def tar(self, sourcePath, destPath, name, version, postfix = None, excludes = [], sourceFiles = [ "." ]):
        if version:
            basename = name + "-" + version
        else:
            basename = name
        if postfix:
            basename += "." + postfix
        destFilepath = os.path.join(os.path.abspath(destPath), basename + ".tar.gz")
        tar = [ "tar", "-czf", destFilepath ]
        for e in excludes:
            tar += [ "--exclude=" + e ]
        tar += [ "--mtime=1970-01-01" ] + sourceFiles
        p = subprocess.Popen(tar, cwd=sourcePath)
        p.communicate()
        if p.returncode:
            raise Exception("error executing: " + " ".join(tar))
        self.splitFileIfNeeded(destFilepath)
        return destFilepath
