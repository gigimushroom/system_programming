import sys
import code_writer
import os
from os import listdir
from os.path import isfile, join


C_PUSH = 'push'
C_POP = 'pop'
C_ARITHMETIC = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}
# Project 8
C_LABEL = 'label'
C_GOTO = 'goto'
C_IF = 'if-goto'
C_FUNCTION  = 'function'
C_RETURN = 'return'
C_CALL = 'call'


class Parser:
  def __init__(self, file_name):
    self.cur_index = -1
    self.contents = []
    self.func_scope = 'main'

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
    if self.cmds[0] == C_POP:
      return C_POP 
    elif self.cmds[0] in C_ARITHMETIC:
      return self.cmds[0]

    return self.cmds[0]

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


def parse_a_file(file_name, cw):
  parser = Parser(file_name)
  while parser.hasMoreCommands():
    parser.advance()
    #print('...', parser.cmds)
    cmd_type = parser.commandType()
    if cmd_type in [C_PUSH, C_POP]:
      #print(cmd_type, parser.arg1(), parser.arg2()) 
      cw.writePushPop(cmd_type, parser.arg1(), parser.arg2())

    elif cmd_type in C_ARITHMETIC:
      #print(parser.arg1())
      cw.writeArithmetic(parser.arg1())

    elif cmd_type == C_LABEL:
      print('Writing label:', parser.arg1())
      cw.writeLabel(parser.arg1())

    elif cmd_type == C_IF:
      print('Writing if-goto:', parser.arg1())
      cw.writeIf(parser.arg1())
    
    elif cmd_type == C_GOTO:
      print('Writing goto:', parser.arg1())
      cw.writeGoto(parser.arg1())

    elif cmd_type == C_FUNCTION:
      print('Writing function:', parser.arg1(), parser.arg2())
      cw.writeFunction(parser.arg1(), parser.arg2())

    elif cmd_type == C_CALL:
      print('Writing Call:', parser.arg1(), parser.arg2())
      cw.writeCall(parser.arg1(), parser.arg2())

    elif cmd_type == C_RETURN:
      print('Writing return')
      cw.writeReturn()

file_name = sys.argv[1]
if os.path.isfile(file_name):
  output = '%s.asm' % os.path.splitext(file_name)[0]
  cw = code_writer.CodeWriter(output)
  cw.set_input_f_name(file_name)
  parse_a_file(file_name, cw)

else:
  dir_name = sys.argv[1]
  # Get last part of dirtectory name. Example: a/b => b
  output = '%s.asm' % os.path.basename(dir_name)
  print(dir_name, output) 
  cw = code_writer.CodeWriter(join(dir_name, output))
  cw.writeInit()

  for f in listdir(dir_name):
    if isfile(join(dir_name, f)) and f.endswith('.vm'):
      cw.set_input_f_name(f)
      parse_a_file(join(dir_name, f), cw)

cw.close()
