def diff(x, y, z):
    """Return whether one argument is the difference between the other two.

    x, y, and z are all integers.

    >>> diff(5, 3, 2) # 5 - 3 is 2
    True
    >>> diff(2, 3, 5) # 5 - 3 is 2
    True
    >>> diff(2, 5, 3) # 5 - 3 is 2
    True
    >>> diff(-2, 3, 5) # 3 - 5 is -2
    True
    >>> diff(-5, -3, -2) # -5 - -2 is -3
    True
    >>> diff(-2, 3, -5) # -2 - 3 is -5
    True
    >>> diff(2, 3, -5)
    False
    >>> diff(10, 6, 4)
    True
    >>> diff(10, 6, 3)
    False
    """
    "*** YOUR CODE HERE ***"
    return (x - y == z) or (x - z == y) or (y - z == x) or (y - x == z) or (z - x == y) or (z - y == x)


def abundant(n):
    """Print all ways of forming positive integer n by multiplying two positive
    integers together, ordered by the first term. Then, return whether the sum
    of the proper divisors of n is greater than n.

    A proper divisor of n evenly divides n but is less than n.

    >>> abundant(12) # 1 + 2 + 3 + 4 + 6 is 16, which is larger than 12
    1 * 12
    2 * 6
    3 * 4
    True
    >>> abundant(14) # 1 + 2 + 7 is 10, which is not larger than 14
    1 * 14
    2 * 7
    False
    >>> abundant(16)
    1 * 16
    2 * 8
    4 * 4
    False
    >>> abundant(20)
    1 * 20
    2 * 10
    4 * 5
    True
    >>> abundant(22)
    1 * 22
    2 * 11
    False
    >>> r = abundant(24)
    1 * 24
    2 * 12
    3 * 8
    4 * 6
    >>> r
    True
    """
    "*** YOUR CODE HERE ***"
    factors = [x for x in range(1, n) if (n) % x == 0]
    printed = []
    for x in factors:
        if x not in printed:
            print (x, '*', n // x)
            printed.append(x)
            printed.append(n // x)
    return sum(factors) > n


def amicable(n):
    """Return the smallest amicable number greater than positive integer n.

    Every amicable number x has a buddy y different from x, such that
    the sum of the proper divisors of x equals y, and
    the sum of the proper divisors of y equals x.

    For example, 220 and 284 are both amicable because
    1 + 2 + 4 + 5 + 10 + 11 + 20 + 22 + 44 + 55 + 110 is 284, and
    1 + 2 + 4 + 71 + 142 is 220

    >>> amicable(5)
    220
    >>> amicable(220)
    284
    >>> amicable(284)
    1184
    >>> r = amicable(5000)
    >>> r
    5020
    """
    "*** YOUR CODE HERE ***"
    num1 = n + 1
    skipped = []
    while 1:
        factors1 = [x for x in range(1, num1) if (num1) % x == 0]
        num2 = sum(factors1)
        factors2 = [x for x in range(1, num2) if (num2) % x == 0]
        if sum(factors2) == num1 and num1 != num2:
            r = min(num1, num2)
            if r > n: return r
            elif max(num1, num2) in skipped: return max(num1, num2)
            else: 
                skipped.append(num1)
                skipped.append(num2)
        else:
            num1 = num1 + 1
