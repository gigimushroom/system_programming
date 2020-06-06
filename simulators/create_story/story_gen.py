# coding=utf-8
import pprint as pp
import random

"""
data structure:
dict, key is 'prev0 prev1'
value is list of suffix.
"""

data = "Show your flowcharts and conceal your tables and I will be mystified. Show your tables and your flowcharts" \
        " will be obvious."

NONWORD = '\n'


def build(data_feeds):
  d = {}
  words = data_feeds.split()
  #print words
  max_size = len(words)

  for i, w in enumerate(words):
    if i >= max_size - 2:
      break

    key = w + ' ' + words[i + 1]
    v = words[i + 2]
    if key in d:
      d[key].append(v)
    else:
      d[key] = [v]
  #pp.pprint(d)
  return d


#build(data)

def generate(book, start_word, nwords):
  result = [start_word]
  prefix = start_word
  for _ in range(nwords):
    if prefix not in book:
      print prefix, 'not in dict'
      break

    words = book[prefix]
    word = random.choice(words)
    result.append(word)
    prev0, prev1 = prefix.split()
    prefix = prev1 + ' ' + word
    #print '...new prefix', prefix

  return ' '.join(result) + '.'

#print generate(build(data), 'Show your', 10)
#print generate(build(data), 'conceal your', 10)


d1 = "if you feel like you have the most interesting job on the planet, well, perfect! It sh" \
     "ouldn’t be hard to use it as plot-fodder for a great short story. On the other hand, if you " \
     "find yourself yawning a lot at work, ask yourself: What could happen to make this work day inte" \
     "resting? Let’s say you work as a receptionist but your real passion lies with art. Write a story " \
     "about a receptionist who sees a colleague hang a new piece of art in their cubicle — one the receptio" \
     "nist recognizes as being famous for going missing a century ago."


f = open("story.txt", "r")
print generate(build(f.read()), 'I would', 30)