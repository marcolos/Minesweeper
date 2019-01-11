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
