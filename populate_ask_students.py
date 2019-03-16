import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_students_project.settings')
import django

django.setup()

from ask_students.models import Category, Question, User, Answer, UserProfile, PlaceOfStudy, Permission


def populate():
    # Changed from list of dictionary to nested dictionary
    users = [{'username': 'YellowPony123', 'first_name': 'Abe', 'last_name': 'MacCabe',
              'password': 'pigsdontfly', 'bio': 'Lover of ponies and the colour yellow',
              'likes': 438, 'dislikes': 51},
             {'username': 'AngryTelephonePole87', 'first_name': 'Belle', 'last_name': 'MacKell',
              'password': 'BigF4TW1ndowL3dge', 'bio': 'Hate the world and I resonate with telephone poles :)',
              'likes': 331, 'dislikes': 29},
             {'username': 'ooeeooahahtingtang', 'first_name': 'Charlie', 'last_name': 'MacFarley',
              'password': 'wallawallabingbang', 'bio': 'Oo ee oo ah ah ting tang walla walla bing bang',
              'likes': 4, 'dislikes': 20},
             {'username': 'DampSeatOnTheBus', 'first_name': 'Doris', 'last_name': 'MacBoris',
              'password': 's4ndp4p3r', 'bio': 'Sitting on a damp seat on the bus could really ruin your day',
              'likes': 27, 'dislikes': 2},
             {'username': 'SweetEdna', 'first_name': 'Edna', 'last_name': 'MacScedna',
              'password': 'Edna', 'bio': 'Born 1942. Love to party.',
              'likes': 3, 'dislikes': 43},
             {'username': 'SeriousFred', 'first_name': 'Fred', 'last_name': 'MacSuede',
              'password': '18gsa35ds68', 'bio': 'Get real.',
              'likes': 754, 'dislikes': 40},
             {'username': 'GustySeagull1942', 'first_name': 'Gill', 'last_name': 'MacMill',
              'password': 'TROONBEACH', 'bio': 'Seagulls and seaweed is all that this gal needs',
              'likes': 3, 'dislikes': 85},
             {'username': 'HealthyLivingForAHealthyBeing', 'first_name': 'Harriot',
              'last_name': 'MacTarrot', 'password': 'carrot', 'bio': '#fitlife',
              'likes': 70, 'dislikes': 61},
             {'username': 'AintGotNoMoney', 'first_name': 'Isabelle',
              'last_name': 'MacDinnerBell', 'password': 'hahaha', 'bio': 'I only play the games that I win at',
              'likes': 3, 'dislikes': 0},
             ]

    for user in users:
        u = add_user(user['username'], user['first_name'], user['last_name'], user['password'])
        add_user_profile(u, user['bio'], user['likes'], user['dislikes'])

    place_of_study = ['University of St Andrews', 'University of Glasgow', 'University of Aberdeen',
                      'University of Edinburgh',
                      'University of Strathclyde', 'Heriot-Watt University', 'University of Dundee',
                      'Univeristy of Stirling',
                      'Edinburgh Napier University', 'Robert Gordon University', 'Glasgow Caledonian University',
                      'Queen Margaret University',
                      'Univesity of the West of Scotland', 'University of the Highlands and Islands']

    permission = ['Student', 'Undergraduate', 'Postgraduate']

    for place in place_of_study:
        add_place_of_study(place)

    for perm in permission:
        add_permission(perm)

    categories = {
        'General':
            {'description': 'Ask general questions about any topic you like',
             'approved': True,
             'questions':
                 [
                     {'name': "Who let the dogs out?",
                      "description": "who?",
                      "views": 10,
                      "answers":
                          [
                              {'answer': 'who?! who?! who?!', 'likes': 5, 'dislikes': 3,
                               'posted': None, 'edited': None, 'user': 'YellowPony123'},
                              {'answer': 'Baha Men', 'likes': 10, 'dislikes': 0,
                               'posted': None, 'edited': None, 'user': 'AngryTelephonePole87'},
                          ]
                      },
                     {'name': "What's brown and sticky?", "description": "serious answers only please.", "views": 30,
                      "answers":
                          [
                              {'answer': 'A brown sticker', 'likes': 4, 'dislikes': 20,
                               'posted': None, 'edited': None, 'user': 'ooeeooahahtingtang'},
                              {'answer': 'A stick', 'likes': 27, 'dislikes': 2,
                               'posted': None, 'edited': None, 'user': 'DampSeatOnTheBus'},
                              {'answer': 'How do I upload pictures to Facebook', 'likes': 0, 'dislikes': 23,
                               'posted': None, 'edited': None, 'user': 'SweetEdna'},
                          ]
                      }
                 ]
             },

        'Computing':
            {'description': 'Ask questions about Computing',
             'approved': True,
             'questions':
                 [
                     {'name': "What is the first index in an array",
                      "description": "I am trying to learn but no one is taking this question seriously",
                      "views": 120,
                      "answers":
                          [
                              {'answer': '0', 'likes': 70, 'dislikes': 15, 'posted': None, 'edited': None,
                               'user': 'SeriousFred'},
                              {'answer': '1', 'likes': 3, 'dislikes': 85, 'posted': None, 'edited': None,
                               'user': 'GustySeagull1942'},
                          ]
                      },
                     {'name': "How to fix wifi not working",
                      "description": "how to fix wifi not working",
                      "views": 750,
                      'answers':
                          [
                              {'answer': 'turn it off and turn it back on again', 'likes': 433, 'dislikes': 48,
                               'posted': None, 'edited': None, 'user': 'YellowPony123'},
                              {'answer': 'How to fix wifi not working', 'likes': 3, 'dislikes': 20, 'posted': None,
                               'edited': None, 'user': 'SweetEdna'},
                              {'answer': "This isn't really the right place to ask this question, "
                                         "try finding a better suited category or create one yourself.",
                               'likes': 683, 'dislikes': 24, 'posted': None,
                               'edited': None, 'user': 'SeriousFred'}
                          ]
                      },
                 ]
             },

        'Student Living General':
            {'description': 'General questions on Student Living',
             'approved': True,
             'questions':
                 [
                     {'name': "Where is a good place to eat out in Glasgow",
                      "description": "Looking for healthy organic food",
                      "views": 654,
                      'answers':
                          [
                              {'answer': 'McDonalds', 'likes': 70, 'dislikes': 61,
                               'posted': None, 'edited': None, 'user': 'HealthyLivingForAHealthyBeing'},
                              {'answer': 'BlueLagoon', 'likes': 321, 'dislikes': 29,
                               'posted': None, 'edited': None, 'user': 'AngryTelephonePole87'},
                          ]},
                     {'name': "Best non-alcoholic drink for students",
                      "description": "amazing!", "views": 12, 'answers':
                          [
                              {'answer': ' Water', 'likes': 3, 'dislikes': 0,
                               'posted': None, 'edited': None, 'user': 'AintGotNoMoney'},
                              {'answer': 'J20', 'likes': 1, 'dislikes': 1,
                               'posted': None, 'edited': None, 'user': 'SeriousFred'},
                          ]
                      }
                 ]
             }
    }

    for cat, cat_data in categories.items():
        c = add_category(cat, cat_data['description'], cat_data['approved'])
        print("Adding {0}...".format(str(c)))

        i = 0
        for question in cat_data['questions']:
            q = add_question(question['name'], question['description'], question['views'], c)
            i += 1
            for answer in question['answers']:
                username = answer['user']
                u = User.objects.get(username=username)
                up = UserProfile.objects.get(user=u)
                add_answer(cat, answer['answer'], answer['likes'], answer['dislikes'], up, q)

        print("  Adding {0} questions to {1}...".format(str(i), str(c)))


def add_place_of_study(title):
    p = PlaceOfStudy.objects.get_or_create(title=title)[0]
    p.save()
    return p


def add_permission(title):
    p = Permission.objects.get_or_create(title=title)[0]
    p.save()
    return p


def add_category(cat, description, approved):
    c = Category.objects.get_or_create(name=cat, description=description, approved=approved, user=None)[0]
    c.save()
    return c


def add_question(name, description, views, cat):
    q = Question.objects.get_or_create(name=name, text=description, category=cat, views=views)[0]
    q.save()
    return q


def add_user(username, first_name, last_name, password):
    u = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name)[0]
    u.set_password(password)
    u.save()
    return u


def add_user_profile(user, bio, likes, dislikes):
    up = UserProfile.objects.get_or_create(user=user, bio=bio, likes=likes, dislikes=dislikes)[0]
    up.save()
    return up


# takes a user profile
def add_answer(cat, answer, likes, dislikes, user, questiontop):
    c_id = Category.objects.get(name=cat)
    a = Answer.objects.get_or_create(category=c_id, text=answer, likes=likes, dislikes=dislikes, user=user
                                     , questiontop=questiontop)[0]
    a.save()
    return a


if __name__ == '__main__':
    print("Running ask_students population script...")

    import subprocess

    subprocess.check_call(['rm', 'db.sqlite3'])
    subprocess.check_call(['python', 'manage.py', 'makemigrations', 'ask_students'])
    subprocess.check_call(['python', 'manage.py', 'migrate'])

    populate()
