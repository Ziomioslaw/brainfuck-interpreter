import sys

class BrainfuckException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Memory():
    MAX = 3000

    def __init__(self):
        self.index = 0
        self.cells = []
        for x in range(0, self.MAX):
            self.cells.append(0)

    def incrementIndex(self):
        if self.index < self.MAX:
            self.index += 1
        else:
            raise BrainfuckException('Index cross maximum value')

    def decrementIndex(self):
        if self.index > 0:
            self.index -= 1
        else:
            raise BrainfuckException('Index cross minimum value')

    def incrementValue(self):
        self._setCellValue(self._getCellValue() + 1)

    def decrementValue(self):
        self._setCellValue(self._getCellValue() - 1)

    def outputValue(self):
        return self._getCellValue()

    def inputValue(self, character):
        self._setCellValue(character)

    def _getCellValue(self):
        if self.index >= 0 and self.index < self.MAX:
            return self.cells[self.index]
        else:
            raise BrainfuckException('Memory read index invaild value (' + str(self.index) + ')')

    def _setCellValue(self, value):
        if self.index >= 0 and self.index < self.MAX:
            self.cells[self.index] = value
        else:
            raise BrainfuckException('Memory read index invaild value')

class Command():
    VOID_POINTER = -1

    def __init__(self, character):
        self.character = character
        self.selfIndex = self.VOID_POINTER

    def setSelfIndex(self, index):
        self.selfIndex = index

    def getSelfIndex(self):
        return self.selfIndex

    def execute(self, memory):
        if self.character == '>':
            memory.incrementIndex()
        elif self.character == '<':
            memory.decrementIndex()
        elif self.character == '+':
            memory.incrementValue()
        elif self.character == '-':
            memory.decrementValue()
        elif self.character == '.':
            sys.stdout.write(chr(memory.outputValue()))
        elif self.character == ',':
            inputCharacter = sys.stdin.read(1)
            memory.inputValue(ord(inputCharacter))
        else:
            raise BrainfuckException('Unknow command: "' + self.character + '"')

        return -1

class JumpCommand(Command):
    def __init__(self, character):
        Command.__init__(self, character)
        self.jumpTo = self.VOID_POINTER

    def getJumpIndex(self):
        if self.jumpTo > self.VOID_POINTER:
            return self.jumpTo

        raise BrainfuckException('Jump index was not set')

    def setJumpIndex(self, jumpToIndex):
        self.jumpTo = jumpToIndex

    def execute(self, memory):
        value = memory.outputValue()
        if self.character == '[' and value == 0:
            return self.jumpTo
        elif self.character == ']' and value != 0:
            return self.jumpTo

        return -1

class Program():
    def __init__(self, commands, memory):
        self.commands = commands
        self.memory = memory

    def run(self):
        try:
            index = 0
            while index < len(self.commands):
                index = self._runCommand(index)
        except Exception as exception:
           command = self.commands[index].character
           raise BrainfuckException('Runtime error: "' + str(exception) + '". Operation: "' + command + '". Operation index: ' + str(index) + '.')

    def _runCommand(self, index):
        command = self.commands[index]
        result = command.execute(self.memory)
        return result if result != -1 else (index + 1)

class ProgramBuilder():
    def __init__(self):
        self.operations = []
        self.index = 0
        self.jumpStack = []

    def buildCommand(self, commandCharacter):
        if '+-<>,.'.find(commandCharacter) > -1:
            command = Command(commandCharacter)
            command.setSelfIndex(self.index)
        elif commandCharacter == '[':
            command = JumpCommand(commandCharacter)
            command.setSelfIndex(self.index)
            self.jumpStack.append(command)
        elif commandCharacter == ']':
            command = JumpCommand(commandCharacter)
            command.setSelfIndex(self.index)

            opening = self.jumpStack.pop()
            command.setJumpIndex(opening.getSelfIndex())
            opening.setJumpIndex(command.getSelfIndex())
        else:
            raise BrainfuckException("Unknown operation character: '" + commandCharacter + "'")

        self._appendCommand(command)

    def _appendCommand(self, command):
        self.index += 1
        self.operations.append(command)

    def __len__(self):
        return self.index

    def getProgram(self, memory):
        return Program(self.operations, memory)

class Parser():
    def __init__(self):
        pass

    def parse(self, inputStream):
        self._prepearEnvariement()

        for line in inputStream:
            for character in line:
                if not self._isCharacterOperation(character):
                    continue

                self.programBuilder.buildCommand(character)

        return self.programBuilder

    def _prepearEnvariement(self):
        self.programBuilder = ProgramBuilder()

    def _isCharacterOperation(self, character):
        return '+-<>[],.'.find(character) > -1
