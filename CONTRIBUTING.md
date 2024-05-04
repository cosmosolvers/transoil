# CONTRIBUTING

## Install

1. update your system
   ```bash
      hydromel@thinkpad:~$ sudo apt update
   ```
2. create working directory
   ```bash
      hydromel@thinkpad:~$ mkdir cosmosolvers && cd cosmosolvers
      hydromel@thinkpad:~/cosmosolvers$
   ```
3. Clone project
   ```bash
      hydromel@thinkpad:~/cosmosolvers$ git clone https://github.com/cosmosolvers/transoil.git
   ```
4. create virtual environment<br>
   for windows
   ```bash
      hydromel@thinkpad:~/cosmosolvers$ python -m venv env
   ```
   for linux and mac
   ```bash
      hydromel@thinkpad:~/cosmosolvers$ python3 -m venv env
      or
      hydromel@thinkpad:~/cosmosolvers$ virtualenv env (in linux)
   ```
5. active your virtual environment<br>
   for windows
   ```bash
      hydromel@thinkpad:~/cosmosolvers$ env\Scripts\activate
      (env) hydromel@thinkpad:~/cosmosolvers$
   ```
   for linux and mac
   ```bash
      hydromel@thinkpad:~/cosmosolvers$ source env/bin/activate
      or
      hydromel@thinkpad:~/cosmosolvers$ . env/bin/activate
      (env) hydromel@thinkpad:~/cosmosolvers$
   ```
6. Install project dependance
   ```bash
      (env) hydromel@thinkpad:~/cosmosolvers$ cd transoil
      (env) hydromel@thinkpad:~/cosmosolvers/transoil$ pip install -r requirements.txt
   ```
## Configuration

1. Créez un fichier `.env` à la racine du projet et ajoutez les variables 
d'environnement nécessaires. Consultez le fichier `.env.example` pour savoir les variables nécessaires.

Pour générer une DJANGO_SECRET_KEY avec Python, vous pouvez utiliser la bibliothèque `secrets`. Pour ce faire, exécutez la commande suivante dans votre terminal :

```python
python -c 'import secrets; print(secrets.token_urlsafe())'  # génération d'une SECRET_KEY avec Python
```
La variable DJANGO_DEBUG : Peut prendre en compte une valeur booléenne "True" or "False" 

La variable DJANGO_ALLOWED_HOSTS : correspond à la liste des hôtes autorisés séparés par des virgules.

Toutes les variables contenu dans la section *database postgres settings* correspondent aux données de votre base de donnée crée.

Toutes les variables contenu respectivement dans la section *jwt settings*, *cinetpay settings*, et *superuser settings* correspondent aux données de configuration de jwt, cinetpay et de superuser.

2. Exécutez les migrations en utilisant la commande suivante :

```python
# Génération des fichiers de migration
python manage.py makemigrations 
```

# Application des migrations en attente à la base de données 
python manage.py migrate

3. Lancez le serveur de développement en utilisant la commande suivante en precisant la configuration à utiliser :

```python
#Lancez le serveur de développement en utilisant la commande suivante :
python manage.py runserver
```
