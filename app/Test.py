"""Make sneakysnake run again.

    This will be a hotbed for exhaustive testing on the different classes
    and their independent functions."""


from Snake import Snake
from Game import Game


num_cases = 0
current_case = 0
# remove global errors
# pylint: disable=W0603

def Snake_test_1():
    """Test basic .getX and .setX functionality.
    This test suite has 11 tests.
    """
    print 'Testing .getX using init'
    global num_cases
    num_cases += 11

    init_params = {'id':'s1', 'coords':[[0, 1], [1, 1]], 'health_points':75}
    s1 = Snake(init_params)

    # test .toString()
    # I am sorry this test is gross.
    testCase(s1.toString(), "identifer: " + str(init_params['id']) + "\n\
health_points: " + str(init_params['health_points']) + "\n\
state: unknown\n\
coords: " + str(init_params['coords']), 'toString')
    testCase(s1.getSize(), len(init_params['coords']), 'getSize')
    testCase(s1.getState(), 'unknown', 'getState')
    testCase(s1.getHealth(), init_params['health_points'], 'getHealth')
    testCase(s1.getHunger(), 100-init_params['health_points'], 'getHunger')
    testCase(s1.getHeadPosition(), init_params['coords'][0], 'getHeadPosition')
    testCase(s1.getTailPosition(), init_params['coords'][-1], 'getTailPosition')
    testCase(s1.getAllPositions(), init_params['coords'], 'getAllPositions')
    testCase(s1.getIdentifier(), init_params['id'], 'getIdentifier')
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

    init_params = {'id':'s2', 'coords':[[0, 1], [1, 1], [1, 2]], 'health_points':66}
    s2 = Snake(init_params)

    update_params = {'health_points':65, 'coords':[[0, 0], [0, 1], [1, 1]]}

    # valid updates
    s2.update(update_params)
    testCase(s2.getHeadPosition(), [0, 0], 'getHeadPosition after update')
    testCase(s2.getHealth(), init_params['health_points']-1, 'getHealth after update')
    testCase(s2.getSize(), len(init_params['coords']), 'getSize after update')

    update_params = {'health_points':100, 'coords':[[1, 0], [0, 0], [0, 1], [1, 1]]}

    s2.update(update_params)
    testCase(s2.getSize(), len(init_params['coords'])+1, 'getSize after update')

    # invalid updates
    try:
        update_params = {'health_points':'dog', 'coords':[[2, 0], [1, 0], [0, 0], [0, 1]]}
        s2.update(update_params)
        testCase('nope', 'failed test', 'invalid update')
    except ValueError:
        testCase(1, 1, 'invalid update')

def Game_test_1():
    """Test game init and update functionality.
    This test suite has 16 tests.
    """
    print 'Testing init and update'
    global num_cases
    num_cases += 16
    init_params = {"width": 20, "height": 20, "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa"}

    g1 = Game(init_params)

    # This is some mangled testing, but c'est la vie.
    # Test init
    testCase(g1.width, init_params['width'], 'init width')
    testCase(g1.height, init_params['height'], 'init height')
    testCase(g1.you, '', 'empty .you')
    testCase(g1.turn, 0, '0 turn')
    testCase(g1.food, [], 'empty food positions array')

    # Test update
    # still can't .get any of these :(
    update_params = {"snakes": [{"taunt": "git gud", "name": "my-snake",
    "id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb", "health_points": 93, "coords":
    [[0, 0], [0, 1], [0, 2]]},{"taunt": "cash me outside", "name":
    "angry-whitegirl", "id": "ex-uuid",
    "health_points": 93, "coords": [[15, 14], [15, 13], [15, 12]]}],
    "height":20, "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa",
    "food":[[4, 5], [8, 9]], "you":"25229082-f0d7-4315-8c52-6b0ff23fb1fb"}

    # does it apply data?
    g1.update(update_params)
    testCase(g1.you, update_params['you'], 'you value')

    # does it make snakes, with correct data?
    ex_snake = g1.snakes['ex-uuid']
    ex_snake_data = update_params['snakes'][1] # ex_snake is second
    testCase(ex_snake.coords, ex_snake_data['coords'], 'init coords')
    testCase(ex_snake.taunt, ex_snake_data['taunt'], 'init taunt')

    testCase(len(g1.snakes), len(update_params['snakes']), 'correct num of snakes')
    testCase(g1.food, update_params['food'], 'init food')

    # new update, more data!
    # test updated taunt, health, coords, and health for both snakes
    update_params = {"snakes": [{"taunt": "eating food", "name": "my-snake",
    "id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb", "health_points": 90, "coords":
[[13, 13], [14, 13], [14, 12]]}, {"taunt": "how bout da?", "name":
    "angry-whitegirl", "id": "ex-uuid",
    "health_points": 20, "coords": [[16, 15], [15, 14], [15, 13], [15, 12]]}],
    "height":20, "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa",
    "food":[[15, 15]], "you":"25229082-f0d7-4315-8c52-6b0ff23fb1fb"}

    g1.update(update_params)
    # first snake update tests
    ex_snake = g1.snakes['25229082-f0d7-4315-8c52-6b0ff23fb1fb']
    ex_snake_data = update_params['snakes'][0]
    testCase(ex_snake.taunt, ex_snake_data['taunt'], 'update taunt 1')
    testCase(ex_snake.coords, ex_snake_data['coords'], 'update coords 1')
    testCase(ex_snake.health_points, ex_snake_data['health_points'], 'update health 1')

    # second snake update tests
    ex_snake = g1.snakes['ex-uuid']
    ex_snake_data = update_params['snakes'][1]
    testCase(ex_snake.taunt, ex_snake_data['taunt'], 'update taunt 1')
    testCase(ex_snake.coords, ex_snake_data['coords'], 'update coords 1')
    testCase(ex_snake.health_points, ex_snake_data['health_points'], 'update health 1')

def Game_test_2():
    """Test update functionality for faulty data.
    This test suite has 0 tests.
    """
    print "This faulty data test suite is not complete."
    global num_cases
    num_cases += 0

def testCase(var1, var2, testIdent):
    """Run comparison tests, and if they fail, will raise an exception."""
    global current_case
    if var1 != var2:
        errStr = str('FAILED TEST for %s. Completed %i of %i tests.'\
                    % (str(testIdent), current_case, num_cases))
        print 'Value 1', var1
        print 'Value 2', var2
        raise ValueError(errStr)
    current_case += 1


if __name__ == '__main__':
    num_cases = 0
    # Snake.py tests
    try:
        print '-- Testing Game.py --'
        Game_test_1()
        print '-- Testing Snake.py --'
        Snake_test_1()
        Snake_test_2()
        print "Test completed successfully. Passed " + str(current_case) + \
         " of " + str(num_cases) + " test cases."
    except ValueError as failure:
        print failure
