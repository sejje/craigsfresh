class Listing:
	""" One 'line' from CL, an actual link of a thing for sale """
	def __init__(self, data):
		self.title = data.find('span', 'pl').find('a').text
		self.url = data.find('span', 'pl').find('a')['href']
		if data.find('small'):
			self.location = data.find('small').text[1:-1]
		else:
			self.location = ""

	def __cmp__(self, other):
		return cmp(self.url, other.url)

