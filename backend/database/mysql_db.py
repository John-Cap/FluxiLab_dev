import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self, host='pta-smartlab.csir.co.za', port=3306, user="pharma", password="Pharma00!", database="pharma"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Connected to the database.")
        except Error as e:
            print(f"Database connection error: {e}")
            self.connection = None

    def ensureConnection(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()

    def fetchRecordByColumnValue(self, table_name, column_name, value):
        self.ensureConnection()
        try:
            query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
            self.cursor.execute(query, (value,)) # type: ignore
            return self.cursor.fetchone() # type: ignore
        except Error as e:
            print(f"Error fetching record: {e}")
            return None

    def getUserRow(self, org_id=None, email=None, user_id=None):
        if email:
            return self.fetchRecordByColumnValue("users", "email", email)
        elif org_id:
            return self.fetchRecordByColumnValue("users", "orgId", org_id)
        elif user_id:
            try:
                user_id = int(user_id)
            except ValueError:
                return None
            return self.fetchRecordByColumnValue("users", "id", user_id)
        return None

    def getUserId(self, org_id=None, email=None):
        user = self.getUserRow(org_id=org_id, email=email)
        return user["orgId"] if user else None # type: ignore

    def getPassword(self, org_id=None, email=None):
        user = self.getUserRow(org_id=org_id, email=email)
        return user["password"] if user else None # type: ignore
    
    def fetch_all_fumehoods(self):
        self.ensureConnection() # type: ignore
        try:
            self.cursor.execute("SELECT * FROM fumehoods") # type: ignore
            return self.cursor.fetchall() # type: ignore
        except Error as e:
            print(f"Error fetching all fumehoods: {e}")
            return []
        
    def fetch_fumehoods_by_user(self, email):
        self.ensureConnection() # type: ignore
        try:
            query = """
                SELECT f.* FROM fumehoods f
                JOIN users u ON f.userId IN (u.id, 0)
                WHERE u.email = %s AND u.active = 1
            """
            self.cursor.execute(query, (email,)) # type: ignore
            return self.cursor.fetchall() # type: ignore
        except Error as e:
            print(f"Error fetching user fumehoods: {e}")
            return []

    def assign_fumehood_to_user(self, fumehood_nr, user_id):
        self.ensureConnection() # type: ignore
        try:
            check = "SELECT userId FROM fumehoods WHERE fumehoodNr = %s"
            self.cursor.execute(check, (fumehood_nr,)) # type: ignore
            row = self.cursor.fetchone() # type: ignore
            if not row or row["userId"] != 0: # type: ignore
                return False

            update = "UPDATE fumehoods SET userId = %s WHERE fumehoodNr = %s"
            self.cursor.execute(update, (user_id, fumehood_nr)) # type: ignore
            self.connection.commit() # type: ignore
            return True
        except Error as e:
            print(f"Checkout error: {e}")
            return False
        
    def release_fumehood(self, fumehood_nr, user_id):
        self.ensureConnection() # type: ignore
        try:
            # Confirm ownership
            check = "SELECT userId FROM fumehoods WHERE fumehoodNr = %s"
            self.cursor.execute(check, (fumehood_nr,)) # type: ignore
            row = self.cursor.fetchone() # type: ignore
            if not row or row["userId"] != user_id: # type: ignore
                return False

            # Release
            update = "UPDATE fumehoods SET userId = 0 WHERE fumehoodNr = %s"
            self.cursor.execute(update, (fumehood_nr,)) # type: ignore
            self.connection.commit() # type: ignore
            return True
        except Error as e:
            print(f"Release error: {e}")
            return False

if __name__ == "__main__":
    db=MySQLDatabase()
    db.connect()
    print(
        db.getUserRow(org_id="309930")
    )