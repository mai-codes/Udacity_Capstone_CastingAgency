# Casting Agency

## Udacity Full Stack Nanodegree Capstone Project
This project is the capstone project for Udacity's FSND. It is a Casting Agency, a company responsible for producing new movies, updating them, and managing the actors in those movies.

## Installing Dependencies
### Python 3.7
Follow instructions to install the latest version of python for your platform in the [!python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Virtual Enviornment
It is recommended to work within a virtual environment whenever using Python for projects. This keeps dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [!python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python). For this project, the required dependencies are listed in the `requirements.txt` file. 

Run `pip3 install -r requirements.txt` to install them.

### Key Dependencies
- Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- SQLAlchemy is the Python SQL toolkit and ORM used handle the lightweight sqlite database. 
- Flask-CORS is the extension used to handle cross origin requests.

Motivation for project
Detailed instructions for scripts to install any project dependencies, and to run the development server.
Documentation of API behavior and RBAC controls

## Running the server
From within the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run 
```

## API Reference

### Error Handling

Errors are returned as JSON in the following format (below 404 shown for reference):<br>
```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
The API will return the following three types of:

- 400 – bad request
- 404 – resource not found
- 422 – unprocessable

### Endpoints

`#### GET \movies`
- Required permissions: Casting Assistant `get:movies` and `get:actors`
- Fetches a dictionary of all available movies

Example response:
```
{
    "movies": [
        {
            "id": 3,
            "release_date": 2014,
            "title": "Iron Man & Captain America: Heroes United"
        },
        {
            "id": 4,
            "release_date": 2002,
            "title": "Batman Begins"
        }
    ],
    "success": true
}
```

`#### GET \actors`
- Required permissions: Casting Assistant `get:movies` and `get:actors`
- Fetches a dictionary of all available actors

Example response:
```
{
    "actors": [
        {
            "age": 43,
            "gender": "Female",
            "id": 2,
            "name": "Amy Poehler"
        },
        {
            "age": 43,
            "gender": "Male",
            "id": 3,
            "name": "Tom Hardy"
        },
        {
            "age": 40,
            "gender": "Male",
            "id": 4,
            "name": "Ryan Gosling"
        }
    ],
    "success": true
}
```

#### POST /questions

- Creates a new question 
- Request example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Which planet is the hottest in the solar system", "answer": "Venus", "difficulty": 3, "category": "3"}`

Example response: 
```
{
    "questions": [
        {
            "answer": "Apollo 13", 
            "category": 5, 
            "difficulty": 4, 
            "id": 2, 
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }, 
        {
            "answer": "Tom Cruise", 
            "category": 5, 
            "difficulty": 4, 
            "id": 4, 
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }, 
        {
            "answer": "Venus", 
            "category": 3, 
            "difficulty": 3, 
            "id": 9, 
            "question": "Which planet is the hottest in the solar system"
        }, 
        
    ], 
    "success": true, 
    "total_questions": 20
}
```

#### POST /questions with search term

- Returns search results
- Request example: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"search_term": "peanut"}'` </br>

Example response:
```
{
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }
  ], 
  "success": true, 
  "total_questions": 45
}
```

#### POST /quizzes

- Allows users to play the quiz game.
- Uses JSON request parameters of category and previous questions.
- Request example:  `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": "1"}}'`<br>
Example response:
```
{
    "question": {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    "success": true
}
```

#### DELETE /questions/<question_id> 

- Delete an existing questions from the repository of available questions
- Request example: `curl http://127.0.0.1:5000/questions/8 -X DELETE`

Example response:
```
{
  "deleted": "28", 
  "success": true
}
```