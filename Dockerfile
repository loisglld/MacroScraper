# Étape 1 : Utiliser une image Python officielle comme image de base
FROM python:3.11

# Étape 2 : Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3 : Copier le code de votre projet dans le conteneur
COPY . .

# Étape 4 : Installer les dépendances de votre projet
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Définir le point d'entrée de votre application
CMD [ "python", "./Main.py" ]
