import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_items(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {'origins': '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                          'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                          'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    allCategories = Category.query.order_by(Category.id).all()
    try:
      return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in allCategories},
        'total_categories': len(allCategories)
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    allQuestions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    try:
      return jsonify({
        'questions': paginate_items(request, allQuestions),
        'total_questions': len(allQuestions),
        'categories': {category.id: category.type for category in categories},
        'current_category': []
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)
    
      question.delete()
      allQuestions = Question.query.order_by(Question.id).all()
      return jsonify({
        'success': True,
        'deleted_id': question_id,
        'total_questions': len(allQuestions)
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()
    try:
      new_question = body.get('question', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)
      new_answer = body.get('answer', None)
      question = Question(question=new_question, category=new_category, answer=new_answer,
                 difficulty=new_difficulty,)
      question.insert()
      questions = Question.query.order_by(Question.id).all()
      return jsonify({
        'success': True,
        'questions': paginate_items(request, questions),
        'total_questions': len(questions)
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search = body.get('searchTerm')
    questions = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
    current_questions = [question.format() for question in questions]
    return jsonify({
      'success':True,
      'questions':current_questions,
      'total_questions':len(questions),
      'current_category':'None'
    })
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    category = Category.query.filter(Category.id == id).one_or_none()
    if (category is None):
        abort(400)
    selection = Question.query.filter_by(category=category.id).all()
    current_questions = paginate_items(request, selection)
    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'current_category': category.type
    })
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_questions():
    body = request.get_json()
    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)
    category_id = quiz_category['id']
    if category_id == 0:
      questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
    else:  
      questions = Question.query.filter(Question.id.notin_(previous_questions), Question.category == category_id).all()

    question = None
    cur_question = ''
    for question in questions:
      if question.id not in previous_questions:
        cur_question = question.format()
        break

    return jsonify({
        'success': True,
        'question': cur_question,
    })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Not Processable"
    }), 422
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400
  
  return app

    
