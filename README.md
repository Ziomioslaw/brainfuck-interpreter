# Brainfuck interpreter

The interpreter for brainfuck language, written in Python.

## What is brainfuck?

Brainfuck is an esoteric programming language created in 1993 by Urban Müller, and notable for its extreme minimalism.

The language consists of only eight simple commands and an instruction pointer. While it is fully Turing-complete, it is not intended for practical use, but to challenge and amuse programmers.

The language's name is a reference to the slang term brainfuck, which refers to things so complicated or unusual that they exceed the limits of one's understanding.

See: [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)

## Usage of program

```bash
$ python brainfuck.py
Please use: brainfuck.py <brainfuck program file>
```

Call program with brainfuck script file as first parameter. Example:

```bash
$ python brainfuck.py brainfuckscripts/helloWorld.bf
Hello World!
```

## License

See LICENSE file.
