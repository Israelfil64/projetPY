import difflib
from typing import Dict, List, Optional, Tuple

class NoyauDictionnaire:
    def __init__(self):
        self.dictionnaire: Dict[str, Dict] = {}
        self.compteur_consultations: Dict[str, int] = {}
    
    def ajouter_mot(self, mot: str, definition: str, categorie: str = "nom") -> bool:
        """Ajoute un nouveau mot au dictionnaire"""
        mot_minuscule = mot.lower()
        if mot_minuscule in self.dictionnaire:
            return False
        
        self.dictionnaire[mot_minuscule] = {
            "mot": mot,
            "definition": definition,
            "categorie": categorie
        }
        self.compteur_consultations[mot_minuscule] = 0
        return True
    
    def rechercher_mot(self, mot: str) -> Optional[Dict]:
        """Recherche un mot et incrémente son compteur de consultation"""
        mot_minuscule = mot.lower()
        if mot_minuscule in self.dictionnaire:
            self.compteur_consultations[mot_minuscule] += 1
            return self.dictionnaire[mot_minuscule]
        return None
    
    def modifier_mot(self, mot: str, nouvelle_definition: str = None, nouvelle_categorie: str = None) -> bool:
        """Modifie la définition ou la catégorie d'un mot existant"""
        mot_minuscule = mot.lower()
        if mot_minuscule not in self.dictionnaire:
            return False
        
        if nouvelle_definition:
            self.dictionnaire[mot_minuscule]["definition"] = nouvelle_definition
        if nouvelle_categorie:
            self.dictionnaire[mot_minuscule]["categorie"] = nouvelle_categorie
        return True
    
    def supprimer_mot(self, mot: str) -> bool:
        """Supprime un mot du dictionnaire"""
        mot_minuscule = mot.lower()
        if mot_minuscule in self.dictionnaire:
            del self.dictionnaire[mot_minuscule]
            del self.compteur_consultations[mot_minuscule]
            return True
        return False
    
    def lister_mots_alphabetiquement(self) -> List[str]:
        """Retourne la liste des mots triés alphabétiquement"""
        return sorted([donnees["mot"] for donnees in self.dictionnaire.values()])
    
    def suggerer_mots_similaires(self, mot: str, nombre: int = 3) -> List[str]:
        """Suggère des mots similaires en cas d'erreur de frappe"""
        mot_minuscule = mot.lower()
        tous_les_mots = list(self.dictionnaire.keys())
        correspondances_proches = difflib.get_close_matches(mot_minuscule, tous_les_mots, n=nombre, cutoff=0.6)
        return [self.dictionnaire[correspondance]["mot"] for correspondance in correspondances_proches]
    
    def obtenir_donnees_dictionnaire(self) -> Dict:
        """Retourne toutes les données du dictionnaire"""
        return {
            "dictionnaire": self.dictionnaire,
            "compteur_consultations": self.compteur_consultations
        }
    
    def definir_donnees_dictionnaire(self, donnees: Dict):
        """Charge les données du dictionnaire"""
        self.dictionnaire = donnees.get("dictionnaire", {})
        self.compteur_consultations = donnees.get("compteur_consultations", {})

