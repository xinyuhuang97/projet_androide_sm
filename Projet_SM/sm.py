import sys
import random
import pandas as pd
import numpy as np
from algo3 import *
from algo4 import *
from copy import deepcopy

# Get liste of male/female name
name_male=list(pd.read_csv('./name_male.csv')['Name'].unique())
name_female=list(pd.read_csv('./name_female.csv')['Name'].unique())

def gennere_set_f_m(dim1,dim2=0):
    """
    Function to generate the data struture of the problem studied
    int*(int)->list(str)*list(str)*dict*dict
    :param dim1: number of males for our study
    :param dim2(optional): number of males for our study

    :return female: list of name of males
    :return male: list of name of males
    :return s_f: a dictionnary with format {name_female :["Single",y],....}, where y represent her preference towards males
    :return s_m: a dictionnary with format {name_male :["Single",y],....}, where y represent his preference towards females
    """
    if dim2==0:
        dim2=dim1
    s_f=dict()
    s_m=dict()
    # Genarate list of males/females
    female=random.sample(name_female, k=dim1)
    male=random.sample(name_male, k=dim2)
    # Two loop to generate two dictionnaries
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
    """
    Function to generate dynamically preference list
    Principe: from the predefine list of preference for male/female
              generate a new list of preference according to name in list of female/male
    list(str)*list(str)*dict*dict - >dict*dict
    :param male: list of name of males
    :param female: list of name of females
    :param pm: the complete preference list for males
    :param pf: the complete preference list for females

    :return dic_male: a new list of preference for males
    :return dic_female: a new list of preference for females
    """
    nbmale=len(male)
    nbmale=len(female)
    dic_male=dict()
    dic_female=dict()
    # two loops to generate two dictionnaries
    for i in male:
        lm=[fm for fm in pm[i][1] if fm in female]
        dic_male[i]=['Single',lm]
    for j in female:
        lf=[ml for ml in pf[j][1] if ml in male]
        dic_female[j]=['Single',lf]
    return dic_male,dic_female


def genere_instance(K, S, male, female, pm, pf):
    """
    Function to generate instance ( list of preference list)
    Principe: from the predefine K and S (list contain number of males and females for each iteartion)
    list(int)*list(int)*list(str)*list(str)*dict*dict - >list((list(male),list(female),dict,dict))

    :param K: list of int -> number of male for each iteration
    :param S: list of int -> number of female for each iteration
    :param male: list of name of males
    :param female: list of name of females
    :param pm: the complete preference list for males
    :param pf: the complete preference list for females

    :return list_instance : list of qua-tuplets contaning
        - male_i/female_i : list of males/females for t=i
        - pm_i/pf_i : dictionary of preference for t=i
    """
    list_instance=[]
    for i in range((len(K))):
        male_i=male[:K[i]]
        female_i=female[:S[i]]
        pm_i, pf_i=genere_pref_dyn(male_i,female_i,pm,pf)
        list_instance.append( (male_i,female_i,pm_i, pf_i))
    return list_instance



def calcul_difference_entre_gen(list_mariage):
    """
    Function to calculate the difference of couples betweens different list of couples for different iterations
    list((male, female))->int
    :param list_mariage: list containing list of tuplet(male, female), couple formed for this iteration

    :return val: value counting difference of couples betweens different list of couples for different iterations
    """
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


def algo_1(list_instance):
    """
    Function using algorithm Gale_Shapley optimizing male side
    :param list_instance : list of qua-tuplets contaning
        - male_i/female_i : list of males/females for t=i
        - pm_i/pf_i : dictionary of preference for t=i

    :return mariage: list containing list of tuplet(male, female), couple formed for this iteration
    """
    mariage=[]
    for i in range(len(list_instance)):
        male_i,female_i,pm_i, pf_i=list_instance[i]
        mariage.append(Gale_Shapley(female_i,male_i,pf_i,pm_i, opt=1))
    return mariage

def algo_2(list_instance):
    """
    Function using algorithm Gale_Shapley optimizing female side
    :param list_instance : list of qua-tuplets contaning
        - male_i/female_i : list of males/females for t=i
        - pm_i/pf_i : dictionary of preference for t=i

    :return mariage: list containing list of tuplet(male, female), couple formed for this iteration
    """
    mariage=[]
    for i in range(len(list_instance)):
        male_i,female_i,pm_i, pf_i=list_instance[i]
        mariage.append(Gale_Shapley(female_i,male_i,pf_i,pm_i))
    return mariage




def algo_3(list_instance):
    """
    Algorithm using iterative linear programmation (cf algo3.py)
    :param list_instance : list of qua-tuplets contaning
        - male_i/female_i : list of males/females for t=i
        - pm_i/pf_i : dictionary of preference for t=i

    :return : list containing list of tuplet(male, female), couple formed for this iteration
    """
    return prog_lineaire(list_instance)
import sys

def lire_entree(file):
    """
    Function to read instance from file
    :param file : name of file

    :return sm/sf: dictionary of preference for male/female
    """
    s_f=dict()
    s_m=dict()
    print("=================================")
    print("Lire les donees depuis un fichier")
    print("=================================")
    f = open(file, "r")
    nbmale=int((f.readline()).rstrip('\n'))
    print(nbmale)
    nbfemale=int((f.readline()).rstrip('\n'))
    male=[]
    female=[]
    for i in range(nbmale):
        line=(f.readline()).rstrip('\n').split(",")
        s_m[line[0]]=["Single",[]]
        male.append(line[0])
        for j in range(1,len(line)):
            s_m[line[0]][1].append(line[j])
    for i in range(nbfemale):
        line=(f.readline()).rstrip('\n').split(",")
        s_f[line[0]]=["Single",[]]
        female.append(line[0])
        for j in range(1,len(line)):
            s_f[line[0]][1].append(line[j])
    return male,female,s_m,s_f


def choix_algo(K,S, male, female, s_m, s_f):

    """
    Function to caululate the values of dynamique stable mariage problem and compare results of differents algorithms
    list(int)*list(int)*list(str)*list(str)*dict*dict -> void

    :param K: list of int -> number of male for each iteration
    :param S: list of int -> number of female for each iteration
    :param male: list of name of males
    :param female: list of name of females
    :param pm: the complete preference list for males
    :param pf: the complete preference list for females
    """
    #Generate instance and variable
    ins=genere_instance(K,S, male, female, s_m, s_f)
    best_algo=-1
    best_val=np.inf

    #calculation for 4 algorithms
    save_stdout = sys.stdout
    sys.stdout = open('trash', 'w')
    res1=algo_1(deepcopy(ins))
    res2=algo_2(deepcopy(ins))
    val1=calcul_difference_entre_gen(res1)
    val2=calcul_difference_entre_gen(res2)
    sys.stdout = save_stdout
    val3=calcul_difference_entre_gen(algo_3(deepcopy(ins)))
    val4=prog_lineaire_advance(deepcopy(ins))

    #choose of best algorithm
    best_algo=np.argmin([val1,val2,val3,val4])+1
    best_val=np.min([val1,val2,val3,val4])
    print([val1,val2,val3,val4])
    print("best algo is : algo",best_algo)
    print("best value is : ",best_val)
