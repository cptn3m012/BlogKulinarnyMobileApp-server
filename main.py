from flask import Flask, request, jsonify
import pyodbc
import hashlib
import base64

app = Flask(__name__)


# Funkcja do haszowania hasła
def HashPassword(password):
    hashed_bytes = hashlib.sha256(password.encode()).digest()
    hashed_password = base64.b64encode(hashed_bytes).decode()
    return hashed_password


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
    hashed_password = HashPassword(password)  # Haszowanie hasła

    # Sprawdzenie, czy użytkownik istnieje w bazie danych
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE (login=? OR mail=?) AND password=?",
                   (username_or_email, username_or_email, hashed_password))
    user = cursor.fetchone()

    conn.close()  # Zamknięcie połączenia z bazą danych

    if user:
        # Jeśli użytkownik istnieje, zwróć poprawną odpowiedź JSON
        return jsonify({'success': True})
    else:
        # Jeśli użytkownik nie istnieje, zwróć błąd 401
        return jsonify({'success': False}), 401


#Endpoint rejestracji
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
        hashed_password = HashPassword(password)  # Haszowanie hasła

        # Sprawdzenie, czy użytkownik o podanym adresie e-mail lub nazwie użytkownika już istnieje
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE mail=? OR login=?", (mail, username))
        existing_user = cursor.fetchone()

        if existing_user:
            # Jeśli użytkownik już istnieje, zwróć błąd 409 (konflikt)
            return jsonify({'error': 'Użytkownik o podanym adresie e-mail lub nazwie użytkownika już istnieje.'}), 409

        # Dodanie nowego użytkownika do bazy danych
        cursor.execute("INSERT INTO Users (mail, login, password, rank, isAccepted) VALUES (?, ?, ?, ?, ?)",
                       (mail, username, hashed_password, 1, 1))

        conn.commit()

        # Zwrócenie odpowiedzi sukcesu
        return jsonify({'success': True}), 200
    except Exception as e:
        # Obsługa błędu
        print(e)
        return jsonify({'error': 'Wystąpił błąd podczas rejestracji.'}), 500
    finally:
        conn.close()  # Zamknięcie połączenia z bazą danych


#Endpoint pobierania przepisów
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
        cursor.execute("SELECT * FROM [recipes] AS [r] WHERE [r].[isAccepted] = 1")

        recipes = []
        current_recipe_id = None
        recipe = None

        for row in cursor.fetchall():
            recipe_id, is_accepted, title, image_url, description, difficulty, avg_time, portions, user_id = row
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
                    "userId": user_id
                }

        if recipe is not None:
            recipes.append(recipe)

        conn.close()
        return jsonify({'recipes': recipes}), 200
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas pobierania przepisów.'}), 500


# Endpoint do resetowania hasła
@app.route('/resetPassword', methods=['POST'])
def reset_password():
    # Pobranie adresu e-mail z ciała żądania
    email = request.json.get('email')

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
        cursor.execute("""
            SELECT TOP(1) [u].[Id], [u].[PasswordResetToken], [u].[ResetTokenExpires], 
            [u].[VerificationToken], [u].[VerifiedAt], [u].[imageURL], [u].[isAccepted], 
            [u].[login], [u].[mail], [u].[password], [u].[rank]
            FROM [users] AS [u]
            WHERE [u].[mail] = ? """, email)

        row = cursor.fetchone()

        if row:
            user_id, password_reset_token, reset_token_expires, verification_token, verified_at, image_url, is_accepted, login, mail, password, rank = row
            # Wygeneruj nowy token resetowania hasła
            # ...

            # Uaktualnij dane użytkownika w bazie danych


            # Wyślij e-mail z linkiem do resetowania hasła
            # ...

            conn.commit()
            conn.close()
            return jsonify({'success': 'Pomyślnie zresetowano hasło.'}), 200
        else:
            conn.close()
            return jsonify({'error': 'Nie znaleziono użytkownika o podanym adresie e-mail.'}), 404
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'error': 'Wystąpił błąd podczas resetowania hasła.'}), 500


# Endpoint do zmiany hasła użytkownika
@app.route('/changePassword', methods=['POST'])
def change_password():
    # Pobranie danych z formularza
    user_id = request.form.get('userId')
    old_password = request.form.get('oldPassword')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')

    # Sprawdzenie, czy nowe hasło i potwierdzenie hasła są zgodne
    if new_password != confirm_password:
        return jsonify({'error': 'Nowe hasło i potwierdzenie hasła nie są zgodne.'}), 400

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
        cursor.execute("""
            SELECT TOP(1) [u].[Id], [u].[PasswordResetToken], [u].[ResetTokenExpires],
            [u].[VerificationToken], [u].[VerifiedAt], [u].[imageURL], [u].[isAccepted],
            [u].[login], [u].[mail], [u].[password], [u].[rank]
            FROM [users] AS [u]
            WHERE [u].[Id] = ?
        """, user_id)

        row = cursor.fetchone()

        if row:
            user_id, password_reset_token, reset_token_expires, verification_token, verified_at, image_url, is_accepted, login, mail, password, rank = row

            # Sprawdzenie, czy stare hasło jest poprawne
            if old_password != password:
                conn.close()
                return jsonify({'error': 'Stare hasło jest niepoprawne.'}), 400

            # Edytuj hasło użytkownika
            # ...

            # Uaktualnij dane użytkownika w bazie danych
            cursor.execute("""
                UPDATE [users]
                SET [password] = ?
                WHERE [Id] = ?
            """, new_password, user_id)

            conn.commit()
            conn.close()
            return jsonify({'success': 'Pomyślnie zmieniono hasło.'}), 200
        else:
            conn.close()
            return jsonify({'error': 'Nie znaleziono użytkownika o podanym identyfikatorze.'}), 404
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'error': 'Wystąpił błąd podczas zmiany hasła.'}), 500

# main
if __name__ == '__main__':
    # Uruchomienie aplikacji Flask z obsługą HTTP
    app.run(host='0.0.0.0', port=5000)
