#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe markov, à utiliser pour solutionner la problématique.
    C'est un gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers.

    Les méthodes aparaissant dans ce fichier définissent une API qui est utilisée par l'application
    de test testmarkov.py
    Les paramètres d'entrée et de sortie (Application Programming Interface, API) sont définis,
    mais le code est à écrire au complet.
    Vous pouvez ajouter toutes les méthodes et toutes les variables nécessaires au bon fonctionnement du système

    La classe markov est invoquée par la classe testmarkov (contenue dans testmarkov.py):

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier testmarkov.py)
        - Note: vous pouvez tester votre code en utilisant les commandes:
            + "python testmarkov.py"
            + "python testmarkov.py -h" (donne la liste des arguments possibles)
            + "python testmarkov.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
"""
import numpy as np
import math
import os
import glob
import ntpath
import random

class markov():
    """Classe à utiliser pour coder la solution à la problématique:

        - Contient certaines fonctions de base pour faciliter le travail (recherche des auteurs).
        - Les interfaces du code à développer sont présentes, mais tout le code est à écrire
        - En particulier, il faut compléter les fonctions suivantes:
            - find_author(oeuvre)
            - gen_text(auteur, taille, textname)
            - get_nth_element(auteur, n)
            - analyze()

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
    """

    # Le code qui suit est fourni pour vous faciliter la vie.  Il n'a pas à être modifié
    # Signes de ponctuation à retirer (compléter la liste qui ne comprend que "!" et "," au départ)
    PONC = ["!",",",";",":","(",")","?","*","…","-","[","]","/",".","«","»","“","”","‘","’","'","\n\n","\n","    ","   ","_","--","...","$","^","#","&","%","@","|","~","<",">","—","-"]


    def set_ponc(self, value):
        """Détermine si les signes de ponctuation sont conservés (True) ou éliminés (False)

        Args:
            value (boolean) : Conserve la ponctuation (Vrai) ou élimine la ponctuation (Faux)

        Returns:
            void : ne fait qu'assigner la valeur du champs keep_ponc
        """
        self.keep_ponc = value

    def print_ponc(self):
        print("Signes de ponctuation à retirer: ", self.PONC)

    def set_auteurs(self):
        """Obtient la liste des auteurs, à partir du répertoire qui les contient tous

        Note: le champs self.rep_aut doit être prédéfini:
            - Par défaut, il contient le répertoire d'exécution du script
            - Peut être redéfini par la méthode set_aut_dir

        Returns:
            void : ne fait qu'obtenir la liste des répertoires d'auteurs et modifier la liste self.auteurs
        """
        files = self.rep_aut + "/*"
        full_path_auteurs = glob.glob(files)
        for auteur in full_path_auteurs:
            self.auteurs.append(ntpath.basename(auteur))
        return

    def get_aut_files(self, auteur):
        """Obtient la liste des fichiers (avec le chemin complet) des oeuvres d'un auteur

        Args:
            auteur (string): le nom de l'auteur dont on veut obtenir la liste des oeuvres

        Returns:
            oeuvres (Liste[string]): liste des oeuvres (avec le chemin complet pour y accéder)
        """
        auteur_dir = self.rep_aut + "/" + auteur + "/*"
        oeuvres = glob.glob(auteur_dir)
        return oeuvres

    def set_aut_dir(self, aut_dir):
        """Définit le nom du répertoire qui contient l'ensemble des répertoires d'auteurs

        Note: L'appel à cette méthode extrait la liste des répertoires d'auteurs et les ajoute à self.auteurs

        Args (string) : Nom du répertoire en question (peut être absolu ou bien relatif au répertoire d'exécution)

        Returns:
            void : ne fait que définir le nom du répertoire qui contient les répertoires d'auteurs
        """
        cwd = os.getcwd()
        if os.path.isabs(aut_dir):
            self.rep_aut = aut_dir
        else:
            self.rep_aut = os.path.join(cwd, aut_dir)

        self.rep_aut = os.path.normpath(self.rep_aut)
        self.set_auteurs()
        return


    def set_ngram(self, ngram):
        """Indique que l'analyse et la génération de texte se fera avec des n-grammes de taille ngram

        Args:
            ngram (int) : Indique la taille des n-grammes (1, 2, 3, ...)

        Returns:
            void : ne fait que mettre à jour le champs ngram
        """
        self.ngram = ngram

    def __init__(self):
        """Initialize l'objet de type markov lorsqu'il est créé

        Args:
            aucun: Utilise simplement les informations fournies dans l'objet Markov_config

        Returns:
            void : ne fait qu'initialiser l'objet de type markov
        """

        #Initialisation des champs nécessaires aux fonctions fournies
        super().__init__()
        self.keep_ponc = True
        self.rep_aut = os.getcwd()
        self.auteurs = []
        self.ngram = 1

        # Au besoin, ajouter votre code d'initialisation de l'objet de type markov lors de sa création

        return

    # Ajouter les structures de données et les fonctions nécessaires à l'analyse des textes,
    #   la production de textes aléatoires, la détection d'oeuvres inconnues,
    #   l'identification des n-ièmes mots les plus fréquents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelée en premier par testmarkov.py
    # Ensuite, selon ce qui est demandé, les fonctions find_author(), gen_text() ou get_nth_element() sont appelées

    def find_author(self, oeuvre):
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'oeuvre inconnue avec les écrits de chacun d'entre eux

        Args:
            oeuvre (string): Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns:
            resultats (Liste[(string,float)]) : Liste de tuples (auteurs, niveau de proximité), où la proximité est un nombre entre 0 et 1)
        """
        resultats = []

        #on fait lanalyse du texte inconnue
        with open(oeuvre, 'r', encoding='utf8') as file:
            textinc = file.read()
            for p in self.PONC:
                textinc = textinc.replace(p, " ")
            textinc = textinc.lower().split()
            keep_wordinc = []
            for word in textinc:
                if len(word) > 2:
                    keep_wordinc.append(word)

        freq_dict_inconnu = {}
        for i in range(len(keep_wordinc)-self.ngram+1):
            ngrammeinc = " ".join(keep_wordinc[i:i+self.ngram])
            if ngrammeinc in freq_dict_inconnu:
                freq_dict_inconnu[ngrammeinc] = freq_dict_inconnu[ngrammeinc] + 1
            else:
                freq_dict_inconnu[ngrammeinc] = 1

        #norme du vecteur de l'inconnu
        norm_inconnu = math.sqrt(sum(freq_dict_inconnu[ngrammeinc]**2 for ngrammeinc in freq_dict_inconnu))

        #calcul avec les autres auteurs

        for auteur in self.freq_dict.keys():
            freq_dict_auteur = self.freq_dict[auteur]
            norm_auteur = math.sqrt(sum(freq_dict_auteur[ngrammeinc]**2 for ngrammeinc in freq_dict_auteur))
            produit_scalaire = sum(freq_dict_auteur.get(ngrammeinc, 0) * freq_dict_inconnu.get(ngrammeinc, 0) for ngrammeinc in set(freq_dict_auteur) | set(freq_dict_inconnu))
            normal = produit_scalaire / (norm_auteur * norm_inconnu)
            resultats.append((auteur, normal))


        # Ajouter votre code pour déterminer la proximité du fichier passé en paramètre avec chacun des auteurs
        # Retourner la liste des auteurs, chacun avec sa proximité au fichier inconnu
        # Plus la proximité est grande, plus proche l'oeuvre inconnue est des autres écrits d'un auteur
        #   Le produit scalaire entre le vecteur représentant les oeuvres d'un auteur
        #       et celui associé au texte inconnu pourrait s'avérer intéressant...
        #   Le produit scalaire devrait être normalisé avec la taille du vecteur associé au texte inconnu:
        #   proximité = (A . B) / (|A| |B|)   où A est le vecteur du texte inconnu et B est celui d'un auteur,
        #           . est le produit scalaire, et |X| est la norme (longueur) du vecteur X

        return resultats

    def gen_text(self, auteur, taille, textname):
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args:
            auteur (string): Nom de l'auteur à utiliser
            taille (int): Taille du texte à générer
            textname (string): Nom du fichier texte à générer.

        Returns:
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        liste_ngramme = []
        probability = []

        for ngram, count in self.freq_dict[auteur].items():
            liste_ngramme.append(ngram)
            probability.append(count)

        probability = np.array(probability)
        probability = probability.astype(float) / probability.sum()

        file = open(textname, "w")
        ngram_index = np.random.choice(len(liste_ngramme), size=taille, p=probability)
        for i in range(taille):
            file.write(liste_ngramme[ngram_index[i]] + " ")
        file.close()

        return


    def get_nth_element(self, auteur, n):
        """Après analyse des textes d'auteurs connus, retourner le n-ième plus fréquent n-gramme de l'auteur indiqué

        Args:
            auteur (string): Nom de l'auteur à utiliser
            n (int): Indice du n-gramme à retourner

        Returns:
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherché (il est possible qu'il y ait plus d'un n-gramme au même rang)
        """

        dict_trie = dict(sorted(self.freq_dict[auteur].items(), key = lambda x: x[1], reverse=True))
        ngramme_trier = list(dict_trie.keys())
        dict_ngramme_trier = {}

        for index, freq in enumerate(dict_trie.values()):
            if freq in dict_ngramme_trier.keys():
                dict_ngramme_trier[freq].append(ngramme_trier[index])
            else:
                dict_ngramme_trier.update({freq: [ngramme_trier[index]]})

        for index, freq in enumerate(dict_ngramme_trier.keys()):
            if index == n - 1:
                return dict_ngramme_trier[freq]


    def analyze(self):
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args:
            void: toute l'information est contenue dans l'objet markov

        Returns:
            void : ne retourne rien, toute l'information extraite est conservée dans des strutures internes
        """


        # Ajouter votre code ici pour traiter l'ensemble des oeuvres de l'ensemble des auteurs
        # Pour l'analyse:  faire le calcul des fréquences de n-grammes pour l'ensemble des oeuvres
        #   d'un certain auteur, à la fois par oeuvre et aussi sans distinction des oeuvres individuelles,
        #       et recommencer ce calcul pour chacun des auteurs
        #   En procédant ainsi, les oeuvres comprenant plus de mots auront un impact plus grand sur
        #   les statistiques globales d'un auteur
        # Il serait possible de considérer chacune des oeuvres d'un auteur comme ayant un poids identique.
        #   Pour ce faire, il faudrait faire les calculs de fréquence pour chacune des oeuvres
        #       de façon indépendante, pour ensuite les normaliser (diviser chaque vecteur par sa norme),
        #       avant des les additionner pour obtenir le vecteur global d'un auteur
        #   De cette façon, les mots d'un court poème auraient une importance beaucoup plus grande que
        #   les mots d'une très longue oeuvre du même auteur. Ce n'est PAS ce qui vous est demandé ici.



        #Initialisation du dictionnaire de fréquence
        self.freq_dict = {}
        for auteur in self.auteurs:
            self.freq_dict[auteur] = {}
        #Parcours des oeuvres de tous les auteurs
        for auteur in self.auteurs:
            aut_files = self.get_aut_files(auteur)
            for oeuvre in aut_files:
                with open(oeuvre, 'r',encoding='utf8') as file:
                    text = file.read().lower()
                    for p in self.PONC:
                        text = text.replace(p, " ")
                    text = text.split()
                    keep_word = []
                    for word in text:
                        if len(word) > 2:
                            keep_word.append(word)

                    #calcul des fréquences des n-grammes
                    for i in range(len(keep_word) - (self.ngram +1)):
                        ngramme = " ".join(keep_word[i:i+self.ngram])
                        if ngramme in self.freq_dict[auteur]:
                            self.freq_dict[auteur][ngramme] = self.freq_dict[auteur][ngramme] + 1
                        else:
                            self.freq_dict[auteur][ngramme] = 1

        return
