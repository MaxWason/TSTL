import sut
import random

sut = sut.sut()
r = random.Random()

print "WHAT ACTIONS DOES IT HAVE?"
sut.prettyPrintTest(sut.actions()) # prints all the actions this SUT has

print "WHAT ENABLED ACTIONS DOES IT HAVE?"
sut.prettyPrintTest(sut.enabled()) # prints all the actions this SUT has

sut.safely(sut.enabled()[0]) # Just do the first action

print "NOW WHAT ENABLED ACTIONS DOES IT HAVE?"
sut.prettyPrintTest(sut.enabled()) # prints all the actions this SUT has

sut.safely(sut.enabled()[0]) # Just do the first action enabled, again

print "THE TEST IS:"
sut.prettyPrintTest(sut.test())

print "NOW WHAT ENABLED ACTIONS DOES IT HAVE?"
sut.prettyPrintTest(sut.enabled()) # prints all the actions this SUT has

print "WE CAN ALSO DO A RANDOM ACTION:"

sut.safely(sut.randomEnabled(r))

print "THE TEST IS:"
sut.prettyPrintTest(sut.test())


# Now let's generate a random test and (assuming it fails) reduce and then normalize it

(t,didFail) = sut.makeTest(100,r)

if not didFail:
   print "IT DIDN'T FAIL, SADLY!"
else:
    print "FAILING (WE HOPE) TEST"
    sut.prettyPrintTest(t)

    r = sut.reduce(t,sut.failsCheck)

    print "REDUCED TEST"
    sut.prettyPrintTest(r)


    n = sut.normalize(r,sut.failsCheck)
    
    print "NORMALIZED TEST"
    sut.prettyPrintTest(n)
