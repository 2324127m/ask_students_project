# Ask Students

1. ## Introduction

   Ask Students is a web app developed using Django for the purpose of allowing university and college staff and students to ask and answer each others questions. The site can be viewed publically, but contributing to discussions, creating categories or asking a new question requires visitor to register an account.

   1. ### Demo App

      We have a demo of our site available for you to experiment on at:

      [Python Anywhere]: http://2324127m.pythonanywhere.com
      [Python Anywhere](http://2324127m.pythonanywhere.com)

2. ## Installation

   1. ### Setup Environment

      It may be advisable, especially when further developing application to use a virtual environment. One such method of doing this is to use Anaconda.

      After setting up you desired virtual or system environment move onto installing Ask Students dependencies

      

   2. ### Install Dependencies

      Open the command line or terminal under you desired environment and navigate to the ask_student_project folder and run.

      `pip install -r requirements.txt`

      Alternatively, open the file in a text editor and install the dependencies listed in the requirements.txt file manually or using pip.

   3. ### Create and Populate Database

      To create the migration scripts to set up the initial models run

      `python manage.py makemigrations ask_students`

      followed by

      `python manage.py migrate`

      Also, for convienence, we have created a utility script which will create the migrations files and migrate the database in one step.

      You can utilise this functionality by running:

      `python clean_migrate_run.py`

      Now we can populate the database with initial values.

      `python populate_ask_students.py`

      Will generate some users, categories, questions and answers, and will give you the option in the terminal to create a super user, which can be helpful for development.

       ***It is not recommended for security reasons to create this super user in production environment***

   4. ### Additional Information about Population Script

      In the population script we have created demo users for testing and demonstration purposes.
      
      Listed below are the details for two of these users, if you wish to log in without creating a new account
      
      USERNAME: YellowPony123   PASSWORD: pigsdontfly
      
      USERNAME: HealthyBeing    PASSWORD: carrot

3. ## External Sources
      We used a number of external sources for the making of this web application:
      - BootStrap 4
      - jQuery 
      - jQuery Validate
      - jQuery UI
      - Django Registration Redux
      - Google reCAPTCHA
