# DAA Practical 3: 0/1 Knapsack using Dynamic Programming
# Each item is either taken completely (1) or not taken (0) - no fractions allowed.
# Formula: dp[i][w] = max( dp[i-1][w] , value[i] + dp[i-1][w - weight[i]] )


def knapsack(weights, values, capacity):      # returns best value, chosen items and the DP table
    n = len(weights)                          # number of items
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]   # table of (n+1) rows x (capacity+1) columns, all 0

    for i in range(1, n + 1):                 # consider items one by one (row i = first i items)
        wt = weights[i - 1]                   # weight of item i (list index starts at 0)
        val = values[i - 1]                   # value of item i
        for w in range(capacity + 1):         # for every possible bag capacity 0..capacity
            dp[i][w] = dp[i - 1][w]           # option 1: do NOT take item i (copy value from row above)
            if wt <= w:                       # option 2 is possible only if item i fits in capacity w
                dp[i][w] = max(dp[i][w], val + dp[i - 1][w - wt])   # take it if that gives more value

    chosen = []                               # list of items picked, found by tracing back
    w = capacity                              # start from the bottom-right cell
    for i in range(n, 0, -1):                 # go from the last item to the first
        if dp[i][w] != dp[i - 1][w]:          # value changed -> item i was taken
            chosen.append(i)                  # remember item number i
            w -= weights[i - 1]               # reduce remaining capacity by its weight
    return dp[n][capacity], sorted(chosen), dp   # answer, items (in order), full table


def solve(weights, values, capacity):         # helper to run and print one problem
    print("Weights:", weights, " Values:", values, " Capacity:", capacity)   # show the input
    best, items, dp = knapsack(weights, values, capacity)                    # solve with DP
    print("DP table (rows = items, columns = capacity 0..W):")               # heading for the table
    for row in dp:                                                            # print each row
        print("  ", row)                                                      # one row of the table
    print("Maximum value :", best)                                            # the final answer
    print("Items chosen  :", items)                                           # item numbers (1-based)
    print("Total weight  :", sum(weights[i - 1] for i in items), "\n")        # must be <= capacity


solve([2, 3, 4, 5], [3, 4, 5, 6], 5)          # practical example -> answer 7 (items 1 and 2)
solve([3, 4, 6, 5], [2, 3, 1, 4], 8)          # assignment question -> answer 6 (items 1 and 4)
# Time  = O(n * W) : every cell of the (n+1) x (W+1) table is filled once
# Space = O(n * W) : size of the table (can be reduced to O(W) with a single row)
