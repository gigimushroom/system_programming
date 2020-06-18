# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes
# as input capacities, goal, and (optionally) start. This function should
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the
# volume of a glass.
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i),
# ('empty', i), ('pour', i, j) where i and j are indices indicating the
# glass number.

import copy
import itertools


def more_pour_problem(capacities, goal, start=None):
  """The first argument is a tuple of capacities (numbers) of glasses; the
  goal is a number which we must achieve in some glass.  start is a tuple
  of starting levels for each glass; if None, that means 0 for all.
  Start at start state and follow successors until we reach the goal.
  Keep track of frontier and previously explored; fail when no frontier.
  On success return a path: a [state, action, state2, ...] list, where an
  action is one of ('fill', i), ('empty', i), ('pour', i, j), where
  i and j are indices indicating the glass number."""

  # your code here
  def is_done(state):
    return goal in state

  def p_successors(state):
    d = {}
    pairs = [i for i in itertools.combinations(range(len(capacities)), 2)]
    for (x, y) in pairs:
      d2 = successor_2_cup(x, y, state)
      d.update(d2)
    #print d
    return d

  def replace(seq, i, val):
    s = list(seq)
    s[i] = val
    return type(seq)(s)

  def successor_2_cup(i, j, state):
    # (x, y) is glass levels; X and Y are glass capacities
    x = state[i]
    y = state[j]
    X = capacities[i]
    Y = capacities[j]
    assert x <= X and y <= Y

    d = {}
    if y + x <= Y:
      s = replace(state, i, 0)
      s = replace(s, j, y + x)
      d[s] = 'pour', i, j
    else:
      s = replace(state, i, x - (Y - y))
      s = replace(s, j, Y)
      d[s] = 'pour', i, j

    if x+y <= X:
      s = replace(state, i, x+y)
      s = replace(s, j, 0)
      d[s] = 'pour', j, i
    else:
      s = replace(state, i, X)
      s = replace(s, j, y-(X-x))
      d[s] = 'pour', j, i

    d[replace(state, i, X)] = 'fill', i
    d[replace(state, j, Y)] = 'fill', j
    d[replace(state, i, 0)] = 'empty', i
    d[replace(state, j, 0)] = 'empty', j

    #         d.update {
    #             ((0, y+x) if y+x<=Y else (x-(Y-y), Y)): 'X->Y',
    #             ((x+y, 0) if x+y<=X else (X, y-(X-x))): 'X<-Y',
    #             (X, y): 'fill X', (x, Y): 'fill Y',
    #             (0, y): 'empty X', (x, 0):'empty Y',
    #         }
    return d

  if start is None:
    start = (0, ) * len(capacities)
  return shortest_path_search(start, p_successors, is_done)


def shortest_path_search(start, successors, is_goal):
  """Find the shortest path from start state to a state
  such that is_goal(state) is true."""
  if is_goal(start):
    return [start]
  explored = set()
  frontier = [[start]]
  while frontier:
    path = frontier.pop(0)
    s = path[-1]
    for (state, action) in successors(s).items():
      if state not in explored:
        explored.add(state)
        path2 = path + [action, state]
        if is_goal(state):
          #print path2
          return path2
        else:
          frontier.append(path2)
  return Fail


Fail = []


def test_more_pour():
  assert more_pour_problem((1, 2, 4, 8), 4) == [
    (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]

  assert more_pour_problem((1, 2, 4, 8), 3) == [
    (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0), ('pour', 2, 0), (1, 0, 3, 0)]

  assert more_pour_problem((1, 2, 4), 3) == [
      (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)]

  starbucks = (8, 12, 16, 20, 24)
  assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
  assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
  assert more_pour_problem((1, 3, 9, 27), 28) == []
  return 'test_more_pour passes'


print test_more_pour()