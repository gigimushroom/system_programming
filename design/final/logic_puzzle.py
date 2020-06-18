"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools

def solve_logic_puzzle():
  """Return a list of the names of the people, in the order they arrive."""
  ## your code here; you are free to define additional functions if needed

  names = ['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']
  items = ['laptop', 'droid', 'tablet', 'iphone']
  job = ['programmer', 'writer', 'manager', 'designer']

  dates_list = Monday, Tuesday, Wednesday, Thursday, Friday = (1, 2, 3, 4, 5)
  orderings = list(itertools.permutations(dates_list))

  return next([Hamming, Knuth, Minsky, Simon, Wilkes]
              for (Hamming, Knuth, Minsky, Simon, Wilkes) in orderings
              if Knuth == Simon + 1  # 6
              for (laptop, droid, tablet, iphone, _) in orderings
              if Wednesday is laptop  # 1
              if Friday is not tablet  # 8
              for (programmer, writer, manager, designer, _) in orderings
              if Thursday is not designer  # 7
              if programmer is not Wilkes  # 2
              if (programmer is Wilkes and droid is Hamming) or (programmer is Hamming and droid is Wilkes)  # 3
              if writer is not Minsky  # 4
              if Knuth is not manager and tablet is not manager  # 5
              if designer is not droid  # 9
              if Knuth == manager + 1  # 10
              if (laptop is Monday and Wilkes is writer) or (laptop is writer and Wilkes is Monday)  # 11
              if (iphone is Tuesday) or (tablet is Tuesday)  # 12
              )


def logic_puzzle():
  Hamming, Knuth, Minsky, Simon, Wilkes = solve_logic_puzzle()
  print Hamming, Knuth, Minsky, Simon, Wilkes
  d = {'Hamming': Hamming, 'Knuth': Knuth, 'Minsky': Minsky, 'Simon': Simon, 'Wilkes': Wilkes}
  results = sorted((v, k) for k, v in d.iteritems())
  print results
  return [name for day, name in results]

print logic_puzzle()


# Example. The person who arrived on Wednesday bought the laptop.
# => if laptop is 3

