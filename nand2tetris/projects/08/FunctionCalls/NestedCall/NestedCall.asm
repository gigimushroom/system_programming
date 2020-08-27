// Set CP to 256
@256
D=A
@SP
M=D
// Set LCL to -1
@LCL
M=-1
// Set ARG to -2
@ARG
M=-1
M=M-1
// Set THIS to -3
@THIS
M=-1
M=M-1
M=M-1
// Set THAT to -4
@THAT
M=-1
M=M-1
M=M-1
M=M-1
// call Sys.init

// Push return address 62
// Use the memory location of the command following the function call
@62
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push LCL
@LCL
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push ARG
@ARG
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push THIS
@THIS
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push THAT
@THAT
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// ARG = SP - 0 - 5
@SP
D=M-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
// ends with re-pos ARG.
// LCL = SP
@SP
D=M
@LCL
M=D
// Go to function(Sys.init)
@Sys.init
0; JMP
// Declare a label for return address. It is current lines no. 62!
(62)

(Sys.init)
// push constant 4000
@4000
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// pop pointer 0
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify THIS pointer
@THIS
M=D

// push constant 5000
@5000
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// pop pointer 1
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify THAT pointer
@THAT
M=D

// Push return address 136
// Use the memory location of the command following the function call
@136
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push LCL
@LCL
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push ARG
@ARG
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push THIS
@THIS
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push THAT
@THAT
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// ARG = SP - 0 - 5
@SP
D=M-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
// ends with re-pos ARG.
// LCL = SP
@SP
D=M
@LCL
M=D
// Go to function(Sys.main)
@Sys.main
0; JMP
// Declare a label for return address. It is current lines no. 136!
(136)

// pop temp 1
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save TEMP memory segment pos(1) to Reg D
@6
D=A
// Store temp ptr to Reg 14
@14
M=D
// Load stored value, set A to correct segment pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment temp is done.
M=D

(LOOP)
@LOOP
0; JMP

(Sys.main)
// push constant 0
@0
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push constant 0
@0
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push constant 0
@0
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push constant 0
@0
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push constant 0
@0
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push constant 4001
@4001
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// pop pointer 0
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify THIS pointer
@THIS
M=D

// push constant 5001
@5001
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// pop pointer 1
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify THAT pointer
@THAT
M=D

// push constant 200
@200
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// pop local 1
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save (local base + ith) address to Reg D
@LCL
D=M
@1
D=D+A
// Store local ptr to Reg 14
@14
M=D
// Load stored value, set A to correct segment pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment local is done.
M=D

// push constant 40
@40
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// pop local 2
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save (local base + ith) address to Reg D
@LCL
D=M
@2
D=D+A
// Store local ptr to Reg 14
@14
M=D
// Load stored value, set A to correct segment pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment local is done.
M=D

// push constant 6
@6
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// pop local 3
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save (local base + ith) address to Reg D
@LCL
D=M
@3
D=D+A
// Store local ptr to Reg 14
@14
M=D
// Load stored value, set A to correct segment pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment local is done.
M=D

// push constant 123
@123
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// Push return address 337
// Use the memory location of the command following the function call
@337
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push LCL
@LCL
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push ARG
@ARG
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push THIS
@THIS
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// Push THAT
@THAT
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D


// ARG = SP - 1 - 5
@SP
D=M-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
// ends with re-pos ARG.
// LCL = SP
@SP
D=M
@LCL
M=D
// Go to function(Sys.add12)
@Sys.add12
0; JMP
// Declare a label for return address. It is current lines no. 337!
(337)

// pop temp 0
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save TEMP memory segment pos(0) to Reg D
@5
D=A
// Store temp ptr to Reg 14
@14
M=D
// Load stored value, set A to correct segment pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment temp is done.
M=D

// push local 0
// Get (LCL base + ith) pointer address
@LCL
D=M
@0
A=D+A
// Save value to Reg D
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push local 1
// Get (LCL base + ith) pointer address
@LCL
D=M
@1
A=D+A
// Save value to Reg D
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push local 2
// Get (LCL base + ith) pointer address
@LCL
D=M
@2
A=D+A
// Save value to Reg D
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push local 3
// Get (LCL base + ith) pointer address
@LCL
D=M
@3
A=D+A
// Save value to Reg D
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push local 4
// Get (LCL base + ith) pointer address
@LCL
D=M
@4
A=D+A
// Save value to Reg D
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// add
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M + D // perform x + y
@SP // fix stack pointer
M=M-1

// add
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M + D // perform x + y
@SP // fix stack pointer
M=M-1

// add
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M + D // perform x + y
@SP // fix stack pointer
M=M-1

// add
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M + D // perform x + y
@SP // fix stack pointer
M=M-1

// Save LCL(Frame) to Reg 13
@LCL
D=M
@13
M=D
// RET = *(FRAME - 5)
D=D-1
D=D-1
D=D-1
D=D-1
A=D-1
D=M // de-reference return address
@14
M=D // Save the return address
// Pop topmost from stack
@SP
A=M
A=A-1
D=M
// Fix stack pointer after pop
@SP
M=M-1
// Save the pop-ed value to arg 0
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
// THAT = * (FRAME - 1)
@13
A=M-1
D=M // de-reference THAT ptr
@THAT
M=D // Restore THAT ptr
// THIS = * (FRAME - 2)
@13
A=M-1
A=A-1
D=M // de-reference THIS ptr
@THIS
M=D // Restore THIS ptr
// ARG = * (FRAME - 3)
@13
A=M-1
A=A-1
A=A-1
D=M // de-reference ARG ptr
@ARG
M=D // Restore ARG ptr
// LCL = * (FRAME - 4)
@13
A=M-1
A=A-1
A=A-1
A=A-1
D=M // de-reference LCL ptr
@LCL
M=D // Restore LCL ptr
@14
A=M
0; JMP

(Sys.add12)
// push constant 4002
@4002
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// pop pointer 0
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify THIS pointer
@THIS
M=D

// push constant 5002
@5002
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// pop pointer 1
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify THAT pointer
@THAT
M=D

// push argument 0
// Get (ARG base + ith) pointer address
@ARG
D=M
@0
A=D+A
// Save value to Reg D
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push constant 12
@12
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// add
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M + D // perform x + y
@SP // fix stack pointer
M=M-1

// Save LCL(Frame) to Reg 13
@LCL
D=M
@13
M=D
// RET = *(FRAME - 5)
D=D-1
D=D-1
D=D-1
D=D-1
A=D-1
D=M // de-reference return address
@14
M=D // Save the return address
// Pop topmost from stack
@SP
A=M
A=A-1
D=M
// Fix stack pointer after pop
@SP
M=M-1
// Save the pop-ed value to arg 0
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
// THAT = * (FRAME - 1)
@13
A=M-1
D=M // de-reference THAT ptr
@THAT
M=D // Restore THAT ptr
// THIS = * (FRAME - 2)
@13
A=M-1
A=A-1
D=M // de-reference THIS ptr
@THIS
M=D // Restore THIS ptr
// ARG = * (FRAME - 3)
@13
A=M-1
A=A-1
A=A-1
D=M // de-reference ARG ptr
@ARG
M=D // Restore ARG ptr
// LCL = * (FRAME - 4)
@13
A=M-1
A=A-1
A=A-1
A=A-1
D=M // de-reference LCL ptr
@LCL
M=D // Restore LCL ptr
@14
A=M
0; JMP

(END)
@END
0;JMP
