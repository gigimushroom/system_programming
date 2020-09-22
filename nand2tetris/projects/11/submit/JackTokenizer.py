# Tokenizer


TYPE_KEYWORD = 'kw'
TYPE_SYMBOL = 'sym'
TYPE_IDENTIFIER = 'id'
TYPE_INT_CONST = 'int'
TYPE_STRING_CONT = 'str'

KEYWORDS = ['class', 'constructor', 'function',
'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
'void', 'true', 'false', 'null', 'this', 'let', 'do',
'if', 'else', 'while', 'return'
]

SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';',
  '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'
]
WHITESPACES = ['\n', ' ', '\t']


def tokenize_line(line):
  """ Parse a line into tokens

  If the char is not a symbol or whitespace, we append the char to our 
  current token, and continue.
  If the current char is a symbol, we save our token to token list, and 
  save the symbol as another token. Last, we clear the token buffer.
  If we got a whitespace, we save out token. Last, clear token buffer.

  If our element is a string which begin with quote, we want to
  include everything we see until meet the ending quote.

  """
  tokens = []
  element = ''
  for ch in line:
    if ch not in SYMBOLS and ch not in WHITESPACES:
      if ch == '"' and element != '':
        # Our current token got an end quote. Save it.
        element += ch
        tokens.append(element)
        element = ''
      else:
        # soak it in current token.
        element += ch

    elif ch in SYMBOLS:
      # If current token is string, the char is also part of our string.
      if element != '' and element[0] == '"':
        element += ch
      else:
        # Otherwise, save current token, symbol, and clear token buffer.
        if element != '':
          tokens.append(element)
        tokens.append(ch)
        element = ''

    elif ch in WHITESPACES and element != '':
      # If we got whitespace char and we have a valid token, save the token
      # if it is not a string.
      if element[0] != '"':
        tokens.append(element)
        element = ''
      else:
        # If our current token is a string, <"abc >
        # We want to take the space into our token, since 
        # the final result can be <"abc def">.
        element += ch

  return tokens

class Tokenizer:
  def __init__(self, file_name):
    self.index = -1
    self.tokens = []

    with open(file_name) as f:
      for line in f:
        # partition returns a tuple: 
        # everything before the partition string, the partition string,
        # and everything after the partition string. 
        # So, by indexing with [0] we take just the part before 
        # the partition string.
        line = line.partition('//')[0]
        line = line.strip()
        line = line.partition('/**')[0]
        line = line.strip()
        # This is hacky, we want to removal line starting with * since
        # that is part of comments.
        if not line.startswith('*'):
          tokens = tokenize_line(line)
          self.tokens.extend(tokens)
          #print(tokens)

  def hasMoreTokens(self):
    if not self.tokens:
      return False

    return self.index < len(self.tokens) - 1
  
  def advance(self):
    self.index += 1
    self.tk = self.tokens[self.index]

  def is_integer(self, s):
    #print(self.index, self.tk, self.tokens)
    if s[0] in ('-', '+'):
      return s[1:].isdigit()
    return s.isdigit()

  def is_string(self, s):
    return s.startswith('"') and s.endswith('"')

  def tokenType(self):
    tk = self.tk
    if tk in KEYWORDS:
      return TYPE_KEYWORD
    elif tk in SYMBOLS:
      return TYPE_SYMBOL
    elif self.is_integer(tk):
      return TYPE_INT_CONST
    elif self.is_string(tk):
      return TYPE_STRING_CONT
    else:
      return TYPE_IDENTIFIER
    
  def keyword(self):
    return self.tk

  def symbol(self):
    # Python XML writer already handles the encoding.
    # I do not need to do anything extra.

    # if self.tk == '<':
    #   return '&lt;'
    # elif self.tk == '>':
    #   return '&gt;'

    return self.tk

  def identifier(self):
    return self.tk

  def intVal(self):
    return int(self.tk)

  def stringVal(self):
    # Skip the double quotes.
    return self.tk[1:-1]



def test_tokenize_line():
  line = ' let ab =   bcd[3]   ;'
  tokens = tokenize_line(line)
  l1 = ['let', 'ab', '=', 'bcd', '[', '3', ']', ';']
  assert(tokens == l1)

  line = '    function void test() {\n'
  tokens = tokenize_line(line)
  l2 = ['function', 'void', 'test', '(', ')', '{']
  assert(tokens == l2)

  print('token tests passed')

def test_comments():

  pass

def test_long_sentence_in_quote():
  line = 'let s = "string __;;;;(constant";'
  tokens = tokenize_line(line)
  #print(tokens)
  l1 = ['let', 's', '=', '"string __;;;;(constant"', ';']
  assert(tokens == l1)
  print('long sentence tests passed')

def test_complex_let():
  line = 'let i = i * (-j);'
  tokens = tokenize_line(line)
  #print(tokens)
  l1 = ['let', 'i', '=', 'i', '*', '(', '-', 'j', ')', ';']
  assert(tokens == l1)
  print('Complex let test passed')

def test_all():
  test_tokenize_line()
  test_long_sentence_in_quote()

#test_complex_let()


