from flask import request, jsonify, Blueprint
from app.utils.database import connect_to_database


bp = Blueprint('recipes', __name__)

@bp.route('/loadRecipes', methods=['GET'])
def loadRecipes():
    # Połączenie z bazą danych
    conn = connect_to_database()

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
                uc.login AS kupa,
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
                LEFT JOIN users AS uc ON c.userId = uc.[Id]
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
                no_of_list, author_login, step_image_url, step_description, \
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
                if comment["usId"] == comment_userid and comment["text"] == comment_text and comment["rate"] == comment_rate:
                    duplicate_comment = True
                    break

            if not duplicate_comment:
                if comment_text is not None and comment_rate is not None and comment_userid is not None:
                    recipe["comments"].append({
                        "usId": comment_userid,
                        "comment_id": comment_id,
                        "login": author_login,
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


@bp.route('/loadRecipesForLoggedUser', methods=['POST'])
def loadRecipesForLoggedUser():
    # Połączenie z bazą danych
    conn = connect_to_database()

    # Pobranie identyfikatora użytkownika z danych przesłanych przez klienta
    user_id = request.json['user_id']

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
                uc.login AS kupa,
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
                LEFT JOIN users AS uc ON c.userId = uc.[Id]
                INNER JOIN (
                    SELECT
                        recipeId,
                        name
                    FROM
                        recipesCategories AS rc
                        INNER JOIN categories AS cat ON rc.categoryId = cat.id
                ) AS cat ON r.id = cat.recipeId
                INNER JOIN users AS u ON r.userId = u.[Id] WHERE u.Id = ?;
        """, (user_id,))

        recipes = []
        current_recipe_id = None
        recipe = None

        for row in cursor.fetchall():
            recipe_id, is_accepted, title, image_url, description, difficulty, avg_time, portions, user_id, \
                no_of_list, author_login, step_image_url, step_description, \
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
                if comment["usId"] == comment_userid and comment["text"] == comment_text and comment["rate"] == comment_rate:
                    duplicate_comment = True
                    break

            if not duplicate_comment:
                if comment_text is not None and comment_rate is not None and comment_userid is not None:
                    recipe["comments"].append({
                        "usId": comment_userid,
                        "comment_id": comment_id,
                        "login": author_login,
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


@bp.route('/updateRecipeState', methods=['POST'])
def updateRecipeState():
    # Połączenie z bazą danych
    conn = connect_to_database()

    try:
        # Otrzymujemy dane z żądania POST
        recipe_id = request.json['id']
        new_state = request.json['isAccepted']

        # Połączenie z bazą danych
        conn = connect_to_database()
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


@bp.route('/delRecipeAdmin', methods=['POST'])
def delRecpieAdmin():
    # Połączenie z bazą danych
    conn = connect_to_database()

    try:
        conn = connect_to_database()
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