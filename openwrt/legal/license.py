import os
import shutil

standardLicenses = { 'GPL-1'    : "specificLicenses/gpl-1.0.txt" 
                   , 'GPL-2'    : "specificLicenses/gpl-2.0.txt" 
                   , 'GPL-3'    : "specificLicenses/gpl-3.0.txt" 
                   , 'LGPL-2.1' : "specificLicenses/lgpl-2.1.txt" 
                   , 'LGPL-3'   : "specificLicenses/lgpl-3.0.txt"
                   }

def licensePath(license):
    return standardLicenses[license]

class License ():
    """license class for license info"""
    
    def __init__(self, aLicenseType, aLicenseFile="LICENSE"):
        self.licenseType  = aLicenseType     # Type of License, e.g: LGPL-2.1
        self.licenseFile  = aLicenseFile     # license file relative to packagePath of Package
      
    def filePath(self, package, legalDir):
        if package.version:
            return os.path.join(legalDir, "license_%s_%s.txt" % (package.name, package.version))
        else:
            return os.path.join(legalDir, "license_%s.txt" % (package.name))
    
    def default(self, o):
        return o.__dict__
