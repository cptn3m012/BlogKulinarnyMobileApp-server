import pyodbc


# Funkcja do nawiązania połączenia z bazą danych
def connect_to_database():
    server = 'YOUR_SERVER_HERE'
    database = 'YOUR_DATABASE_NAME_HERE'
    login = 'YOUR_LOGIN_HERE'
    password = 'YOUR_PASSWORD_HERE'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={login};PWD={password}"
    conn = pyodbc.connect(conn_str)
    return conn