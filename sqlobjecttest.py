from sqlobject import *

sqlhub.processConnection = connectionForURI('sqlite:/:memory:')

class Watch(SQLObject):
	url = TextCol()
	
