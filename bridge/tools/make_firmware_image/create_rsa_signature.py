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

###########################################################################################################################################################
def main():
    parser = argparse.ArgumentParser(description='Generate signature ')
    parser.add_argument('-keyname', help='Name used in the generated file names')
    parser.add_argument('-inFile', help='Input file to encrypt')
    args = parser.parse_args()
        
    keyname = args.keyname
    inFile = args.inFile

    pwd = os.path.dirname(os.path.abspath(__file__))
    privKey = pwd + "/certs/RSA_" + keyname + ".pem";
    command = "openssl dgst -sha256 -sign " + privKey + " -out " + inFile + ".sign " + inFile
    #print command
    call(command, shell=True)
    
if __name__ == '__main__':
    main()
