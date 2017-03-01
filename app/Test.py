"""Make sneakysnake run again.

    This will be a hotbed for exhaustive testing on the different classes
    and their independent functions."""


from Snake import Snake


num_cases = 0
current_case = 0
# remove global errors
# pylint: disable=W0603

def Snake_test_1():
    """Test basic .getX and .setX functionality.
    This test suite has 9 tests.
    """
    print 'Testing .getX using init'
    global num_cases
    num_cases += 9

    init_params = [2, [[0, 1], [1, 1]], 75, 's1']
    s1 = Snake(init_params[0], init_params[1], init_params[2], init_params[3])

    # test .toString()
    # I am sorry this test is gross.
    testCase(s1.toString(), "identifer: " + str(init_params[3]) + "\n\
health: " + str(init_params[2]) + "\n\
size: " + str(init_params[0]) + "\n\
state: unknown\n\
positions: " + str(init_params[1]), 'toString')
    testCase(s1.getState(), 'unknown', 'getState')
    testCase(s1.getHealth(), init_params[2], 'getHealth')
    testCase(s1.getSize(), init_params[0], 'getSize')
    testCase(s1.getHeadPosition(), init_params[1][0], 'getHeadPosition')
    testCase(s1.getAllPositions(), init_params[1], 'getAllPositions')
    testCase(s1.getIdentifier(), init_params[3], 'getIdentifier')
    # not implelemented yet
    # testCase(s1.getFoodUrgency(), X, num)

    print 'Testing .setState'
    # a) valid state
    s1.setState('food')
    testCase(s1.getState(), 'food', 'valid setState')
    # b) invalid state
    try:
        s1.setState('watermelon')
        testCase('absolutely', 'terribly wrong', 'invalid setState')
    except ValueError:
        testCase(1, 1, 'invalid setState')
    del s1


def Snake_test_2():
    """Test update() functionality.
    This test suite has 5 tests.
    """
    print 'Testing update'
    global num_cases
    num_cases += 5

    init_params = [3, [[0, 1], [1, 1], [1, 2]], 66, 's2']
    s2 = Snake(init_params[0], init_params[1], init_params[2], init_params[3])

    # valid updates
    s2.update([1, 0], init_params[2]-1)
    testCase(s2.getHeadPosition(), [1, 0], 'getHeadPosition after update')
    testCase(s2.getHealth(), init_params[2]-1, 'getHealth after update')
    testCase(s2.getSize(), init_params[0], 'getSize after update')

    s2.update([2, 0], 100)
    testCase(s2.getSize(), init_params[0]+1, 'getSize after update')

    # invalid updates
    try:
        s2.update([3, 0], 'dog')
        testCase('nope', 'failed test', 'invalid update')
    except ValueError:
        testCase(1, 1, 'invalid update')


def testCase(var1, var2, testIdent):
    """Run comparison tests, and if they fail, will raise an exception."""
    global current_case
    if var1 != var2:
        errStr = str('FAILED TEST for %s. Completed %i of %i tests.'\
                    % (str(testIdent), current_case, num_cases))
        raise ValueError(errStr)
    current_case += 1


if __name__ == '__main__':
    num_cases = 0
    # Snake.py tests
    print '-- Testing Snake.py --'
    try:
        Snake_test_1()
        Snake_test_2()
        print "Test completed successfully. Passed " + str(current_case) + \
         " of " + str(num_cases) + " test cases."
    except ValueError as failure:
        print failure
