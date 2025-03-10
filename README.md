### **🚀 README.md pour ton projet d'authentification JWT avec Flask & JavaScript**  

Crée un fichier `README.md` à la racine de ton projet et ajoute ce contenu :  

---


# 🔐 Authentification JWT avec Flask & JavaScript

Ce projet met en place une **authentification sécurisée** avec **JWT (JSON Web Token)** en utilisant **Flask** pour le backend et **JavaScript, HTML, CSS** pour le frontend.  
L'objectif est de **gérer l'authentification sans stocker les tokens dans `localStorage`**, en utilisant des **cookies `HttpOnly` sécurisés**.  

---

## 🎯 **Fonctionnalités**
✔️ **Création d'un compte utilisateur** 📌  
✔️ **Connexion avec génération de tokens (`access_token` & `refresh_token`)** 🔐  
✔️ **Stockage sécurisé des tokens via `HttpOnly Cookies`** 🍪  
✔️ **Accès aux routes protégées sans envoyer le token dans les headers** 🔒  
✔️ **Rafraîchissement automatique du `access_token` en cas d'expiration** 🔄  
✔️ **Déconnexion avec suppression des tokens** 🚪  

---

## 🛠 **Technologies utilisées**
### **Backend (Flask)**
- 🐍 Flask (Micro-framework Python)
- 🔑 Flask-JWT (pour la gestion des tokens JWT)
- 📦 Flask-SQLAlchemy (pour la gestion de la base de données)
- 🛠️ flask_bcrypt (pour le hachage des mots de passe)

### **Frontend**
- 🌐 HTML, CSS (interface utilisateur)
- ⚡ JavaScript (gestion de l'authentification et des requêtes API)
- 🎨 Bootstrap (pour le design responsive)

---

## 🔧 **Installation et exécution**
### **1️⃣ Cloner le projet**
```bash
git clone https://github.com/ton-nom-utilisateur/auth-jwt-flask.git
cd auth-jwt-flask


### **2️⃣ Créer un environnement virtuel et installer les dépendances**
```bash
python -m venv venv  # Crée un environnement virtuel
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate  # (Windows)
pip install -r requirements.txt  # Installe les dépendances
```

### **3️⃣ Configurer la base de données**
```bash
flask run
```
Le serveur sera accessible sur **`http://127.0.0.1:5000`** 🚀

---

## 🔑 **Utilisation de l'authentification**
### **1️⃣ Inscription**
- **Route :** `POST /register`
- **Données :**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "123456"
}
```
- **Réponse :**  
```json
{
  "message": "Utilisateur créé avec succès"
}
```

### **2️⃣ Connexion**
- **Route :** `POST /login`
- **Données :**
```json
{
  "email": "test@example.com",
  "password": "123456"
}
```
- **Réponse :**
```json
{
  "message": "Connexion réussie"
}
```
🔹 **Les tokens (`access_token`, `refresh_token`) sont stockés dans des cookies `HttpOnly` automatiquement.**

### **3️⃣ Accéder à une page protégée**
- **Route :** `GET /dashboard`
- **Fonctionnement :**  
  ✅ Pas besoin d'envoyer le token dans les headers ! Flask le récupère depuis le cookie automatiquement.  
- **Réponse en cas de succès :**  
```json
{
  "message": "Bienvenue sur votre dashboard, utilisateur X"
}
```
- **Réponse si l'utilisateur n'est pas connecté :**
```json
{
  "message": "Token is missing"
}
```

### **4️⃣ Rafraîchir automatiquement le `access_token`**
- **Si le `access_token` expire**, Flask le **renouvelle automatiquement avec le `refresh_token`**, sans que l'utilisateur s'en rende compte.

### **5️⃣ Déconnexion**
- **Route :** `POST /logout`
- **Action :** Supprime les tokens et empêche l'accès aux pages protégées.
- **Réponse :**
```json
{
  "message": "Déconnexion réussie"
}
```

---

## 📁 **Arborescence du projet**
```
auth-jwt-flask/
│
│   ├── models.py         # Définition des modèles (User, Token)
│   ├── auth_service.py         # fontion d'authentification
│   ├── main_routes.py         # Routes API page(login,register,dashboad)
│   ├── auth_routes.py         # Routes API (authentification)
│   ├── main.py       # Configuration Flask
│
│── templates/
│   ├── login.html        # Page de connexion
│   ├── register.html     # Page d'inscription
│   ├── dashboard.html    # Page protégée
│
│── static/
    │── assets/
│     ├── css/              # Fichiers CSS
│     ├── js/               # Fichiers JavaScript
│

│── config.py             # Fichier de configuration (SECRET_KEY, DB, etc.) Vous devez créer le votre
│── requirements.txt      # Dépendances du projet
│── run.py                # Point d'entrée de l'application Flask
│── README.md             # Documentation du projet
```

---

## 💡 **Améliorations possibles**
✅ **Ajout d'un système de rôles (Admin, Utilisateur)**  
✅ **Limiter l'accès à certaines pages selon le rôle**  
✅ **Gérer les tentatives de connexion incorrectes (brute force protection)**  
✅ **Ajouter un système d'activation par email (avec Flask-Mail)**  
✅ **Intégration avec une base de données plus robuste (PostgreSQL)**  
✅ **Créer une version avec un frontend moderne (React, Vue, ou Angular)**  

---

## 🛠 **Problèmes et corrections**
Si tu rencontres des erreurs, voici quelques solutions :  
### **🔹 "Token is missing"**
➡ **Vérifie que les cookies sont bien envoyés dans les requêtes.**  
➡ **Utilise `credentials: "include"` dans `fetch()` côté frontend.**  

### **🔹 "Signature has expired"**
➡ **Vérifie que `refresh_token` est bien utilisé pour renouveler l'`access_token`.**  
➡ **Augmente la durée d'expiration dans `generate_token()`.**  

### **🔹 "Invalid token"**
➡ **Vérifie que le `SECRET_KEY` est identique partout (backend & frontend).**  
➡ **Ne modifie pas un token manuellement.**  

---

## 🎯 **Contribuer**
Tu veux améliorer ce projet ? **Forke-le, améliore-le et propose un `Pull Request` !**  
Tout retour ou amélioration est le bienvenu. 🚀

---

## 📜 **Licence**
Ce projet est sous licence **MIT**. Tu peux l'utiliser librement et le modifier à ta guise.

---

### **🚀 Merci d'avoir exploré ce projet !**
Si ce projet t’a aidé, **n’oublie pas de laisser une ⭐ sur GitHub !** 😃🔥  
```
