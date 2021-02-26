# Casting Agency
Link to Website: https://castingagency-udacityfsnd.herokuapp.com

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

#### Roles & Permissions
- Casting Assistant
    - `get:movies`
    - `get:actors`  
- Casting Director
    - All permissions a Casting Assistant has +
    - `post:actors`
    - `delete:actors`
    - `patch:movies`
    - `patch:actors`
- Executive Producer
    - All permissions a Casting Director has +
    -  `post:movies`
    -  `delete:movies`

#### `GET \movies`
- Required permissions: Casting Assistant, Casting Director, or Executive Producer
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

#### `GET \actors`
- Required permissions: Casting Assistant, Casting Director, or Executive Producer
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

#### `POST /movies`
- Required permissions: Executive Producer
- Creates a new movie 

Example body:
```
{
  "title": "Thor",
  "release_date": "2012"
}
```

Example response: 
```
{
    "movie": [
        {
            "id": 6,
            "release_date": 2012,
            "title": "Thor"
        }
    ],
    "success": true
}
```

#### `POST /actors`
- Required permissions: Casting Director or Executive Producer
- Creates a new movie 

Example body:
```
{
    "name": "Ryan Gosling",
    "age": "40",
    "gender": "Male"
}
```

Example response:
```
{
    "actor": [
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

#### `PATCH /movies/<id>`

- Required permissions: Casting Director or Executive Producer
- Updates a movie 

Example body:
```
{
  "title": "Thor",
  "release_date": "2012"
}
```

Example response: 
```
{
    "movie": [
        {
            "id": 6,
            "release_date": 2012,
            "title": "Thor"
        }
    ],
    "success": true
}
``` 

#### `PATCH /actors/<id>
- Required permissions: Casting Director or Executive Producer
- Updates an actor 

Example body:
```
{
    "name": "Ryan Gosling",
    "age": "40",
    "gender": "Male"
}
```

Example response:
```
{
    "actor": [
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

#### `DELETE /movies/<id>`
- Required permissions: Executive Producer
- Delete an existing movie from the repository of available movies

Example response:
```
{
  "success": true,
  "delete": 2
}
```

#### `DELETE /actors/<id>`
- Required permissions: Casting Director or Executive Producer
- Delete an existing actor from the repository of available actors

Example response:
```
{
  "success": true,
  "delete": 1 
}
```