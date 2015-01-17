#!/usr/bin/python
# Every program has to start somewhere
import os, errno

from scheduler import Scheduler
from audioManager import AudioManager
from log import log
from time_Ambiance import *
from subprocess import call

timeSlots = dict()

def setup():
# Do some basic prep work. e.g. Generating folders
	for hour in xrange(0,24):
		timeSlots[hour] = timeStr(hour) + ':00'

	createTimeSlots()


def createTimeSlots():
	mkDir('TimeSlots')
	mkDir('TimeSlots/Day')
	mkDir('TimeSlots/Day/Songs')
	mkDir('TimeSlots/Day/Background')
	mkDir('TimeSlots/Night')
	mkDir('TimeSlots/Night/Songs')
	mkDir('TimeSlots/Night/Background')
	for hour in xrange(0,24):
		if hour > 7 and hour < 20:
			mkDir( os.path.join( 'TimeSlots/Day', timeSlots[hour] ) )
			mkDir( os.path.join( 'TimeSlots/Day', timeSlots[hour], 'Songs' ) )
			mkDir( os.path.join( 'TimeSlots/Day', timeSlots[hour], 'Background' ) )
		else:
			mkDir( os.path.join( 'TimeSlots/Night', timeSlots[hour] ) );
			mkDir( os.path.join( 'TimeSlots/Night', timeSlots[hour], 'Songs' ) );
			mkDir( os.path.join( 'TimeSlots/Night', timeSlots[hour], 'Background' ) );

def mkDir(dirName):
	try:
		os.mkdir( dirName )
		log( 'Setup', 'Created dir ' + str(dirName) )
	except Exception, e:
		if e.errno == 17:
			pass
		else:
			log('Setup', e)
			print( 'Uh-oh. Something weird occured. Check `.log` for more details')
			exit();

# - - - - - - #
# Start Here  #
# - - - - - - #

if call(['which', 'play']):
	print("'sox' is not installed or PATH is incorrectly set")
	print("Be sure to install extra libs for sox too:")
	print("	apt-get install libsox-fmt-all")
	exit(1)

log('Start', '#################################')
log('Start', '       Ambiance Launched         ')
log('Start', '#################################')
# Setup Directories
setup()
# Start the Scheduler
scheduler = Scheduler()
# Make SongQ
songQ = SongQ(timeSlots, scheduler)
# Make the AudioManager
audioManager = AudioManager(scheduler, songQ)

