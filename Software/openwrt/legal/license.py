import os
import shutil

class License ():
  """license class for license info"""

  licenseRootDir = "licenses"

  standardLicenses = { 'GPL-1'    : "standardLicenses/gpl-1.0.txt" 
                     , 'GPL-2'    : "standardLicenses/gpl-2.0.txt" 
                     , 'GPL-3'    : "standardLicenses/gpl-3.0.txt" 
                     , 'LGPL-2.1' : "standardLicenses/lgpl-2.1.txt" 
                     , 'LGPL-3'   : "standardLicenses/lgpl-3.0.txt"
                     }

  def __init__(self, aLicenseType, aLicenseFile="LICENSE"):
    self.licenseType  = aLicenseType     # Type of License, e.g: LGPL-2.1
    self.licenseFile  = aLicenseFile     # license file relative to packagePath of Package
    
    try:
      shutil.rmtree(License.licenseRootDir)
    except Exception as e:
      print "Unable to delete directory: %s" % (e)

    os.makedirs(License.licenseRootDir)

  def filePath(self, package):
    return "%s/license_%s_%s.txt" % (License.licenseRootDir, package.name, package.version)

  def default(self, o):
    return o.__dict__
