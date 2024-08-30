import SQLDatabase as db

class RollCounter():
    def __init__(self, tableName):
        self._diceTables = db.DataBaseSQLite(tableName, "", '''CREATE TABLE IF NOT EXISTS D20Table(
                                               UserID INTEGER PRIMARY KEY,
                                               Roll1 INTEGER,
                                               Roll2 INTEGER,
                                               Roll3 INTEGER,
                                               Roll4 INTEGER,
                                               Roll5 INTEGER,
                                               Roll6 INTEGER,
                                               Roll7 INTEGER,
                                               Roll8 INTEGER,
                                               Roll9 INTEGER,
                                               Roll10 INTEGER,
                                               Roll11 INTEGER,
                                               Roll12 INTEGER,
                                               Roll13 INTEGER,
                                               Roll14 INTEGER,
                                               Roll15 INTEGER,
                                               Roll16 INTEGER,
                                               Roll17 INTEGER,
                                               Roll18 INTEGER,
                                               Roll19 INTEGER,
                                               Roll20 INTEGER);''')

        self._diceTables.CreateTable('''CREATE TABLE IF NOT EXISTS D12Table(
                                               UserID INTEGER PRIMARY KEY,
                                               Roll1 INTEGER,
                                               Roll2 INTEGER,
                                               Roll3 INTEGER,
                                               Roll4 INTEGER,
                                               Roll5 INTEGER,
                                               Roll6 INTEGER,
                                               Roll7 INTEGER,
                                               Roll8 INTEGER,
                                               Roll9 INTEGER,
                                               Roll10 INTEGER,
                                               Roll11 INTEGER,
                                               Roll12 INTEGER);''')

        self._diceTables.CreateTable('''CREATE TABLE IF NOT EXISTS D10Table(
                                               UserID INTEGER PRIMARY KEY,
                                               Roll1 INTEGER,
                                               Roll2 INTEGER,
                                               Roll3 INTEGER,
                                               Roll4 INTEGER,
                                               Roll5 INTEGER,
                                               Roll6 INTEGER,
                                               Roll7 INTEGER,
                                               Roll8 INTEGER,
                                               Roll9 INTEGER,
                                               Roll10 INTEGER);''')

        self._diceTables.CreateTable('''CREATE TABLE IF NOT EXISTS D8Table(
                                               UserID INTEGER PRIMARY KEY,
                                               Roll1 INTEGER,
                                               Roll2 INTEGER,
                                               Roll3 INTEGER,
                                               Roll4 INTEGER,
                                               Roll5 INTEGER,
                                               Roll6 INTEGER,
                                               Roll7 INTEGER,
                                               Roll8 INTEGER);''')

        self._diceTables.CreateTable('''CREATE TABLE IF NOT EXISTS D6Table(
                                               UserID INTEGER PRIMARY KEY,
                                               Roll1 INTEGER,
                                               Roll2 INTEGER,
                                               Roll3 INTEGER,
                                               Roll4 INTEGER,
                                               Roll5 INTEGER,
                                               Roll6 INTEGER);''')

        self._diceTables.CreateTable('''CREATE TABLE IF NOT EXISTS D4Table(
                                               UserID INTEGER PRIMARY KEY,
                                               Roll1 INTEGER,
                                               Roll2 INTEGER,
                                               Roll3 INTEGER,
                                               Roll4 INTEGER);''')

    def incrementCounter(self, dieType, discordID, dieRolled):
        RollList = []
        valuesString = "?, " + "?, " * (dieType-1) + "?"
        for num in range(dieType):
            RollList.append("Roll" + str(num + 1))

        insertionString = "({}, ".format(discordID)
        for num in range(len(RollList)):
            if not (num == len(RollList) - 1):
                insertionString = insertionString + RollList[num] + ", "

            else:
                insertionString = insertionString + RollList[num] + ")"

        table = "D" + str(dieType) + "Table"
        fetchQuery = "SELECT UserID FROM {}".format(table)
        IDlist = self._diceTables.FetchData(fetchQuery)
        idList = []
        dataList = []
        for idTuple in IDlist:
            idList.append(idTuple[0])
        if discordID in idList:
            fetchQuery = "SELECT * FROM {} WHERE UserID = {}".format(table, discordID)
            userData = self._diceTables.FetchData(fetchQuery)
            for dataTuple in userData:
                for i in range(dieType + 1):
                    dataList.append(dataTuple[i])
            arg1 = "Roll" + str(dieRolled)
            arg2 = dataList[dieRolled] + 1
            updateQuery = "UPDATE {} SET {} = {} WHERE UserID = {}".format(table, arg1, arg2, discordID)
            self._diceTables.UpdateData(updateQuery)
                    

        else:
            tempList = [discordID]
            for num in range(dieType):
                tempList.append(0)

            tempList[dieRolled] = 1
            if dieType == 4:
                insertQuery = 'INSERT INTO D4Table (UserID, Roll1, Roll2, Roll3, Roll4) values (?, ?, ?, ?, ?)'

            elif dieType == 6:
                insertQuery = 'INSERT INTO D6Table (UserID, Roll1, Roll2, Roll3, Roll4, Roll5, Roll6) values (?, ?, ?, ?, ?, ?, ?)'

            elif dieType == 8:
                insertQuery = 'INSERT INTO D8Table (UserID, Roll1, Roll2, Roll3, Roll4, Roll5, Roll6, Roll7, Roll8) values (?, ?, ?, ?, ?, ?, ?, ?, ?)'

            elif dieType == 10:
                insertQuery = 'INSERT INTO D10Table (UserID, Roll1, Roll2, Roll3, Roll4, Roll5, Roll6, Roll7, Roll8, Roll9, Roll10) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

            elif dieType == 12:
                insertQuery = 'INSERT INTO D12Table (UserID, Roll1, Roll2, Roll3, Roll4, Roll5, Roll6, Roll7, Roll8, Roll9, Roll10, Roll11, Roll12) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

            elif dieType == 20:
                insertQuery = 'INSERT INTO D20Table (UserID, Roll1, Roll2, Roll3, Roll4, Roll5, Roll6, Roll7, Roll8, Roll9, Roll10, Roll11, Roll12, Roll13, Roll14, Roll15, Roll16, Roll17, Roll18, Roll19, Roll20) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(tn=table)

            tempTuple = tuple(tempList)
            self._diceTables.InsertData(tempTuple, insertQuery)

    def getD20Count(self, discordID, dieType):
        table = "D" + str(dieType) + "Table"
        fetchQuery = "SELECT * FROM {} WHERE UserID = {}".format(table, discordID)
        resultsTuple = self._diceTables.FetchData(fetchQuery)
        diceList = []
        diceTable = []
        dataDict = {}
        for diceTuple in resultsTuple:
            for i in range(1, dieType + 1):
                diceList.append(diceTuple[i])
                appendString = str(i) + "s"
                diceTable.append(appendString)
        for num in range(dieType):
            dataDict[diceTable[num]] = diceList[num]
        dataString = ""
        for key in dataDict:
            dataString = dataString + key + ": " + str(dataDict[key]) + "\n"
        return(dataString)
                

