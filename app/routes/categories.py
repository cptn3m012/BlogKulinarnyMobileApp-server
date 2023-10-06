from flask import request, jsonify, Blueprint
from app.utils.database import connect_to_database

bp = Blueprint('categories', __name__)


# Endpoint do pobierania kategorii
@bp.route('/loadCategories', methods=['GET'])
def loadCategories():
    # Połączenie z bazą danych
    conn = connect_to_database()

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


@bp.route('/updateCategoryState', methods=['POST'])
def updateCategoryState():
    # Połączenie z bazą danych
    conn = connect_to_database()

    try:
        # Otrzymujemy dane z żądania POST
        category_id = request.json['id']
        new_state = request.json['isAccepted']

        # Połączenie z bazą danych
        conn = connect_to_database()
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


@bp.route('/deleteCategory/<int:category_id>', methods=['DELETE'])
def deleteCategory(category_id):
    # Połączenie z bazą danych
    conn = connect_to_database()

    try:
        # Połączenie z bazą danych

        conn = connect_to_database()
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