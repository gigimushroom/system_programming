# Study Section 1
```
RE => seq RE | seq
```

## What if I only do `RE => seq RE`
Result:
```
['seq', 'RE'] a*b*c*
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

### The fix
At the last step, we want to switch to another alternative.
That is, at reminder text is `c*`, we do not want to search in `['seq', 'RE']`.
Instead, we want to search in `[seq]` only.
Result is good then:
```
['seq'] c*
debug: ['\\w+'] lit ['c']
debug: ['lit'] unit [['lit', 'c']]
debug: ['unit', '[*]'] star [['unit', ['lit', 'c']], '*']
debug: ['star'] seq [['star', ['unit', ['lit', 'c']], '*']]
debug: ['seq'] RE [['seq', ['star', ['unit', ['lit', 'c']], '*']]]
debug: ['seq', 'RE'] RE [['seq', ['star', ['unit', ['lit', 'b']], '*']], ['RE', ['seq', ['star', ['unit', ['lit', 'c']], '*']]]]
debug: ['seq', 'RE'] RE [['seq', ['star', ['unit', ['lit', 'a']], '*']], ['RE', ['seq', ['star', ['unit', ['lit', 'b']], '*']], ['RE', ['seq', ['star', ['unit', ['lit', 'c']], '*']]]]]
```
Thus, we want to have pattern: `RE => seq RE | seq`.


