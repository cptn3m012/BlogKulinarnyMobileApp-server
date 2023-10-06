from flask import request, jsonify, Blueprint
from app.utils.database import connect_to_database

bp = Blueprint('comments', __name__)


# Endpoint do dodania komentarza przez user'a
@bp.route('/addUserComm', methods=['POST'])
def addUserComm():
    # Połączenie z bazą danych
    conn = connect_to_database()

    try:
        conn = connect_to_database()
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
@bp.route('/delUserComm', methods=['POST'])
def delUserComm():
    # Połączenie z bazą danych
    conn = connect_to_database()

    try:
        conn = connect_to_database()
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
@bp.route('/addCommAdmin', methods=['POST'])
def addCommAdmin():
    # Połączenie z bazą danych
    conn = connect_to_database()

    try:
        conn = connect_to_database()
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
