import mysql.connector

def getAllNewEvents():
    con = mysql.connect()
    cursor = con.cursor()
    query = ("Select * from tbl_events_log where status=false")
    cursor.execute(query)
    results = cursor.fetchall()
    eveIdList=[]
    for row in results:
        eveIdList.append(row[0].encode("utf-8"))
    cursor.close()
    con.close()
    return eveIdList

def updateEventsLog(eventids):
    con = mysql.connect()
    cursor = con.cursor()
    for k in eventids:
        query="update tbl_events_log set status=1 where event_id='"+k+"'"
        cursor.execute(query)
        con.commit()
    cursor.close()
    con.close()


def getEventDetails(eventids):
    con = mysql.connect()
    cursor = con.cursor()
    query = 'Select * from tbl_event where event_id in (' + ','.join((str(n) for n in eventids)) + ')'
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results

def createEventsWebsite_1():
     #Create an Event in Website 1 using API
     print("Info Pushed in Website 1")

def createEventsWebsite_2():
    #Create an Event in Website 2 using API
    print("Info Pushed in Website 2")

def createEventsWebsite_3():
    # Create an Event in Website 3 using API
    print("Info Pushed in Website 3")

def createEventsWebsite_4():
    # Create an Event in Website 4 using API
    print("Info Pushed in Website 4")

def createEventsWebsite_5():
    # Create an Event in Website 5 using API
    print("Info Pushed in Website 5")


list=getAllNewEvents()
EventsList=getEventDetails(list)
createEventsWebsite_1()
createEventsWebsite_2()
createEventsWebsite_3()
createEventsWebsite_4()
createEventsWebsite_5()
updateEventsLog(list)
print("Updation done")


