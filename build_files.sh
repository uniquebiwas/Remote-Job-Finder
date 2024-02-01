# Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 manage.py makemigrations 
python3.9 manage.py migrate 

# echo "Collect Static..."
python3.9 manage.py collectstatic --noinput


echo "Collecting Media Files..."
python3.9 manage.py collectstatic --noinput --ignore=*.js,*.css,*.scss,*.html,*.txt
