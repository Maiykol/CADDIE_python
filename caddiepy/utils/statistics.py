import numpy as np

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def contingency_table(pred, test, cutoff=10):
    # calculates contingency table comparing a list of predictions "pred" to list of expected elements "test"
    # lists need to be of same length and contain the same elements
    # cut lists based of cutoff
    test_cutoff = test[:cutoff]
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for i, x in enumerate(pred):
        if i < cutoff:
            if x in test_cutoff:
                tp += 1
            else:
                fp += 1
        else:  # i > cutoff
            if x in test_cutoff:
                fn += 1
            else:
                tn += 1
    return [[tp, fp], [fn, tn]]


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = [[0. for x in range(size_y)] for y in range(size_x)]
    for x in range(size_x):
        matrix[x][0] = x
    for y in range(size_y):
        matrix[0][y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix[x][y] = min(
                    matrix[x-1][y] + 1,
                    matrix[x-1][y-1],
                    matrix[x][y-1] + 1
                )
            else:
                matrix[x][y] = min(
                    matrix[x-1][y] + 1,
                    matrix[x-1][y-1] + 1,
                    matrix[x][y-1] + 1
                )
    return matrix[size_x - 1][size_y - 1]