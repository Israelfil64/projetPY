#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJET: DICTIONNAIRE DE MOTS EN PYTHON
======================================

Ce programme implémente un dictionnaire interactif complet avec:
- Gestion CRUD (Créer, Lire, Modifier, Supprimer) des mots
- Recherche avancée et statistiques
- Persistance des données en JSON
- Exportation en TXT/CSV
- Jeux interactifs
- Interface utilisateur en ligne de commande

Modules:
- noyau_dictionnaire.py: Gestion des mots en mémoire
- stockage_donnees.py: Persistance des données
- fonctionnalites_avancees.py: Recherche et statistiques
- exportation_bonus.py: Exportation et jeux
- interface_principale.py: Interface utilisateur CLI

Auteur: Équipe de développement
Date: 2025
"""

from interface_principale import InterfaceDictionnaire

def main():
    """Fonction principale du programme"""
    print("🚀 Démarrage du Dictionnaire Interactif Python...")
    
    try:
        # Créer et lancer l'application
        application = InterfaceDictionnaire()
        application.executer()
    
    except KeyboardInterrupt:
        print("\n\n👋 Programme interrompu par l'utilisateur. Au revoir!")
    
    except Exception as erreur:
        print(f"\n❌ Erreur critique: {erreur}")
        print("Le programme va se fermer.")
    
    finally:
        print("🏁 Fin du programme.")

if __name__ == "__main__":
    main()

