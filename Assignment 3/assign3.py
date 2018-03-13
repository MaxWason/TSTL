# CS 499
#     Professor Alex Groce
#     Assignment #3
#         Test generator
#     Max Wason
#         Detailed comments are below, where my code starts.
#         Do note that it requires numpy, if you don't have it already.

from __future__ import division
from collections import defaultdict
import numpy as np
# 3 NEW IMPORTS!
import sut
import random
import time
import sys

def takeAction(action):
    ok = sut.safely(action)
    checkOk = sut.check()

    if len(sut.newStatements()) > 0:
        print "NEW STATEMENT COVERAGE:"#,time.time(),len(sut.allStatements()),sut.newStatements()        
    if len(sut.newBranches()) > 0:
        print "NEW BRANCH COVERAGE:"#,time.time()-start,len(sut.allBranches()),sut.newBranches()
    
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

"""
Thought processes:

1st (initial) solution:
Simply reset the timer after a given length of steps. Won't get deeply nested bugs (need to use something like bfs), 
but should get most other ones. I arbitrarily chose 50 (as the random tester is fast), as a general number to use.

Code:
# Init variables
LENGTH = 50
step = 0

(In end of while loop)
# Every x actions restart
step += 1 
if step % LENGTH == 0:
    sut.restart()

Works for the basic test case, but is unappealing. I can do much better.


2nd (final) solution:
---------------------
My broad idea was to choose "good" paths semi-randomly, and simply call paths good if the coverage was increased. I wanted to use
randomly choosen actions to improve this, with a possible reset if it seems to stagnate (i.e. not increase coverage 
for a while). It definitely won't get every niche bug, but it should catch most other ones, and do it relatively quickly.

I decided to simply resuse your bfs code, as there's no reason to re-do that, but to alter it to choose actions much more
intelligently. I made a dictionary to hold the weight of each action; an action gets a higher priority/weight simply 
if it increases statement or branch coverage. Then, by using some probability math and randomization, you can choose a likely useful action. 

**
Ideally you're trying to take the action that hasn't happened before that has a good chance of increasing coverage. This is 
one of the most likely way to run into a bug, so it's what you're shooting for in this suite.
**

The probability math was definitely a challenge (it's ridiculous how long it takes to write like 10 LoC), but I think I have good results now. 
I mainly tested with microjson, introducing random bugs, as the simple.tstl was too small to get new coverage. 
It won't find a super obscure bug (whereas something like a neural network would, eventually), 
but is rather intended to lie inbetween that and the basic harness you provided; fast and relatively simple/easy 
but it (intentionally) doesn't have insane depth because of that. The code should be very well commented, so hopefully you can follow it.
"""

# ----------------- My Code Start ----------------------

# The number of actions that will be taken after no new coverage is found before resetting
MAXIMUM_ACTION_LENGTH_BEFORE_RESET = 500
# The following two are for the random number generation:
# Bias is for how much the program should weigh actions with a chance of new coverage when choosing actions
BIAS = .9
# Rand_Multiplier is for how much to randomize the probabilities of choosing actions
RAND_MULTIPLIER = .005
# NOTE: I haven't extensively tested the above params, going to extreme values with them may break everything.


# Your basic initialization
actionCount = defaultdict(lambda:0) # For -> action:timesUsed
actionCoverageWeight = defaultdict(lambda:1) # For -> action:timesMadeNewCoverage
resetCounter = 0 # For resetting the entire thing (so as to avoid getting "stuck"); and randomization bails us out

# ------------------ Probability Functions -------------------------

# Generates a list of probabilites with bias towards first element
# Ex: [.52, .27, .13, .06, .02, .012, .003, 0.0006, ...]
# -------
# Params:
# someLen = Length of probability spectrum to generate
# myList = List to hold probabilites of choosing elements
# bias = The strength of the bias towards the first element (1 is 100%, .5 is half that, 0 is no bias)
def genProbabilityList(someLen, myList, bias):

    # Generate relative weights individually (exponential-ish distribution overall)
    for i in xrange(someLen):
        # Some magic with numbers to get the general spread desired
        x = (bias * (i+1/someLen)) * i 
        # Randomize the results a little, weighted towards the size of each element to increase the exponentially curving nature of the distribution
        x *= 1 + R.uniform(0, (x * RAND_MULTIPLIER)) 
        # Add the generated number to the list
        myList.append(x)

    # Normalize to a scale of 0.0 to 1.0
    s = sum(myList) 
    norm = [float(i)/s for i in myList] 

    # Reverse the list, so that the first element is most likely 
    return sorted(norm, reverse = True) 


# Get a random int in the range 0 to someLen, using the probability spread in weightedList
def genRandomWithBias(someLen, weightedList):
    # Return a "random" int as an index from 0 to someLen, with the probability spectrum defined by weightedList
    decision = np.random.choice(someLen, p=weightedList)
    return int(decision)

# --------------- Main Code Loop ----------------------

# Loop until timeout
while (time.time() - start) < timeout:
    
    # Increment counter
    resetCounter += 1    
    
    # Utilize your bfs code for searching for least used actions (initially)
    actions = sut.enabled()
    R.shuffle(actions)
    
    sortActions = sorted(actions, key = lambda x: actionCount[sut.serializable(x)])

    # Sort again to prioritize actions that increase coverage 
    weightedActions = sorted(sortActions, key = lambda x: actionCoverageWeight[sut.serializable(x)], reverse = True)

    # Generate an intelligent index, biased towards 0, randomly (for prioritizing possible new coverage)
    # - Regenerate the distribution, have to do so here in the main loop due to sut.enabled()'s length changing
    weightedProbabilityList = genProbabilityList(len(sut.enabled()), list(), BIAS) 
    # - Get a random index using the values generated in the previous call
    biasedIndex = genRandomWithBias(len(weightedActions), weightedProbabilityList) 

    # Use the "smart" index to get an action
    action = weightedActions[biasedIndex]
    saction = sut.serializable(action)

    # if coverage increase (branch or statement), increase weight of action and reset resetCounter timer to 0
    if ((len(sut.newStatements())) > 0 or (len(sut.newBranches()) > 0)):
        actionCoverageWeight[saction] += 1
        resetCounter = 0

    print saction, actionCount[saction], actionCoverageWeight[saction] # Print statement for showing the actions, if desired
    
    # Actually call the action and increase it's usage count
    takeAction(action)
    actionCount[saction] += 1

    # check resetCounter timer (time since last coverage increase), if larger than x -> restart
    if (resetCounter > MAXIMUM_ACTION_LENGTH_BEFORE_RESET):
        sut.restart()

# -------------------- End My Code ---------------------

# DO NOT MODIFY CODE BELOW HERE, WE ALWAYS WANT A FULL COVERAGE REPORT WHEN WE DON'T FIND ANY BUGS
    
sut.internalReport()
sys.exit(0)