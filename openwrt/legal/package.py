import os

class Package ():
  """Package class for licensing info"""

  def __init__(self, aName, aVersion, aWebsite, aPackagePath, aLicenses, aOnTarget, aIgnore):
    self.name           = aName                                    # name
    self.version        = aVersion                                 # version
    self.website        = aWebsite                                 # website
    self.packageRoot    = self.rootOfPath(aPackagePath)            # package root directory
    self.packagePath    = aPackagePath
    self.licenses       = aLicenses                                # license file relative to packageRootDir
    self.onTarget       = aOnTarget                                # package will be deployed on target
    self.ignore         = aIgnore                                  # will not be processed to license list on product target

  def path(self, targetBuildRootDir):
    return os.path.join(targetBuildRootDir, self.packagePath)

  def rootOfPath(self,path):
    return path[:path.index(os.sep)] if os.sep in path else path

  def default(self, o):
    return o.__dict__
    
