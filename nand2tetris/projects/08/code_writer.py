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

TEMP_REG_START_INDEX = 5

POP_TOP_MOST_FROM_STACK = [
  # Store topmost value to Reg D.
  '@SP',
  'A=M',
  'A=A-1',
  'D=M',
  # Fix up stack pointer.
  '@SP',
  'M=M-1',
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
    # Set 2nd Value in Stack to 0 if not equal.
    ops.extend(FIND_2ND_VALUE_IN_STACK)
    ops.extend([
      'M=0 // set to 0 if False',
      '@LABEL_%d_DONE' % label,
      '0;JMP',
      '(LABEL_%d)' % label,
    ])
    # Set 2nd Value in Stack to 0xffff(-1) if equals.
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

  def _get_reg_name_from_segment(self, segment):
    if segment == 'local':
      reg = 'LCL'
    elif segment == 'argument':
      reg = 'ARG'
    elif segment == 'this':
      reg = 'THIS'
    elif segment == 'that':
      reg = 'THAT'
    else:
      reg = None
    
    return reg

  def _gen_push_cmd(self, segment, index):
    register = None
    codes = None

    suffix_push_to_sp = [
      '@SP',
      'M=M+1',
      'A=M-1',
      'M=D',
      '\n',
    ]

    # We store the value we want to push to Register D.
    if segment == 'constant':
      codes = [
        '@%s' % index,
        'D=A',
      ]
    elif segment == 'temp':
      # TEMP segment holds values from Reg[5 - 12]
      # To get 6th, we need to: 5 + 6
      pos = TEMP_REG_START_INDEX + int(index)
      codes = [
        '@%s' % pos,
        'D=M',
      ]
    elif segment == 'pointer':
      ptr = 'THIS' if int(index) == 0 else 'THAT'
      codes = [
        '@%s' % ptr,
        'D=M',
      ]
    elif segment == 'static':
      sym = 'Xxx.%s' % index
      codes = [
        '@%s' % sym,
        'D=M',
      ]
    else:
      reg = self._get_reg_name_from_segment(segment)
      codes = [
        '// Get (%s base + ith) pointer address' % reg,
        '@%s' % reg,
        'D=M',
        '@%s' % index,
        'A=D+A',
        '// Save value to Reg D',
        'D=M',
      ]

    codes.extend(suffix_push_to_sp)

    return codes

  def _gen_pop_cmd(self, segment, index):
    POP_PREFIX = [
      '// Save top value in stack to Reg 13',
      '@SP',
      'A=M-1',
      'D=M',
      '@13',
      'M=D ',
      '// Fix stack ptr.',
      '@SP',
      'M=M-1',
    ]

    if segment == 'temp':
      pos = TEMP_REG_START_INDEX + int(index)
      contents = [
        '// Save TEMP memory segment pos(%s) to Reg D' % index,
        '@%s' % pos,
        'D=A',
      ]
    elif segment == 'pointer':
      # Pointer case is special. It only modify THIS or That register.
      ptr = 'THIS' if int(index) == 0 else 'THAT'
      codes = POP_PREFIX
      contents = [
        '// Modify %s pointer' % ptr,
        '@%s' % ptr,
        'M=D',
        '\n',
      ]
      codes.extend(contents)
      return codes
    elif segment == 'static':
      # Save content from Reg D to correct Register symbol.
      sym = 'Xxx.%s' % index
      codes = POP_PREFIX
      contents = [
        '// Modify %s static value' % sym,
        '@%s' % sym,
        'M=D',
        '\n',
      ]
      codes.extend(contents)
      return codes

    else:
      reg = self._get_reg_name_from_segment(segment)
      contents = [
        '// Save (%s base + ith) address to Reg D' % segment,
        '@%s' % reg,
        'D=M',
        '@%s' % index,
        'D=D+A',
      ]
    
    # We want to transfer the data from top in stack, to memory segment
    # correct location. We have to use some registers for help.
    POP_SUFFIX = [
      '// Store %s ptr to Reg 14' % segment,
      '@14',
      'M=D',
      '// Load stored value, set A to correct segment pointer',
      '@13',
      'D=M',
      '@14',
      'A=M',
      '// Pop from stack to memory segment %s is done.' % segment,
      'M=D',
      '\n',
    ]
    
    codes = POP_PREFIX
    codes.extend(contents)
    codes.extend(POP_SUFFIX)
    
    return codes

  def writePushPop(self, cmd, segment, index, debug=False):
    if cmd == 'push':
      codes = self._gen_push_cmd(segment, index)
    else:
      codes = self._gen_pop_cmd(segment, index)

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

  def writeInit(self):
    pass

  def writeLabel(self, label, debug=False):
    cmd = '(%s)\n' % label

    if debug:
      print(cmd)
    else:
      self.f.write(cmd)

  def writeGoto(self, label):
    codes = [
      '@%s' % label,
      '0; JMP',
      '\n',
    ]

    self.f.write('\n'.join(codes))

  def writeIf(self, label, debug=False):
    codes = POP_TOP_MOST_FROM_STACK
    codes.extend([
      '@%s' % label,
      'D; JNE',
      '\n',
    ])

    if debug:
      print('\n'.join(codes))
    else:
      self.f.write('\n'.join(codes))

  def writeCall(self):
    pass

  def writeReturn(self, debug=False):
    """ The key of return is to reset to beginning.
    When call a function, we push args, and save registers, set locals, etc
    After return, we want to go back to the 1st arg, 
    and save our return value there.
    Then, we set Stack Pointer to ARG + 1.
    Thus, we clear all the rest of contents in stack below.
    """

    # Frame = LCL, Save as temp
    codes = [
      '// Save LCL(Frame) to Reg 13',
      '@LCL',
      'D=M',
      '@13',
      'M=D',
    ]

    # RET = *(FRAME - 5)
    codes.extend([
      '// RET = *(FRAME - 5)',
      'D=D-1',
      'D=D-1',
      'D=D-1',
      'D=D-1',
      'A=D-1',
      'D=M // de-reference return address',
      '@14',
      'M=D // Save the return address',
    ])

    # Reposition the return value for the caller, set to 1st arg
    # *ARG = pop()
    codes.extend([
      '// Pop topmost from stack',
      '@SP',
      'A=M',
      'A=A-1',
      'D=M',
      '// Fix stack pointer after pop',
      '@SP',
      'M=M-1',
      '// Save the pop-ed value to arg 0',
      '@ARG',
      'A=M',
      'M=D',
    ])

    # Restore SP of the caller
    # SP = ARG + 1
    codes.extend([
      '@ARG',
      'D=M+1',
      '@SP',
      'M=D',
    ])

    # Restore the rest
    # THAT = * (FRAME - 1)
    codes.extend([
      '// THAT = * (FRAME - 1)',
      '@13',
      'A=M-1',
      'D=M // de-reference THAT ptr',
      '@THAT',
      'M=D // Restore THAT ptr',
    ])

    # THIS = * (FRAME - 2)
    codes.extend([
      '// THIS = * (FRAME - 2)',
      '@13',
      'A=M-1',
      'A=A-1',
      'D=M // de-reference THIS ptr',
      '@THIS',
      'M=D // Restore THIS ptr',
    ])

    # ARG = * (FRAME - 3)
    codes.extend([
      '// ARG = * (FRAME - 3)',
      '@13',
      'A=M-1',
      'A=A-1',
      'A=A-1',
      'D=M // de-reference ARG ptr',
      '@ARG',
      'M=D // Restore ARG ptr',
    ])

    # LCL = * (FRAME - 4)
    codes.extend([
      '// LCL = * (FRAME - 4)',
      '@13',
      'A=M-1',
      'A=A-1',
      'A=A-1',
      'A=A-1',
      'D=M // de-reference LCL ptr',
      '@LCL',
      'M=D // Restore LCL ptr',
    ])

    # goto RET
    codes.extend([
      '@14',
      'A=M',
      '0; JMP',
      '\n',
    ])

    if debug:
      print('\n'.join(codes))
    else:
      self.f.write('\n'.join(codes))

  def writeFunction(self, func_name, num_of_locals, debug=False):
    self.writeLabel(func_name, debug=debug)

    for i in range(int(num_of_locals)):
      self.writePushPop('push', 'constant', 0, debug=debug)


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

def test_writer_pop_local():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 10, debug=True)
  cw.writePushPop('pop', 'local', 0, debug=True)

def test_writer_pop_args():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 21, debug=True)
  cw.writePushPop('push', 'constant', 22, debug=True)
  cw.writePushPop('pop', 'argument', 2, debug=True)
  cw.writePushPop('pop', 'argument', 1, debug=True)

def test_push_local():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 99, debug=True)
  cw.writePushPop('pop', 'local', 1, debug=True)
  cw.writePushPop('push', 'constant', 33, debug=True)
  cw.writePushPop('push', 'local', 1, debug=True)

def test_push_pop_temp():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 66, debug=True)
  cw.writePushPop('pop', 'temp', 1, debug=True)
  cw.writePushPop('push', 'constant', 33, debug=True)
  cw.writePushPop('push', 'temp', 1, debug=True)

def test_pop_pointer():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 3030, debug=True)
  cw.writePushPop('pop', 'pointer', 0, debug=True)

def test_pop_pointer2():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 3030, debug=True)
  cw.writePushPop('pop', 'pointer', 0, debug=True)
  cw.writePushPop('push', 'constant', 66, debug=True)
  cw.writePushPop('push', 'pointer', 0, debug=True)

def test_push_pop_static():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 111, debug=True)
  cw.writePushPop('pop', 'static', 8, debug=True)
  cw.writePushPop('push', 'constant', 888, debug=True)
  cw.writePushPop('push', 'static', 8, debug=True)

def test_goto():
  cw = CodeWriter('xxx.asm')
  cw.writePushPop('push', 'constant', 10, debug=True)
  cw.writeLabel('LOOP_START', debug=True)
  cw.writePushPop('pop', 'local', 0, debug=True)
  cw.writeIf('LOOP_START', debug=True)

def test_simple_func():
  cw = CodeWriter('xxx.asm')
  cw.writeFunction('SimpleFunction.test', 2, debug=True)
  cw.writeReturn(debug=True)

#test_simple_func()
