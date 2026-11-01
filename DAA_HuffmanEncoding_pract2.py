# DAA Practical 2: Huffman Encoding using a Greedy strategy
# Idea: frequent characters get SHORT codes, rare characters get LONG codes (lossless compression)
#
# Sample input : text "mississippi"  ->  frequencies m:1  i:4  s:4  p:2
# Sample output: codes  i = 0, s = 11, m = 100, p = 101
#                Encoded bits : 100011110111101011010
#                Huffman bits : 21  vs  fixed 8-bit ASCII: 88
#                Decoded OK   : True

import heapq                                  # heapq gives a min-heap (priority queue): pop always returns the smallest
from collections import Counter               # Counter counts how many times each character appears


class Node:                                   # one node of the Huffman tree
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq                      # frequency of this node (sum of children for internal nodes)
        self.char = char                      # the character (only leaf nodes have a character)
        self.left = left                      # left child  (edge labelled 0)
        self.right = right                    # right child (edge labelled 1)

    def __lt__(self, other):                  # "less than" lets heapq compare two nodes
        return self.freq < other.freq         # the node with the smaller frequency is "smaller"


def build_tree(freq):                         # freq is a dict like {'a': 5, 'b': 9}
    heap = [Node(f, ch) for ch, f in freq.items()]   # make one leaf node for every character
    heapq.heapify(heap)                       # arrange the list as a min-heap in O(n)
    while len(heap) > 1:                      # keep merging until only one node (the root) is left
        x = heapq.heappop(heap)               # GREEDY step: take the smallest frequency node
        y = heapq.heappop(heap)               # take the second smallest frequency node
        print(f"Merge {x.freq} + {y.freq} = {x.freq + y.freq}")   # show each merge step
        heapq.heappush(heap, Node(x.freq + y.freq, None, x, y))  # new parent node goes back into the heap
    return heap[0]                            # the last node is the root of the Huffman tree


def make_codes(node, code="", codes=None):    # walk the tree and build the code of every character
    if codes is None:                         # first call: create an empty dictionary
        codes = {}                            # will hold {character: code}
    if node.char is not None:                 # leaf node reached -> this is a real character
        codes[node.char] = code or "0"        # save its code ("0" if the text has only one character)
        return codes                          # nothing below a leaf
    make_codes(node.left, code + "0", codes)  # going left adds a 0
    make_codes(node.right, code + "1", codes) # going right adds a 1
    return codes                              # return the finished dictionary


def encode(text, codes):                      # turn text into a string of bits
    return "".join(codes[ch] for ch in text)  # replace every character by its code and join them


def decode(bits, codes):                      # turn the bit string back into text
    reverse = {c: ch for ch, c in codes.items()}   # reverse lookup: code -> character
    result, current = "", ""                  # result text and the bits read so far
    for b in bits:                            # read one bit at a time
        current += b                          # add the bit to the current code
        if current in reverse:                # prefix property: the first match is always correct
            result += reverse[current]        # output the character
            current = ""                      # start reading the next code
    return result                             # decoded text


def huffman(text):                            # complete Huffman process for one message
    print("\nText:", text)                    # show the input
    freq = Counter(text)                      # count frequency of every character
    print("Frequencies:", dict(freq))         # show the counts
    root = build_tree(freq)                   # Part 1: build the tree (greedy merging)
    codes = make_codes(root)                  # Part 2: read codes from the tree
    print("Char  Freq  Code")                 # table header
    for ch in sorted(codes, key=lambda c: len(codes[c])):   # shortest codes first
        print(f"{ch:<5} {freq[ch]:<5} {codes[ch]}")         # one row per character
    bits = encode(text, codes)                # compress the text
    print("Encoded bits :", bits)             # show the bit string
    print("Huffman bits :", len(bits), " vs  fixed 8-bit ASCII:", len(text) * 8)   # compression achieved
    print("Decoded OK   :", decode(bits, codes) == text)   # check that nothing was lost (lossless)


huffman("mississippi")                        # viva question example
huffman("aaaabbc")                            # small example
huffman("aaaa")                               # edge case: only one distinct character
# Time  = O(n log n) : n-1 merges, each heap push/pop costs O(log n)  (n = distinct characters)
# Space = O(n)       : the heap and the tree store about 2n nodes
