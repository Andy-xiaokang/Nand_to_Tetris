# Nand2Tetris
一个vscode 上好用的工具[Nand2Tetris tools](https://marketplace.visualstudio.com/items?itemName=leafvmaple.nand2tetris&ssr=false#overview)  可以自动运行后生成.out 文件 并与.cmp 文件对比。以及自动压缩需要提交的文件，打开模拟器等。
运行程序方式可以 cmd + P 打开命令面板，**按下`>`终端命令提示符**， 然后才可以nand2tetris 模糊搜索对应命令。
## project0
提交文件，熟悉是否能够使用coursera提交作业。
## project1 Boolean logic
use primitive nand gates to yield a basic chip-set.  
pay attention to HDL  select two representative Chip's implementation

```HDL
CHIP Mux8Way16 {
    IN a[16], b[16], c[16], d[16],
       e[16], f[16], g[16], h[16],
       sel[3];
    OUT out[16];

    PARTS:
    // Put your code here:
    Mux4Way16(a=a, b=b, c=c, d=d, sel=sel[0..1], out=out1);
    Mux4Way16(a=e, b=f, c=g, d=h, sel=sel[0..1], out=out2);
    Mux16(a=out1, b=out2, sel=sel[2], out=out);
}
```
draw the true table and simplify the bool logic
```HDL
CHIP Mux {
    IN a, b, sel;
    OUT out;

    PARTS:
    // Put your code here:
    Not(in=sel, out=notsel);
    And(a=notsel, b=a, out=out1);
    And(a=b, b=sel, out=out2);
    Or(a=out1, b=out2, out=out);
}
```
## project2 Boolean Arithmetric
the main problem is ALU  
use Mux16 chip for control bit. zx nx zy ny f no etc.

```HDL
    Mux16(a=x, b=false, sel=zx, out=x1);
    Not16(in=x1, out=notx1);
    Mux16(a=x1, b=notx1, sel=nx, out=x2);
```

## Project03 Memory
1bit register -> 16bit register -> 8RAM -> 64RAM -> 512RAM -> 4KRAM -> 16KRAM  
use DMUX plus top address bits to load the `load` to the selected RAM   
use behinds bits to load the input  
use MUX and the top bits of address to output the selected RAM's output.
the main problem is PC  

```HDL
    Inc16(in=state, out=out1);
    Mux16(a=state, b=out1, sel=inc, out=out2);  //In most cases, the counter has to simply increment itself by 1 in each clock cycle
    Mux16(a=out2, b=in, sel=load, out=out3);
    Mux16(a=out3, b=false, sel=reset, out=out4);
    Register(in=out4, load=true, out=out, out=state);
```

