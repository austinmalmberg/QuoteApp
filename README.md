
# Flask Boilerplate

Flask Boilerplate is a scaffold to get your next Flask web application off the ground quick.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Notable Libraries](#notable-libraries)
3. [Features](#features)
4. [Endpoints](#endpoints)
5. [FAQs](#faqs)


## Getting Started

Install requirements.

    > pip install -r requirements.txt

Initialize Flask-Migrate.

    > flask db init

Run application. (Linux users should use `export` instead of `set`)
  
    > set FLASK_ENV=development
    > flask run


## Notable Libraries

- Flask (obviously)
- SQLAlchemy
- WTForms
- Flask-Migrate (for managing database migrations)


## Features

### MVC Design Pattern

Implements an MVC design pattern. Endpoint should retrieve data from `data_access` methods, which can be passed
directly into the view or cleansed first using a Data Transfer Object (DTO).

### Database

Initializes a local SQLite database for development. For production,
set the `SQLALCHEMY_DATABASE_URI` environmental variable.

Flask-Migrate allows for easy management of database changes. Check out the Flask-Migration documentation.

### Authentication

See Flask-Login documentation.

### WTForms

An easy way to create forms and handle validation. See the Flask_WTF documentation

### Bootstrap 5

For speedy styling.

### Custom Error Page

Because errors need love too.


## Endpoints

### Core

#### `/`

The homepage

#### `/dashboard` _(Login required)_

_(Login required)_. A restricted view.

### Authentication

#### `/register` (`GET`, `POST`)

The registration page.

#### `/login` (`GET`, `POST`)

The login page.

#### `/logout`

_(Login required)_. Logs out the current user.

### Admin

#### `/admin`

_(Role `admin` required)_. View all app users.

#### `/admin/users/<id>/delete` (`POST`)

_(Role `admin` required)_. Delete user with `id`.


### API

#### `/api/user`

_(Login required)_. User info as JSON.

#### `/api/user/all`

_(Role `admin` required)_. App users as JSON.


## FAQs

### How do I create a new Admin user?

    > flask shell
    >>> from app.data_access.user import add_user
    >>> add_user('admin@app.com', 'password1234', role='admin')