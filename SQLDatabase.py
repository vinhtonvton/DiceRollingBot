import sqlite3

class DataBaseSQLite():
    def __init__(self, databaseName, fileName, table_query):
        databaseName = databaseName + ".db"
        self._sqliteConnection = sqlite3.connect(databaseName)
        self._databaseName = databaseName
        self._filename = fileName
        self.CreateTable(table_query)
        
    def readFileAsString(self):
        with open(self._filename, 'r') as file:
            blobData = file.read()
            return blobData
        
    def CreateTable(self, table_query):
        try:
            self._sqliteConnection = sqlite3.connect(self._databaseName)
            sqlite_create_table_query = table_query
            cursor = self._sqliteConnection.cursor()
            print("Successfuly connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            self._sqliteConnection.commit()
            print("SQLite table created.")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while creating an SQLite table", error)

        finally:
            if (self._sqliteConnection):
                self._sqliteConnection.close()
    
    def InsertData(self, dataTuple, insertion_query):
        try:
            self._sqliteConnection = sqlite3.connect(self._databaseName)
            cursor = self._sqliteConnection.cursor()
            cursor.execute(insertion_query, dataTuple)
            self._sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into table", error)

        finally:
            if (self._sqliteConnection):
                self._sqliteConnection.close()
            

    def FetchData(self, fetch_query):
        self._sqliteConnection = sqlite3.connect(self._databaseName)
        cursorObj = self._sqliteConnection.cursor()
        self._sqliteConnection.cursor()
        sel = fetch_query
        cursorObj.execute(sel)
        rows = cursorObj.fetchall()
        return rows

    def DeleteData(self, delete_query):
        try:
            self._sqliteConnection = sqlite3.connect(self._databaseName)
            cursor = self._sqliteConnection.cursor()
            print("Connected to SQLite")
            cursor.execute(delete_query)
            self._sqliteConnection.commit()
            print("Record deleted successfully.")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)

        finally:
            if (self._sqliteConnection):
                self._sqliteConnection.close()

    def UpdateData(self, updateQuery):
        try:
            self._sqliteConnection = sqlite3.connect(self._databaseName)
            cursor = self._sqliteConnection.cursor()
            print("Connected to SQLite")
            cursor.execute(updateQuery)
            self._sqliteConnection.commit()
            print("Updated successfully.")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to update", error)

        finally:
            if self._sqliteConnection:
                self._sqliteConnection.close()
            

