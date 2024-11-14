#!/bin/bash

# Attendre que la base de données soit prête (si vous utilisez PostgreSQL)
#while ! nc -z db 5432; do
#    echo "En attente de la base de données..."
#    sleep 1
#done

# Effectuer les migrations

# sleep 3
# python manage.py makemigrations
# python manage.py migrate

# # Démarrer le serveur
# python manage.py runserver 0.0.0.0:8000
echo "Début du script entrypoint.sh"
sleep infinity