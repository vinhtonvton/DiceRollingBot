import re
import random
import diceCount as dC
from datetime import date
today = date.today()
fileName = "DiceRolled"

#### NEXT: ADD FOR IF MOD = 0

diceCount = dC.RollCounter(fileName)

diceList = [4, 6, 8, 10, 12, 20]

def rollSingleDice(diceString, userID):
    if re.search("[\+]+[0-9]+$", diceString): #If adding modifier.
        diceString = diceString.strip("d")
        diceString = diceString.split("+")
        diceNumber = int(diceString[0])
        diceMod = int(diceString[1])
        dieResult = random.randint(1, diceNumber)
        total = diceMod + dieResult
        if diceNumber in diceList:
            diceCount.incrementCounter(diceNumber, userID, dieResult)
        return(dieResult, diceMod, total, diceNumber)

    elif re.search("[\-]+[0-9]+$", diceString): #If subtracting modifier.
        diceString = diceString.strip("d")
        diceString = diceString.split("-")
        diceNumber = int(diceString[0])
        diceMod = int(diceString[1]) * -1
        dieResult = random.randint(1, diceNumber)
        total = diceMod + dieResult
        return(dieResult, diceMod, total, diceNumber)
        
    else:
        diceString = diceString.strip("d")
        diceNumber = int(diceString)
        dieResult = random.randint(1, diceNumber)
        if diceNumber in diceList:
            diceCount.incrementCounter(diceNumber, userID, dieResult)
        return(dieResult, 0, dieResult, diceNumber)

def rollMultiDice(diceString, userID): #Rolling groups of dice, e.g. 4d6, 3d8. Adds modiifer at end.
    diceString = diceString.split("d")
    numOfDice = int(diceString[0])
    numRolls = 0
    result = []
    while numRolls < numOfDice:
        result.append(rollSingleDice(diceString[1], userID))
        numRolls += 1
    rolls = []
    total = 0
    for numTuple in result:
        rolls.append(int(numTuple[0]))
        total = int(numTuple[0]) + total
        numType = numTuple[3]
    total = result[0][1] + total
    mod = result[0][1]
    return(rolls, mod, total, numType)


def rollDiceGroups(diceString, userID):
    diceString = diceString.split(" ")
    numGroups = int(diceString[0])
    diceString = diceString[1]
    rolledGroups = 0
    groupResults = []
    
    while rolledGroups < numGroups:
        if re.search("[0-9]+d[0-9]+", diceString):
            groupResults.append(rollMultiDice(diceString, userID))

        else:
            groupResults.append(rollSingleDice(diceString, userID))
        rolledGroups += 1

    return(groupResults)

def parseDiceString(diceString, userID):
    results = ""
    msg = ""
    if re.search("[0-9]+ [0-9]*d[0-9]+", diceString):
        results = rollDiceGroups(diceString, userID)
        for dataTuple in results:
            dieRolls = dataTuple[0]
            dieMod = dataTuple[1]
            total = dataTuple[2]
            if type(dataTuple[0]) == list:
                msg = msg + "\nRolls: " + str(dieRolls) + "\nMod: " + str(dieMod) + "\nTotal: " + str(total)

            else:
                if dieMod >= 0:
                    msg = msg + "\nResult: " + str(total) + "(" + str(dieRolls) + "+" + str(dieMod) + ")"
                    if dieRolls == 20 and dataTuple[3] == 20:
                        msg = msg + "CRIT!"

                    elif dieRolls == 1 and dataTuple[3] == 20:
                        msg = msg + "FUMBLE!"

                else:
                    msg = msg + "\nResult: " + str(total) + "(" + str(dieRolls) + str(dieMod) + ")"
                    if dieRolls == 1 and dataTuple[3] == 20:
                        msg = msg + "FUMBLE!"

                    elif dieRolls == 20 and dataTuple[3] == 20:
                        msg = msg + "CRIT!"


    elif re.search("[0-9]+d[0-9]+", diceString):
        results = rollMultiDice(diceString, userID)
        dieRolls = results[0]
        dieMod = results[1]
        total = results[2]
        msg = "\nResult: " + str(dieRolls) + "\nMod: " + str(dieMod) + "\nTotal: " + str(total)

    elif re.search("d[0-9]+", diceString):
        results = rollSingleDice(diceString, userID)
        if (type(results)) == tuple:
            total = int(results[0]) + int(results[1])
            msg = "\nResult: " + str(results[0]) + "\nMod: " + str(results[1]) + "\nTotal: " + str(total)
            if results[0] == 20:
                msg = msg + "\nCRIT!"

            elif results[0] == 1:
                msg = msg + "\nFUMBLE!"

    return msg
        
