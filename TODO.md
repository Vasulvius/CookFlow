# 📌 Cahier des charges – CookFlow  

## ✅ 1. Présentation du projet  
- **Nom de l'application** : CookFlow  
- **Technologies principales** : FastAPI (backend), Streamlit (frontend)  
- **Objectif** : Application de gestion de repas permettant de :  
  - [ ] Trouver des recettes selon les ingrédients disponibles  
  - [ ] Enregistrer des préférences  
  - [ ] Planifier des repas  
  - [ ] Générer une liste de courses  

---

## 🍽 2. Fonctionnalités principales  

### **2.1. Gestion des ingrédients**  
- [ ] Ajouter des ingrédients à la base de données  
- [ ] Décrire les ingrédients disponibles dans son frigo/placard  
- [ ] Associer des ingrédients à des catégories (viande, légumes, épices, etc.)  

### **2.2. Gestion des recettes**  
- [ ] Ajouter des recettes avec une liste d’ingrédients et instructions  
- [ ] Trouver des recettes en fonction des ingrédients disponibles  
- [ ] Filtrer les recettes par catégorie (végétarien, rapide, économique, etc.)  
- [ ] Noter et commenter les recettes  

### **2.3. Préférences utilisateur**  
- [ ] Enregistrer ses plats préférés  
- [ ] Exclure certains ingrédients (allergies, goûts personnels)  
- [ ] Personnaliser les suggestions de recettes  

### **2.4. Planification des repas**  
- [ ] Planifier ses repas sur une semaine  
- [ ] Générer un planning interactif et modifiable  
- [ ] Ajouter des recettes planifiées à une liste de courses automatique  

### **2.5. Liste de courses**  
- [ ] Générer une liste de courses en fonction des repas planifiés  
- [ ] Regrouper les ingrédients par catégorie (ex : fruits/légumes, épicerie, etc.)  
- [ ] Modifier et personnaliser la liste avant export  

---

## 🏗 3. Architecture technique  

### **3.1. Backend (FastAPI)**  
- [ ] Base de données relationnelle (PostgreSQL ou SQLite)  
- [ ] API REST pour la gestion des utilisateurs, ingrédients, recettes et planification  
- [ ] Système d’authentification (optionnel)  

### **3.2. Frontend (Streamlit)**  
- [ ] Interface utilisateur intuitive pour interagir avec l’API  
- [ ] Formulaires pour ajouter/modifier recettes et ingrédients  
- [ ] Tableaux et visualisations pour la planification des repas  

---

## 🔮 4. Contraintes et évolutions possibles  
- [ ] Import/export de recettes (JSON, CSV)  
- [ ] Mode collaboratif (partage de listes de courses, recommandations entre amis)  
- [ ] Intégration avec une API externe de recettes  
