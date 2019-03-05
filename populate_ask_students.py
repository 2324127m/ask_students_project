import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_students_project.settings')
import django

django.setup()

from ask_students.models import Category, Question


def populate():
    categories = {'General': {'description': 'Ask general questions about any topic you like',
                              'approved': True,
                              'questions': [
                                  {'name': "My First Question has 10 views", "description": "this works?", "views": 10},
                                  {'name': "My Second Question has 30 views", "description": "yes it does!",
                                   "views": 30}
                              ]},
                  'Computing': {'description': 'Ask questions about Computing',
                                'approved': True,
                                'questions': [
                                    {'name': "My Third Question has 20 views", "description": "but does it really?",
                                     "views": 20},
                                    {'name': "My Fourth Question has 750 views", "description": "amazing!",
                                     "views": 750}
                                ]},
                  'Mo Category': {'description': 'Ask questions about Mo',
                                  'approved': True,
                                  'questions': [
                                      {'name': "My Third Question has 20 views", "description": "but does it really?",
                                       "views": 20},
                                      {'name': "My Fourth Question has 750 views", "description": "amazing!",
                                       "views": 750}
                                  ]}
                  }

    for cat, cat_data in categories.items():
        c = add_category(cat, cat_data['description'], cat_data['approved'])
        print("Adding {0}...".format(str(c)))

        i = 0
        for question in cat_data['questions']:
            add_question(question['name'], question['description'], question['views'], c)
            i += 1

        print("  Adding {0} questions to {1}...".format(str(i), str(c)))


def add_category(cat, description, approved):
    c = Category.objects.get_or_create(name=cat, description=description, approved=approved, user=None)[0]
    c.save()
    return c


def add_question(name, description, views, cat):
    c = Question.objects.get_or_create(name=name, text=description, category=cat, views=views)[0]
    c.save()
    return c


if __name__ == '__main__':
    print("Running ask_students population script...")
    populate()
