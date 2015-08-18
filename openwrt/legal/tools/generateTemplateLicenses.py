#!/usr/bin/python

import os

f = open('templateLicenses','w')

rootdir = '../../qualcomm/qsdk/build_dir/target-mips_34kc_uClibc-0.9.33.2/'

dirs = [name for name in os.listdir(rootdir)
    if os.path.isdir(os.path.join(rootdir, name))]

dirs = sorted(dirs)

firstLoop = True
for dir in dirs:
    print rootdir + dir
    if firstLoop:
        f.write("packages = [\n")
        f.write('             Package( "%s"\n' % (dir))
        firstLoop = False
    else:
        f.write('           , Package( "%s"\n' % (dir))
    
    f.write('                    , "<version>"\n')
    f.write('                    , "<website>"\n')
    f.write('                    , "%s"\n' % (dir))
    f.write('                    , License ("<license>", "LICENSE")\n')
    f.write('                    , None )\n')

f.write('           ]\n')

f.close()