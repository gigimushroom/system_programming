# ---------------
# A Regex Engine
# ---------------

from functools import update_wrapper
from string import split
import re
import pprint as pp
import sys


def grammar(description, whitespace=r'\s*'):
  """Convert a description to a grammar.  Each line is a rule for a
  non-terminal symbol; it looks like this:
      Symbol =>  A1 A2 ... | B1 B2 ... | C1 C2 ...
  where the right-hand side is one or more alternatives, separated by
  the '|' sign.  Each alternative is a sequence of atoms, separated by
  spaces.  An atom is either a symbol on some left-hand side, or it is
  a regular expression that will be passed to re.match to match a token.
  Notation for *, +, or ? not allowed in a rule alternative (but ok
  within a token). Use '\' to continue long lines.  You must include spaces
  or tabs around '=>' and '|'. That's within the grammar description itself.
  The grammar that gets defined allows whitespace between tokens by default;
  specify '' as the second argument to grammar() to disallow this (or supply
  any regular expression to describe allowable whitespace between tokens)."""
  G = {' ': whitespace}
  description = description.replace('\t', ' ')  # no tabs!
  for line in split(description, '\n'):
    if not line: continue
    lhs, rhs = split(line, ' => ', 1)
    alternatives = split(rhs, ' | ')
    G[lhs] = tuple(map(split, alternatives))
  # pp.pprint(G)
  return G


def decorator(d):
  "Make function d a decorator: d wraps a function fn."

  def _d(fn):
    return update_wrapper(d(fn), fn)

  update_wrapper(_d, d)
  return _d


@decorator
def memo(f):
  """Decorator that caches the return value for each call to f(args).
  Then when called again with same args, we can just look it up."""
  cache = {}

  def _f(*args):
    try:
      return cache[args]
    except KeyError:
      cache[args] = result = f(*args)
      return result
    except TypeError:
      # some element of args can't be a dict key
      return f(args)

  return _f


def parse(start_symbol, text, grammar):
  """Example call: parse('Exp', '3*x + b', G).
  Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
  string. Failure iff remainder is None. This is a deterministic PEG parser,
  so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
  longest parse first; don't do 'E => T | T op E'
  Also, no left recursion allowed: don't do 'E => E op T'"""

  tokenizer = grammar[' '] + '(%s)'

  def parse_sequence(sequence, text):
    result = []
    for atom in sequence:
      tree, text = parse_atom(atom, text)
      if text is None: return Fail
      result.append(tree)
    return result, text

  # @memo
  def parse_atom(atom, text):
    if atom in grammar:  # Non-Terminal: tuple of alternatives
      for alternative in grammar[atom]:
        # if atom == 'RE':
        #  print alternative, text
        tree, rem = parse_sequence(alternative, text)
        if rem is not None:
          # print 'debug:', alternative, atom, tree
          return [atom] + tree, rem

      return Fail
    else:  # Terminal: match characters against start of text
      m = re.match(tokenizer % atom, text)
      # if m:
      #  print 'searching:', tokenizer % atom, text, 'Result:', m.group(1)
      return Fail if (not m) else (m.group(1), text[m.end():])

  # Body of parse:
  return parse_atom(start_symbol, text)


Fail = (None, None)

REGRAMMAR = grammar("""
RE => expr RE | expr
lit => \w+
oneof => [[] lit []]
star => unit [*]
plus => unit [+]
opt => unit [?]
group => [(] RE [)]
alt => [(] unit [|] unit [)]
eol => [$]
dot => [.]
expr => star | plus | opt | alt | oneof | group | lit | dot | eol
unit => alt | oneof | group | lit | dot | eol
""", whitespace='\s*')


def parse_re(pattern):
  # Parse a standard regex pattern by converting it to the regex API format used in class.
  return convert(parse('RE', pattern, REGRAMMAR))


def convert(tree):
  # Convert the tree to the regex API format used in class."
  pp.pprint(tree)
  # Preprocessing only once to remove () and ending ''.
  if isinstance(tree, tuple):
    tree = tree[0]

  results = []
  process_expr(tree, results)
  if not results: return None
  if len(results) == 1:
    return results[0]
  elif len(results) == 2:
    return "seq(%s, %s)" % (results[0], results[1])

  return None


def process_expr(tree, results):
  if not tree: return
  root = tree[0]
  if root == 'expr':
    results.append(convert(tree[1]))
  elif root == 'unit':
    results.append(convert(tree[1]))
  elif root == 'oneof':
    results.append("oneof('%s')" % tree[2][1])
  elif root == 'star':
    results.append("star(%s)" % convert(tree[1]))
  elif root == 'opt':
    results.append("opt(%s)" % convert(tree[1]))
  elif root == 'alt':
    results.append("alt(%s, %s)" % (convert(tree[2][1]), convert(tree[4][1])))
  elif root == 'plus':
    results.append("plus(%s)" % convert(tree[1]))
  elif root == 'eol':
    results.append("eol('$')")
  elif root == 'dot':
    results.append("oneof('?')")
  elif root == 'group':
    results.append(convert(tree[2]))
  elif root == 'RE':
    results.append(convert(tree[1]))
    if len(tree) > 2:
      results.append(convert(tree[2]))
  elif root == 'lit':
    results.append("lit('%s')" % tree[1])
  else:
    print "un-handled key:", root

  return None


def test_convert():
  tree1 = ['RE', ['expr', ['lit', 'hello']]]
  tree2 = ['RE',
           ['expr', ['star', ['unit', ['lit', 'a']], '*']],
           ['RE',
            ['expr', ['star', ['unit', ['lit', 'b']], '*']],
            ['RE', ['expr', ['star', ['unit', ['lit', 'c']], '*']]]
            ]
           ]
  tree3 = ['RE', ['expr', ['star', ['unit', ['oneof', '[', ['lit', 'ab'], ']']], '*']]]

  tree4 = ['RE',
           ['expr', ['oneof', '[', ['lit', 'bcfhrsm'], ']']],
           ['RE', ['expr', ['lit', 'at']]]
           ]

  tree5 = ['RE',
           ['expr',
            ['star',
             ['unit',
              ['alt',
               '(',
               ['unit', ['lit', 'a']],
               '|',
               ['unit', ['lit', 'b']],
               ')']],
             '*']],
           ['RE', ['expr', ['opt', ['unit', ['lit', 'c']], '?']]]
           ]
  res = convert(tree5)
  print 'Converted to', res


def test_parser():
  assert parse_re('hello') == "lit('hello')"
  assert parse_re('a*b*c*') == "seq(star(lit('a')), seq(star(lit('b')), star(lit('c'))))"
  assert parse_re('[ab]*') == "star(oneof('ab'))"
  assert parse_re('a+(b+c+)') == "seq(plus(lit('a')), seq(plus(lit('b')), plus(lit('c'))))"
  assert parse_re('[bcfhrsm]at') == "seq(oneof('bcfhrsm'), lit('at'))"

  assert parse_re('(a|b)*c?') == "seq(star(alt(lit('a'), lit('b'))), opt(lit('c')))"

  assert parse_re('(a*)?') == "opt(star(lit('a')))"
  assert parse_re('abc.$') == "seq(lit('abc'), seq(oneof('?'), eol('$')))"
  return "Parser tests pass"


print test_parser()


# test_convert()

def match1(pattern, text):
  """Match pattern against start of text; return longest match found or None.
  :param pattern: Patterns in APIs format. Ex: star(lit('a'))
  :param text: The sequence to search from.
  :return: longest match found or None
  """
  remainders = pattern(text)
  if remainders:
    shortest = min(remainders, key=len)
    return text[:len(text) - len(shortest)]

def match(pattern, text):
  """Match pattern against start of text; return longest match found or None.
    :param pattern: Patterns in String format. Ex: 'a*'
    :param text: The sequence to search from.
    :return: longest match found or None
    """

  # Parse the string pattern to AST, then to APIs format but in string format.
  pattern = parse_re(pattern)
  # Use eval() to convert APIs in string format to lambda functions.
  pattern = eval(pattern)
  # Call our general match1() to pattern matching.
  return match1(pattern, text)

def lit(s): return lambda t: set([t[len(s):]]) if t.startswith(s) else null
def seq(x, y): return lambda t: set().union(*map(y, x(t)))
def alt(x, y): return lambda t: x(t) | y(t)
def oneof(chars): return lambda t: set([t[1:]]) if (t and t[0] in chars) else null
dot = lambda t: set([t[1:]]) if t else null
eol = lambda t: set(['']) if t == '' else null
def star(x): return lambda t: (set([t]) |
                               set(t2 for t1 in x(t) if t1 != t
                                   for t2 in star(x)(t1)))

class APIs:
  def lit(self, s): return lambda t: set([t[len(s):]]) if t.startswith(s) else null

  def seq(x, y): return lambda t: set().union(*map(y, x(t)))

  def alt(x, y): return lambda t: x(t) | y(t)

  def oneof(chars): return lambda t: set([t[1:]]) if (t and t[0] in chars) else null

  dot = lambda t: set([t[1:]]) if t else null
  eol = lambda t: set(['']) if t == '' else null

  def star(x): return lambda t: (set([t]) |
                                 set(t2 for t1 in x(t) if t1 != t
                                     for t2 in star(x)(t1)))

null = frozenset([])

def test_match():
  assert match1(star(lit('a')), 'aaaaabbbaa') == 'aaaaa'
  assert match1(lit('hello'), 'hello how are you?') == 'hello'
  assert match1(lit('x'), 'hello how are you?') is None
  assert match1(oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
  assert match1(oneof('xyz'), '   x is here!') is None
  return 'Matcher tests pass'


print test_match()

def test_engine():
  assert match('a*', 'aaaaabbbaa') == 'aaaaa'
  assert match('hello', 'hello how are you?') == 'hello'
  assert match('[xyz]', 'x**2 + y**2 = r**2') == 'x'
  assert match('[xyz]', '   x is here!') is None

  return 'Engine tests pass'

print test_engine()