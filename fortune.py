def fortune(num, userID):
    tempMsg = f"<@{userID}>\n" + str(num) + ". "
    if num == 1:
            tempMsg += "Your rolls are going to be ass this session."

    elif num == 2:
        tempMsg += "Your rolls are going to be mid this session."

    elif num == 3:
        tempMsg += "Your rolls are going to be godly this session."

    elif num == 4:
        tempMsg += "You will roll well once and not again."

    else:
        tempMsg += "You will fail when the time comes."

    return tempMsg
