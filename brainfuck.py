import sys
import os
import brainfuckinterpreter

if len(sys.argv) > 1:
    path = os.path.abspath(sys.argv[1])
    programFile = open(path, 'r')
    parser = brainfuckinterpreter.Parser()

    builder = parser.parse(programFile)
    program = builder.getProgram()

    program.run(brainfuckinterpreter.Memory(), sys.stdout, sys.stdin)
else:
    print('Please use: brainfuck.py <file>')
