import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('postgres:01110931793@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data['success'], 0)
        self.assertEqual(len(data['categories']), 6)
    
    def test_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data['success'], 0)
        self.assertNotEqual(len(data['questions']), 0)
    
    def test_category_id_400(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
    
    def test_question_delete(self):
        question = Question(question='fwd', answer='fwd',
                            category=3, difficulty=3)
        question.insert()
        question_id = question.id
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
    
    def test_page_200(self):
        res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_delete_id_404(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_create_questions(self):
        res = self.client().post('/questions', json={'question': 'fwd fwd fwd','answer': 'fwd fwd fwd','difficulty': 1,'category': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'question'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)

    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 0}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], False)
        self.assertNotEqual(len(data['question']), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
