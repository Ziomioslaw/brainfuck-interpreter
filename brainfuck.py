import sys
import os
import brainfuckinterpreter

if len(sys.argv) > 1:
    path = os.path.abspath(sys.argv[1])
    programFile = open(path, 'r')
    parser = brainfuckinterpreter.BrainfuckParser()

    builder = parser.parse(programFile)
    program = builder.getBrainfuckProgram(brainfuckinterpreter.BrainfuckMemory())

    program.run()
else:
    print('Please use: brainfuck.py <file>')
