from flask import request, jsonify, Blueprint
from app.utils.database import connect_to_database
from app.utils.hashing import HashPassword


bp = Blueprint('user_management', __name__)


@bp.route('/update_user', methods=['POST'])
def update_user():
    # Połączenie z bazą danych
    conn = connect_to_database()

    # Pobranie danych z żądania POST
    login = request.json.get('login')
    mail = request.json.get('mail')
    user_id = request.json.get('user_id')

    # Sprawdzenie czy użytkownik o podanym mailu już istnieje
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE mail = ? AND Id != ?", (mail, user_id))
    count = cursor.fetchone()[0]

    if count > 0:
        return jsonify({'message': 'Użytkownik o podanym mailu już istnieje.'}), 400

    # Sprawdzenie czy użytkownik o podanym loginie już istnieje
    cursor.execute("SELECT COUNT(*) FROM Users WHERE login = ? AND Id != ?", (login, user_id))
    count = cursor.fetchone()[0]

    if count > 0:
        return jsonify({'message': 'Użytkownik o podanym loginie już istnieje.'}), 400

    # Zaktualizowanie danych w bazie danych
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET login=?, mail=? WHERE Id=?", (login, mail, user_id))
    conn.commit()
    conn.close()  # Zamknięcie połączenia z bazą danych

    return jsonify({'message': 'Dane użytkownika zostały zaktualizowane.'})


@bp.route('/update_password', methods=['POST'])
def update_password():
    # Połączenie z bazą danych
    conn = connect_to_database()

    # Pobranie danych z żądania POST
    user_id = request.json.get('user_id')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    cursor = conn.cursor()

    # Pobranie hasła z bazy danych
    cursor.execute("SELECT [password] FROM [dbo].[users] WHERE [Id] = ?", user_id)
    row = cursor.fetchone()
    if row is None:
        return jsonify({'message': 'Użytkownik o podanym identyfikatorze nie istnieje.'}), 400

    hashed_old_password = HashPassword(old_password)
    password = row[0]

    if hashed_old_password != password:
        return jsonify({'message': 'Podane stare hasło jest nieprawidłowe.'}), 400

    # Zaktualizowanie hasła w bazie danych
    hashed_new_password = HashPassword(new_password)
    cursor.execute("UPDATE Users SET password=? WHERE Id=?", (hashed_new_password, user_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Hasło użytkownika zostało zaktualizowane.'})



@bp.route('/delete_account', methods=['POST'])
def delete_account():
    # Połączenie z bazą danych
    conn = connect_to_database()

    # Pobranie danych z żądania POST
    user_id = request.json.get('user_id')
    password = request.json.get('password')

    cursor = conn.cursor()

    # Sprawdzenie, czy podane hasło zgadza się z hasłem w bazie danych
    cursor.execute("SELECT password FROM Users WHERE Id=?", user_id)
    row = cursor.fetchone()
    if row:
        stored_password = row.password
        hashed_passwrod = HashPassword(password)
        if hashed_passwrod != stored_password:
            return jsonify({'error': 'Podano złe hasło!'}), 400

    # Usunięcie użytkownika z bazy danych
    cursor.execute("DELETE FROM Users WHERE Id=?", user_id)
    conn.commit()
    conn.close()

    return jsonify({'message': 'Użytkownik został usunięty z bazy danych.'}), 200


# Endpoint pobierania YOUR_LOGIN_HEREow
@bp.route('/loadUsersToAccept', methods=['GET'])
def loadUsersToAccept():
    # Połączenie z bazą danych
    conn = connect_to_database()

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
@bp.route('/deleteUsersToAccept/<int:user_id>', methods=['DELETE'])
def deleteUsersToAccept(user_id):
    # Połączenie z bazą danych
    conn = connect_to_database()

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



@bp.route('/updateUserAccept', methods=['POST'])
def updateUserAccept():
    # Połączenie z bazą danych
    conn = connect_to_database()

    try:

        user_id = request.json['id']
        new_state = request.json['isAccepted']

        # Połączenie z bazą danych
        conn = connect_to_database()
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


