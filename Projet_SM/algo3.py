from gurobipy import *
from gs import Gale_Shapley

NB_M=7
NB_F=7
def prog_lineaire(list_instance):
    #female,male,s_f,s_m=gennere_set_f_m(5,6)
    #cote_optimal=male
    #pref_cote_opt=s_m
    #cote_dessimale=female
    #pref_cote_des=s_f
    print("**********")
    print(list_instance)
    print("**********")
    mariage=[]
    male_i,female_i,pm_i, pf_i=list_instance[0]

    #print(pm_i)
    mariage_avant=Gale_Shapley(male_i,female_i,pm_i,pf_i)
    print(mariage_avant)
    mariage.append(mariage_avant)

    nb_opt=len(male_i)
    nb_des=len(female_i)


    # Creation la liste de preference
    for nb in range(1,len(list_instance)):
        print("!!!!!!!",nb,"!!!!!!!!!!")
        print(mariage_avant)
        list_pref_cote_opt=[]
        list_pref_cote_des=[]
        male_i,female_i,pm_i, pf_i=list_instance[nb]

        nb_opt=len(male_i)
        nb_des=len(female_i)
        pref_cote_opt=pm_i
        pref_cote_des=pf_i
        cote_optimal=male_i
        cote_dessimale=female_i
        #if nb==1:
        vecteur_mariage=[]
        for j in range(len(male_i)):
            for k in range(len(female_i)):
                if (male_i[j],female_i[k]) in mariage_avant:
                    print(male_i[j],female_i[k])
                    vecteur_mariage.append(1)
                else:
                    vecteur_mariage.append(0)
        print(mariage_avant)
        print(male_i,female_i)
        print(vecteur_mariage)

        nbvar=len(male_i)*len(female_i)#nb_opt*nb_des
        print(nbvar)
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
            #print("!!!!!!!!count")
            #print(i)
            #print("!!!!!!!!count!!!!")
            x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d" % (i+1)))

        m.update()

        obj = LinExpr();
        obj =0
        #print(nb_opt, nb_des)
        #print(len(c),len(x))
        for j in colonnes:
            #print(colonnes,len(c))
            #print(nbvar)
            obj += c[j] * x[j]

        # definition de l'objectif
        m.setObjective(obj,GRB.MAXIMIZE)

        for i in range(nb_opt):
            print("size",nb_opt)
            #print([y+nb_des*i for y in range(nb_des)])
            m.addConstr(quicksum(x[j] for j in [y+nb_des*i for y in range(nb_des)]) <= 1, "Contrainte%d" % i)
        for i in range(nb_des):
            #print([y*nb_des+i for y in range(nb_opt)])
            m.addConstr(quicksum(x[j] for j in [y*nb_des+i for y in range(nb_opt)]) <= 1, "Contrainte%d" % i)
        for i in range(nbvar):
            m.addConstr(x[i]  >= 0, "Contrainte%d" % i)
            m.addConstr(x[i]  <= 1, "Contrainte%d" % i)
        # maj du modele pour integrer les nouvelles variables
        valmin=min(len(male_i),len(female_i))
        m.addConstr(quicksum(x[j]  for j in [ y for y in range(nbvar)] ) <=valmin, "Contrainte%d" % i)
        m.addConstr(quicksum(x[j]  for j in [ y for y in range(nbvar)] ) >=valmin, "Contrainte%d" % i)
        m.optimize()


        #print("")
        #print('Solution optimale:')
        vecteur_mariage=[]
        ma=[]
        for j in colonnes:
            print(j)
            vecteur_mariage.append(x[j].x)
            if x[j].x==1:

                index_homme=(j)//len(cote_dessimale)
                index_femme=j-index_homme*len(cote_dessimale)
                print(j,cote_optimal[index_homme],cote_dessimale[index_femme])
                ma.append( (cote_optimal[index_homme],cote_dessimale[index_femme]) )
            #print('x%d'%(j+1), '=', x[j].x)
        print("here")
        print(cote_optimal,cote_dessimale)
        print(vecteur_mariage)
        mariage_avant=ma
        print(ma)
        mariage.append(ma)
        #mariage_avant=vecteur_mariage
        #print("")
        #print('Valeur de la fonction objectif :', m.objVal)
    return mariage
