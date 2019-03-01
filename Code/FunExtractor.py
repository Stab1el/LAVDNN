# -*- coding: utf-8 -*-

import os
import re
import sys
dict=[]
root_dir = sys.argv[1]    # The folder of target programs
out_putfile=sys.argv[2]   # The output file

for dirpath,dirnames,filenames in os.walk(root_dir):
    for filepath in filenames:
        FILE=os.path.join(dirpath,filepath)


        ## python FILE
        if '.py' in filepath:
            f=open(FILE,'r',encoding='UTF-8')
            list=f.readlines()
            for line in list:
                line=line.rstrip('\n')
                if 'def' in line:
                    if '(' in line:
                        if line[-1]==':':
                            line=line.split()[1].split('(')[0]
                            if func != '' and func not in dict:
                                dict.append(func)

            f.close()
        ## C FILE
        if '.cpp' in filepath or '.c' in filepath:
            f = open(FILE, 'r', encoding='UTF-8')
            list = f.readlines()
            for line in list:
                line = line.rstrip('\n')
                line = line.rstrip(';')
                if 'void ' in line or 'int ' in line or 'char' in line or 'const' in line or 'double' in line:
                #    print (line.split()[0])
                        if '(' in line:
                            if line[0]!='' and line[0]!=' ':
                                if not '=' in line:
                                    blocks=line.split()
                                    for b in blocks:
                                        if '(' in b:
                                            func=b.split('(')[0]
                                            if '::' in func:
                                                func=func.replace('::','_')
                                            if func!='' and func not in dict:
                                                dict.append(func)
            f.close()

with open(out_putfile,'w') as f:
    for line in dict:
        f.write(line)
        f.write('\n')


