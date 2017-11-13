import requests
import BeautifulSoup
import sys
import time

class Sub:
	""" A sub-section on craigslist, like 'free' """
	def __init__(self, url):
		self.url = url
		self.fetch()
		self.listings = self.find_listings()

	def fetch(self):
		r = requests.get(self.url)
		self.data = BeautifulSoup.BeautifulSoup(r.text)
		self.timestamp = time.time()
		return r.status_code

	def find_listings(self):
		peas = [p for p in self.data.findAll('p', 'row')]
		listings = [Listing(link) for link in peas]
		return listings

	def new_listings(self):
		new = []
		if self.listings[0] != self.old_listings[0]:
			if self.old_listings[0] in self.listings:
				i = self.listings.index(self.old_listings[0])
				new = self.listings[:index]
		return new

class Listing:
	def __init__(self, data):
		self.title = data.find('span', 'pl').find('a').text
		self.url = data.find('span', 'pl').find('a')['href']
		if data.find('small'):
			self.location = data.find('small').text[1:-1]
		else:
			self.location = ""

	def __cmp__(self, other):
		return cmp(self.url, other.url)

s = Sub("http://fortmyers.craigslist.org/zip/")
