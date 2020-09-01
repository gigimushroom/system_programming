

## Convert 2D matric to single array
Given a 3 * 3 table:
| col, row | col, row | col, row |
|------|------|------|
| 0, 0 | 1, 0 | 2, 0 |
| 0, 1 | 1, 1 | 2, 1 |
| 0, 1 | 1, 2 | 2, 2 |

Each row size is 3.
The method to convert it to single array is: <br>
`index = size ^ row + column`


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