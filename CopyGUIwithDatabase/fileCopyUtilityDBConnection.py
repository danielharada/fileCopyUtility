import sqlite3
import time

class copyUtilityDB:

    def __init__(self):
        self.makeDBConnection()
        self.createTableIfNotExist()

    def createTableIfNotExist(self):
        table_create_query = "CREATE TABLE IF NOT EXISTS copyDates (ID INTEGER PRIMARY KEY, CopyTime REAL);"
        self.cursor.execute(table_create_query)

    def retrieveLastCopyDate(self):
        last_copy_query = "SELECT CopyTime FROM copyDates WHERE ID = (SELECT MAX(ID) FROM copyDates);"
        self.cursor.execute(last_copy_query)
        query_result = self.cursor.fetchone()
        if query_result is not None:
            query_result = query_result[0]
        return query_result

    def insertNewCopyDate(self, time_stamp):
        add_new_date_query = "INSERT INTO copyDates (CopyTime) VALUES(?);"
        self.cursor.execute(add_new_date_query, (time_stamp,))
        self.connection.commit()

    def makeDBConnection(self):
        self.connection = sqlite3.connect('copyUtility.db')
        self.cursor = self.connection.cursor()

    def dropTable(self, table_name):
        drop_table_query = "DROP TABLE IF EXISTS {};".format(table_name)
        self.cursor.execute(drop_table_query)

    def closeDBConnection(self):
        self.connection.commit()
        self.connection.close()


if __name__ == '__main__':
    database = copyUtilityDB()
    no_entries = database.retrieveLastCopyDate()
    print('no_entries is', no_entries)
    database.insertNewCopyDate(100) #artbitray time stamp to test insert statement
    one_entry = database.retrieveLastCopyDate()
    print('one_entry is', one_entry)
    database.dropTable('copyDates')
    database.closeDBConnection()
    
    


