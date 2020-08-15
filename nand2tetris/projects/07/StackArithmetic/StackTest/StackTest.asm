// push constant 17
@17
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 17
@17
D=A
@SP
M=M+1
A=M-1
M=D

// eq 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
D= M - D // D = x - y, x is 2nd val, y is 1st val
@LABEL_0  // a location
D;JEQ // jump if satified comp
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

// push constant 17
@17
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 16
@16
D=A
@SP
M=M+1
A=M-1
M=D

// eq 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
D= M - D // D = x - y, x is 2nd val, y is 1st val
@LABEL_1  // a location
D;JEQ // jump if satified comp
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=0 // set to 0 if False
@LABEL_1_DONE
0;JMP
(LABEL_1)
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=-1  // set to 0xffff if True
(LABEL_1_DONE)
@SP // fix stack pointer
M=M-1

// push constant 16
@16
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 17
@17
D=A
@SP
M=M+1
A=M-1
M=D

// eq 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
D= M - D // D = x - y, x is 2nd val, y is 1st val
@LABEL_2  // a location
D;JEQ // jump if satified comp
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=0 // set to 0 if False
@LABEL_2_DONE
0;JMP
(LABEL_2)
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=-1  // set to 0xffff if True
(LABEL_2_DONE)
@SP // fix stack pointer
M=M-1

// push constant 892
@892
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 891
@891
D=A
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
D= M - D // D = x - y, x is 2nd val, y is 1st val
@LABEL_3  // a location
D;JLT // jump if satified comp
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=0 // set to 0 if False
@LABEL_3_DONE
0;JMP
(LABEL_3)
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=-1  // set to 0xffff if True
(LABEL_3_DONE)
@SP // fix stack pointer
M=M-1

// push constant 891
@891
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 892
@892
D=A
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
D= M - D // D = x - y, x is 2nd val, y is 1st val
@LABEL_4  // a location
D;JLT // jump if satified comp
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=0 // set to 0 if False
@LABEL_4_DONE
0;JMP
(LABEL_4)
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=-1  // set to 0xffff if True
(LABEL_4_DONE)
@SP // fix stack pointer
M=M-1

// push constant 891
@891
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 891
@891
D=A
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
D= M - D // D = x - y, x is 2nd val, y is 1st val
@LABEL_5  // a location
D;JLT // jump if satified comp
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=0 // set to 0 if False
@LABEL_5_DONE
0;JMP
(LABEL_5)
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=-1  // set to 0xffff if True
(LABEL_5_DONE)
@SP // fix stack pointer
M=M-1

// push constant 32767
@32767
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D

// gt 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
D= M - D // D = x - y, x is 2nd val, y is 1st val
@LABEL_6  // a location
D;JGT // jump if satified comp
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=0 // set to 0 if False
@LABEL_6_DONE
0;JMP
(LABEL_6)
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=-1  // set to 0xffff if True
(LABEL_6_DONE)
@SP // fix stack pointer
M=M-1

// push constant 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 32767
@32767
D=A
@SP
M=M+1
A=M-1
M=D

// gt 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
D= M - D // D = x - y, x is 2nd val, y is 1st val
@LABEL_7  // a location
D;JGT // jump if satified comp
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=0 // set to 0 if False
@LABEL_7_DONE
0;JMP
(LABEL_7)
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=-1  // set to 0xffff if True
(LABEL_7_DONE)
@SP // fix stack pointer
M=M-1

// push constant 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D

// gt 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
D= M - D // D = x - y, x is 2nd val, y is 1st val
@LABEL_8  // a location
D;JGT // jump if satified comp
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=0 // set to 0 if False
@LABEL_8_DONE
0;JMP
(LABEL_8)
@SP // Need to find the place to store EQ result.
A=M // get stack pointer base address
A=A-1 // get top-most value address
A=A-1
M=-1  // set to 0xffff if True
(LABEL_8_DONE)
@SP // fix stack pointer
M=M-1

// push constant 57
@57
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 31
@31
D=A
@SP
M=M+1
A=M-1
M=D

// push constant 53
@53
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
M= M + D // perform x + y
@SP // fix stack pointer
M=M-1

// push constant 112
@112
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

// neg 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
M = -M // -y

// and 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M & D // perform x & y
@SP // fix stack pointer
M=M-1

// push constant 82
@82
D=A
@SP
M=M+1
A=M-1
M=D

// or 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
A=A-1
M= M | D // perform x | y
@SP // fix stack pointer
M=M-1

// not 
@SP
A=M // get stack pointer base address
A=A-1 // get top-most value address
D=M // store top-most value to register D
M = !M // Not y

(END)
@END
0;JMP
