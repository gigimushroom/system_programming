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

(Class1.set)
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

// pop static 0
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify Class1.0 static value
@Class1.0
M=D

// push argument 1
// Get (ARG base + ith) pointer address
@ARG
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

// pop static 1
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify Class1.1 static value
@Class1.1
M=D

// push constant 0
@0
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

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

(Class1.get)
// push static 0
@Class1.0
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push static 1
@Class1.1
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// sub
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M - D // perform x - y, x is 2nd val, y is 1st val
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

(Sys.init)
// push constant 6
@6
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push constant 8
@8
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// Push return address 290
// Use the memory location of the command following the function call
@290
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


// ARG = SP - 2 - 5
@SP
D=M-1
D=D-1
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
// Go to function(Class1.set)
@Class1.set
0; JMP
// Declare a label for return address. It is current lines no. 290!
(290)

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

// push constant 23
@23
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push constant 15
@15
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// Push return address 364
// Use the memory location of the command following the function call
@364
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


// ARG = SP - 2 - 5
@SP
D=M-1
D=D-1
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
// Go to function(Class2.set)
@Class2.set
0; JMP
// Declare a label for return address. It is current lines no. 364!
(364)

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

// Push return address 424
// Use the memory location of the command following the function call
@424
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
// Go to function(Class1.get)
@Class1.get
0; JMP
// Declare a label for return address. It is current lines no. 424!
(424)

// Push return address 468
// Use the memory location of the command following the function call
@468
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
// Go to function(Class2.get)
@Class2.get
0; JMP
// Declare a label for return address. It is current lines no. 468!
(468)

(WHILE)
@WHILE
0; JMP

(Class2.set)
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

// pop static 0
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify Class2.0 static value
@Class2.0
M=D

// push argument 1
// Get (ARG base + ith) pointer address
@ARG
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

// pop static 1
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify Class2.1 static value
@Class2.1
M=D

// push constant 0
@0
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

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

(Class2.get)
// push static 0
@Class2.0
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// push static 1
@Class2.1
D=M
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// sub
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M - D // perform x - y, x is 2nd val, y is 1st val
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
