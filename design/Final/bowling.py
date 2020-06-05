"""
UNIT 1: Bowling:

You will write the function bowling(balls), which returns an integer indicating
the score of a ten-pin bowling game.  balls is a list of integers indicating
how many pins are knocked down with each ball.  For example, a perfect game of
bowling would be described with:

    >>> bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    300

The rules of bowling are as follows:

(1) A game consists of 10 frames. In each frame you roll one or two balls,
except for the tenth frame, where you roll one, two, or three.  Your total
score is the sum of your scores for the ten frames.
(2) If you knock down fewer than ten pins with your two balls in the frame,
you score the total knocked down.  For example, bowling([8, 1, 7, ...]) means
that you knocked down a total of 9 pins in the first frame.  You score 9 point
for the frame, and you used up two balls in the frame. The second frame will
start with the 7.
(3) If you knock down all ten pins on your second ball it is called a 'spare'
and you score 10 points plus a bonus: whatever you roll with your next ball.
The next ball will also count in the next frame, so the next ball counts twice
(except in the tenth frame, in which case the bonus ball counts only once).
For example, bowling([8, 2, 7, ...]) means you get a spare in the first frame.
You score 10 + 7 for the frame; the second frame starts with the 7.
(4) If you knock down all ten pins on your first ball it is called a 'strike'
and you score 10 points plus a bonus of your score on the next two balls.
(The next two balls also count in the next frame, except in the tenth frame.)
For example, bowling([10, 7, 3, ...]) means that you get a strike, you score
10 + 7 + 3 = 20 in the first frame; the second frame starts with the 7.

"""


def is_spare(hand):
  return len(hand) == 2 and sum(hand) == 10

def is_strike(hand):
  return len(hand) == 1 and hand[0] == 10


def generate_hands(balls):
  hands = []
  n = len(balls)
  i = 0
  while i < n:
    if len(hands) == 9:
      hands.append(balls[i:])
      return hands

    if balls[i] + balls[i + 1] <= 10:
      hands.append([balls[i], balls[i + 1]])
      i += 2
    elif balls[i] == 10:
      hands.append([balls[i]])
      i += 1

  return None

def calc_hand(hands, i):
  hand = hands[i]
  score = sum(hand)
  # Now look forward for special move.
  if is_spare(hand):
    if i < 10:
      score += hands[i+1][0]
  elif is_strike(hand):
    if i < 10:
      balls_list = [item for sublist in hands[i+1:] for item in sublist]
      score += sum(balls_list[:2])

  return score

def bowling(balls):
  """Compute the total score for a player's game of bowling."""
  ## bowling([int, ...]) -> int
  ## your code here
  hands = generate_hands(balls)
  scores = 0
  for i, hand in enumerate(hands):
    score = calc_hand(hands, i)
    #print i, hand, score
    scores += score

  #print 'final', scores
  return scores

def test_hands():
  """
[[9, 1], [9, 1], [9, 1], [9, 1], [9, 1], [9, 1], [9, 1], [9, 1], [9, 1], [9, 1, 9]]
[10, 10, 10, 10, 10, 10, 10, 10, 10, [10, 10, 10]]
[10, [5, 5], 10, [5, 5], 10, [5, 5], 10, [5, 5], 10, [5, 5, 10]]
[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [10, 1, 0]]
  """
  print generate_hands([9, 1] * 10 + [9])
  print generate_hands([10] * 12)
  print generate_hands([10, 5, 5] * 5 + [10])
  print generate_hands([0, 0] * 9 + [10, 1, 0])


# test_hands()

def test_bowling():
  assert 0 == bowling([0] * 20)
  assert 20 == bowling([1] * 20)
  assert 80 == bowling([4] * 20)
  assert 190 == bowling([9, 1] * 10 + [9])
  assert 300 == bowling([10] * 12)
  assert 200 == bowling([10, 5, 5] * 5 + [10])
  assert 11 == bowling([0, 0] * 9 + [10, 1, 0])
  assert 12 == bowling([0, 0] * 8 + [10, 1, 0])
  print 'PASSED'

test_bowling()
