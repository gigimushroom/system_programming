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

(Main.fibonacci)
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

// push constant 2
@2
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// lt
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
D= M - D // M(x) is 2nd val, D(y) is 1st val
@LABEL_0  // a location
D;JLT // jump if satified comp
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=0 // set to 0 if False
@LABEL_0_DONE
0;JMP
(LABEL_0)
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=-1  // set to 0xffff if True
(LABEL_0_DONE)
@SP // fix stack pointer
M=M-1

@SP
A=M
A=A-1
D=M
@SP
M=M-1
@IF_TRUE
D; JNE

@IF_FALSE
0; JMP

(IF_TRUE)
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

(IF_FALSE)
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

// push constant 2
@2
D=A
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

// Push return address 240
// Use the memory location of the command following the function call
@240
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
// Go to function(Main.fibonacci)
@Main.fibonacci
0; JMP
// Declare a label for return address. It is current lines no. 240!
(240)

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

// push constant 1
@1
D=A
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

// Push return address 308
// Use the memory location of the command following the function call
@308
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
// Go to function(Main.fibonacci)
@Main.fibonacci
0; JMP
// Declare a label for return address. It is current lines no. 308!
(308)

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

(Sys.init)
// push constant 4
@4
D=A
// Save value from D to stack
@SP
M=M+1
A=M-1
M=D

// Push return address 421
// Use the memory location of the command following the function call
@421
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
// Go to function(Main.fibonacci)
@Main.fibonacci
0; JMP
// Declare a label for return address. It is current lines no. 421!
(421)

(WHILE)
@WHILE
0; JMP

(END)
@END
0;JMP
