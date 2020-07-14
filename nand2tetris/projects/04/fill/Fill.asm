// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(BLANK)
(CLEANUP)
  @temp
  D=M // D = i
  @8192
  D=D-A // D = i - 8192
  @FINISHCLEANUP
  D;JGE // if i - R1 >= 0, go to FINISH CLEANUP

  @temp
  D=M // D = Mem[i]
  @SCREEN
  D=A+D  // D = 16384 + i

  A=D // Set address to 16384 + i
  M=0 // Drawing to BLANK

  @temp
  M=M+1  // i++
  @CLEANUP
  0;JMP // goto CLEANUP
(FINISHCLEANUP)

@temp
M=0 // reset

(LOOP)
  @KBD
  D=M
  @BLANK
  D;JEQ // If keyboard is 0, means not pressed, loop again.

  @i
  M=0 // i = 0

(DRAWLOOP)
  @i
  D=M // D = i
  @8192
  D=D-A // D = i - 32
  @DRAWEND
  D;JGE // if i - R1 >= 0, go to DRAWEND

  @i
  D=M // D = Mem[i]
  @SCREEN
  D=A+D  // D = 16384 + i

  A=D // Set address to 16384 + i
  M=-1 // Drawing...

  @i
  M=M+1  // i++
  @DRAWLOOP
  0;JMP // goto DRAWLOOP
(DRAWEND)

  @LOOP
  0;JMP // go to LOOP
