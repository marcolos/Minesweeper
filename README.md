# Minesweeper

## Overview
Minesweeper is a single-player puzzle video game. The objective of the game is to clear a rectangular board containing hidden "mines" or bombs without detonating any of them, with help from clues about the number of neighboring mines in each field. The game originates from the 1960s, and has been written for many computing platforms in use today.
The player is initially presented with a grid of undifferentiated squares. Some randomly selected squares, unknown to the player, are designated to contain mines. Typically, the size of the grid and the number of mines are set in advance by the user, either by entering the numbers or selecting from defined skill levels, depending on the implementations. (In the Microsoft variant, this is limited to 30 times 24 with 667 mines.)
The game is played by revealing squares of the grid by clicking or otherwise indicating each square. If a square containing a mine is revealed, the player loses the game. If no mine is revealed, a digit is instead displayed in the square, indicating how many adjacent squares contain mines; if no mines are adjacent, the square becomes blank, and all adjacent squares will be recursively revealed. The player uses this information to deduce the contents of other squares, and may either safely reveal each square or mark the square as containing a mine. The game is won when all mine-free squares are revealed, because all mines have been located.

## Rules of the Game
The of Minesweeper are fairly simple:
- You are presented with a board of squares. Some squares contain mines (bombs), others don’t.
- If you click on a square containing a bomb, you lose. If you manage to click all the squares (without clicking on any bombs) you win.
- Clicking a square which doesn’t have a bomb reveals the number of neighbouring squares containing bombs. Use this information plus some guess work to avoid the bombs.
- To open a square, point at the square and left click on it.
- To mark a square you think is a bomb, point and right-click.
- If you mark a bomb incorrectly, you will have to correct the mistake before you can win. Incorrect bomb marking doesn’t kill you, but it can lead to mistakes which do.
- You don’t have to mark all the bombs to win; you just need to open all non-bomb squares.

## Implementation
The game was implemented using Python. The GUI was implemented using PyQt5 framework .
The app was developed using the MVC(Model-View-Control) pattern

### The Model
The main model has been implemented in the `MinesweeperModel` Class.

This class contains the game state and the rules of the game.

It provides methods to get, set, modify and evolve the state following the rules.

Attributes:
- size = Minesweeper size (square form)
- counter = is the timer counter
- n_mines = number of mine in the map
- n_caselline_open = number of square opened
- n_caselline_flagged = number of square flagged
- oldWin = is a boolean value. It's used to handler the save and resume features. It's true if when the game is closed, your state was SUCCESS. It's has been used to no re-open the insertWinner dialog.
- status = is the game status. It can be Ready,Playing,Failed or Success
- caselline = is a matrix of casellina(square)

For the leaderboard has been implemented another Model Class named `LeaderboardModel`.

### The View
There are a main view, a leaderboard view, custom view and insert winner view.
They are implemented in the `MinesweeperView`, `LeaderboardDialog` `CustomDialog` and `InsertWinnerDialog` classes.
- The main view shows all the Minesweeper game.
- The leaderboard view shows the leaderboards.
- The custom view allows you to set the mine numbers, and size.
- The insert winner dialog allows you to insert your name when you are playing at Beginner, Intermediate or Expert level and you win.

## Functionalities
The game can be launched from the `main.py` script:
```
$ python3 main.py
```
or if you have installed anaconda you can do:
```
$ ipython
$ run main.py
```
### Main window
The Main window presents itself like this:

![ ](https://github.com/marcolos/Minesweeper/blob/master/git_image/gui.png)

### Leaderboard
When the user is playing at Beginner, Intermediate or Expert level and he win, he can insert his name in the Leaderboard. There is one leaderboard for each level that shows the best 10 player, sorted by increasing elapsed time. 

![ ](https://github.com/marcolos/Minesweeper/blob/master/git_image/leaderboard.png)

### Customized game 
The user can custom the game setting the size and the bombs number or he can select the three levels from Menu Bar 

![custum](https://github.com/marcolos/Minesweeper/blob/master/git_image/custom.png)

![select from menu bar](https://github.com/marcolos/Minesweeper/blob/master/git_image/select.png)

### Save and Reload
The game automatically will be saved when the user closes the app and it will be automatically reloaded when the user reopens the app. This is achieved creating a csv file that will maintain all the necessary variables to reload the game.

### Game demonstration

<img src="https://github.com/marcolos/Minesweeper/blob/master/git_image/play.gif" alt="Demonstration Gif" data-load="full">

## Requirements

| Software       | Version        | Required |
| -------------- |:--------------:| --------:|
| **Python**     |     >= 3.5     |    Yes   |
| **PyQt5**      |     >= 5.1     |    Yes   |
