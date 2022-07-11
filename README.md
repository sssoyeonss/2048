# 2048-client

A Python module to interact with Du Tuyen 2021's 2048 server.

## Setup

The module doesn't require any third-party dependencies.
Simply clone with '''git clone'''

## Usage

The game.py provides a class named Client. This represents a game, and provides methods such as make_move and get_state
The get_state functions gets data from a deque, each object corresponds to a response from the server (Board, Game, or Result)
For more information, refer to the source codes provided
