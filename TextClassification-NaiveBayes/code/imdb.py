import os
import sys

# Sparse matrix implementation
from scipy.sparse import csr_matrix
from Vocab import Vocab
import numpy as np
from collections import Counter

np.random.seed(1)


class IMDBdata:
    def __init__(self, directory, vocab=None):
        """ Reads in data into sparse matrix format """
        # print directory
        pFiles = os.listdir("%s/pos" % directory)
        nFiles = os.listdir("%s/neg" % directory)

        if not vocab:
            self.vocab = Vocab()
        else:
            self.vocab = vocab

        # For csr_matrix (see http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.sparse.csr_matrix.html#scipy.sparse.csr_matrix)

        self.X_reviews = []
        X_values = []
        X_row_indices = []
        X_col_indices = []
        Y = []

        # Read positive files
        for i in range(len(pFiles)):
            f = pFiles[i]
            lines = ""
            # print("Positive file::", f)
            for line in open("%s/pos/%s" % (directory, f), errors='ignore'):
                lines += line
                wordCounts = Counter([self.vocab.GetID(w.lower()) for w in line.split(" ")])
                for (wordId, count) in wordCounts.items():
                    if wordId >= 0:
                        X_row_indices.append(i)
                        X_col_indices.append(wordId)
                        X_values.append(count)
            Y.append(+1.0)
            self.X_reviews.append(lines)

        # Read negative files
        for i in range(len(nFiles)):
            f = nFiles[i]
            # print("Negative file::", f)
            lines = ""
            for line in open("%s/neg/%s" % (directory, f), errors='ignore'):
                lines += line
                wordCounts = Counter([self.vocab.GetID(w.lower()) for w in line.split(" ")])
                for (wordId, count) in wordCounts.items():
                    if wordId >= 0:
                        X_row_indices.append(len(pFiles) + i)
                        X_col_indices.append(wordId)
                        X_values.append(count)
            Y.append(-1.0)
            self.X_reviews.append(lines)

        self.vocab.Lock()

        # for i in range(11):
        #     print("Word:", self.vocab.GetWord(i))
        #
        # print("Length of X_row_indices:", len(X_row_indices))
        # print("Length of X_col_indices:", len(X_col_indices))
        # print("Length of X_values:", len(X_values))
        #
        # print("X_row_indices::", X_row_indices)
        # print("X_col_indices::", X_col_indices)
        # print("X_values::", X_values)

        # Create a sparse matrix in csr format
        self.X = csr_matrix((X_values, (X_row_indices, X_col_indices)),
                            shape=(max(X_row_indices) + 1, self.vocab.GetVocabSize()))
        self.Y = np.asarray(Y)

        # Randomly shuffle
        index = np.arange(self.X.shape[0])
        np.random.shuffle(index)
        self.X = self.X[index, :]
        self.Y = self.Y[index]


if __name__ == "__main__":
    data = IMDBdata("../../data/aclImdb/train/")
    print(data.X)
