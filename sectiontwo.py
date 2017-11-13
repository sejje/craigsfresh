import threading
import requests
import time
from listing import Listing
from BeautifulSoup import BeautifulSoup as make_soup

class Section(threading.Thread):
	def __init__(self, url):
		threading.Thread.__init__(self)
		self.url = url.lower()
		self.locale = self.get_locale()
		self.section = self.get_section()
		self.soup = make_soup("")
		self.old_soup = make_soup("")
		self.kill = False
		self.timestamps = []
		self.next_update = 0

	def __iter__(self):
		return iter(self.get_listings())

	def __cmp__(self, other):
		return cmp((self.locale, self.section), (other.locale, other.section))

	def fetch(self):
		return requests.get(self.url).text

	def get_listings(self, soup):
		paragraphs_of_class_row = [x for x in soup.findAll('p', 'row')]
		listings = [Listing(x) for x in paragraphs_of_class_row]
		return listings

	def get_new_listings(self):
		old_listings = self.get_listings(self.old_soup)
		new_listings = self.get_listings(self.soup)
		return [item for item in new_listings if item not in old_listings]

	def get_locale(self):
		return self.url.split('.')[0][7:]

	def get_name(self):
		return "(" + self.locale + ")[" + self.section + "]"

	def get_section(self):
		return self.url.split('.')[2][4:-1]

	def report(self):
		print self.get_name() + " next update: " + str(int(self.next_update - time.time())) + " seconds"

	def run(self):
		while self.kill == False:
			time.sleep(1)
			if self.time_before_update() % 30 == 0:
				self.report()
			if time.time() > self.next_update:
				self.update()
				print self.get_new_listings()

	def set_next_update_time(self):
		min_update_time = 400
		max_update_time = 900

		seconds_until_update = self.get_average_time_between_updates()
		
		if seconds_until_update < min_update_time:
			seconds_until_update = min_update_time
		if seconds_until_update > max_update_time:
			seconds_until_update = max_update_time

		self.next_update = time.time() + seconds_until_update

	def get_average_time_between_updates(self):
		x = self.timestamps
		time_between_updates = [stamp - x[i - 1] for i, stamp in enumerate(x) if i > 0]

		try:
			seconds_until_update = sum(time_between_updates) / len(time_between_updates)
		except ZeroDivisionError:
			seconds_until_update = 0

		return seconds_until_update

	def stamp(self):
		self.timestamps.append(time.time())
		if len(self.timestamps) > 10:
			self.timestamps.pop(0)

	def time_before_update(self):
		time_before_update = self.next_update - time.time()
		return int(time_before_update)

	def update(self):
		self.update_soup()
		self.set_next_update_time()

	def update_soup(self):
		soup_of_section = make_soup(self.fetch())
		if soup_of_section != self.soup:
			self.old_soup = self.soup
			self.soup = soup_of_section
			self.stamp()

		else:
			self.next_update = time.time() + 60
