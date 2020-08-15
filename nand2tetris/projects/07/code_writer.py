import sys

BINARY_CMD_PREFIX = [
  '@SP',
  'A=M // get stack pointer base address',
  'A=A-1 // get top-most value address',
  'D=M // store top-most value to register D',
  'A=A-1',
]
BINARY_CMD_SUFFIX = [
  '@SP // fix stack pointer',
  'M=M-1',
  '\n',
]

UNARY_CMD_PREFIX = [
  '@SP',
  'A=M // get stack pointer base address',
  'A=A-1 // get top-most value address',
  'D=M // store top-most value to register D',
]
UNARY_CMD_SUFFIX = [
  '\n',
]

FIND_2ND_VALUE_IN_STACK = [
  '@SP // Need to find the place to store EQ result.',
  'A=M // get stack pointer base address',
  'A=A-1 // get top-most value address',
  'A=A-1',
]

"""
      |x|
      |y|       
SP -> | |  
..........
after BINARY_CMD_PREFIX,
D is y, top value in stack
M is x, 2nd top value in stack

Example:
Push constant 892
Push constant 891
lt

We have: x = 892, y = 891
lt => x < y => 892 < 891 => False

"""

class CodeWriter:
  def __init__(self, file_name):
    self.f = open(file_name, 'w')
    self.label_start_index = -1

  def _get_next_label(self):
    self.label_start_index += 1
    return self.label_start_index

  def _gen_compare_cmds(self, op=''):
    if not op: 
      print("Error: no operation for compare command.")
      return None

    label = self._get_next_label()
    # Compare x and y
    ops = [
      'D= M - D // M(x) is 2nd val, D(y) is 1st val',
      '@LABEL_%d  // a location' % label,
      'D;%s // jump if satified comp' %op,
    ]
    # Set 2nd Value in Stack to -1 if not equal.
    ops.extend(FIND_2ND_VALUE_IN_STACK)
    ops.extend([
      'M=0 // set to 0 if False',
      '@LABEL_%d_DONE' % label,
      '0;JMP',
      '(LABEL_%d)' % label,
    ])
    # Set 2nd Value in Stack to 1 if equals.
    ops.extend(FIND_2ND_VALUE_IN_STACK)
    ops.extend([
      'M=-1  // set to 0xffff if True',
      '(LABEL_%d_DONE)' % label,
    ])
    return ops
  

  def writeArithmetic(self, cmd, debug=False):
    codes = []
    ops = []

    if cmd not in ['neg', 'not']:
      if cmd == 'add':
        ops = ['M= M + D // perform x + y']
      elif cmd == 'sub':
        ops = ['M= M - D // perform x - y, x is 2nd val, y is 1st val']
      elif cmd == 'and':
        ops = ['M= M & D // perform x & y']
      elif cmd == 'or':
        ops = ['M= M | D // perform x | y']
      elif cmd == 'eq':
        ops = self._gen_compare_cmds(op='JEQ')
      elif cmd == 'gt':
        ops = self._gen_compare_cmds(op='JGT')
      elif cmd == 'lt':
        ops = self._gen_compare_cmds(op='JLT')
      else:
        print(cmd, "not supported yet")
        exit(0)
      
      codes.extend(BINARY_CMD_PREFIX)
      codes.extend(ops)
      codes.extend(BINARY_CMD_SUFFIX)
    else:
      if cmd == 'neg':
        ops.append('M = -M // -y')
      else:
        ops.append('M = !M // Not y')

      codes.extend(UNARY_CMD_PREFIX)
      codes.extend(ops)
      codes.extend(UNARY_CMD_SUFFIX)

    if debug:
      print('\n'.join(codes))
    else:
      self.f.write('// %s \n' % cmd)
      self.f.write('\n'.join(codes))

  def writePushPop(self, cmd, segment, index, debug=False):
    codes = []

    if segment == 'constant':
      addr = '@%s' % index
      codes = [
        addr,
        'D=A',
        '@SP',
        'M=M+1',
        'A=M-1',
        'M=D',
        '\n',
      ]
    else:
      print('Segment not supported', segment)

    if debug:
      print('\n'.join(codes))
    else:
      self.f.write('// %s %s %s\n' % (cmd, segment, index))
      self.f.write('\n'.join(codes))

  def close(self):
    self.f.write('(END)\n')
    self.f.write('@END\n')
    self.f.write('0;JMP\n')
    
    self.f.close()


def test_writer():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 7)
  cw.writeArithmetic('add')
  cw.close()

def test_writer_eq1():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 7, debug=True)
  cw.writePushPop('push', 'constant', 6, debug=True)
  cw.writeArithmetic('eq', debug=True)
  cw.close()

def test_writer_eq2():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 7, debug=True)
  cw.writePushPop('push', 'constant', 7, debug=True)
  cw.writeArithmetic('eq', debug=True)
  cw.close()

def test_writer_sub():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 7, debug=True)
  cw.writePushPop('push', 'constant', 8, debug=True)
  cw.writePushPop('push', 'constant', 3, debug=True)
  cw.writeArithmetic('sub', debug=True)
  cw.close()

def test_writer_neg():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 7, debug=True)
  cw.writePushPop('push', 'constant', 3, debug=True)
  cw.writeArithmetic('neg', debug=True)
  cw.close()

def test_writer_eq3():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 17, debug=True)
  cw.writePushPop('push', 'constant', 17, debug=True)
  cw.writeArithmetic('eq', debug=True)
  cw.writePushPop('push', 'constant', 17, debug=True)
  cw.writePushPop('push', 'constant', 16, debug=True)
  cw.writeArithmetic('eq', debug=True)
  cw.close()

test_writer_eq3()
