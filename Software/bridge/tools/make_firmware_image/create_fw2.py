#!/usr/bin/python

import os
import sys
import hashlib
import hmac
import binascii
import re
import argparse
from subprocess import call

###########################################################################################################################################################
'''
    Firmware creation class
'''
class firmware:
    def __init__(self, name=None, variant='dev', product='BSB002', versionFile=None):
        self.name = name
        self.files = 0
        self.size = 34             # Size of header, not including signature
        self.product = product
        self.variant = variant
        self.version = 'local'
        self.writer = ''
        self.location = 34
        self.content = [0] * (10 * 1024 * 1024)
        if 'BUILD_MACHINE_NAME' in os.environ:
            self.builder = os.environ['BUILD_MACHINE_NAME']
        elif 'USERNAME' in os.environ:
            self.builder = os.environ['USERNAME']
        else:
            self.builder = os.environ['LOGNAME']

        if self.variant == 'dev':
            self.key='dev_01'
        elif self.variant == 'prod':
            self.key='prod_01'
        else:
            raise Exception("Unsuported variant")
   
        if versionFile<>None:
            self.version = self.getSvnVersion(versionFile);
        
        print "Using version: " + self.version
        print "Using key signature: " + self.getKeyFileName()

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
        if size <> None:
            strlen = size
        for i in range(strlen):
            if i < len(value):
                self.write(ord(value[i]))
            else:
                self.write(0)
        
    def create_signature(self, fileToSign):
        #print "Create signature for {0} with key {1}".format(fileToSign, self.key)
        pwd = os.path.dirname(os.path.abspath(__file__))
        
        cmd = "python " + pwd + os.sep + "create_rsa_signature.py -inFile " + fileToSign +" -keyname " + self.key;
        retcode = call(cmd, shell=True)
        if retcode <> 0:
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
        
    def store(self, name=None):
        self.addPublicKey()    

        outfile = self.name
        if name <> None:
            outfile = name
        if name == None:
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

    def readFile(self, file_image):
        content=open(file_image, "rb").read()
        size = os.path.getsize(file_image)
        return (content, size)
        

    def getFullFileNameInCertDir(self, fileName):
        pwd = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(pwd, 'certs', fileName)
        

    def encryptContainerFile(self, file_image):
        print "Encrypting {0}".format(file_image)
        
        file_image_enc = file_image + '.enc'
        pwd = os.path.dirname(os.path.abspath(__file__))

        retcode = call(os.path.join(pwd, "aes-256-cbc.sh") + " -e -k " + self.getFullFileNameInCertDir('enc.k') + " -f " + file_image +" -o "+  file_image_enc, shell=True)
        if retcode <> 0:
            raise Exception("Encyption error")

        content, size = self.readFile(file_image_enc);
        os.remove(file_image_enc);
        return (content, size);

    def getSvnVersion(self, versionFile):
        #use 'svn info > revision.txt' to generate a test file
        try:
            revNr = 0
            (content, size) = self.readFile(versionFile)
            if content.isdigit():
                revNr = content
            else:
                p = re.compile(ur'Last Changed Rev:\s(\d+)\s')
                m = re.search(p, content)
                revNr = m.group(1)
            return "01" + '{:0>6}'.format(revNr)
        except:
            print "Error reading version file, use 'local'"
            return "local"

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

    def getPublicKeyFileName(self):
        pwd = os.path.dirname(os.path.abspath(__file__))
        return pwd + os.sep + "certs" + os.sep +"RSA_" + self.key + "_pub.pem";

    def getKeyFileName(self):
        pwd = os.path.dirname(os.path.abspath(__file__))
        return pwd + os.sep + "certs" + os.sep +"RSA_" + self.key + ".pem";
    
    def addPublicKey(self):
        file_image = self.getPublicKeyFileName();
        hwid = 0x00FE
        flags = 0x00000000;
        (content, size) = self.readFile(file_image)
        version=self.key;
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
    parser = argparse.ArgumentParser(description='Create firmware file for Linux beased bridges')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-dev', dest='variant', action='store_const', const='dev', help='use development key')
    group.add_argument('-prod', dest='variant', action='store_const', const='prod', help='use production key')
    parser.add_argument('-out', help='Output filename, if not provided default name is chosen')
    parser.add_argument('-allowdowngrading', action='store_true', help='allow downgrading')
    parser.add_argument('-nofactorynew', action='store_true', help='force resetting to factory new')
    parser.add_argument('-nowhitelist', action='store_true', help='do not require a whitelist entry')
    parser.add_argument('-noreboot', action='store_true', help='do not execute a reboot after transfer of firmware')
    parser.add_argument('-allowcommissioninginterface', action='store_true', help='Allow use of commissioning commands on test interface')
    parser.add_argument('-allowfactoryinterface', action='store_true', help='Allow use of factory (VTech and LiteOn) commands on test interface')
    parser.add_argument('-allowtestinterface', action='store_true', help='Allow use of test commands on test interface')
    parser.add_argument('-product', help='Set product variant, default = BSB002')
    parser.add_argument('-versionFile', help='Path of svn-info revision file with ("Last Changed Rev: xxxx") used for version in content file. !Only use on build server!')
    parser.add_argument('files', nargs=argparse.REMAINDER, help='files to add')
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()
    
    variant = 'dev'
    if args.variant <> None:
        variant = args.variant
   
    product = 'BSB002'
    if args.product <> None:
        product = args.product;
    
    fw = firmware(variant=variant, product=product, versionFile=args.versionFile)

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

    if flags <> 0:
        fw.addSpecialFlagsContainer(flags)
    elif args.files <> None:
        for file in args.files:
            fw.add(file_image=file)
    
    fw.store(args.out)

if __name__ == '__main__':
    main()
