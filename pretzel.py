#!/usr/bin/env python
# (c) Jan Dlabal (http://houbysoft.com), 2010.
# provided under the GNU GPL v3 License.

from mncmp import mncmp
from sys import argv
from sys import stdout
from os import system

class Pretzel:
    def __init__(self):
        self.pretzel_keys = []
        print "Loading data... ",
        stdout.flush()
        try:
            if len(argv)==2:
                self.datafile = argv[1]
            else:
                self.datafile = "pretzel.dat"
            f = open(self.datafile)
            str = f.readline()
            while str:
                if str[-1]=='\n':
                    str = str[:-1]
                self.pretzel_keys.append([str[:str.find(':')],str[str.find(':')+1:]])
                str = f.readline()
            print "[done]"
        except:
            self.pretzel_keys.append(['hello','hi'])
            self.pretzel_keys.append(['how are you','fine, thanks'])
            self.pretzel_keys.append(['exit','exit'])
            self.pretzel_keys.append(['quit','quit'])
            print "[failed] (new database will be created after a clean exit)"
        print "Initializing mncmp()... ",
        stdout.flush()
        mncmp("doors","walls") # need to pass anything through it once so that the wordnet dictionnaries get loaded etc.
        print "[done]"

    def flushdb(self):
        f = open(self.datafile,"w")
        for item in self.pretzel_keys:
            f.write(item[0]+":"+item[1]+"\n")
        f.close()

    def panic(self):
        print "I don't know what to do!"
        return raw_input("Please enter desired response (enter text for text reply, or /shell command args to run command with args as response): ")

    def execute(self,cmd):
        if len(cmd)==0:
            return
        if cmd[0]=='/':
            if cmd[1:6]=='shell':
                system(cmd[6:]+"&")
        else:
            print cmd

    def main(self):
        die = False

        while not die:
            user = raw_input("> ")
            success = False
            for item in self.pretzel_keys:
                if mncmp(user,item[0]):
                    success = True
                    if item[1]=='exit':
                        die = True
                    else:
                        self.execute(item[1])
                    break
            if not success:
                self.pretzel_keys.append([user,self.panic()])

        self.flushdb()

p = Pretzel()        
p.main()
