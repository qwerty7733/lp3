# DAA Practical 1: Fibonacci numbers - non-recursive (iterative) and recursive
# Series: 0, 1, 1, 2, 3, 5, 8, ...   Rule: F(n) = F(n-1) + F(n-2), F(0) = 0, F(1) = 1

import time                                   # time module is used to measure how long each method takes


# ---------------- Method 1: Non-recursive (iterative) ----------------
def fib_iterative(n):                         # returns the n-th Fibonacci number using a loop
    a, b = 0, 1                               # a = F(0), b = F(1) : the first two numbers
    for _ in range(n):                        # repeat n times to move forward n steps
        a, b = b, a + b                       # shift: new a = old b, new b = sum of old a and b
    return a                                  # after n steps, a holds F(n)
# Time  = O(n)  -> the loop runs n times
# Space = O(1)  -> only two variables are used, whatever the value of n


# ---------------- Method 2: Recursive ----------------
calls = 0                                     # global counter: how many times fib_recursive() is called

def fib_recursive(n):                         # returns the n-th Fibonacci number using recursion
    global calls                              # we want to change the global variable 'calls'
    calls += 1                                # count this call
    if n <= 1:                                # base case: F(0) = 0 and F(1) = 1
        return n                              # stop the recursion here
    return fib_recursive(n - 1) + fib_recursive(n - 2)   # recursive case: sum of the previous two
# Time  = O(2^n) -> every call makes two more calls, same values are computed again and again
# Space = O(n)   -> the deepest chain of calls waiting on the stack is n


# ---------------- Bonus: Recursive with memoization (top-down DP) ----------------
def fib_memo(n, memo={}):                     # memo is a dictionary that remembers answers already found
    if n <= 1:                                # base case
        return n                              # F(0) = 0, F(1) = 1
    if n not in memo:                         # compute only if we have not computed F(n) before
        memo[n] = fib_memo(n - 1) + fib_memo(n - 2)   # store the result so it is never recomputed
    return memo[n]                            # return the stored answer
# Time = O(n), Space = O(n) -> shows how DP fixes the slow recursion


# ---------------- Main program ----------------
n = 10                                                    # number of terms to print
print("First", n, "Fibonacci numbers")                    # heading
print("Iterative :", [fib_iterative(i) for i in range(n)])   # build list F(0)..F(9) with the loop method
print("Recursive :", [fib_recursive(i) for i in range(n)])   # same list with the recursive method
print("Memoized  :", [fib_memo(i) for i in range(n)])        # same list with the memoized method

print("\nTime comparison")                                # heading for the analysis table
print(f"{'n':<5}{'F(n)':<10}{'Iterative(s)':<15}{'Recursive(s)':<15}{'Recursive calls'}")  # table header
for n in [10, 20, 25, 30]:                                # try bigger and bigger n
    start = time.perf_counter()                           # start the timer
    v1 = fib_iterative(n)                                 # run the iterative method
    t1 = time.perf_counter() - start                      # time taken = now - start

    calls = 0                                             # reset the call counter before each run
    start = time.perf_counter()                           # start the timer again
    v2 = fib_recursive(n)                                 # run the recursive method
    t2 = time.perf_counter() - start                      # time taken by recursion

    assert v1 == v2                                       # both methods must give the same answer
    print(f"{n:<5}{v1:<10}{t1:<15.6f}{t2:<15.6f}{calls}")    # print one row of the table

print("\nComplexity summary")                             # final summary for the write-up
print("Iterative : Time O(n),   Space O(1)")              # loop with two variables
print("Recursive : Time O(2^n), Space O(n)")              # exponential calls, stack depth n
print("Memoized  : Time O(n),   Space O(n)")              # each value computed once, stored in memo
