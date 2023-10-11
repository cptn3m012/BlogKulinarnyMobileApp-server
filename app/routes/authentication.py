from flask import request, jsonify, Blueprint
from app.utils.database import connect_to_database
from app.utils.hashing import HashPassword


bp = Blueprint('authentication', __name__)

# Endpoint logowania
@bp.route('/login', methods=['POST'])
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
        return jsonify({'result': True, 'user.rank': user[5], 'user.id': user[0], 'user.login': user[1],
                        'user.mail': user[3], 'user.password': user[2]})
    else:
        # Jeśli użytkownik nie istnieje, zwróć błąd 401
        return jsonify({'result': False}), 401


# Endpoint rejestracji
@bp.route('/register', methods=['POST'])
def register():
    # Połączenie z bazą danych
    server = 'sqldemodesi.database.windows.net'
    database = 'applicationDB'
    login = 'uzytkownik'
    password = 'hasloBazy123!'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"
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