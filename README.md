# Zombie Survival Shooter
This is a zombie survival game shown in birds view. Zombies will attack from all directions
and the player needs to defend himself. The goal is to survive as long as possible.

## Running / Developing

### Prerequisites 
You need to have python 3.7 and ideally you use a virtual environment to use exactly the 
same library dependencies for this project. This project uses pygame as a framework 
and artwork from open game arts. 

#### Python and Dependencies Setup
Dependencies are managed via a virtual environment.

##### MacOS 
Follow these steps to fulfill prerequisites:
1. in terminal "cd" to this module directory
1. brew update
1. brew install python3
1. brew upgrade python3
1. virtualenv virtenv
1. source virtenv/bin/activate
1. pip install -r requirements.txt

In PyCharm make sure to select this new virtual environment as project interpreter.
Go to settings, then search for "interpreter". Then click cog wheel (settings) and 
new python interpreter as virtual environment with interpreter path
.../tombie-pygame/virtenv/bin/python 

### Work on project
Activate virtual environment
1. in terminal "cd" to this module directory
1. source virtenv/bin/activate

## Roadmap
The following features are intended to be added in the future:
1. multi player mode via network
1. zombies get sound / noise events as input to react to
1. zombie hordes learn via reinforcement learning how to best attack players