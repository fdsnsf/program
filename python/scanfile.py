#coding=utf-8

import os 
import sys
import re
def scanfile(searchType, rootDir,s): 
    list_dirs = os.walk(rootDir) 
    for root, dirs, files in list_dirs: 
        #for d in dirs: 
        #    print os.path.join(root, d)  
        for f in files: 
            filename = os.path.join(root, f)
            if searchType == 'filename':
                if filename.find(s) > 0:
                    print filename
                continue
            f = file(filename)
            for line in f:
            	#line = unicode(line, "gb2312")
            	if line.find(s) > 0:
            		 print filename 
            		 break

print sys.argv

if len(sys.argv) >2:
    scanfile(sys.argv[1], sys.argv[2], sys.argv[3])
