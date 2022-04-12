from gurobipy import *
from gs import Gale_Shapley

def prog_lineaire(list_instance):
    """
    :param :list_instance : list of qua-tuplets contaning
        - male_i/female_i : list of males/females for t=i
        - pm_i/pf_i : dictionary of preference for t=i
    Principe de l'algo:
    #Methode: PL
    #Variable:
        - x_{ij}^{t} -> variable xij a l'instant t
    #Valeur de variable:
        - 1 si xij forme une couple a l'instant t
        - 0 sinon
    #Fonction objective:
        Max save all couples
    #Contraintes:
        - pour tout t, sum xij sur i ou j soit inf a 1 (mariage)
        - xijt>=0
        - xijt<=1
        - for all t sum xij should be == to min(nbmale, nbfemale)

    :return : list of couples of different generations
    """
    mariage=[]
    male_i,female_i,pm_i, pf_i=list_instance[0]

    # The first generation is genarated by Gale_Shapley
    mariage_avant=Gale_Shapley(male_i,female_i,pm_i,pf_i)
    mariage.append(mariage_avant)

    nb_opt=len(male_i)
    nb_des=len(female_i)


    # Creation la liste de preference
    for nb in range(1,len(list_instance)):
        list_pref_cote_opt=[]
        list_pref_cote_des=[]
        male_i,female_i,pm_i, pf_i=list_instance[nb]

        nb_opt=len(male_i)
        nb_des=len(female_i)
        pref_cote_opt=pm_i
        pref_cote_des=pf_i
        cote_optimal=male_i
        cote_dessimale=female_i

        vecteur_mariage=[]

        #Generate vecteur_mariage
        for j in range(len(male_i)):
            for k in range(len(female_i)):
                if (male_i[j],female_i[k]) in mariage_avant:
                    print(male_i[j],female_i[k])
                    vecteur_mariage.append(1)
                else:
                    vecteur_mariage.append(0)

        nbvar=len(male_i)*len(female_i)#nb_opt*nb_des
        #1. somme sur j, xij<=1 un homme au plus une femme
        #2. somme sur i, xij<=1 une femme au plus un homme
        #3. stabilite
        #4. xij egal a zero ou 1 (deux contraintes par variable)
        nbcont = nb_des+nb_opt + nbvar*2+2

        c=vecteur_mariage

        lignes = range(nbcont)
        colonnes = range(nbvar)
        m = Model("mogplex")

        # declaration variables de decision
        x = []
        for i in colonnes:
            x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d" % (i+1)))

        m.update()

        obj = LinExpr();
        obj =0

        for j in colonnes:
            obj += c[j] * x[j]

        # definition de l'objectif
        m.setObjective(obj,GRB.MAXIMIZE)

        for i in range(nb_opt):
            print("size",nb_opt)
            m.addConstr(quicksum(x[j] for j in [y+nb_des*i for y in range(nb_des)]) <= 1, "Contrainte%d" % i)
        for i in range(nb_des):
            m.addConstr(quicksum(x[j] for j in [y*nb_des+i for y in range(nb_opt)]) <= 1, "Contrainte%d" % i)
        for i in range(nbvar):
            m.addConstr(x[i]  >= 0, "Contrainte%d" % i)
            m.addConstr(x[i]  <= 1, "Contrainte%d" % i)
        # maj du modele pour integrer les nouvelles variables
        valmin=min(len(male_i),len(female_i))
        m.addConstr(quicksum(x[j]  for j in [ y for y in range(nbvar)] ) <=valmin, "Contrainte%d" % i)
        m.addConstr(quicksum(x[j]  for j in [ y for y in range(nbvar)] ) >=valmin, "Contrainte%d" % i)
        m.optimize()


        vecteur_mariage=[]
        ma=[]
        #generation of ocuples
        for j in colonnes:
            print(j)
            vecteur_mariage.append(x[j].x)
            if x[j].x==1:
                index_homme=(j)//len(cote_dessimale)
                index_femme=j-index_homme*len(cote_dessimale)
                ma.append( (cote_optimal[index_homme],cote_dessimale[index_femme]) )


        mariage_avant=ma
        mariage.append(ma)
        #print('Valeur de la fonction objectif :', m.objVal)
    return mariage
