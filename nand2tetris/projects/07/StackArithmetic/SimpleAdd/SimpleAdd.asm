// push constant 7
@7
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 8
@8
D=A
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
M=M+D // perform x + y
@SP // fix stack pointer
M=M-1

(END)
@END
0;JMP
