# Puissance 4 interface graphique
import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog


Plateau=list[list[str]]
PR:str="R"
PJ:str="J"
p:Plateau
coup_jouer:int #Nombre total de coup jouÃ©s
vicPR:int=0 #Nombre de victoire du joueur R
vicPJ:int=0 #Nombre de victoire du joueur J

# Moteur
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

def sauvegarderPartie(p):
    fichierDeSauvegarde = filedialog.asksaveasfilename(parent=root, title="Sauvez la manche sous...") 
    f = open(fichierDeSauvegarde,'w')
    f.write(Afficher(p))
    f.close()
    showinfo(title="Manche Sauvegarder", message="La manche est sauvegarder dans le fichier : "+fichierDeSauvegarde)
    return None               

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

def JouerPossible(p:Plateau,col:int,pointjoue,ligne): #Renvoie True si la piece Jaune a etait joue correctement dans la colonne sinon False
    if(Colonne_pleine(p,col)==False and col>=0 and col<=6):
        for i in range(1,7):
            if(Case_est_vide(p,-i,col)==True):
                p[-i][col]=pointjoue
                ligne=i
                return ligne
    else:
        return 0

def Gagner(p:Plateau): #Renvoie la couleur gagnante si une couleur gagne sinon None
    li:int
    col:int
    for li in range(3): #test verticalement
        for col in range(7):
            if(p[li][col] == p[li+1][col] == p[li+2][col] == p[li+3][col] and (p[li][col]==PR or p[li][col]==PJ)): 
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

# Interface graphique
def chargerJeu () : #pour charger le jeu a partir du nfichier
    global p
    win = Toplevel(root)
    filetypes = (("text files", "*.txt"),("All files", "*.*"))
    file_name = filedialog.askopenfilename(initialdir = "/",title = "Selectionnez le fichier",filetypes = filetypes)
    f=open(file_name,"r")
    p=[str(ligne.strip()) for ligne in f]
    i:int
    j:int
    Ltmp:list[str]=[]
    Lres:list[list[str]]=[]
    for i in range(1,12,2):
        for j in range(2,29,4):
            Ltmp.append(p[i][j])
        Lres.append(Ltmp)
        Ltmp=[]
    f.close()
    p=Lres
    plateauDeJeu (False)

def lancerMenu () : 
    
    frame = Frame(root, bg='darkblue', bd=1, relief=SUNKEN) 

    label_title= Label(frame, text="Puissance 4", font=("arial" , 40), bg='darkblue' , fg='red') 
    label_title.pack() 

    label_subtitle= Label(frame, text="jouer une partie des puissance 4", font=("darkblue" , 20), bg='darkblue' , fg='red')
    label_subtitle.pack()

    # ajouter les boutons
    jouer_button= Button(frame, text="lancer une partie", font=("arial" , 15), bg='red' , fg='darkblue', command=lambda: [frame.destroy(),lancerJeu()])
    jouer_button.pack(pady=25) 

    continuer_button= Button(frame, text="continuer une partie", font=("arial" , 15), bg='red' , fg='darkblue', command=lambda: [frame.destroy(),chargerJeu()])
    jouer_button.pack(pady=25) 
    continuer_button.pack(pady=25) 

    quitter_button= Button(frame, text="quitter", font=("arial" , 15), bg='red' , fg='darkblue', command=quit)
    quitter_button.pack(pady=25)
    
    frame.pack(expand=YES)

def vider_frame():
    for element in frame.winfo_children():
        element.pack_forget() 

def jouer (canvas,quitter_button,couleur_joueur, choix_joueur, colonne_jouee): # un joueur joue
    global coup_jouer
    global vicPR
    global vicPJ
    
    # Demande de confirmation pour annuler le coup
    reponse = askokcancel("jouer", "Etes vous sÃ»r de vouloir jouer colonne "+colonne_jouee.get())
    if reponse:
        # La reponse est confirmee
        coup_jouer+=1
        ligne = 1
        pointJoue="J"
        if couleur_joueur == 'red' :
                pointJoue="R"
        colonne = int(colonne_jouee.get())-1
        ligne = JouerPossible(p,colonne,pointJoue,ligne)
        if ligne > 0:
            ajouterJeton(canvas,colonne,6-ligne,couleur_joueur)
            if(Gagner(p)==PJ): #Victoire du joueur Jaune
                vicPJ+=1
                showinfo(title="Manche Gagne", message="Le joueur jaune a  gagne la manche("+str(vicPJ)+" victoire(s) / "+str(manche)+")")
                if(vicPJ>=manche): #Victoire final
                    showinfo(title="Partie Gagne", message="Le joueur jaune a gagne la partie")
                    canvas.destroy()
                    quitter_button.destroy()
                    lancerMenu()
                else:
                    canvas.destroy()
                    quitter_button.destroy()
                    plateauDeJeu (True)
                
            elif(Gagner(p)==PR): #Victoire du joueur Rouge             
                vicPR+=1    
                showinfo(title="aAnche Gagne", message="Le joueur rouge a gagne la manche ("+str(vicPR)+" victoire(s)/ "+str(manche)+")")
                if(vicPR>=manche): #Victoire final
                    showinfo(title="Partie Gagne", message="Le joueur rouge a gagne la partie")
                    canvas.destroy()
                    quitter_button.destroy()
                    lancerMenu()
                else:
                    canvas.destroy()
                    quitter_button.destroy()
                    plateauDeJeu (True)

            else: # pas de victoire la manche continue            
                if coup_jouer>=42: #Le max de coup possible 
                    showinfo(title="Manche nulle", message="Egalite : Aucun joueur ne gagne la manche !")             
                    canvas.destroy()
                    quitter_button.destroy()
                    plateauDeJeu (True)
                else:
                    if couleur_joueur == 'red' :
                        couleur_joueur = 'yellow'
                        choix_joueur = nomPJ
                    else : 
                        couleur_joueur = 'red'
                        choix_joueur = nomPR
                proposerJouer(canvas,quitter_button,choix_joueur,couleur_joueur)
        else :
            askretrycancel(message='La colonne est pleine',title='Erreur')

######################################################

def quitterManche(canvas, quitter_button):
    reponse = askokcancel("quitter", "Etes vous sur de vouloir quitter la partie ?")
    if reponse:
        quitter_button.destroy()
        canvas.destroy() 
        lancerMenu()

def proposerJouer(canvas,quitter_button,choix_joueur,couleur_joueur):
    global coup_jouer
    cmd = root.register(lambda s: not s or s.isdigit()) #La valeur saisie doit Ãªtre un entier
    jouer_label = Label(root, text="Le joueur "+choix_joueur+" doit choisir une colonne entre 1 a 7 : ", font=("arial" , 15))
    canvas.create_window(250, 20, window=jouer_label)
    
    colonne_jouer = Entry(root, font=("arial" , 15), validate="key", vcmd=(cmd, "%P"))
    canvas.create_window(500, 20, window=colonne_jouer, width=30)
    
    jouer_button= Button(text='Jouer', font=("arial" , 15), bg=couleur_joueur , fg='darkblue', command=lambda: [jouer(canvas,quitter_button,couleur_joueur,choix_joueur,colonne_jouer)])
    canvas.create_window(570, 20, window=jouer_button)

def remplirPlateau(canvas):
    for ligne in range(6):
        for colonne in range(7):                
            if p[ligne][colonne]=='R':
                ajouterJeton(canvas,colonne,ligne,'red')
            elif p[ligne][colonne]=='J':
                ajouterJeton(canvas,colonne,ligne,'yellow')
            else:
                ajouterJeton(canvas,colonne,ligne,'white')

def plateauDeJeu (vide):
    
    global coup_jouer
    global p
    global vicPR
    global vicPJ
    
    choix_joueur:str #Joueur qui doit jouer

    canvas = Canvas(root, width=800, height=600)
    canvas.pack()
    a = canvas.create_rectangle(100, 40, 700, 600, fill='blue')

    if vide:
        p = initPlateau()
        # Affichage du plateau vide
        for colonne in range(7):
            for ligne in range(6):
                ajouterJeton(canvas,colonne,ligne,'white')
    else:
        remplirPlateau(canvas)
    
    
    # Boutons 
    quitter_button= Button(root, text="Quitter la manche", font=("arial" , 15), bg='red' , fg='darkblue', command=lambda: [quitterManche (canvas, quitter_button)])
    quitter_button.pack()
    sauvegarder_button= Button(root, text="Sauvegarder la manche", font=("arial" , 15), bg='red' , fg='darkblue', command=lambda: [sauvegarderPartie(p)])
    sauvegarder_button.pack()

    choix_joueur = nomPR
    couleur_joueur = 'red'
    
    if((vicPJ+vicPR)%2==0): #Alternance des joueurs au debut
        choix_joueur=nomPR
        couleur_joueur = 'red'
    else:
        choix_joueur=nomPJ
        couleur_joueur = 'yellow'
    coup_jouer=0
    
    proposerJouer(canvas,quitter_button,choix_joueur,couleur_joueur)

######################################################

def ajouterJeton(canvas,colonne, ligne,couleur):
    o = canvas.create_oval(130+colonne*constante,80+ligne*constante,190+colonne*constante,140+ligne*constante, fill=couleur)
    canvas.move(o, 20, 20)

def getNomPR(nomPR_entry,nomPR_button,label_nomPJ):
    global nomPR
    global choixNomR 
    
    nomPR = nomPR_entry.get()
    label_nomPR_Rep= Label(root, text="Joueur rouge = "+nomPR, font=("arial" , 10), bg='darkblue' , fg='white') 
    label_nomPR_Rep.pack() 
    nomPR_entry.destroy()
    nomPR_button.destroy()
    label_nomPJ.destroy()   
    choixNomR = True
    if choixNomR and choixNomJ and choixManche :
        plateauDeJeu (True)
    
def getNomPJ(nomPJ_entry,nomPJ_button,label_nomPJ):
    global nomPJ
    global choixNomJ 

    nomPJ = nomPJ_entry.get()
    label_nomPJ_Rep= Label(root, text="Joueur jaune = "+nomPJ, font=("arial" , 10), bg='darkblue' , fg='white') 
    label_nomPJ_Rep.pack() 
    nomPJ_entry.destroy()
    nomPJ_button.destroy()
    label_nomPJ.destroy()
    choixNomJ = True
    if choixNomR and choixNomJ and choixManche :
        plateauDeJeu (True)

def getManche(manche_entry,manche_button,label_manche):
    global manche 
    global choixManche

    manche = int(manche_entry.get())
    label_manche_Rep= Label(root, text=str(manche)+" Manche(s)", font=("arial" , 10), bg='darkblue' , fg='white') 
    label_manche_Rep.pack()
    manche_entry.destroy()
    manche_button.destroy()
    label_manche.destroy()
    choixManche = True
    if choixNomR and choixNomJ and choixManche :
        plateauDeJeu (True)


def lancerJeu () :
    
    label_nomPR= Label( text="Le nom du joueur rouge :", font=("arial" , 10), bg='darkblue' , fg='white') 
    label_nomPR.pack()
    nomPR_entry = Entry(root, width=40)
    nomPR_entry.pack(pady=20)
    nomPR_button = Button(root, height=1, width=30, text="Lire le nom du joueur rouge", command=lambda: [getNomPR(nomPR_entry,nomPR_button,label_nomPR)])
    nomPR_button.pack()
    
    label_nomPJ= Label( text="Le nom du joueur jaune :", font=("arial" , 10), bg='darkblue' , fg='white') 
    label_nomPJ.pack()
    nomPJ_entry = Entry(root, width=40)
    nomPJ_entry.pack(pady=20)
    nomPJ_button = Button(root, height=1, width=30, text="Lire le nom du joueur jaune", command=lambda: [getNomPJ(nomPJ_entry,nomPJ_button,label_nomPJ)])
    nomPJ_button.pack()
    
    label_manche= Label( text="Le nombre de manches gagnantes : ", font=("arial" , 10), bg='darkblue' , fg='white') 
    label_manche.pack()
    manche_entry = Entry(root, width=40)
    manche_entry.pack(pady=20)
    manche_button = Button(root, text="Lire le nombre de manche", font=("arial" , 15), command=lambda: [getManche(manche_entry,manche_button,label_manche)])
    manche_button.pack()

# 

root = Tk() 
constante = 80

# personnaliser la fenÃªtre 
root.title("Interface graphique puissance 4") 
root.geometry("1080x720") 
root.config(background='darkblue') 

canvas = Canvas()
frame = Frame()

label_nom= Label( text="Fait par Luc", font=("arial" , 10), bg='darkblue' , fg='white') 
label_nom.pack()

nomPR = "Rouge"
choixNomR = False
nomPJ = "Jaune"
choixNomJ = False
manche:int = 1
choixManche = False

lancerMenu()

root.mainloop()
