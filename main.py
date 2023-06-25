from flask import Flask, request, jsonify
import pyodbc
import hashlib
import base64
import json

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
        return jsonify({'result': True, 'user.rank': user[5], 'user.id': user[0], 'user.login': user[1],
                        'user.mail': user[3], 'user.password': user[2]})
    else:
        # Jeśli użytkownik nie istnieje, zwróć błąd 401
        return jsonify({'result': False}), 401


# Endpoint rejestracji
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
                       (mail, username, hashed_password, 0, 0))

        conn.commit()

        # Zwrócenie odpowiedzi sukcesu
        return jsonify({'success': True}), 200
    except Exception as e:
        # Obsługa błędu
        print(e)
        return jsonify({'error': 'Wystąpił błąd podczas rejestracji.'}), 500
    finally:
        conn.close()  # Zamknięcie połączenia z bazą danych


@app.route('/update_user', methods=['POST'])
def update_user():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"
    conn = pyodbc.connect(conn_str)

    # Pobranie danych z żądania POST
    login = request.json.get('login')
    mail = request.json.get('mail')
    user_id = request.json.get('user_id')

    # Zaktualizowanie danych w bazie danych
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET login=?, mail=? WHERE Id=?", (login, mail, user_id))
    conn.commit()
    conn.close()  # Zamknięcie połączenia z bazą danych

    return jsonify({'message': 'Dane użytkownika zostały zaktualizowane.'})


@app.route('/update_password', methods=['POST'])
def update_password():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"
    conn = pyodbc.connect(conn_str)

    # Pobranie danych z żądania POST
    user_id = request.json.get('user_id')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    cursor = conn.cursor()

    # Zaktualizowanie hasła w bazie danych
    hashed_new_password = HashPassword(new_password)
    cursor.execute("UPDATE Users SET password=? WHERE Id=?", (hashed_new_password, user_id))
    conn.commit()

    return jsonify({'message': 'Hasło użytkownika zostało zaktualizowane.'})
    conn.close()


@app.route('/delete_account', methods=['POST'])
def delete_account():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"
    conn = pyodbc.connect(conn_str)

    # Pobranie danych z żądania POST
    user_id = request.json.get('user_id')

    cursor = conn.cursor()

    # Usunięcie użytkownika z bazy danych
    cursor.execute("DELETE FROM Users WHERE Id=?", user_id)
    conn.commit()

    return jsonify({'message': 'Użytkownik został usunięty z bazy danych.'})
    conn.close()


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
        cursor.execute("""
            SELECT
                r.id AS recipeIdentifier,
                r.isAccepted,
                r.title,
                r.imageURL,
                r.description,
                r.difficulty,
                r.avgTime,
                r.portions,
                r.userId,
                re.noOfList,
                re.imageURL AS stepImageURL,
                re.description AS stepDescription,
                u.login,
                c.userId AS usId,
                c.Id AS comment_id,
                c.Text AS commentText,
                c.Rate AS commentRate,
                c.[isBlocked] AS isB,
                cat.name AS categoryName
            FROM
                recipes AS r
                INNER JOIN (
                    SELECT
                        recipeId,
                        MIN(noOfList) AS noOfList,
                        imageURL,
                        description
                    FROM
                        recipesElements
                    GROUP BY
                        recipeId,
                        imageURL,
                        description
                ) AS re ON r.id = re.recipeId
                LEFT JOIN (
                    SELECT
					*
                    FROM
                        comments AS ce
                ) AS c ON r.id = c.recipeId
                INNER JOIN (
                    SELECT
                        recipeId,
                        name
                    FROM
                        recipesCategories AS rc
                        INNER JOIN categories AS cat ON rc.categoryId = cat.id
                ) AS cat ON r.id = cat.recipeId
                INNER JOIN users AS u ON r.userId = u.[Id];
        """)

        recipes = []
        current_recipe_id = None
        recipe = None

        for row in cursor.fetchall():
            recipe_id, is_accepted, title, image_url, description, difficulty, avg_time, portions, user_id, \
                no_of_list, step_image_url, step_description, \
                comment_userLogin, comment_userid, comment_id, comment_text, comment_rate, isBlocked, category_name = row
            if recipe_id != current_recipe_id:
                if recipe is not None:
                    recipes.append(recipe)
                current_recipe_id = recipe_id
                recipe = {
                    "recipeIdentifier": recipe_id,
                    "isAccepted": is_accepted,
                    "title": title,
                    "imageURL": image_url,
                    "description": description,
                    "difficulty": difficulty,
                    "avgTime": avg_time,
                    "portions": portions,
                    "userId": user_id,
                    "u.login": comment_userLogin,
                    "steps": [],
                    "comments": [],
                    "categories": []
                }

            if {"imageURL": step_image_url, "description": step_description, "noOfList": no_of_list} not in recipe[
                "steps"]:
                recipe["steps"].append({
                    "imageURL": step_image_url,
                    "description": step_description,
                    "noOfList": no_of_list
                })

            # Check for duplicate comments
            duplicate_comment = False
            for comment in recipe["comments"]:
                if comment["usId"] == comment_userid and comment["text"] == comment_text and comment[
                    "rate"] == comment_rate:
                    duplicate_comment = True
                    break

            if not duplicate_comment:
                if comment_text is not None and comment_rate is not None and comment_userid is not None:
                    recipe["comments"].append({
                        "usId": comment_userid,
                        "comment_id": comment_id,
                        "login": comment_userLogin,
                        "text": comment_text,
                        "rate": comment_rate,
                        "isBlocked": isBlocked
                    })

            if category_name not in recipe["categories"]:
                recipe["categories"].append(category_name)

        if recipe is not None:
            recipes.append(recipe)
        print(recipes)
        conn.close()
        return jsonify({'recipes': recipes}), 200

    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas pobierania przepisów.'}), 500


# Endpoint pobierania YOUR_LOGIN_HEREow
@app.route('/loadUsersToAccept', methods=['GET'])
def loadUsersToAccept():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    log = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"
    conn = pyodbc.connect(conn_str)

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT [u].[Id], [u].[imageURL], [u].[isAccepted], [u].[login], [u].[mail], [u].[rank] \
                        FROM [users] AS [u] WHERE [u].[isAccepted] = 0")

        users = []

        for row in cursor.fetchall():
            user_id, image_url, is_accepted, login, mail, rank = row
            user = {
                "id": user_id,
                "imageURL": image_url,
                "isAccepted": is_accepted,
                "login": login,
                "mail": mail,
                "rank": rank
            }
            users.append(user)

        conn.close()
        return jsonify({'users': users}), 200
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas pobierania danych użytkowników.'}), 500


# Endpoint usuwania YOUR_LOGIN_HEREow
@app.route('/deleteUsersToAccept/<int:user_id>', methods=['DELETE'])
def deleteUsersToAccept(user_id):
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    log = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"
    conn = pyodbc.connect(conn_str)

    try:

        cursor = conn.cursor()
        cursor.execute("DELETE FROM [users] WHERE [Id] = ?", (user_id,))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Użytkownik został pomyślnie usunięty.'}), 200
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas usuwania użytkownika.'}), 500


# Endpoint do pobierania kategorii
@app.route('/loadCategories', methods=['GET'])
def loadCategories():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    log = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"
    conn = pyodbc.connect(conn_str)

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT [c].[id], [c].[isAccepted], [c].[name] FROM [categories] AS [c]")

        categories = []

        for row in cursor.fetchall():
            category_id, is_accepted, name = row
            category = {
                "id": category_id,
                "isAccepted": is_accepted,
                "name": name
            }
            categories.append(category)

        conn.close()
        return jsonify({'categories': categories}), 200
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas pobierania danych kategorii.'}), 500


@app.route('/updateCategoryState', methods=['POST'])
def updateCategoryState():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    log = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"
    conn = pyodbc.connect(conn_str)

    try:
        # Otrzymujemy dane z żądania POST
        category_id = request.json['id']
        new_state = request.json['isAccepted']

        # Połączenie z bazą danych
        conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Aktualizacja stanu kategorii w bazie danych
        cursor.execute("UPDATE [categories] SET [isAccepted] = ? WHERE [id] = ?", new_state, category_id)
        conn.commit()
        conn.close()

        return jsonify({'success': 'Stan kategorii został zaktualizowany.'}), 200
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas aktualizacji stanu kategorii.'}), 500


@app.route('/deleteCategory/<int:category_id>', methods=['DELETE'])
def deleteCategory(category_id):
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    log = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"

    try:
        # Połączenie z bazą danych

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Usunięcie kategorii z bazy danych
        cursor.execute("DELETE FROM [categories] WHERE [id] = ?", category_id)
        conn.commit()
        conn.close()

        return jsonify({'success': 'Kategoria została usunięta.'}), 200
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas usuwania kategorii.'}), 500


@app.route('/updateUserAccept', methods=['POST'])
def updateUserAccept():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    log = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"
    conn = pyodbc.connect(conn_str)

    try:

        user_id = request.json['id']
        new_state = request.json['isAccepted']

        # Połączenie z bazą danych
        conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Aktualizacja stanu isAccepted użytkownika
        cursor.execute("UPDATE [users] SET [isAccepted] = ? WHERE [id] = ?",
                       new_state, user_id)
        conn.commit()
        conn.close()
        return jsonify({'success': 'Stan YOUR_LOGIN_HEREa został zaktualizowany.'}), 200

    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas aktualizacji stanu kategorii.'}), 500


@app.route('/updateRecipeState', methods=['POST'])
def updateRecipeState():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    log = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"
    conn = pyodbc.connect(conn_str)

    try:
        # Otrzymujemy dane z żądania POST
        recipe_id = request.json['id']
        new_state = request.json['isAccepted']

        # Połączenie z bazą danych
        conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={log};PWD={password}"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Aktualizacja stanu kategorii w bazie danych
        cursor.execute("UPDATE [recipes] SET [isAccepted] = ? WHERE [id] = ?", new_state, recipe_id)
        conn.commit()
        conn.close()

        return jsonify({'success': 'Stan przepisu został zaktualizowany.'}), 200
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({'error': 'Wystąpił błąd podczas aktualizacji stanu kategorii.'}), 500


# Endpoint do dodania komentarza przez user'a
@app.route('/addUserComm', methods=['POST'])
def addUserComm():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # Pobranie danych rejestracji z żądania POST
        data = request.get_json()

        message = data['text']
        rate = data['rate']
        recipe_id = data['recipe_id']
        user_id = data['user_id']

        # Dodanie nowego komentarza do bazy danych
        cursor.execute("INSERT INTO Comments (Rate,Text, recipeId, userId) VALUES (?, ?, ?, ?)",
                       (rate, message, recipe_id, user_id))
        conn.commit()

        cursor.execute("""
                   SELECT c.*, u.login
                   FROM comments c
                   INNER JOIN users u ON c.userId = u.Id
                   WHERE c.recipeId = ?""", recipe_id)
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        comments = [dict(zip(columns, row)) for row in rows]

        response = {
            'comment_added': True,
            'comments': comments
        }

        # Return success response
        return jsonify(response), 200
    except Exception as e:
        # Obsługa błędu
        print(e)
        return jsonify({'error': 'Wystąpił błąd podczas tworzenia komentarza.'}), 500
    finally:
        if conn:
            conn.close() # Zamknięcie połączenia z bazą danych


# Endpoint do dodania komentarza przez user'a
@app.route('/delUserComm', methods=['POST'])
def delUserComm():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # Pobranie danych rejestracji z żądania POST
        data = request.get_json()

        id = data["comment_id"]
        recipe_id = data["recipe_id"]

        # Dodanie nowego komentarza do bazy danych
        cursor.execute("DELETE FROM comments WHERE Id = ?", id)
        conn.commit()

        # Zapytanie SELECT dla pobrania wszystkich komentarzy
        cursor.execute("SELECT c.*, u.login FROM comments c INNER JOIN users u ON c.userId = u.Id WHERE c.recipeId = ?"
                       , recipe_id)
        rows = cursor.fetchall()

        # Pobranie nazw kolumn
        columns = [column[0] for column in cursor.description]

        # Konwersja wyników zapytania na listę słowników
        comments = [dict(zip(columns, row)) for row in rows]

        # Zwrócenie odpowiedzi z usuniętym komentarzem i pobranymi danymi
        response = {
            'comment_deleted': True,
            'comments': comments
        }
        # Zwrócenie odpowiedzi sukcesu
        print(response)
        return jsonify(response), 200
    except Exception as e:
        # Obsługa błędu
        print(e)
        return jsonify({'error': 'Wystąpił błąd podczas tworzenia komentarza.'}), 500
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()  # Zamknięcie połączenia z bazą danych


# Endpoint do dodania komentarza dla admina
@app.route('/addCommAdmin', methods=['POST'])
def addCommAdmin():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # Pobranie danych rejestracji z żądania POST
        data = request.get_json()

        message = data['text']
        rate = data['rate']
        recipe_id = data['recipe_id']
        user_id = data['user_id']
        isb = data['isB']

        # Dodanie nowego komentarza do bazy danych
        cursor.execute \
            ("INSERT INTO Comments (Rate,Text, isBlocked, recipeId, userId) VALUES (?, ?, ?, ?, ?)",
             (rate, message, isb, recipe_id, user_id))
        conn.commit()

        # Zwrócenie odpowiedzi sukcesu
        return jsonify({'comment added': True}), 200
    except Exception as e:
        # Obsługa błędu
        print(e)
        return jsonify({'error': 'Wystąpił błąd podczas rejestracji.'}), 500
    finally:
        conn.close()  # Zamknięcie połączenia z bazą danych


@app.route('/delRecipeAdmin', methods=['POST'])
def delRecpieAdmin():
    # Połączenie z bazą danych
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # Pobranie danych rejestracji z żądania POST
        data = request.get_json()

        id = data['recipe_id']

        # Usunięcie przepisu z bazy danych
        cursor.execute("DELETE FROM RECIPES WHERE id = ?", (id,))
        conn.commit()

        # Zwrócenie odpowiedzi sukcesu
        return jsonify({'recipe deleted': True}), 200
    except Exception as e:
        # Obsługa błędu
        print(e)
        return jsonify({'error': 'Wystąpił błąd podczas usuwania przepisu.'}), 500
    finally:
        conn.close()  # Zamknięcie połączenia z bazą danych


# main
if __name__ == '__main__':
    # Uruchomienie aplikacji Flask z obsługą HTTP
    app.run(host='0.0.0.0', port=5000)
