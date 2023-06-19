from flask import Blueprint, jsonify, request
from db_utils import connect_to_database
from password_utils import HashPassword

auth_bp = Blueprint('auth', __name__)

# Endpoint logowania
@auth_bp.route('/login', methods=['POST'])
def login():
    # Połączenie z bazą danych
    conn = connect_to_database()

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
        return jsonify({'result': True, 'user.rank': user.rank})
    else:
        # Jeśli użytkownik nie istnieje, zwróć błąd 401
        return jsonify({'result': False}), 401


# Endpoint rejestracji

@auth_bp.route('/register', methods=['POST'])
def register():
    # Połączenie z bazą danych
    conn = connect_to_database()

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