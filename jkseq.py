# State Machine Sequence Controller Logic Design for use with J-K Flip Flops
# Each Flip Flop identified as Qn..Q0 where n = number of bits - 1
# n = bit number with bit 0 being least significant bit position
# Each Flip Flop Qn has Jn and Kn imputs with Qn and !Qn outputs
# Author:  Darrell Harriman  harrimand@gmail.com

from pandas import DataFrame as dF
from pandas import concat
import numpy as np
from os import system
from qm import *

cls = lambda: system("clear")

# seq = [0, 15, 1, 14, 3, 12, 2, 13, 6, 9, 7, 8, 5, 10, 4, 11]
# seq = [0, 15, 14, 12, 13, 9, 8, 10, 11, 15]
seq = [0, 1, 2, 4, 8, 9, 10, 12, 13, 14, 15, 7, 11, 3, 5, 0]
# seq = [0, 3, 7, 5, 4, 1, 3]
# seq = [0, 5, 2, 6, 1, 3, 5]
# seq = [0, 4, 3, 5, 2, 6, 1, 4]


def dispDF(dFrame, cols):
    '''Display dataFrame with count sequence and requred J + K states.'''
    JK_1 = {}
    JK_X = {}
    JK_1 = {jk:dFrame.index[jkdF[jk] == '1'].tolist() for jk in cols}
    JK_X = {jk:dFrame.index[jkdF[jk] == 'X'].tolist() for jk in cols}
    print(" Implicants:")
    # for k in JK_1.keys():
    for k in mkSet(JK_1).keys():
        print('\t', k, JK_1[k])
    print("\n")
    print(" Don't Cares:")
    for k in JK_X.keys():
        print('\t', k, JK_X[k])
    print("\n")
    return (JK_1, JK_X)

def SSOPS(jkdF):
    ''' Use qm library to generate Simplified Sum of Products for each
    J and K input'''
    Cols = list(jkdF.columns)[list(jkdF.columns).index('|')+1:]
    imps, DC = dispDF(jkdF, jkCols)
    bl = max([max(n) for n in list(imps.values()) if len(n) > 0]).bit_length()
    Qvars = "".join([chr(65+n) for n in range(bl)])
    SS = {jk:qmSimp(imps[jk], DC[jk], Qvars) for jk in Cols if imps[jk]}
    SOPS = {s:(jkdF[s].iloc[0] if s not in SS.keys() else SS[s]) for s in Cols}
    return(SOPS)

def dispSOPS(SOPS):
    '''Display list of Sum of Products expressions for each J and K input'''
    print("\n SOPS:")
    for i in SOPS.items():
        print("\t",i[0],": ",i[1])
    print("\n")

def mkSet(jkdict):
    ''' Remove duplicates values dictionary'''
    R = {}
    for L in jkdict.keys():
        C = []
        for i in jkdict[L]:
            if i not in C:
                C.append(i)
        R[L] = C
    return R

def fillNC(dataF):
    '''Fill n-bit sequence with Don't Care states for missing implicants'''
    bL = max(list(dataF.index)).bit_length()
    bR = list(range(2**bL))
    niL = [n for n in bR if n not in list(dataF.index)]
    nc = dF([[' ']*bL+['|']+['X']*(2*bL)], index=niL, columns=dataF.columns)
    return concat([dataF, nc], axis=0)

def ch2Qn(SOPS):
    '''Substitute A, B, C variables in SOP for Qn..Q0 to represent Flip Flops'''
    ABC = [chr(n+65) for n in range(len(list(SOPS.keys()))//2)]
    R = list(range(len(list(SOPS.keys()))//2-1, -1,-1))
    qn = ['Q'+str(n)+' ' for n in R]
    for a, q in zip(ABC, qn):
        for i, sop in list(SOPS.items()):
            if(a in sop):
                SOPS[i] = sop.replace(a, q).replace('  ', ' ')
    return SOPS

jin = ['0', '1', 'X', 'X']
kin = jin[::-1]
ls = len(seq)
bl = max(seq).bit_length()
seqbin = [[int(b) for b in bin(B)[2:].zfill(bl)] for B in seq]
jx = [[jin[seqbin[n][c]*2+ seqbin[(n+1)% ls][c]] for c in range(bl)] for n in range(ls)]
kx = [[kin[seqbin[n][c]*2+ seqbin[(n+1)% ls][c]] for c in range(bl)] for n in range(ls)]

Z = [[c + d for c, d in zip(a, b)] for a, b in zip(jx, kx)]
jkx = np.array([list("".join(a)) for a in Z])
FFCols = ['Q' + str(n) for n in range(bl-1,-1,-1)]
Qn = dF(np.array([[str(n) for n in m] for m in seqbin]), index = seq, columns = FFCols)
jkCols = ''.join(['J'+str(n)+' K' + str(n) + ' ' for n in range(bl-1, -1, -1)]).split()
jkFFseq = dF(jkx, index=seq, columns = jkCols)
Div = dF(np.array([['|']]*len(seq)), index=seq, columns=['|'])
jkdF = concat([Qn, Div, jkFFseq], axis=1)
print('\n', jkdF, '\n\n')

jkdF = fillNC(jkdF) # Fill dataFrame with missing implicants and Don't-Cares
# jkdF = jkdF[~jkdF.index.duplicated()]

# imps, DC = dispDF(jkdF, jkCols)
SOPS = SSOPS(jkdF) # Use qm.py to generate simplified sum of products
SOPS = ch2Qn(SOPS) # Replace charasters in SOP A,B,... with Qn, Qn-1..Q0
dispSOPS(SOPS) # Display Sum of Products expressions for each J and K input


