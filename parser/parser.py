# ---------------
# User Instructions
#
# In this problem, you will be using many of the tools and techniques
# that you developed in unit 3 to write a grammar that will allow
# us to write a parser for the JSON language.
#
# You will have to visit json.org to see the JSON grammar. It is not
# presented in the correct format for our grammar function, so you
# will need to translate it.

# ---------------
# Provided functions
#
# These are all functions that were built in unit 3. They will help
# you as you write the grammar.  Add your code at line 102.

from functools import update_wrapper
from string import split
import re
import pprint as pp

# def convert(tree):
# 	"Convert the tree to the regex API format used in class."
# 	if isinstance(tree, tuple): tree = tree[0] # Remove () and ending ''.
# 	seq = tree[1:] # Remove opening 'RE'.
# 	if len(seq) == 1: return parse_unit(seq[0])	# Single-unit sequences
# 	return "seq(%s, %s)" % (parse_unit(seq[0]), parse_unit(seq[1]))
#
# def parse_unit(unit):
# 	"Parse an individual unit of a regex pattern."
# 	type = unit[0]
# 	if type == 'RE': return convert(unit)
# 	if type == 'expr': return parse_unit(unit[1])
# 	if type == 'group': return convert(unit[2])
# 	if type == 'star': return "star(%s)" % parse_unit(unit[1][1])
# 	if type == 'plus': return "plus(%s)" % parse_unit(unit[1][1])
# 	if type == 'opt': return "opt(%s)" % parse_unit(unit[1][1])
# 	if type == 'alt': return "alt(%s, %s)" % (parse_unit(unit[2][1]), parse_unit(unit[4][1]))
# 	if type == 'oneof': return "oneof('%s')" % unit[2][1]
# 	if type == 'lits' or type == 'lit': return "lit('%s')" % unit[1]
# 	if type == 'dot': return "oneof('?')"
# 	if type == 'eol': return "eol('$')"
# 	return "Unable to parse unit."

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
  #pp.pprint(G)
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
        if atom == 'RE':
          print alternative, text
        tree, rem = parse_sequence(alternative, text)
        if rem is not None:
          print 'debug:', alternative, atom, tree
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
  top = tree[1] if tree[0] == 'RE' else None
  results = []
  post_order_convert(top, results)

  print 'Result set:', results
  print 'APIs', ''.join([e for e in results])



def post_order_convert(tree, results):
  if tree and isinstance(tree, list):
    results.append('(')
    post_order_convert(tree[0], results)
    results.append(')')
    results.append('(')
    post_order_convert(tree[1], results)
    results.append(')')
  elif isinstance(tree, str):
    results.append(tree)
    print tree


def test_convert():
  tree1 = ['RE', ['expr', ['lit', 'hello']]]
  tree2 = ['RE',
            ['expr', ['star', ['unit', ['lit', 'a']], '*']],
            ['RE',
             ['expr', ['star', ['unit', ['lit', 'b']], '*']],
             ['RE', ['expr', ['star', ['unit', ['lit', 'c']], '*']]]
            ]
          ]
  print convert(tree2)


def test():
  #assert parse_re('hello') == "lit('hello')"

  # parse_re('a*b*c*')

  assert parse_re('a*b*c*') == "seq(star(lit('a')), seq(star(lit('b')), star(lit('c'))))"

  # assert parse_re('[ab]*') == "star(oneof('ab'))"
  # assert parse_re('a+(b+c+)') == "seq(plus(lit('a')), seq(plus(lit('b')), plus(lit('c'))))"
  # assert parse_re('[bcfhrsm]at') == "seq(oneof('bcfhrsm'), lit('at'))"
  # assert parse_re('(a|b)*c?') == "seq(star(alt(lit('a'), lit('b'))), opt(lit('c')))"
  # assert parse_re('(a*)?') == "opt(star(lit('a')))"
  # assert parse_re('abc.$') == "seq(lit('abc'), seq(oneof('?'), eol('$')))"
  return "tests pass"


#print test()

print test_convert()
