#!/usr/bin/env python
# (c) Jan Dlabal (http://houbysoft.com), 2010.
# provided under the GNU GPL v3 License.

from argmatch import *
from sys import argv
from sys import stdout
from os import system
import readline
from cmd import Cmd

class Pretzel(Cmd):
    def __init__(self,verbose=False):
        self.models = []
        self.prompt = '> '
        self.completekey = None
        self.cmdqueue = []
        self.stop = False
        self.stdout = stdout
        self.minsim = 0.34
        self.verbose = verbose
        print "Loading data... ",
        stdout.flush()
        try:
            if len(argv)==2:
                self.datafile = argv[1]
            else:
                self.datafile = "pretzel.dat"
            f = open(self.datafile)
            str = f.readline()
            while str and len(str) is not 0:
                if str[-1]=='\n':
                    str = str[:-1]
                self.models.append([Model(str[:str.find(':')]),str[str.find(':')+1:]])
                str = f.readline()
            print "[done]"
        except:
            self.models.append([Model('hello'),'hi'])
            self.models.append([Model('how are you'),'fine, thanks'])
            self.models.append([Model('exit'),'exit'])
            self.models.append([Model('quit'),'quit'])
            print "[failed] (new database will be created in pretzel.dat after a clean exit (type exit to do that))"
        print "Initializing argmatch()... ",
        stdout.flush()
        argmatch(Model("doors"),"walls") # need to pass anything through it once so that the wordnet dictionnaries get loaded etc.
        print "[done]"

    def flushdb(self):
        f = open(self.datafile,"w")
        for item in self.models:
            f.write(item[0].getsentence()+":"+item[1]+"\n")
        f.close()

    def panic(self):
        print "I don't know what to do!"
        return raw_input("Please enter desired response (simple text, /shell command, or /python command): ")

    def execute(self,cmd):
        if len(cmd)==0:
            return
        if cmd=='exit' or cmd=='quit':
            self.stop = True
            return
        if cmd[0]=='/':
            if cmd[1:7]=='shell ':
                if self.verbose:
                    print "Shell : "+cmd[7:]
                system(cmd[7:])
            elif cmd[1:8]=='python ':
                if self.verbose:
                    print "Python : "+cmd[8:]
                exec(cmd[8:])
        else:
            print cmd

    def postcmd(self, stop, line):
        return self.stop

    def do_help(self, args):
        self.default('help '+args)

    def arg_translate(self, arg, recursive=False):
        success = False
        for item in self.models:
            args = argmatch(item[0],arg) #mncmp(arg,item[0],self.minsim)
            itemtmp = item[1]
            if args is not False:
                if args is not True:
                    # means we have some arguments
                    for arg in args:
                        itemtmp = itemtmp.replace(arg[0],self.arg_translate(arg[1],True))
                success = True
                if not recursive:
                    self.execute(itemtmp)
                else:
                    return itemtmp
                break
        if not success:
            if recursive:
                return arg
            else:
                cmd = self.panic()
                if cmd!="":
                    self.models.append([Model(arg),cmd])
                else:
                    print "Received empty input; not adding to database."

    def default(self, user):
        self.arg_translate(user)
        self.flushdb()

p = Pretzel()
p.cmdloop()
