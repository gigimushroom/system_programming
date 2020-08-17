// push constant 111
@111
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 333
@333
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 888
@888
D=A
@SP
M=M+1
A=M-1
M=D

// pop static 8
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify Xxx.8 static value
@Xxx.8
M=D

// pop static 3
// Save top value in stack to Reg 13
@SP
A=M-1
D=M
@13
M=D 
// Fix stack ptr.
@SP
M=M-1
// Modify Xxx.3 static value
@Xxx.3
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
// Modify Xxx.1 static value
@Xxx.1
M=D

// push static 3
@Xxx.3
D=M
@SP
M=M+1
A=M-1
M=D

// push static 1
@Xxx.1
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

// push static 8
@Xxx.8
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
