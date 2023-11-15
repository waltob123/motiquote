
# Motiquote
This is a web application that serves as both an API and a platform for motivational writers to share their inspiring quotes. Users can view motivational quotes posted by various authors through the API, and writers can contribute their own quotes to be showcased on the platform.

# Technologies Used
HTML: Used for structuring the web pages.

CSS: Applied for styling and improving the overall user interface.

JavaScript: Employed for client-side scripting and enhancing user interactivity.

Jinja Templating: Integrated with Flask to dynamically generate HTML content.

Flask: A micro web framework for Python used to build the backend of the application.

GitHub: Utilized for version control and collaborative development.

Git: Implemented for tracking changes and managing codebase.

NGINX: Used as a web server to handle HTTP requests.

Gunicorn: Employed as a WSGI server to run the Flask application.

# Features
Motivational Quote API:

The API provides endpoints to retrieve motivational quotes.
Writers can submit new quotes via API calls.
# Web Application:

Users can browse and view motivational quotes on the web platform.
Writers can log in and post their motivational quotes.
Responsive design for a seamless experience on various devices.
# Getting Started
Prerequisites

Python 3.x

Flask (pip install flask)

Gunicorn (pip install gunicorn)

# Installation
Clone the repository:

```{bash}
git clone https://github.com/waltob123/motiquote.git

cd motivational-quote-app
```

# Install dependencies:
```{bash}
pip install -r requirements.txt
```

# Run the application:


```{bash}
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
Open your browser and visit http://localhost:5000 to access the web application.

# Usage
### API Endpoints
GET /api/v1/quotes

Retrieve a list of all motivational quotes.

GET /api/v1/quotes/{quote_id}

Retrieve a motivational quote by ID.

GET /api/v1/quotes/search?author=

Search for a motivational quote by a particular author.

# Web Application
Visit the home page to view a collection of motivational quotes.

Writers can log in to post new quotes.

# Author
Desmond Asiedu Asamoah

# Contributing
If you would like to contribute to this project, please follow the contributing guidelines.

# License
This project is licensed under the MIT License.

# Acknowledgments
Special thanks to all contributors and the open-source community.
