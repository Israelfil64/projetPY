import csv
import random
from typing import List
from noyau_dictionnaire import NoyauDictionnaire

class ExportationBonus:
    def __init__(self, noyau_dictionnaire: NoyauDictionnaire):
        self.noyau = noyau_dictionnaire
    
    def exporter_vers_txt(self, nom_fichier: str = "exportation_dictionnaire.txt") -> bool:
        """Exporte le dictionnaire vers un fichier texte"""
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as fichier:
                fichier.write("DICTIONNAIRE DE MOTS\n")
                fichier.write("=" * 50 + "\n\n")
                
                mots = sorted(self.noyau.dictionnaire.values(), key=lambda x: x["mot"].lower())
                for donnees_mot in mots:
                    fichier.write(f"{donnees_mot['mot']} ({donnees_mot.get('categorie', 'nom')})\n")
                    fichier.write(f"Définition: {donnees_mot['definition']}\n")
                    fichier.write("-" * 30 + "\n\n")
            return True
        except Exception as erreur:
            print(f"Erreur lors de l'exportation TXT: {erreur}")
            return False
    
    def exporter_vers_csv(self, nom_fichier: str = "exportation_dictionnaire.csv") -> bool:
        """Exporte le dictionnaire vers un fichier CSV"""
        try:
            with open(nom_fichier, 'w', newline='', encoding='utf-8') as fichier:
                redacteur = csv.writer(fichier)
                redacteur.writerow(["Mot", "Définition", "Catégorie", "Consultations"])
                
                for cle_mot, donnees_mot in self.noyau.dictionnaire.items():
                    consultations = self.noyau.compteur_consultations.get(cle_mot, 0)
                    redacteur.writerow([
                        donnees_mot["mot"],
                        donnees_mot["definition"],
                        donnees_mot.get("categorie", "nom"),
                        consultations
                    ])
            return True
        except Exception as erreur:
            print(f"Erreur lors de l'exportation CSV: {erreur}")
            return False
    
    def jeu_deviner_mot(self) -> bool:
        """Jeu: deviner le mot à partir de sa définition"""
        if not self.noyau.dictionnaire:
            print("Le dictionnaire est vide!")
            return False
        
        donnees_mot = random.choice(list(self.noyau.dictionnaire.values()))
        mot = donnees_mot["mot"]
        definition = donnees_mot["definition"]
        
        print(f"\nJEU: DEVINEZ LE MOT!")
        print(f"Définition: {definition}")
        print(f"Catégorie: {donnees_mot.get('categorie', 'inconnu')}")
        print(f"Le mot contient {len(mot)} lettres.")
        
        tentatives = 3
        while tentatives > 0:
            supposition = input(f"\nVotre réponse ({tentatives} essais restants): ").strip()
            
            if supposition.lower() == mot.lower():
                print(f"🎉 Bravo! La réponse était bien '{mot}'!")
                return True
            else:
                tentatives -= 1
                if tentatives > 0:
                    # Donner un indice
                    if len(supposition) == len(mot):
                        print("❌ Mauvaise réponse, mais la longueur est correcte!")
                    else:
                        print(f"❌ Mauvaise réponse! Le mot a {len(mot)} lettres.")
        
        print(f"😞 Dommage! La réponse était '{mot}'.")
        return False
    
    def jeu_deviner_definition(self) -> bool:
        """Jeu: deviner la définition à partir du mot"""
        if not self.noyau.dictionnaire:
            print("Le dictionnaire est vide!")
            return False
        
        donnees_mot = random.choice(list(self.noyau.dictionnaire.values()))
        mot = donnees_mot["mot"]
        definition = donnees_mot["definition"]
        
        print(f"\nJEU: DÉFINISSEZ LE MOT!")
        print(f"Mot: {mot}")
        print(f"Catégorie: {donnees_mot.get('categorie', 'inconnu')}")
        
        definition_utilisateur = input("\nDonnez votre définition: ").strip()
        
        print(f"\nVotre définition: {definition_utilisateur}")
        print(f"Vraie définition: {definition}")
        
        score_similarite = self._calculer_similarite(definition_utilisateur.lower(), definition.lower())
        
        if score_similarite > 0.5:
            print(f"🎉 Excellente définition! Similarité: {score_similarite:.0%}")
            return True
        else:
            print(f"📖 Pas mal, mais la vraie définition est différente. Similarité: {score_similarite:.0%}")
            return False
    
    def _calculer_similarite(self, texte1: str, texte2: str) -> float:
        """Calcule une similarité basique entre deux textes"""
        mots1 = set(texte1.split())
        mots2 = set(texte2.split())
        
        if not mots1 and not mots2:
            return 1.0
        if not mots1 or not mots2:
            return 0.0
        
        intersection = mots1.intersection(mots2)
        union = mots1.union(mots2)
        
        return len(intersection) / len(union)

