"""Team Sneaky Snake Battlesnake implementation.
    Reponds to POST /start and POST /move.

    Picks movments depending on Djikstra's algortithm (thanks, python-igraph).
"""

import os
import random
import bottle
from Game import Game

MAPS = {}

@bottle.route('/static/<path:path>')
def static(path):
    """???."""
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    """Respond to POST /start with important details like what our snake looks
    like, and what our taunt is."""
    # pylint: disable=E1136
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    MAPS[game_id] = [board_height, board_width]

    head_url = '%s://%s/static/head.png' % (
        # pylint: disable=E1101
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': 'SSssssSSSsSSsssS',
        'head_url': head_url,
        'name': 'sneak'
    }

@bottle.post('/move')
def move():
    """Respond to POST /move with an adequate choice of movement."""

    first_turn = True
    data = bottle.request.json

    food_loc = data['food']
    snakes = data['snakes']
    us = data['you']
    height = data['height']
    turn = data['turn']
    game_id = data['game_id']

    if first_turn:
        battle = Game(height)
        first_turn = False
    else:
        battle.update(snakes, food_loc)

    directions = ['up', 'down', 'left', 'right']



    return {
        'move': random.choice(directions),
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
APPLICATION = bottle.default_app()
if __name__ == '__main__':

    bottle.run(APPLICATION, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
