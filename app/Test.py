"""Make sneakysnake run again.

    This will be a hotbed for exhaustive testing on the different classes
    and their independent functions."""


from Snake import Snake

NUM_CASES = 13
current_case = 0

def Snake_test_1():
    """Test basic .getX and .setX functionality."""
    print 'Testing .getX using init'
    init_params = [2, [[0, 1], [1, 1]], 75, 's1']
    s1 = Snake(init_params[0], init_params[1], init_params[2], init_params[3])

    # test .toString()
    # I am sorry this test is gross.
    testCase(s1.toString(), "identifer: " + str(init_params[3]) + "\n\
health: " + str(init_params[2]) + "\n\
size: " + str(init_params[0]) + "\n\
state: unknown\n\
positions: " + str(init_params[1]), 0)
    testCase(s1.getState(), 'unknown', 1)
    testCase(s1.getHealth(), init_params[2], 2)
    testCase(s1.getSize(), init_params[0], 3)
    testCase(s1.getHeadPosition(), init_params[1][0], 4)
    testCase(s1.getAllPositions(), init_params[1], 5)
    # not implelemented yet
    # testCase(s1.getFoodUrgency(), X, num)

    print 'Testing .setState'
    # a) valid state
    s1.setState('food')
    testCase(s1.getState(), 'food', 6)
    # b) invalid state
    try:
        s1.setState('watermelon')
        testCase('absolutely', 'terribly wrong', 7)
    except ValueError:
        testCase(1, 1, 7)
    del s1

    Snake_test_2()

def Snake_test_2():
    """Update tests."""
    print 'Testing update'
    init_params = [3, [[0, 1], [1, 1], [1, 2]], 66, 's2']
    s2 = Snake(init_params[0], init_params[1], init_params[2], init_params[3])

    # valid updates
    s2.update([1, 0], 'false', init_params[2]-1)
    testCase(s2.getHeadPosition(), [1, 0], 8)
    testCase(s2.getHealth(), init_params[2]-1, 9)
    testCase(s2.getSize(), init_params[0], 10)

    s2.update([2, 0], 'true', init_params[2]-2)
    testCase(s2.getSize(), init_params[0]+1, 11)

    # invalid updates
    try:
        s2.update([3, 0], 'true', 'dog')
        testCase('nope', 'failed test', 12)
    except ValueError:
        testCase(1, 1, 12)


def testCase(var1, var2, testNum):
    """Run comparison tests, and if they fail, will raise an exception."""
    global current_case
    if var1 != var2:
        raise ValueError('FAILED TEST ' + str(testNum))
    current_case += 1

# Snake.py tests
print '-- Testing Snake.py --'
try:
    Snake_test_1()
    print "Test completed successfully. Passed " + str(current_case) + \
     " of " + str(NUM_CASES) + " test cases."
except ValueError as failure:
    print failure
