# P9 – Lead a Data Project: Les Derniers Flocons ❄️

### Analyse climatique & prédiction de fermeture des stations de ski alpines

---

## 📌 Présentation du projet

**Les Derniers Flocons** est une application permettant d’anticiper l’impact du changement climatique sur les stations de ski des Alpes françaises.  
Elle s'appuie sur plus de cinquante ans de données météorologiques (1970–2024) et sur plusieurs modèles statistiques pour :

- analyser l’évolution des chutes de neige et des températures,
- identifier les tendances climatiques selon l’altitude,
- prédire l’évolution future des paramètres climatiques,
- estimer le risque de fermeture de chaque station dans le temps.

L’application est destinée aux **professionnels de la montagne**, aux **décideurs publics**, ainsi qu’à toute personne souhaitant comprendre l’avenir des stations alpines.

---

## 🔗 Application déployée

👉 **Accéder à l'application Streamlit :**  
https://andreea73-les-derniers-flocons.hf.space/

---

## 📊 Données utilisées

### **1. Données météo (Open-Meteo API)**
- 148 stations situées dans les Alpes françaises  
- Données journalières de **1970 à 2024**  
- Variables intégrées :
  - température moyenne de l’air  
  - température du sol (0 à -100 cm)  
  - cumul des chutes de neige  
  - équivalent en eau des chutes de neige  
  - cumul des précipitations pluvieuses  
  - durée d’ensoleillement  
  - vitesse moyenne du vent  
  - couverture nuageuse  

### **2. Données stations**
- Scraping initial pour récupérer :
  - nom des stations  
  - coordonnées GPS  
  - altitudes  
- Vérifications et corrections manuelles  
- Ajout des stations **définitivement fermées**, avec leur date de fermeture

---

## 🛠️ Méthodologie

### **1. Exploration & Visualisation**
Analyse station par station :  
- tendances de température  
- tendances de neige  
- comportements climatiques par altitude  
- comparaison entre régions

### **2. Modélisation avec Prophet**
Prévisions à 5 ans :  
- des températures moyennes annuelles  
- des cumuls neigeux  
Découpage par tranches d’altitude :  
- < 1000 m  
- 1000–1300 m  
- 1300–1600 m  
- > 1600 m  

### **3. Analyse de survie (Survival Analysis)**
Objectif : estimer la **probabilité de fermeture** d’une station dans le temps.  
Résultats :
- courbes de survie par station  
- comparaison visuelle entre stations  
- estimation du “moment critique” selon les données historiques

---

## 🧩 Fonctionnalités de l’application

### **🏠 Accueil**
- Carte interactive des stations de ski  
- Présentation du projet

### **ℹ️ À Propos**
- Contexte du projet  
- Méthodologie globale  
- Visual simplifié des données  
- Photos illustratives

### **📊 Visualisation des Données Météo**
- Températures annuelles  
- Précipitations pluie/neige  
- Cumuls neige par saison  
- Interprétations des graphiques

### **📈 Tendances Météorologiques**
Prévisions Prophet par altitude :
- neige cumulée  
- températures moyennes  
avec interprétations pour chaque tranche.

### **🌨️ Ma Station**
- Sélection d’une station spécifique  
- Prévisions personnalisées neige & température  
- Interprétation 

### **🔍 Stations à Risques**
- Modèle de survie  
- Courbes de survie interactives  
- Sélection de stations pour comparaison

---

## 📁 Structure du projet

```
les_derniers_flocons/
│
├── src/
│   ├── streamlit_app.py          # Code principal de l'application Streamlit
│   ├── donnees_meteo_148_stations.csv
│   ├── donnees_meteo_avec_stations_et_altitudes_full.csv
│   ├── df_combined_cox_results.csv
│   ├── image1.png
│   ├── image2.png
│   └── image3.png
│
├── requirements.txt               # Dépendances Python
└── README.md                      # Documentation du projet
```

## 🤝 Équipe

Projet réalisé dans le cadre de la formation Data Science (Jedha) par :  
- **Ambre TRAN**  
- **Andreea LOUISON**  
- **Mathilde REJASSE**  
- **Nicolas Saad FORTUIT**

