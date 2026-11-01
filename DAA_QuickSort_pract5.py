# DAA Practical 5: Quick Sort - Deterministic vs Randomized
# Deterministic : pivot is ALWAYS the last element  -> sorted input gives worst case O(n^2)
# Randomized    : pivot is a RANDOM element         -> expected O(n log n) for any input
#
# Sample input : [10, 7, 8, 9, 1, 5]
# Sample output: Sorted: [1, 5, 7, 8, 9, 10]
# Sample input : already sorted list of n = 1000 numbers
# Sample output: Deterministic makes 499,500 comparisons (worst case n(n-1)/2),
#                Randomized makes only about 10,000 to 12,000 comparisons

import random                                 # random is used to pick a random pivot and make test data
import sys                                    # sys lets us raise Python's recursion limit
import time                                   # time is used to measure the running time

sys.setrecursionlimit(10000)                  # sorted input makes deterministic recursion n levels deep
comparisons = 0                               # global counter of element comparisons


def partition(arr, low, high):                # Lomuto partition with arr[high] as pivot
    global comparisons                        # we update the global counter
    pivot = arr[high]                         # choose the last element as pivot
    i = low - 1                               # i marks the end of the "smaller than pivot" part
    for j in range(low, high):                # scan every element except the pivot
        comparisons += 1                      # one comparison with the pivot
        if arr[j] <= pivot:                   # element belongs to the left (small) side
            i += 1                            # grow the small side by one
            arr[i], arr[j] = arr[j], arr[i]   # swap it into the small side
    arr[i + 1], arr[high] = arr[high], arr[i + 1]   # put the pivot just after the small side
    return i + 1                              # final position of the pivot


def quick_sort(arr, low, high, randomized=False):   # one function for both variants
    if low < high:                            # sub-array has 2 or more elements
        if randomized:                        # randomized variant?
            r = random.randint(low, high)     # pick a random index
            arr[r], arr[high] = arr[high], arr[r]   # move random element to the end so it becomes the pivot
        p = partition(arr, low, high)         # pivot is now at its correct sorted position p
        quick_sort(arr, low, p - 1, randomized)    # sort the left part
        quick_sort(arr, p + 1, high, randomized)   # sort the right part


def test(data, randomized):                   # sort a copy, return comparisons and time
    global comparisons                        # reset the global counter
    arr = data[:]                             # copy so the original data is not changed
    comparisons = 0                           # start counting from 0
    start = time.perf_counter()               # start timer
    quick_sort(arr, 0, len(arr) - 1, randomized)   # sort
    t = time.perf_counter() - start           # elapsed time
    assert arr == sorted(data)                # make sure the result is really sorted
    return comparisons, t                     # return the measurements


sample = [10, 7, 8, 9, 1, 5]                  # small example
arr = sample[:]                               # copy of the sample
quick_sort(arr, 0, len(arr) - 1)              # deterministic sort
print("Original:", sample, " Sorted:", arr)   # show the result

random.seed(1)                                # fixed seed so the output is repeatable
n = 1000                                      # input size for the analysis
inputs = {                                    # different kinds of input
    "Random": random.sample(range(10 * n), n),   # random order -> average case
    "Sorted": list(range(n)),                    # already sorted -> worst case for last-element pivot
    "Reverse": list(range(n, 0, -1)),            # reverse sorted -> also worst case
}
print(f"\n{'Input':<10}{'Variant':<15}{'Comparisons':<14}{'Time (s)'}")   # table header
for name, data in inputs.items():             # for every input type
    for randomized in (False, True):          # run both variants
        c, t = test(data, randomized)         # measure
        label = "Randomized" if randomized else "Deterministic"   # readable name
        print(f"{name:<10}{label:<15}{c:<14}{t:.5f}")             # one row

print("\nDeterministic: best/average O(n log n), worst O(n^2)")    # summary for the write-up
print("Randomized   : expected O(n log n) for every input")        # random pivot avoids bad splits
print("Space        : O(log n) average recursion stack, O(n) worst case")
