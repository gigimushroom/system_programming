# Game of Life Simulation
It is a zero-player [cellular automaton](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) game, its evolution is determined by its initial state, requiring no further input. 

## Feature
Press `p` to pause the game. Pause again to continue.

## Rules
- Any live cell with two or three live neighbors lives on to the next generation.
- Any empty cell with exactly three live neighbors becomes a live cell in the next generation.
- All other cells are empty in the next generation.


## Notes
1. JACK does not have operator priority. Hence, we must use `()` to set up priority.
2. JACK array's feature is limited, a few workaround has to be used, caused the program containing duplicated code.

## Tech Details
### Convert 2D matric to single array
Given a 3 * 3 table:
| col, row | col, row | col, row |
|------|------|------|
| 0, 0 | 1, 0 | 2, 0 |
| 0, 1 | 1, 1 | 2, 1 |
| 0, 1 | 1, 2 | 2, 2 |

Each row size is 3.
The method to convert it to single array is: <br>
`index = size ^ row + column`

### a
We re-map the 512 * 256 Screen to a smaller board: `32 * 16 (col * row)`. \
`Column (0 <= r <= 31). Row(0 <= row <= 16)` \
Each row has 32 words, each word can either be filled or empty. 

In our 32 * 16 board, each cell is a 16 * 16 bits square. \
The size of cell in Screen is 32 * 16, where 32 is Screen's row size. 

Example: \
To display cell `(1, 1)` in Screen: \
Row is `row * 32 * 16`, and column is `col`. \
The memory address in RAM is: `row * 32 * 16 + col`


### Error in nandteris

```
Code Method/Function       Description
---- ---------------       -----------------------------------------------
 1   Sys.wait              Duration must be positive
 2   Array.new             Array size must be positive
 3   Math.divide           Division by zero
 4   Math.sqrt             Cannot compute square root of a negative number
 5   Memory.alloc          Allocated memory size must be positive
 6   Memory.alloc          Heap overflow
 7   Screen.drawPixel      Illegal pixel coordinates
 8   Screen.drawLine       Illegal line coordinates
 9   Screen.drawRectangle  Illegal rectangle coordinates
12   Screen.drawCircle     Illegal center coordinates
13   Screen.drawCircle     Illegal radius
14   String.new            Maximum length must be non-negative
15   String.charAt         String index out of bounds
16   String.setCharAt      String index out of bounds
17   String.appendChar     String is full
18   String.eraseLastChar  String is empty
19   String.setInt         Insufficient string capacity
20   Output.moveCursor     Illegal cursor location
```