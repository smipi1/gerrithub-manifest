#!/usr/bin/python

import shutil
import sys
import os
import licenses
from package import Package
from license import License
from packageAndLicenseEncoder import PackageAndLicenseEncoder
from operator import itemgetter

# 1) check contents of licenses
# 2) copy license text
# q1) how to deal with multiple licenses

ownDir = os.path.dirname(os.path.realpath(__file__))

processedPackages = []

def exitWithError(errorText):
  print "Error in licenses: %s" % (errorText)
  sys.exit(1)

def append(source, dest):
    source = open(source, 'r')
    destination = open(dest, 'a')
    shutil.copyfileobj(source, destination)
    destination.write('\n------------------------------------------------------------------------------\n');
    destination.close()
    source.close()

def createLicenseFiles(package):
    if( (package.licenses == None) or (package.licenses == []) ):
        exitWithError("No licenses found for package: %s" % (package.name))
    
    licenseFiles = {}
    i = 0
    for license in package.licenses:
        if not license.licenseFile:
            if license.licenseType in License.standardLicenses:
                source = License.standardLicenses[license.licenseType]
            else:
                source = "specificLicenses/" + package.name + '.txt'
        else:
            source = "%s/%s" % (package.path(), license.licenseFile)

        licenseFiles[source] = ( i, license.filePath(package) )
        i = i + 1
    
    for src, item in sorted(licenseFiles.iteritems(), key=itemgetter(0)):
        append(src , item[1])

def currentUsedPackages(packagesDirectory):
  usedPackages = [name for name in os.listdir(packagesDirectory)
    if os.path.isdir(os.path.join(packagesDirectory, name))]
  return usedPackages 

def packagesVerified(packagesInLicenses):
  errorList = []
  packagesUsedOnTarget = currentUsedPackages(packagesInLicenses[0].packageRootDir)

  for packageOnTarget in packagesUsedOnTarget:
    packageFoundInLicenses = False
    for package in packagesInLicenses:
      if packageOnTarget == package.packageRoot:
        packageFoundInLicenses = True
        break;
    if not packageFoundInLicenses:
      errorList.append('Used package "%s" is not found in the Licenses list' % (packageOnTarget))

  if len(errorList) is 0:
    return True
  
  for item in errorList:
    print item

  return False

def createAllLicenseFiles(packages):
  for package in packages:
    if package.onTarget:
        if not package.ignore and package.onTarget:
          try:
            createLicenseFiles(package)
            processedPackages.append(package)
            print 'license file created for package "%s"' % (package.name)
          except IOError, e:
            exitWithError("Unable to copy file. %s" % (e))
        else:
            print 'package "%s" is ignored because: %s' % (package.name, package.ignore)

def packagesToJson(aPackages):
  """transforms package List of Package to JSON"""
  import json
  f = open('%s/%s' % (License.licenseRootDir,'licenses.json'), 'w')
  f.write(json.dumps(aPackages, cls=PackageAndLicenseEncoder, indent=2, sort_keys=True))
  f.close()

#------------------------------------------------------------------------------------------------------------------------------


if not packagesVerified(licenses.packages):
  print "Licenses of some of the package(s) are not correctly verified. Maybe the version changed or the package is new"
  exitWithError("Please update the licenses file to correct: %s/%s.py" % (ownDir, License.licenseRootDir))

createAllLicenseFiles(licenses.packages)
print packagesToJson(processedPackages)

sys.exit(0)
