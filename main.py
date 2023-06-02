from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Endpoint logowania
@app.route('/login', methods=['POST'])
def login():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"
    conn = pyodbc.connect(conn_str)

    # Pobranie danych logowania z żądania POST
    username_or_email = request.json['username_or_email']
    password = request.json['password']

    # Sprawdzenie, czy użytkownik istnieje w bazie danych
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE (login=? OR mail=?) AND password=?", (username_or_email, username_or_email, password))
    user = cursor.fetchone()

    conn.close()  # Zamknięcie połączenia z bazą danych

    if user:
        # Jeśli użytkownik istnieje, zwróć poprawną odpowiedź JSON
        return jsonify({'success': True})
    else:
        # Jeśli użytkownik nie istnieje, zwróć błąd 401
        return jsonify({'success': False}), 401

@app.route('/register', methods=['POST'])
def register():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"
    conn = pyodbc.connect(conn_str)

    try:
        # Pobranie danych rejestracji z żądania POST
        data = request.get_json()
        mail = data['mail']
        username = data['login']
        password = data['password']

        # Sprawdzenie, czy użytkownik o podanym adresie e-mail lub nazwie użytkownika już istnieje
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE mail=? OR login=?", (mail, username))
        existing_user = cursor.fetchone()

        if existing_user:
            # Jeśli użytkownik już istnieje, zwróć błąd 409 (konflikt)
            return jsonify({'error': 'Użytkownik o podanym adresie e-mail lub nazwie użytkownika już istnieje.'}), 409

        # Dodanie nowego użytkownika do bazy danych
        cursor.execute("INSERT INTO Users (mail, login, password, rank, isAccepted) VALUES (?, ?, ?, ?, ?)", (mail, username, password, 1, 1))

        conn.commit()

        # Zwrócenie odpowiedzi sukcesu
        return jsonify({'success': True}), 200
    except Exception as e:
        # Obsługa błędu
        print(e)
        return jsonify({'error': 'Wystąpił błąd podczas rejestracji.'}), 500
    finally:
        conn.close()  # Zamknięcie połączenia z bazą danych

@app.route('/loadRecipes', methods=['GET'])
def loadRecipes():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"
    conn = pyodbc.connect(conn_str)

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM [recipes] AS [r] WHERE [r].[isAccepted] = 1")

        recipes = []
        current_recipe_id = None
        recipe = None

        for row in cursor.fetchall():
            recipe_id, is_accepted, title, image_url, description, difficulty, avg_time, portions, user_id, category_id = row

            if recipe_id != current_recipe_id:
                if recipe is not None:
                    recipes.append(recipe)
                current_recipe_id = recipe_id
                recipe = {
                    "id": recipe_id,
                    "isAccepted": is_accepted,
                    "title": title,
                    "imageURL": image_url,
                    "description": description,
                    "difficulty": difficulty,
                    "avgTime": avg_time,
                    "portions": portions,
                    "userId": user_id,
                    "CategoryId": category_id
                }

            if category_id is not None:
                category = {
                    "id": category_id,
                    "name": category_name
                }

        if recipe is not None:
            recipes.append(recipe)

        conn.close()
        return jsonify({'recipes': recipes}), 200
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas pobierania przepisów.'}), 500


#main
if __name__ == '__main__':
    # Uruchomienie aplikacji Flask z obsługą HTTP
    app.run(host='0.0.0.0', port=5000)
