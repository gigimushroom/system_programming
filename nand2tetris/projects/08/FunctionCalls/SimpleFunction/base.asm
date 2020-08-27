(SimpleFunction.test)
// push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 0
@0
D=A
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

// push local 1
// Get (LCL base + ith) pointer address
@LCL
D=M
@1
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

// not 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
M = !M // Not y

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