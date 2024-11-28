### IMPORTATION DES MODULE ###
from flask import Flask, render_template, request, flash, session, jsonify

app=Flask(__name__)

app.secret_key = 'azerty'  #pour session (pour recuperer id pour enregistrement victoire)

### IMPORTATION BDD ###

import mysql.connector

conn = mysql.connector.connect(
host="localhost",
user="root",                  
password="",                  #a completer
database="mini_jeux",)

### TEST BDD ###

"""
def affichage ():
   cursor = conn.cursor()
   cursor.execute(" SELECT * FROM mini_jeux;")
   result = cursor.fetchall()
   for x in result:
      print(x)

def affichage2 ():
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM mini_jeux WHERE pseudo = 'nino' ;")
   result = cursor.fetchall()
   for x in result:
      print(x)

print("\n\ntest toute la BDD :")
affichage()
print("\n\ntest BDD avec id et mdp :")
affichage2()
print("\n\n")
"""

### PAGE PRINCIPAL SITE ###
@app.route('/')
def index():
   #print(session)
   session.clear()
   #print(session)
   return render_template('choix_jeux.html')


### PAGE PRESENTATION SNAKE ###
@app.route('/popupSnake')
def popupSnake():
   return render_template('popup_snake.html')


### PAGE DIFFICULTE SNAKE ###
@app.route('/snake')
def difficulteSnake():
   return render_template('difficulte_snake.html')


### SNAKE DIFFICULTE 1 ###
@app.route('/1')
def snake1():
   return render_template('1.html')


### SNAKE DIFFICULTE 2 ###
@app.route('/2')
def snake2():
   return render_template('2.html')


### SNAKE DIFFICULTE 3 ###
@app.route('/3')
def snake3():
   return render_template('3.html')


### PAGE PRESENTATION MORPION ###
@app.route('/popupMorpion')
def popupMorpion():
   return render_template('popup_morpion.html')


### PAGE MORPION ###
@app.route('/morpion')
def Morpion():
   return render_template('morpion.html')


### PAGE PRESENTATION PUISSANCE 4  ###
@app.route('/popupPuissance4')
def popupPuissance4():
   return render_template('popup_puissance4.html')


### PAGE PUISSANCE 4  ###
@app.route('/puissance4')
def Puissance4():
   return render_template('puissance4.html')


### CONNEXION / CREATION COMPTE MORPION ### 
@app.route('/morpion',methods=['POST'])
def morpion():
   action = request.form.get('action')       #permet de separer les connexion des creation de compte

   if action == 'co' :

      ### CONNEXION MORPION ###
      id_co_m = request.form['id_co_m']
      mdp_co_m = request.form['mdp_co_m']

      cursor = conn.cursor()
      cursor.execute("""SELECT * FROM mini_jeux WHERE pseudo = %s and mdp = %s;""",(id_co_m, mdp_co_m,))
      compte_ok = cursor.fetchone()

      if compte_ok is not None :
         session['id_co_m'] = id_co_m
         return render_template('morpion.html') 
      else :
         return render_template('erreur_id_ou_mdp.html')


   elif action == 'creation_compte' :

      ### CREATION COMPTE MORPION ###
      id_crea_m = request.form['id_crea_m']
      mdp_crea_m = request.form['mdp_crea_m']

      cursor = conn.cursor()
      cursor.execute("""SELECT * FROM mini_jeux WHERE pseudo = %s ;""",(id_crea_m,))     # verifie si l'id est deja utilise en BDD
      pseudo_deja_utiliser = cursor.fetchone()

      if pseudo_deja_utiliser == None :            # si pas utiliser ajoute l'id et mdp comme nouveau compte en BDD
         session['id_crea_m'] = id_crea_m            
         cursor = conn.cursor()
         cursor.execute("""INSERT INTO mini_jeux(pseudo,mdp,snake_1,snake_2,snake_3,nb_joue_snake,nb_victoire_morpion,nb_joue_morpion, nb_victoire_puissance_4, nb_joue_puissance_4) VALUES (%s,%s,0,0,0,0,0,0,0,0); """,(id_crea_m, mdp_crea_m,))
         conn.commit()
         return render_template('morpion.html')    
      else :                                       # sinon refuse car pas possible que plusieurs compte est le meme id
         return render_template('erreur_id_utilise.html')
   

### CONNEXION / CREATION COMPTE SNAKE ### 
@app.route('/snake',methods=['POST'])
def snake():
   action = request.form.get('action')       #permet de separer les connexion des creation de compte

   if action == 'co' :

      ### CONNEXION SNAKE ###
      id_co_s = request.form['id_co_s']
      mdp_co_s = request.form['mdp_co_s']

      cursor = conn.cursor()
      cursor.execute("""SELECT * FROM mini_jeux WHERE pseudo = %s and mdp = %s;""",(id_co_s, mdp_co_s,))
      compte_ok = cursor.fetchone()

      if compte_ok is not None :
         session['id_co_s'] = id_co_s
         return render_template('difficulte_snake.html')
      else :
         return render_template('erreur_id_ou_mdp2.html')


   elif action == 'creation_compte' :

      ### CREATION COMPTE SNAKE ###
      id_crea_s = request.form['id_crea_s']
      mdp_crea_s = request.form['mdp_crea_s']

      cursor = conn.cursor()
      cursor.execute("""SELECT * FROM mini_jeux WHERE pseudo = %s ;""",(id_crea_s,))     # verifie si l'id est deja utilise en BDD
      pseudo_deja_utiliser = cursor.fetchone()

      if pseudo_deja_utiliser == None :            # si pas utiliser ajoute l'id et mdp comme nouveau compte en BDD
         cursor = conn.cursor()
         cursor.execute("""INSERT INTO mini_jeux(pseudo,mdp,snake_1,snake_2,snake_3,nb_joue_snake,nb_victoire_morpion,nb_joue_morpion, nb_victoire_puissance_4, nb_joue_puissance_4) VALUES (%s,%s,0,0,0,0,0,0,0,0); """,(id_crea_s, mdp_crea_s,))
         conn.commit()
         session['id_crea_s'] = id_crea_s
         return render_template('difficulte_snake.html')    
      else :                                       # sinon refuse car pas possible que plusieurs compte est le meme id
         return render_template('erreur_id_utilise2.html')

### CONNEXION / CREATION COMPTE PUISSANCE 4 ### 
@app.route('/puissance4',methods=['POST'])
def puissance4():
   action = request.form.get('action')       #permet de separer les connexion des creation de compte

   if action == 'co' :

      ### CONNEXION PUISSANCE 4 ###
      id_co_p4 = request.form['id_co_p4']
      mdp_co_p4 = request.form['mdp_co_p4']

      cursor = conn.cursor()
      cursor.execute("""SELECT * FROM mini_jeux WHERE pseudo = %s and mdp = %s;""",(id_co_p4, mdp_co_p4,))
      compte_ok = cursor.fetchone()

      if compte_ok is not None :
         session['id_co_p4'] = id_co_p4
         return render_template('puissance4.html') 
      else :
         return render_template('erreur_id_ou_mdp.html')


   elif action == 'creation_compte' :

      ### CREATION COMPTE PUISSANCE 4 ###
      id_crea_p4 = request.form['id_crea_p4']
      mdp_crea_p4 = request.form['mdp_crea_p4']

      cursor = conn.cursor()
      cursor.execute("""SELECT * FROM mini_jeux WHERE pseudo = %s ;""",(id_crea_p4,))     # verifie si l'id est deja utilise en BDD
      pseudo_deja_utiliser = cursor.fetchone()

      if pseudo_deja_utiliser == None :            # si pas utiliser ajoute l'id et mdp comme nouveau compte en BDD
         session['id_crea_p4'] = id_crea_p4           
         cursor = conn.cursor()
         cursor.execute("""INSERT INTO mini_jeux(pseudo,mdp,snake_1,snake_2,snake_3,nb_joue_snake,nb_victoire_morpion,nb_joue_morpion, nb_victoire_puissance_4, nb_joue_puissance_4) VALUES (%s,%s,0,0,0,0,0,0,0,0); """,(id_crea_p4, mdp_crea_p4,))
         conn.commit()
         return render_template('puissance4.html')    
      else :                                       # sinon refuse car pas possible que plusieurs compte est le meme id
         return render_template('erreur_id_utilise.html')


### ENREGISTREMENT VICTOIRE MORPION ###
@app.route('/enregistrer_gagnant', methods=['POST'])
def enregistrer_gagnant():
   #print(session)
   id_m = None
   if 'id_co_m' in session:      #verifie si id_co_m est dans la session. si oui la stock dans une nouvelle varaible
      #print('enregistre en connexion m')
      id_m = session['id_co_m']

   elif 'id_crea_m' in session:  #verifie sinon si la variable id_crea_m dans la session et la stock dans la nouvelle varaible
      #print('enregistre par crea compte m')
      id_m = session['id_crea_m']

   else :                        # si aucune des 2 var est dans la session
      print('erreur enregistrement morpion')

   victoire = request.json                    #recupere les donnee JSON dans la var victoire
   gagnant = victoire.get('gagnant', '')      #recupere la valeur dont la cle est gagnant et la mes dans la var gagnant 

   ### POUR VERIFIER SI PAS ERREUR ###
   
   #print("id_m :", id_m) 
   #print(f"Le joueur gagnant est : {gagnant}")


   cursor = conn.cursor()  
   cursor.execute(""" UPDATE mini_jeux SET nb_joue_morpion = nb_joue_morpion + 1 WHERE pseudo = %s ; """,(id_m,))      #ajoute 1 au nb de partie jouer
   conn.commit()

   if gagnant == "X" :  #si gagne fait +1 en nb victoire (toujours les X pour le joueur)
      #print('victoire')
      cursor = conn.cursor()
      cursor.execute(""" UPDATE mini_jeux SET nb_victoire_morpion = nb_victoire_morpion + 1 WHERE pseudo = %s ; """,(id_m,))
      conn.commit()
   else :
      print('perdu')

   return render_template("morpion.html") 


### ENREGISTREMENT SCORE SNAKE 1 ###
@app.route('/envoyer_score1', methods=['POST'])
def score1():
   #print(session)
   if 'id_co_s' in session:      #verifie si id_co_s est dans la session. si oui la stock dans une nouvelle varaible
      id_s = session['id_co_s']

   elif 'id_crea_s' in session :  #verifie sinon si la variable id_crea_s dans la session et la stock dans la nouvelle varaible
      id_s = session['id_crea_s']

   else :                        # si aucune des 2 var est dans la session
      print('erreur enregistrement snake')

   score = request.json
   score1 = int(score['score'])
   
   #print('id_s :',id_s)
   #print('score :',score1)

   cursor = conn.cursor()  
   cursor.execute(""" UPDATE mini_jeux SET nb_joue_snake = nb_joue_snake + 1 WHERE pseudo = %s ; """,(id_s,))      #ajoute 1 au nb de partie jouer
   conn.commit()

   cursor = conn.cursor()  
   cursor.execute(""" SELECT snake_1 FROM mini_jeux WHERE pseudo = %s ; """,(id_s,))      #recupere valeur actuel de la  BDD
   score=cursor.fetchone()
   score = score[0]

   if score1 > score :  # si nouveau score > a l'ancien score
      #print('changement score snake 1')
      cursor = conn.cursor()  
      cursor.execute(""" UPDATE mini_jeux SET snake_1 = %s WHERE pseudo = %s ; """,(score1, id_s,))      #remplace par nouveau score
      conn.commit()
   else :
      print('pas de changement snake 1')

   return render_template('1.html')


### ENREGISTREMENT SCORE SNAKE 2 ###
@app.route('/envoyer_score2', methods=['POST'])
def score2():
   if 'id_co_s' in session:      #verifie si id_co_s est dans la session. si oui la stock dans une nouvelle varaible
      id_s = session['id_co_s']

   elif 'id_crea_s' in session :  #verifie sinon si la variable id_crea_s dans la session et la stock dans la nouvelle varaible
      id_s = session['id_crea_s']

   else :                        # si aucune des 2 var est dans la session
      print('erreur enregistrement snake')

   score = request.json
   score2 = int(score['score'])

   #print('id_s :',id_s)
   #print('score :',score2)

   cursor = conn.cursor()  
   cursor.execute(""" UPDATE mini_jeux SET nb_joue_snake = nb_joue_snake + 1 WHERE pseudo = %s ; """,(id_s,))      #ajoute 1 au nb de partie jouer
   conn.commit()

   cursor = conn.cursor()  
   cursor.execute(""" SELECT snake_2 FROM mini_jeux WHERE pseudo = %s ; """,(id_s,))      #recupere valeur actuel de la  BDD
   score=cursor.fetchone()
   score = score[0]

   if score2 > score :  # si nouveau score > a l'ancien score
      #print('changement score snake 2')
      cursor = conn.cursor()  
      cursor.execute(""" UPDATE mini_jeux SET snake_2 = %s WHERE pseudo = %s ; """,(score2, id_s,))      #remplace par nouveau score
      conn.commit()
   else :
      print('pas de changement snake 2')

   return render_template('2.html')


### ENREGISTREMENT SCORE SNAKE 3 ###
@app.route('/envoyer_score3', methods=['POST'])
def score3():
   if 'id_co_s' in session:      #verifie si id_co_s est dans la session. si oui la stock dans une nouvelle varaible
      id_s = session['id_co_s']

   elif 'id_crea_s' in session :  #verifie sinon si la variable id_crea_s dans la session et la stock dans la nouvelle varaible
      id_s = session['id_crea_s']

   else :                        # si aucune des 2 var est dans la session
      print('erreur enregistrement snake')

   score = request.json
   score3 = int(score['score'])

   #print('id_s :',id_s)
   #print('score :',score3)

   cursor = conn.cursor()  
   cursor.execute(""" UPDATE mini_jeux SET nb_joue_snake = nb_joue_snake + 1 WHERE pseudo = %s ; """,(id_s,))      #ajoute 1 au nb de partie jouer
   conn.commit()

   cursor = conn.cursor()  
   cursor.execute(""" SELECT snake_3 FROM mini_jeux WHERE pseudo = %s ; """,(id_s,))      #recupere valeur actuel de la  BDD
   score=cursor.fetchone()
   score = score[0]

   if score3 > score :  # si nouveau score > a l'ancien score
      #print('changement score snake 3')
      cursor = conn.cursor()  
      cursor.execute(""" UPDATE mini_jeux SET snake_3 = %s WHERE pseudo = %s ; """,(score3, id_s,))      #remplace par nouveau score
      conn.commit()
   else :
      print('pas de changement snake 3')

   return render_template('3.html')


### PAGE CLASSEMENT ###
@app.route('/popupClassement')
def classement ():
   
   cursor = conn.cursor(dictionary=True)  # pour morpion (recupere dans un dic les 'ligne' des meilleur personne  max 10 et les renvoie pour les afficher)
   cursor.execute("""SELECT pseudo, nb_victoire_morpion, nb_joue_morpion FROM mini_jeux order by nb_victoire_morpion desc limit 10;""")
   classement_m = cursor.fetchall()
   #print("morpion :",classement_m)

   cursor = conn.cursor(dictionary=True)  #pour snake 1
   cursor.execute("""SELECT pseudo, snake_1, nb_joue_snake FROM mini_jeux order by snake_1 desc limit 10;""")
   classement_s1 = cursor.fetchall()
   #print("snake 1 :", classement_s1)

   cursor = conn.cursor(dictionary=True)  #pour snake 2
   cursor.execute("""SELECT pseudo, snake_2, nb_joue_snake FROM mini_jeux order by snake_2 desc limit 10;""")
   classement_s2 = cursor.fetchall()
   #print("snake 2 :", classement_s2)

   cursor = conn.cursor(dictionary=True)  #pour snake 3
   cursor.execute("""SELECT pseudo, snake_3, nb_joue_snake FROM mini_jeux order by snake_3 desc limit 10;""")
   classement_s3 = cursor.fetchall()
   #print("snake 3 :", classement_s3)

   cursor = conn.cursor(dictionary=True)  #pour puissance 4
   cursor.execute("""SELECT pseudo, nb_victoire_puissance_4, nb_joue_puissance_4 FROM mini_jeux order by nb_victoire_puissance_4 desc limit 10;""")
   classement_p4 = cursor.fetchall()
   #print("puissance 4 :", classement_p4)

   return render_template('popup_classement.html',classement_m = classement_m, classement_s1 = classement_s1, classement_s2 = classement_s2, classement_s3 = classement_s3, classement_p4=classement_p4) 
   # renvoie la page html et les variable qui on chacune les donnee d'un tableau pour les afficher


app.run(debug=True)
