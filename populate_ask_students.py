import os, subprocess, platform

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_students_project.settings')
import django

django.setup()

from ask_students.models import Category, Question, User, Answer, UserProfile, PlaceOfStudy, Permission


def populate():
    # Populate place of study with all universities in Scotland
    place_of_study = ['University of St Andrews', 'University of Glasgow', 'University of Aberdeen',
                      'University of Edinburgh',
                      'University of Strathclyde', 'Heriot-Watt University', 'University of Dundee',
                      'Univeristy of Stirling',
                      'Edinburgh Napier University', 'Robert Gordon University', 'Glasgow Caledonian University',
                      'Queen Margaret University',
                      'University of the West of Scotland', 'University of the Highlands and Islands']

    # Populate permissions with different roles a user can have
    permission = ['Student', 'Undergraduate', 'Postgraduate']

    for place in place_of_study:
        add_place_of_study(place)

    for perm in permission:
        add_permission(perm)

    # Populate users with 9 sample users
    users = [{'username': 'YellowPony123', 'first_name': 'Abe', 'last_name': 'MacCabe', 'email': 'yellowpony123@gmail.com',
              'password': 'pigsdontfly', 'bio': 'Lover of ponies and the colour yellow', 'image': 'profile_images/YellowPony123.jpg',
              'likes': 598, 'dislikes': 82, 'permission': 'Student', 'place_of_study': "University of Glasgow"},
             {'username': 'AngryTelephonePole87', 'first_name': 'Belle', 'last_name': 'MacKell', 'email': 'angry@theworld.com',
              'password': 'BigF4TW1ndowL3dge', 'bio': 'Hate the world and I resonate with telephone poles :)', 'image': 'profile_images/AngryTelephonePole87.jpg',
              'likes': 379, 'dislikes': 41, 'permission': 'Student', 'place_of_study': 'University of Glasgow'},
             {'username': 'ooeeooahahtingtang', 'first_name': 'Charlie', 'last_name': 'MacFarley', 'email': 'qwertyuip@yahoo.co.uk',
              'password': 'wallawallabingbang', 'bio': 'Oo ee oo ah ah ting tang walla walla bing bang',
              'likes': 91, 'dislikes': 37, 'permission': 'Undergraduate', 'place_of_study': 'Glasgow Caledonian University'},
             {'username': 'DampSeatOnTheBus', 'first_name': 'Doris', 'last_name': 'MacBoris', 'email': 'doris.macboris@gmail.com',
              'password': 's4ndp4p3r', 'bio': 'Sitting on a damp seat on the bus could really ruin your day',
              'likes': 47, 'dislikes': 5, 'permission': 'Postgraduate', 'place_of_study': 'Univeristy of Stirling'},
             {'username': 'SweetEdna', 'first_name': 'Edna', 'last_name': 'MacScedna', 'email': 'edna@aol.com',
              'password': 'Edna', 'bio': 'Born 1942. Love to party.',
              'likes': 20, 'dislikes': 44, 'permission': 'Postgraduate', 'place_of_study': 'University of the Highlands and Islands'},
             {'username': 'SeriousFred', 'first_name': 'Fred', 'last_name': 'MacSuede', 'email': 'fred_mascsuede@hotmail.com',
              'password': '18gsa35ds68', 'bio': 'Get real.',
              'likes': 830, 'dislikes': 66, 'permission': 'Student', 'place_of_study': 'Edinburgh Napier University'},
             {'username': 'GustySeagull1942', 'first_name': 'Gill', 'last_name': 'MacMill', 'email': 'mrsmacmill@gmail.com',
              'password': 'TROONBEACH', 'bio': 'Seagulls and seaweed is all that this gal needs', 'image': 'profile_images/GustySeagull1942.jpg',
              'likes': 111, 'dislikes': 105, 'permission': 'Undergraduate', 'place_of_study': 'Robert Gordon University'},
             {'username': 'HealthyLivingForAHealthyBeing', 'first_name': 'Harriot', 'last_name': 'MacTarrot', 'email': 'harriot_mactarrot@yahoo.co.uk',
              'password': 'carrot', 'bio': '#fitlife',
              'likes': 176, 'dislikes': 86, 'permission': 'Student', 'place_of_study': 'University of Glasgow'},
             {'username': 'AintGotNoMoney', 'first_name': 'Isabelle', 'last_name': 'MacDinnerBell', 'email': 'dinner_bell@gmail.com',
              'password': 'hahaha', 'bio': 'I only play the games that I win at', 'image': 'profile_images/AintGotNoMoney.png',
              'likes': 119, 'dislikes': 26, 'permission': 'Undergraduate', 'place_of_study': 'University of the West of Scotland'},
             ]

    for user in users:
        u = add_user(user['username'], user['first_name'], user['last_name'], user['password'], user['email'])
        if len(user) == 11:
            add_user_profile(u, user['bio'], user['likes'], user['dislikes'], user['permission'], user['place_of_study'], user['image'])
        else:
            add_user_profile(u, user['bio'], user['likes'], user['dislikes'], user['permission'], user['place_of_study'])

    
    categories = {
        'General':
            {'description': 'Ask general questions about any topic you like',
             'approved': True,
             'questions':
                 [
                     {'name': "Who let the dogs out?",
                      "description": "who?",
                      "views": 10,
                      "user": "YellowPony123",
                      "support_file": "support_files/who-let-them-out.jpg",
                      "answers":
                         [
                             {'answer': 'who?! who?! who?!', 'likes': 5, 'dislikes': 3,
                              'posted': None, 'edited': None, 'user': 'YellowPony123'},
                             {'answer': 'Baha Men', 'likes': 10, 'dislikes': 0,
                              'posted': None, 'edited': None, 'user': 'AngryTelephonePole87'},
                             {'answer': 'I did', 'likes': 8, 'dislikes': 5,
                              'posted': None, 'edited': None, 'user': 'GustySeagull1942'},
                         ]
                      },
                     {'name': "What's brown and sticky?",
                      "description": "serious answers only please.",
                      "views": 30,
                      "user": "AngryTelephonePole87",
                      "answers":
                         [
                             {'answer':'A brown sticker', 'likes':4, 'dislikes':20,
                              'posted': None, 'edited': None, 'user': 'ooeeooahahtingtang'},
                             {'answer':'A stick', 'likes':27, 'dislikes':2,
                              'posted': None, 'edited': None, 'user': 'DampSeatOnTheBus' },
                             {'answer':'How do I upload pictures to Facebook', 'likes':0, 'dislikes': 23,
                              'posted': None, 'edited': None, 'user' : 'SweetEdna'},
                         ]
                      },
                     {'name': "This is a really really long question title so we can see what it looks like!",
                      "description": "I really need ideas on what to have for dinner",
                      "views": 180000,
                      "user": "ooeeooahahtingtang",
                      "support_file": "support_files/hungry.jpg",
                      "answers":
                         [
                             {'answer': 'Ravioli', 'likes': 5, 'dislikes': 3,
                              'posted': None, 'edited': None, 'user': 'DampSeatOnTheBus'},
                             {'answer': 'Order a Chinese', 'likes': 40, 'dislikes': 7,
                              'posted': None, 'edited': None, 'user': 'YellowPony123'},
                             {'answer': 'Roast Beef', 'likes': 12, 'dislikes': 3,
                              'posted': None, 'edited': None, 'user': 'GustySeagull1942'},
                             {'answer': 'Got to be pizza', 'likes': 19, 'dislikes': 2,
                              'posted': None, 'edited': None, 'user': 'AintGotNoMoney'},
                         ]
                      },
                      {'name': "Who wrote Around the World in 80 Days?",
                      "description": "I need to know for an essay I'm writing",
                      "views": 40,
                      "user": "GustySeagull1942",
                      "answers":
                         [
                             {'answer':'Jules Verne', 'likes':12, 'dislikes':0,
                              'posted': None, 'edited': None, 'user': 'SeriousFred'},
                             {'answer':'Why didn\'t you just google this?' , 'likes':35, 'dislikes':1,
                              'posted': None, 'edited': None, 'user': 'YellowPony123' },
                        ]
                    },
                     {'name': "What is this website all about?",
                      "description": "I'm seriously confused",
                      "views": 60,
                      "user": "SweetEdna",
                      "answers":
                         [
                             {'answer': 'Just click about on the bar at the bottom of the page', 'likes': 13, 'dislikes': 3,
                              'posted': None, 'edited': None, 'user': 'HealthyLivingForAHealthyBeing'},
                             {'answer': 'Its for students to ask questions, obviously', 'likes':22, 'dislikes': 7,
                              'posted': None, 'edited': None, 'user': 'YellowPony123'},
                             {'answer': 'Nobody knows for sure', 'likes': 10, 'dislikes': 10,
                              'posted': None, 'edited': None, 'user': 'AngryTelephonePole87'},
                         ]
                      },
                     {'name': "Where is everyone from",
                      "description": "Just interested",
                      "views": 463,
                      "user": "SeriousFred",
                      "answers":
                         [
                             {'answer': 'SCOTLAND', 'likes': 88, 'dislikes': 12,
                              'posted': None, 'edited': None, 'user': 'GustySeagull1942'},
                             {'answer': 'Im from Glasgow', 'likes': 44, 'dislikes': 15,
                              'posted': None, 'edited': None, 'user': 'YellowPony123'},
                             {'answer': 'I was born in Oban, moved to Edinburgh, and now stay in Inverness', 'likes': 12, 'dislikes': 0,
                              'posted': None, 'edited': None, 'user': 'SweetEdna'},
                             {'answer': 'Bosnia', 'likes': 19, 'dislikes': 2,
                              'posted': None, 'edited': None, 'user': 'ooeeooahahtingtang'},
                             {'answer': 'A wee town in Ayrshire', 'likes': 38, 'dislikes': 2,
                              'posted': None, 'edited': None, 'user': 'AngryTelephonePole87'},
                         ]
                      },

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
                      "user": "DampSeatOnTheBus",
                      "support_file": "support_files/array.jpg",
                      "answers":
                          [
                              {'answer':'0', 'likes': 70, 'dislikes':15, 'posted': None, 'edited': None, 'user': 'SeriousFred'},
                              {'answer':'1', 'likes':3, 'dislikes': 85, 'posted': None, 'edited': None, 'user': 'GustySeagull1942'},
                          ]
                      },
                     {'name': "How to fix wifi not working",
                      "description": "how to fix wifi not working",
                      "views": 750,
                      "user": "YellowPony123",
                      'answers':
                         [
                             {'answer':'turn it off and turn it back on again', 'likes': 433, 'dislikes': 48, 'posted': None, 'edited': None, 'user': 'YellowPony123'},
                             {'answer':'How to fix wifi not working', 'likes': 3, 'dislikes': 20, 'posted': None, 'edited': None, 'user': 'SweetEdna'},
                             {'answer':"This isn't really the right place to ask this question, "
                                       "try finding a better suited category or create one yourself.",
                              'likes':683, 'dislikes':24, 'posted': None,
                              'edited': None, 'user':'SeriousFred'}
                         ]
                      },
                     {'name': "Whats your favourite programming language",
                      "description": "Personally I like python",
                      "views": 253,
                      "user": "DampSeatOnTheBus",
                      "answers":
                         [
                             {'answer': 'I prefer C', 'likes': 50, 'dislikes': 13,
                              'posted': None, 'edited': None, 'user': 'HealthyLivingForAHealthyBeing'},
                             {'answer': 'Java', 'likes':31, 'dislikes': 15,
                              'posted': None, 'edited': None, 'user': 'SeriousFred'},
                             {'answer': 'I agree, python is best', 'likes': 68, 'dislikes': 15,
                              'posted': None, 'edited': None, 'user': 'ooeeooahahtingtang'},
                             {'answer': 'Haskell 4 life', 'likes': 4, 'dislikes': 1,
                              'posted': None, 'edited': None, 'user': 'AintGotNoMoney'},
                        ]
                    },
                     {'name': "Can someone help me with python",
                      "description": "I need to know how to loop through a list in python, but I only know C style for loops. Help!",
                      "views": 42,
                      "user": "HealthyLivingForAHealthyBeing",
                      "answers":
                         [
                             {'answer': 'Do for item in list: Simple as that ', 'likes': 15, 'dislikes': 0,
                              'posted': None, 'edited': None, 'user': 'DampSeatOnTheBus'},
                        ]
                    }
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
                      "user": "SeriousFred",
                      'answers':
                         [
                             {'answer':'McDonalds', 'likes': 70, 'dislikes' : 61,
                              'posted': None, 'edited': None, 'user': 'HealthyLivingForAHealthyBeing'},
                             {'answer':'BlueLagoon', 'likes':321, 'dislikes': 29,
                              'posted': None, 'edited': None, 'user': 'AngryTelephonePole87'},
                         ]},
                     {'name': "Best non-alcoholic drink for students",
                      "description": "amazing!",
                      "views": 12,
                      "user": "AintGotNoMoney",
                      'answers':
                          [
                              {'answer':' Water', 'likes': 3, 'dislikes':0,
                               'posted': None, 'edited': None, 'user': 'AintGotNoMoney'},
                              {'answer': 'J20', 'likes': 1, 'dislikes': 1,
                               'posted': None, 'edited': None, 'user': 'SeriousFred'},
                          ]
                      },
                     {'name': "How do you study",
                      "description": "I just can't do it... I always get distracted",
                      "views": 380,
                      "user": "GustySeagull1942",
                      "support_file": "support_files/study.jpg",
                      'answers':
                          [
                              {'answer':'You need to come up with a study plan, then follow that plan every day. Dont be lazy.', 'likes': 33, 'dislikes':11,
                               'posted': None, 'edited': None, 'user': 'SeriousFred'},
                              {'answer': 'Keep yourself focused by turning off your phone', 'likes': 43, 'dislikes': 9,
                               'posted': None, 'edited': None, 'user': 'HealthyLivingForAHealthyBeing'},
                              {'answer': 'Dont worry about it too much. Stress doesnt help anything', 'likes': 80, 'dislikes': 21,
                               'posted': None, 'edited': None, 'user': 'AintGotNoMoney'},
                              {'answer': 'I also find it difficult. Maybe we should request a new category to be made call "Study Tips"?', 'likes': 19, 'dislikes': 1,
                               'posted': None, 'edited': None, 'user': 'YellowPony123'},
                          ]
                      },
                     {'name': "What city has the best nightlife in Scotland",
                      "description": "I need to know",
                      "views": 22,
                      "user": "DampSeatOnTheBus",
                      'answers':
                          [
                              {'answer':' Glasgow 100%', 'likes': 13, 'dislikes':2,
                               'posted': None, 'edited': None, 'user': 'AintGotNoMoney'},
                              {'answer': 'Dundee', 'likes': 5, 'dislikes': 1,
                               'posted': None, 'edited': None, 'user': 'SweetEdna'},
                          ]
                      },
                 ]
             }
    }

    for cat, cat_data in categories.items():
        c = add_category(cat, cat_data['description'], cat_data['approved'])
        print("Adding {0}...".format(str(c)))

        i = 0
        for question in cat_data['questions']:
            username = question['user']
            u = User.objects.get(username=username)
            up = UserProfile.objects.get(user=u)
            if len(question) == 6:
                q = add_question(question['name'], question['description'], question['views'], c, up, question['support_file'])
            else:
                q = add_question(question['name'], question['description'], question['views'], c, up)
            i += 1
            for answer in question['answers']:
                username = answer['user']
                u = User.objects.get(username=username)
                up = UserProfile.objects.get(user=u)
                add_answer(cat, answer['answer'], answer['likes'], answer['dislikes'], up, q)

        print("  Adding {0} questions to {1}...".format(str(i), str(c)))


    print()
    print("Marking selected questions as answered...")
    mark_as_answer(Answer.objects.get(pk=2))
    mark_as_answer(Answer.objects.get(pk=11))
    mark_as_answer(Answer.objects.get(pk=21))
    mark_as_answer(Answer.objects.get(pk=23))
    mark_as_answer(Answer.objects.get(pk=30))


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


def add_question(name, description, views, cat, user, support_file=None):
    q = Question.objects.get_or_create(name=name, text=description, category=cat, views=views, user=user)[0]
    if support_file:
        q.support_file = support_file
    q.save()
    return q


def add_user(username, first_name, last_name, password, email):
    u = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name, email=email)[0]
    u.set_password(password)
    u.save()
    return u


def add_user_profile(user, bio, likes, dislikes, permission, place_of_study, image=None):
    p = Permission.objects.get(title=permission)
    pos = PlaceOfStudy.objects.get(title=place_of_study)
    up = UserProfile.objects.get_or_create(user=user, bio=bio, likes=likes, dislikes=dislikes, permission=p, place_of_study=pos)[0]
    if image:
        up.image=image
    up.save()
    return up


# takes a user profile
def add_answer(cat, answer, likes, dislikes, user, questiontop):
    c_id = Category.objects.get(name=cat)
    a = Answer.objects.get_or_create(category=c_id, text=answer, likes=likes, dislikes=dislikes, user=user
                                     , questiontop=questiontop)[0]
    a.save()
    return a

def mark_as_answer(answer):
    question = answer.questiontop
    question.answered = answer
    question.save()
    return


def clean_db():
    if platform.system() == "Windows":
        subprocess.call(['del', 'db.sqlite3'], shell=True)
    else:
        subprocess.call(['rm', 'db.sqlite3'])

    subprocess.call(['python', 'manage.py', 'makemigrations', 'ask_students'])
    subprocess.call(['python', 'manage.py', 'migrate'])


def create_super_user():
    print()
    result = input("would you like to create superuser with USERNAME: admin PASSWORD: 12345678? (y/n): ")
    if result == "y":
        u = User(username='admin')
        u.set_password('12345678')
        u.is_superuser = True
        u.is_staff = True
        u.save()

        add_user_profile(u, "Site Administrator", 0, 0, "Student", "University of Glasgow", "profile_images/admin.jpg")


def run_server():
    print()
    run = input("would you like to run the server? (y/n): ")
    if run == "y":
        subprocess.call(['python', 'manage.py', 'runserver'])


if __name__ == '__main__':
    print("\nCleaning old database...\n")
    clean_db()

    print("\nPopulating database...\n")
    populate()

    create_super_user()
    run_server()

