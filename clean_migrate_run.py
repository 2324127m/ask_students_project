import os, subprocess, platform
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_students_project.settings')
import django

django.setup()

from ask_students.models import User, UserProfile

# Delete old database and make new migrations
def clean_db():
    if platform.system() == "Windows":
        subprocess.call(['del', 'db.sqlite3'], shell=True)
    else:
        subprocess.call(['rm', 'db.sqlite3'])

    subprocess.call(['python', 'manage.py', 'makemigrations', 'ask_students'])
    subprocess.call(['python', 'manage.py', 'migrate'])



# Run the server
def run_server():
    print()
    run = input("would you like to run the server? (y/n): ")
    if run == "y":
        subprocess.call(['python', 'manage.py', 'runserver'])


if __name__ == '__main__':
    print("\nCleaning old database...\n")
    clean_db()
    # run_server()