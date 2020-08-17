// push constant 3030
@3030
D=A
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

// push constant 3040
@3040
D=A
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

// push constant 32
@32
D=A
@SP
M=M+1
A=M-1
M=D

// pop this 2
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
@2
D=D+A
// Store this ptr to Reg 14
@14
M=D
// Load stored value, set A to correct segment pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment this is done.
M=D// push constant 46
@46
D=A
@SP
M=M+1
A=M-1
M=D

// pop that 6
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
@6
D=D+A
// Store that ptr to Reg 14
@14
M=D
// Load stored value, set A to correct segment pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment that is done.
M=D// push pointer 0
@THIS
D=M
@SP
M=M+1
A=M-1
M=D

// push pointer 1
@THAT
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

// push this 2
// Get (THIS base + ith) pointer address
@THIS
D=M
@2
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

// push that 6
// Get (THAT base + ith) pointer address
@THAT
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

(END)
@END
0;JMP
