import sys
from scipy.sparse import csr_matrix, find
import numpy as np
row = np.array([0, 0, 1, 1, 2, 2])
col = np.array([0, 2, 1, 2, 0, 3])
values = np.array([2, 3, 5, 1, 8, 1])
csr = csr_matrix((values, (row, col)), shape=(3,4))
print (csr.toarray())
A1 = []
A2 = []
A1, A2 = (csr.nonzero())
for i in range(len(A1)):
    print (csr[A1[i],A2[i]])
Y = np.asarray([1, 1, -1])
index = (np.arange(csr.shape[0]))
print (index)
np.random.shuffle(index)
print (index)
#csr = csr[index,:]
#Y = Y[index]
print (csr)
#(csr[index,:])
print (Y)
#(Y[index])
positive_indices = np.argwhere(Y == 1.0).flatten()
negative_indices = np.argwhere(Y == -1.0).flatten()
sum = 0
print (csr.A)
R = []
C = []
V = []
R, C, V = (find(csr))
count_positive = []
count_positive = np.zeros([1,csr.shape[1]])
count_negative = np.zeros([1,csr.shape[1]])
print (csr.shape[0])
'''
for i,v  in enumerate(count_positive):
    print (i)
for i,v in enumerate(R):
    print (i)
for i,v in enumerate(R):
    for j in positive_indices:
        if (j == R[i]):
            #print (j)
            count_positive[0, C[i]] = count_positive[0, C[i]] + V[i]
    for j in negative_indices:
        if (j == R[i]):
            #print (j)
            count_negative[0, C[i]] = count_negative[0, C[i]] + V[i]
    print (i, v)
sum = 0
for i in positive_indices:
    print (i)
    sum = sum + (csr[i].sum(axis=1))
    #for j in (csr[i]):
        #print (j)
print (sum)
sum = 0
for i in negative_indices:
    print (i)
    sum = sum + (csr[i].sum(axis=1))
print (sum)
'''
