from sm import *

def print_pref(pref):
    for k,v in pref.items():
        print("Personne :",k)
        s='\t'.join(str(p) for p in v[1])
        print(f"Preference : {s}")
def compare(m1, m2):
    if len(m1)!=len(m2):
        return False
    for ele in m2:
        if ele not in m1:
            return False
    return True
random.seed(30)

female,male,s_f,s_m=gennere_set_f_m(3,3)
print("=======pref_female=======")
print_pref(s_f)
print("========pref_male========")
print_pref(s_m)

print("--------------check1--------------")
res1=Gale_Shapley(female,male,s_f,s_m,optimal=1)
print(res1)
check1=[('Lucy','Kiyoko'),('Courtney','Elayne'), ('Deon','Alisha')]
assert(compare(res1,check1))
print("***************work***************")
print("----------------------------------")

female,male,s_f,s_m=gennere_set_f_m(4,3)
print("=======pref_female=======")
print_pref(s_f)
print("========pref_male========")
print_pref(s_m)

print("--------------check2--------------")
res2=Gale_Shapley(female,male,s_f,s_m,optimal=1)
print(res2)
check2=[('Marchello','Kimberlie'),('Alexandre','Antonia'),('Reese','Violetta')]
assert(compare(res2,check2))
print("***************work***************")
print("----------------------------------")

female,male,s_f,s_m=gennere_set_f_m(3,4)
print("=======pref_female=======")
print_pref(s_f)
print("========pref_male========")
print_pref(s_m)

print("--------------check3--------------")
res3=Gale_Shapley(female,male,s_f,s_m,optimal=1)
check3=[('Javier','Blake'),('Cicero','Tatyana'),('Irene','Alicia')]
assert(compare(res3,check3))
print("***************work***************")
print("----------------------------------")


female,male,s_f,s_m=gennere_set_f_m(4,4)
print("=======pref_female=======")
print_pref(s_f)
print("========pref_male========")
print_pref(s_m)

K=[3,3,3]
S=[1,2,3]
print("--------------check4--------------")

ins=genere_instance(K,S, male, female, s_m, s_f)
save_stdout = sys.stdout
sys.stdout = open('trash', 'w')
res4=prog_lineaire(ins)
sys.stdout = save_stdout
#check4=[ [], ]
print(res4)
print("----------------------------------")

print("--------------check5--------------")

ins=genere_instance(K,S, male, female, s_m, s_f)
save_stdout = sys.stdout
sys.stdout = open('trash', 'w')
#res5,val=prog_lineaire_advance(ins)
sys.stdout = save_stdout
check5=[ [], ]
#print(res5)
print("----------------------------------")

K=[i for i in range(100)]
S=[100 for i in range(100)]
#print(len(K),len(S))
ins=genere_instance(K,S, male, female, s_m, s_f)
val=prog_lineaire_advance(ins)
print(val)



"""
1. codes utilisables (commente, readme, facilise pour l'utilisation->interface)
2. test
    n = 4
    homme=max femme=range(1,max)
    1) temps de calcul en fonction de n (courbe temps de calcul)
    2) valeurs des algorithme alg1/alg4 .....
        - moyenne, pire cas, courbe en fonction de n
    3) ALGO4:
        xijt en reel ->relaxation continue

    18 mai/23,24 mai
"""
