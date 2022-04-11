
"""
Algo de Gale-Shapley
"""
import pandas as pd
import numpy as np
from algo3 import *
from algo4 import *

name_male=pd.read_csv('./name_male.csv')['Name'].unique()
name_female=pd.read_csv('./name_female.csv')['Name'].unique()

import random
def gennere_set_f_m(dim1,dim2=0):
    if dim2==0:
        dim2=dim1
    s_f=dict()
    s_m=dict()
    female=random.choices(name_female, k=dim1)
    male=random.choices(name_male, k=dim2)
    for i in range(dim1):
        x=male.copy()
        random.shuffle(x)
        s_f[female[i]]=["Single",x]
    for i in range(dim2):
        y=female.copy()
        random.shuffle(y)
        s_m[male[i]]=["Single",y]
    return female,male,s_f,s_m


#Notons K->nombre d'homme, S->nombre de femme
#       male->la liste des homme, female
#       pm->preference complet des hommes, pf

def genere_pref_dyn(male, female, pm, pf):
    nbmale=len(male)
    nbmale=len(female)
    dic_male=dict()
    dic_female=dict()
    for i in male:
        #print(pm[i][1])
        lm=[fm for fm in pm[i][1] if fm in female]
        dic_male[i]=['Single',lm]
    for j in female:
        lf=[ml for ml in pf[j][1] if ml in male]
        dic_female[j]=['Single',lf]
    return dic_male,dic_female


def genere_instance(K, S, male, female, pm, pf):
    list_instance=[]
    for i in range((len(K))):
        male_i=male[:K[i]]
        female_i=female[:S[i]]
        pm_i, pf_i=genere_pref_dyn(male_i,female_i,pm,pf)
        list_instance.append( (male_i,female_i,pm_i, pf_i))
        #list_mariage.append(Gale_Shapley(female_i,male_i,pf_i,pm_i))
    return list_instance



def calcul_difference_entre_gen(list_mariage):
    print(list_mariage)
    mariage_avant=list_mariage[0]
    val=0
    for i in range(1, len(list_mariage)):
        mariage_present=list_mariage[i]
        for cp in mariage_present:
            if cp in mariage_avant:
                val+=0
            else:
                val+=1
        mariage_avant=mariage_present
    return val

def algo_2(list_instance):

    mariage=[]
    for i in range(len(list_instance)):
        male_i,female_i,pm_i, pf_i=list_instance[i]
        mariage.append(Gale_Shapley(female_i,male_i,pf_i,pm_i))
    return mariage

def algo_1(list_instance):
    mariage=[]
    for i in range(len(list_instance)):
        male_i,female_i,pm_i, pf_i=list_instance[i]
        mariage.append(Gale_Shapley(male_i,female_i,pm_i,pf_i))
    return mariage


def algo_3(list_instance):
    return prog_lineaire(list_instance)
import sys

def lire_entree(file):

    s_f=dict()
    s_m=dict()
    print("=================================")
    print("Lire les donees depuis un fichier")
    print("=================================")
    f = open(file, "r")
    nbmale=int((f.readline()).rstrip('\n'))
    nbfemale=int((f.readline()).rstrip('\n'))
    print(nbmale,nbfemale)
    for i in range(nbmale):
        line=(f.readline()).rstrip('\n').split(",")
        print(line,"here")
        #print(male_name)
        s_m[line[0]]=["Single",[]]
        for j in range(1,len(line)):
            s_m[line[0]][1].append(line[j])
    for i in range(nbfemale):
        line=(f.readline()).rstrip('\n').split(",")
        s_f[line[0]]=["Single",[]]
        for j in range(1,len(line)):
            s_f[line[0]][1].append(line[j])
    """else:
        print("L'utilisation :")
        print("1) lire les donnees depuis terminale")
        print("2) lire les donnees depuis un fichier")
        print("Veuillez reessayer")
        exit(1)"""
    return s_m,s_f

from copy import deepcopy

def choix_algo(K,S, male, female, s_m, s_f):
    ins=genere_instance(K,S, male, female, s_m, s_f)
    best_algo=-1
    best_val=np.inf


    import sys
    save_stdout = sys.stdout
    sys.stdout = open('trash', 'w')
    res1=algo_1(deepcopy(ins))
    res2=algo_2(deepcopy(ins))
    val1=calcul_difference_entre_gen(res1)
    val2=calcul_difference_entre_gen(res2)

    sys.stdout = save_stdout
    val3=calcul_difference_entre_gen(algo_3(deepcopy(ins)))
    val4=prog_lineaire_advance(deepcopy(ins))
    best_algo=np.argmin([val1,val2,val3,val4])+1
    best_val=np.min([val1,val2,val3,val4])
    print([val1,val2,val3,val4])
    print("best algo is : algo",best_algo)
    print("best value is : ",best_val)

    #print(res1,"\n",res2)



random.seed(30)
"""read from file"""
#s_m,s_f=lire_entree("donne.csv")
#print(s_m,s_f)
"""test"""
female,male,s_f,s_m=gennere_set_f_m(7,7)
#print(female, male)
#genere_pref_dyn(5,3)
#res=Gale_Shapley(female,male,s_f,s_m)
#print(res)
K=[1,3,2,5,5,6,4,2,5]
S=[1,2,7,6,5,3,2,3,7]
#K=[7,7,7,7,7,7,7]
#S=[1,2,3,4,5,6,7]
#print(genere_instance(K,S, male, female, s_m, s_f))
#choix_algo(K,S, male, female, s_m, s_f)
#r=gennere_set_f_m(5)
#print(r)
#res=Gale_Shapley(female,male,s_f,s_m)
#print(res,"\n")
#print(s_m)
