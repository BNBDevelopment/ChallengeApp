

class IdGenerator:

    #SQL Should have already been run in the database
    #CREATE SEQUENCE dbObjectIdSequence START 0;

    #Should be dependencyInjected
    dbConnector = DBConnector()

    def generateId(self):
        self.dbConnector.directExecuteSQL("SELECT nextval('dbObjectIdSequence');")

