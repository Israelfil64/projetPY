import os
import sys
from noyau_dictionnaire import NoyauDictionnaire
from stockage_donnees import StockageDonnees
from fonctionnalites_avancees import FonctionnalitesAvancees
from exportation_bonus import ExportationBonus

class InterfaceDictionnaire:
    def __init__(self):
        self.noyau = NoyauDictionnaire()
        self.stockage = StockageDonnees()
        self.avancee = FonctionnalitesAvancees(self.noyau)
        self.exportation = ExportationBonus(self.noyau)
        
        # Charger les données au démarrage
        self.stockage.charger_dictionnaire(self.noyau)
    
    def effacer_ecran(self):
        """Efface l'écran"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def afficher_bienvenue(self):
        """Affiche le message de bienvenue"""
        self.effacer_ecran()
        print(" DICTIONNAIRE INTERACTIF PYTHON ")
        print("=" * 50)
        
        # Afficher un mot aléatoire
        mot_aleatoire, definition_aleatoire = self.avancee.obtenir_mot_aleatoire()
        if mot_aleatoire:
            print(f"\n Mot du jour: {mot_aleatoire}")
            print(f"   Définition: {definition_aleatoire}")
        
        statistiques = self.avancee.obtenir_statistiques()
        print(f"\n Statistiques: {statistiques['total_mots']} mots dans le dictionnaire")
        print("=" * 50)
    
    def afficher_menu(self):
        """Affiche le menu principal"""
        print("\n  MENU PRINCIPAL:")
        print(" 1.   Rechercher un mot")
        print(" 2.   Ajouter un nouveau mot")
        print(" 3.   Modifier un mot")
        print(" 4.   Supprimer un mot")
        print(" 5.   Lister tous les mots")
        print(" 6.   Rechercher dans les définitions")
        print(" 7.   Mots par lettre initiale")
        print(" 8.   Mots contenant une séquence")
        print(" 9.   Statistiques du dictionnaire")
        print(" 10.  Mots les plus consultés")
        print(" 11.  Filtrer par catégorie")
        print(" 12.  Exporter le dictionnaire")
        print(" 13.  Jeux")
        print(" 0.   Quitter")
        print("-" * 30)
    
    def menu_rechercher_mot(self):
        """Menu de recherche de mot"""
        mot = input("Entrez le mot à rechercher: ").strip()
        if not mot:
            print(" Veuillez entrer un mot valide!")
            return
        
        resultat = self.noyau.rechercher_mot(mot)
        if resultat:
            print(f"\n Mot trouvé:")
            print(f"   Mot: {resultat['mot']}")
            print(f"   Définition: {resultat['definition']}")
            print(f"   Catégorie: {resultat.get('categorie', 'inconnu')}")
            consultations = self.noyau.compteur_consultations.get(mot.lower(), 0)
            print(f"   Consultations: {consultations}")
        else:
            print(f" Mot '{mot}' non trouvé.")
            suggestions = self.noyau.suggerer_mots_similaires(mot)
            if suggestions:
                print(f" Mots similaires: {', '.join(suggestions)}")
    
    def menu_ajouter_mot(self):
        """Menu d'ajout de mot"""
        mot = input("Entrez le nouveau mot: ").strip()
        if not mot:
            print(" Veuillez entrer un mot valide!")
            return
        
        definition = input("Entrez la définition: ").strip()
        if not definition:
            print(" Veuillez entrer une définition!")
            return
        
        print("\nCatégories disponibles: nom, verbe, adjectif, adverbe, autre")
        categorie = input("Entrez la catégorie (par défaut: nom): ").strip() or "nom"
        
        if self.noyau.ajouter_mot(mot, definition, categorie):
            print(f" Mot '{mot}' ajouté avec succès!")
            self.stockage.sauvegarde_automatique(self.noyau)
        else:
            print(f" Le mot '{mot}' existe déjà!")
    
    def menu_modifier_mot(self):
        """Menu de modification de mot"""
        mot = input("Entrez le mot à modifier: ").strip()
        if not mot:
            print(" Veuillez entrer un mot valide!")
            return
        
        actuel = self.noyau.rechercher_mot(mot)
        if not actuel:
            print(f" Mot '{mot}' non trouvé!")
            return
        
        print(f"\nMot actuel: {actuel['mot']}")
        print(f"Définition actuelle: {actuel['definition']}")
        print(f"Catégorie actuelle: {actuel.get('categorie', 'inconnu')}")
        
        nouvelle_definition = input("\nNouvelle définition (Entrée pour garder): ").strip()
        nouvelle_categorie = input("Nouvelle catégorie (Entrée pour garder): ").strip()
        
        if nouvelle_definition or nouvelle_categorie:
            if self.noyau.modifier_mot(mot, nouvelle_definition or None, nouvelle_categorie or None):
                print(f" Mot '{mot}' modifié avec succès!")
                self.stockage.sauvegarde_automatique(self.noyau)
            else:
                print(f" Erreur lors de la modification!")
        else:
            print("ℹ Aucune modification effectuée.")
    
    def menu_supprimer_mot(self):
        """Menu de suppression de mot"""
        mot = input("Entrez le mot à supprimer: ").strip()
        if not mot:
            print(" Veuillez entrer un mot valide!")
            return
        
        actuel = self.noyau.rechercher_mot(mot)
        if not actuel:
            print(f" Mot '{mot}' non trouvé!")
            return
        
        print(f"\nMot à supprimer: {actuel['mot']}")
        print(f"Définition: {actuel['definition']}")
        
        confirmation = input("\nÊtes-vous sûr de vouloir supprimer ce mot? (oui/non): ").strip().lower()
        if confirmation in ['oui', 'o', 'yes', 'y']:
            if self.noyau.supprimer_mot(mot):
                print(f" Mot '{mot}' supprimé avec succès!")
                self.stockage.sauvegarde_automatique(self.noyau)
            else:
                print(f" Erreur lors de la suppression!")
        else:
            print("ℹ Suppression annulée.")
    
    def menu_lister_mots(self):
        """Menu de listage des mots"""
        mots = self.noyau.lister_mots_alphabetiquement()
        if not mots:
            print(" Le dictionnaire est vide!")
            return
        
        print(f"\n Liste des {len(mots)} mots (par ordre alphabétique):")
        print("-" * 50)
        
        for i, mot in enumerate(mots, 1):
            print(f"{i:3d}. {mot}")
            if i % 20 == 0 and i < len(mots):
                input("\nAppuyez sur Entrée pour continuer...")
    
    def menu_rechercher_definitions(self):
        """Menu de recherche dans les définitions"""
        mot_cle = input("Entrez le mot-clé à rechercher dans les définitions: ").strip()
        if not mot_cle:
            print(" Veuillez entrer un mot-clé valide!")
            return
        
        resultats = self.avancee.rechercher_dans_definitions(mot_cle)
        if resultats:
            print(f"\n {len(resultats)} résultat(s) trouvé(s) pour '{mot_cle}':")
            print("-" * 50)
            for mot, definition in resultats:
                print(f" {mot}: {definition}")
                print()
        else:
            print(f" Aucun résultat trouvé pour '{mot_cle}'.")
    
    def menu_rechercher_par_lettre(self):
        """Menu de recherche par lettre initiale"""
        lettre = input("Entrez la lettre initiale: ").strip()
        if not lettre or len(lettre) != 1:
            print(" Veuillez entrer une seule lettre!")
            return
        
        mots = self.avancee.rechercher_par_lettre_initiale(lettre)
        if mots:
            print(f"\n {len(mots)} mot(s) commençant par '{lettre.upper()}':")
            print("-" * 30)
            for mot in sorted(mots):
                print(f"• {mot}")
        else:
            print(f" Aucun mot commençant par '{lettre.upper()}'.")
    
    def menu_rechercher_par_sequence(self):
        """Menu de recherche par séquence"""
        sequence = input("Entrez la séquence de lettres: ").strip()
        if not sequence:
            print(" Veuillez entrer une séquence valide!")
            return
        
        mots = self.avancee.rechercher_par_sequence(sequence)
        if mots:
            print(f"\n {len(mots)} mot(s) contenant '{sequence}':")
            print("-" * 30)
            for mot in sorted(mots):
                print(f"• {mot}")
        else:
            print(f" Aucun mot contenant '{sequence}'.")
    
    def menu_afficher_statistiques(self):
        """Menu des statistiques"""
        statistiques = self.avancee.obtenir_statistiques()
        
        print("\n STATISTIQUES DU DICTIONNAIRE:")
        print("=" * 40)
        print(f"Nombre total de mots: {statistiques['total_mots']}")
        
        if statistiques['total_mots'] > 0:
            print(f"Mot le plus long: {statistiques['mot_plus_long']} ({len(statistiques['mot_plus_long'])} lettres)")
            print(f"Mot le plus court: {statistiques['mot_plus_court']} ({len(statistiques['mot_plus_court'])} lettres)")
            print(f"Longueur moyenne: {statistiques['longueur_moyenne']:.1f} lettres")
            
            print(f"\n Répartition par catégories:")
            for categorie, nombre in statistiques['categories'].items():
                print(f"  • {categorie}: {nombre} mot(s)")
    
    def menu_afficher_plus_consultes(self):
        """Menu des mots les plus consultés"""
        plus_consultes = self.avancee.obtenir_mots_plus_consultes(10)
        
        if plus_consultes:
            print("\n MOTS LES PLUS CONSULTÉS:")
            print("-" * 30)
            for i, (mot, nombre) in enumerate(plus_consultes, 1):
                print(f"{i:2d}. {mot} ({nombre} consultation(s))")
        else:
            print(" Aucune consultation enregistrée.")
    
    def menu_filtrer_par_categorie(self):
        """Menu de filtrage par catégorie"""
        statistiques = self.avancee.obtenir_statistiques()
        categories = list(statistiques.get('categories', {}).keys())
        
        if not categories:
            print(" Aucune catégorie disponible!")
            return
        
        print(f"\n Catégories disponibles: {', '.join(categories)}")
        categorie = input("Entrez la catégorie à filtrer: ").strip()
        
        if not categorie:
            print(" Veuillez entrer une catégorie valide!")
            return
        
        mots = self.avancee.filtrer_par_categorie(categorie)
        if mots:
            print(f"\n {len(mots)} mot(s) dans la catégorie '{categorie}':")
            print("-" * 30)
            for mot in sorted(mots):
                print(f"• {mot}")
        else:
            print(f" Aucun mot dans la catégorie '{categorie}'.")
    
    def menu_exportation(self):
        """Menu d'exportation"""
        print("\n EXPORTATION:")
        print("1. Exporter en TXT")
        print("2. Exporter en CSV")
        
        choix = input("Votre choix (1-2): ").strip()
        
        if choix == '1':
            nom_fichier = input("Nom du fichier TXT (par défaut: exportation_dictionnaire.txt): ").strip()
            nom_fichier = nom_fichier or "exportation_dictionnaire.txt"
            if self.exportation.exporter_vers_txt(nom_fichier):
                print(f" Dictionnaire exporté vers {nom_fichier}")
            else:
                print(" Erreur lors de l'exportation!")
        
        elif choix == '2':
            nom_fichier = input("Nom du fichier CSV (par défaut: exportation_dictionnaire.csv): ").strip()
            nom_fichier = nom_fichier or "exportation_dictionnaire.csv"
            if self.exportation.exporter_vers_csv(nom_fichier):
                print(f" Dictionnaire exporté vers {nom_fichier}")
            else:
                print(" Erreur lors de l'exportation!")
        
        else:
            print(" Choix invalide!")
    
    def menu_jeux(self):
        """Menu des jeux"""
        print("\n JEUX:")
        print("1. Deviner le mot à partir de sa définition")
        print("2. Donner la définition d'un mot")
        
        choix = input("Votre choix (1-2): ").strip()
        
        if choix == '1':
            self.exportation.jeu_deviner_mot()
        elif choix == '2':
            self.exportation.jeu_deviner_definition()
        else:
            print(" Choix invalide!")
    
    def executer(self):
        """Lance l'application"""
        self.afficher_bienvenue()
        
        while True:
            self.afficher_menu()
            choix = input("Votre choix (0-13): ").strip()
            
            try:
                if choix == '0':
                    print(" Au revoir!")
                    self.stockage.sauvegarder_dictionnaire(self.noyau)
                    break
                elif choix == '1':
                    self.menu_rechercher_mot()
                elif choix == '2':
                    self.menu_ajouter_mot()
                elif choix == '3':
                    self.menu_modifier_mot()
                elif choix == '4':
                    self.menu_supprimer_mot()
                elif choix == '5':
                    self.menu_lister_mots()
                elif choix == '6':
                    self.menu_rechercher_definitions()
                elif choix == '7':
                    self.menu_rechercher_par_lettre()
                elif choix == '8':
                    self.menu_rechercher_par_sequence()
                elif choix == '9':
                    self.menu_afficher_statistiques()
                elif choix == '10':
                    self.menu_afficher_plus_consultes()
                elif choix == '11':
                    self.menu_filtrer_par_categorie()
                elif choix == '12':
                    self.menu_exportation()
                elif choix == '13':
                    self.menu_jeux()
                else:
                    print(" Choix invalide! Veuillez entrer un nombre entre 0 et 13.")
            
            except KeyboardInterrupt:
                print("\n\n Au revoir!")
                self.stockage.sauvegarder_dictionnaire(self.noyau)
                break
            except Exception as erreur:
                print(f" Une erreur est survenue: {erreur}")
            
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    application = InterfaceDictionnaire()
    application.executer()

