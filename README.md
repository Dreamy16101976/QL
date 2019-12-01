# QL
Q-learning in action or machine learning with Python+Pygame

This program allows beginners to play around with a machine learning method such as Q-learning.

The agent must learn to follow the optimal route, avoiding walls and traps.

The text of the program, abundantly provided with comments, is in the ql.py.
The settings are described in the settings.py: 
hyperparameters:
ALPHA = 1.0 # learning rate
GAMMA = 0.95 # discount 
walls:
WALLS = {(2,4), (3,4), (4,4), (5,4), (6,4), (10,8), (9,8), (10,6), (9,6), (8,6), (7,6), (6,6), (5,6), (1,7), (1,8), (1,9)}
traps:
TRAPS = {(2,2), (3,6), (5,8)}
