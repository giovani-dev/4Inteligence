echo "Generate migrations"
python manage.py makemigrations

echo "Appling migrations"
python manage.py migrate