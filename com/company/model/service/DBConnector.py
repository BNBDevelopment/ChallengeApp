import inspect

import psycopg2

from com.company.model.entity.Bet import Bet
from com.company.model.service import PropertiesManager


class DBConnector:

    def __init__(self):
        schema = PropertiesManager.getProperty("DBSchema")
        host =  PropertiesManager.getProperty("DBHost")
        port = PropertiesManager.getProperty("DBPort")
        username = PropertiesManager.getProperty("DBUser")
        password = PropertiesManager.getProperty("DBPass")

        print("LOG: Attempting to connect to database.")
        self.connection = psycopg2.connect(database=schema, user=username, password=password, host=host, port=port)
        print("LOG: Connected to database successfully.\n"
              "Host: " + host + "\t Port: " + port + "\n"
              "Schema: " + schema + "\t Username: " + username)


    def insert(self, dbObject):
        cursor = self.connection.cursor()

        #REQUIRES CAPITALIZATION OF FIELD NAME???
        columnsString = ""
        columnsString.join(vars(dbObject).keys(), ',')
        valuesString = ""
        valuesString.join(vars(dbObject).values(), ',')

        tableName = getattr(dbObject, "dbTableName")

        insertStatement = "INSERT INTO " + tableName + " (" + columnsString + ") VALUES(" + valuesString + ")"
        print("LOG: Executing SQL -> " + insertStatement)
        cursor.execute(insertStatement)

        #TODO: Group commits into batches to save DB space
        self.connection.commit()


    def update(self, dbObject):
        cursor = self.connection.cursor()

        tableName = getattr(dbObject, "dbTableName")
        objectId = getattr(dbObject, "id")

        settingStatments = []
        for propertyName, value in vars(dbObject).items():
            itemSetString = propertyName + " = " + value
            settingStatments.append(itemSetString)
        setStatement = "".join(settingStatments, ",")

        updateStatement = "UPDATE " + tableName + " SET " + setStatement + " WHERE Id = " + objectId
        print("LOG: Executing SQL -> " + updateStatement)
        cursor.execute(updateStatement)

        #TODO: Group commits into batches to save DB space
        self.connection.commit()


    def delete(self, dbObject):
        cursor = self.connection.cursor()

        tableName = getattr(dbObject, "dbTableName")
        objectId = getattr(dbObject, "id")

        deleteStatement = "DELETE FROM " + tableName + " WHERE Id = " + objectId

        print("LOG: Executing SQL -> " + deleteStatement)
        cursor.execute(deleteStatement)

        #TODO: Group commits into batches to save DB space
        self.connection.commit()


    def findObject(self, id, objectClass):
        cursor = self.connection.cursor()
        tableName = getattr(objectClass, "dbTableName")
        cursor.execute("SELECT * from " + tableName)
        rows = cursor.fetchall()

        matchedObject = None

        for row in rows:
            if row['Id'] == id:
                matchedObject = objectClass()
                for property in vars(objectClass).keys():
                    capitalizedPropName = property.capitalize()
                    dbValue =  row[capitalizedPropName]
                    setattr(matchedObject, property, dbValue)

        return matchedObject


    def directExecuteSQL(self, sqlStatement):
        cursor = self.connection.cursor()
        cursor.execute(sqlStatement)

        print("LOG: CAUTION! DIRECT EXECUTION OF SQL! Executing SQL -> " + sqlStatement)
        cursor.execute(sqlStatement)

        #TODO: Group commits into batches to save DB space
        self.connection.commit()

        rows = cursor.fetchall()
        return rows
