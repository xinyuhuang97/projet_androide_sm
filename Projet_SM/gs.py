def Gale_Shapley(female,male,pref_f,pref_m,optimal=0):
    """
    Gale Shapley algorithm to resolve stable mariage problem
    :param female : a liste containning name of females
    :param female : a liste containning name of males
    :param pref_f : a dictionnary with format {name_female :["Single",y],....}, where y represent her preference towards males
    :param pref_m : a dictionnary with format {name_male :["Single",y],....}, where y represent his preference towards females
    :param optimal : by defaut, algo is female-optimal, and it will change to male-optimal by specifying optimal=1

    return : a list of name of couples [(optimal, dessimale)]
    """

    # choose which side to optimize
    if optimal==0:
        side_opt=female.copy()
        pref_opt=pref_f
        side_des=male.copy()
        pref_des=pref_m
    else:
        side_opt=male.copy()
        pref_opt=pref_m
        side_des=female.copy()
        pref_des=pref_f

    # The algos continue while it exists single people on the optimal side
    while side_opt:
        person=side_opt.pop()
        for person_partner in (pref_opt[person][1]):
            # when the partner is single, we form directely a couple
            if pref_des[person_partner][0]=="Single":
                pref_opt[person][0]=person_partner
                pref_des[person_partner][0]=person
                pref_opt[person][0]=person_partner
                break
            # when the partner is not single, we will compare with the competitor in the list of prefernce of partner
            else:
                competitor=pref_des[person_partner][0]
                pref_comp=pref_des[person_partner][1].index(competitor)
                pref_person=pref_des[person_partner][1].index(person)
                if pref_person<pref_comp:
                    pref_des[person_partner][0]=person
                    pref_opt[person][0]=person_partner
                    pref_opt[competitor][0]="Single"
                    side_opt.append(competitor)
                    break
            #print(pref_opt,"\n")
            #print(pref_des,"\n")
    return [(x, y[0])  for x,y in pref_opt.items() if y[0]!='Single']
