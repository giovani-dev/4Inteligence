echo "Generate migrations"
python manage.py makemigrations

echo "Appling migrations"
python manage.py migrate

echo "Loadding user"
python manage.py loaddata user.json