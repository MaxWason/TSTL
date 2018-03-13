# Your name and other comments about your code

import sut
import random
import time
import sys
from collections import defaultdict
# (can add other Python standard library imports you need)

def takeAction(action):
    ok = sut.safely(action)
    checkOk = sut.check()

    if len(sut.newStatements()) > 0:
        print "NEW STATEMENT COVERAGE:",time.time(),len(sut.allStatements()),sut.newStatements()        
    if len(sut.newBranches()) > 0:
        print "NEW BRANCH COVERAGE:",time.time()-start,len(sut.allBranches()),sut.newBranches()
    
    if (not ok) or (not checkOk):
        print "FAILED TEST"
        sut.prettyPrintTest(sut.test())
        sut.saveTest(sut.test(),"failure.test")
        sys.exit(255)

timeout = int(sys.argv[1])
start = time.time()

sut = sut.sut()

sut.setDebugSafelyMode(True)

R = random.Random(sys.argv[2])

# only command line arguments are 1) how long to test and 2) a random number seed for reproducibility

# DO NOT MODIFY CODE ABOVE HERE, EXCEPT TO ADD MORE IMPORTS!

# You can add code here, to set up any data structures you need

LENGTH = 5

count = defaultdict(lambda:0)
step = 0

while (time.time() - start) < timeout:
    # Your method for choosing actions goes here
    step += 1    
    
    actions = sut.enabled()
    R.shuffle(actions)
    
    sortActions = sorted(actions, key = lambda x: count[sut.serializable(x)])

    action = sortActions[0]
    saction = sut.serializable(action)

    # print saction,count[saction]
    takeAction(action)
    count[saction] += 1

    if step % LENGTH == 0:
        sut.restart()
    
# DO NOT MODIFY CODE BELOW HERE, WE ALWAYS WANT A FULL COVERAGE REPORT WHEN WE DON'T FIND ANY BUGS
    
sut.internalReport()
sys.exit(0)
