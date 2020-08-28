### Issues in Square example
1. Keep pressing inc/dec size does not keep growing size. Either VM Emulator has issues or the code has bug. It should keep growing each iteration.
2. MoveDown() function tries to remove a small piece of block from top of square, then add another small block at the bottom of square. But the math is wrong, so the new added block does not connect to the existing one.

Instead of:
```
/** Moves the square left by 2 pixels. */
   method void moveLeft() {
      if (x > 1) {
         do Screen.setColor(false);
         do Screen.drawRectangle((x + size) - 1, y, x + size, y + size);
         let x = x - 2;
         do Screen.setColor(true);
         do Screen.drawRectangle(x, y, x + 1, y + size);
      }
      return;
   }
```

It should be:
```
/** Moves the square left by 2 pixels. */
   method void moveLeft() {
      if (x > 1) {
         do Screen.setColor(false);
         do Screen.drawRectangle((x + size) - 2, y, x + size, y + size);
         let x = x - 2;
         do Screen.setColor(true);
         do Screen.drawRectangle(x, y, x + 2, y + size);
      }
      return;
   }
```
