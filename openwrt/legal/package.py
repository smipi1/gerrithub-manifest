import os
from PackageSource import PackageSource


class Package ():
  """Package class for licensing info"""

  def __init__(self, aName, aVersion, aWebsite, aPackagePath, aLicenses, aPackageSource, aIgnore):
    self.name           = aName                                    # name
    self.version        = aVersion                                 # version
    self.website        = aWebsite                                 # website
    self.packagePath    = aPackagePath
    self.licenses       = aLicenses                                # license file relative to packageRootDir
    self.packageSource  = aPackageSource 
    self.ignore         = aIgnore                                  # will not be processed to license list on product target
    self.packageRoot    = self.rootOfPath(aPackagePath)            # package root directory

  def path(self, targetBuildRootDir):
    return os.path.join(targetBuildRootDir, self.packagePath[0])

  def rootOfPath(self,path):
    return path[:path.index(os.sep)] if os.sep in path else path

  def default(self, o):
    return o.__dict__
    
