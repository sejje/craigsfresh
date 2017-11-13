import requests
import BeautifulSoup
import time
import threading
import random
from listing import Listing

class Section(threading.Thread):
	""" A sub-section on craigslist, like 'free' """

	def __init__(self, subdomain, section):
		threading.Thread.__init__(self)
		self.subdomain = subdomain
		self.section = section
		self.timestamps = []
		self.next_fetch = time.time()
		self.data = ""
		self.url = "http://" + subdomain + "/" + section + "/"
		self.fetch()
		self.old_listings = []
		self.listings = self.find_listings()
		self.kill = False
	
	def __iter__(self):
		return iter(self.find_listings())

	def __unicode__(self):
		return "Section(" + self.section + ")"

	def update(self):
		if time.time() > self.next_fetch:
			self.fetch()
			self.old_listings = self.listings
			self.listings = self.find_listings()
			self.print_new()
		else:
			time_remaining = self.next_fetch - time.time()
			#print self.section + " updating in " + str(time_remaining) + " seconds."

	def stamp(self):
		self.timestamps.append(time.time())
		if len(self.timestamps) > 10:
			self.timestamps.pop(0)

	def set_next_fetch(self, changes=False):
		z = self.timestamps
		average_diffs = [stamp - z[i - 1] for i, stamp in enumerate(z) if i > 0]
		try:
			avg_diff = sum(average_diffs) / len(average_diffs)
		except ZeroDivisionError:
			avg_diff = 0

		print self.section + " actual avg_diff: " + str(avg_diff) + " seconds"
		
		if avg_diff < 400:
			avg_diff = 400
		if avg_diff > 900:
			avg_diff = 900
		if changes:
			avg_diff -= 20

		next_fetch = time.time() + avg_diff

		print self.section + " next fetch: " + str(avg_diff) + " seconds"
		self.next_fetch = next_fetch


	def fetch(self):
		print("fetching " + self.url)
		start_time = time.time()
		r = requests.get(self.url)
		rdata = BeautifulSoup.BeautifulSoup(r.text)
		if rdata != self.data:
			print ("changes in " + self.section)
			self.data = BeautifulSoup.BeautifulSoup(r.text)
			self.stamp()
			self.set_next_fetch(True)
		else:
			self.next_fetch += 60 #try in one minute if no changes
		print "request time: " + str(time.time() - start_time)
		return r.status_code

	def find_listings(self):
		peas = [p for p in self.data.findAll('p', 'row')]
		listings = [Listing(item) for item in peas]
		return listings

	def new_listings(self, old, new):
		return [item for item in new if item not in old]

	def print_new(self):
		new = self.new_listings(self.old_listings, self.listings)
		print str(len(new)) + " new listings"
		for item in new:
			print item.title

	def run(self):
		while True:
			global killall
			if self.kill == True:
				break
			slp = 10
			time.sleep(slp)
			self.update()

if __name__ == "__main__":
	s = Section("fortmyers.craigslist.org", "zip")
	x = Section("fortmyers.craigslist.org", "sss")
	s.start()
	x.start()

	while True:
		if threading.activeCount() == 1:
			exit()
		try:
			time.sleep(1)
		except:
			s.kill = True
			a.kill = True
