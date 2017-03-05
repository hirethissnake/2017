"""Team Sneaky Snake Battlesnake implementation.
    Reponds to POST /start and POST /move.

    Picks movments depending on Djikstra's algortithm (thanks, python-igraph).
"""

import os
import bottle
import time
from Game import Game

gameDic = dict()

print "main.py is now running"


@bottle.route('/static/<path:path>')
def static(path):
    """???."""
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    """Respond to POST /start with important details like what our snake looks
    like, and what our taunt is."""
    # E1136 Value 'data' is insubscriptable
    # pylint: disable=E1136


    data = bottle.request.json

    print 'We have begun a new game!'
    print data

    #Create a game object with the data given
    game_id = data['game_id']
    battle = Game(data)
    #Enter the game into the GameDictionary with the key value set to it's id
    gameDic[game_id] = battle

    head_url = '%s://%s/static/head.png' % (
        # pylint: disable=E1101
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    sendingData = {
        'color': '#FFEBD0',
        'taunt': 'SSssssSSSsSSsssS',
        'head_url': head_url,
        'name': 'Sneakysnake',
        'head_type': 'tongue',
        'tail_type': 'curled'
    }

    # log and return
    print sendingData
    return sendingData

@bottle.post('/move')
def move():
    """Respond to POST /move with an adequate choice of movement."""
    # E1135 Value 'data' doesn't support membership test
    # E1136 Value 'data' is insubscriptable
    # pylint: disable=E1135, E1136
    data = bottle.request.json
    print data
    #Store the id of this game and then access the matching object in GameDict

    # get game_id
    if 'game_id' in data:
        curGame = data['game_id']
    else:
        print 'Data missing game_id'
    # get curGame from gameDic
    if curGame in gameDic:
        battle = gameDic[curGame]
        #Update the game with new gamestate
        start = time.time()
        battle.update(data)
        #Request next best move
        nextMove = battle.getNextMove()
        #nextTaunt = battle.getTaunt()
        print("--- %s seconds ---" % (time.time() - start))
    else:
        print 'ERROR: Received request for game that does not exist'
        print '  To avoid collateral damage to other games, responding with \
        default move'
        nextMove = 'up'
        #nextTaunt = 'yeaboi'

    sendingData = {
        'move': nextMove,
        'taunt': 'please no'
    }#nextTaunt

    # log and return
    print sendingData
    return sendingData


# Expose WSGI app (so gunicorn can find it)
APPLICATION = bottle.default_app()
if __name__ == '__main__':

    bottle.run(APPLICATION, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
