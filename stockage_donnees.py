import json
import os
from typing import Dict
from noyau_dictionnaire import NoyauDictionnaire

class StockageDonnees:
    def __init__(self, nom_fichier: str = "donnees_dictionnaire.json"):
        self.nom_fichier = nom_fichier
    
    def sauvegarder_dictionnaire(self, noyau_dictionnaire: NoyauDictionnaire) -> bool:
        """Sauvegarde le dictionnaire dans un fichier JSON"""
        try:
            donnees = noyau_dictionnaire.obtenir_donnees_dictionnaire()
            with open(self.nom_fichier, 'w', encoding='utf-8') as fichier:
                json.dump(donnees, fichier, ensure_ascii=False, indent=2)
            return True
        except Exception as erreur:
            print(f"Erreur lors de la sauvegarde: {erreur}")
            return False
    
    def charger_dictionnaire(self, noyau_dictionnaire: NoyauDictionnaire) -> bool:
        """Charge le dictionnaire depuis un fichier JSON"""
        try:
            if os.path.exists(self.nom_fichier):
                with open(self.nom_fichier, 'r', encoding='utf-8') as fichier:
                    donnees = json.load(fichier)
                noyau_dictionnaire.definir_donnees_dictionnaire(donnees)
                return True
            else:
                # Créer un dictionnaire avec quelques mots par défaut
                self._creer_dictionnaire_par_defaut(noyau_dictionnaire)
                return True
        except Exception as erreur:
            print(f"Erreur lors du chargement: {erreur}")
            return False
    
    def _creer_dictionnaire_par_defaut(self, noyau_dictionnaire: NoyauDictionnaire):
        """Crée un dictionnaire par défaut avec quelques mots"""
        mots_par_defaut = [
            ("ordinateur", "Machine électronique de traitement de l'information", "nom"),
            ("programmer", "Écrire du code informatique", "verbe"),
            ("python", "Langage de programmation interprété", "nom"),
            ("algorithme", "Suite d'instructions pour résoudre un problème", "nom"),
            ("variable", "Élément pouvant prendre différentes valeurs", "nom"),
            ("fonction", "Bloc de code réutilisable qui effectue une tâche spécifique", "nom"),
            ("boucle", "Structure de contrôle qui répète des instructions", "nom"),
            ("condition", "Expression qui peut être vraie ou fausse", "nom")
        ]
        
        for mot, definition, categorie in mots_par_defaut:
            noyau_dictionnaire.ajouter_mot(mot, definition, categorie)
    
    def sauvegarde_automatique(self, noyau_dictionnaire: NoyauDictionnaire):
        """Sauvegarde automatique après modification"""
        self.sauvegarder_dictionnaire(noyau_dictionnaire)

