#!/usr/bin/env python

import pymssql, datetime, time, socket

conn = pymssql.connect(server="", user="", password="", database="")

dtoday = str(datetime.date.today())
ttime = str(time.strftime('%H:%M:%S'))
PIID = str(socket.gethostname())
cur = conn.cursor()

def UpdateDB(State, Date, Time, ID, Num):
	stateQuery = "UPDATE CORR_STATUS SET Corr_State = %s, Entry_Date = %s, Entry_Time = %s, Unit_ID = %s WHERE Corr_Number = %s"
# 	state, date, time, id, num
	cur.execute(stateQuery, (State, Date, Time, ID, Num) )

	conn.commit()

def IsPrinted(corr):
	printedQuery = "SELECT Corr_State FROM CORR_STATUS WHERE Corr_Number = %s"
#	cur.execute('SELECT * FROM CORR_STATUS')
	cur.execute(printedQuery, (corr))
	row = cur.fetchone()
	while row:
		if str(row[0]) == 'PRINTED':
			return True
		else:
			return False
		row = cur.fetchone()

	conn.commit()
#conn.close()
