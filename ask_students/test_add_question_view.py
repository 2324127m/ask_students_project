from django.test import TestCase
from ask_students.models import Question, Category, Answer
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from ask_students.forms import AskQuestionForm


class AddQuestionViewTests(TestCase):
        
    def TestQuestionFields(self):
        #name, text, category, supported file
        form = AskQuestionForm({
            'name': "Testing Testing 123",
            'text': "This is a testtt",
            'category': "Test",
            }, entry=self.entry)
        
            self.assertTrue(form.is_valid())
            Question = form.save()
            self.assertEqual(Question.name, "Testing Testing 123")
            self.assertEqual(Question.text, "This is a testtt")
            self.assertEqual(Question.category, "Test")
            self.assertEqual(Question.entry, self.entry)

    def TestEmptyForm(self):
        form = AskQuestionForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['required'],
            'text': ['required'],
            'category': ['required'],
        })
        

    def TestQuestionPostWithoutFile(self):
       form = AskQuestionForm({'name' : 'TestFiles',
                               'text' : 'Test for No files',
                               'category' : 'Test',
                               'support_file': (blank = True),
                               }, entry = self.entry)
       self.assetTrue(form.is_valid())
       Question = form.save()
       self.assertEqual(Question.support_file,(blank = True))
