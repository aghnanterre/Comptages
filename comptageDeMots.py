#!/usr/bin/python 
# -*- coding: utf-8 -*-
#Filename: 2018_01_16_comptageDeMots.py
#iso-8859-1



#####################################################################
#####################################################################
#
#	Le programme compte les mots de tous les textgrids qui se trouvent dans le répertoire repertoireFichierTraite

#Pour chaque enquête, les tires dans lesquels les mots sont comptés sont explicitement énumérées.

#
#####################################################################
#####################################################################


##########################################################################################################################################
# FONCTION PRINCIPALE : qui calcule les nombre de mots par tire  ##########################################################################################################################################

#################################################################################
#fonction nombreDeMots(repertoireFichierTraite : string,nomEnquete,nomRepertoireFichiersSortie : nom du répertoire où mettre les fichiers résultats
#
#################################################################################

def nombreDeMots(repertoireFichierTraite,nomEnquete):
	# Ouverture du fichier sur lequel effectuer la requête
	# fichier Texte exporté depuis Praat au format txt, codage utf-8


#	print "*** Début de la phase d'ouverture" # Debug
	
#	print "Essai d'ouverture du fichier dont le nom est fourni en quatrième paramètre: ",nomEnquete # Debug

	try :
		fo = open(repertoireFichierTraite+"/"+nomEnquete, "r")
	except IOError:
		print(e)

	# Initialisation des variables
	nomTrouve=0
	texteTrouve=0
	nbOcc=0
	resu=""
	#---------------------------------------------------		
	#BOUCLE PRINCIPALE (de traitement du fichier Textgrid entree.txt)
	#il faut remettre le pointeur au début du fichier
	print("***********************************************************************************************")
	print("Comptage des mots dans l'enquête ",nomEnquete)
	resu=resu+"******************************\n"
	resu=resu+"Enumération des tours de parole dans le fichier "+nomEnquete+"\n"
	resu=resu+"******************************\n"



	fo.seek(0)
	nbOccTrouvees=0
	indiceNomCourant=-1
	cptLignes=0
	resuCSV="Enquete;Tire;xDeb;nbMots;Tour de parole\n"
	resuCSVTires="Enquete;Tire;nbMotsTire\n"
	nbMotsEnquete=0
	nbMotsTire=0

	for line in fo:
#		print(line[0:20]) #debug
		cptLignes=cptLignes+1
	# Identification du locuteur (nomTire)
		trouveNomEnPosition = line.find("name =")
#		print line.find(\"name\") = ",line.find("name =") #Debug
		if trouveNomEnPosition>0:
			print("tire trouvée pour ",nomEnquete," : \n",line)
			if indiceNomCourant!=-1:
				resuCSVTires=resuCSVTires+nomEnquete+";"+nomTire+";"+str(nbMotsTire)+"\n"
			nbMotsTire=0
			nbMotsTourDeParole=0
			nomTrouve=1
			indiceNomCourant +=1
			line= line[trouveNomEnPosition+8:]
			nomTire=line[0:len(line)-3]
			print("Tire : ", nomTire)
			
			

		
	# positionIntervalle (coordonnée x du début de l'intervalle)		
		trouveXEnPosition= line.find("xmin")
		if trouveXEnPosition>0:
			line= line[trouveNomEnPosition+12:]
			xDeb=line[8:15]
	
	# lorsque la ligne contient "text"		
		trouveTexteEnPosition = line.find("text")
		
		if trouveTexteEnPosition>0:
	# Si cette ligne du Textgrid correspond à un intervalle (si texte !="")
			line2= line[trouveTexteEnPosition+8:]
			texte=line2[0:len(line2)-3]

			# C'est ici qu'on compte les mots
			if (texte!=""):
#				print(texte)	#DEBUG
			# suppression des marques de chevauchement 
				texte=texte.replace('<','')
				texte=texte.replace('>','')
			# suppression des parenthèses
				texte=re.sub('\(.*?\)','', texte.rstrip())
			
			
			
#comptage proprement dit

			#spliter les mots séparés par des espaces
				listeMotsProvisoire=texte.split()
			
			#spliter les mots séparés par des apostrophes
				listeMots=list()
				for m in listeMotsProvisoire:
					listeMots.extend(m.split('\''))
					
			#supprimer du comptage les silences, les points d'interrogation
			#supprimer les mots '(.)' et '(..)"
					motsASupprimer = ["(.)","(..)","?",'.','..']
					for mas in motsASupprimer:
						while listeMots.count(mas)>0:
							listeMots.remove(mas)

							
			
				nbMotsTourDeParole=len(listeMots)
				#print texte #Debug
				#print nbMotsTourDeParole #Debg
				resuCSV=resuCSV+nomEnquete+";"+nomTire+";"+xDeb+";"+str(nbMotsTourDeParole)+";"+texte+";\n"
				nbMotsTire = nbMotsTire + nbMotsTourDeParole
	print(cptLignes," lignes traitées")

#ici un fichier résultat est fait qui donne le compte par tour de parole pour l'enquête nomEnquête
	fichierResu=open("Resultats/"+date+"/"+row+"_comptages.csv",'w')
	fichierResu.write(resuCSV)
	fichierResuTires=open("Resultats/"+date+"/"+row+"_comptagesParTire.csv",'w')
	resuCSVTires=resuCSVTires+nomEnquete+";"+nomTire+";"+str(nbMotsTire)+"\n" # il faut ajouter à resuCSVTires le nombre de mmots de la dernière tire traitée
	fichierResuTires.write(resuCSVTires)

	fo.close()
	return('Fin du traitement de',row)	


##################################################################################################################################################################################################################################################################################### 

#PROGRAMME PRINCIPAL

##############################################################################################################################################################################################################################################################################
import os
import os.path
#import csv
import sys
#import codecs
import string
import re
#import utilsES
import datetime


###
###  PARAMETRES A METTRE A JOURï
###
print("*********************\n DEBUT EXECUTION \n*********************\n")
print("  PARAMETRES\n")

# DATE
date=datetime.datetime.now().strftime("%y_%m_%d")
print("date (pour les résultats) = ",date,"\n")

#Repertoire où sont tous les fichiers à traiter
repertoireFichierTraite="./Textgrids_a_compter"

nomRepertoireFichiersSortie="Resultats/"+date+"/"
print("nomRepertoireFichiersSortie = ",nomRepertoireFichiersSortie,"\n")


# Création éventuelle du sous-répertoire qui vient d'être nommé
nomRepertoireACreer = nomRepertoireFichiersSortie
print("Répertoire créé s'il n'existait pas :",nomRepertoireACreer,"\n")
try:
		os.mkdir(nomRepertoireACreer)
except OSError:
	pass
print("    FIN PARAMETRES \n**************************\n")

####
### FIN DES PARAMETRES A METTRE A JOUR
####


#################################################################
# RE-CREATION DU FICHIER CSV QUI CONTIENT LA LISTE DES Textgrids
# à "compter"
#### récupération de la liste des fichiers dans le répertoire des transcriptions à compter ; 
print("Récupération de la liste des fichiers du répertoire où il y a les transcriptions à compter ",repertoireFichierTraite,"\n")
listefic = os.listdir(repertoireFichierTraite)


####écriture de la liste des fichiers récupérée plus haut dans un fichier listeEnquetesACompter.csv
print("Ecriture du fichier qui contient la liste des enquêtes traitées\n")
listeEnquetesTraitees = date+"_LogListeEnquetesACompterCSV.csv"
listeFichiers = open(listeEnquetesTraitees, 'a')
for f in listefic:
	listeFichiers.write(f+"\n")
print("La liste des enquêtes dont les mots sont à dénombrer est dans le fichier log : ",listeEnquetesTraitees,"\n")

listeTranscriptionsATraiter = listefic # si on n'a pas listefic, on peut remplir listeTranscriptionsAtraiter avec le contenu de listeEnquetesTraitees


for row in listeTranscriptionsATraiter:
	print("Row = ", row)
	if not row.find(".DS_Store")>-1: # si dans la liste des fichiers du répertoire, il y a ".DS_Store", on ignore.
		print(nombreDeMots(\
			repertoireFichierTraite,\
			row))

