#!/usr/bin/python

import os
import tempfile
import sys
import hashlib
import hmac
import binascii
import re
import argparse
import shutil

from subprocess import call

###########################################################################################################################################################

'''
    Firmware creation class
'''
class firmware:
    def __init__(self, priKey=None, product='BSB002', versionFile=None, allowLocalVersion=False, encKey=None):
        self.files = 0
        self.size = 34             # Size of header, not including signature
        self.product = product
        self.version = 'local'
        self.writer = ''
        self.location = 34
        self.content = [0] * (10 * 1024 * 1024)
        self.allowLocalVersion = allowLocalVersion
        self.encKey = encKey
        
        self.priKey = priKey
        if 'BUILD_MACHINE_NAME' in os.environ:
            self.builder = os.environ['BUILD_MACHINE_NAME']
        elif 'USERNAME' in os.environ:
            self.builder = os.environ['USERNAME']
        else:
            self.builder = os.environ['LOGNAME']
   
        if versionFile!=None:
            self.version = self.getSvnVersion(versionFile)

        print "Using version: " + self.version
        print "Using private key: " + self.priKey
        print "Using encryption key: " + self.encKey
        print "Using builder: " + self.builder

    ''' Set write location
        Updates size of firmware as well
    '''
    def setlocation(self, location):
        self.location = location
        if (self.location > self.size):
            self.size = self.location
    
    ''' Write data into firmware
        Auto increment location
    '''
    def write(self, value):
        self.content[self.location] = value
        self.setlocation(self.location + 1)

    def write_u16(self, value):
        self.write( (value >> 8) & 255)
        self.write( (value     ) & 255)

    def write_u32(self, value):
        self.write( (value >> 24) & 255)
        self.write( (value >> 16) & 255)
        self.write( (value >>  8) & 255)
        self.write( (value      ) & 255)

    def write_string(self, value, size=None):
        strlen = len(value)
        if size != None:
            strlen = size
        for i in range(strlen):
            if i < len(value):
                self.write(ord(value[i]))
            else:
                self.write(0)
        
    def create_signature(self, fileToSign):
        pwd = os.path.dirname(os.path.abspath(__file__))
        cmd = "openssl dgst -sha256 -sign " + self.priKey + " -out " + fileToSign + ".sign " + fileToSign
        retcode = call(cmd, shell=True)
        if retcode != 0:
            raise Exception("RSA signature error")

    def update_header(self):
        self.setlocation(0)
        self.write_string(self.product)
        self.write(0)
        self.write(self.files)
        self.write_u32(self.size)

        # get the name of the build machine for an official build, the windows user name for a local build
        self.write_string(value=self.builder, size=22)
            
        self.setlocation(34)
        print "Create header"
        print "  files = {0}".format(self.files)
        print "  size = {0}".format(self.size)
        print "  builder = {0}".format(self.builder)
        
    def CreatePublicKey(self):
        self.pubKey = os.path.join(self.tmpDir, "pubkey.pem")
        command = "openssl rsa -pubout -inform  pem -in {0} -outform pem -out {1} ".format(self.priKey, self.pubKey);
        retcode = call(command, shell=True)
        if retcode != 0:
            raise Exception("Encyption error")

    def store(self, name=None):
        self.tmpDir = tempfile.mkdtemp()
        self.CreatePublicKey()
        self.addPublicKey()    

        if name != None:
            outfile = name
        else:
            outfile = "{0}_test.fw2".format(self.product)
            
        print "Make firmware data {0}".format(outfile)
        self.update_header()
        
        #save
        with open(outfile + '.tmp', 'wb') as f_filename:
            f_filename.write(bytearray(self.content[0:self.size]))

        #sign
        self.create_signature(outfile + '.tmp');
        content_sign = open(outfile + '.tmp.sign').read()
        os.remove(outfile + '.tmp')
        os.remove(outfile + '.tmp.sign')
        
        #append
        with open(outfile, 'wb') as f_filename:
            f_filename.write(bytearray(self.content[0:self.size]))
            f_filename.write(bytearray(content_sign))

        shutil.rmtree(self.tmpDir)

    def readFile(self, file_image):
        content=open(file_image, "rb").read()
        size = os.path.getsize(file_image)
        return (content, size)

    def encryptContainerFile(self, file_image):
        print "Encrypting {0}".format(file_image)
        
        file_image_enc = file_image + '.enc'
        pwd = os.path.dirname(os.path.abspath(__file__))
        command="bash " + os.path.join(pwd, "aes-256-cbc.sh") + " -e -k " + self.encKey + " -f " + file_image +" -o "+  file_image_enc
    
        print command

        retcode = call(command, shell=True)
        if retcode != 0:
            raise Exception("Encyption error")

        content, size = self.readFile(file_image_enc);
        os.remove(file_image_enc);
        return (content, size);

    def getSvnVersion(self, versionFile):
        #use 'svn info > revision.txt' to generate a test file
        try:
            revNr = 0
            (content, size) = self.readFile(versionFile)
            content = content.strip()
            if content.isdigit():
                revNr = content
            return "01" + '{:0>6}'.format(revNr)
        except:
            if (self.allowLocalVersion):
                print "Error reading version file, using 'local' (allowed by -allowLocalVersion)"
                return "local"
            raise Exception("Version error")

    def addContainer(self, content, size, hwid, flags, version):
        self.setlocation(self.size)
        self.write_u32(size)
        self.write_u16(hwid)
        self.write_u32(flags)
        self.write_string(value=version, size=16)
        
        for i in range(size):
            self.write(content[i])

        self.files = self.files + 1

    def addSpecialFlagsContainer(self, flags):
        hwid=0x00FF
        content = []
        size = 0
        version="01999999"
        print "Adding special flags   (hwid: 0x{1:04X}, size: {0}, version: '{2}')".format(size, hwid, version)
        self.addContainer(content, size, hwid, flags, version)

    def addFileGz(self, file_image):
        hwid = 0x0103
        (content, size) = self.encryptContainerFile(file_image);
        flags = 0x00000000;
        version=self.version;
        print "Adding content file    (hwid: 0x{2:04X}, size: {1}, version: '{3}', filename: {0}".format(os.path.basename(file_image), size, hwid, version)
        self.addContainer(content, size, hwid, flags, version)

    
    
    def addPublicKey(self):
        file_image = self.pubKey
        hwid = 0x00FE
        flags = 0x00000000;
        (content, size) = self.readFile(file_image)
        version=self.version;
        print "Adding public key file (hwid: 0x{2:04X}, size: {1}, version: '{3}', filename: {0}".format(os.path.basename(file_image), size, hwid, version)
        self.addContainer(content, size, hwid, flags, version)

    def add(self, file_image):
        filename, extention = os.path.splitext(file_image)

        if extention == '.gz':
            self.addFileGz(file_image)
        else:
            raise Exception("Unsupported file")

    
###########################################################################################################################################################
def main():

    if not sys.platform.startswith("linux"):
        sys.exit("Error: Run this application only on Linux")

    parser = argparse.ArgumentParser(description='Create firmware file for Linux beased bridges')
    parser.add_argument('-out', help='Output filename, if not provided default name is chosen')
    parser.add_argument('-priKey', help='Path of the private the key to use, default ./certs/RSA_dev_01.pem')
    parser.add_argument('-allowdowngrading', action='store_true', help='allow downgrading')
    parser.add_argument('-nofactorynew', action='store_true', help='force resetting to factory new')
    parser.add_argument('-nowhitelist', action='store_true', help='do not require a whitelist entry')
    parser.add_argument('-noreboot', action='store_true', help='do not execute a reboot after transfer of firmware')
    parser.add_argument('-allowcommissioninginterface', action='store_true', help='Allow use of commissioning commands on test interface')
    parser.add_argument('-allowfactoryinterface', action='store_true', help='Allow use of factory (VTech and LiteOn) commands on test interface')
    parser.add_argument('-allowtestinterface', action='store_true', help='Allow use of test commands on test interface')
    parser.add_argument('-allowLocalVersion', action='store_true', help='Allow to use "local version" when reading versionFile fails')
    parser.add_argument('-product', help='Set product variant, default = BSB002')
    parser.add_argument('-versionFile', help='Path of svn-info revision file with ("Last Changed Rev: xxxx") used for version in content file. !Only use on build server!')
    parser.add_argument('-encKey', help='path to image encryption key, default ./certs/enc.k')
    parser.add_argument('files', nargs=argparse.REMAINDER, help='files to add')
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()
   
    pwd = os.path.dirname(os.path.abspath(__file__))

    priKey = os.path.join(pwd, "certs", "RSA_dev_01.pem")
    if args.priKey != None:
        priKey = args.priKey

    encKey = os.path.join(pwd, "certs", "enc.k")
    if args.encKey != None:
        encKey = args.encKey

    product = 'BSB002'
    if args.product != None:
        product = args.product;
    
    fw = firmware(priKey=priKey, product=product, versionFile=args.versionFile, allowLocalVersion=args.allowLocalVersion, encKey=encKey)

    flags = 0
    if args.allowdowngrading == True:
        flags = flags | (1 << 0)
    if args.nofactorynew == True:
        flags = flags | (1 << 1)
    if args.nowhitelist == True:
        flags = flags | (1 << 2)
    if args.noreboot == True:
        flags = flags | (1 << 3)
    if args.allowcommissioninginterface == True:
        flags = flags | (1 << 4)
    if args.allowfactoryinterface == True:
        flags = flags | (1 << 5)
    if args.allowtestinterface == True:
        flags = flags | (1 << 6)

    if flags != 0:
        fw.addSpecialFlagsContainer(flags)
    else:
        if args.files == None or len(args.files) == 0:
            raise Exception("No firmware given to pack into .fw2 file")

        for file in args.files:
            fw.add(file_image=file)
    
    fw.store(args.out)

if __name__ == '__main__':
    main()