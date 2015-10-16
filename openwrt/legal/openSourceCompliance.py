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
import hashlib
import glob
import fnmatch
import magic
import pprint
import subprocess
import tempfile

ownDir = os.path.dirname(os.path.realpath(__file__))

processedPackages = []

def hashFile(filepath):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filepath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    hasher.update(os.path.basename(filepath))
    return hasher.hexdigest()

def exitWithError(errorText):
  print "error: %s" % (errorText)
  sys.exit(1)

def append(source, dest):
    source = open(source, 'r')
    destination = open(dest, 'a')
    shutil.copyfileobj(source, destination)
    destination.write('\n------------------------------------------------------------------------------\n');
    destination.close()
    source.close()

def createLicenseFiles(args, package, legalDir):
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
      source = os.path.join(package.path(args.targetBuildRootDir), license.licenseFile)
      if not os.path.isfile(source):
        source = os.path.join(legalDir, "specificLicenses", license.licenseFile )
        if not os.path.isfile(source):
          exitWithError("License file not found: %s: %s" % (package.name, source))       

    licenseFiles[source] = ( i, license.filePath(package, args.licensesDestDir) )
    i = i + 1
    
  # print "Creating license file for: ", package.name
  for src, item in sorted(licenseFiles.iteritems(), key=itemgetter(0)):
    try:
      append(src , item[1])
      # print "appending: ", src, item[1]
    except IOError, e:
      exitWithError("License file not found: %s: %s" % (package.name, src))

def packageIsIgnored(packageFromLicenses):
  if packageFromLicenses.ignore:
    return True
  else:
    return False

def createAllLicenseFiles(args, packagesOnTarget, legalDir):
  for package in packagesOnTarget:
    packageDetails = packagesOnTarget[package]
    if packageIsIgnored(packageDetails):
      if args.licensesDestDir:
        print 'skip license: %s (%s)' % (packageDetails.name, packageDetails.ignore)
    else:
      processedPackages.append(packageDetails)
      if args.licensesDestDir:
        print 'add license: %s' % (packageDetails.name)
        createLicenseFiles(args, packageDetails, legalDir)

def packagesToJson(aPackages, manifestFile):
  """transforms package List of Package to JSON"""
  import json
  f = open(manifestFile, 'w')
  f.write(json.dumps(aPackages, cls=PackageAndLicenseEncoder, indent=2, sort_keys=True))
  f.close()

def recursiveDirectorySearchInDirectory(searchDirectory, searchName):
  foundDirectories = []
  
  for root, dirnames, filenames in os.walk(searchDirectory):
    for filename in fnmatch.filter(dirnames, searchName):
      foundDirectories.append(os.path.join(root, filename))
      
  return foundDirectories

def searchDirectoriesThatStartWithSpecificWordInDirectory(searchDirectory, searchDirName):
  foundDirectories = []
  
  for dirname in os.listdir(searchDirectory):
    directoryPath = os.path.join(searchDirectory, dirname)
    if os.path.isdir(directoryPath):
      if dirname.find(searchDirName) == 0:
        foundDirectories.append(directoryPath)

  return foundDirectories

def fileIsExecutableOrElf(filePath):
  try:
    magicData = magic.from_file(filePath)
    if 'executable' in magicData:
      return True
    elif 'ELF' in magicData:
      return True
  except IOError as e:
    pass

  return False

def searchTargetFilesAndAddHash(searchDirectories):
  filesDict = {}
  for directory in searchDirectories:
    for filePath in recursiveFileSearchInDirectory(directory):
      if fileIsExecutableOrElf(filePath):
        filesDict[hashFile(filePath)] = filePath

  return filesDict

def recursiveFileSearchInDirectory(searchDirectory):
  files = []
  for root, dirnames, filenames in os.walk(searchDirectory):
    for filename in filenames:
      files.append(os.path.join(root, filename))
  return files

def toRelativePackagePath(packagePath, args):
  return packagePath.replace(args.targetBuildRootDir + "/", "")

def toRelativeRootFilePath(filePath, args):
  return filePath.replace(args.targetBuildRootDir + "/root-ar71xx", "")

def createCleanDir(dir):
  try:
    shutil.rmtree(dir)
  except Exception as e:
    print "Unable to delete directory: %s" % (e)
  os.makedirs(dir)

def hashAvailableTargetFiles(args):
  ipkgDirectories = recursiveDirectorySearchInDirectory(args.targetBuildRootDir, args.targetFileDirName)
  return searchTargetFilesAndAddHash(ipkgDirectories)

def hashFilesOnTarget(args):
  targetFileDirectory = searchDirectoriesThatStartWithSpecificWordInDirectory(args.targetBuildRootDir, "root-")
  if len(targetFileDirectory) > 1:
    exitWithError("More then one directory that start with 'root-' in " + args.targetBuildRootDir)
  return searchTargetFilesAndAddHash(targetFileDirectory)

def listFilesInRootfsAndWhereTheyComeFrom(args, filesOnTarget, availableTargetFiles):
  fileMapping = {}
  for targetFile in filesOnTarget:
    try:
      fullPackagePath = availableTargetFiles[targetFile]
    except KeyError:
      exitWithError("Used target file not found in packages directory: " + args.targetBuildRootDir)
    targetFilepath = toRelativeRootFilePath(filesOnTarget[targetFile], args)
    fileMapping[targetFilepath] = toRelativePackagePath(fullPackagePath, args)

  args.rootfsListingFilepath.truncate()
  args.rootfsListingFilepath.write(pprint.pformat(fileMapping))
  args.rootfsListingFilepath.flush()
  args.rootfsListingFilepath.close()

def addAdditionalPackages(packagesOnTarget, errors, names):
    for name in names:
        found = False
        for package in licenses.packages:
            if name is package.name:
                packagesOnTarget[package.name] = package
                found = True
        if not found:
            errors.append(name)

def checkLicensesForFilesOnTarget(args, filesOnTarget, availableTargetFiles):
  errors = []
  packagesOnTarget = {}
  for targetFile in filesOnTarget:
    try:
      fullPackagePath = availableTargetFiles[targetFile]
    except KeyError:
      exitWithError("Used target file not found in packages directory: " + args.targetBuildRootDir)
    
    packagePath = toRelativePackagePath(fullPackagePath, args)
    
    match = False;
    for package in licenses.packages:
      if not isinstance(package.packagePath, list):
        exitWithError("packagePath not an array of strings: '%s' in %s" % (package.name, os.path.join(ownDir, "licenses.py")))
      for path in package.packagePath:
          if packagePath.find(path) == 0:
            packagesOnTarget[package.name] = package
            match = True
            break;
    
    if not match:
      errors.append(fullPackagePath)

  errors.sort()
  return errors, packagesOnTarget

def copySourcesTo(args, packagesOnTarget):
  for package in packagesOnTarget:
    packageDetails = packagesOnTarget[package]
    if packageIsIgnored(packageDetails):
      print 'skip sources: %s (%s)' % (packageDetails.name, packageDetails.ignore)
    else:
      packageDetails.packageSource.copyTo(args, packageDetails.name, packageDetails.version, packageDetails.packagePath, args.packageSourceDestDir)
      print 'add source: %s' % (packageDetails.name)

#------------------------------------------------------------------------------------------------------------------------------

def main():
    defaultOutputDir=os.path.join(ownDir,'..',"release","licenses.production")
    parser = argparse.ArgumentParser(description='Hue OpenWRT open-source compliance tool')
    parser.add_argument('-q', '--qsdk-root-dir', dest='qsdkRootDir',
                        default=os.path.join("..", "qualcomm", "qsdk"),
                        help='QSDK OpenWRT root directory (defaults: %(default)s)')
    parser.add_argument('-t', '--target-build-root-dir', dest='targetBuildRootDir',
                        default=os.path.join("..", "qualcomm", "qsdk", "build_dir", "target-mips_34kc_uClibc-0.9.33.2"),
                        help='Directory where the target files are located (defaults: %(default)s)')
    parser.add_argument('-i', '--target-file-dir-name', dest='targetFileDirName',
                        default="ipkg-ar71xx",
                        help='Directory name where the files are located that are copied to the target(defaults: %(default)s)')
    parser.add_argument('-d', '--dump-rootfs-listing-to', dest='rootfsListingFilepath',
                        type=argparse.FileType('w'),
                        help='Dump list of files found on rootfs to specified file')
    parser.add_argument('-l', '--licenses-dest-dir', dest='licensesDestDir',
                        default=None,
                        help='Generate licensing information in the specified directory')
    parser.add_argument('-s', '--package-source-dest-dir', dest='packageSourceDestDir',
                        default=None,
                        help='Generate package source archives in the specified directory')
    
    args = parser.parse_args()

    if args.licensesDestDir:
        createCleanDir(args.licensesDestDir)
        args.manifestFile = os.path.join(args.licensesDestDir, "licenses.json")

    availableTargetFiles = hashAvailableTargetFiles(args)
    filesOnTarget = hashFilesOnTarget(args)
    
    if args.rootfsListingFilepath != None:
        listFilesInRootfsAndWhereTheyComeFrom(args, filesOnTarget, availableTargetFiles)

    [incompleteLicenses, packagesOnTarget] = checkLicensesForFilesOnTarget(args, filesOnTarget, availableTargetFiles)
    addAdditionalPackages(packagesOnTarget, incompleteLicenses, [ "linux", "uboot" ])

    if incompleteLicenses:
      print "Missing license information:"
      print "The following files are installed to the root file-system, but are not covered by a known license description:"
      for error in incompleteLicenses:
        print error
      print "Please update: " + os.path.join(ownDir, "licenses.py")
      exitWithError("Inconsistent license information")

    if args.licensesDestDir:
      createAllLicenseFiles(args, packagesOnTarget, ownDir)
      print packagesToJson(processedPackages, args.manifestFile)
    
    if args.packageSourceDestDir:
        try:
            args.preparedPackageRootDir = tempfile.mkdtemp("qca-prepared-package-sources")
            make = [ "make", "target/prepare", "package/prepare", "BUILD_DIR=" + args.preparedPackageRootDir ]
            p = subprocess.Popen(make, cwd=args.qsdkRootDir)
            p.communicate()
            if p.returncode:
              shutil.rmtree(args.preparedPackageRootDir, ignore_errors=True)
              raise Exception("error executing: " + " ".join(make))
            copySourcesTo(args, packagesOnTarget)
        finally:
            shutil.rmtree(args.preparedPackageRootDir, ignore_errors=True)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
    
