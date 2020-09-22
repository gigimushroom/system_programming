# A LL(1) Parser

import xml.etree.cElementTree as ET
import sys
import os
import lib
import SymbolTable as SB

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
    
    if tag == 'identifier':
      existed = 'used'
      my_kind = ''
      my_type = ''
      my_index = ''
      if self.symbol_tb.IndexOf(text) == -1 and category in SB.VALID_SCOPE:
        existed = 'defined'
        # Got an indentifier to save in Symbol table.
        self.symbol_tb.create(text, var_type=var_type, kind=category)
        if var_type == '':
          print('Error on creating symbol', text, category, self.index)

      my_kind = self.symbol_tb.KindOf(text)
      my_type = self.symbol_tb.TypeOf(text)
      my_index = self.symbol_tb.IndexOf(text)
      
      text = '%s present(%s) kind(%s) type(%s) index(%s)' % \
            (text, existed, my_kind, my_type, my_index)

    node = self._writeNode(tag, text, self.parent)
    self.index += 1
    return node

  def _writeNode(self, tag, text, parent):
    node = ET.SubElement(parent, tag)

    # TODO: plug in symbol table
    node.text = text
    return node

  def CompileClass(self):
    self.eat('class')

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

  def CompileSubroutineDec(self):
    self.symbol_tb.startSubroutine()

    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'subroutineDec')
    self.parent = sub_node

    self.eat() # constructor, function, method

    self.eat() # void or type
    self.eat(category='subroutine') 

    self.eat('(')
    # Handle params list.
    self.CompileParameterList()
    self.eat(')')

    # Handle body
    cached_body = self.parent
    body_node = ET.SubElement(self.parent, 'subroutineBody')
    self.parent = body_node

    self.eat('{')

    while (self.CompileVarDec()):
      pass

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
    _, text = self.tokens[self.index]
    if text.strip() != 'var':
      return False

    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'varDec')
    self.parent = sub_node

    self.eat('var')

    ident_type = self._getTokenText()
    self.eat() # type

    self.eat(category='var', var_type=ident_type) # var name

    tt = self._getTokenText()
    while (tt == ','):
      self.eat(',')
      self.eat(category='var', var_type=ident_type) # var name
      tt = self._getTokenText()

    self.eat(';')

    self.parent = cached_parent

    return True

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

  def CompileDo(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'doStatement')
    self.parent = sub_node

    self.eat('do')

    # Look ahead to see if this is a() or class.a()
    _, text = self.tokens[self.index + 1]
    text = text.strip()
    if text == '.':
      self.eat() # Class name or var name
      self.eat('.')

    self.eat(category='subroutine') # subroutine Name 
    self.eat('(')
    self.CompileExpressionList()
    self.eat(')')

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

    self.eat() # varName

    if self.isLetHasArrayAsElement():
      self.eat('[')
      self.CompileExpression()
      self.eat(']')

    self.eat('=')

    self.CompileExpression()

    self.eat(';')

    self.parent = cached_parent

  def CompileWhile(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'whileStatement')
    self.parent = sub_node

    self.eat('while')

    self.eat('(')
    self.CompileExpression()
    self.eat(')')

    self.eat('{')
    self.CompileStatements()
    self.eat('}')

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

    self.eat(';')

    self.parent = cached_parent

  def isIfHasElse(self):
    _, text = self.tokens[self.index]
    return text.strip() == 'else'

  def CompileIf(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'ifStatement')
    self.parent = sub_node

    self.eat('if')

    self.eat('(')
    self.CompileExpression()
    self.eat(')')

    self.eat('{')
    self.CompileStatements()
    self.eat('}')

    if self.isIfHasElse():
      self.eat('else')
      self.eat('{')
      self.CompileStatements()
      self.eat('}')

    self.parent = cached_parent

  def isExpHasMoreTerms(self):
    _, text = self.tokens[self.index]
    return text.strip() in OP_LIST

  def CompileExpression(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'expression')
    self.parent = sub_node

    self.CompileTerm()

    #Handle term (op term)*
    while (self.isExpHasMoreTerms()):
      self.eat()
      self.CompileTerm()

    self.parent = cached_parent

  def CompileTerm(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'term')
    self.parent = sub_node

    tt = self._getTokenText()
    if tt in UNARYOP_LIST:
      # Handle unaryOp term case. Example: while (~exit)
      self.eat(tt)
      self.CompileTerm()

    elif tt == '(':
      # Handle (exp) case
      self.eat('(')
      self.CompileExpression()
      self.eat(')')

    else:
      # Eat one whatever...
      self.eat()
      # Peak next token to determine type.
      text = self._getTokenText()

      if text == '[':
        # Array case: a[b]
        self.eat('[')
        # eat the index as expression
        self.CompileExpression()
        self.eat(']')
      elif text == '(':
        # subroutine call type: a(b)
        self.eat('(')
        self.CompileExpressionList()
        self.eat(')')
      elif text == '.':
        # subroutine call type: class.method(...)
        self.eat('.')
        self.eat() # eat the function name
        self.eat('(')
        self.CompileExpressionList()
        self.eat(')')

    self.parent = cached_parent

  def CompileExpressionList(self):
    cached_parent = self.parent
    sub_node = ET.SubElement(self.parent, 'expressionList')
    self.parent = sub_node

    tt = self._getTokenText()
    if tt == ')':
      # Empty case.
      sub_node.text = '\n'
      self.parent = cached_parent
      return

    # Compile one expression.
    self.CompileExpression()

    # Process the rest of expressions if any.
    tt = self._getTokenText()
    while (tt == ','):
      self.eat(',')
      self.CompileExpression()
      tt = self._getTokenText()

    self.parent = cached_parent


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




