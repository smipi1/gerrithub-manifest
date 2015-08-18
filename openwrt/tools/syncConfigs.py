#!/usr/bin/python

import argparse
import sys
import re

class Configs():

    def __init__(self, productConfigFile, developConfigFile, newConfigFile):
        self.productFile = productConfigFile
        self.productConfig = self.parseConfig(self.productFile)
        self.developFile = developConfigFile
        self.developConfig = self.parseConfig(self.developFile)
        self.newFile = newConfigFile
        self.newConfig = self.parseConfig(self.newFile)

    def parseConfig(self, file):
        config={}
        for rawLine in file:
            try:
                key, value = self.getKeyAndValue(rawLine.strip())
                config[key] = value
            except ValueError, e:
                pass
        return config
    
    def getKeyAndValue(self, line):
        p = re.compile(r'^([\w\-]+)=(.+)')
        if not p.match(line):
            raise ValueError("Not a key-value pair: " + line)
        return p.split(line)[1:3]
    
    def update(self):
        self.compareWithNewConfig()
        if len(self.added | self.removed | self.modified) == 0:
            self.printSummary("Nothing modified")
            print
            return
        self.printSummary()
        for key in self.added:
            self.addKey(key)
        for key in self.removed:
            self.removeKey(key)
        for key in self.modified:
            self.modifyKey(key)
        self.printRationale()
        self.writeConfig(self.productFile, self.productConfig)
        self.writeConfig(self.developFile, self.developConfig)
    
    def compareWithNewConfig(self):
        raise NotImplementedError("Abstract method not implemented in base class")
    
    def compareConfigs(self, oldConfig, newConfig):
        oldKeys = oldConfig.viewkeys()
        newKeys = newConfig.viewkeys()
        keyDelta = oldKeys ^ newKeys
        shared = oldKeys & newKeys 
        added = keyDelta & newKeys
        removed = keyDelta & oldKeys
        modified = set()
        for key in shared:
            if not oldConfig[key] == newConfig[key]:
                modified.add(key)
        return (added, removed, modified)

    def printSummary(self, notice=None):
        raise NotImplementedError("Abstract method not implemented in base class")

    def formatSummary(self, oldFilename, pairedFilename, notice=None):
        if notice:
            maxKeyLen=len(notice)
        else:
            maxKeyLen=0
        for key in self.added | self.removed | self.modified:
            maxKeyLen = max(maxKeyLen, len(key))
        self.format = "%%-%ds    %%-%ds    %%-%ds" % (maxKeyLen, len(oldFilename), len(pairedFilename)) 
        print "Summary:"
        print self.format % ("", oldFilename, pairedFilename)
        if notice:
            print self.format % (notice, "-", "-")

    def addKey(self, key):
        raise NotImplementedError("Abstract method not implemented in base class")

    def removeKey(self, key):
        raise NotImplementedError("Abstract method not implemented in base class")

    def modifyKey(self, key):
        raise NotImplementedError("Abstract method not implemented in base class")

    def printRationale(self):
        print
        print "Rationale:"
        print "1. '%s' must always be a sub-set of the '%s'." % (self.productFile.name, self.developFile.name)
        print "2. Both '%s' and '%s' must have consistent configuration values." % (self.productFile.name, self.developFile.name)

    def writeConfig(self, file, config):
        '''
        Writes a config to a file, sorting all keys
        Key sorting ignores case and non-alphanumeric characters
        '''
        def compareKeys(item1, item2):
            '''
            Compares two values ignoring case and non-alphanumeric characters
            '''
            return cmp(item1.lower(), item2.lower())
        
        file.seek(0)
        file.truncate()
        for key in sorted(config, cmp=compareKeys):
            file.write("%s=%s\n" % (key, config[key]))
        file.flush()
        file.close()

class ConfigOnProductChanged(Configs):
    def __init__(self, productConfigFile, developConfigFile, newConfigFile):
        Configs.__init__(self, productConfigFile, developConfigFile, newConfigFile)

    def compareWithNewConfig(self):
        self.added, self.removed, self.modified = self.compareConfigs(self.productConfig, self.newConfig)
    
    def printSummary(self, notice=None):
        self.formatSummary(self.productFile.name, self.developFile.name, notice)
        
    def addKey(self, key):
        self.productConfig[key] = self.newConfig[key]
        oldSum="added"
        if not key in self.developConfig:
            self.developConfig[key] = self.newConfig[key]
            pairedSum="added(1)"
        elif self.developConfig[key] != self.newConfig[key]:
            self.developConfig[key] = self.newConfig[key]
            pairedSum="modified(2)"
        else:
            pairedSum="-"
        print self.format % (key, oldSum, pairedSum)
        
    def removeKey(self, key):
        self.productConfig.pop(key)
        print self.format % (key, "removed", "-")
        
    def modifyKey(self, key):
        self.productConfig[key] = self.newConfig[key]
        oldSum="modified"
        if not key in self.developConfig:
            self.developConfig[key] = self.newConfig[key]
            pairedSum="added(1)"
        elif self.developConfig[key] != self.newConfig[key]:
            self.developConfig[key] = self.newConfig[key]
            pairedSum="modified(2)"
        else:
            pairedSum="-"
        print self.format % (key, oldSum, pairedSum)

class ConfigOnDevelopChanged(Configs):
    def __init__(self, productConfigFile, developConfigFile, newConfigFile):
        Configs.__init__(self, productConfigFile, developConfigFile, newConfigFile)

    def compareWithNewConfig(self):
        self.added, self.removed, self.modified = self.compareConfigs(self.developConfig, self.newConfig)
    
    def printSummary(self, notice=None):
        self.formatSummary(self.developFile.name, self.productFile.name, notice)
        
    def addKey(self, key):
        self.developConfig[key] = self.newConfig[key]
        print self.format % (key, "added", "-")

    def removeKey(self, key):
        self.developConfig.pop(key)
        if key in self.productConfig:
            self.productConfig.pop(key)
            pairedSum="removed(1)"
        else:
            pairedSum="-"
        print self.format % (key, "removed", pairedSum)

    def modifyKey(self, key):
        self.developConfig[key] = self.newConfig[key]
        if (key in self.productConfig) and (self.productConfig[key] != self.newConfig[key]):
            self.productConfig[key] = self.newConfig[key]
            pairedSum="modified(2)"
        else:
            pairedSum="-"
        print self.format % (key, "modified", pairedSum)

def main():
    parser = argparse.ArgumentParser(
        description='Hue QSDK config updater',
        epilog='''
            Changes to either of the QSDK configs (product or development) must be handled consistently.
            In particular, the development config must always include EVERYTHING that is included in the
            product config. Additionally, changes to either of the two configs requires more insight into
            the user's intent. This script prompts the user with a few questions when the config is changed
            to gain an understanding of the user's intent. Susequently, both configs are updated consistently.''')
    parser.add_argument("--product-config", dest="product_config",
                        required=True,
                        type=argparse.FileType("r+"),
                        help="Current product QSDK config file path")
    parser.add_argument("--develop-config", dest="develop_config",
                        type=argparse.FileType("r+"),
                        required=True,
                        help="Current development QSDK config file path")
    parser.add_argument("--new-config", dest="new_config",
                        type=argparse.FileType("r"),
                        required=True,
                        help="New product QSDK config file path")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--product", dest="product",
                        action='store_true',
                        help="New config is a 'product' config")
    group.add_argument("--develop", dest="develop",
                        action='store_true',
                        help="New config is a 'develop' config")
    args = parser.parse_args()

    if args.product:
        ConfigOnProductChanged(args.product_config, args.develop_config, args.new_config).update()
    elif args.develop:
        ConfigOnDevelopChanged(args.product_config, args.develop_config, args.new_config).update()
        
    sys.exit(0)

if __name__ == "__main__":
    main()
