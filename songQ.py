#!/usr/bin/python
import os, errno, time
from mutagen.mp3 import MP3
# Purpose/Function:
#	Load music to be played for each hour
#	Each time slot can have any number of songs (including 0)
#	TimeSlots are subfolders in the 'TimeSlots' directory
#	PlayList class receives requests for the next song to play
#	and determines which song to play, then returns it.
#	It will only have music for the current (and next?) hour
#	loaded into a lineup (nextHourLineUp?)
#
# Notes:
# 	This class assumes all paths are full qualified
# 	and doesn't do much defensive programming against the otherwise
#
# ToDo:
# 	Create getter to return playlist info such as
# 		playlist total length and # of songs
#	Add support for multiple types of music files
#		currently only supporting mp3

class SongQ:
	songQ		= []		# Current music lineup for the hour
	nxtSongQ	= []		# Next hour's song queue
	timeSlots 	= dict()	# Stores Directory name locations for each hour
	songQIndex	= 0			# Index for songs within the queue
	
	for hour in xrange(0,24):	# Dirty way to fill the dict() 
		time = '0' + str(hour) + ':00'
		if hour > 9:
			time = time[1:]
		timeSlots[hour] = 'Slot: ' + time	# Done filling 

	def __init__(self, hour):
			self.createTimeSlots()
			self.loadLineUp(self.curHour); 
			self.hourlyUpdate() # sets us all up to get rocking

	def createTimeSlots(self):
			self.mkFile('TimeSlots')
			for hour in xrange(0,24):
				self.mkFile( os.path.join( 'TimeSlots', self.timeSlots[hour]) );

	def mkFile(self, path):
		# Attempts to make a file/dir. If it exists, fails silently
		try:
			os.mkdir( path )
		except Exception as e:
			if e.errno == 17: # File Exists Error, OK move on to next dir
				pass
			else: # Something whacky happened
				print(e)
				exit();
  
	def loadNextSongQ(self, hour):
		# Loads new songs for the given hour
		# Can load any hour, intended for the next hour 
		for curDir, subDirs, files in os.walk(os.path.join( 'TimeSlots', self.timeSlots[hour] ) ):
			for curFile in files:
				audioFile = os.path.join(curDir, curFile)
				self.nxtSongQ.append( audioFile );
				linUpTime += MP3(audioFile).info.length

	def hourlyUpdate(self):
		# Swap songQs then empty nxtSongQ
		SongQ, nxtSongQ = nxtSongQ, []
		# This one-liner took me by surprise, and is oh so satisfying

	def nextSong(self):
		if songQIndex > len(songQ) - 1:
			songQIndex = 0
		else:
			 songQIndex += 1
		return self.songQ[songQIndex];

	@property
	def getSongQInfo():
		return ( len(songQ), self.songQPlaytime() )

	def songQPlaytime(self):
		pass
