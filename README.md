## Q-learning in action or machine learning with Python+Pygame<br><br>
This program allows beginners to play around with a machine learning method such as Q-learning.<br><br>
The whole charm of the Q-learning algorithm is that *it works when the agent does not even know HOW to achieve the desired result*.<br><br>
The agent must learn to follow the optimal route, avoiding walls and traps.<br><br>
For the successful application of this method, an agent feedback mechanism is required - reward. 
For reaching the end point of the route, the agent receives a reward of **+100** (motivates the agent to reach the required position), and for each move - a penalty of **-1** (motivates the agent to achieve the result for the minimum number of moves).<br><br>
The text of the program, abundantly provided with comments, is in the **ql.py**.<br><br>
The settings are described in the **settings.py**:<br>
*hyperparameters*:<br>
ALPHA = 1.0<br>
GAMMA = 0.95<br>
*walls*:<br>
WALLS = {(2,4), (3,4), (4,4), (5,4), (6,4), (10,8), (9,8), (10,6), (9,6), (8,6), (7,6), (6,6), (5,6), (1,7), (1,8), (1,9)}<br>
*traps*:<br>
TRAPS = {(2,2), (3,6), (5,8)}<br>
<br>
When starting up, the desired number of episodes is requested (the last of them will be test).<br>
Then the learning process starts, during which the agent’s travel process is graphically displayed.<br><br>
Play it! :-)
