

class VMWriter:
  def __init__(self):
    self.contents = []

  def writePush(self, segment, index):
    cmd = 'push %s %s' % (segment, index)
    print(cmd)
    self.contents.append(cmd)

  def writePop(self, segment, index):
    cmd = 'pop %s %s' % (segment, index)
    print(cmd)
    self.contents.append(cmd)


  def writeArithmetic(self, cmd):
    print(cmd)
    self.contents.append(cmd)

  def writeLabel(self, label):
    self.contents.append('label %s' % label)

  def writeGoto(self, label):
    self.contents.append('goto %s' % label)

  def writeIf(self, label):
    self.contents.append('if-goto %s' % label)
  
  def writeFunction(self, name, nLocals):
    cmd = 'function %s %d' % (name, nLocals)
    print(cmd)
    self.contents.append(cmd)

  def writeCall(self, name, nArgs, ignore_ret=False):
    cmd = 'call %s %s' % (name, nArgs)
    print(cmd)
    self.contents.append(cmd)

    if ignore_ret:
      self.writePop('temp', 0)


  def writeReturn(self):
    print('return')
    self.contents.append('return')


  def writeToVMFile(self, output):
    with open(output, 'w') as f:
      for c in self.contents:
        # if not c.startswith('label'):
        #   c = '  ' + c
        f.write("%s\n" % c)
