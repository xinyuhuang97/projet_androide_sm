import os
from sm import *
import random
import time
import matplotlib.pyplot as plt



size_K=20
size_S=20


lt1,lt2,lt3,lt4=[],[],[],[]
lv1,lv2,lv3,lv4=[],[],[],[]

nb_for_generation=5
for i in range(5,(size_S+1)):
    K=[i]*i
    S=[j for j in range(1,i+1)]

    t=[0]*4
    sl1, sl2, sl3 ,sl4 = [], [], [], []
    import sys
    print(i)
    for j in range(nb_for_generation):
        female,male,s_f,s_m=gennere_set_f_m(i,i)
        ins=genere_instance(K,S, male, female, s_m, s_f)
        start = time.time()
        res3=calcul_difference_entre_gen(algo_3(deepcopy(ins)))
        print(res3)
        stop = time.time()
        t[2]+=stop-start
        sl3.append(res3)
    print("i==",i)

    lv3.append(sl3)
    lt3.append(np.mean(t[2]))
