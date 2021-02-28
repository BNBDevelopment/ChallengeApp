import psycopg2

class DBConnector:

    def __init__(self):
        schema = PropertiesManager.getProperty("DBSchema")
        host =  PropertiesManager.getProperty("DBHost")
        port = PropertiesManager.getProperty("DBPort")
        username = PropertiesManager.getProperty("DBUser")
        password = PropertiesManager.getProperty("DBPass")

        self.connection = psycopg2.connect(database=schema, user=username, password=password, host=host, port=port)
        print("LOG: Connected to database successfully.\n"
              "Host: " + host + "\t Port: " + port + "\n"
              "Schema: " + schema + "\t Username: " + username)


    def insert(self, dbObject):

    def update(self, dbObject):

    def delete(self, dbObject):


    def findbet(self, betId):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from Bets")
        rows = cursor.fetchall()

        for row in rows: