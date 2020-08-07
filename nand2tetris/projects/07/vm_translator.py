import sys
import code_writer


C_PUSH = 'push'
C_POP = 'pop'
C_ARITHMETIC = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}

class Parser:
  def __init__(self, file_name):
    self.cur_index = -1
    self.contents = []

    with open(file_name) as f:
      for line in f:
        # partition returns a tuple: 
        # everything before the partition string, the partition string,
        # and everything after the partition string. 
        # So, by indexing with [0] we take just the part before 
        # the partition string.
        line = line.partition('//')[0]
        line = line.strip()
        if line:
          self.contents.append(line)

  def hasMoreCommands(self):
    if not self.contents:
      return False

    return self.cur_index < len(self.contents) - 1

  def advance(self):
    self.cur_index += 1
    cmd = self.contents[self.cur_index]
    self.cmds = cmd.split()

  def commandType(self):
    if not self.cmds:
      return None

    if self.cmds[0] == C_PUSH:
      return C_PUSH
    elif self.cmds[0] in C_ARITHMETIC:
      return self.cmds[0]

    return None

  def arg1(self):
    if self.commandType() in C_ARITHMETIC:
      return self.cmds[0]
    else:
      return self.cmds[1]

  def arg2(self):
    if len(self.cmds) < 2:
      print("cmds does not have arg2", self.cmds)
      return None

    return self.cmds[2]



file_name = sys.argv[1]
parser = Parser(file_name)

output = sys.argv[2]
cw = code_writer.CodeWriter(output)

while parser.hasMoreCommands():
  parser.advance()

  cmd_type = parser.commandType()
  if cmd_type in [C_PUSH, C_POP]:
    print(cmd_type, parser.arg1(), parser.arg2()) 
    cw.writePushPop(cmd_type, parser.arg1(), parser.arg2())
  else:
    print(parser.arg1())
    cw.writeArithmetic(parser.arg1())

cw.close()
