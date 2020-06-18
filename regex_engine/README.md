# Pattern Matching Engine Overview
- Define context free grammar.
- Implement a LR parser
- Implement a pattern matching function, with a few lambda helpers.

# How the pattern matcher works
## Input
Given pattern in string: `'a*'`, and a text to search from. \
Example: `match('a*', 'aaaaabbbaa')`

## Parsing to AST
Result: `['star'] seq [['star', ['unit', ['lit', 'b']], '*']]`

### LR Parser supports 4 kinds of input
- expr
- seq: expr expr ...
- alternatives: seq | seq | ...
- regex

```
parse_atom(atom):
  if atom in Grammar:
    alternatives = G[atom]
    for each alternative:
      result = parse_seq(alternative)
      return result if not None
    if none of them matches, Fail
  else:
    do the regex matching

parse_seq(seq):
  results = []
  for each atom in seq:
    r = parse_atom(atom)
    # We requires all atoms in seq match!
    if r is None, Fail
    add r to results
  return results

```

## Converter
Convert the AST to API string format. \
Example result: `'star(lit(‘a’))'`

## Start pattern matching
- `eval` converts the API string format to actual functions.
- Use the provided compiled lambdas, like `alt`, `star`, `lit`, etc.
- Return a set of reminders from the matches.

## Pick result
Among the reminders, find the smallest reminder, return the longest match word.


## Case Study
### Choose start symbol and patterns
```
RE => seq RE | seq
```

### What if I only do `RE => seq RE`
Result:
```
['seq', 'RE’] a*b*c*
debug: ['\\w+'] lit ['a']
debug: ['lit'] unit [['lit', 'a']]
debug: ['unit', '[*]'] star [['unit', ['lit', 'a']], '*']
debug: ['star'] seq [['star', ['unit', ['lit', 'a']], '*']]
['seq', 'RE'] b*c*
debug: ['\\w+'] lit ['b']
debug: ['lit'] unit [['lit', 'b']]
debug: ['unit', '[*]'] star [['unit', ['lit', 'b']], '*']
debug: ['star'] seq [['star', ['unit', ['lit', 'b']], '*']]
['seq', 'RE'] c*
debug: ['\\w+'] lit ['c']
debug: ['lit'] unit [['lit', 'c']]
debug: ['unit', '[*]'] star [['unit', ['lit', 'c']], '*']
debug: ['star'] seq [['star', ['unit', ['lit', 'c']], '*']]
['seq', 'RE'] <EMPTY_STR>
(None, None)
```
Reminder text is '', which is empty string. But we still want to search for `seq`,
so we got None as result.

### The solution
At the last step, we want to switch to another alternative.
That is, at reminder text is `c*`, we do not want to search in `[‘seq’, ‘RE’]`.
Instead, we want to search in `[seq]` only.
Result is good then:
```
[‘seq’] c*
debug: ['\\w+'] lit ['c']
debug: ['lit'] unit [['lit', 'c']]
debug: ['unit', '[*]'] star [['unit', ['lit', 'c']], '*']
debug: ['star'] seq [['star', ['unit', ['lit', 'c']], '*']]
debug: ['seq'] RE [['seq', ['star', ['unit', ['lit', 'c']], '*']]]
debug: ['seq', 'RE'] RE [['seq', ['star', ['unit', ['lit', 'b']], '*']], ['RE', ['seq', ['star', ['unit', ['lit', 'c']], '*']]]]
debug: ['seq', 'RE'] RE [['seq', ['star', ['unit', ['lit', 'a']], '*']], ['RE', ['seq', ['star', ['unit', ['lit', 'b']], '*']], ['RE', ['seq', ['star', ['unit', ['lit', 'c']], '*']]]]]
```
Thus, we want to have pattern: `RE => seq RE | seq`.
