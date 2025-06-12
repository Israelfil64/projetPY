import random
from typing import List, Dict, Tuple
from noyau_dictionnaire import NoyauDictionnaire

class FonctionnalitesAvancees:
    def __init__(self, noyau_dictionnaire: NoyauDictionnaire):
        self.noyau = noyau_dictionnaire
    
    def rechercher_dans_definitions(self, mot_cle: str) -> List[Tuple[str, str]]:
        """Recherche un mot-clé dans les définitions"""
        mot_cle_minuscule = mot_cle.lower()
        resultats = []
        
        for donnees_mot in self.noyau.dictionnaire.values():
            if mot_cle_minuscule in donnees_mot["definition"].lower():
                resultats.append((donnees_mot["mot"], donnees_mot["definition"]))
        
        return resultats
    
    def rechercher_par_lettre_initiale(self, lettre: str) -> List[str]:
        """Retourne tous les mots commençant par une lettre donnée"""
        lettre_minuscule = lettre.lower()
        return [donnees["mot"] for donnees in self.noyau.dictionnaire.values() 
                if donnees["mot"].lower().startswith(lettre_minuscule)]
    
    def rechercher_par_sequence(self, sequence: str) -> List[str]:
        """Recherche tous les mots contenant une séquence de lettres"""
        sequence_minuscule = sequence.lower()
        return [donnees["mot"] for donnees in self.noyau.dictionnaire.values() 
                if sequence_minuscule in donnees["mot"].lower()]
    
    def obtenir_statistiques(self) -> Dict:
        """Calcule et retourne les statistiques du dictionnaire"""
        if not self.noyau.dictionnaire:
            return {"total_mots": 0}
        
        mots = [donnees["mot"] for donnees in self.noyau.dictionnaire.values()]
        longueurs_mots = [len(mot) for mot in mots]
        
        statistiques = {
            "total_mots": len(mots),
            "mot_plus_long": max(mots, key=len) if mots else "",
            "mot_plus_court": min(mots, key=len) if mots else "",
            "longueur_moyenne": sum(longueurs_mots) / len(longueurs_mots) if longueurs_mots else 0,
            "categories": self._obtenir_statistiques_categories()
        }
        
        return statistiques
    
    def _obtenir_statistiques_categories(self) -> Dict[str, int]:
        """Retourne les statistiques par catégorie"""
        categories = {}
        for donnees in self.noyau.dictionnaire.values():
            categorie = donnees.get("categorie", "inconnu")
            categories[categorie] = categories.get(categorie, 0) + 1
        return categories
    
    def obtenir_mot_aleatoire(self) -> Tuple[str, str]:
        """Retourne un mot aléatoire avec sa définition"""
        if not self.noyau.dictionnaire:
            return "", ""
        
        donnees_mot = random.choice(list(self.noyau.dictionnaire.values()))
        return donnees_mot["mot"], donnees_mot["definition"]
    
    def obtenir_mots_plus_consultes(self, nombre: int = 5) -> List[Tuple[str, int]]:
        """Retourne les mots les plus consultés"""
        mots_tries = sorted(
            [(self.noyau.dictionnaire[mot]["mot"], nombre_consultations) 
             for mot, nombre_consultations in self.noyau.compteur_consultations.items()],
            key=lambda x: x[1], reverse=True
        )
        return mots_tries[:nombre]
    
    def filtrer_par_categorie(self, categorie: str) -> List[str]:
        """Filtre les mots par catégorie"""
        return [donnees["mot"] for donnees in self.noyau.dictionnaire.values() 
                if donnees.get("categorie", "").lower() == categorie.lower()]

