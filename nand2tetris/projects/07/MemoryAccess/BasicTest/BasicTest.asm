// push constant 10
@10
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
// Load stored value, set A to correct local pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment local is done.
M=D// push constant 21
@21
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 22
@22
D=A
@SP
M=M+1
A=M-1
M=D

// pop argument 2
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
@2
D=D+A
// Store argument ptr to Reg 14
@14
M=D
// Load stored value, set A to correct local pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment argument is done.
M=D// pop argument 1
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
@1
D=D+A
// Store argument ptr to Reg 14
@14
M=D
// Load stored value, set A to correct local pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment argument is done.
M=D// push constant 36
@36
D=A
@SP
M=M+1
A=M-1
M=D

// pop this 6
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save (this base + ith) address to Reg D
@THIS
D=M
@6
D=D+A
// Store this ptr to Reg 14
@14
M=D
// Load stored value, set A to correct local pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment this is done.
M=D// push constant 42
@42
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 45
@45
D=A
@SP
M=M+1
A=M-1
M=D

// pop that 5
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save (that base + ith) address to Reg D
@THAT
D=M
@5
D=D+A
// Store that ptr to Reg 14
@14
M=D
// Load stored value, set A to correct local pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment that is done.
M=D// pop that 2
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save (that base + ith) address to Reg D
@THAT
D=M
@2
D=D+A
// Store that ptr to Reg 14
@14
M=D
// Load stored value, set A to correct local pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment that is done.
M=D// push constant 510
@510
D=A
@SP
M=M+1
A=M-1
M=D

// pop temp 6
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Save TEMP memory segment pos(6) to Reg D
@11
D=A
// Store temp ptr to Reg 14
@14
M=D
// Load stored value, set A to correct local pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment temp is done.
M=D// push local 0
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

// push that 5
// Get (THAT base + ith) pointer address
@THAT
D=M
@5
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

// push argument 1
// Get (ARG base + ith) pointer address
@ARG
D=M
@1
A=D+A
// Save value to Reg D
D=M
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

// push this 6
// Get (THIS base + ith) pointer address
@THIS
D=M
@6
A=D+A
// Save value to Reg D
D=M
@SP
M=M+1
A=M-1
M=D

// push this 6
// Get (THIS base + ith) pointer address
@THIS
D=M
@6
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

// sub 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M - D // perform x - y, x is 2nd val, y is 1st val
@SP // fix stack pointer
M=M-1

// push temp 6
@11
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

(END)
@END
0;JMP
