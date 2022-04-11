# projet_androide_sm

**L’introduction**

Le problème des mariages stables est au cœur de nombreuses procédures d'affectation, la plus connue en France étant probablement ParcourSup. Il y a dans ce problème deux types de joueurs (hommes/femmes, candidat(e)s/universités, ...), chaque joueur d'un type donnant ses préférences sur les joueurs de l'autre type (les universités classent les candidat(e)s par exemple). Le but est de trouver une affectation/un couplage vérifiant une propriété de stabilité.
L'algorithme le plus connu pour trouver une telle affectation est l'algorithme de Gale-Shapley. Nous nous intéressons dans ce projet non seulement coder les solutions en algorithme de Gale-Shapley et programmation linéaire, mais aussi étudier ce problème dans une situation dynamique : à chaque pas de temps nous réinitialise le nombre de l’homme et femme et on va trouvé une algorithme qui minimiser le changement de couples. 

**Different algorithmes used**
- Gale-shapley (algo 1,2)
- Iteratif linear programmation
- Global linear programmation
    
**Description of files**
- name_female.json, name_femal.json / csv : data of humans' name
- get_csv.py : turn files from json to csv
- gs.py : principal code of algorithmes Gale-shapley
- sm.py : principal file contains functions:
    - gennere_set_f_m
    - genere_pref_dyn
    - genere_instance 
    - calcul_difference_entre_gen
    - algo_1 
    - algo_2
    - lire_entree
    - choix_algo
- moplex.py, moplex_new.py : application of linear programmtion
- algo3.py : contains the function for the Iteratif linear programmation
- algo4.py : contains the function for the Global linear programmation
