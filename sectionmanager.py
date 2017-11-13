from sectiontwo import Section
import time

class SectionManager():
	def __init__(self):
		self.sections = []

	def __iter__(self):
		return iter(self.sections)
		
	def get_section_list_from_database(self):
		urlone = "http://fortmyers.craigslist.org/zip/"
		urltwo = "http://fortmyers.craigslist.org/sss/"
		urlthree = "http://fortmyers.craigslist.org/pha/"
		urlfour = "http://fortmyers.craigslist.org/vga/"
		urlfive = "http://notindatabase.craigslist.org/vvv/"
		return [urlone, urltwo, urlthree, urlfour, urlfive]

	def check_for_new_sections(self):
		not_loaded = []
		for url in self.get_section_list_from_database():
			if (self.url_in_sections(url) == False):
				not_loaded.append(url)
		return not_loaded

	def url_in_sections(self, url):
		for section in self.sections:
			if section.url == url:
				return True
		return False

	def load_sections(self):
		s = Section("http://fortmyers.craigslist.org/zip/")
		x = Section("http://fortmyers.craigslist.org/sss/")
		f = Section("http://fortmyers.craigslist.org/pha/")
		v = Section("http://fortmyers.craigslist.org/vga/")
		self.sections = [s, x, f, v]

	def start_sections(self):
		for section in self.sections:
			try:
				section.start()
			except RuntimeError:
				#create new section, start it, add it?
				pass

	def add_section(self, section):
		self.sections.append(section)

	def section_is_loaded(self, section):
		return section in self.sections

	def report(self):
		sections = str(len(self.sections))
		active = str(len([section for section in self if section.is_alive()]))
		print sections + " sections, " + active + " active"

if __name__ == "__main__":
	a = SectionManager()
	a.load_sections()
	a.start_sections()
	while True:
		if (len([section for section in a if section.is_alive()]) == 0):
			exit()
		try:
			time.sleep(1)
		except:
			print "Shutting down..."
			for section in a:
				section.kill = True
