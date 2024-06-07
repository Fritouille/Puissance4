Plateau=list[list[str]]
PR:str="R"
PJ:str="J"

def initPlateau(): #Renvoie le plateau de jeu 7x6 vide
    res:Plateau=[]
    for li in range(6):
        newli:list[str]=[]
        for col in range(7):
            newli.append(" ")
        res.append(newli)
    return res

def Case_est_vide(p:Plateau,li:int,col:int): #Renvoie True si une case est vide sinon False
    if (p[li][col]==" "):
        return True
    else:
        return False

def Colonne_pleine(p:Plateau,col:int): #Renvoie True si la colonne est pleine sinon False
    if(Case_est_vide(p,0,col)==True):
        return False
    return True

def JouerPJ(p:Plateau,col:int): #Renvoie True si la piece Jaune a etait joue correctement dans la colonne sinon False
    if(Colonne_pleine(p,col)==False and col>=0 and col<=6):
        for i in range(1,7):
            if(Case_est_vide(p,-i,col)==True):
                p[-i][col]=PJ
                return True
    else:
        return False

def JouerPR(p:Plateau,col:int): #Renvoie True si la piece Rouge a etait joue correctement dans la colonne sinon False
    if(Colonne_pleine(p,col)==False and col>=0 and col<=6):
        for i in range(1,7):
            if(Case_est_vide(p,-i,col)==True):
                p[-i][col]=PR
                return True
    else:
        return False
        
def Afficher(p:Plateau): #Affiche le plateau de jeu
    li:int=0
    col:int
    res:str="|"+"-"*27+"|\n"
    sep:int=1
    while li<6:
        res+="|"
        if sep%2==0:
            res+="-"*27+"|"
            sep+=1
        else:
            for col in range(7):
                res+=" "+str(p[li][col])+" |"
                sep+=1
            li+=1
        res+="\n"
    res+="|"+"-"*27+"|\n"
    return res

def Gagner(p:Plateau): #Renvoie la couleur gagnante si une couleur gagne sinon None
    li:int
    col:int
    for li in range(3): #test verticalement
        for col in range(7):
            if(p[li][col] == p[li+1][col] == p[li+2][col] == p[li-3][col] and (p[li][col]==PR or p[li][col]==PJ)): 
                return p[li][col]
            
    for li in range(6): #test horizontalement
        for col in range(4):
             if(p[li][col] == p[li][col+1] == p[li][col+2] == p[li][col+3]and (p[li][col]==PR or p[li][col]==PJ)): 
                return p[li][col]
             
    for li in range(3): #diagonale haut gauche vers bas droite
        for col in range(4): 
            if(p[li][col] == p[li+1][col+1] == p[li+2][col+2] == p[li+3][col+3]and (p[li][col]==PR or p[li][col]==PJ)): 
                return p[li][col]
            
    for li in range(3,6): #diagonale bas gauche vers haut droite
        for col in range(4): 
            if(p[li][col] == p[li-1][col+1] == p[li-2][col+2] == p[li-3][col+3]and (p[li][col]==PR or p[li][col]==PJ)): 
                return p[li][col]
    return None

def Annuler(p:Plateau,Lastcol:int): #Renvoie True si la derniere piece a bien etait annule sinon False
    for i in range(6):
        if(Case_est_vide(p,i,Lastcol)==False):
            p[i][Lastcol]=" "
            return True
    else:
        return False

def Sauvegarder(file:str,p:Plateau): #Sauvegarde la partie en cours dans un fichier
    f=open(file,"w")
    f.write(Afficher(p))
    f.close()
    return None
	
def Charger(file:str): #Renvoie la partie sauvegarde, on suppose que le fichier existe deja
    f=open(file,"r")
    p:Plateau=[str(ligne.strip()) for ligne in f]
    i:int
    j:int
    Ltmp:list[str]=[]
    Lres:list[list[str]]=[]
    for i in range(1,12,2):
        for j in range(2,29,4):
            Ltmp.append(p[i][j])
        #print("Ltmp :\n")
        #print(Ltmp)
        Lres.append(Ltmp)
        Ltmp=[]
    f.close()
    return Lres

def P4(): #Demarre le jeu 
    nomPR:str=input("Le nom du joueur rouge : ")
    nomPJ:str=input("Le nom du joueur jaune : ")
    manche:int=int(input("Le nombre de manche gagnantes : "))
    vicPR:int=0
    vicPJ:int=0
    coup_jouer:int
    p:Plateau=initPlateau()
    choix_joueur:str
    load:str=input("Avez vous une sauvegarde, si oui taper le nom du fichier avec extension sinon taper n : ")
    save:str=""

    if(load!="n"): #On suppose que le fichier existe
        p=Charger(load)

    while(vicPR<manche and vicPJ<manche): #Le nombre de manche pour gagner
        coup_jouer=0
        if((vicPJ+vicPR)%2==0): #Alternance des joueurs au debut
            choix_joueur=nomPR
        else:
            choix_joueur=nomPJ
            
        while(coup_jouer<42): #Le max de coup possible
            print(Afficher(p))
            colonne_jouer=int(input("Le joueur "+choix_joueur+" doit choisir une colonne entre 1 a 7 ou 0 pour sauvegarder et quitter: "))-1

            if(colonne_jouer==-1):
                save=input("Taper un nom de fichier avec extension : ") #Sauvegarder la partie
                Sauvegarder(save,p)
                print("La partie se sauvegarde ainsi \n"+Afficher(p))
                return None

            if(choix_joueur==nomPJ): #Le joueur Jaune joue

                if(JouerPJ(p,colonne_jouer)==False): #Joue la piece si la colonne est possible sinon choisir une autre
                    print("Colonne pleine, choisir une autre colonne")
                    continue
                coup_jouer+=1
                annuler:str=input("Voulez vous annuler le coup (Repondre y/n) : ")

                if(annuler=="y"): #Annule le coup jouer
                    Annuler(p,colonne_jouer)
                    coup_jouer-=1
                    continue

            else: #Le joueur Rouge joue

                if(JouerPR(p,colonne_jouer)==False): #Joue la piece si la colonne est possible sinon choisir une autre
                    print("Colonne pleine, choisir une autre colonne")
                    continue
            
                coup_jouer+=1
                annuler:str=input("Voulez vous annuler le coup (Repondre y/n) : ")

                if(annuler=="y"): #Annule le coup jouer
                    Annuler(p,colonne_jouer)
                    coup_jouer-=1
                    continue

            if(Gagner(p)!=None): #Si quelqu'un gagne on arrete de jouer
                break
        
            if(choix_joueur==nomPR): #Changement de joueur a chaque tour
                choix_joueur=nomPJ 
            else:
                choix_joueur=nomPR
        
        if(save==""): #Si on ne veut pas sauvegarder
            if(Gagner(p)==PJ): #Victoire du joueur Jaune
                print(Afficher(p))
                print("Le joueur "+str(nomPJ)+" gagne cette manche")
                vicPJ+=1

            elif(Gagner(p)==PR): #Victoire du joueur Rouge
                print(Afficher(p))
                print("Le joueur "+str(nomPR)+" gagne cette manche")
                vicPR+=1

            else: #Match nul
                print(Afficher(p))
                print("Match nul")
            p=initPlateau()

        print("Le score est de "+nomPR+" : "+str(vicPR)+" et "+nomPJ+" : "+str(vicPJ))
    
    if(vicPJ==manche): #Victoire final
        print("Le joueur "+nomPJ+" a gagne la partie")
    else:
        print("Le joueur "+nomPR+" a gagne la partie")
    return None

P4() #enlever le commentaire et lancer le script
