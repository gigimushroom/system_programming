@66
D=A
@SP
M=M+1
A=M-1
M=D


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
// Load stored value, set A to correct local pointer
@13
D=M
@14
A=M
// Pop from stack to memory segment temp is done.
M=D
@33
D=A
@SP
M=M+1
A=M-1
M=D


@6
D=M
@SP
M=M+1
A=M-1
M=D


