# Square.io

*A game by ThorLePug*

This is my first real python game, made with the pygame library. It is quite small but does
include multiple features, such as a menu, a leaderboard and, of course, the game.

The game itself is quite simple : you are a cube trying to destroy other cubes to protect yourself.

(The following section is made for no-pythoners, if you already have the classic python tools such as python as well 
as git, you can skip the next steps)

## Installing the game to run it

This game is made entirely in python, which means you will need to install (if not done) the python langiage to play it.
As it is made in python 3.10, ou should be using at least python version 3.10.

### Setting up the game on Linux

If you do not know how to use python in Linux, I recommend this tutorial:
> https://docs.python-guide.org/starting/install3/linux/

### Setting up the game on Windows

If you do not know how to use python in Linux, I recommend this tutorial:

> https://docs.python-guide.org/starting/install3/win/

### Installing pip

Pypi, the PYthon Package Index (commonly known as PIP), is necessary to run this game, which uses the pygame library to
run graphics for instance. When installing Python, check the box 'Install Pypi' for it to get installed automatically.

### Setting up the project files

If you have never used git, you should read this tutorial to be able to use github and clone the game.

> https://github.com/git-guides/install-git

Then, go to the folder where you want to install the game and type the following command in the git bash : 
```commandline
git clone https://github.com/ThorLePug/Square.io && cd Square.io
```

Then, back in the terminal, type :

```commandline
pip install virtualenv
source venv/bin/activate 
pip install -r requirements.txt
```

You can then launch the game (make sure the directory indicated is 
path/to/project/Square.io:

- Windows
```commandline
python main.py 
```
- Linux
```commandline
python3 main.py 
```

## Playing the game

### Controls

- Arrows : Directions (no sideways movement)
- Space bar : Shield (protects you from incoming fire)
- Mouse movement and button : Aim and Shoot bullets (no reload)

Enjoy !!!

