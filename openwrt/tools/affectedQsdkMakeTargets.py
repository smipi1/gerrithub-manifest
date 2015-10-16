#!/usr/bin/python

import sys, os, re, subprocess, argparse

toolsPath = os.path.dirname(sys.argv[0])
openwrtPath = os.path.abspath(os.path.join(toolsPath, "..")) 
qsdkPath = os.path.join(openwrtPath, "qualcomm", "qsdk")
ubootPath = os.path.join(qsdkPath, "qca", "src", "qca-legacy-uboot")

def defaultPath(path):
    return os.path.relpath(path, os.path.curdir)

def modifiedGitPaths(gitDir, reference, commit=None):
    paths = []
    args = ["git", "diff", "--name-status", reference]
    if commit:
        args.append(commit)
    p = subprocess.Popen(args, cwd=gitDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    git_stdout, git_stderr = p.communicate()
    for change in git_stdout.splitlines():
        paths.append(change.split("\t")[1])
    if not p.returncode is 0:
        sys.stderr.write("error calling '" " ".join(args) + "' from '" + gitDir + "':\n" + git_stderr)
        sys.exit(p.returncode)
    return paths

def hasLinesStartingWith(filepath, match):
    for l in open(filepath).readlines():
        if l.find(match) >= 0:
            return True
    return False 
    
def findQsdkMakeTargets(qsdkPath, modifiedPaths):
    targets={}
    for p in modifiedPaths:
        dir = os.path.dirname(p)
        while dir:
            makefile = os.path.join(dir, "Makefile")
            makefilePath = os.path.join(qsdkPath, makefile)
            if os.path.exists(makefilePath) and not hasLinesStartingWith(makefilePath, "BOARD:="):
                if not targets.has_key(dir):
                    targets[dir] = []
                targets[dir].append(p)
                break
            dir = os.path.dirname(dir)
    return targets
    
def main():
    
    parser = argparse.ArgumentParser(description='Determines which QSDK make targets are affected between two git commits')
    parser.add_argument('reference', metavar='reference',
                        help='reference git commit')
    parser.add_argument('commit', metavar='commit', nargs='?',
                        default=None,
                        help='commit to compare with (default: compare with work directory)')
    parser.add_argument('-o', '--openwrt-path', dest='openwrtPath',
                        default=openwrtPath,
                        help='path to the Hue openwrt directory (defaults: %s)' % defaultPath(openwrtPath))
    parser.add_argument('-q', '--qsdk-path', dest='qsdkPath',
                        default=qsdkPath,
                        help='path to the QSDK root (defaults: %s)' % defaultPath(qsdkPath))
    parser.add_argument('-u', '--uboot-path', dest='ubootPath',
                        default=ubootPath,
                        help='path to the QSDK u-boot feed (defaults: %s)' % defaultPath(ubootPath))
    args = parser.parse_args()

    modifiedPaths = modifiedGitPaths(args.qsdkPath, args.reference, args.commit)
    targets = findQsdkMakeTargets(args.qsdkPath, modifiedPaths)
    for t in targets:
        print t

if __name__ == "__main__":
    main()
