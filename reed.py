#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from sql import UpdateDB, IsPrinted
import datetime, socket, time

GPIO.setwarnings(False)

try:
	GPIO.cleanup()
except:
	pass

# Date/Time
dtoday = str(datetime.date.today())
ttime = str(time.strftime('%H:%M:%S'))
# PI ID
piid = str(socket.gethostname())
# Corrigator Number
corr = 1
# GPIO
reed = 8
led = 3
# state
state = 'IDLE'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(reed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)

while True:
	if not GPIO.input(reed) and state == 'IDLE':
		print "[-] State: " + str(state) + " Waiting for dryer..."

	if GPIO.input(reed) and state == 'IDLE':
		# 	state, date, time, id, num
		state = 'RUNNING'
		UpdateDB(state, dtoday, ttime, piid, corr)
		print "[+] State: " + str(state) + " Switch is open. Waiting for closed."
		GPIO.output(led, True)
		sleep(1)

	if not GPIO.input(reed) and state == 'RUNNING':
		state = 'PRINT'
		UpdateDB(state, dtoday, ttime, piid, corr)
		print "[*] State: " + str(state) + " Switch is closed. READY TO PRINT!!"
		GPIO.output(led, False)
		sleep(3)
		while True:
			if IsPrinted(str(corr)):
				state = 'IDLE'
				UpdateDB('IDLE', dtoday, ttime, piid, corr)
				break
			else:
				sleep(3)
		print '\n\n[+] Label has been printed. Restarting'
		sleep(5)
try:
	GPIO.cleanup()
except:
	pass
