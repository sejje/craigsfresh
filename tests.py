import unittest
import time
from sectiontwo import Section
from listing import Listing

free = Section("http://fortmyers.craigslist.org/zip/")
all_listings = Section("http://fortmyers.craigslist.org/sss/")

class testSection(unittest.TestCase):
	def testLocale(self):
		self.assertEqual(free.get_locale(), "fortmyers")

	def testSection(self):
		self.assertEqual(free.get_section(), "zip")

	def testGetAverageTimeBetweenUpdates(self):
		free.timestamps = [800, 900]
		self.assertEqual(free.get_average_time_between_updates(), 100)

	def testGetListings(self):
		free.update()
		listings = free.get_listings(free.soup)
		self.assertEqual(len(listings), 100)

	def testGetListingsType(self):
		listings = free.get_listings(free.soup)
		self.assertTrue(isinstance(listings[0], Listing), True)

	def testGetNewListings(self):
		new_listings = free.get_new_listings()
		self.assertEqual(len(new_listings), 100)

	def testTimeBeforeUpdate(self):
		older = free.time_before_update()
		time.sleep(1)
		self.assertTrue(older > free.time_before_update())

	def testStamp(self):
		free.stamp()
		stamptime = free.timestamps[-1]
		now = time.time()
		self.assertTrue(time.time() - stamptime < 1)

	def testStampMaxLength(self):
		for i in range(25):
			free.stamp()
		self.assertEqual(len(free.timestamps), 10)

class testListing(unittest.TestCase):
	def testTitle(self):
		for listing in free.get_listings(free.soup):
			self.assertTrue(listing.title != "")

	def testURL(self):
		for listing in free.get_listings(free.soup):
			self.assertTrue(listing.url != "")
			self.assertTrue(listing.url.startswith("/"))

from sectionmanager import SectionManager as SM
sm = SM()
class testSectionManager(unittest.TestCase):
	def testLoadSections(self):
		sm.load_sections()
		self.assertTrue(len(sm.sections) > 2)

	def testCheckForNewSections(self):
		sm.load_sections()
		self.assertEqual(sm.check_for_new_sections(), ["http://notindatabase.craigslist.org/vvv/"])

	def testSectionIsLoaded(self):
		freeSection = Section("http://fortmyers.craigslist.org/zip/")
		self.assertTrue(freeSection in sm.sections)
		
	def testAddSection(self):
		newSection = Section("http://fortmyers.craigslist.org/zzz/")
		sm.add_section(newSection)
		self.assertTrue(newSection in sm.sections)

	def testUrlInSections(self):
		url = "http://fortmyers.craigslist.org/zip/"
		urltwo = "http://fortmyers.craigslist.org/vvv/"
		self.assertTrue(sm.url_in_sections(url))
		self.assertFalse(sm.url_in_sections(urltwo))

	
if __name__ == "__main__":
	unittest.main()
