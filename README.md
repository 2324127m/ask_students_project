# Ask Students

1. Introduction

2. Installation

   1. Setup Environment

   2. Install Dependencies

   3. Create and Populate Database

      

1. ## Introduction

   Ask Students is a web app developed using Django for the purpose of allowing university and college staff and students to ask and answer each others questions. The site can be viewed publically, but contributing to discussions, creating categories or asking a new question requires visitor to register an account.

   

2. ## Installation

   1. ### Setup Environment

      It may be advisable, especially when further developing application to use a virtual environment. One such method of doing this is to use Anaconda.

      After setting up you desired virtual or system environment move onto installing Ask Students dependencies

      

   2. ### Install Dependencies

      Open the command line or terminal under you desired environment and navigate to the ask_student_project folder and run.

      `pip install -r requirements.txt`

      Alternatively, open the file in a text editor and install manually using pip.

   3. ### Create and Populate Database

      To create the migration scripts to set up the initial models run

      `python manage.py makemigrations ask_students`

      followed by

      `python manage.py migrate`

      to create the database file and define the schemea using the previously created migration scripts.

      ***Optionally*** *You can choose to populate the database with some initial dummy users, questions, answers, etc for testing or other development purposes.*

      

      

      

   1. ### 