"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    "*** REPLACE THIS LINE ***"
    total = 0
    gotOne = False
    for x in range (0, num_rolls):
        roll = dice()
        if roll == 1: gotOne = True
        else: total = total + roll
    return total if not gotOne else 0
    # END Question 1

def is_prime(num):
    if num < 2: return False
    for i in range(2,int(num**0.5)+1):
        if num%i==0:
            return False
    return True

def next_prime(num):
    while(1):
        num = num + 1
        if is_prime(num): return num

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    "*** REPLACE THIS LINE ***"
    if num_rolls == 0:
        result = max([int(i) for i in str(opponent_score)]) + 1
    else:
        result = roll_dice(num_rolls, dice)
    return next_prime(result) if is_prime(result) else result

    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    "*** REPLACE THIS LINE ***"
    return four_sided if ((score + opponent_score) % 7 == 0) else six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    "*** REPLACE THIS LINE ***"
    # break the score down to integers and store the last two
    score0_last2 = [int(i) for i in str(score0 % 100)]
    score1_last2 = [int(i) for i in str(score1 % 100)]
    # make sure there are two integers
    if len(score0_last2) == 1: score0_last2.insert(0, 0) # faster than score0_last2 = [0] + score0_last2
    if len(score1_last2) == 1: score1_last2.insert(0, 0) # faster than score1_last2 = [0] + score1_last2

    return score0_last2[0] == score1_last2[1] and score1_last2[0] == score0_last2[1]

    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    "*** REPLACE THIS LINE ***"

    while (score0 < goal) and (score1 < goal):
        
        if who == 0:
            this_score = take_turn(strategy0(score0, score1), score1, select_dice(score0, score1))
            # print("Score0", this_score)
            if this_score == 0:
                score1 += strategy0(score0, score1)
            else: 
                score0 += this_score
        else:
            this_score = take_turn(strategy1(score1, score0), score0, select_dice(score1, score0))
            # print("Score1", this_score)
            if this_score == 0:
                score0 += strategy1(score1, score0)
            else: 
                score1 += this_score
        
        if (is_swap(score0, score1)):
            temp = score0
            score0 = score1
            score1 = temp

        who = other(who)
        # print (score0, score1)

    # END Question 5
    return score0, score1

# import hog
# hog.four_sided = hog.make_test_dice(1)
# hog.six_sided = hog.make_test_dice(3)
# always = hog.always_roll
# s0, s1 = hog.play(always(5), always(5), goal=10)


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    "*** REPLACE THIS LINE ***"
    def return_average(*args):
        result = 0
        for i in range (0, num_samples):
            result += fn(*args)
        return result / num_samples
    return return_average
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    "*** REPLACE THIS LINE ***"
    max_average = 0
    score_map = {}
    
    for i in range(1, 11):
        average = make_averaged(roll_dice, num_samples) # function to get average score of calling roll_dice num_samples of times
        average_score = average(i, dice)
        if average_score >= max_average:
            max_average = average_score
            if average_score in score_map.keys():
                score_map[average_score].append(i)
            else:
                score_map[average_score] = [i]
    return min(score_map[max_average])
    # END Question 7

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    "*** REPLACE THIS LINE ***"
    roll0_score = max([int(i) for i in str(opponent_score)]) + 1
    roll0_score_hogtimus = next_prime(roll0_score) if is_prime(roll0_score) else roll0_score
    return 0 if (roll0_score_hogtimus >= margin) else num_rolls # Replace this statement
    # END Question 8

def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    "*** REPLACE THIS LINE ***"
    roll0_score = max([int(i) for i in str(opponent_score)]) + 1
    roll0_score_hogtimus = next_prime(roll0_score) if is_prime(roll0_score) else roll0_score
    new_score = score + roll0_score_hogtimus
    if new_score == opponent_score:
        return num_rolls
    elif is_swap(new_score, opponent_score) and opponent_score > new_score:
        return 0
    else:
        return num_rolls
    # END Question 9

def wild_strategy(score, opponent_score, num_rolls=5):
    points = max((int(opponent_score / 10), int(opponent_score % 10))) + 1
    tot_score = score + points
    if (tot_score + opponent_score) % 7 == 0:
        return 0    
    else:
        return num_rolls

def desired_pigout(score, opponent_score):
    num_rolls = 1
    for i in range(3,11):
        num_rolls = i
        if is_swap(score, opponent_score + i) == True:
            return num_rolls
    return 1

# try:
#     from utils import final_win_rate
# except ImportError:
#     from tests.utils import final_win_rate
# print('\nFinal strategy win rate:', final_win_rate())

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN Question 10
    "*** REPLACE THIS LINE ***"
    # if select_dice(score, opponent_score) == four_sided:
    #     num_rolls = 4
    # else: 
    #     num_rolls = 6

    # diff = score - opponent_score
    
    # if diff > 0:
    #     margin = 2
    # else:
    #     margin = 6

    # if swap_strategy(score, opponent_score, num_rolls) == 0:
    #     return 0

    # if bacon_strategy(score, opponent_score, margin, num_rolls) == 0:
    #     return 0

    # # if diff < -21:
    # #     return 5
    # # if diff < -11:
    # #     return 6

    # return num_rolls
    num_rolls = 4
    diff = 100 - score
    bacon_pts = max((int(opponent_score / 10), int(opponent_score % 10))) + 1
    
    if bacon_pts >= diff:
        return 0    
    if swap_strategy(score, opponent_score, 4) == 0:
        return 0
    if desired_pigout(score, opponent_score) > 1:
        if score < opponent_score:    
            return desired_pigout(score, opponent_score)
    if bacon_strategy(score, opponent_score, 6, 4) == 0:
        return 0
    if wild_strategy(score, opponent_score, 4) == 0:
        return 0

    if score - 21 > opponent_score:
        return 3
    if score - 11 > opponent_score:
        return 2
    if score + 20 < opponent_score:
        return 5
    if score + 32 < opponent_score:
        return 6
    
    return num_rolls

    # return 5  # Replace this statement
    # END Question 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
