# Vacuum-Robot-Simulator
A vacuum robot simulator made in pygame

# How to play

1. Run `main.py` while inside the main folder (so the `assets` can be loaded)

2. Choose the type of robot control from:

    - Automatic control: The controller controls the robot with a random walk algorithm

    - Manual control: The player controls the robot with the following controls

|       W      |             A            |        S       |         D        |        SPACEBAR       |     ENTER     |
|:------------:|:------------------------:|:--------------:|:----------------:|:---------------------:|:-------------:|
| Walk forward | Rotate counter-clockwise | Walk backwards | Rotate clockwise | Turn on vacuum motors | Stop movement |

3. Draw the house walls and obstacles or use the default (by not drawing anything)

4. Try to vacuum all dust in the shortest time possible

5. The simulation ends when all dust was cleaned
