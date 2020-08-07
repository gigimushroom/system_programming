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

class CodeWriter:
  def __init__(self, file_name):
    self.f = open(file_name, 'w')

  def writeArithmetic(self, cmd, debug=False):
    codes = []
    ops = []

    if cmd not in ['neg', 'not']:
      if cmd == 'add':
        ops = ['M=M+D // perform x + y']
      elif cmd == 'eq':
        """
        D=D-M // y = y-x
        @100  // a location
        D;JEQ // jump if eq
        M=-1 // set to False if not eq
        ...
        // at location 100
        (100)
        M=1  // set to True if eq
        """
        ops = [

        ]
      else:
        print(cmd, "not supported yet")
        exit(0)
      
      codes.extend(BINARY_CMD_PREFIX)
      codes.extend(ops)
      codes.extend(BINARY_CMD_SUFFIX)

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

