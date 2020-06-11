"""
UNIT 3: Functions and APIs: Polynomials

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

    p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

    p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:

    p1.coefs == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

    >>> p1
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

    >>> p1.__name__
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**'
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

    is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""

from string import split
import re

def format_coefs(coefs):
  f_name = []
  for i, c in enumerate(coefs):
    if c == 0:
      continue

    if i == 0:
      expr = str(c)
    elif i == 1:
      expr = "%d * x" % c if c != 1 else 'x'
    else:
      expr = "%d * x**%d" % (c, i) if c != 1 else "x**%d" % i

    f_name.append(expr)

  f_name.reverse()
  return ' + '.join(f_name)

def poly(coefs):
  """Return a function that represents the polynomial with these coefficients.
  For example, if coefs=(10, 20, 30), return the function of x that computes
  '30 * x**2 + 20 * x + 10'.  Also store the coefs on the .coefs attribute of
  the function, and the str of the formula on the .__name__ attribute.'"""
  # your code here (I won't repeat "your code here"; there's one for each function)
  def formula(x):
    items = []
    for i, c in enumerate(coefs):
      items.append(c * x ** i)
    return sum(items)

  formula.__name__ = format_coefs(coefs)
  formula.coefs = tuple(coefs)
  return formula

def test_poly():
  global p1, p2, p3, p4, p5, p9  # global to ease debugging in an interactive session

  p1 = poly((10, 20, 30))
  assert p1(0) == 10
  for x in (1, 2, 3, 4, 5, 1234.5):
    assert p1(x) == 30 * x ** 2 + 20 * x + 10
  assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

  assert is_poly(p1)
  assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

  p3 = poly((0, 0, 0, 1))
  assert p3.__name__ == 'x**3'
  p9 = mul(p3, mul(p3, p3))   # mul(x^3, x^6) => x^9
  assert p9(2) == 512
  p4 = add(p1, p3)
  assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

  assert same_name(poly((1, 1)).__name__, 'x + 1')

  assert same_name(power(poly((1, 1)), 10).__name__,
                   'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
                   ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

  assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11, 22, 33)
  assert sub(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (9, 18, 27)
  assert mul(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (10, 40, 100, 120, 90)
  assert power(poly((1, 1)), 2).coefs == (1, 2, 1)
  assert power(poly((1, 1)), 10).coefs == (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)

  assert deriv(p1).coefs == (20, 60)
  assert integral(poly((20, 60))).coefs == (0, 20, 30)
  p5 = poly((0, 1, 2, 3, 4, 5))
  assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
  assert p5(1) == 15
  assert p5(2) == 258
  assert same_name(deriv(p5).__name__, '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
  assert deriv(p5)(1) == 55
  assert deriv(p5)(2) == 573

  print 'Basic ploy tests PASSED!'


def same_name(name1, name2):
  """I define this function rather than doing name1 == name2 to allow for some
  variation in naming conventions."""

  def canonical_name(name): return name.replace(' ', '').replace('+-', '-')

  return canonical_name(name1) == canonical_name(name2)


def is_poly(x):
  """Return true if x is a poly (polynomial)."""
  ## For examples, see the test_poly function
  if not callable(x) or not hasattr(x, 'coefs'):
    return False

  return True

def add(p1, p2):
  """Return a new polynomial which is the sum of polynomials p1 and p2."""
  c1 = p1.coefs
  c2 = p2.coefs
  c3 = tuple(map(sum, zip(c1, c2)))

  if len(c1) < len(c2):
    c3 += tuple(c2[len(c1):])

  def inner(x):
    return p1(x) + p2(x)

  inner.coefs = c3
  inner.__name__ = format_coefs(c3)
  return inner

def sub(p1, p2):
  """Return a new polynomial which is the difference of polynomials p1 and p2."""
  c1 = p1.coefs
  c2 = p2.coefs
  c3 = tuple([x - y for x, y in zip(c1, c2)])

  if len(c1) < len(c2):
    c3 += tuple(c2[len(c1):])

  def sub_inner(x):
    return p1(x) - p2(x)

  sub_inner.coefs = c3
  sub_inner.__name__ = format_coefs(c3)
  return sub_inner

def mul_coef(c1, c2):
  l1 = len(c1)
  l2 = len(c2)
  # Total length of poly mul is (len(p1) + len(p2) - 1).
  coefs = [0] * (l1 + l2 - 1)
  for i in range(l1):
    pi = c1[i]
    for j in range(l2):
      coefs[i + j] += pi * c2[j]
  return coefs

def mul(p1, p2):
  """Return a new polynomial which is the product of polynomials p1 and p2."""
  def inner(x):
    return p1(x) * p2(x)

  coefs = mul_coef(p1.coefs, p2.coefs)
  inner.coefs = tuple(coefs)
  inner.__name__ = format_coefs(coefs)
  return inner


def power(p, n):
  """Return a new polynomial which is p to the nth power (n a non-negative integer)."""
  def inner(x):
    res = 1
    for i in range(n):
      res *= mul(p, p)(x)
    return res

  c = p.coefs
  for i in range(n-1):
    c = mul_coef(p.coefs, c)

  inner.coefs = tuple(c)
  inner.__name__ = format_coefs(c)
  return inner

"""
If your calculus is rusty (or non-existant), here is a refresher:
The derivative of a polynomial term (c * x**n) is (c*n * x**(n-1)).
The derivative of a sum is the sum of the derivatives.
So the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20).

The integral is the anti-derivative:
The integral of 60 * x + 20 is  30 * x**2 + 20 * x + C, for any constant C.
Any value of C is an equally good anti-derivative.  We allow C as an argument
to the function integral (withh default C=0).
"""


def deriv(p):
  """Return the derivative of a function p (with respect to its argument)."""
  def formula(x):
    items = []
    for i, c in enumerate(p.coefs):
      # constant is skipped.
      if i != 0:
        items.append(c * i * x ** (i - 1))
    return sum(items)

  # Find deriv's coefs.
  coefs = ()
  for i, c in enumerate(p.coefs):
    # constant is skipped.
    if i != 0:
      coefs += (c * i,)

  formula.__name__ = format_coefs(coefs)
  formula.coefs = tuple(coefs)
  return formula

def integral(p, C=0):
  """Return the integral of a function p (with respect to its argument)."""
  # I decided to hack a bit, use divider to find integral number.
  integral_num = 2 if p.coefs[-1] % 2 == 0 else 3

  def formula(x):
    items = [C]
    for i, c in enumerate(p.coefs):
      if i == 0:
        items.append(c * x)
      else:
        items.append(c / integral_num * x ** (i + 1))
    return sum(items)

  # Find coefs.
  coefs = [C]
  for i, c in enumerate(p.coefs):
    if i == 0:
      coefs.append(c)
    else:
      coefs.append(c / integral_num)

  formula.__name__ = format_coefs(coefs)
  formula.coefs = tuple(coefs)
  return formula


test_poly()


"""
Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:

(1) By defining poly as a class rather than a function, and overloading the 
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
call the function test_poly1().  Make sure that poly objects can still be called.

(2) Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, Poly, which takes one argument, a string,
as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
"""


def test_poly1():
  # I define x as the polynomial 1*x + 0.
  x = poly((0, 1))
  # From here on I can create polynomials by + and * operations on x.
  newp1 = 30 * x ** 2 + 20 * x + 10  # This is a poly object, not a number!
  assert p1(100) == newp1(100)  # The new poly objects are still callable.
  assert same_name(p1.__name__, newp1.__name__)
  assert (x + 1) * (x - 1) == x ** 2 - 1 == poly((-1, 0, 1))




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
    description = description.replace('\t', ' ') # no tabs!
    for line in split(description, '\n'):
        if not line: continue
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    #print G
    return G

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
    #print 'seq result', result, text
    return result, text

  def parse_atom(atom, text):
    if atom in grammar:  # Non-Terminal: tuple of alternatives
      for alternative in grammar[atom]:
        tree, rem = parse_sequence(alternative, text)
        if rem is not None:
          #print 'debug:', atom, tree, 'reminder', rem
          return [atom] + tree, rem
      return Fail
    else:  # Terminal: match characters against start of text
      m = re.match(tokenizer % atom, text)
      return Fail if (not m) else (m.group(1), text[m.end():])

  # Body of parse:
  return parse_atom(start_symbol, text)


Fail = (None, None)

POLY_GRAMMAR = grammar("""
seq => expr plus | expr
expr => const times | const
times => \* power
const => -?[1-9][0-9]*
power => x\*\*[0-9] | x
plus => \+ seq
""", whitespace='\s*')


# CONVERTER
# I decided to cheat a bit. I could have defined a set of APIS, and calculate the polynomial result,
# but I want to re-use the functions I wrote above: poly(coefs)
# So the job of converter is to parse the coefs out of the AST.

def convert(tree):
  #pp.pprint(tree)
  # Preprocessing only once to remove () and ending ''.
  if isinstance(tree, tuple):
    tree = tree[0]

  results = []
  process_expr(tree, results)

  results.reverse()

  return [int(r) for r in results]


def process_expr(tree, results):
  if not tree: return
  root = tree[0]
  if root == 'seq':
    process_expr(tree[1], results)
    if len(tree) > 2:
      process_expr(tree[2], results)
  elif root == 'expr':
    process_expr(tree[1], results)
  elif root == 'const':
    results.append(tree[1])
  elif root == 'times':
    return
  elif root == 'plus':
    process_expr(tree[2], results)
  else:
    print "un-handled key:", root

  return None


# The master call.
def Poly(text):
  AST = Poly_helper(text)
  coefs = convert(AST)
  return poly(coefs)

def Poly_helper(text):
  return parse('seq', text, POLY_GRAMMAR)


def test_poly_parser():
  assert Poly_helper('20 * x + 10') == (['seq', ['expr', ['const', '20'], ['times', '*', ['power', 'x']]], ['plus', '+', ['seq', ['expr', ['const', '10']]]]], '')

  assert Poly_helper('30 * x**2 + 20 * x + 10') == (['seq', ['expr', ['const', '30'], ['times', '*', ['power', 'x**2']]],
                                              ['plus', '+', ['seq', ['expr', ['const', '20'], ['times', '*', ['power', 'x']]],
                                                             ['plus', '+', ['seq', ['expr', ['const', '10']]]]]]], '')
  print 'Parser Test Passed'

def test_converter():
  assert convert(Poly_helper('20 * x + 10')) == [10, 20]
  assert convert(Poly_helper('30 * x**2 + 20 * x + 10')) == [10, 20, 30]

  print "Converter passed"

def test_poly2():
  test_poly_parser()
  test_converter()

  p1 = poly((10, 20, 30))
  newp1 = Poly('30 * x**2 + 20 * x + 10')
  assert p1(100) == newp1(100)
  assert same_name(p1.__name__, newp1.__name__)

  assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11, 22, 33)
  assert add(Poly('30 * x**2 + 20 * x + 10'), Poly('3 * x**2 + 2 * x + 1')).coefs == (11, 22, 33)

  print "poly2 challenge passed!"

test_poly2()



"""
https://stackoverflow.com/questions/5413158/multiplying-polynomials-in-python

Multiplying polynomials in python
s1 = [1,5,2]
s2 = [6,1,4,3]
res = [0]*(len(s1)+len(s2)-1)  # TOTAL LENGTH
for o1,i1 in enumerate(s1):
    for o2,i2 in enumerate(s2):
        res[o1+o2] += i1*i2

"""
