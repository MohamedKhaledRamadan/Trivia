# Full Stack Trivia API Project
The API has the following functionalities:
1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

### Installing Dependencies
Developers using this project should already have Python3, pip, node, and npm installed.

#### Frontend Dependencies
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Backend Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.
##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend micro-services framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first en sure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Omit the dropdb command the first time you run tests.

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
* Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable

# Endpoints
### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

Example: `curl http://localhost:5000/categories`
```
{
	'1' : "Science",
	'2' : "Art",
	'3' : "Geography",
	'4' : "History",
	'5' : "Entertainment",
	'6' : "Sports"
}
```

### GET '/questions'
- Fetches a dictionary of questions, paginated in groups of 10. 
- Returns JSON object of categories, questions dictionary with answer, category, difficulty, id and question.

Example: `curl http://localhost:5000/questions`
```
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "current_category": [],
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
        ... # omitted for brevity 
    ],
    "success": true,
    "total_questions": 33
}
```

### DELETE '/questions/<int:question_id>'
- Deletes selected question by id
- Returns 200 if question is successfully deleted.
- Returns 404 if question did not exist
- Returns JSON object of deleted id, remaining questions, and length of total questions

Example: `curl -X DELETE http://localhost:5000/question/2`
```
{
    "deleted": 2,
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }    
        ... # omitted for brevity 
    ],
    "success": true,
    "total_questions": 32
}
```

### POST '/questions'
- Creates a new question posted from the react front end.
- Fields are: answer, difficulty and category. 
- Returns a success value and ID of the question.
- If search field is present will return matching expressions
```

### GET '/categories/<cat_id>/questions'
- Returns JSON response of current_category, and the questions pertaining to that category

Example: `curl http://localhost:5000/categories/1/questions`
```
{
 "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
   ... # omitted for brevity
  ], 
  "success": true, 
  "total_questions": 6
}
```


### POST '/quizzes'
- Generates a quiz based on category or a random selection depending on what the user chooses.
- Returns a random question

Example: `curl http://localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"type":"Art","id":2}}'`
```
{
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }, 
  "success": true
}
```
