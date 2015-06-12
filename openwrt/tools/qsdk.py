#!/usr/bin/python

import sys
import xml.etree.ElementTree as Et
import git
import argparse

currentFunction = []
defaultTheirManifestFile = ".repo/manifest.xml"

def normalizeQsdkPathForOurRemote(name):
    '''
    Simplifies the QSDK repository paths by:
    * Removing the leading quic/qsdk/oss/ path
    * Replacing any remaining '/'-es with underscores for compatibility with git stash
    '''
    return name.replace("quic/qsdk/oss/","").replace("oss/","").replace("/","_")

def abortOnMultipleFunctionOptions(nextFunction):
    if len(currentFunction):
        sys.exit("Cannot combine %s and %s" % (currentFunction[0], nextFunction))
    else:
        currentFunction.append(nextFunction)

def abortOnOurRemoteUnspecified(args):
    if args.ourRemoteRepoName is None:
        sys.exit("Missing mandatory --our-remote-repo-name option")
    if args.ourRemoteRepoRoot is None:
        sys.exit("Missing mandatory --our-remote-repo-root option")
    
def main():
    
    parser = argparse.ArgumentParser(description='QSDK manifest utility')
    parser.add_argument('-f', '--manifest-file-path', dest='theirManifestFile',
                        default=defaultTheirManifestFile,
                        help='path to the QSDK manifest file (defaults: %s)' % defaultTheirManifestFile)
    parser.add_argument('-n', '--our-remote-repo-name', dest='ourRemoteRepoName',
                        default=None,
                        help='our remote repo name used in manifest file')
    parser.add_argument('-r', '--our-remote-repo-root', dest='ourRemoteRepoRoot',
                        default=None,
                        help='our remote repo root URL used in manifest file')
    parser.add_argument('-e', '--our-remote-repo-prefix', dest='ourRemoteRepoPrefix',
                        default="",
                        help='Prefixes to add to each repo used in manifest file')
    parser.add_argument('-u', '--prune-out-projects', dest='theirProjectsToPrune',
                        default="",
                        help='List of source projects to prune (remove)')
    parser.add_argument('-c', '--current-remotes', dest='printCurrentRemotes',
                        default=False, action='store_true',
                        help='Print the current remote name(s)')
    parser.add_argument('-d', '--default-remote', dest='printDefaultRemote',
                        default=False, action='store_true',
                        help='Print the default remote')
    parser.add_argument('-l', '--list', dest='printList',
                        default=False, action='store_true',
                        help='list the QSDK projects (project path, QSDK remote name, and our remote URL)')
    parser.add_argument('-O', '--store-our-manifest', dest='ourNewManifestFile',
                        default=None,
                        help='path to write out manifest file to')
    parser.add_argument('-p', '--print-our-manifest', dest='printOurNewManifest',
                        default=False, action='store_true',
                        help='path to write out manifest file to')
    args = parser.parse_args()

    if args.printDefaultRemote:
        abortOnMultipleFunctionOptions("--default-remote")
    if args.printCurrentRemotes:
        abortOnMultipleFunctionOptions("--current-remotes")
    if args.printList:
        abortOnMultipleFunctionOptions("--list")
        abortOnOurRemoteUnspecified(args)
    if args.ourNewManifestFile:
        abortOnMultipleFunctionOptions("--store-our-manifest")
        abortOnOurRemoteUnspecified(args)
    if args.printOurNewManifest:
        abortOnMultipleFunctionOptions("--print-our-manifest")
        abortOnOurRemoteUnspecified(args)
        
    args.theirProjectsToPrune = args.theirProjectsToPrune.split(" ")

    manifest = Et.ElementTree(file=args.theirManifestFile)
    root = manifest.getroot()

    alreadyHasRemote = False
    theirDefaultRemoteName = None
    currentRemoteNames=[]
    for e in root.findall(".//*"):
        if args.printDefaultRemote:
            if cmp(e.tag, "default") is 0:
                theirDefaultRemoteName = e.attrib["remote"] 
        elif args.printCurrentRemotes:
            if cmp(e.tag, "remote") is 0:
                currentRemoteNames.append(e.attrib)
        elif cmp(e.tag, "remote") is 0:
            if alreadyHasRemote:
                root.remove(e)
            else:
                e.attrib["fetch"] = args.ourRemoteRepoRoot
                e.attrib["name"] = args.ourRemoteRepoName
                if "review" in e.attrib:
                    del e.attrib["review"]
                alreadyHasRemote = True

        elif cmp(e.tag, "default") is 0:
            theirDefaultRemoteName = e.attrib["remote"] 
            e.attrib["remote"] = args.ourRemoteRepoName

        elif cmp(e.tag, "project") is 0:
            if e.attrib["name"] in args.theirProjectsToPrune:
                root.remove(e)
            else:
                theirRemoteName = None
                if "remote" in e.attrib:
                    theirRemoteName = e.attrib["remote"]
                    del e.attrib["remote"]
                else:
                    theirRemoteName = theirDefaultRemoteName
    
                ourLocalProjectPath = e.attrib["path"]
                ourRemotePath = e.attrib["name"] = args.ourRemoteRepoPrefix + normalizeQsdkPathForOurRemote(e.attrib["name"])
                ourRemoteRepo = args.ourRemoteRepoRoot + ourRemotePath
                
                if args.printList:
                    print ourLocalProjectPath, theirRemoteName, ourRemoteRepo
    
    if args.printDefaultRemote:
        print theirDefaultRemoteName
    elif args.printCurrentRemotes:
        for remote in currentRemoteNames:
            print "%s:%s" % (remote["name"], remote["fetch"])
    elif args.ourNewManifestFile:
        manifest.write(args.ourNewManifestFile, encoding="utf-8", xml_declaration=True)
    elif args.printOurNewManifest:
        manifest.write(sys.stdout, encoding="utf-8", xml_declaration=True)
        
    sys.exit(0)

if __name__ == "__main__":
    main()
