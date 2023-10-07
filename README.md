# BlogKulinarnyMobileApp Server

## Overview
This repository contains the server-side code for the "BlogKulinarnyMobileApp" - a culinary blog mobile application. The server is implemented using Flask and provides various endpoints for user authentication, recipe management, comments, and more. This server acts as the backend for the [BlogKulinarnyMobileApp-client](https://github.com/cptn3m012/BlogKulinarnyMobileApp-client), handling data storage, user requests, and serving content to the client. The client-side application communicates with this server to fetch and display content, post new recipes, manage user accounts, and facilitate interactions between users.



## Features
* **User Authentication**: Secure user registration and login functionality.
* **Recipe Management**: Add, update, and delete recipes. Retrieve a list of all recipes or details of a specific recipe.
* **Comments**: Users can add comments to recipes.
* **Categories**: Manage different categories for recipes.
* **User Management**: Admin functionalities to manage users.

## Extension:
* Restful: [Flask-RESTful](http://flask-restplus.readthedocs.io/en/stable/)
* SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
* JWT Authentication: [Flask-JWT-Extended](http://flask.pocoo.org/docs/0.12/testing/)
* Password Hashing: [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
* Template Engine: [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/)
* Data Serialization: [itsdangerous](https://itsdangerous.palletsprojects.com/en/2.0.x/)
* WSGI Utility: [Werkzeug](https://werkzeug.palletsprojects.com/en/2.0.x/)
* CORS: [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/)
* Form Handling: [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)[Flask-WTF](https://flask-wtf.readthedocs.io/en/1.2.x/)

## Clone and install
Follow these steps to clone the project and install the necessary dependencies:
1. Clone the repozitory:
```
$ git clone https://github.com/cptn3m012/BlogKulinarnyMobileApp-server
$ cd BlogKulinarnyMobileApp-server
```
2. Set Up a Virtual Environment (optional but recommended):
```
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install Dependencies:
```
$ pip install -r requirements.txt
```
4. Configure Database Connection:
Before running the server, you need to configure the database connection. Open the database.py file. You will see placeholders where you need to provide your database details:
 ```
 $ server = 'YOUR_SERVER_HERE'
 $ database = 'YOUR_DATABASE_NAME_HERE'
 $ login = 'YOUR_LOGIN_HERE'
 $ password = 'YOUR_PASSWORD_HERE'
```  
5. Run the Server:
 ```
$ flask run
```
After following these steps, the server should be up and running locally on your machine. Make sure to check the client-side application [BlogKulinarnyMobileApp-client](https://github.com/cptn3m012/BlogKulinarnyMobileApp-client) for the complete experience.

## License

_For more info, please refer to the [Documentation](https://github.com/cptn3m012/BlogKulinarnyMobileApp-server/blob/master/Dokumentacja%20PUM.pdf)_
