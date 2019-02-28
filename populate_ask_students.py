import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_students_project.settings')
import django
django.setup()

from ask_students.models import Category

def populate():

	categories = {'General': {'description': 'Ask general questions about any topic you like',
			                  'approved': True,},
			      'Computing': {'description': 'Ask questions about Computing',
			     				'approved': True}}

	for cat, cat_data in categories.items():
		c = add_category(cat, cat_data['description'], cat_data['approved'])

	for c in Category.objects.all():
		print("Adding {0}...".format(str(c)))

def add_category(cat, description, approved):
	c = Category.objects.get_or_create(name = cat, description = description, approved = approved, user = None)[0]
	c.save()
	return c

if __name__ == '__main__':
	print("Running ask_students population script...")
	populate()	