#!/usr/bin/python

import shutil
import sys
import os
import licenses
import argparse
from package import Package
import license as stdLicenses
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

def createLicenseFiles(package, targetBuildRootDir, outputDir, legalDir):
    if( (package.licenses == None) or (package.licenses == []) ):
        exitWithError("No licenses found for package: %s" % (package.name))
    
    licenseFiles = {}
    i = 0
    for license in package.licenses:
        if not license.licenseFile:
            try:
                source = os.path.join(legalDir, stdLicenses.licensePath(license.licenseType))
            except KeyError:
                source = os.path.join(legalDir, "specificLicenses", package.name + ".txt")
        else:
            source = os.path.join(package.path(targetBuildRootDir), license.licenseFile)

        licenseFiles[source] = ( i, license.filePath(package, outputDir) )
        i = i + 1
    
    for src, item in sorted(licenseFiles.iteritems(), key=itemgetter(0)):
        append(src , item[1])

def currentUsedPackages(packagesDirectory):
  usedPackages = [name for name in os.listdir(packagesDirectory)
    if os.path.isdir(os.path.join(packagesDirectory, name))]
  return usedPackages 

def packagesVerified(packagesInLicenses, targetBuildRootDir):
  errorList = []
  packagesUsedOnTarget = currentUsedPackages(targetBuildRootDir)

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

def createAllLicenseFiles(packages, targetBuildRootDir, outputDir, legalDir):
    for package in packages:
        if package.onTarget:
            if not package.ignore and package.onTarget:
                try:
                    createLicenseFiles(package, targetBuildRootDir, outputDir, legalDir)
                    processedPackages.append(package)
                    print 'add license: %s' % (package.name)
                except IOError, e:
                    exitWithError("Unable to copy file. %s" % (e))
            else:
                print 'skip license: %s (%s)' % (package.name, package.ignore)

def packagesToJson(aPackages, manifestFile):
  """transforms package List of Package to JSON"""
  import json
  f = open(manifestFile, 'w')
  f.write(json.dumps(aPackages, cls=PackageAndLicenseEncoder, indent=2, sort_keys=True))
  f.close()

#------------------------------------------------------------------------------------------------------------------------------

def main():
    defaultOutputDir=os.path.join(ownDir,'..',"release","licenses.production")
    parser = argparse.ArgumentParser(description='Hue OpenWRT license validation and generation')
    parser.add_argument('-o', '--output-dir', dest='outputDir',
                        default=defaultOutputDir,
                        help='Directory where the output should be generated (defaults: %(default)s)')
    parser.add_argument('-m', '--manifest-file', dest='manifestFile',
                        default=os.path.join(defaultOutputDir, "licenses.json"),
                        help='Directory where the output should be generated (defaults: %(default)s)')
    parser.add_argument('-t', '--target-build-root-dir', dest='targetBuildRootDir',
                        default=os.path.join(ownDir, "..", "qualcomm", "qsdk", "build_dir", "target-mips_34kc_uClibc-0.9.33.2"),
                        help='Directory where the output should be generated (defaults: %(default)s)')
    args = parser.parse_args()

    if not packagesVerified(licenses.packages, args.targetBuildRootDir):
      print "Licenses of some of the package(s) are not correctly verified. Maybe the version changed or the package is new"
      exitWithError("Please update the licenses file to correct: " + os.path.join(ownDir, "licenses.py"))
    
    try:
      shutil.rmtree(args.outputDir)
    except Exception as e:
      print "Unable to delete directory: %s" % (e)
    os.makedirs(args.outputDir)

    createAllLicenseFiles(licenses.packages, args.targetBuildRootDir, args.outputDir, ownDir)
    print packagesToJson(processedPackages, args.manifestFile)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
    
