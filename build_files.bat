@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Running collectstatic...
python manage.py collectstatic --noinput

echo Done!
