// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

    @8192
    D = A 
    @n 
    M = D // n = 8K

(LOOP)
    @SCREEN
    D = A 
    @address
    M = D // address = 16384

    @i
    M = 0 // initialise i = 0

    @KBD
    D = M 
    @BLACK
    D;JGT  //if KBD value > 0 jump to black

    @KBD
    D = M 
    @WHITE
    D;JMP // if KBD value = 0 jump to white

    (WHITE)
        @i
        D = M 
        @n 
        D = D - M 
        @LOOP
        D;JGE //if i - n >= 0 jmp to loop

        @address
        A = M 
        M = 0 

        @address
        M = M + 1  //address = address + 1

        @i
        M = M + 1  // i = i + 1

        @WHITE
        0;JMP


    (BLACK)
        @i
        D = M 
        @n 
        D = D - M 
        @LOOP
        D;JGE //if i - n >= 0 jmp to loop

        @address
        A = M 
        M = -1 

        @address
        M = M + 1  //address = address + 1

        @i
        M = M + 1  //i = i + 1

        @BLACK
        0;JMP 

    @LOOP
    0;JMP