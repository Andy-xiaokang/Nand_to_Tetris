@256
D=A
@SP
M=D
@bootstrap
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(bootstrap)
(Sys.init)
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@0
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@1
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@Sys.main$ret0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(Sys.main$ret0)
@5
D=A
@1
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
(Sys.init$LOOP)
@Sys.init$LOOP
0;JMP
(Sys.main)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@0
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@1
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@1
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@2
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@3
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
@Sys.add12$ret1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(Sys.add12$ret1)
@5
D=A
@0
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@LCL
D=M
@0
D=A+D
@R15
M=D
@R15
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@1
D=A+D
@R15
M=D
@R15
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@2
D=A+D
@R15
M=D
@R15
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@3
D=A+D
@R15
M=D
@R15
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@4
D=A+D
@R15
M=D
@R15
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
@SP
AM=M-1
D=M
A=A-1
M=M+D
@SP
AM=M-1
D=M
A=A-1
M=M+D
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
D=M
@R13
M=D
@5
D=A
@R13
A=M-D
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@1
D=A
@R13
A=M-D
D=M
@THAT
M=D
@2
D=A
@R13
A=M-D
D=M
@THIS
M=D
@3
D=A
@R13
A=M-D
D=M
@ARG
M=D
@4
D=A
@R13
A=M-D
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Sys.add12)
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@0
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@1
D=A+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@ARG
D=M
@0
D=A+D
@R15
M=D
@R15
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@12
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
D=M
@R13
M=D
@5
D=A
@R13
A=M-D
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@1
D=A
@R13
A=M-D
D=M
@THAT
M=D
@2
D=A
@R13
A=M-D
D=M
@THIS
M=D
@3
D=A
@R13
A=M-D
D=M
@ARG
M=D
@4
D=A
@R13
A=M-D
D=M
@LCL
M=D
@R14
A=M
0;JMP
