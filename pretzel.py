#!/usr/bin/env python
# (c) Jan Dlabal (http://houbysoft.com), 2010.
# provided under the GNU GPL v3 License.

from mncmp import mncmp
from sys import argv
from sys import stdout
from os import system

pretzel_keys = []

def pretzel_init():
    print "Loading data... ",
    stdout.flush()
    try:
        if len(argv)==2:
            f = open(argv[1],"r")
        else:
            f = open("pretzel.dat","r")
        str = f.readline()
        while str:
            if str[-1]=='\n':
                str = str[:-1]
            pretzel_keys.append([str[:str.find(':')],str[str.find(':')+1:]])
            str = f.readline()
        print "[done]"
    except:
        pretzel_keys.append(['hello','hi'])
        pretzel_keys.append(['how are you','fine, thanks'])
        pretzel_keys.append(['exit','exit'])
        pretzel_keys.append(['quit','quit'])
        print "[failed] (new database will be created after a clean exit)"
    print "Initializing mncmp()... ",
    stdout.flush()
    mncmp("doors","walls") # need to pass anything through it once so that the wordnet dictionnaries get loaded etc.
    print "[done]"

def pretzel_flushdb():
    if len(argv)==2:
        f = open(argv[1],"w")
    else:
        f = open("pretzel.dat","w")
    for item in pretzel_keys:
        f.write(item[0]+":"+item[1]+"\n")
    f.close()

def pretzel_panic():
    print "I don't know what to do!"
    return raw_input("Please enter desired response (enter text for text reply, or /shell command args to run command with args as response): ")

def pretzel_exec(cmd):
    if len(cmd)==0:
        return
    if cmd[0]=='/':
        if cmd[1:6]=='shell':
            system(cmd[6:]+"&")
    else:
        print cmd

def pretzel_main():
    pretzel_init()
    die = False

    while not die:
        user = raw_input("> ")
        success = False
        for item in pretzel_keys:
            if mncmp(user,item[0]):
                success = True
                if item[1]=='exit':
                    die = True
                else:
                    pretzel_exec(item[1])
                break
        if not success:
            pretzel_keys.append([user,pretzel_panic()])

    pretzel_flushdb()
                
pretzel_main()
