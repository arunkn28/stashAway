Prerequisites:
1) Python 3.7 is installed

To run the project in local follow the below steps:
Run command ->
pip install requirements.txt
python manage.py makemigrations
python manage.py migrate

HIT below url in a browser:
localhost:8000/workflows/worflows

This will list approval pending workflows

On the same screen you will get a form to submit a new approval

To change the status of an approval hit
localhost:8000/workflows/worflows/<workflow_id>

The screen will show the current status of the workflow as well as a form
to change the status