# HBnB Web Application

![framework](../assets/framework.gif)

## Description

This is a web application that allows users to create, update, and delete objects. The application is built using Flask, a micro web framework written in Python. The application uses SQLAlchemy to connect to a MySQL database. The application also uses Jinja2 to render HTML templates.

## Routes

### Home Routes

- `/` - Displays the home page

### State Routes

- `/states` - Displays a list of all states
- `/states/<state_id>` - Displays information about a specific state
- `/states/<state_id>/cities` - Displays a list of all cities in a specific state
- `/states/<state_id>/cities/<city_id>` - Displays information about a specific city in a specific state

## Models

| Class       | Description               |
| ----------- | ------------------------- |
| `BaseModel` | Base class for all models |
| `User`      | Represents a user         |
| `State`     | Represents a state        |
| `City`      | Represents a city         |
| `Amenity`   | Represents an amenity     |
| `Place`     | Represents a place        |
| `Review`    | Represents a review       |

## Controllers

| File           | Description              |
| -------------- | ------------------------ |
| `app.py`       | Main application file    |
| `states.py`    | Controller for states    |
| `cities.py`    | Controller for cities    |
| `places.py`    | Controller for places    |
| `users.py`     | Controller for users     |
| `amenities.py` | Controller for amenities |
| `reviews.py`   | Controller for reviews   |
