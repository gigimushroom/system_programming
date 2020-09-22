# A LL(1) Parser

import xml.etree.cElementTree as ET
import sys
import os
import lib
import SymbolTable as SB
import VMWriter as VM

OP_LIST = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARYOP_LIST = ['-', '~']


class Parser:
  def __init__(self, input, is_input_str=False, output=None):
    self.output = output
    self.tokens = []
    self.index = 0
    self.root = ET.Element("class")
    self.parent = self.root
    self.output = output

    if not is_input_str:
      tree = ET.parse(input)
      root = tree.getroot()
    else:
      root = ET.fromstring(input)

    for c in root:
      t = (c.tag, c.text)
      self.tokens.append(t)

    self.symbol_tb = SB.SymbolTable()
    self.class_name = None
    self.vm_writer = VM.VMWriter()
    self.label_index = 0

  def WriteAsFile(self):
    tree = ET.ElementTree(self.root)
    lib.indent(self.root)

    tree.write(file_or_filename=self.output, short_empty_elements=False)

  def eat(self, token=None, category=None, var_type=''):
    tag, text = self.tokens[self.index]

    if token:
      tt = lib.pretty_token(token)
      if text != tt:
        raise ValueError('Invalid token!', self.index, tag, text, token)
    
    text = text.strip()
    
    if tag == 'identifier':
      # Look at next token, if it is '.', skip because we are looking at
      # function call. Example: a.foo()
      _, next_token = self.tokens[self.index + 1]
      # Look at prev token. Skip if it is function name. Example: foo
      _, prev_token = self.tokens[self.index - 1]

      if next_token.strip() != '.' and prev_token.strip() != '.':
        existed = 'used'
        my_kind = ''
        my_type = ''
        my_index = ''
        if self.symbol_tb.IndexOf(text) == -1 and category in SB.VALID_SCOPE:
          existed = 'defined'
          #print(text, category)
          # Got an indentifier to save in Symbol table.
          result = self.symbol_tb.create(text, var_type=var_type, kind=category)
          if not result:
            print('Fail to create symbol for', text, category)
          if var_type == '':
            print('Error on creating symbol', text, category, self.index)

        my_kind = self.symbol_tb.KindOf(text)
        my_type = self.symbol_tb.TypeOf(text)
        my_index = self.symbol_tb.IndexOf(text)
        
        text = '%s present(%s) kind(%s) type(%s) index(%d)' % \
              (text, existed, my_kind, my_type, my_index)
        print(text)
        #self.symbol_tb.display()

    # node = self._writeNode(tag, text, self.parent)
    self.index += 1
    # return node

  def _writeNode(self, tag, text, parent):
    node = ET.SubElement(parent, tag)

    # TODO: plug in symbol table
    node.text = text
    return node

  def WriteToDisk(self, output):
    self.vm_writer.writeToVMFile(output)

  def CompileClass(self):
    self.eat('class')

    self.class_name = self._getTokenText()
    self.eat(category='class')

    self.eat('{')

    # Handle one or many class vars.
    while (self.peakClassVar()):
      self.CompileClassVarDec()

    while(self.peakSubRoutine()):
      self.CompileSubroutineDec()

    self.eat('}')

    print('Lastest symbol table')
    self.symbol_tb.display()

  def peakClassVar(self):
    # Check if the token belongs to class var.
    tag, text = self.tokens[self.index]
    if tag != 'keyword':
      return False

    if 'static' in text or 'field' in text:
      return True

    return False

  def CompileClassVarDec(self):
    cached_parent = self.parent
    var_dec_node = ET.SubElement(self.parent, 'classVarDec')

    self.parent = var_dec_node
    
    category = self._getTokenText()
    self.eat() # static or field

    ident_type = self._getTokenText()
    self.eat() # type

    self.eat(category=category, var_type=ident_type) # varName

    tt = self._getTokenText()
    while (tt == ','):
      self.eat(',')

      ident_type = self._getTokenText()
      self.eat(category=category, var_type=ident_type) # var name

      tt = self._getTokenText()

    self.eat(';')

    self.parent = cached_parent

  def peakSubRoutine(self):
    tag, text = self.tokens[self.index]
    if text.strip() in ['constructor', 'function', 'method']:
      return True

    return False

  def _is_contructor(self, token):
    return token == 'constructor'

  def _is_method(self, token):
    return token == 'method'

  def CompileSubroutineDec(self):
    self.symbol_tb.startSubroutine()

    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'subroutineDec')
    self.parent = sub_node

    func_type = self._getTokenText()
    self.eat() # constructor, function, method

    self.eat() # void or type

    func_name = '%s.%s' % (self.class_name, self._getTokenText())
    self.eat(category='subroutine') 

    if self._is_method(func_type):
      # Important: Push this pointer as argument 0!
      # So the rest args are starting with index 1.
      self.symbol_tb.create('this', var_type=self.class_name, kind=SB.ARG)

    self.eat('(')
    # Handle params list.
    self.CompileParameterList()
    self.eat(')')

    # Handle body
    cached_body = self.parent
    body_node = ET.SubElement(self.parent, 'subroutineBody')
    self.parent = body_node

    self.eat('{')

    size = 0
    while (self._getTokenText() == 'var'):
      size += self.CompileVarDec()

    self.vm_writer.writeFunction(func_name, nLocals=size)

    if self._is_method(func_type):
      # Before compile statements, if it is method,
      # we need to insert VM code to set the base of the this segment.
      # We know argument 0 is always the object itself.
      # push argument 0
      # pop pointer 0 -> THIS = argument 0
      self.vm_writer.writePush('argument', 0)
      self.vm_writer.writePop('pointer', 0)
    elif self._is_contructor(func_type):
      # Allocate enough space for the object, save in THIS segment.
      # this = Memory.alloc(size)
      # pop top-most value from stack to pointer 0.

      # Find out object size by counting number of fields
      size = self.symbol_tb.VarCount(SB.FIELD)
      self.vm_writer.writePush('constant', size)
      self.vm_writer.writeCall('Memory.alloc', 1)
      self.vm_writer.writePop('pointer', 0)


    # Now, code gen for statements.
    self.CompileStatements()

    self.eat('}')

    # Reset parent to parent of sub rountine.
    self.parent = cached_parent

  def CompileParameterList(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'parameterList')
    self.parent = sub_node

    tt = self._getTokenText()
    # Return if we do not have any params.
    if tt == ')':
      sub_node.text = '\n'
      self.parent = cached_parent
      return

    ident_type = self._getTokenText()
    self.eat() # type
    self.eat(category=SB.ARG, var_type=ident_type) # varName

    tt = self._getTokenText()
    while (tt == ','):
      self.eat(',')
      ident_type = self._getTokenText()
      self.eat() # type
      self.eat(category=SB.ARG, var_type=ident_type) # var name
      tt = self._getTokenText()

    self.parent = cached_parent

  def _getTokenText(self):
    _, text = self.tokens[self.index]
    text = text.strip()
    return text

  def CompileVarDec(self):
    size = 0;

    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'varDec')
    self.parent = sub_node

    self.eat('var')

    ident_type = self._getTokenText()
    self.eat() # type

    self.eat(category=SB.VAR, var_type=ident_type) # var name
    size += 1

    tt = self._getTokenText()
    while (tt == ','):
      self.eat(',')
      self.eat(category=SB.VAR, var_type=ident_type) # var name
      size += 1
      tt = self._getTokenText()

    self.eat(';')

    self.parent = cached_parent

    return size

  def PeekStatements(self):
    _, text = self.tokens[self.index]
    text = text.strip()
    if text in ['let', 'if', 'while', 'do', 'return']:
      return True

    return False

  def _compile_statement(self):
      _, text = self.tokens[self.index]
      text = text.strip()
      if text == 'let':
        self.CompileLet()
      elif text == 'do':
        self.CompileDo()
      elif text == 'return':
        self.CompileReturn()
      elif text == 'if':
        self.CompileIf()
      elif text == 'while':
        self.CompileWhile()
      else:
        print(self.index, 'Unhandled statements!')

  def CompileStatements(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'statements')
    self.parent = sub_node

    while (self.PeekStatements()):
      self._compile_statement()
    
    self.parent = cached_parent

  def _prepare_vm_method(self, class_or_var):
    # Check if indentifier is a class name or intance name in symbol table.
    if self.symbol_tb.IndexOf(class_or_var) != -1:
      # The indentifier is an instance of class, we need to push as arg 0.
      segment = self.symbol_tb.KindOf(class_or_var)
      index = self.symbol_tb.IndexOf(class_or_var)
      self.vm_writer.writePush(segment, index)
      return True

    return False

  def _get_type_of_token_from_symbol_tb(self, token):
    if self.symbol_tb.IndexOf(token) != -1:
      return self.symbol_tb.TypeOf(token)
    return token

  def CompileDo(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'doStatement')
    self.parent = sub_node

    self.eat('do')

    # Look ahead to see if this is a() or class.a()
    _, text = self.tokens[self.index + 1]
    text = text.strip()
    sym = ''
    is_method = False
    if text == '.':
      class_or_var = self._getTokenText()
      self.symbol_tb.display()

      is_method = self._prepare_vm_method(class_or_var)
      
      # Example: game.run()
      # We want to generate VM code: SquareGame.run, instead of game.run
      # Hence, we need to get the actual type of the object.
      if is_method:
        sym += self.symbol_tb.TypeOf(class_or_var)
      else:
        sym += class_or_var

      self.eat() # Class name or var name
      self.eat('.')
      sym += '.'
    elif text == '(':
      # Case: method calling another method. Ex: a(), where a is a method.
      sym = self.class_name + '.'
      is_method = True
      self.vm_writer.writePush('pointer', 0)
      print('Handle method calling method', sym)

    sym += self._getTokenText()
    self.eat(category='subroutine') # subroutine Name 
    self.eat('(')
    # This will push more args for VM code gen.
    size = self.CompileExpressionList()
    self.eat(')')

    # Method has an extra arg 0 which is the object's instance.
    # Write vm Call.
    n_args = size + 1 if is_method else size
    self.vm_writer.writeCall(sym, n_args, ignore_ret=True)

    self.eat(';')

    self.parent = cached_parent

  def isLetHasArrayAsElement(self):
    _, text = self.tokens[self.index]
    return text.strip() == '['

  def CompileLet(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'letStatement')
    self.parent = sub_node

    self.eat('let')

    # TODO: needs to handle array
    segment, index = self._get_symbol_infos_from_cur_token()
    self.eat() # varName

    is_array = False
    if self.isLetHasArrayAsElement():
      is_array = True
      # Push array base pointer.
      self.vm_writer.writePush(segment, index)

      self.eat('[')
      self.CompileExpression()
      self.eat(']')

      # Compute (arr + i) address. Store at top-most of Stack.
      self.vm_writer.writeArithmetic('add')

    self.eat('=')

    self.CompileExpression()

    self.eat(';')

    if is_array:
      # Now set the array[exp1] = exp2 !
      # Store exp2 to temp 0.
      self.vm_writer.writePop('temp', 0)
      # Set THAT pointer
      self.vm_writer.writePop('pointer', 1)
      # Push exp2 to top of stack.
      self.vm_writer.writePush('temp', 0)
      # Pop exp2 from stack, save to *(arr + i).
      self.vm_writer.writePop('that', 0)
    else:
      self.vm_writer.writePop(segment, index)

    self.parent = cached_parent

  def CompileWhile(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'whileStatement')
    self.parent = sub_node

    self.eat('while')

    l1 = self._gen_label()
    l2 = self._gen_label()

    self.vm_writer.writeLabel(l1)

    self.eat('(')
    cached_index = self.index
    self.CompileExpression()
    # Compute ~(cond) for VM code gen.

    # if self.index - cached_index == 1:
    #   # If our expression(cond) is a single element, it is a boolean.
    #   # We need to compare the exp with True.
    #   # True is: push constant 1 + applying negative
    #   self.vm_writer.writePush('constant', 1)
    #   self.vm_writer.writeArithmetic('not')
    #   self.vm_writer.writeArithmetic('eq')

    self.vm_writer.writeArithmetic('not')
    self.eat(')')

    # If condition is false, we break out the loop.
    self.vm_writer.writeIf(l2)
    
    self.eat('{')
    self.CompileStatements()
    self.eat('}')

    # Continue the loop.
    self.vm_writer.writeGoto(l1)

    # We are done with the while loop. Condition is false.
    self.vm_writer.writeLabel(l2)

    self.parent = cached_parent

  def isReturnHasExp(self):
    _, text = self.tokens[self.index]
    return text.strip() != ';'

  def CompileReturn(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'returnStatement')
    self.parent = sub_node

    self.eat('return')

    if self.isReturnHasExp():
      self.CompileExpression()
    else:
      # Push constant 0 as convention
      self.vm_writer.writePush('constant', 0)

    self.eat(';')

    self.vm_writer.writeReturn()

    self.parent = cached_parent

  def isIfHasElse(self):
    _, text = self.tokens[self.index]
    return text.strip() == 'else'

  def _gen_label(self):
    i = self.label_index
    self.label_index += 1

    label = '%s_%d' % (self.class_name, i)
    return label

  def CompileIf(self):
    """
    if (cond)
      s1
    else
      s2

    CONVERT TO VM:
      computing ~(cond)
      if-goto L1
      s1
      goto L2
    label L1
      s2
    label L2
      ...
    """
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'ifStatement')
    self.parent = sub_node

    self.eat('if')

    self.eat('(')
    self.CompileExpression()
    # Compute ~(cond)
    self.vm_writer.writeArithmetic('not')
    self.eat(')')

    l1 = self._gen_label()
    l2 = self._gen_label()

    self.vm_writer.writeIf(l1)
    self.eat('{')
    self.CompileStatements()
    self.eat('}')

    self.vm_writer.writeGoto(l2)

    self.vm_writer.writeLabel(l1)

    if self.isIfHasElse():
      self.vm_writer
      self.eat('else')
      self.eat('{')
      self.CompileStatements()
      self.eat('}')

    self.vm_writer.writeLabel(l2)

    self.parent = cached_parent

  def isExpHasMoreTerms(self):
    _, text = self.tokens[self.index]
    return text.strip() in OP_LIST

  def CompileExpression(self, unary=None):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'expression')
    self.parent = sub_node

    self.CompileTerm()

    # Handle term (op term)*
    while (self.isExpHasMoreTerms()):
      # Cache operand.
      op = self._getTokenText()
      self.eat()
      self.CompileTerm()
      # Postfix, write a, b, then +/-/*
      self._write_math(op)

    self.parent = cached_parent

  def _write_math(self, t):
    if t == '*':
      self.vm_writer.writeCall('Math.multiply', 2)
      return
    
    if t == '/':
      self.vm_writer.writeCall('Math.divide', 2)
      return

    if t == '+':
      cmd = 'ADD'
    elif t == '-':
      cmd = 'SUB'
    elif t == '-':
      cmd = 'NEG'
    elif t == '=':
      cmd = 'EQ'
    elif t == '>':
      cmd = 'GT'
    elif t == '<':
      cmd = 'LT'
    elif t == '&':
      cmd = 'AND'
    elif t == '|':
      cmd = 'OR'
    elif t == '~':
      cmd = 'NOT'
    else:
      cmd = None
      print(t, 'not supported')
    
    if cmd:
      self.vm_writer.writeArithmetic(cmd.lower())

  def _write_push_from_cur_token(self, unary=None):
    """ Write push vm cmd from current token.
    True is mapped to constant -1.

    -1 ->
    push constant 1
    neg
    """
    tag, ori_t = self.tokens[self.index]
    t = ori_t.strip()
   
    _, prev = self.tokens[self.index - 1]
    _, p_prev = self.tokens[self.index - 2]
    if 'Constant' in tag:
      if tag != 'stringConstant':
        self.vm_writer.writePush('constant', t)
      else:
        # Handle string constant.
        # str = String.new(length)
        # loop length: do str.appendChar(nextChar)
        length = len(ori_t) - 2
        token = ori_t[1:-1]
        print('.......', token, ori_t)
        self.vm_writer.writePush('constant', length)
        self.vm_writer.writeCall('String.new', 1)

        for i in range(length):
          # NOTE: String appendChar()'s argument 0 is THIS.
          # Thus, number of args is 2.
          self.vm_writer.writePush('constant', ord(token[i]))
          self.vm_writer.writeCall('String.appendChar', 2)


    elif self.symbol_tb.IndexOf(t) != -1:
      segment = self.symbol_tb.KindOf(t)
      index = self.symbol_tb.IndexOf(t)
      self.vm_writer.writePush(segment, index)
    else:
      if t == 'true':
        self.vm_writer.writePush('constant', 1)
        self.vm_writer.writeArithmetic('neg')
      elif t == 'false' or t == 'null':
        self.vm_writer.writePush('constant', 0)
      elif t == 'this':
        self.vm_writer.writePush('pointer', 0)
    
    # Check if we got a negative value: , -3 by
    # check prev is -, and prev of prev is ',' or '('.
    # if prev.strip() == '-' and (p_prev.strip() == ',' or p_prev.strip() == '('):
    #   self.vm_writer.writeArithmetic('neg')

  def _get_symbol_infos_from_cur_token(self):
    t = self._getTokenText()
    segment = self.symbol_tb.KindOf(t)
    index = self.symbol_tb.IndexOf(t)
    return segment, index

  def CompileTerm(self, unary=None):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'term')
    self.parent = sub_node

    tt = self._getTokenText()
    if tt in UNARYOP_LIST:
      # Handle unaryOp term case. Example: while (~exit)
      self.eat(tt)
      self.CompileTerm(unary=tt)
      
      if tt == '~':
        self.vm_writer.writeArithmetic('not')
      if tt == '-':
        self.vm_writer.writeArithmetic('neg')

    elif tt == '(':
      # Handle (exp) case
      self.eat('(')
      self.CompileExpression()
      self.eat(')')

    else:
      self._write_push_from_cur_token(unary)

      # Eat one whatever...
      class_or_var = self._getTokenText()
      self.eat()

      # Peak next token to determine type.
      text = self._getTokenText()

      if text == '[':
        # Array case: a[b]
        self.eat('[')
        # eat the index as expression
        self.CompileExpression()
        self.eat(']')
        
        # Handle RHS array access. Example: arr[2]
        # push arr, push constant 2, add.
        # Now stack has the address of (arr + i)
        # Set THAT pointer: pop pointer 1
        # Push *(arr + i) to stack: push that 0
        self.vm_writer.writeArithmetic('add')
        self.vm_writer.writePop('pointer', 1)
        self.vm_writer.writePush('that', 0)

      elif text == '(':
        # subroutine call type: a(b)
        self.eat('(')
        self.CompileExpressionList()
        self.eat(')')
      elif text == '.':
        # subroutine call type: class.method(...)
        tk_type = self._get_type_of_token_from_symbol_tb(class_or_var)
        self.eat('.')

        func_name = self._getTokenText()
        self.eat() # eat the function name
        self.eat('(')

        is_method = self._prepare_vm_method(class_or_var)

        size = self.CompileExpressionList()
        self.eat(')')

        # Write vm Call.
        sym = '%s.%s' % (tk_type, func_name)
        n_args = size + 1 if is_method else size
        self.vm_writer.writeCall(sym, n_args)


    self.parent = cached_parent

  def CompileExpressionList(self):
    size = 0
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'expressionList')
    self.parent = sub_node

    tt = self._getTokenText()
    if tt == ')':
      # Empty case.
      sub_node.text = '\n'
      self.parent = cached_parent
      return size

    # Compile one expression.
    self.CompileExpression()
    size += 1

    # Process the rest of expressions if any.
    tt = self._getTokenText()
    while (tt == ','):
      self.eat(',')
      self.CompileExpression()
      size += 1
      tt = self._getTokenText()

    self.parent = cached_parent

    return size


def test_many_class_vars():
  xml_text = """
  <tokens>
    <keyword> class </keyword>
    <identifier> Main </identifier>
    <symbol> { </symbol>
    <keyword> static </keyword>
    <keyword> boolean </keyword>
    <identifier> test </identifier>
    <symbol> ; </symbol>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier> direction </identifier>
    <symbol> ; </symbol>
    <symbol> } </symbol>
  </tokens>
  """

  pp = Parser(xml_text, is_input_str=True)
  pp.CompileClass()

  tree = ET.ElementTree(pp.root)
  lib.indent(pp.root)

  count = len(pp.root)
  print(count)

  # fn = 'test.xml'
  # tree.write(fn)

  assert(count == 6)
  print('Test class vars passed!')

#test_many_class_vars()


# pp = Parser('mini_test/output/MainT.xml')
# pp.CompileClass()

# tree = ET.ElementTree(pp.root)
# lib.indent(pp.root)

# fn = 'test.xml'
# tree.write(fn, short_empty_elements=False)




