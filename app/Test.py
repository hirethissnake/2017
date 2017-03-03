"""Make sneakysnake run again.

    This will be a hotbed for exhaustive testing on the different classes
    and their independent functions."""


import json
import requests
from Snake import Snake
from Game import Game


numCases = 0
currentCase = 0
URL = 'http://localhost:8080'
# remove global errors
# pylint: disable=W0603

def snakeTest1():
    """Test basic .getX and .setX functionality.
    This test suite has 11 tests.
    """
    print 'Testing .getX using init'
    global numCases
    numCases += 11

    initParams = {'id':'s1', 'coords':[[0, 1], [1, 1]], 'health_points':75}
    s1 = Snake(initParams)

    # test .toString()
    # I am sorry this test is gross.
    testCase(s1.toString(), "identifer: " + str(initParams['id']) + "\n\
healthPoints: " + str(initParams['health_points']) + "\n\
state: unknown\n\
coords: " + str(initParams['coords']), 'toString')
    testCase(s1.getSize(), len(initParams['coords']), 'getSize')
    testCase(s1.getState(), 'unknown', 'getState')
    testCase(s1.getHealth(), initParams['health_points'], 'getHealth')
    testCase(s1.getHunger(), 100-initParams['health_points'], 'getHunger')
    testCase(s1.getHeadPosition(), initParams['coords'][0], 'getHeadPosition')
    testCase(s1.getTailPosition(), initParams['coords'][-1], 'getTailPosition')
    testCase(s1.getAllPositions(), initParams['coords'], 'getAllPositions')
    testCase(s1.getIdentifier(), initParams['id'], 'getIdentifier')
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


def snakeTest2():
    """Test update() functionality.
    This test suite has 5 tests.
    """
    print 'Testing update'
    global numCases
    numCases += 5

    initParams = {'id':'s2', 'coords':[[0, 1], [1, 1], [1, 2]], 'health_points':66}
    s2 = Snake(initParams)

    updateParams = {'health_points':65, 'coords':[[0, 0], [0, 1], [1, 1]]}

    # valid updates
    s2.update(updateParams)
    testCase(s2.getHeadPosition(), [0, 0], 'getHeadPosition after update')
    testCase(s2.getHealth(), initParams['health_points']-1, 'getHealth after update')
    testCase(s2.getSize(), len(initParams['coords']), 'getSize after update')

    updateParams = {'health_points':100, 'coords':[[1, 0], [0, 0], [0, 1], [1, 1]]}

    s2.update(updateParams)
    testCase(s2.getSize(), len(initParams['coords'])+1, 'getSize after update')

    # invalid updates
    try:
        updateParams = {'health_points':'dog', 'coords':[[2, 0], [1, 0], [0, 0], [0, 1]]}
        s2.update(updateParams)
        testCase('nope', 'failed test', 'invalid update')
    except ValueError:
        testCase(1, 1, 'invalid update')

def gameTest1():
    """Test game init and update functionality.
    This test suite has 16 tests.
    """
    print 'Testing init and update'
    global numCases
    numCases += 16
    initParams = {"width": 20, "height": 20, "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa"}

    g1 = Game(initParams)

    # This is some mangled testing, but c'est la vie.
    # Test init
    testCase(g1.width, initParams['width'], 'init width')
    testCase(g1.height, initParams['height'], 'init height')
    testCase(g1.you, '', 'empty .you')
    testCase(g1.turn, 0, '0 turn')
    testCase(g1.food, [], 'empty food positions array')

    # Test update
    # still can't .get any of these :(
    updateParams = {"snakes": [{"taunt": "git gud", "name": "my-snake",
    "id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb", "health_points": 93, "coords":
    [[0, 0], [0, 1], [0, 2]]}, {"taunt": "cash me outside", "name":
    "angry-whitegirl", "id": "ex-uuid",
    "health_points": 93, "coords": [[15, 14], [15, 13], [15, 12]]}],
    "height":20, "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa",
    "food":[[4, 5], [8, 9]], "you":"25229082-f0d7-4315-8c52-6b0ff23fb1fb"}

    # does it apply data?
    g1.update(updateParams)
    testCase(g1.you, updateParams['you'], 'you value')

    # does it make snakes, with correct data?
    exSnake = g1.snakes['ex-uuid']
    exSnakeData = updateParams['snakes'][1] # exSnake is second
    testCase(exSnake.coords, exSnakeData['coords'], 'init coords')
    testCase(exSnake.taunt, exSnakeData['taunt'], 'init taunt')

    testCase(len(g1.snakes), len(updateParams['snakes']), 'correct num of snakes')
    testCase(g1.food, updateParams['food'], 'init food')

    # new update, more data!
    # test updated taunt, health, coords, and health for both snakes
    updateParams = {"snakes": [{"taunt": "eating food", "name": "my-snake",
    "id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb", "health_points": 90, "coords":
[[13, 13], [14, 13], [14, 12]]}, {"taunt": "how bout da?", "name":
    "angry-whitegirl", "id": "ex-uuid",
    "health_points": 20, "coords": [[16, 15], [15, 14], [15, 13], [15, 12]]}],
    "height":20, "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa",
    "food":[[15, 15]], "you":"25229082-f0d7-4315-8c52-6b0ff23fb1fb"}

    g1.update(updateParams)
    # first snake update tests
    exSnake = g1.snakes['25229082-f0d7-4315-8c52-6b0ff23fb1fb']
    exSnakeData = updateParams['snakes'][0]
    testCase(exSnake.taunt, exSnakeData['taunt'], 'update taunt 1')
    testCase(exSnake.coords, exSnakeData['coords'], 'update coords 1')
    testCase(exSnake.healthPoints, exSnakeData['health_points'], 'update health 1')

    # second snake update tests
    exSnake = g1.snakes['ex-uuid']
    exSnakeData = updateParams['snakes'][1]
    testCase(exSnake.taunt, exSnakeData['taunt'], 'update taunt 1')
    testCase(exSnake.coords, exSnakeData['coords'], 'update coords 1')
    testCase(exSnake.healthPoints, exSnakeData['health_points'], 'update health 1')

def gameTest2():
    """Test update functionality for faulty data.
    This test suite has 0 tests.
    """
    print "This faulty data test suite is not complete."
    global numCases
    numCases += 0

def mainTest1():
    """Test update functionality for game starting.
    This test suite has 8 tests.
    """
    print "Testing main /start."
    global numCases
    numCases += 8

    paramData = {'width':20, 'height':20, 'game_id':'game1'}
    headers = {'Content-Type':'application/json'}

    # start testing
    r = requests.post(str(URL)+'/start', json=paramData, headers=headers)

    try:
        responseData = json.loads(r.text)
    except TypeError:
        testCase('data', 'invalid', 'json-formatted /start response data')
    except AttributeError:
        testCase('data', 'invalid', 'json-formatted /start response data')

    testCase('color' in responseData, True, 'main returns color')
    testCase('head_url' in responseData, True, 'main returns head_url')
    testCase('name' in responseData, True, 'main returns name')
    testCase('taunt' in responseData, True, 'main returns taunt')

    # optional tests
    try:
        testCase('head_type' in responseData, True, 'main returns head_type (optional)')
    except ValueError as err:
        print err
    try:
        testCase('tail_type' in responseData, True, 'main returns tail_type (optional)')
    except ValueError as err:
        print err
    try:
        testCase('secondary_color' in responseData, True, 'main returns secondary_color (optional)')
    except ValueError as err:
        print err

def mainTest2():
    """Test update functionality for game movement.
    This test suite has 0 tests.
    """
    print "Testing main /move."
    global numCases
    numCases += 2

    paramData = {"snakes": [{"taunt": "git gud", "name": "my-snake",
    "id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb", "health_points": 93, "coords":
    [[0, 0], [0, 1], [0, 2]]}, {"taunt": "cash me outside", "name":
    "angry-whitegirl", "id": "ex-uuid",
    "health_points": 93, "coords": [[15, 14], [15, 13], [15, 12]]}], "width":20,
    "height":20, "game_id": "game1",
    "food":[[4, 5], [8, 9]], "you":"25229082-f0d7-4315-8c52-6b0ff23fb1fb"}
    headers = {'Content-Type':'application/json'}

    # start testing
    r = requests.post(str(URL)+'/move', json=paramData, headers=headers)

    try:
        responseData = json.loads(r.text)
    except TypeError:
        testCase('data', 'invalid', 'json-formatted /move response data')
    except AttributeError:
        testCase('data', 'invalid', 'json-formatted /move response data')

    testCase('move' in responseData, True, 'main returns move')
    testCase('taunt' in responseData, True, 'main returns new taunt')

    testCase(responseData['move'], 'up' or 'down' or 'left' or 'right', 'valid move')

def testCase(var1, var2, testIdent):
    """Run comparison tests, and if they fail, will raise an exception."""
    global currentCase
    if var1 != var2:
        #errStr = str('FAILED TEST for %s. Completed %i of %i tests.'\
        #            % (str(testIdent), currentCase, numCases))
        errStr = str('FAILED TEST for %s.' % str(testIdent))
        print '  Value 1', var1
        print '  Value 2', var2
        raise ValueError(errStr)
    currentCase += 1


if __name__ == '__main__':
    numCases = 0
    # Snake.py tests
    try:
        print '-- Testing Game.py --'
        gameTest1()
        print '-- Testing Snake.py --'
        snakeTest1()
        snakeTest2()
        print '-- Testing Main.py --'
        mainTest1()
        mainTest2()
        print "Test completed successfully."
    except ValueError as failure:
        print failure

    print "Passed %s of %s test cases." % (str(currentCase), str(numCases))
