# Project 11 Compiler II Code Generation

Created: Sep 11, 2020 10:57 AM
Tags: compiler

This will be the end of the four-module journey in which you've developed a two-tier compiler, based on a backend virtual machine.

## Learning

### Handling nested scoping

![Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-11_at_3.54.36_PM.png](Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-11_at_3.54.36_PM.png)

### Rules

Object data is accessed via the `this` segment

Array data is accessed via the `that` segment

Before using these segments, we must first anchor them using `pointer`

`pop pointer 0` : Pop top-most value from stack and save in `this` register (Mem addr 3)

# Object

All OOP code will be translated to Procedural VM Code!

## Object Manipulation

![Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/2020-09-12_9.14.20.png](Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/2020-09-12_9.14.20.png)

JACK code: `p1.distance(p2)`

Translated VM code:

```jsx
push p1
push p2
call p1.distance
```

As u can see, p1 is always argument 0!

For the method distance VM code, we have:

```jsx
push argument 0
pop pointer 0
```

We know arg 0 has the `object`, so push to stack. Pop it to pointer 0 (THIS register).

From now on, our THIS pointer is pointed to the object.

For code: `x - other.get();`

We look up `x` in class level symbol table, it has index 0.

So we generate `push this 0`

Interestingly, this is very similar to python `self`!!!

## Handling Arrays

### Set this and that

![Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_10.04.51_AM.png](Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_10.04.51_AM.png)

### Array access

![Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_10.09.09_AM.png](Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_10.09.09_AM.png)

**I think:**

These VM instructions work but not great.

It treats address of `arr + 2` as array start, and set value. Use `pop that 0`

The common sense is to have `that` pointer set to `arr`, then navigate to 3rd element and set it.

```python
push arr
pop pointer 1
push 17
pop that 2
```

**However,**

Actually! The common sense code only works for constant offsets (indices)!

The simple code cannot be used when the source statement is, say, “let arr[x] = y”

## Complex Array Access

![Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_10.26.57_AM.png](Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_10.26.57_AM.png)

### General solution

![Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_10.28.18_AM.png](Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_10.28.18_AM.png)

Store LHS address of `arr + i` to stack.

Save RHS result to temp.

Set `THAT` pointer.

Save result to correct location in array.

## Loop

![Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/IMG_20200922_150044.jpg](Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/IMG_20200922_150044.jpg)

Same thing for `for loop`

```python
for(;cond;++) { s1 }
```

```python
Label L1
  computing ~(cond)
  if-goto L2
  vm code for s1
  ++/-- vm code
  goto L1

L2
...
```

# Implementation

### Example

![Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_4.01.09_PM.png](Project%2011%20Compiler%20II%20Code%20Generation%207ef1d408eb26494597f6f2d2cebea895/Screen_Shot_2020-09-14_at_4.01.09_PM.png)

### Compile control structures

```
if (cond)
      s1
    else
      s2
```

Convert to VM code:

```
  computing ~(cond)
  if-goto L1
  s1
  goto L2
label L1
  s2
label L2
```

## Case study

```python
class Square {

   field int x, y; // screen location of the square's top-left corner
   field int size; // length of this square, in pixels

   /** Constructs a new square with a given location and size. */
   constructor Square new(int Ax, int Ay, int Asize) {
      let x = Ax;
      let y = Ay;
      let size = Asize;
      do draw();
      return this;
   }
```

### Handle method calling method

`do draw()` is an internal method, called from constructor.

We need to push THIS, as argument 0.

Then, `call Square.draw 0`

## Debug Pong issue

Use baseline bat.vm from provided Compiler.sh

Found out bat.vm having issue. The problem is the bat cannot move by keyboard.

The fix is:

When generating VM code for method impl, argument 0 is for `this`, all listed arguments must start from index 1. Thus, push `this` to symbol table argument hash table, and everything works.

```python
method foo(int arg_1) { ... }
```