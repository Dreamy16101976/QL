## Q-learning in action or machine learning with Python+Pygame

This program allows beginners to play around with a machine learning method such as Q-learning.

The whole charm of the Q-learning algorithm is that * it works when the agent does not even know HOW to achieve the desired result *.

The agent must learn to follow the optimal route, avoiding walls and traps.<br>
The text of the program, abundantly provided with comments, is in the **ql.py**.<br>
The settings are described in the **settings.py**:<br>
*hyperparameters*:
ALPHA = 1.0 # learning rate
GAMMA = 0.95 # discount 
*walls*:
WALLS = {(2,4), (3,4), (4,4), (5,4), (6,4), (10,8), (9,8), (10,6), (9,6), (8,6), (7,6), (6,6), (5,6), (1,7), (1,8), (1,9)}
*traps*:
TRAPS = {(2,2), (3,6), (5,8)}<br>
<br>
When starting up, the desired number of episodes is requested (the last of them will be test).<br>
Then the learning process starts, during which the agent’s travel process is graphically displayed.<br>
Play it!!! :-)
