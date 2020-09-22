
STATIC = 'static'
FIELD = 'field'
ARG = 'argument'
VAR = 'local'

CLASS_SCOPE = [STATIC, FIELD]
SUB_ROUTINE_SCOPE = [ARG, VAR]
VALID_SCOPE = [STATIC, FIELD, ARG, VAR]

class SymbolTable:
  def __init__(self):
    self.class_table = {}
    self.subroutine_table = {}

    self.class_table[STATIC] = {}
    self.class_table[FIELD] = {}

    self.subroutine_table[ARG] = {}
    self.subroutine_table[VAR] = {}

  def startSubroutine(self):
    #self.display()
    #print('DEBUG start new sub routine!')
    self.subroutine_table[ARG] = {}
    self.subroutine_table[VAR] = {}

  def create(self, name, var_type, kind):
    name = name.strip()
    index = self.VarCount(kind)

    if kind in CLASS_SCOPE:
      self.class_table[kind][name] = (index, var_type) 

    elif kind in SUB_ROUTINE_SCOPE:
      self.subroutine_table[kind][name] = (index, var_type) 

    else:
      #print('Invalid type!')
      return False

    return True

  def VarCount(self, kind):
    if kind in CLASS_SCOPE and self.class_table:
        return len(self.class_table[kind])

    elif kind in SUB_ROUTINE_SCOPE and self.subroutine_table:
        return len(self.subroutine_table[kind]) 
    
    return -1

  def KindOf(self, name):
    # Return the kind(static, field, arg, or var) of the identifier
    # in current scope.
    if len(self.subroutine_table) > 0:
      for k in SUB_ROUTINE_SCOPE:
        if name in self.subroutine_table[k]:
          # Each value is (index, type)
          return k
    
    for k in CLASS_SCOPE:
      if name in self.class_table[k]:
        return k

    return None

  def TypeOf(self, name):
    # Return type(int, string, etc) of the identifier.
    print('searching...', name)

    if len(self.subroutine_table) > 0:
      for k in SUB_ROUTINE_SCOPE:
        if name in self.subroutine_table[k]:
          # Each value is (index, type)
          return self.subroutine_table[k][name][1]
    
    for k in CLASS_SCOPE:
      if name in self.class_table[k]:
        return self.class_table[k][name][1]

    return None

  def IndexOf(self, name):
    # Return index assigned to the identifier.
    if len(self.subroutine_table) > 0:
      for k in SUB_ROUTINE_SCOPE:
        if name in self.subroutine_table[k]:
          # Each value is (index, type)
          return self.subroutine_table[k][name][0]
    
    for k in CLASS_SCOPE:
      if name in self.class_table[k]:
        return self.class_table[k][name][0]

    return -1

  def display(self):
    print('Class table', self.class_table)
    print('Sub table', self.subroutine_table)


def test_symbol_table():
  tb = SymbolTable()
  tb.create('baba', 'int', STATIC)
  tb.create('wawa', 'int', STATIC)
  tb.create('diudiu', 'int', STATIC)
  tb.create('mama', 'string', ARG)
  tb.display()
  print('type of diudiu is', tb.KindOf('diudiu'))
  print('type of mama is', tb.KindOf('mama'))

  print('type of diudiu is', tb.IndexOf('diudiu'))
  print('type of mama is', tb.IndexOf('mama'))

  print('type of diudiu is', tb.TypeOf('diudiu'))
  print('type of mama is', tb.TypeOf('mama'))

#test_symbol_table()

