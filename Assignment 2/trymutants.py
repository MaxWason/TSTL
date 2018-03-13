import subprocess
import glob
import os
import sys
import shutil
import random

# change this to "tstl_rt" if you have it installed on your system
# otherwise, change this path to wherever your tstl files are
# python ~/tstl/generators/randomtester.py
tstl_rt = "tstl_rt"

make_logs = 0

dnull = open(os.devnull,'w')

rlist = glob.glob("mutants/*_mutant_*.py")
random.shuffle(rlist)

tried = 0
killed = 0.0

attempted = []
try:
    for l in open("attempted.txt"):
        attempted.append(l[:-1])
except IOError:
    pass

attemptf = open("attempted.txt",'a')

for f in rlist:
    fdir = f.replace("mutants/","faults_").replace(".py","")
    tried += 1
    if os.path.exists(fdir):
        print "ALREADY ANALYZED AND KILLED\n"
        killed += 1
        continue
    if f in attempted:
        print "ALREADY ANALYZED AND NOT KILLED\n",
        continue
    print "MUTANT #",tried, ":", f
    shutil.copy(f,"microjson.py")
    if os.path.exists("microjson.pyc"):
        os.remove("microjson.pyc")
    subprocess.call(["rm -rf *.test"],shell=True,stdout=dnull,stderr=dnull)
    r = subprocess.call(["ulimit -t 400; " + tstl_rt + " --progress"],shell=True,stderr=dnull,stdout=dnull)
    if r == 152:
        subprocess.call(["cp currtest.test timeout.test"], shell=True)
        print "TIMEOUT (PROBABLE NON-TERMINATING LOOP DUE TO MUTANT)"
    try:
        os.remove("currtest.test")
    except:
        pass

    if glob.glob("*.test") != []:
        print "MUTANT KILLED"
        if make_logs == True:
            os.mkdir(fdir)
            subprocess.call(["mv *.test " + fdir + "/"],shell=True,stderr=dnull,stdout=dnull)
            shutil.copy(f,fdir+"/")
        killed += 1
    try:
        shutil.copy("originalmicrojson.py","microjson.py")
    except:
        pass

    print tried,"MUTANTS ANALYZED, KILL RATE:",killed/tried, "KILLED:", killed
    print "="*50
    attemptf.write(f+"\n")
    sys.stdout.flush()
    attemptf.flush()

attemptf.close()
