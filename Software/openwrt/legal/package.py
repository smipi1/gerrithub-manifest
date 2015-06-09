import os

class Package ():
  """Package class for licensing info"""

  packageRootDir = "../qualcomm/qsdk/build_dir/target-mips_34kc_uClibc-0.9.33.2"

  def __init__(self, aName, aVersion, aWebsite, aPackagePath, aLicenses, aOnTarget, aIgnore):
    self.name           = aName                                    # name
    self.version        = aVersion                                 # version
    self.website        = aWebsite                                 # website
    self.packageRoot    = self.rootOfPath(aPackagePath)            # package root directory
    self.packagePath    = Package.packageRootDir + "/" + aPackagePath # path relative to current dir
    self.licenses       = aLicenses                                # license file relative to packageRootDir
    self.onTarget       = aOnTarget                                # package will be deployed on target
    self.ignore         = aIgnore                                  # will not be processed to license list on product target

  def path(self):
    return self.packagePath

  def rootOfPath(self,path):
    return path[:path.index(os.sep)] if os.sep in path else path

  def default(self, o):
    return o.__dict__
    
