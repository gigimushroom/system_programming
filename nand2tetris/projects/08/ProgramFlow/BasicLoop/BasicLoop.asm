// push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D

// pop local 0
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
@0
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

(LOOP_START)
// push argument 0
// Get (ARG base + ith) pointer address
@ARG
D=M
@0
A=D+A
// Save value to Reg D
D=M
@SP
M=M+1
A=M-1
M=D

// push local 0
// Get (LCL base + ith) pointer address
@LCL
D=M
@0
A=D+A
// Save value to Reg D
D=M
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

// pop local 0
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
@0
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

// push argument 0
// Get (ARG base + ith) pointer address
@ARG
D=M
@0
A=D+A
// Save value to Reg D
D=M
@SP
M=M+1
A=M-1
M=D

// push constant 1
@1
D=A
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

// pop argument 0
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save (argument base + ith) address to Reg D
@ARG
D=M
@0
D=D+A
// Store argument ptr to Reg 14
@14
M=D
// Load stored value, set A to correct segment pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment argument is done.
M=D

// push argument 0
// Get (ARG base + ith) pointer address
@ARG
D=M
@0
A=D+A
// Save value to Reg D
D=M
@SP
M=M+1
A=M-1
M=D

@SP
A=M
A=A-1
D=M
@SP
M=M-1
@LOOP_START
D; JNE

// push local 0
// Get (LCL base + ith) pointer address
@LCL
D=M
@0
A=D+A
// Save value to Reg D
D=M
@SP
M=M+1
A=M-1
M=D

(END)
@END
0;JMP
